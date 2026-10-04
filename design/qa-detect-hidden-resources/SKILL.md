---
name: qa-detect-hidden-resources
section: responsiveness
description: "Detects desktop-only elements that are CSS-hidden on mobile but still download heavy resources (images, iframes, videos) — wasting mobile bandwidth without improving UX"
model: haiku
applyOn: [mobile, tablet]
needsSetup: false
viewportSensitive: true
---

## What it checks

`display:none` hides an element visually but the browser still downloads its resources. On mobile, this means a desktop-only hero carousel, sidebar ad, or data table silently wastes bandwidth that mobile users pay for. This skill finds those cases.

- `hiddenDesktopImagesDownloaded` — element hidden on mobile contains `<img>` tags with already-downloaded `naturalWidth > 0` (browser fetched the full image)
- `hiddenDesktopIframeLoaded` — element hidden on mobile contains `<iframe>` or `<video>` with a `src` attribute (browser opened a connection / loaded media)
- `hiddenDesktopHeavyBackground` — element hidden on mobile has a `background-image: url(...)` in computed style (browser may have fetched it even though hidden)

## Probe (browser_evaluate)
```js
() => {
  const out = [];
  const bb = () => ({ x: 0, y: 0, w: 0, h: 0 }); // hidden elements have no bbox

  // Patterns that indicate desktop-only containers
  const desktopPatterns = [
    '[class*="desktop"]', '[class*="d-none"]', '[class*="hidden-xs"]', '[class*="hidden-sm"]',
    '[class*="hide-mobile"]', '[class*="desktop-only"]', '[class*="hide-on-mobile"]',
    '[class*="sm-hide"]', '[class*="mobile-hidden"]', '[class*="no-mobile"]'
  ];

  const seenEls = new Set();

  for (const pattern of desktopPatterns) {
    for (const el of document.querySelectorAll(pattern)) {
      if (out.length >= 10 || seenEls.has(el)) continue;
      seenEls.add(el);

      const s = getComputedStyle(el);
      // Must actually be hidden (not just have a desktop class without being hidden)
      const isHidden = s.display === 'none' || s.visibility === 'hidden' || parseFloat(s.opacity) === 0;
      if (!isHidden) continue;

      const sel = `${el.tagName.toLowerCase()}${el.id ? '#' + el.id : (el.className ? '.' + String(el.className).trim().split(/\s+/)[0] : '')}`.slice(0, 120);

      // 1. Downloaded images inside hidden element
      const downloadedImgs = [...el.querySelectorAll('img[src]')].filter(img => {
        return img.naturalWidth > 0 && img.src && !img.src.startsWith('data:');
      });
      if (downloadedImgs.length > 0) {
        const srcs = downloadedImgs.slice(0, 2).map(i => i.src.split('/').pop()).join(', ');
        out.push({ issueType: 'hiddenDesktopImagesDownloaded', severity: 'medium', selector: sel,
          description: `${downloadedImgs.length} image(s) inside CSS-hidden desktop element "${sel}" are already downloaded on mobile (${srcs}). Use loading="lazy" on images or conditional rendering to avoid wasting mobile bandwidth.`,
          bbox: bb() });
      }

      // 2. Iframes and videos with src inside hidden element (connection was opened)
      const heavyEmbeds = el.querySelectorAll('iframe[src], video[src], video > source[src]');
      if (heavyEmbeds.length > 0) {
        const firstSrc = (heavyEmbeds[0].src || heavyEmbeds[0].getAttribute('src') || '').slice(0, 60);
        out.push({ issueType: 'hiddenDesktopIframeLoaded', severity: 'high', selector: sel,
          description: `${heavyEmbeds.length} iframe/video element(s) inside CSS-hidden desktop element "${sel}" have src="${firstSrc}" — browser has opened a connection to load this media on mobile. Use conditional rendering or lazy src assignment instead.`,
          bbox: bb() });
      }

      // 3. Background-image on hidden element (browser may prefetch)
      const bgEls = [...el.querySelectorAll('*')].filter(child => {
        const bg = getComputedStyle(child).backgroundImage;
        return bg && bg !== 'none' && bg.startsWith('url') && !bg.includes('data:');
      });
      if (bgEls.length > 0 && downloadedImgs.length === 0 && heavyEmbeds.length === 0) {
        out.push({ issueType: 'hiddenDesktopHeavyBackground', severity: 'low', selector: sel,
          description: `${bgEls.length} element(s) inside CSS-hidden desktop container "${sel}" have background-image URLs — browser may have fetched these images even though the element is hidden. Consider using media queries on the background-image itself or lazy-loading via JavaScript.`,
          bbox: bb() });
      }
    }
  }

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| hiddenDesktopImagesDownloaded | medium | "{N} image(s) inside CSS-hidden desktop element already downloaded on mobile — use loading=lazy or conditional rendering" |
| hiddenDesktopIframeLoaded | high | "{N} iframe/video inside CSS-hidden desktop element has src — browser opened connection on mobile" |
| hiddenDesktopHeavyBackground | low | "{N} elements inside hidden desktop container have background-image URLs — may have been prefetched" |

## Self-skip
If no elements match the desktop-pattern selectors OR none are actually hidden via CSS → return `[]`.
