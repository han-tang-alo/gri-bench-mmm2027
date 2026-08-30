# GRI-Bench — MMM 2027 anonymous artifacts

Anonymous supplementary material and annotation pack for the MMM 2027 submission *Directional Prompting for Gaze-Referential Inference in Large Multimodal Models*.

## Downloads

- [Supplementary PDF](supplementary.pdf)
- [GRI-Bench annotation pack (zip)](gri-bench-v1.zip)
- Unpacked pack: [`gri-bench/`](gri-bench/)

## What is in the pack

GRI-Bench is **annotation-only**. No source-dataset pixels are redistributed.

| Track | N | Join key |
|---|---:|---|
| FG-GRI | 904 | Zhang et al. Stimuli `source_relpath` |
| CG-GRI / VAT-GRI | 200 | VideoAttentionTarget `source_relpath` under `images/` |
| CG-GRI / GF-GRI | 283 | GazeFollow `source_relpath` under `test/` |

Each JSONL row has `instance_id`, `source_relpath`, candidates, label, observer box (CG-GRI), and a **human-annotated** ground-truth arrow. UniGaze rays are an experimental condition and are not included.

After you have the original images:

```bash
cd gri-bench
python materialize_images.py --fg-root /path/to/stimuli \
  --vat-root /path/to/videoattentiontarget --gf-root /path/to/gazefollow
python render_overlays.py
```

## Source image releases

- Zhang et al. Stimuli: https://huggingface.co/datasets/Zory/gaze-referent-stimuli
- VideoAttentionTarget: https://github.com/ejcgt/attention-target-detection
- GazeFollow: http://gazefollow.csail.mit.edu/download.html

## License

Our annotations, questions, derived coordinates, and scripts are CC BY 4.0.
Zhang et al. Stimuli, VideoAttentionTarget, and GazeFollow pixels stay under their original licenses.
