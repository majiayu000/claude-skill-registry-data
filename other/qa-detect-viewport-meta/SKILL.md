---
name: qa-detect-viewport-meta
section: responsiveness
description: "Detects missing or harmful viewport meta tag — wrong viewport breaks every mobile layout, and user-scalable=no fails WCAG 1.4.4"
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
---

## What it checks

The `<meta name="viewport">` tag is the single most important responsiveness signal. Common bugs:
- **Missing tag** — mobile browsers fall back to 980px desktop simulation, breaking all responsive design
- **`user-scalable=no` or `maximum-scale=1`** — disables pinch-zoom (WCAG 1.4.4 violation, blocks low-vision users)
- **No `width=device-width`** — viewport scales incorrectly
- **`viewport-fit=cover` missing on PWAs** — content goes under iOS notch

## Probe (browser_evaluate)

```js
() => {
  const out = [];
  const metas = [...document.querySelectorAll('meta[name="viewport" i]')];

  // 1. No viewport meta at all
  if (metas.length === 0) {
    out.push({
      issueType: 'viewportMetaMissing',
      severity: 'high',
      selector: 'head',
      description: 'No <meta name="viewport"> tag — mobile browsers render at 980px desktop width and all responsive design fails. Add <meta name="viewport" content="width=device-width, initial-scale=1">.',
      bbox: { x: 0, y: 0, w: 200, h: 30 }
    });
    return out;
  }

  // 2. Inspect content of each viewport meta
  for (const m of metas) {
    const content = (m.getAttribute('content') || '').toLowerCase().replace(/\s+/g, '');
    const sel = m.id ? `#${m.id}` : 'meta[name="viewport"]';

    if (!content.includes('width=device-width')) {
      out.push({
        issueType: 'viewportNoDeviceWidth',
        severity: 'high',
        selector: sel,
        description: `Viewport meta content="${content}" does not include width=device-width — mobile rendering will be incorrect.`,
        bbox: { x: 0, y: 0, w: 200, h: 30 }
      });
    }

    // user-scalable=no — accessibility violation
    if (/user-scalable\s*=\s*(no|0)/i.test(content) || /user-scalable\s*=\s*(no|0)/i.test(m.getAttribute('content') || '')) {
      out.push({
        issueType: 'viewportNoScaling',
        severity: 'high',
        selector: sel,
        description: 'Viewport meta has user-scalable=no — disables pinch-zoom, blocks low-vision users. WCAG 1.4.4 violation. Remove this restriction.',
        bbox: { x: 0, y: 0, w: 200, h: 30 }
      });
    }

    // maximum-scale=1 also blocks zoom
    if (/maximum-scale\s*=\s*1(\.0+)?[,;\s]/i.test(content + ',')) {
      out.push({
        issueType: 'viewportMaxScale1',
        severity: 'high',
        selector: sel,
        description: 'Viewport meta has maximum-scale=1 — blocks user zoom. WCAG 1.4.4 violation. Allow scaling up to at least 5.',
        bbox: { x: 0, y: 0, w: 200, h: 30 }
      });
    }
  }

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| viewportMetaMissing | high | "No <meta name=viewport> — mobile renders at 980px desktop simulation, all responsive design fails" |
| viewportNoDeviceWidth | high | "Viewport meta missing width=device-width" |
| viewportNoScaling | high | "Viewport has user-scalable=no — blocks pinch zoom, WCAG 1.4.4 violation" |
| viewportMaxScale1 | high | "Viewport has maximum-scale=1 — blocks zoom, WCAG 1.4.4 violation" |
