---
name: webp-images
description: Implement images into page sections. Converts from /public/raw/[page]/ to WebP with responsive variants, replaces CDN placeholders with Next.js Image component. Use after midjourney-prompts skill. Triggers on "implement images", "add images to page", "replace placeholder images".
---

# Image Implementation

Convert and implement images into page sections.

## Workflow

1. User provides: page route, source folder, image-to-section mapping
2. Run WebP conversion script
3. Replace CDN placeholders with Next.js `<Image>`
4. Add alt text keys to i18n files

## Convert Images

```bash
./scripts/convert-to-webp.sh [input_dir] [output_dir]
```

**Default paths:**
- Input: `/public/raw/[page]/`
- Output: `/public/images/[page]/`

Generates responsive variants: 640w, 1024w, 1920w

## Replace Patterns

See references/nextjs-patterns.md for code examples.

## Quick Reference

| Image Type | Props | Use Case |
|------------|-------|----------|
| Fixed size | `width`, `height` | Testimonials, logos |
| Fill container | `fill`, `sizes` | Hero, project thumbnails |
| Above fold | `priority` | First visible image |
| Object fit | `className="object-cover"` | Cropped images |

## i18n Alt Text

Add to `messages/de.json` and `messages/en.json`:

```json
{
  "hero": {
    "imageAlt": "Beschreibung des Bildes"
  },
  "projects": {
    "items": {
      "0": { "imageAlt": "Projekt 1 Beschreibung" }
    }
  }
}
```

## Checklist

- [ ] Images converted to WebP
- [ ] Responsive variants generated
- [ ] CDN URLs replaced with local paths
- [ ] `<img>` tags converted to `<Image>`
- [ ] Alt text added to i18n
- [ ] `priority` set for above-fold images
- [ ] `sizes` prop set for responsive images
