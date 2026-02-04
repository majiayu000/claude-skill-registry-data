---
name: image-editor
description: Image processing for basic edits and color adjustments. Use this skill when users request image operations like resize, rotate, crop, flip, or color adjustments (brightness, contrast, saturation). Supports both uploaded images and images from URLs.
---

# Image Editor

## Overview

This skill provides image processing capabilities for basic editing operations and color adjustments. Use the provided Python scripts to perform operations efficiently and consistently. All scripts support both local file paths and image URLs.

## Quick Start

### Check Image Information First

Before performing operations, get image information to understand current dimensions and format:

```bash
python3 scripts/get_image_info.py <input_path_or_url>
```

This displays:
- Image format (PNG, JPEG, etc.)
- Dimensions (width x height)
- Color mode (RGB, RGBA, etc.)
- File size (for local files)

### Working with Images

All operations use the `scripts/process_image.py` script with the following pattern:

```bash
python3 scripts/process_image.py <input> <output> --operation <op_name> [operation-specific args]
```

**Input sources:**
- Local file path: `/path/to/image.jpg`
- Uploaded file: `/mnt/user-data/uploads/filename.png`
- URL: `https://example.com/image.jpg`

**Output location:**
- Save to `/mnt/user-data/outputs/` for files users should access
- Specify format via file extension (`.png`, `.jpg`, etc.) or `--format` flag

## Basic Edits

### Resize

Resize images to specific dimensions. By default, maintains aspect ratio (recommended).

**Maintain aspect ratio** (image fits within dimensions):
```bash
python3 scripts/process_image.py input.jpg output.jpg \
  --operation resize \
  --width 800 \
  --height 600 \
  --maintain-aspect
```

**Exact dimensions** (may distort):
```bash
python3 scripts/process_image.py input.jpg output.jpg \
  --operation resize \
  --width 800 \
  --height 600
```

**Common use cases:**
- Web display: 1920x1080, 1280x720, 800x600
- Thumbnails: 300x300, 200x200, 150x150
- Social media: 1200x630 (Facebook), 1080x1080 (Instagram)

### Rotate

Rotate images by any angle. Use positive values for clockwise, negative for counter-clockwise.

**90° clockwise:**
```bash
python3 scripts/process_image.py input.jpg output.jpg \
  --operation rotate \
  --angle 90
```

**Common rotations:**
- 90°: Quarter turn clockwise
- -90° or 270°: Quarter turn counter-clockwise
- 180°: Upside down

**Note:** Image dimensions change after rotation (except 180°). The script uses `expand=True` to prevent cropping.

### Crop

Crop images to a specific rectangular region using pixel coordinates (left, top, right, bottom).

```bash
python3 scripts/process_image.py input.jpg output.jpg \
  --operation crop \
  --left 100 \
  --top 50 \
  --right 500 \
  --bottom 400
```

**Coordinate system:**
- Origin (0, 0) is top-left corner
- Use `get_image_info.py` to check current dimensions first

**Examples for 1000x800 image:**
- Center square: `--left 250 --top 100 --right 750 --bottom 600`
- Left half: `--left 0 --top 0 --right 500 --bottom 800`
- Top half: `--left 0 --top 0 --right 1000 --bottom 400`

### Flip

Mirror images horizontally or vertically.

**Horizontal flip** (left-right mirror):
```bash
python3 scripts/process_image.py input.jpg output.jpg \
  --operation flip \
  --direction horizontal
```

**Vertical flip** (top-bottom mirror):
```bash
python3 scripts/process_image.py input.jpg output.jpg \
  --operation flip \
  --direction vertical
```

## Color Adjustments

All color adjustments use a `--factor` parameter:
- **< 1.0**: Decrease effect
- **= 1.0**: No change (original)
- **> 1.0**: Increase effect

Refer to `references/image_processing_guide.md` for detailed factor ranges and recommendations.

### Brightness

Adjust image brightness (lightness/darkness).

```bash
python3 scripts/process_image.py input.jpg output.jpg \
  --operation brightness \
  --factor 1.3
```

**Factor guide:**
- 0.0: Completely black
- 0.5: Half brightness (darker)
- 1.0: Original (no change)
- 1.3: 30% brighter
- 2.0: Double brightness

**Typical range:** 0.5 to 2.0
**Subtle adjustments:** ±0.2 to ±0.5

### Contrast

Adjust contrast between light and dark areas.

```bash
python3 scripts/process_image.py input.jpg output.jpg \
  --operation contrast \
  --factor 1.2
```

**Factor guide:**
- 0.0: Completely gray (no contrast)
- 0.5: Half contrast (flatter)
- 1.0: Original (no change)
- 1.5: 50% more contrast (more dramatic)
- 2.0: Double contrast

**Typical range:** 0.5 to 2.0
**Subtle adjustments:** ±0.2 to ±0.5

### Saturation

Adjust color intensity/vibrancy.

```bash
python3 scripts/process_image.py input.jpg output.jpg \
  --operation saturation \
  --factor 1.4
```

**Factor guide:**
- 0.0: Grayscale (no color)
- 0.5: Half saturation (washed out)
- 1.0: Original (no change)
- 1.4: 40% more saturated (more vibrant)
- 2.0: Double saturation

**Typical range:** 0.0 to 2.0
**Special case:** Use 0.0 to convert to grayscale

### Sharpness

Adjust image sharpness (clarity vs blur).

```bash
python3 scripts/process_image.py input.jpg output.jpg \
  --operation sharpness \
  --factor 1.5
```

**Factor guide:**
- 0.0: Maximum blur
- 0.5: Softened
- 1.0: Original (no change)
- 1.5: 50% sharper
- 2.0: Very sharp

**Typical range:** 0.5 to 2.0
**Warning:** Values >2.0 can introduce artifacts

## Format Conversion

Convert between image formats by specifying the output file extension or using `--format`.

**By file extension:**
```bash
# PNG to JPEG
python3 scripts/process_image.py input.png output.jpg --operation brightness --factor 1.0

# JPEG to PNG
python3 scripts/process_image.py input.jpg output.png --operation brightness --factor 1.0
```

**Using --format flag:**
```bash
python3 scripts/process_image.py input.png output.jpg \
  --operation brightness --factor 1.0 \
  --format JPEG \
  --quality 90
```

**Format considerations:**
- **PNG**: Lossless, supports transparency, larger files
- **JPEG**: Lossy, no transparency, smaller files, quality 1-100 (recommended: 85-95)
- **Note:** JPEG cannot save transparent images (RGBA mode). Script auto-converts to RGB with white background.

## Workflow Best Practices

### Operation Order

For best results, perform operations in this sequence:
1. Crop
2. Resize
3. Rotate/Flip
4. Color adjustments (brightness, contrast, saturation, sharpness)

### Multiple Operations

For images requiring multiple operations, apply operations sequentially:

```bash
# Example: Crop, resize, and brighten
python3 scripts/process_image.py input.jpg temp_cropped.jpg \
  --operation crop --left 100 --top 100 --right 900 --bottom 700

python3 scripts/process_image.py temp_cropped.jpg temp_resized.jpg \
  --operation resize --width 800 --height 600 --maintain-aspect

python3 scripts/process_image.py temp_resized.jpg /mnt/user-data/outputs/final.jpg \
  --operation brightness --factor 1.2
```

### Preserving Originals

Always save to a new filename to preserve the original image. Use descriptive output names:
- `image_resized.jpg`
- `image_bright.jpg`
- `image_final.jpg`

### Handling URLs

For images from URLs, download and process in one step:

```bash
python3 scripts/process_image.py \
  "https://example.com/photo.jpg" \
  /mnt/user-data/outputs/processed.jpg \
  --operation resize \
  --width 800 \
  --height 600 \
  --maintain-aspect
```

## Common Request Patterns

**"Make this image brighter"**
→ Use brightness adjustment with factor 1.2-1.5

**"Resize this for the web"**
→ Use resize with --maintain-aspect and appropriate dimensions (e.g., 1280x720)

**"Rotate this 90 degrees"**
→ Use rotate with --angle 90

**"Convert this PNG to JPEG"**
→ Use any operation with .jpg output extension

**"Make this image grayscale"**
→ Use saturation with --factor 0.0

**"Crop out the background"**
→ Check dimensions first, then use crop with appropriate coordinates

**"Make the colors more vibrant"**
→ Use saturation with factor 1.3-1.5

## Dependencies

The scripts require:
- Python 3
- Pillow (PIL fork)
- requests (for URL support)

Install if needed:
```bash
pip install Pillow requests --break-system-packages
```

## Resources

### scripts/process_image.py
Main image processing script supporting all basic edits and color adjustments. Handles both local files and URLs.

### scripts/get_image_info.py
Utility script to display image information (format, dimensions, mode, file size).

### references/image_processing_guide.md
Comprehensive reference with detailed explanations of:
- Color adjustment factor ranges and recommendations
- Image format comparisons (PNG vs JPEG)
- Resize guidelines and best practices
- Rotation and coordinate systems
- Workflow optimization tips

Load this reference when users need detailed guidance on parameters or when providing recommendations for adjustments.
