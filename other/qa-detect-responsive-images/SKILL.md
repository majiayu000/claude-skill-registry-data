---
name: qa-detect-responsive-images
section: responsiveness
description: "Detects images served without srcset, missing max-width:100%, missing loading='lazy' below the fold, and oversized natural dimensions for the viewport"
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: true
requires: [hasImages]
---

## What it checks

- Images that lack `srcset` or `sizes` (single-source, served at one resolution to every device)
- Images without `max-width: 100%` styling (cause overflow on small screens)
- Below-fold images without `loading="lazy"` (waste mobile bandwidth)
- Images whose natural size is >2× their display size (oversized payload)

## Probe (browser_evaluate)

```js
() => {
  const sel = el => {
    const id = el.id ? `#${el.id}` : '';
    const src = (el.currentSrc || el.src || '').split('/').pop().slice(0, 30);
    return (el.tagName.toLowerCase() + id + (src ? `[${src}]` : '')).slice(0, 140);
  };
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };
  const out = [];
  const vh = window.innerHeight;
  const dpr = window.devicePixelRatio || 1;

  for (const img of document.querySelectorAll('img')) {
    if (out.length >= 20) break;
    const r = img.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;
    if (!img.complete || img.naturalWidth === 0) continue;

    const style = getComputedStyle(img);
    const hasSrcset = !!img.srcset || !!img.closest('picture')?.querySelector('source[srcset]');
    const hasResponsiveCSS = style.maxWidth === '100%' || style.maxWidth.includes('%') ||
                              style.width === '100%' || style.width.includes('%');
    const isLazy = img.loading === 'lazy' || img.getAttribute('loading') === 'lazy';
    const isBelowFold = r.top > vh;

    // 1. No srcset on a substantial image
    if (!hasSrcset && r.width >= 200) {
      out.push({
        issueType: 'imageNoSrcset',
        severity: 'medium',
        selector: sel(img),
        description: `Image ${sel(img)} (${Math.round(r.width)}×${Math.round(r.height)}) has no srcset — served at single resolution to every device`,
        bbox: bb(img)
      });
    }

    // 2. Missing max-width:100% on wide images — overflow risk
    if (!hasResponsiveCSS && r.width >= 300) {
      out.push({
        issueType: 'imageNoMaxWidth',
        severity: 'medium',
        selector: sel(img),
        description: `Image ${sel(img)} is ${Math.round(r.width)}px wide but lacks max-width or % width — overflow risk on narrow viewports`,
        bbox: bb(img)
      });
    }

    // 3. Below-fold without lazy
    if (isBelowFold && !isLazy && img.naturalWidth >= 200) {
      out.push({
        issueType: 'imageNotLazy',
        severity: 'low',
        selector: sel(img),
        description: `Image ${sel(img)} is below the fold (y=${Math.round(r.top)}px) but missing loading="lazy" — wastes initial bandwidth`,
        bbox: bb(img)
      });
    }

    // 4. Oversized natural size
    const naturalArea = img.naturalWidth * img.naturalHeight;
    const displayArea = r.width * r.height * dpr * dpr;
    if (displayArea > 0 && naturalArea > displayArea * 4 && img.naturalWidth >= 600) {
      out.push({
        issueType: 'imageOversizedNatural',
        severity: 'medium',
        selector: sel(img),
        description: `Image ${sel(img)} natural ${img.naturalWidth}×${img.naturalHeight}px is >2× display ${Math.round(r.width)}×${Math.round(r.height)}px — wasted bytes`,
        bbox: bb(img)
      });
    }
  }

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| imageNoSrcset | medium | "Image has no srcset — single-resolution served to every device" |
| imageNoMaxWidth | medium | "Image lacks max-width:100% — overflow risk on narrow viewports" |
| imageNotLazy | low | "Below-fold image missing loading=lazy" |
| imageOversizedNatural | medium | "Image natural size 2× larger than display size" |
