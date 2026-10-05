---
type: Skill
name: design-image-optimization
description: Optimize images for web performance — format conversion (WebP, AVIF), responsive sizing, compression, background removal, lazy loading, and WordPress media library integration. Uses MCP bridge tools (resize_image, remove_background) as primary; the Design Stack media worker (Sharp) as fallback for advanced/batch processing. Use when you need to resize images for social media, convert formats for faster page loads, remove backgrounds from product photos, generate alt text, or batch-process an entire media library.
license: Proprietary. See LICENSE.txt
metadata:
  type: Skill
---

# Image Optimization

Use this skill when optimizing images for web delivery, social media, or storage. MCP bridge tools are the primary interface; the media worker Sharp API is the fallback for batch and advanced operations.

## MCP Tool Discovery

The mcp-ai-wpoos plugin may register tools under **agent-specific prefixes**.
Always check your tool list for the correct names. These tools are typically
available as bare names across all agent contexts:

| Optimization Task | Tool Name | Notes |
|---|---|---|
| Resize images | `resize_image` | Bare name — usually registered everywhere |
| Remove backgrounds | `remove_background` | Bare name |
| Generate alt text | `generate_image_alt_text_validated` | Bare name |
| Generate captions | `generate_image_caption_validated` | Bare name |
| Analyze image content | `analyze_image` | Bare name |
| OCR text extraction | `extract_image_text` | Bare name |
| Cross-site media check | `remote_wp_connection` | Discover spoke sites before optimizing for them |
| Bulk resize images | `bulk_resize_media` | Resize multiple images in one operation |
| Bulk compress images | `bulk_compress_media` | Compress multiple images to target sizes |
| Find unused media | `find_unused_media` | Detect orphaned attachments consuming storage |

**Use these tools directly.** The media worker (`http://localhost:3100/api/image/optimize`)
is the fallback for WebP/AVIF format conversion and batch operations not yet
covered by MCP tools.

## WP-CLI Commands

Key `mcp-ai` WP-CLI commands for image optimization workflows. Run via `terminal`:

| Command | Use for |
|---|---|
| `wp mcp-ai bulk` | Batch-process images — resize, compress, format convert |
| `wp mcp-ai cache clear` | Clear media caches after bulk optimization |
| `wp mcp-ai health` | Verify image processing tools are registered |
| `wp mcp-ai log` | Check optimization success/failure logs |

## When to use this skill

Trigger when ANY of the following is true:

- Images are being uploaded to or served from WordPress.
- Page speed / Core Web Vitals scores need improvement (especially LCP).
- Converting between image formats (PNG → WebP, JPEG → AVIF).
- Generating responsive image variants (srcset).
- Bulk-processing existing media libraries.
- Preparing images for social media platforms with specific dimension requirements.
- Removing backgrounds from product photos or portraits.

## Resizing images via MCP (Primary)

Use `resize_image` to resize any image in your Media Library or from a URL:

```
Parameters:
  attachment_id  — WordPress attachment ID of the image (or use url/file_id)
  url            — URL to an external image
  width          — Target width in pixels (1–10000)
  height         — Target height in pixels (1–10000)
  maintain_ratio — Keep aspect ratio (default: true)
  crop           — Crop to exact dimensions (default: false)
  output_format  — "default" (same as source) or "svg" (vectorize)
  file_name      — Optional base name for the saved attachment
```

**Examples:**
- Resize hero image to 1200px wide: `width: 1200, maintain_ratio: true`
- Square Instagram crop: `width: 1080, height: 1080, crop: true`
- Thumbnail: `width: 300, maintain_ratio: true`

## Background removal via MCP (Primary)

Use `remove_background` to make image backgrounds transparent:

```
Parameters:
  attachment_id — WordPress attachment ID
  url           — URL alternative
  method        — "auto" (tries free first), "free" (rembg), "paid" (remove.bg API)
  file_name     — Optional base name
```

Best for: product photos, portraits, logos that need transparent backgrounds for overlays.

## AI-powered metadata via MCP

### Alt text generation

Use `generate_image_alt_text_validated` to create accessible alt text:

```
Parameters:
  attachment_id — WordPress attachment ID
  url           — URL alternative
  context       — Optional context about the image's usage
```

### Caption generation

Use `generate_image_caption_validated` for detailed image captions:

```
Parameters:
  attachment_id — WordPress attachment ID
  url           — URL alternative
  context       — Optional context for more relevant captions
```

### Image analysis

Use `analyze_image` for comprehensive AI vision analysis: object detection, color extraction, composition analysis, and OCR.

## Format selection guide

| Format | Best For | Compression | Browser Support |
|---|---|---|---|
| **WebP** | General web images, photos, thumbnails | ~30% smaller than JPEG | 97%+ (all modern) |
| **AVIF** | High-quality photos, hero images | ~50% smaller than JPEG | 93%+ (Chrome, Firefox, Safari 16+) |
| **JPEG** | Photos (fallback) | Lossy, good at 80% | 100% |
| **PNG** | Logos, icons, transparency | Lossless | 100% |
| **SVG** | Vector logos, icons, illustrations | Tiny (text-based) | 100% |

**Rule of thumb:** WebP for everything, AVIF for hero/LCP images, fallback JPEG for email clients.

> **Note:** WebP/AVIF format conversion currently requires the media worker fallback (`/api/image/optimize`). MCP `resize_image` preserves the source format.

## Social media image dimensions

| Platform | Feed Post | Story/Reel | Profile |
|---|---|---|---|
| **Instagram** | 1080×1080 (1:1) / 1080×1350 (4:5) | 1080×1920 (9:16) | 320×320 |
| **Facebook** | 1200×630 (1.91:1) | 1080×1920 | 180×180 |
| **Twitter/X** | 1200×675 (16:9) | — | 400×400 |
| **LinkedIn** | 1200×627 (1.91:1) | — | 400×400 |
| **Pinterest** | 1000×1500 (2:3) | — | 165×165 |

Use `resize_image` with these dimensions to prepare platform-specific variants from a single source image.

## Media worker fallback (advanced)

For WebP/AVIF conversion, batch processing, or custom quality settings, use the media worker:

### Format conversion
```javascript
const form = new FormData();
form.append('file', imageBlob, 'hero.jpg');
form.append('format', 'webp');
form.append('width', '1200');
form.append('quality', '80');

const response = await fetch('http://localhost:3100/api/image/optimize', {
  method: 'POST',
  body: form,
});

const { b64, optimized_size, savings_percent } = await response.json();
```

### Batch processing
```javascript
const form = new FormData();
images.forEach((img, i) => form.append('files', img));
form.append('format', 'webp');
form.append('width', '800');

const response = await fetch('http://localhost:3100/api/image/batch', {
  method: 'POST',
  body: form,
});
```

## WordPress integration

### Responsive srcset with WebP (using media worker)

```php
function design_responsive_image( $attachment_id, $sizes = [ 400, 800, 1200 ] ) {
    $src = wp_get_attachment_url( $attachment_id );
    $srcset = [];

    foreach ( $sizes as $width ) {
        $srcset[] = "$src?w={$width}&format=webp {$width}w";
    }

    return sprintf(
        '<img src="%s" srcset="%s" sizes="(max-width: 800px) 100vw, 800px" loading="lazy" decoding="async" />',
        "$src?w=800&format=webp",
        implode( ', ', $srcset )
    );
}
```

## Performance targets

| Metric | Target |
|---|---|
| **LCP image size** | < 100 KB (WebP/AVIF) |
| **Hero image dimensions** | Max 2400px wide (2x retina = 1200px display) |
| **Thumbnail** | 150–300px, < 20 KB |
| **Social sharing (og:image)** | 1200×630, < 200 KB |
| **Total page image weight** | < 1 MB for above-fold |

## Critical rules

- **MCP first** — use `resize_image` and `remove_background` for individual image operations.
- **WebP first, JPEG fallback** — use `<picture>` element for format switching; convert via media worker.
- **Never serve full-resolution originals** — resize to display dimensions × 2 (retina).
- **Strip EXIF data** — removes GPS, camera info; reduces file size and privacy risk.
- **Lazy-load below fold** — `loading="lazy"` on all images except LCP candidate.
- **Explicit width/height** — prevents layout shift (CLS); WordPress outputs these by default since 5.5.
- **Always add alt text** — use `generate_image_alt_text_validated` for AI-generated descriptions.

## Common mistakes

```html
<!-- WRONG — 4000px original served as 400px thumbnail -->
<img src="photo.jpg" width="400" />

<!-- RIGHT — responsive with WebP and srcset -->
<picture>
  <source srcset="photo-400.webp 400w, photo-800.webp 800w" type="image/webp" />
  <img src="photo-400.jpg" srcset="photo-400.jpg 400w, photo-800.jpg 800w"
       sizes="(max-width: 600px) 400px, 800px"
       width="800" height="600" loading="lazy" decoding="async"
       alt="AI-generated description of the image" />
</picture>
```

## What This Skill Does NOT Cover

- **Image generation** — use `design-image-generation` for AI creation of new images via Gemini, DALL·E, or other providers.
- **Video processing** — use `design-video-creation` for video transcoding, frame extraction, and format conversion.
- **Social media publishing** — use `design-social-publishing` to post optimized images to Instagram, Facebook, Twitter/X, or LinkedIn.
- **Media workflow automation** — use `design-media-workflow` for end-to-end pipelines that chain generation, optimization, and publishing.
- **Brand asset management** — use `design-brand-kit` for logo placement, brand color application, and visual identity consistency.
- **Image analysis and OCR** — use `analyze_image` or `extract_image_text` for content analysis rather than optimization.

## Cross-references

- Run **`design-image-generation`** before optimization — check your tool list for the Gemini image tool.
- Run **`design-social-publishing`** to attach optimized images to social posts.
- Run **`design-media-workflow`** for end-to-end pipeline automation including cross-site optimization.
- Run **`mcp-ai-wpoos-plugin`** for `remote_wp_connection` — verify spoke sites before optimizing media for them.
- Use **`bulk_resize_media`** to resize multiple images in a single batch operation.
- Use **`bulk_compress_media`** to compress multiple images with format selection (WebP/AVIF).
- Use **`find_unused_media`** to identify orphaned attachments for cleanup or optimization.

## References

- Sharp documentation: <https://sharp.pixelplumbing.com/>
- WebP browser support: <https://caniuse.com/webp>
- AVIF browser support: <https://caniuse.com/avif>
- WordPress responsive images: <https://developer.wordpress.org/apis/responsive-images/>
