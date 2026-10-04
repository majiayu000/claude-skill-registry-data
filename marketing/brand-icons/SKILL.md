---
name: brand-icons
description: >
  Brand icon and visual identity management for BroomVA projects. Helps the agent
  produce favicons, app icons, Open Graph images, and social media avatars from
  brand assets, keeping a consistent visual identity across web, mobile, and social
  platforms. Use when: (1) generating favicon sets (ICO, PNG, SVG) for a web project,
  (2) creating app icons for iOS/Android, (3) generating Open Graph and Twitter Card
  images, (4) producing social media profile/banner images, (5) ensuring brand
  consistency across platforms.
version: 1.0.0
category: design
latent_only: true
tags:
  - brand
  - icons
  - favicons
  - og-images
  - app-icons
  - visual-identity
  - social-media
dependencies:
  - arcan-glass
  - seo-llmeo
---

# Brand Icons

Visual identity asset generation and management for BroomVA projects.

> **This is a latent skill — it ships no CLI or scripts.** Everything below is a
> *workflow the agent performs itself*, using whatever image tooling is available
> in the working environment (e.g. ImageMagick `magick`/`convert`, `sharp`,
> `rsvg-convert`, `pngquant`, or the agent's own image-generation tools). There is
> no `brand-icons` binary to run — do not invoke these as shell commands. The
> headings name the *intent*; the agent maps each to concrete file-producing steps
> with the tools at hand, and falls back to the closest available tool when a
> specific one is missing.

## Capabilities

| Area | What it does |
|------|-------------|
| Favicons | Produce multi-size favicon sets (16, 32, 48, 180, 192, 512) from a source SVG/PNG |
| App icons | iOS (1024x1024 + sizes) and Android (adaptive icon, mipmap) sets |
| OG images | Template-based Open Graph images (1200x630) with title, description, branding |
| Social avatars | Profile pictures and banners sized for X, LinkedIn, GitHub, etc. |
| Brand consistency | Color palette extraction, contrast checking, asset catalog management |

## Workflows

### Generating a full icon set

**When asked to generate an icon set from a source image**, read the source
SVG/PNG (it must be at least 512x512 so nothing is upscaled) and produce a complete
set of favicons, app icons, and a PWA/OG template, writing them under the output
directory (default `icons/`).

Target output structure:
```
icons/
├── favicon.ico          # 16x16, 32x32, 48x48 combined
├── favicon-16x16.png
├── favicon-32x32.png
├── apple-touch-icon.png # 180x180
├── icon-192.png         # PWA manifest
├── icon-512.png         # PWA manifest
├── android/
│   ├── mipmap-mdpi/     # 48x48
│   ├── mipmap-hdpi/     # 72x72
│   ├── mipmap-xhdpi/    # 96x96
│   ├── mipmap-xxhdpi/   # 144x144
│   └── mipmap-xxxhdpi/  # 192x192
└── ios/
    └── AppIcon.appiconset/
        └── Contents.json + sized PNGs
```

### Generating an Open Graph image

**When asked to create an Open Graph image**, produce one from the given title
using the BroomVA brand template (optionally with a subtitle).

Specifications:
- Dimensions: 1200x630 pixels
- Format: PNG (with JPEG fallback for smaller size)
- Brand elements: Logo, gradient background, typography from DESIGN.md
- Dynamic text: Title (max 60 chars), optional subtitle

### Auditing a project for brand assets

**When asked to audit a project**, check the project tree for missing or
inconsistent brand assets and report against this checklist:
- [ ] favicon.ico present
- [ ] apple-touch-icon.png present (180x180)
- [ ] PWA icons in manifest (192, 512)
- [ ] OG image referenced in meta tags
- [ ] Twitter card image present
- [ ] Icons use consistent brand colors
- [ ] No pixelated/upscaled icons (source must be >= target size)

### Generating social media images

**When asked for platform-specific images**, produce profile and banner images at
the right dimensions for the target platform:

| Platform | Profile | Banner/Cover |
|----------|---------|-------------|
| X (Twitter) | 400x400 | 1500x500 |
| LinkedIn | 400x400 | 1584x396 |
| GitHub | 460x460 | — |
| YouTube | 800x800 | 2560x1440 |
| Discord | 128x128 | 960x540 |

## Size Reference

### Favicons

| File | Size | Purpose |
|------|------|---------|
| favicon.ico | 16+32+48 | Browser tab |
| favicon-16x16.png | 16x16 | Small browser tab |
| favicon-32x32.png | 32x32 | Standard browser tab |
| apple-touch-icon.png | 180x180 | iOS home screen |
| icon-192.png | 192x192 | Android Chrome / PWA |
| icon-512.png | 512x512 | PWA splash screen |
| maskable-icon.png | 512x512 | Android adaptive (safe area: 80%) |

### HTML Integration

```html
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
<meta name="theme-color" content="#0a0a12">
```

### manifest.webmanifest

```json
{
  "icons": [
    { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" },
    { "src": "/maskable-icon.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ]
}
```

## Integration

Works with:
- `arcan-glass` — pulls brand tokens (colors, typography) for OG image generation
- `content-creation` — generates OG images for new blog posts
- `seo-llmeo` — ensures OG/Twitter meta tags reference correct image assets
- `design-engineering` — aligns icon assets with DESIGN.md visual identity
