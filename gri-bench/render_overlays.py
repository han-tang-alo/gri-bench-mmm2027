#!/usr/bin/env python3
"""Overlay ground-truth arrows on materialized GRI-Bench RGB images.

Requires a prior run of materialize_images.py. Writes sibling folders:
  images/fg/rgb_a_gt
  images/cg/{vat,gf}_a_gt
"""
from __future__ import annotations

import argparse
import json
import math
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
SPLITS = (
    ("annotations/fg_gri.jsonl", "images/fg/rgb_a_gt"),
    ("annotations/cg_vat.jsonl", "images/cg/vat_a_gt"),
    ("annotations/cg_gf.jsonl", "images/cg/gf_a_gt"),
)


def _load_rows(rel: str) -> list[dict]:
    return [json.loads(line) for line in (HERE / rel).read_text(encoding="utf-8").splitlines() if line.strip()]


def _coord(arrow: dict, which: str, width: int, height: int) -> tuple[int, int]:
    px = arrow.get(f"pixel_{which}_x")
    py = arrow.get(f"pixel_{which}_y")
    if px is not None and py is not None:
        return int(round(float(px))), int(round(float(py)))
    x, y = float(arrow[f"{which}_x"]), float(arrow[f"{which}_y"])
    fmt = str(arrow.get("format") or "")
    if fmt == "pixels" or max(abs(x), abs(y)) > 1.5:
        return int(round(x)), int(round(y))
    return int(round(x * (width - 1))), int(round(y * (height - 1)))


def _draw_arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], width: int) -> None:
    x0, y0 = start
    x1, y1 = end
    draw.line((x0, y0, x1, y1), fill=(255, 255, 255), width=width + 4)
    draw.line((x0, y0, x1, y1), fill=(220, 20, 20), width=width)
    ang = math.atan2(y1 - y0, x1 - x0)
    length = max(12, width * 4)
    left = (x1 - length * math.cos(ang - 0.45), y1 - length * math.sin(ang - 0.45))
    right = (x1 - length * math.cos(ang + 0.45), y1 - length * math.sin(ang + 0.45))
    draw.polygon([end, left, right], fill=(220, 20, 20))


def _render_one(src: Path, dest: Path, arrow: dict) -> None:
    im = Image.open(src).convert("RGB")
    start = _coord(arrow, "start", im.width, im.height)
    end = _coord(arrow, "end", im.width, im.height)
    draw = ImageDraw.Draw(im)
    _draw_arrow(draw, start, end, width=max(3, min(im.size) // 220))
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest)


def main() -> None:
    argparse.ArgumentParser(description="Render ground-truth arrows onto materialized RGB images.").parse_args()
    n_ok = 0
    n_skip = 0
    for jsonl, gt_dir in SPLITS:
        for row in _load_rows(jsonl):
            src = HERE / row["image"]
            if not src.is_file():
                n_skip += 1
                continue
            rest = Path(*Path(row["image"]).parts[3:])
            _render_one(src, HERE / gt_dir / rest, row["gt_arrow"])
            n_ok += 1
    if n_ok == 0:
        raise SystemExit("no materialized RGB images found; run materialize_images.py first")
    print(f"rendered {n_ok} instances; skipped {n_skip} missing RGB files")


if __name__ == "__main__":
    main()
