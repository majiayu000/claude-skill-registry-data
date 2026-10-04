---
name: qa-detect-viewport-units
section: responsiveness
description: "Detects 100vh-not-dvh (content clipped under the mobile address bar) and retina-blurry raster images (natural resolution < 2x render, no srcset) — pixel-density + viewport-unit responsiveness"
model: haiku
applyOn: [mobile]
needsSetup: false
viewportSensitive: false
requires: [hasViewportUnits]
---

# qa-detect-viewport-units

## What it checks
Two responsiveness issues that only bite on real mobile devices and are invisible to width-only testing:

1. **`100vh` without `dvh`** — on mobile browsers the address bar collapses/expands, so `100vh` is taller than the visible area. Content (or a sticky CTA) pinned to `100vh` gets clipped under the bar. The fix is `100dvh` (dynamic viewport height).
2. **Retina-blurry images** — phones render at 2–3× device-pixel-ratio. A raster image whose natural resolution is barely its CSS size (no `srcset`/2× variant) looks soft/blurry on every modern phone.

Static DOM/CSS inspection → Haiku. Runs once per route on the mobile leader cell (`viewportSensitive: false`).

## Self-skip
Skip if the page has no stylesheets readable AND no `<img>` elements.

## Probe (browser_evaluate)
```js
() => {
  const findings = [];

  // 1) 100vh without dvh — scan readable stylesheets for `100vh` not paired with a dvh fallback
  try {
    let vhRuleCount = 0, dvhSeen = false;
    for (const sheet of document.styleSheets) {
      let rules;
      try { rules = sheet.cssRules; } catch { continue; } // cross-origin sheet — skip
      if (!rules) continue;
      for (const rule of rules) {
        const t = rule.cssText || '';
        if (/\bdvh\b/.test(t)) dvhSeen = true;
        if (/(height|min-height|max-height)\s*:\s*100vh/.test(t)) vhRuleCount++;
      }
    }
    if (vhRuleCount > 0 && !dvhSeen) {
      findings.push({
        issueType: 'viewport100vhNotDvh', severity: 'medium',
        selector: 'stylesheet',
        description: `${vhRuleCount} rule(s) use height:100vh with no dvh fallback. On mobile the address bar makes 100vh taller than the visible area, clipping content. Use 100dvh (or svh/lvh) for full-height layout.`
      });
    }
  } catch (e) {}

  // 1b) live full-height elements that equal innerHeight (likely 100vh) and overflow the visual viewport
  const vv = (window.visualViewport && window.visualViewport.height) || window.innerHeight;
  document.querySelectorAll('header, footer, [class*="hero"], [class*="full"], main, section').forEach(el => {
    const r = el.getBoundingClientRect();
    if (Math.abs(r.height - window.innerHeight) <= 2 && r.height > vv + 8) {
      findings.push({
        issueType: 'fullHeightClippedByChrome', severity: 'low',
        selector: el.tagName.toLowerCase() + (typeof el.className === 'string' && el.className ? '.' + el.className.split(/\s+/)[0] : ''),
        description: `Full-height element (${Math.round(r.height)}px ≈ 100vh) exceeds the visible viewport (${Math.round(vv)}px) — its bottom is hidden behind the mobile browser chrome.`
      });
    }
  });

  // 2) retina-blurry raster images — natural res < 2x rendered, no srcset/2x source
  document.querySelectorAll('img').forEach(img => {
    const r = img.getBoundingClientRect();
    if (r.width < 24 || r.height < 24) return;                 // skip tiny icons
    const src = (img.currentSrc || img.src || '');
    if (/\.svg(\?|$)/i.test(src)) return;                      // vector — DPR-safe
    const hasSrcset = !!img.getAttribute('srcset') ||
      (img.closest('picture') && img.closest('picture').querySelector('source[srcset]'));
    if (hasSrcset) return;
    if (img.naturalWidth > 0 && img.naturalWidth < r.width * 2 - 1) {
      findings.push({
        issueType: 'imageBlurryOnRetina', severity: 'low',
        selector: 'img[src="' + src.slice(0, 80) + '"]',
        description: `Image renders at ${Math.round(r.width)}px CSS but its natural width is only ${img.naturalWidth}px (< 2×). It will look blurry on retina/2×-DPR phones. Provide a 2× srcset.`
      });
    }
  });

  return findings;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| viewport100vhNotDvh | medium | Stylesheet uses 100vh without a dvh fallback — content clipped under the mobile address bar |
| fullHeightClippedByChrome | low | A live full-height (≈100vh) element extends past the visible viewport on mobile |
| imageBlurryOnRetina | low | Raster image lacks the resolution/srcset for 2×-DPR screens and will appear blurry on phones |

## Notes
- The 100vh check reads `document.styleSheets`; cross-origin sheets are skipped (their rules aren't readable) — same-origin app CSS is what matters.
- The retina check approximates DPR without device emulation (the MCP browser runs at 1×); it flags images that structurally cannot be crisp at 2×, which is deterministic and accurate.
- For TRUE 2×/3× rendering you can add a device-emulated MCP server (`--device "iPhone 15"`) to the pool; this skill covers the structural cases without it.
