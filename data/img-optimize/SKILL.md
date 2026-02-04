---
name: img-optimize
description: This skill should be used when optimizing, converting, or resizing images. Trigger when user mentions image optimization, HEIC/HEIF conversion, JPEG/PNG/WebP/AVIF processing, reducing image file size, or batch image processing. Uses sharp-cli as the primary tool.
---

# Image Optimization Skill

Optimize and convert images for various use cases using sharp-cli.

## Tools

- **sharp-cli** — Primary tool for all image optimization (JPEG/PNG/WebP/AVIF). Run `sharp --help` for full reference.
- **heif-convert** — Convert HEIC/HEIF to JPEG first, then use sharp for further optimization.

## Workflow

### 1. Analyze Input

Determine what images to process:
- Check for specific files or glob pattern (e.g., `*.HEIC`, `*.jpg`)
- List matching files to confirm scope
- Detect formats and sizes if helpful

### 2. Analyze Reference Image (Optional)

If matching a reference image:

```bash
file reference.webp      # Get format and dimensions
ls -lah reference.webp   # Get file size
```

Extract: format, dimensions (width x height), approximate file size.

### 3. Determine Parameters

Ask user for unclear parameters. Smart defaults by use case:

**Presets:**
| Preset | Size | Quality | Options |
|--------|------|---------|---------|
| web | 1920px | 78 | progressive, mozjpeg |
| standard | 2560px | 90 | mozjpeg, metadata |
| high | 3500px | 90 | 4:4:4 chroma, metadata |
| extra-high | 4000px | 95 | 4:4:4 chroma, metadata |

**Parameters:**
- **Format**: jpg, png, webp, avif (default: jpg for photos)
- **Resolution**: max dimension in pixels (default: 2560)
- **Quality**: 1-100 (default: 90 standard, 78 web)
- **Progressive**: JPEG only (default: web only)
- **Mozjpeg**: better compression (default: true for JPEG)
- **Chroma**: 4:2:0 (smaller) vs 4:4:4 (higher quality)
- **Metadata**: preserve EXIF (default: true unless web)
- **Output**: directory or in-place (default: ask if unclear)

### 4. Handle HEIC/HEIF Conversion

Convert HEIC/HEIF to JPEG first:

```bash
for f in *.HEIC *.heic; do
  [[ -f "$f" ]] || continue
  heif-convert -q 90 "$f" "${f%.*}.jpg"
done
```

Then process resulting JPEGs with sharp.

### 5. Build Sharp Command

**Structure:** `sharp -i <input> -o <output-dir> [options] [resize <w> <h>]`

**Key options:**
| Option | Description |
|--------|-------------|
| `-f webp/jpeg/png/avif` | Output format |
| `-q <1-100>` | Quality |
| `-p` / `--progressive` | Progressive JPEG |
| `--mozjpeg` | Better compression |
| `-m` / `--withMetadata` | Preserve EXIF |
| `--chromaSubsampling '4:4:4'` | High quality chroma |
| `resize <w> <h> --fit inside` | Resize maintaining aspect ratio |

**Examples:**

```bash
# Web-optimized
sharp -i *.jpg -o ./optimized resize 1920 1920 --fit inside -q 78 -p --mozjpeg

# Standard with metadata
sharp -i *.jpg -o ./ resize 2560 2560 --fit inside -q 90 --mozjpeg -m

# High quality
sharp -i *.jpg -o ./ resize 3500 3500 --fit inside -q 90 --chromaSubsampling '4:4:4' -m

# Convert to WebP
sharp -i *.jpg -o ./webp -f webp resize 1920 1920 --fit inside -q 80

# Match reference (2200x980 webp)
sharp -i input.png -o . -f webp -q 80 resize 2200 980
```

### 6. Execute and Verify

- Show command before executing
- Run and report results (files processed, size reduction)
- Handle errors gracefully

## Notes

- Always prefer sharp-cli over cwebp, imagemagick, etc.
- Use `--fit inside` for resize to maintain aspect ratio
- Web: progressive, mozjpeg, quality 75-85
- Archival: quality 90-95, metadata, 4:4:4 chroma
- Default to non-destructive (new directory) unless user wants in-place
- Match reference: use `file` for dimensions/format, `ls -lah` for size
