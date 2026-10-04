---
name: image-enhancer
description: Improve image quality by enhancing resolution, sharpness, and clarity. Perfect for screenshots, documentation, presentations, and social media images.
compatibility:
  use-case: Image processing, visual content preparation, quality enhancement
  frameworks: Image upscaling, sharpening, artifact reduction
---

# Image Enhancer

## Use This Skill When

- Improving screenshot quality for blog posts or documentation
- Sharpening blurry or low-resolution images
- Upscaling images to higher resolution
- Preparing images for presentations or reports
- Reducing compression artifacts from JPEG images
- Cleaning up images before social media posting
- Batch processing multiple images
- Preparing visual content for printing

## When NOT to Use

- Editing content or composition (different skill)
- Adding text or watermarks
- Professional photo retouching or color grading
- Creating new graphics from scratch
- Legal/forensic image analysis
- Images with privacy/sensitive information

## Context: Image Quality Enhancement Maturity

**Undeveloped**: Use images as-is; blurry screenshots posted directly.

**Target**: Enhance resolution, sharpen details, reduce noise; optimize for use case.

**Optimized**: Automatic quality detection, ML-based upscaling, batch processing, use-case optimization (web vs. print vs. social).

## Core Principle

**Image quality reflects professionalism.** Poor screenshots, blurry photos, or compressed artifacts undermine content. Enhancement improves clarity, readability, and visual impact with minimal manual effort.

## Instructions

### Step 1: Analyze Image Quality

**Assess current image state:**

```markdown
## Image Analysis: screenshot.png

**Current Specs**:
- Resolution: 1920x1080 (native)
- Format: PNG
- File Size: 3.2 MB
- Color Depth: 24-bit
- Compression: Moderate

**Quality Assessment**:
- ✓ Good resolution for web
- ⚠️ Slight blur in text areas
- ⚠️ Some compression artifacts in gradients
- ✓ Colors well-saturated

**Recommendations**:
1. Sharpen text edges
2. Reduce gradient banding artifacts
3. Upscale to 2560x1440 for retina displays
4. Optimize file size for web delivery
```

### Step 2: Choose Enhancement Strategy

**Select based on use case:**

| Use Case | Strategy | Output Resolution | Format |
|----------|----------|------------------|--------|
| **Web display** | Sharpen + optimize | 1920-2560 | PNG/WebP |
| **Retina display** | Upscale + sharpen | 2x native (2560x1440) | PNG |
| **Print (300dpi)** | Upscale + detail enhance | High DPI | PNG/TIFF |
| **Social media** | Optimize + compress | 1200-1600 | JPG (optimized) |
| **Documentation** | Sharpen + artifact reduce | Native + 20% | PNG |

### Step 3: Apply Resolution Enhancement

**Upscale intelligently:**

```bash
# Option 1: 1.5x upscaling (minimal quality loss)
upscale --input original.png --output upscaled.png --factor 1.5

# Option 2: 2x upscaling (retina)
upscale --input original.png --output upscaled.png --factor 2

# Using AI/ML upscaling (preserves detail)
# Better than bicubic interpolation
```

**Output comparison:**

```markdown
## Resolution Enhancement

**Original**: 1920x1080 (1 MB)
**After 1.5x Upscale**: 2880x1620 (2.1 MB)
**After 2x Upscale**: 3840x2160 (4K, 4.2 MB)

**Recommendation**: 1.5x for web, 2x for retina/print
```

### Step 4: Enhance Sharpness and Details

**Sharpen edges without over-processing:**

```bash
# Apply unsharp mask (standard sharpening)
sharpen --input upscaled.png --output sharpened.png \
  --radius 0.5 --amount 1.0 --threshold 0

# Adaptive sharpening (preserves smooth areas)
sharpen --input upscaled.png --output sharpened.png \
  --method adaptive --strength medium
```

**Before/after:**

```markdown
## Sharpness Enhancement

**Before**: Blurry text, soft edges
**After Sharpening**: Crisp text, defined boundaries

**Settings Applied**:
- Unsharp mask radius: 0.5
- Strength: 1.0x
- Preservation: Smooth gradients protected

**Result**: Text highly readable, no over-sharpening artifacts
```

### Step 5: Reduce Compression Artifacts

**Clean up JPEG compression artifacts:**

```bash
# Reduce banding and block artifacts
denoise --input original.jpg --output denoised.jpg \
  --method nlm --strength 0.7  # Non-local means
  
# Alternative: bilateral filter (preserves edges)
bilateral --input original.jpg --output cleaned.jpg \
  --sigma-spatial 2 --sigma-intensity 20
```

**Results:**

```markdown
## Artifact Reduction

**Common Artifacts Found**:
- JPEG blocking (8x8 block boundaries)
- Color banding in gradients
- Chroma subsampling halos

**After Denoising**:
✓ Blocks smoothed
✓ Banding reduced
✓ Colors blended naturally
✗ Minimal detail loss
```

### Step 6: Optimize for Delivery

**Optimize file size and format:**

**For Web:**
```bash
# PNG for lossless (screenshots, text)
convert input.png -strip -interlace Plane \
  -quality 95 output.png

# WebP for better compression
cwebp -q 80 input.png -o output.webp
```

**For Print:**
```bash
# TIFF with 300 DPI
convert input.png -density 300x300 -format tiff output.tif
```

**For Social Media:**
```bash
# Optimize JPG for fast loading
jpegoptim --max=85 --strip-all input.jpg
# Result: 1200-1600px width, <200KB
```

**Delivery optimization:**

```markdown
## Format Comparison

| Format | Size | Quality | Use |
|--------|------|---------|-----|
| PNG (native) | 3.2 MB | Lossless | Web, documentation |
| PNG (optimized) | 1.8 MB | Lossless | Balance of size/quality |
| WebP | 1.2 MB | 80% quality | Modern web (95% browser support) |
| JPG (80%) | 0.9 MB | 80% quality | Social media |
| TIFF (300dpi) | 8.1 MB | Lossless | Print |

**Recommended**: WebP for web (best compression)
**Fallback**: PNG for universal compatibility
```

### Step 7: Batch Process Multiple Images

**Enhance entire folder:**

```bash
#!/bin/bash
# enhance-images.sh

INPUT_DIR="${1:-.}"
OUTPUT_DIR="${INPUT_DIR}/enhanced"
SCALE_FACTOR="${2:-1.5}"

mkdir -p "$OUTPUT_DIR"

for img in "$INPUT_DIR"/*.{png,jpg,jpeg}; do
  if [ -f "$img" ]; then
    filename=$(basename "$img")
    echo "Processing $filename..."
    
    # Upscale + sharpen + optimize
    convert "$img" \
      -scale $(($(identify -format %w "$img") * SCALE_FACTOR / 100))x \
      \( +clone -blur 0x0.5 \) \
      -compose Difference -composite \
      +compose \
      -compose Multiply -composite \
      "$OUTPUT_DIR/enhanced-$filename"
      
    echo "✓ Saved to $OUTPUT_DIR/enhanced-$filename"
  fi
done
```

**Run:**
```bash
chmod +x enhance-images.sh
./enhance-images.sh ~/screenshots 150  # 1.5x upscale
```

### Step 8: Quality Assurance

**Verify enhancements:**

```markdown
## QA Checklist

**Visual Quality**:
- [ ] Text is crisp and readable
- [ ] No excessive sharpening artifacts
- [ ] Colors accurate (not oversaturated)
- [ ] Smooth gradients (no banding)
- [ ] Edges clean (no halos)

**File Size**:
- [ ] Web images <2MB
- [ ] Social media <300KB
- [ ] Print-ready at 300 DPI

**Format Appropriateness**:
- [ ] PNG for graphics/screenshots
- [ ] JPG for photographs
- [ ] WebP for modern web
- [ ] TIFF for print

**Before/After**:
- [ ] Original preserved with -original suffix
- [ ] Enhanced version shows clear improvement
- [ ] No significant quality loss compared to original
```

## Common Enhancements

| Issue | Solution |
|-------|----------|
| **Blurry text** | Sharpen with unsharp mask, increase radius |
| **Low resolution** | Upscale 1.5-2x with AI/ML method |
| **Compression artifacts** | Denoise with NLM or bilateral filter |
| **Color banding** | Apply noise dithering or gradient smoothing |
| **Large file size** | Convert to WebP, reduce DPI to 72 for web |
| **Pixelated edges** | Gentle blur + sharpen combination |

## Output

**Deliver:**

1. **Quality Analysis** (current state assessment)
2. **Enhancement Strategy** (recommended approach for use case)
3. **Before/After Comparison** (visual improvement documented)
4. **Optimized Files**
   - Enhanced version with clear naming
   - Original preserved with -original suffix
   - File size reduction percentage
5. **Format Recommendations** (PNG/JPG/WebP based on context)
6. **Batch Processing Results** (if multiple images)