# GRI-Bench (MMM 2027)

Annotation pack only. **No images are redistributed.** Recover frames from the
three source datasets using `source_relpath`, then optionally overlay the
released ground-truth arrows.

| Track | N | Join key |
|---|---:|---|
| FG-GRI | 904 | Zhang et al. Stimuli `source_relpath`. Three source images omitted. |
| CG-GRI / VAT-GRI | 200 | VideoAttentionTarget `source_relpath` under `images/`. |
| CG-GRI / GF-GRI | 283 | GazeFollow `source_relpath` under `test/`. |

## Source datasets

Obtain the original images from these official releases, then run the
materialize script. This pack does not redistribute those pixels.

- **Zhang et al. Stimuli** (FG-GRI): https://huggingface.co/datasets/Zory/gaze-referent-stimuli
- **VideoAttentionTarget** (CG-GRI / VAT): https://github.com/ejcgt/attention-target-detection
- **GazeFollow** (CG-GRI / GF): http://gazefollow.csail.mit.edu/download.html

All 1,387 items are **test-only**. There is no train split.

```bash
python materialize_images.py --check --fg-root /path/to/stimuli \
  --vat-root /path/to/videoattentiontarget --gf-root /path/to/gazefollow
python materialize_images.py --fg-root /path/to/stimuli \
  --vat-root /path/to/videoattentiontarget --gf-root /path/to/gazefollow
python render_overlays.py
```

`materialize_images.py` writes clean RGB to the `image` path in each JSONL row.
On CG-GRI it also draws the unfilled red observer box used in every condition.
`render_overlays.py` then writes ground-truth arrow images. UniGaze rays are
an experimental condition, not part of this annotation pack.

## Files

- `annotations/*.jsonl` — questions, labels, observer boxes, GT arrow coordinates, source paths
- `arrows/` — the same ground-truth rays, keyed by `instance_id`
- `prompts.md` — FG / CG / textual-arrow stems
- `materialize_images.py` — copy frames from a local Zhang / VAT / GazeFollow tree
- `render_overlays.py` — draw GT arrows on those frames

Each JSONL row has `instance_id` (track prefix + `source_relpath`),
`source_relpath`, `image` (destination after materialize), `candidates`,
`label`, and `question`. Scoring is case-insensitive exact match of the model
`answer` against `label`. The pack does not include our internal stimulus IDs.

## License

Our annotations, questions, derived coordinates, and scripts are **CC BY 4.0**.
Zhang et al. Stimuli, VideoAttentionTarget, and GazeFollow pixels stay under
their original licenses. Do not upload those images with this pack.

## Contact

Anonymous MMM 2027 submission. A camera-ready author list and DOI will
replace this line upon publication.
