---
name: image-manipulator
description: Expert in image manipulation using ImageMagick. Handles rotation, resizing, cropping, format conversion, filters, watermarks, batch processing, and advanced transformations.
---

# Image Manipulator Skill

Expert in image manipulation and transformation using ImageMagick command-line tools.

## Core Capabilities

- **Rotation & Orientation:** Rotate, flip, auto-orient images
- **Resizing & Scaling:** Resize, scale, thumbnail generation with aspect ratio preservation
- **Cropping:** Crop to specific dimensions or percentages
- **Format Conversion:** Convert between formats (JPG, PNG, WEBP, GIF, PDF, etc.)
- **Quality & Compression:** Adjust quality, optimize file size
- **Filters & Effects:** Blur, sharpen, grayscale, sepia, edge detection
- **Watermarks & Overlays:** Add text or image watermarks
- **Batch Processing:** Process multiple images with same operations
- **Metadata:** View and edit EXIF data
- **Advanced:** Color adjustments, transformations, distortions

## When to Use This Skill

Use this skill when users request:
- "Rotate this image 90 degrees"
- "Resize image to 800x600"
- "Convert PNG to JPG"
- "Add watermark to image"
- "Crop this image"
- "Make image grayscale"
- "Batch resize all images in folder"
- "Compress image to reduce file size"

## Prerequisites

### Installation

**macOS:**
```bash
brew install imagemagick
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install imagemagick
```

**Verification:**
```bash
magick -version
```

### ImageMagick Version Differences

**ImageMagick 7+ (RECOMMENDED):**
- Use `magick` command for all operations
- Example: `magick input.jpg -resize 50% output.jpg`

**ImageMagick 6 (Legacy):**
- Uses `convert` command
- Example: `magick input.jpg -resize 50% output.jpg`

**Note:** This skill uses ImageMagick 7 syntax (`magick`) throughout. If you have ImageMagick 6, replace `magick` with `convert` in all commands.

## Basic Operations

### 1. Rotation

**Rotate by specific angle:**
```bash
# Rotate 90 degrees clockwise
magick input.jpg -rotate 90 output.jpg

# Rotate 10 degrees clockwise
magick input.jpg -rotate 10 output.jpg

# Rotate counter-clockwise (negative angle)
magick input.jpg -rotate -45 output.jpg

# Rotate with white background fill
magick input.jpg -background white -rotate 15 output.jpg

# Rotate with transparent background (PNG)
magick input.png -background none -rotate 30 output.png
```

**Flip/Mirror:**
```bash
# Flip vertically
magick input.jpg -flip output.jpg

# Flip horizontally (mirror)
magick input.jpg -flop output.jpg

# Auto-orient based on EXIF data
magick input.jpg -auto-orient output.jpg
```

### 2. Resizing & Scaling

**Resize to exact dimensions:**
```bash
# Resize to 800x600 (may distort)
magick input.jpg -resize 800x600! output.jpg

# Resize maintaining aspect ratio (fit within 800x600)
magick input.jpg -resize 800x600 output.jpg

# Resize width only (height auto)
magick input.jpg -resize 800x output.jpg

# Resize height only (width auto)
magick input.jpg -resize x600 output.jpg

# Resize by percentage
magick input.jpg -resize 50% output.jpg
```

**Thumbnail generation:**
```bash
# Create thumbnail (max 200x200, preserve aspect ratio)
magick input.jpg -thumbnail 200x200 thumbnail.jpg

# Create square thumbnail (crop to center)
magick input.jpg -thumbnail 200x200^ -gravity center -extent 200x200 thumbnail.jpg
```

**Scale (faster, lower quality):**
```bash
# Quick scale for previews
magick input.jpg -scale 50% preview.jpg
```

### 3. Cropping

**Crop to dimensions:**
```bash
# Crop 800x600 from top-left corner
magick input.jpg -crop 800x600+0+0 output.jpg

# Crop 800x600 starting at position (100,50)
magick input.jpg -crop 800x600+100+50 output.jpg

# Crop from center
magick input.jpg -gravity center -crop 800x600+0+0 output.jpg

# Crop by percentage (50% of original)
magick input.jpg -crop 50%x50%+0+0 output.jpg
```

**Auto-crop (remove borders):**
```bash
# Remove white borders
magick input.jpg -fuzz 10% -trim output.jpg

# Remove borders and add 10px padding
magick input.jpg -fuzz 10% -trim +repage -bordercolor white -border 10 output.jpg
```

### 4. Format Conversion

**Convert between formats:**
```bash
# PNG to JPG
magick input.png output.jpg

# JPG to PNG
magick input.jpg output.png

# Any format to WEBP
magick input.jpg -quality 80 output.webp

# PDF to JPG (first page)
magick input.pdf[0] output.jpg

# Multiple images to PDF
magick image1.jpg image2.jpg image3.jpg output.pdf

# GIF to individual frames
magick animation.gif frame-%03d.png
```

**Quality settings:**
```bash
# High quality JPG
magick input.jpg -quality 95 output.jpg

# Compressed JPG
magick input.jpg -quality 60 output.jpg

# PNG compression
magick input.png -quality 85 output.png

# WEBP with quality
magick input.jpg -quality 80 output.webp
```

### 5. Filters & Effects

**Grayscale & Sepia:**
```bash
# Convert to grayscale
magick input.jpg -colorspace Gray output.jpg

# Sepia tone
magick input.jpg -sepia-tone 80% output.jpg
```

**Blur & Sharpen:**
```bash
# Blur (radius x sigma)
magick input.jpg -blur 0x8 output.jpg

# Gaussian blur
magick input.jpg -gaussian-blur 5x2 output.jpg

# Sharpen
magick input.jpg -sharpen 0x1 output.jpg

# Unsharp mask (radius x sigma + amount + threshold)
magick input.jpg -unsharp 0x5+0.5+0 output.jpg
```

**Edge & Enhance:**
```bash
# Edge detection
magick input.jpg -edge 1 output.jpg

# Enhance (reduce noise)
magick input.jpg -enhance output.jpg

# Contrast stretch
magick input.jpg -contrast-stretch 0 output.jpg
```

**Brightness & Contrast:**
```bash
# Increase brightness (+20)
magick input.jpg -modulate 120 output.jpg

# Decrease brightness (-20)
magick input.jpg -modulate 80 output.jpg

# Adjust contrast
magick input.jpg -contrast output.jpg
magick input.jpg +contrast output.jpg  # Reduce

# Auto-level (normalize)
magick input.jpg -auto-level output.jpg
```

**Color adjustments:**
```bash
# Negate (invert colors)
magick input.jpg -negate output.jpg

# Posterize (reduce colors)
magick input.jpg -posterize 8 output.jpg

# Adjust saturation (+50%)
magick input.jpg -modulate 100,150 output.jpg

# Desaturate (-50%)
magick input.jpg -modulate 100,50 output.jpg
```

### 6. Watermarks & Overlays

**Text watermark:**
```bash
# Simple text watermark
magick input.jpg -gravity southeast -pointsize 30 -fill white \
  -annotate +10+10 "Copyright 2025" output.jpg

# Text with shadow
magick input.jpg -gravity southeast -pointsize 40 -fill white \
  -stroke black -strokewidth 2 -annotate +20+20 "Watermark" output.jpg

# Semi-transparent text
magick input.jpg -gravity center -pointsize 60 -fill "rgba(255,255,255,0.5)" \
  -annotate +0+0 "DRAFT" output.jpg
```

**Image watermark:**
```bash
# Overlay logo (bottom-right)
magick input.jpg logo.png -gravity southeast -geometry +10+10 \
  -composite output.jpg

# Semi-transparent overlay
magick input.jpg \( logo.png -alpha set -channel A -evaluate multiply 0.5 +channel \) \
  -gravity center -composite output.jpg
```

### 7. Borders & Frames

**Add borders:**
```bash
# Simple border
magick input.jpg -border 10x10 -bordercolor black output.jpg

# Colored border
magick input.jpg -border 20x20 -bordercolor "#FF5733" output.jpg

# Frame with shadow
magick input.jpg -mattecolor gray -frame 10x10+5+5 output.jpg
```

### 8. Batch Processing

**Process multiple images:**
```bash
# Resize all JPGs in directory
for img in *.jpg; do
  magick "$img" -resize 800x600 "resized_$img"
done

# Convert all PNGs to JPG
for img in *.png; do
  magick "$img" "${img%.png}.jpg"
done

# Add watermark to all images
for img in *.jpg; do
  magick "$img" -gravity southeast -pointsize 30 -fill white \
    -annotate +10+10 "© 2025" "watermarked_$img"
done
```

**Mogrify (in-place editing):**
```bash
# Resize all JPGs in place (overwrites originals!)
mogrify -resize 800x600 *.jpg

# Convert format in place
mogrify -format png *.jpg

# Rotate all images
mogrify -rotate 90 *.jpg
```

### 9. Image Information

**Get image details:**
```bash
# Basic info
identify input.jpg

# Detailed info
identify -verbose input.jpg

# Specific properties
identify -format "%wx%h" input.jpg  # Width x Height
identify -format "%b" input.jpg     # File size
identify -format "%m" input.jpg     # Format

# EXIF data
identify -format "%[EXIF:*]" input.jpg
```

### 10. Advanced Operations

**Combine images:**
```bash
# Append horizontally
magick image1.jpg image2.jpg +append output.jpg

# Append vertically
magick image1.jpg image2.jpg -append output.jpg

# Create montage/grid
montage *.jpg -tile 3x3 -geometry +5+5 montage.jpg
```

**Transparency:**
```bash
# Make white background transparent
magick input.jpg -transparent white output.png

# Make specific color transparent
magick input.jpg -fuzz 10% -transparent "#FFFFFF" output.png

# Add alpha channel
magick input.jpg -alpha set output.png
```

**Perspective & Distortion:**
```bash
# Perspective distortion
magick input.jpg -distort Perspective "0,0 20,60  90,0 70,63  0,90 5,83  90,90 85,88" output.jpg

# Barrel distortion
magick input.jpg -distort Barrel "0.0 0.0 -0.3" output.jpg
```

## Common Workflows

### Workflow 1: Prepare Image for Web

```bash
# Resize, compress, and optimize for web
magick input.jpg \
  -resize 1200x1200 \
  -quality 85 \
  -strip \
  output.jpg
```

**Explanation:**
- Resize to max 1200x1200 (maintains aspect ratio)
- Set quality to 85% (good balance)
- Strip metadata to reduce file size

### Workflow 2: Create Thumbnail Gallery

```bash
# Create thumbnails
for img in *.jpg; do
  magick "$img" -thumbnail 200x200^ -gravity center -extent 200x200 "thumb_$img"
done

# Create montage
montage thumb_*.jpg -tile 5x -geometry +2+2 gallery.jpg
```

### Workflow 3: Batch Straighten Scanned Documents

```bash
# Deskew (auto-straighten) all scans
for img in scan_*.jpg; do
  magick "$img" -deskew 40% "straight_$img"
done
```

### Workflow 4: Add Copyright to All Photos

```bash
# Add semi-transparent copyright text
for img in photo_*.jpg; do
  magick "$img" \
    -gravity southeast \
    -pointsize 24 \
    -fill "rgba(255,255,255,0.7)" \
    -annotate +10+10 "© 2025 Your Name" \
    "copyright_$img"
done
```

### Workflow 5: Convert and Optimize for Email

```bash
# Resize to email-friendly size and compress
magick large_image.jpg \
  -resize 800x800 \
  -quality 70 \
  -strip \
  email_image.jpg
```

## Best Practices

### 1. Preserve Originals

Always work on copies or use different output names:
```bash
# Good
magick original.jpg -resize 50% resized.jpg

# Risky (overwrites original with mogrify)
mogrify -resize 50% original.jpg
```

### 2. Quality Settings

- **High quality:** `-quality 95` (large files)
- **Good quality:** `-quality 85` (recommended for web)
- **Acceptable:** `-quality 70-80` (smaller files)
- **Low quality:** `-quality 60` (very small, visible artifacts)

### 3. Format Selection

- **JPG:** Photos, images with gradients (lossy compression)
- **PNG:** Images with transparency, sharp edges, text (lossless)
- **WEBP:** Modern web format (better compression than JPG/PNG)
- **GIF:** Simple animations, limited colors
- **TIFF:** Professional/archival (lossless, large files)

### 4. Aspect Ratio

- Use `-resize WxH` (without `!`) to maintain aspect ratio
- Use `-resize WxH!` to force exact dimensions (may distort)
- Use `-thumbnail` for better quality small images

### 5. Background Color

When rotating with transparent areas:
- JPG: Use `-background white` (no transparency support)
- PNG: Use `-background none` (preserve transparency)

### 6. Performance

- Use `-strip` to remove metadata and reduce file size
- Use `-thumbnail` instead of `-resize` for small images (faster)
- Use `-scale` for quick previews (lower quality, much faster)
- Consider batch processing at night for large operations

## Common Use Cases

### Passport/ID Photo Processing

```bash
# Straighten scanned passport
magick passport_scan.jpg -rotate 10 -background white straightened.jpg

# Crop to passport photo
magick photo.jpg -crop 600x600+100+50 passport_photo.jpg

# Resize to standard passport size (2x2 inches at 300 DPI = 600x600 pixels)
magick photo.jpg -resize 600x600! -quality 95 passport.jpg
```

### Social Media Optimization

```bash
# Instagram square (1080x1080)
magick photo.jpg -resize 1080x1080^ -gravity center -extent 1080x1080 instagram.jpg

# Facebook cover (820x312)
magick banner.jpg -resize 820x312! facebook_cover.jpg

# Twitter header (1500x500)
magick header.jpg -resize 1500x500! twitter_header.jpg
```

### Document Scanning

```bash
# Enhance scanned document
magick scan.jpg \
  -deskew 40% \
  -auto-level \
  -sharpen 0x1 \
  -quality 90 \
  enhanced_scan.jpg

# Convert to PDF
magick scan_page1.jpg scan_page2.jpg scan_page3.jpg document.pdf
```

## Troubleshooting

### "convert: not found"

**Solution:**
```bash
# Check if ImageMagick is installed
which convert

# Install if missing
brew install imagemagick  # macOS
sudo apt-get install imagemagick  # Ubuntu
```

### ImageMagick 7+ Command Differences

ImageMagick 7 uses `magick` instead of `convert`:
```bash
# ImageMagick 6
magick input.jpg output.png

# ImageMagick 7 (both work)
magick input.jpg output.png
magick magick input.jpg output.png
```

### Large File Processing

For very large images:
```bash
# Limit memory usage
magick -limit memory 256MiB -limit map 512MiB input.jpg output.jpg

# Use streaming for huge files
stream -map rgb -storage-type char input.jpg output.rgb
```

### Permission Errors with PDFs

Edit `/etc/ImageMagick-6/policy.xml` (or similar) and comment out PDF restrictions:
```xml
<!-- <policy domain="coder" rights="none" pattern="PDF" /> -->
```

## Quick Reference

### Rotation
```bash
magick input.jpg -rotate 90 output.jpg           # Clockwise 90°
magick input.jpg -rotate -45 output.jpg          # Counter-clockwise 45°
magick input.jpg -flip output.jpg                # Vertical flip
magick input.jpg -flop output.jpg                # Horizontal flip
```

### Resize
```bash
magick input.jpg -resize 800x600 output.jpg      # Fit in 800x600
magick input.jpg -resize 50% output.jpg          # Scale to 50%
magick input.jpg -thumbnail 200x200 output.jpg   # Thumbnail
```

### Crop
```bash
magick input.jpg -crop 800x600+0+0 output.jpg    # Crop from top-left
magick input.jpg -gravity center -crop 500x500+0+0 output.jpg  # Center crop
```

### Convert
```bash
magick input.png output.jpg                       # PNG to JPG
magick input.jpg -quality 85 output.jpg           # Compress JPG
magick *.jpg output.pdf                           # Images to PDF
```

### Effects
```bash
magick input.jpg -colorspace Gray output.jpg      # Grayscale
magick input.jpg -blur 0x8 output.jpg             # Blur
magick input.jpg -sharpen 0x1 output.jpg          # Sharpen
```

### Watermark
```bash
magick input.jpg -gravity southeast -pointsize 30 -fill white \
  -annotate +10+10 "Text" output.jpg               # Text watermark
```

## Response Approach

When users request image manipulation:

1. **Identify operation:** Rotation, resize, crop, convert, effect, watermark, batch
2. **Check input:** Verify file exists, check format
3. **Determine output:** Format, quality, naming convention
4. **Execute command:** Use appropriate ImageMagick command
5. **Verify result:** Check output file was created
6. **Open/display:** Show result to user if requested
7. **Cleanup:** Remove temporary files if needed

## Advanced Topics

For more advanced operations, see:
- [ImageMagick Official Documentation](https://imagemagick.org/)
- [Command-line Options Reference](https://imagemagick.org/script/command-line-options.php)
- [Examples Gallery](https://imagemagick.org/Usage/)
