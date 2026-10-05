---
name: background-remover
description: Remove backgrounds from images (sprites/icons/UI) using an AI segmentation model via `rembg`, outputting transparent PNGs.
---

# Background Remover (AI / `rembg`)

Remove backgrounds from images to produce **transparent PNG** assets. This skill is optimized for **game sprites, icons, UI elements**, and other assets where you want clean alpha.

> Note: This skill uses an **AI-based** (`rembg`) segmentation model with **boundary artifact removal** post-processing.

## When to Use This Skill

Use this skill when users request:
- Remove background / make background transparent / cut out subject
- Turn a sprite sheet / icon / UI element into a transparent PNG
- Quickly get usable game assets (foreground extraction)

## What It Does

1. **Padding**: Adds a white border (100px) around the image to improve AI edge detection.
2. **AI Segmentation**: Uses `rembg` with `isnet-general-use` model to segment foreground vs background.
3. **Boundary Artifact Removal**: Crops back to original size (discarding any artifacts in the padded area), then applies:
   - Contour detection to find the main subject
   - Contour fill to preserve internal patterns
   - Edge erosion (2 iterations) to remove fine white halos
   - Gaussian blur for smooth edges
4. **Final Crop**: Removes extra transparent pixels via `getbbox()`.
5. **Output**: Writes a PNG with an **alpha channel**, leaving the original file unchanged.

## How to Use

The entry script is `scripts/remove_background.py`.

### Single File

```bash
python3 scripts/remove_background.py input.png
```

### Specify Output

```bash
python3 scripts/remove_background.py input.png -o output.png
```

### Resize Output

```bash
# Resize to exact dimensions (128x128)
python3 scripts/remove_background.py input.png -o output.png --resize 128x128

# Resize by width only (proportional height)
python3 scripts/remove_background.py input.png -o output.png --resize 256x

# Resize by height only (proportional width)
python3 scripts/remove_background.py input.png -o output.png --resize x512
```

### Batch Processing (Recommended)

The script processes **one input per run**. For batches, use your shell:

```bash
# Bash/zsh example: process all png files in a folder
for f in *.png; do
  python3 scripts/remove_background.py "$f" -o "${f%.*}_ai.png"
done
```

## CLI Parameters

- **`input`** (positional): input image path.
- **`-o, --output`** (optional): output path.
- **`--resize`** (optional): resize output image. Format: `WxH` (exact), `Wx` (width-proportional), `xH` (height-proportional). Examples: `128x128`, `256x`, `x512`.

### Default Output Naming

When `--output` is not provided, the script uses: `args.input.replace(".", "_clean.")`.

**It is strongly recommended to always pass `-o/--output`** and ensure the output ends with `.png`.

## Dependencies

Install dependencies (project/environment-specific):

```bash
python3 -m pip install rembg Pillow opencv-python numpy
```

Depending on platform, `rembg` may also require an ONNX runtime backend.

## Tips / Common Issues

- **Audio/engine note**: This skill only manipulates images; it does not touch Phaser code.
- **Halo / jagged edges**: Prefer higher-resolution source images; if needed, do a quick manual cleanup pass.
- **Wrong cutout**: Improve contrast (object vs background) or try a different source image.

## Files in This Skill

- `scripts/remove_background.py`: CLI entry.
- `references/background_removal_guide.md`: usage & troubleshooting guide.
- `assets/removal_presets.json`: legacy reference (not used by current AI pipeline).
