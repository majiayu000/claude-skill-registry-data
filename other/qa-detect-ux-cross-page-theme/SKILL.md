---
name: qa-detect-ux-cross-page-theme
section: visual
description: "Detects color/theme drift ACROSS pages — sidebar background color changes between routes, header bar uses different hues on different pages, theme primary varies across the audit run, active-state color drifts. The per-cell probe records color fingerprints; scripts/check-cross-page-theme.cjs aggregates them after the run and emits findings."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
---

## Why this skill exists

The current per-cell theme-consistency probes (qa-detect-ux-theme-consistency, qa-detect-ux-card-consistency, etc.) compute a fresh "theme primary" per page. If Page A uses dark navy and Page B uses bright blue, each page is internally consistent — but the **brand identity drifts** as the user navigates.

This skill captures color fingerprints from key structural elements per cell. A post-run script (`scripts/check-cross-page-theme.cjs`) reads all cells' fingerprints, compares them, and emits drift findings.

## What it catches — 5 issue types (emitted by the aggregation script after the cell loop)

| issueType | severity | What |
|---|---|---|
| `sidebarColorDriftAcrossPages` | high | Sidebar background color hue drifts > 15° across cells (your two-shades-of-blue screenshot) |
| `headerColorDriftAcrossPages` | high | Page header / top-bar background hue drifts > 15° across cells |
| `themePrimaryDriftAcrossPages` | high | Detected theme primary hue drifts > 15° between any two cells — brand identity instability |
| `activeNavColorDriftAcrossPages` | medium | Active nav item highlight color drifts across cells |
| `cardBgDriftAcrossPages` | low | Card background tone drifts across cells |

## Per-cell probe (browser_evaluate)

Returns an array of **informational** records (issueType prefixed with `_meta_`) so they pass through the normal JSONL pipeline. The post-run script filters these and does the actual analysis.

```js
() => {
  function parseRGB(s) {
    if (!s) return null;
    const m = s.match(/rgba?\((\d+)\s*,\s*(\d+)\s*,\s*(\d+)(?:\s*,\s*([\d.]+))?\)/);
    if (!m) return null;
    return { r: +m[1], g: +m[2], b: +m[3], a: m[4] !== undefined ? +m[4] : 1 };
  }
  function rgbToHsl(r, g, b) {
    r /= 255; g /= 255; b /= 255;
    const max = Math.max(r, g, b), min = Math.min(r, g, b);
    let h = 0, s = 0; const l = (max + min) / 2;
    if (max !== min) {
      const d = max - min;
      s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
      switch (max) {
        case r: h = ((g - b) / d + (g < b ? 6 : 0)); break;
        case g: h = ((b - r) / d + 2); break;
        case b: h = ((r - g) / d + 4); break;
      }
      h *= 60;
    }
    return { h: Math.round(h), s: Math.round(s * 100), l: Math.round(l * 100) };
  }
  function isSaturated(rgb) {
    if (!rgb || rgb.a < 0.5) return false;
    const max = Math.max(rgb.r, rgb.g, rgb.b), min = Math.min(rgb.r, rgb.g, rgb.b);
    return max - min > 40 && max > 80;
  }
  function visible(el) {
    if (!el || el.nodeType !== 1) return false;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  }
  function fingerprintBgOf(selector) {
    const el = [...document.querySelectorAll(selector)].filter(visible)[0];
    if (!el) return null;
    const cs = getComputedStyle(el);
    const bg = parseRGB(cs.backgroundColor);
    if (!bg || !isSaturated(bg)) return null;
    return { rgb: bg, hsl: rgbToHsl(bg.r, bg.g, bg.b) };
  }
  function detectThemePrimary() {
    const samples = [];
    for (const b of document.querySelectorAll('button, .btn, .badge, thead, header, .navbar, [class*="primary"]')) {
      if (samples.length >= 12) break;
      if (!visible(b)) continue;
      const bg = parseRGB(getComputedStyle(b).backgroundColor);
      if (!isSaturated(bg)) continue;
      samples.push({ rgb: bg, hsl: rgbToHsl(bg.r, bg.g, bg.b) });
    }
    if (samples.length < 2) return null;
    const bins = new Map();
    for (const s of samples) {
      const bin = Math.round(s.hsl.h / 10) * 10;
      if (!bins.has(bin)) bins.set(bin, []);
      bins.get(bin).push(s);
    }
    let topBin = null, topN = 0;
    for (const [bin, arr] of bins) {
      if (arr.length > topN) { topN = arr.length; topBin = bin; }
    }
    if (topN < 2) return null;
    const dom = bins.get(topBin);
    const avgH = Math.round(dom.reduce((s, c) => s + c.hsl.h, 0) / dom.length);
    const avgS = Math.round(dom.reduce((s, c) => s + c.hsl.s, 0) / dom.length);
    const avgL = Math.round(dom.reduce((s, c) => s + c.hsl.l, 0) / dom.length);
    return { h: avgH, s: avgS, l: avgL, sampleCount: dom.length };
  }
  function detectActiveNavColor() {
    const candidates = [...document.querySelectorAll(
      '.active, .selected, .is-active, [aria-current="page"], [aria-current="true"], [class*="active"], [class*="--active"]'
    )].filter(visible);
    for (const c of candidates) {
      // Only consider nav-context active items
      if (!c.closest('nav, [role="navigation"], .sidebar, .side-nav, .menu, [class*="nav"], [class*="menu"]')) continue;
      const cs = getComputedStyle(c);
      const bg = parseRGB(cs.backgroundColor);
      if (isSaturated(bg)) return { rgb: bg, hsl: rgbToHsl(bg.r, bg.g, bg.b) };
    }
    return null;
  }
  function fingerprintCardBgs() {
    const tones = new Map();
    for (const c of document.querySelectorAll('.card, [class*="card"]:not([class*="card-header"]):not([class*="card-body"]), .panel')) {
      if (!visible(c)) continue;
      const cs = getComputedStyle(c);
      const bg = parseRGB(cs.backgroundColor);
      if (!bg || bg.a < 0.5) continue;
      // Off-white only (not saturated)
      if (bg.r > 220 && bg.g > 220 && bg.b > 220) {
        const key = bg.r + ',' + bg.g + ',' + bg.b;
        tones.set(key, (tones.get(key) || 0) + 1);
      }
    }
    return [...tones.entries()].map(([k, n]) => ({ rgb: k.split(',').map(Number), count: n }));
  }

  const fingerprints = {
    sidebar: fingerprintBgOf('.sidebar, .side-nav, [class*="sidenav"], aside.menu, nav.sidebar, [class*="sidebar"]'),
    header: fingerprintBgOf('header, [role="banner"], .header, .navbar, .top-bar, [class*="topbar"]'),
    themePrimary: detectThemePrimary(),
    activeNav: detectActiveNavColor(),
    cardBgTones: fingerprintCardBgs()
  };

  // Emit as a single informational finding so the orchestrator collects it
  // through the normal JSONL pipeline. The post-run script reads these
  // _meta_colorFingerprint records to do cross-cell analysis.
  return [{
    issueType: '_meta_colorFingerprint',
    severity: 'low',
    selector: 'body',
    description: 'cross-page-theme fingerprint',
    metadata: fingerprints
  }];
}
```

## Post-run aggregation script

After all cells complete (after Step 5.7.5 annotation sweep, before Step 7 bug filing), the orchestrator invokes:

```
node scripts/check-cross-page-theme.cjs <runId>
```

The script:
1. Reads every `.tmp/{runId}/issues/cell-*.jsonl`
2. Filters records where `issueType === '_meta_colorFingerprint'`
3. Groups by viewport (only compares cells with same viewportClass — desktop sidebars vs mobile sidebars are different)
4. For each fingerprint slot (sidebar, header, themePrimary, activeNav):
   - Computes hue variance across cells of the same viewport
   - If variance > 15° (high impact) or > 8° (medium) → emit drift finding
5. Writes findings to `.tmp/{runId}/issues/_cross-page-theme.jsonl`
6. Step 7 bug filer picks them up like any other findings

## Notes

- The probe is intentionally cheap (~3ms) — it just samples background colors
- The `_meta_` prefix on issueType signals informational records to the bug filer (it skips them — only the post-run script processes them)
- Viewport-isolated: mobile sidebars are compared only to other mobile sidebars (sidebars collapse on mobile, so cross-viewport noise is avoided)
- Self-skips when no sidebar/header/cards detected on the page
