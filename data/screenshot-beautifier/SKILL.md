---
name: screenshot-beautifier
description: Beautify screenshots using ImageMagick - add rounded corners, drop shadows, gradient backgrounds, padding. Use when preparing screenshots for blog posts, documentation, or presentations. Transforms raw Playwright/browser screenshots into polished images.
allowed-tools: Read, Glob, Bash
---

# Screenshot Beautifier (ImageMagick)

Transform raw screenshots into polished, professional images with rounded corners, shadows, and backgrounds.

## Prerequisites

ImageMagick 7 must be installed:
```bash
# macOS
brew install imagemagick

# Ubuntu/Debian
apt-get install imagemagick

# Check installation
magick --version
```

## Quick Beautification Commands

### Default: macOS Window Style (RECOMMENDED)

This matches native macOS Cmd+Shift+4+Space window captures - rounded corners, soft shadow, transparent background:

```bash
INPUT="screenshot.png"
OUTPUT="screenshot_polished.png"
RADIUS=10

WIDTH=$(magick identify -format '%w' "$INPUT")
HEIGHT=$(magick identify -format '%h' "$INPUT")

# Step 1: Create rounded corner mask
magick -size ${WIDTH}x${HEIGHT} xc:black \
  -fill white -draw "roundrectangle 0,0,$((WIDTH-1)),$((HEIGHT-1)),$RADIUS,$RADIUS" \
  /tmp/mask.png

# Step 2: Apply mask to get rounded corners
magick "$INPUT" /tmp/mask.png -alpha off -compose CopyOpacity -composite /tmp/rounded.png

# Step 3: Create shadow from rounded image
magick /tmp/rounded.png -background 'rgba(0,0,0,0.35)' -shadow 100x24+0+12 /tmp/shadow.png

# Step 4: Composite on transparent background (shadow + image)
magick -size $((WIDTH+80))x$((HEIGHT+80)) xc:none \
  /tmp/shadow.png -gravity center -composite \
  /tmp/rounded.png -gravity center -composite \
  "$OUTPUT"

# Cleanup
rm /tmp/mask.png /tmp/rounded.png /tmp/shadow.png
```

For a solid background instead of transparent, change `xc:none` to `xc:'#f0f0f0'` in Step 4.

Or use the helper script:
```bash
./scripts/beautify.sh screenshot.png macos screenshot_polished.png
```

### Alternative: Rounded Corners + Shadow + White Background

```bash
INPUT="screenshot.png"
OUTPUT="screenshot_polished.png"
RADIUS=12

WIDTH=$(magick identify -format '%w' "$INPUT")
HEIGHT=$(magick identify -format '%h' "$INPUT")

# Step 1: Create mask
magick -size ${WIDTH}x${HEIGHT} xc:black \
  -fill white -draw "roundrectangle 0,0,$((WIDTH-1)),$((HEIGHT-1)),$RADIUS,$RADIUS" \
  /tmp/mask.png

# Step 2: Apply mask
magick "$INPUT" /tmp/mask.png -alpha off -compose CopyOpacity -composite /tmp/rounded.png

# Step 3: Create shadow
magick /tmp/rounded.png -background black -shadow 60x8+0+4 /tmp/shadow.png

# Step 4: Composite on white background
magick -size $((WIDTH+60))x$((HEIGHT+60)) xc:white \
  /tmp/shadow.png -gravity center -composite \
  /tmp/rounded.png -gravity center -composite \
  "$OUTPUT"

rm /tmp/mask.png /tmp/rounded.png /tmp/shadow.png
```

### Modern: Gradient Background (Purple/Blue)

```bash
INPUT="screenshot.png"
OUTPUT="screenshot_gradient.png"
RADIUS=12

WIDTH=$(magick identify -format '%w' "$INPUT")
HEIGHT=$(magick identify -format '%h' "$INPUT")
BG_WIDTH=$((WIDTH + 120))
BG_HEIGHT=$((HEIGHT + 120))

# Step 1: Create mask
magick -size ${WIDTH}x${HEIGHT} xc:black \
  -fill white -draw "roundrectangle 0,0,$((WIDTH-1)),$((HEIGHT-1)),$RADIUS,$RADIUS" \
  /tmp/mask.png

# Step 2: Apply mask
magick "$INPUT" /tmp/mask.png -alpha off -compose CopyOpacity -composite /tmp/rounded.png

# Step 3: Create shadow
magick /tmp/rounded.png -background black -shadow 80x12+0+8 /tmp/shadow.png

# Step 4: Composite on gradient background
magick -size ${BG_WIDTH}x${BG_HEIGHT} gradient:'#667eea'-'#764ba2' \
  /tmp/shadow.png -gravity center -composite \
  /tmp/rounded.png -gravity center -composite \
  "$OUTPUT"

rm /tmp/mask.png /tmp/rounded.png /tmp/shadow.png
```

### Minimal: Light Gray Background + Subtle Shadow (No Rounded Corners)

```bash
INPUT="screenshot.png"
OUTPUT="screenshot_minimal.png"

WIDTH=$(magick identify -format '%w' "$INPUT")
HEIGHT=$(magick identify -format '%h' "$INPUT")

# Step 1: Create shadow
magick "$INPUT" -background 'rgba(0,0,0,0.15)' -shadow 40x6+0+3 /tmp/shadow.png

# Step 2: Composite on light gray background
magick -size $((WIDTH+80))x$((HEIGHT+80)) xc:'#f5f5f5' \
  /tmp/shadow.png -gravity center -composite \
  "$INPUT" -gravity center -composite \
  "$OUTPUT"

rm /tmp/shadow.png
```

### Dark Mode: Dark Background + Glow

```bash
INPUT="screenshot.png"
OUTPUT="screenshot_dark.png"
RADIUS=10

WIDTH=$(magick identify -format '%w' "$INPUT")
HEIGHT=$(magick identify -format '%h' "$INPUT")
BG_WIDTH=$((WIDTH + 100))
BG_HEIGHT=$((HEIGHT + 100))

# Step 1: Create mask
magick -size ${WIDTH}x${HEIGHT} xc:black \
  -fill white -draw "roundrectangle 0,0,$((WIDTH-1)),$((HEIGHT-1)),$RADIUS,$RADIUS" \
  /tmp/mask.png

# Step 2: Apply mask
magick "$INPUT" /tmp/mask.png -alpha off -compose CopyOpacity -composite /tmp/rounded.png

# Step 3: Create purple glow shadow
magick /tmp/rounded.png -background '#4a00e0' -shadow 100x20+0+0 /tmp/shadow.png

# Step 4: Composite on dark background
magick -size ${BG_WIDTH}x${BG_HEIGHT} xc:'#1a1a2e' \
  /tmp/shadow.png -gravity center -composite \
  /tmp/rounded.png -gravity center -composite \
  "$OUTPUT"

rm /tmp/mask.png /tmp/rounded.png /tmp/shadow.png
```

## Batch Processing

Process all screenshots in a directory (shadow only, no rounded corners):

```bash
for img in screenshots/*.png; do
  OUTPUT="${img%.png}_polished.png"
  WIDTH=$(magick identify -format '%w' "$img")
  HEIGHT=$(magick identify -format '%h' "$img")

  magick "$img" -background black -shadow 60x8+0+4 /tmp/shadow.png
  magick -size $((WIDTH+60))x$((HEIGHT+60)) xc:white \
    /tmp/shadow.png -gravity center -composite \
    "$img" -gravity center -composite \
    "$OUTPUT"

  echo "Processed: $OUTPUT"
done
rm /tmp/shadow.png
```

## Parameters Explained

- **Rounded corners**: Create a black canvas with `-size WxH xc:black`, draw a white `roundrectangle` mask (format: `x1,y1,x2,y2,rx,ry`), save to temp file, then apply as alpha with `-compose CopyOpacity -composite`
- **Shadow**: `-shadow 60x8+0+4` = opacity 60%, blur 8px, offset x+0 y+4. Must be created as separate step due to ImageMagick 7 alpha channel issues
- **Multi-step approach**: ImageMagick 7 has issues with inline `\( +clone -shadow \) +swap -layers merge` when the source has transparency. Use separate temp files instead
- **Background**: Use `xc:none` for transparent, `xc:white` for solid white, `xc:'#f0f0f0'` for light gray, or `gradient:'#color1'-'#color2'` for gradients

## Common Adjustments

| Want | Change |
|------|--------|
| Larger shadow | Increase blur: `-shadow 80x12+0+8` |
| More padding | Increase extent values (e.g., `+120` instead of `+80`) |
| Sharper corners | Reduce `RADIUS` value (e.g., `8` instead of `12`) |
| Rounder corners | Increase `RADIUS` value (e.g., `20` instead of `12`) |
| Different gradient | Change colors: `gradient:'#ff6b6b'-'#feca57'` |

## Integration with Playwright Screenshots

After taking a screenshot with Playwright:

```bash
# 1. Screenshot is saved by Playwright to screenshots/raw/
# 2. Beautify it
INPUT="screenshots/raw/mlflow-traces.png"
OUTPUT="screenshots/mlflow-traces.png"
RADIUS=10

WIDTH=$(magick identify -format '%w' "$INPUT")
HEIGHT=$(magick identify -format '%h' "$INPUT")

# Create mask, apply rounded corners, create shadow, composite
magick -size ${WIDTH}x${HEIGHT} xc:black \
  -fill white -draw "roundrectangle 0,0,$((WIDTH-1)),$((HEIGHT-1)),$RADIUS,$RADIUS" \
  /tmp/mask.png

magick "$INPUT" /tmp/mask.png -alpha off -compose CopyOpacity -composite /tmp/rounded.png
magick /tmp/rounded.png -background 'rgba(0,0,0,0.35)' -shadow 100x24+0+12 /tmp/shadow.png

magick -size $((WIDTH+80))x$((HEIGHT+80)) xc:none \
  /tmp/shadow.png -gravity center -composite \
  /tmp/rounded.png -gravity center -composite \
  "$OUTPUT"

rm /tmp/mask.png /tmp/rounded.png /tmp/shadow.png

# 3. Reference the beautified version in blog posts
# ![MLflow Traces](./screenshots/mlflow-traces.png)
```

## Troubleshooting

**"magick: command not found"**
→ Install ImageMagick: `brew install imagemagick`

**Transparency not preserved**
→ Use `xc:none` for background, save as PNG

**Image too large/small after processing**
→ Adjust the canvas size in the final composite step, or add explicit resize: `-resize 1200x`

**Shadow appears wrong / image looks corrupted**
→ ImageMagick 7 has issues with inline `\( +clone -shadow \) +swap -layers merge` when the source has an alpha channel. Use the multi-step approach with temp files instead.

**Corners look folded/distorted**
→ Don't use the old polygon+circle masking technique. Use `roundrectangle` to draw proper rounded corners.
