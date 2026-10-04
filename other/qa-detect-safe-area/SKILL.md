---
name: qa-detect-safe-area
section: responsiveness
description: "Detects fixed/sticky elements at the top or bottom of the viewport that don't use env(safe-area-inset-*) — content gets hidden behind iPhone notch / home indicator"
model: haiku
applyOn: [mobile]
needsSetup: false
viewportSensitive: false
---

## What it checks

iPhone X+ and modern Android devices have notches, dynamic islands, and home indicators that overlap the viewport's edges. Content needs `env(safe-area-inset-top)` / `env(safe-area-inset-bottom)` and the `viewport-fit=cover` meta value to render correctly. Without these:
- Top nav gets hidden behind the notch / dynamic island
- Bottom tab bar gets pushed under the home indicator
- Buttons in the bottom 34px become unreachable

## Probe (browser_evaluate)

```js
() => {
  const sel = el => {
    const id = el.id ? `#${el.id}` : '';
    return (el.tagName.toLowerCase() + id).slice(0, 120);
  };
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };
  const out = [];

  // 🚫 SELF-SKIP when the environment has NO safe area at all. A regular browser — even resized
  //    to an iPhone width — has ZERO notch/inset: env(safe-area-inset-*) resolves to 0px. The
  //    "content overlaps the notch/dynamic island" defect can ONLY occur on a real notched device
  //    (or a device emulation that injects safe-area-insets). Flagging it in a plain browser
  //    viewport is a false positive — there is no safe area to respect. So measure the ACTUAL
  //    insets and bail out when they are all zero.
  const _saProbe = document.createElement('div');
  _saProbe.style.cssText = 'position:fixed;top:0;left:0;visibility:hidden;padding:' +
    'env(safe-area-inset-top,0px) env(safe-area-inset-right,0px) env(safe-area-inset-bottom,0px) env(safe-area-inset-left,0px);';
  document.documentElement.appendChild(_saProbe);
  const _ps = getComputedStyle(_saProbe);
  const _insetSum = ['paddingTop','paddingRight','paddingBottom','paddingLeft']
    .reduce((s,p) => s + (parseFloat(_ps[p]) || 0), 0);
  _saProbe.remove();
  if (_insetSum === 0) return [];   // no real safe area in this environment → nothing to overlap → skip

  // 1. Check viewport-fit=cover
  const viewport = document.querySelector('meta[name="viewport"]');
  const viewportContent = viewport ? (viewport.getAttribute('content') || '').toLowerCase() : '';
  const hasCoverFit = /viewport-fit\s*=\s*cover/i.test(viewportContent);

  // Helper: does a CSS property string contain env(safe-area-inset)?
  const usesSafeArea = (...vals) => vals.some(v =>
    v && /env\(\s*safe-area-inset|constant\(\s*safe-area-inset/i.test(v)
  );

  // 2. Find fixed/sticky elements at the very top or very bottom
  const vh = window.innerHeight;
  const candidates = document.querySelectorAll(
    'header, nav, footer, aside, ' +
    '[class*="navbar"], [class*="topbar"], [class*="tab-bar"], ' +
    '[class*="bottom-bar"], [class*="bottom-nav"], [class*="sticky"], [class*="fixed"]'
  );

  for (const el of candidates) {
    if (out.length >= 10) break;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    const style = getComputedStyle(el);
    if (style.position !== 'fixed' && style.position !== 'sticky') continue;

    // Element at very top
    const atTop = r.top <= 8 && r.height < vh * 0.5;
    // Element at very bottom
    const atBottom = (vh - r.bottom) <= 8 && r.height < vh * 0.5;
    if (!atTop && !atBottom) continue;

    // Read inline style + computed properties for env() usage
    const inlinePadding = el.getAttribute('style') || '';
    const safeAreaUsed = usesSafeArea(
      inlinePadding,
      style.paddingTop, style.paddingBottom,
      style.marginTop, style.marginBottom,
      style.top, style.bottom
    );
    // Also accept padding-block / margin-block (logical)
    const logicalUsed = /env\(safe-area-inset/i.test(inlinePadding);

    if (!safeAreaUsed && !logicalUsed) {
      out.push({
        issueType: atTop ? 'safeAreaTopMissing' : 'safeAreaBottomMissing',
        severity: 'medium',
        selector: sel(el),
        description: `${atTop ? 'Top' : 'Bottom'} fixed/sticky element ${sel(el)} does not use env(safe-area-inset-${atTop ? 'top' : 'bottom'}) — content will overlap with iPhone ${atTop ? 'notch/dynamic island' : 'home indicator'}.`,
        bbox: bb(el)
      });
    }
  }

  // 3. If there are bottom-fixed elements but viewport-fit=cover is missing, flag separately
  if (!hasCoverFit && out.some(o => o.issueType === 'safeAreaBottomMissing' || o.issueType === 'safeAreaTopMissing')) {
    out.push({
      issueType: 'viewportFitCoverMissing',
      severity: 'medium',
      selector: 'meta[name="viewport"]',
      description: 'Viewport meta does not include viewport-fit=cover — required for env(safe-area-inset-*) values to be non-zero on iPhone X+.',
      bbox: { x: 0, y: 0, w: 200, h: 30 }
    });
  }

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| safeAreaTopMissing | medium | "Top fixed/sticky element does not use env(safe-area-inset-top) — content hidden by iPhone notch" |
| safeAreaBottomMissing | medium | "Bottom fixed/sticky element does not use env(safe-area-inset-bottom) — content under iPhone home indicator" |
| viewportFitCoverMissing | medium | "Viewport meta missing viewport-fit=cover — safe-area-inset values will be zero on iPhone X+" |
