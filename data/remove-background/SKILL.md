---
name: remove-background
description: Remove backgrounds from images using rembg (local AI model). Use when user asks to remove background, make transparent, or cut out subjects from images.
---

# Remove Background Skill

## When to Use This Skill

- User asks to remove background from an image
- User wants to make an image transparent
- User needs to cut out a subject from a photo
- User wants to process multiple images for background removal

## Prerequisites

- Python 3.8+ installed
- Run setup once: `pip install "rembg[cpu]"` (or `rembg[gpu]` for NVIDIA GPU)

## How It Works

1. User provides image path(s) or glob pattern
2. Run rembg to remove backgrounds
3. Save transparent PNG files with `_nobg` suffix

## Procedure

```bash
# Install rembg (first time only)
pip install "rembg[cpu]"

# Remove background from single image
rembg i input.png output.png

# Process multiple images
for f in *.png; do rembg i "$f" "${f%.png}_nobg.png"; done

# Process entire folder
rembg p input_folder output_folder
```

## Options

- `-m MODEL` - Use specific model (u2net, u2netp, u2net_human_seg, silueta, isnet-general-use, isnet-anime)
- `-a` - Alpha matting for better edges
- `-ae` - Alpha matting foreground erosion size
- `-om` - Only output the mask

## Models

- `u2net` (default) - General purpose, good quality
- `u2netp` - Lightweight, faster but lower quality
- `u2net_human_seg` - Optimized for human subjects
- `silueta` - Good for portraits
- `isnet-general-use` - High quality general purpose
- `isnet-anime` - Optimized for anime/cartoon images

## Examples

**User**: "Remove background from player.png"

**Expected behavior**:
1. Run `rembg i player.png player_nobg.png`
2. Report success and output path

**User**: "Remove backgrounds from all images in the characters folder"

**Expected behavior**:
1. Run `rembg p characters/ characters_nobg/`
2. Or loop: `for f in characters/*.png; do rembg i "$f" "${f%.png}_nobg.png"; done`
3. Report number of images processed

**User**: "Remove background from this anime character"

**Expected behavior**:
1. Use anime-optimized model: `rembg i -m isnet-anime input.png output.png`
2. Report success
