---
name: remove-background
description: "Remove background from images using AI (rembg / U²-Net). Use this skill whenever the user asks to: remove background, cut out object, make transparent background, delete background, extract subject, remove bg, убрать фон, удалить фон, вырезать объект, сделать прозрачный фон, фон убрать, без фона, отделить от фона, background removal, cutout, transparent PNG, isolate subject, or any variation of removing/replacing image backgrounds. Also trigger when user mentions rembg, u2net, or background eraser."
---

# Remove Background

AI-powered background removal from images using rembg (U²-Net neural network).

## How It Works

The skill uses `remove_bg.py` (in the same directory as this SKILL.md) that wraps the `rembg` library. The script auto-installs dependencies if missing.

## Quick Start

For most requests, just run:

```bash
python <skill-dir>/remove_bg.py "<input_image>" "<output_image>"
```

Replace `<skill-dir>` with the actual path to this skill's directory (the folder containing this SKILL.md).

## Available Models

| Model | Speed | Quality | Best for |
|---|---|---|---|
| `u2net` (default) | Medium | High | General purpose — objects, products, people |
| `u2netp` | Fast | Good | Quick previews, batch processing |
| `u2net_human_seg` | Medium | High | People, portraits, full-body shots |
| `isnet-general-use` | Medium | High | Complex scenes, fine details |

Use `--model` flag to select: `--model u2net_human_seg`

## Output Formats

| Format | Flag | Result |
|---|---|---|
| Transparent PNG | `--format png` (default) | Subject on transparent background |
| White background | `--format white` | Subject on solid white |
| Black background | `--format black` | Subject on solid black |

## Advanced Options

- `--alpha-matting` — Enables alpha matting for cleaner edges on hair, fur, and fine details. Slower but better quality.

## Workflow

1. Identify the input image path (from user upload or workspace)
2. Decide on model — use `u2net` by default, `u2net_human_seg` for people
3. Run the script:
   ```bash
   python <skill-dir>/remove_bg.py "/path/to/input.jpg" "/path/to/output.png" --model u2net --format png
   ```
4. Save output to the workspace folder so the user can access it
5. Show the result to the user with a computer:// link

## Batch Processing

For multiple images, run in a loop:

```bash
for img in /path/to/images/*.jpg; do
    python <skill-dir>/remove_bg.py "$img" --format png
done
```

Output files are saved as `<original_name>_nobg.png` by default.

## First Run

The first run downloads the U²-Net model (~170MB). Subsequent runs are instant since the model is cached. If `rembg` is not installed, the script auto-installs it.

## Troubleshooting

- **Slow first run**: Model download, normal — subsequent runs are fast
- **Poor edges on hair/fur**: Add `--alpha-matting`
- **Memory issues on large images**: Resize first with Pillow, then remove background
- **Wrong subject detected**: Try `isnet-general-use` model
