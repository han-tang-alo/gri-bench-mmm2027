#!/usr/bin/env python3
"""Copy GRI-Bench frames from local source-dataset trees. Do not publish those files.

Join key in each JSONL row is source_relpath:
  FG-GRI: Zhang et al. Stimuli relative path
  VAT-GRI: path under the VideoAttentionTarget images/ tree
  GF-GRI: path under the GazeFollow test/ tree
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw

def _pack_root() -> Path:
    here = Path(__file__).resolve().parent
    if (here / "annotations").is_dir():
        return here
    nested = here / "gri-bench"
    if (nested / "annotations").is_dir():
        return nested
    raise SystemExit("run this script from the unpacked gri-bench directory")


HERE = _pack_root()


def _load_rows(jsonl_name: str) -> list[dict]:
    path = HERE / "annotations" / jsonl_name
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _resolve(src_root: Path, rel: str, extras: list[Path] | None = None) -> Path | None:
    candidates = [src_root / rel]
    parts = Path(rel).parts
    if parts:
        candidates.append(src_root / Path(*parts[1:]))
        candidates.append(src_root / Path(rel).name)
    if extras:
        candidates.extend(extras)
    for cand in candidates:
        if cand.is_file():
            return cand
    return None


def _box_xyxy(row: dict, width: int, height: int) -> tuple[int, int, int, int] | None:
    box = row.get("head_bbox") or {}
    if not box:
        return None
    x0, y0, x1, y1 = (float(box[k]) for k in ("x_min", "y_min", "x_max", "y_max"))
    if str(row.get("head_bbox_format") or "").lower() == "normalized" or max(x0, y0, x1, y1) <= 1.5:
        x0, x1 = x0 * width, x1 * width
        y0, y1 = y0 * height, y1 * height
    return tuple(int(round(v)) for v in (x0, y0, x1, y1))


def _draw_observer_box(image_path: Path, row: dict) -> None:
    im = Image.open(image_path).convert("RGB")
    xyxy = _box_xyxy(row, im.width, im.height)
    if xyxy is None:
        return
    draw = ImageDraw.Draw(im)
    draw.rectangle(xyxy, outline=(220, 20, 20), width=max(3, min(im.size) // 180))
    im.save(image_path)


def _copy_split(
    jsonl_name: str,
    src_root: Path,
    *,
    stamp_box: bool,
    limit: int,
    check_only: bool,
) -> int:
    missing: list[str] = []
    n = 0
    rows = _load_rows(jsonl_name)
    if limit:
        rows = rows[:limit]
    for row in rows:
        src = _resolve(src_root, row["source_relpath"])
        if src is None:
            missing.append(f"{row['instance_id']} {row['source_relpath']}")
            continue
        if not check_only:
            dest = HERE / row["image"]
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            if stamp_box:
                _draw_observer_box(dest, row)
        n += 1
    if missing:
        raise SystemExit(f"{jsonl_name}: missing {len(missing)} files, e.g. {missing[0]}")
    return n


def main() -> None:
    ap = argparse.ArgumentParser(description="Materialize GRI-Bench images from source datasets.")
    ap.add_argument("--fg-root", type=Path, help="Zhang et al. Stimuli root (joined by source_relpath)")
    ap.add_argument("--vat-root", type=Path, help="VideoAttentionTarget root (contains images/)")
    ap.add_argument("--gf-root", type=Path, help="GazeFollow root (contains test/)")
    ap.add_argument("--limit", type=int, default=0, help="optional cap per split")
    ap.add_argument("--check", action="store_true", help="resolve join keys only; do not copy")
    args = ap.parse_args()
    wrote = False
    kw = dict(limit=args.limit, check_only=args.check)
    if args.fg_root:
        print("FG", _copy_split("fg_gri.jsonl", args.fg_root, stamp_box=False, **kw))
        wrote = True
    if args.vat_root:
        print("VAT", _copy_split("cg_vat.jsonl", args.vat_root, stamp_box=True, **kw))
        wrote = True
    if args.gf_root:
        print("GF", _copy_split("cg_gf.jsonl", args.gf_root, stamp_box=True, **kw))
        wrote = True
    if not wrote:
        raise SystemExit("pass --fg-root and/or --vat-root and/or --gf-root")


if __name__ == "__main__":
    main()
