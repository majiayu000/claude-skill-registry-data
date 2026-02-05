---
name: resize-image
description: Resize images using ImageMagick when they are too large to view or process. Use this skill when you encounter an image file that exceeds token limits, is too large to read, or when you need to create a smaller version of an image for viewing.
allowed-tools: Bash, Read
---

# Resize Image Skill

This skill allows you to resize images using ImageMagick's `convert` command when they are too large to view or process.

## When to Use

- When reading an image file fails due to token limits
- When an image is too large to process
- When you need to create a thumbnail or smaller version of an image
- When a user provides a mockup or screenshot that's too large

## Prerequisites

ImageMagick must be installed. Check with:
```bash
which convert || echo "ImageMagick not installed"
```

If not installed, suggest the user install it:
- Ubuntu/Debian: `sudo apt-get install imagemagick`
- macOS: `brew install imagemagick`

## Instructions

### Step 1: Check the original image size
```bash
identify "/path/to/image.png"
```

This shows dimensions and file size.

### Step 2: Resize the image

Resize to a maximum width/height while maintaining aspect ratio:
```bash
convert "/path/to/original.png" -resize 800x600\> "/tmp/resized-image.png"
```

The `\>` flag ensures the image is only shrunk, never enlarged.

Common resize options:
- `-resize 800x600` - Fit within 800x600, maintain aspect ratio
- `-resize 50%` - Scale to 50% of original size
- `-resize 400x` - Set width to 400px, auto-calculate height
- `-resize x400` - Set height to 400px, auto-calculate width

### Step 3: Reduce quality/colors for smaller file size (optional)

For PNG files, reduce colors:
```bash
convert "/path/to/original.png" -resize 800x600\> -colors 256 "/tmp/resized-image.png"
```

For JPEG files, reduce quality:
```bash
convert "/path/to/original.jpg" -resize 800x600\> -quality 80 "/tmp/resized-image.jpg"
```

### Step 4: Read the resized image
```bash
# Verify the new size
ls -la /tmp/resized-image.png
identify /tmp/resized-image.png
```

Then use the Read tool to view the resized image:
```
Read /tmp/resized-image.png
```

## Examples

### Example 1: Resize a large mockup
```bash
# Check original size
identify "/mnt/c/Users/user/mockup.png"
# Output: mockup.png PNG 2400x1800 ...

# Resize to fit within 800x600
convert "/mnt/c/Users/user/mockup.png" -resize 800x600\> "/tmp/mockup-small.png"

# Verify
identify "/tmp/mockup-small.png"
# Output: mockup-small.png PNG 800x600 ...
```

### Example 2: Create a thumbnail
```bash
convert "/path/to/screenshot.png" -resize 400x -colors 128 "/tmp/thumbnail.png"
```

### Example 3: Batch resize multiple images
```bash
for img in /path/to/images/*.png; do
  convert "$img" -resize 800x600\> "/tmp/$(basename "$img")"
done
```

## Output Location

Always save resized images to `/tmp/` with a descriptive name:
- `/tmp/resized-mockup.png`
- `/tmp/thumbnail-screenshot.png`
- `/tmp/small-diagram.png`

## Troubleshooting

**"convert: command not found"**
ImageMagick is not installed. Ask the user to install it.

**"convert: unable to open image"**
Check the file path. Windows paths under WSL should use `/mnt/c/...` format.

**Image still too large after resize**
Try reducing colors or quality, or resize to smaller dimensions.
