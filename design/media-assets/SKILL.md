---
name: media-assets
description: "Use and manage visual/media assets: reuse-first, formats, responsive delivery, fonts, caching, fallbacks, accessibility. Use when adding or optimizing images, icons, fonts, video."
---

# media-assets

Reuse first. An existing asset that satisfies the requirement beats a new one every time.

## Activate when

- Adding, replacing, or optimizing images, icons, fonts, video/audio, favicons, or background media.

## Do NOT activate for

- Design decisions (see design-systems); layout (see responsive-design).

## Decision procedure

```
reuse existing asset? -> inspect dimensions/type/licensing/fit
  -> determine delivery format -> optimize -> integrate
  -> verify loading/performance/accessibility
```

## Procedure

1. Inventory before creating: search `public/`, `assets/`, `static/`, framework asset dirs, and existing icon/font sets. If a project asset fits (dimensions, style, license), reuse it. Do not generate or download a duplicate.
2. Format: AVIF first with WebP fallback for photos (JPEG only where ancient clients matter); SVG for logos/icons/illustrations; PNG only for transparency-needing raster without vector source. Confirm licensing on any third-party asset.
3. Responsive delivery: `srcset` + `sizes` with density-appropriate variants; `<picture>` for art direction (different crops per breakpoint); explicit `width`/`height` or `aspect-ratio` to prevent layout shift; retina variants at 2x for critical imagery only.
4. Loading: eager + `fetchpriority="high"` for LCP/hero only; `loading="lazy"` + async decoding below the fold; `preload` critical fonts/hero image sparingly, `preconnect` for the image CDN; never preload everything.
5. Optimize: compress to the quality threshold where artifacts are invisible (tool-gated: IF sharp/squoosh/imagemin available use it, ELSE use the framework/CDN pipeline); strip metadata; cap dimensions to display need.
6. CDN/caching: image CDN with signed/parameterized transforms where justified; long-cache immutable hashed filenames, cache-busting by content hash (never query-string on far-future assets); versioned asset directories.
7. SVG/icons: inline small icons (sprite or component), external files for large illustrations; SVGs sanitized (no scripts/event handlers) when user-uploaded — treat as untrusted content.
8. Favicons/app icons: full set (favicon.ico, PNG sizes, apple-touch-icon, maskable PWA icons, theme-color meta); verify on real devices.
9. Fonts: variable fonts preferred; `font-display: swap`; subset to used glyphs/languages; self-host over third-party where privacy/performance demands; preloaded only the critical weights.
10. Video/audio: poster image + preload="none"/"metadata" by default; muted autoplay only; captions/transcripts for accessibility; thumbnails generated, not screenshotted ad hoc.
11. Variants/fallbacks: dark/light variants where the design demands; descriptive alt text (empty alt only for pure decoration); `onerror`/skeleton fallbacks for missing/broken media; background images never carry sole-meaning content.
12. Framework systems: Next.js — research the `next/image` API for the installed Next.js major in https://nextjs.org/docs (remotePatterns, loader, placeholder behavior are version-sensitive); never fight the optimizer with unoptimized originals.
13. Organization: `assets/` by type (`images/`, `icons/`, `fonts/`, `video/`), descriptive kebab-case names with dimensions where relevant (`hero-1600.avif`), source files separated from build output.
14. Verify: Lighthouse/media audit, layout-shift check, broken-asset sweep, alt-text review, cache-header inspection. Record tool used or manual steps taken.

## Failure modes

- Duplicate near-identical assets; 5MB hero images; layout shift from dimensionless images; lazy-loading the LCP image; unlicensed stock; SVG XSS via uploads; font-induced invisible text.

## References
- Related: `../responsive-design/`, `../performance/`, `../accessibility/`, `../technical-seo/` (image SEO).
