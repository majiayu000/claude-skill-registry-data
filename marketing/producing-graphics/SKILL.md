---
name: producing-graphics
metadata:
  version: "1.0.0"
allowed-tools: "Bash, Read, Write"
description: >
  Create export-ready graphics for web, print, and social media with correct
  formats, color spaces, resolution, and optimization. Use when preparing assets
  for production, exporting from Figma or Sketch, creating marketing materials,
  converting image formats, optimizing file sizes, generating responsive srcsets,
  building favicon packages, or exporting print-ready PDFs. Also triggers on:
  WebP conversion, srcset, image optimization, JPEG quality, PNG transparency,
  SVG optimization, SVGO, CMYK, print bleed, DPI, social media image sizes,
  responsive images, favicon export, logo package, or color space conversion.
---

# Production Graphics

Prepare export-ready graphics with correct formats, optimization, and specs for web, print, and social media.

<intake>

**Choose workflow based on output medium:**

| User Says | Route To |
|-----------|----------|
| "Web graphics" / "optimize images" / "srcset" / "WebP" | Step 1 — Web Graphics Export |
| "Print" / "CMYK" / "bleed" / "DPI" / "PDF/X-1a" | Step 2 — Print Graphics Export |
| "Social media" / "Instagram" / "LinkedIn" / "Twitter" | Step 3 — Social Media Specs |
| "Icon" / "SVG" / "SVGO" / "logo" | Step 4 — Vector Graphics |
| "Logo package" / "brand assets" / "full logo export" | Step 5 — Logo Export |

</intake>

## Step 1: Web Graphics Export

**Image format decision tree:**

```
Is it a photograph or complex image?
├─ Yes → WebP (quality 80) with JPEG fallback
└─ No → Is it a simple graphic or logo?
   ├─ Yes → SVG (scalable, tiny file size)
   └─ No → Does it need transparency?
      ├─ Yes → WebP (quality 80) with PNG-24 fallback
      └─ No → WebP (quality 80) with JPEG fallback
```

**Format targets:**

| Format | Use Case | Quality Setting | Max Size |
|--------|----------|-----------------|----------|
| WebP | All modern browsers | 80% | <150KB |
| JPEG | Legacy fallback for photos | 80–85% | <200KB |
| PNG-24 | Transparency fallback | Lossless | <150KB |
| SVG | Icons, logos, illustrations | N/A (minify) | <50KB |

**Optimization commands:**

```bash
# Convert to WebP (requires cwebp — brew install webp or apt-get install webp)
cwebp -q 80 input.png -o output.webp
cwebp -q 80 input.jpg -o output.jpg.webp

# Optimize JPEG
jpegoptim --max=85 --strip-all input.jpg
# Or: mogrify -quality 85 -strip input.jpg  (ImageMagick)

# Optimize PNG
pngquant --quality=80-90 --output output.png input.png

# Generate responsive srcset variants (ImageMagick)
convert source@2x.jpg -resize 800x  image-800.jpg
convert source@2x.jpg -resize 1200x image-1200.jpg
convert source@2x.jpg -resize 1600x image-1600.jpg

# Batch WebP conversion for a directory
for f in *.jpg *.png; do
  cwebp -q 80 "$f" -o "${f%.*}.webp"
done
```

**Responsive image HTML:**

```html
<picture>
  <source
    srcset="image-800.webp 800w, image-1200.webp 1200w, image-1600.webp 1600w"
    type="image/webp"
  />
  <img
    srcset="image-800.jpg 800w, image-1200.jpg 1200w, image-1600.jpg 1600w"
    sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 800px"
    src="image-800.jpg"
    alt="Description"
    loading="lazy"
    width="800"
    height="600"
  />
</picture>
```

**Web graphics checklist:**
- [ ] Format: WebP primary, JPEG/PNG fallback
- [ ] File size: <200KB photos, <150KB graphics
- [ ] Responsive variants exported (800px, 1200px, 1600px)
- [ ] Color space: sRGB (not CMYK or Display P3)
- [ ] Alt text prepared
- [ ] `loading="lazy"` on below-fold images
- [ ] `width` and `height` attributes set (prevents CLS)

## Step 2: Print Graphics Export

**Print specifications by material:**

| Material | Resolution | Color Mode | Format | Bleed |
|----------|-----------|------------|--------|-------|
| Business card | 300 DPI | CMYK | PDF/X-1a | 3mm |
| Flyer / poster | 300 DPI | CMYK | PDF/X-1a | 5mm |
| Large banner | 150 DPI | CMYK | PDF/X-1a | 10mm |
| Magazine ad | 300 DPI | CMYK | PDF/X-1a | 3mm |
| Billboard | 72–100 DPI | CMYK | PDF/X-1a | 10mm |

**DPI rule:** 300 DPI at final print size. Large format viewed at distance can use 150 DPI. Billboards 72–100 DPI.

**RGB → CMYK conversion:**

```bash
# ImageMagick with ICC profile (preferred)
convert input.png \
  -profile /path/to/sRGB.icc \
  -colorspace CMYK \
  -profile /path/to/USWebCoatedSWOP.icc \
  output.tif

# Quick conversion without profile (loses accuracy — preview before sending to print)
convert input.png -colorspace CMYK output.tif
```

**Bleed math:**

```
Final print size: 90mm × 50mm (business card)
+ Bleed:          3mm all sides
= Export size:    96mm × 56mm

Safe zone: 3mm inset from trim on all sides
(no critical text or logos within 3mm of edge)
```

**PDF/X-1a settings (Figma → print PDF):**
- Figma doesn't natively export PDF/X-1a — export as high-res PNG (300 DPI) then use Acrobat or Affinity Publisher to convert
- InDesign: File → Export → PDF (Print) → PDF/X-1a:2001
- Settings: CMYK, embed all fonts, flatten transparency, include bleed marks

**Print graphics checklist:**
- [ ] Resolution: 300 DPI at final print size (150 for large format)
- [ ] Color mode: CMYK (Coated FOGRA39 or US Web Coated SWOP)
- [ ] Format: PDF/X-1a or TIFF
- [ ] Bleed: 3–10mm extended background (material-dependent)
- [ ] Safe zone: 3mm margin from trim edge — no critical text
- [ ] Fonts: embedded or converted to outlines
- [ ] Rich black for large black areas: C:60 M:40 Y:40 K:100 (not K:100 only)
- [ ] File size: <50MB for email delivery

## Step 3: Social Media Graphics

**Platform specifications (2025):**

| Platform | Profile | Post | Story / Reel |
|----------|---------|------|--------------|
| Instagram | 320×320px | 1080×1080px (1:1) or 1080×1350px (4:5) | 1080×1920px (9:16) |
| Facebook | 180×180px | 1200×630px (1.91:1) | 1080×1920px (9:16) |
| Twitter/X | 400×400px | 1200×675px (16:9) | — |
| LinkedIn | 400×400px | 1200×627px (1.91:1) | — |
| YouTube | 800×800px | 1280×720px (thumbnail) | — |
| TikTok | 200×200px | — | 1080×1920px (9:16) |

**Export settings:**

```bash
# Resize to platform spec (ImageMagick)
convert source.png -resize 1080x1080^ -gravity center -extent 1080x1080 instagram-square.png
convert source.png -resize 1080x1350^ -gravity center -extent 1080x1350 instagram-portrait.png
convert source.png -resize 1200x675^  -gravity center -extent 1200x675  twitter-post.png

# Optimize for social (platforms re-compress anyway — use quality 90-95)
jpegoptim --max=92 --strip-all social-post.jpg
```

**Text legibility rules for mobile:**
- Minimum font size: 40px at export resolution
- Max line length: 40 characters
- Safe zone: 10% margin from all edges (platforms crop aggressively)
- Contrast: ≥4.5:1 for text over background

**Social media checklist:**
- [ ] Dimensions match platform spec exactly
- [ ] Text readable on mobile (≥40px at export size)
- [ ] 10% safe zone respected from all edges
- [ ] Text contrast ≥4.5:1
- [ ] File size under platform limit (Twitter: 5MB, Instagram: 30MB, LinkedIn: 10MB)
- [ ] Format: JPEG for photos, PNG for text/graphics
- [ ] Color space: sRGB
- [ ] Preview on actual mobile device before posting

## Step 4: Vector Graphics (SVG/Icons)

**SVG optimization:**

```bash
# Install SVGO
npm install -g svgo

# Optimize single file
svgo icon.svg -o icon.optimized.svg

# Optimize directory
svgo -f ./icons/ -o ./icons/optimized/

# Typical size reduction: 30–70%
```

**Clean SVG structure:**

```xml
<!-- ✅ Production SVG -->
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M12 2L2 7l10 5 10-5-10-5z" fill="currentColor"/>
</svg>

<!-- ❌ Bloated export from Illustrator -->
<svg id="Layer_1" style="enable-background:new 0 0 24 24;">
  <g id="Group_1"><path id="Path_1" style="fill:#000000;" d="..."/></g>
</svg>
```

**Icon sizing standards:** 16px, 20px, 24px, 32px for web. Always use `currentColor` so icons inherit CSS color.

**Favicon package:**

```bash
# Generate multi-size favicon (requires ImageMagick)
convert logo.png -resize 16x16  favicon-16.png
convert logo.png -resize 32x32  favicon-32.png
convert logo.png -resize 48x48  favicon-48.png
convert favicon-16.png favicon-32.png favicon-48.png favicon.ico

# Modern scalable favicon
cp logo.svg favicon.svg
```

**Icon checklist:**
- [ ] Optimized with SVGO (<10KB)
- [ ] `viewBox` set correctly
- [ ] No embedded fonts or raster images
- [ ] Colors use `currentColor`
- [ ] `aria-label` or `<title>` for interactive icons
- [ ] PNG fallbacks at 16px, 24px, 32px

## Step 5: Logo Export (Multi-Format Package)

**Complete logo delivery structure:**

```
logo-package/
├── web/
│   ├── logo.svg              (scalable, primary web asset)
│   ├── logo@2x.png           (2000px wide, transparent)
│   ├── logo-white.svg        (reverse — for dark backgrounds)
│   ├── logo-white@2x.png     (transparent)
│   └── logo-black.svg        (single-color)
├── print/
│   ├── logo-cmyk.pdf         (PDF/X-1a, vector, CMYK)
│   └── logo-cmyk.eps         (vector, CMYK, for legacy tools)
├── favicon/
│   ├── favicon.ico           (16, 32, 48px multi-size)
│   └── favicon.svg           (scalable, modern browsers)
└── social/
    ├── logo-square.png       (1080×1080px for profile photos)
    └── logo-og.png           (1200×630px for Open Graph)
```

**Generate the package:**

```bash
# Web variants (requires ImageMagick)
convert logo.svg -resize 2000x logo@2x.png
convert logo.svg -resize 1000x logo@1x.png

# Favicon package
convert logo.png -resize 16x16  favicon-16.png
convert logo.png -resize 32x32  favicon-32.png
convert logo.png -resize 48x48  favicon-48.png
convert favicon-16.png favicon-32.png favicon-48.png favicon.ico

# Social variants
convert logo.png -resize 1080x1080^ -gravity center -extent 1080x1080 -background none logo-square.png
convert logo.png -resize 1200x630^  -gravity center -extent 1200x630  -background white logo-og.png
```

**Clear space rule:** Minimum clear space = height of the logo's capital letter on all sides. Never crop or place competing elements inside this zone.

**Minimum sizes:** Print: 20mm width. Web: 120px width. Mobile: 80px width.

## Quality Gates

Before delivery:

- [ ] Correct format for use case (web: WebP/SVG, print: PDF/X-1a, social: JPEG/PNG)
- [ ] Correct color space (web: sRGB, print: CMYK)
- [ ] Resolution matches specs (web: 2x minimum, print: 300 DPI)
- [ ] File size optimized and within limits
- [ ] Multiple formats provided (SVG + PNG fallback for logos)
- [ ] Responsive variants exported for web (800w, 1200w, 1600w)
- [ ] Bleed included for print
- [ ] Fonts embedded or outlined for print
- [ ] Safe zones respected (social: 10%, print: 3mm from trim)
- [ ] Preview verified on target medium (screen or printed proof)

## CLAIMS

- [SOURCED] PDF/X-1a is the most compatible print-ready PDF standard — ISO 15929:2000
- [GENERATED] WebP at quality 80 typically achieves 25–35% smaller file size than JPEG at quality 85 for photographic content — exact savings vary by image content
- [GENERATED] Social platform size specs are accurate as of Q1 2025 — platforms update these periodically; verify against official platform documentation before major campaigns
- [GENERATED] Rich black (C:60 M:40 Y:40 K:100) prevents muddy appearance on large solid areas that can occur with K:100 alone on offset presses

## GAPS / BLINDSPOTS / UNKNOWN-UNKNOWNS

- Social platform specs change without notice — Instagram has updated image ratios multiple times
- Display P3 wide-gamut color for high-end web (not covered here) — relevant for products targeting HDR displays
- AVIF format has better compression than WebP at low quality settings but browser support and tooling are still maturing
- ImageMagick commands assume version 7 (magick) or version 6 (convert) — syntax differs between versions
