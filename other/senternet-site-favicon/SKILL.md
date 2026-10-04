---
name: senternet-site-favicon
description: Generate favicon and app icon assets for a marketing site.
---

# Favicon and App Icon Setup

Generate the site's favicon assets and wire them into the public head tags. This skill is for the small but visible icon set every marketing site needs in browser tabs, bookmarks, mobile home screens, and search previews.

## What this skill produces

- `public/favicon.svg`
- `public/favicon.png`
- `public/favicon.ico`
- `public/apple-touch-icon.png`

If the site already has some of these files, patch only the missing or outdated ones.

## Steps

### 1. Find the brand mark

Look for the strongest existing source of the site's identity:

1. `src/assets/`, `public/`, or any design export assets for a logo, glyph, or wordmark
2. `index.html` or the homepage copy for a clean initial monogram if no logo exists
3. The brand colors from the design system or the page styles

Prefer a simple, high-contrast mark that still reads at 16x16. If there is no logo, create a minimal monogram or symbol rather than trying to fit the full wordmark into the favicon.

### 2. Create `public/favicon.svg`

Use SVG as the source of truth whenever possible. Keep it simple, square, and legible at small sizes:

- single background shape or transparent background
- one primary glyph or monogram
- no tiny text
- no thin strokes that collapse at 16px

If the site already has a vector logo, simplify it for favicon use instead of copying the full mark unchanged.

### 3. Generate raster fallbacks

Create the raster variants from the SVG:

- `public/favicon.png` at 512x512 or 256x256
- `public/apple-touch-icon.png` at 180x180
- `public/favicon.ico` with multi-size support for legacy browsers

Use the existing asset pipeline if the repo already has one. Otherwise generate the PNGs from the SVG and build the ICO from the PNG.

### 4. Keep the head tags aligned

Make sure the site references the new icon files in `index.html` or the shared meta-tags component:

```html
<link rel="icon" type="image/png" href="/favicon.png" />
<link rel="icon" type="image/svg+xml" href="/favicon.svg" />
<link rel="shortcut icon" href="/favicon.ico" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
```

If `/senternet-site-metatags` has already been run, update only the missing references or replace stale placeholder paths.

### 5. Verify the result

Check the generated files at browser-tab size and on a dark and light background:

- the icon should still be recognizable at 16x16
- the SVG should not depend on external fonts or scripts
- the PNG should not be blurry
- the ICO should exist for compatibility

If the favicon is used in a prerendered or deployed site, confirm the public paths resolve from the final hosting root.

### 6. Commit the generated assets

These files are generated build outputs, so commit them as the final step, never leaving the working tree dirty across sessions. Stage the generated icons together with any head-tag wiring from Step 4 and commit with a descriptive message:

```bash
git add public/favicon.svg public/favicon.png public/favicon.ico public/apple-touch-icon.png
git add index.html   # and/or the shared meta-tags component, if the icon references changed
git commit -m "Add favicon and app icon assets"
```

If you only patched a subset of the icons, stage just those files. Confirm `git status` is clean before finishing.

## Notes

- Keep favicon design intentionally simpler than the main logo
- Favor one bold shape over detail
- Reuse the brand accent color only if contrast stays strong
- Do not use oversized transparent padding around the mark

## Framework: Next.js track

Generation is identical — same source image, same sizes, same Sharp pipeline. Placement and linking differ.

Next uses file conventions in `app/` that emit the `<link>` tags automatically:

| File | Replaces |
|---|---|
| `app/favicon.ico` | `public/favicon.ico` + `<link rel="shortcut icon">` |
| `app/icon.png` (and/or `app/icon.svg`) | `public/favicon.png` / `favicon.svg` + `<link rel="icon">` |
| `app/apple-icon.png` (180×180) | `public/apple-touch-icon.png` + `<link rel="apple-touch-icon">` |

Do not also hand-write the `<link>` tags in `app/layout.tsx` — they would duplicate the generated ones. A PWA `manifest.webmanifest` still goes in `public/` and is referenced from the layout's `metadata.manifest`.

See `/senternet-site-framework` for the full convention map.
