# Prompts

Replace `{choices}` with one candidate per line.

## FG-GRI (plain)

What is the person looking at in the image? You must choose
exactly one option from the following options:
{choices}
Please answer in the following format:
```json{"answer": "<your chosen option>", "reasoning": "<your reasoning>"}```

## CG-GRI (plain)

What is the person in the red bounding box looking at?
You must choose one from the following options:
{choices}
Please answer in the following format:
```json{"answer": "<your chosen option>", "reasoning": "<your reasoning>"}```

## Textual arrow (FG wording)

What is the person looking at in the image? The target person's gaze ray originates from pixel ({x1}, {y1}) and ends at pixel ({x2}, {y2}). The origin (0, 0) is at the top-left corner of the image.
You must choose exactly one option from the following options:
{choices}
Please answer in the following format:
```json{"answer": "<your chosen option>", "reasoning": "<your reasoning>"}```

On CG-GRI the first sentence uses “the person in the red bounding box”.
Coordinates come from `gt_arrow` (use the pixel fields).
