---
name: qa-detect-ux-selected-color-mix
section: visual
description: "Detects multiple different colors used for SELECTED/ACTIVE/HIGHLIGHTED indicators in the same UI region (e.g. calendar with 'today' in light purple, 'month' view in dark purple, '5' date in blue — three different colors all conveying 'selected'). Catches the 'same widget uses 3 shades for the same concept' bug class."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
requires: [hasNavigation, hasTabs]
---

## What it catches — 4 issue types

| issueType | severity | What |
|---|---|---|
| `selectedIndicatorMultiHue` | medium | A single UI region (calendar, toolbar, card, list) has 3+ "selected/active/highlighted" elements using distinct saturated colors (Δhue > 12° between any pair). Users get confused about what "selected" means here |
| `selectedShadeDriftSameHue` | low | Same hue but 3+ noticeably different lightness/saturation values used for selected states in same region (e.g. 3 shades of purple). Looks unintentional |
| `selectedFillVsOutlineMix` | low | One selected element uses filled background, another uses outline/border — same meaning, different visual treatment |
| `selectedShapeMixedInGroup` | low | Selected indicators use mixed shapes (circle for one, rectangle for another, underline for a third) in the same group |

## Probe (browser_evaluate)

```js
() => {
  const sel = el => {
    const id = el.id ? '#' + el.id : '';
    const cls = (el.className && typeof el.className === 'string')
      ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
    return (el.tagName.toLowerCase() + id + cls).slice(0, 120);
  };
  const bb = el => {
    const r = el.getBoundingClientRect();
    return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) };
  };
  const visible = el => {
    if (!el || el.nodeType !== 1) return false;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  };
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
    return { h, s: s * 100, l: l * 100 };
  }
  function hueDelta(a, b) { const d = Math.abs(a - b) % 360; return d > 180 ? 360 - d : d; }
  function isSaturatedBg(rgb) {
    if (!rgb || rgb.a < 0.5) return false;
    const max = Math.max(rgb.r, rgb.g, rgb.b), min = Math.min(rgb.r, rgb.g, rgb.b);
    return max - min > 50 && max > 100;   // saturated, not greyscale
  }
  const out = [];

  // ── Find candidate UI regions: widget-like containers ────────────────
  const regions = [...document.querySelectorAll(
    '[role="toolbar"], [role="tablist"], .toolbar, .calendar, [class*="calendar"], .datepicker, [class*="datepicker"], .fc-toolbar, .fc-view, .button-group, .btn-group, .actions, [class*="action-bar"], .card, .panel'
  )].filter(visible);

  for (const region of regions.slice(0, 6)) {
    // Find "selected/active/highlighted" elements inside this region
    const selectedSel = '.active, .selected, .is-active, .is-selected, .highlighted, [aria-selected="true"], [aria-current="true"], [aria-current="page"], [aria-current="date"], .today, .fc-day-today, .mat-calendar-body-selected, .ng-star-inserted.active, [class*="--active"], [class*="--selected"]';
    let selectedEls = [...region.querySelectorAll(selectedSel)].filter(visible);

    // Also include elements with bg color noticeably different from siblings (visually-active heuristic)
    // Look at button groups — pick the one with the most saturated background
    if (selectedEls.length < 2) {
      const btns = [...region.querySelectorAll('button, a, [role="button"], [role="tab"]')].filter(visible);
      const saturated = btns.filter(b => {
        const bg = parseRGB(getComputedStyle(b).backgroundColor);
        return isSaturatedBg(bg);
      });
      if (saturated.length >= 2 && saturated.length < btns.length) {
        selectedEls = [...selectedEls, ...saturated.filter(s => !selectedEls.includes(s))];
      }
    }

    if (selectedEls.length < 2) continue;

    // Collect background colors of selected elements
    const colors = [];
    for (const el of selectedEls) {
      const cs = getComputedStyle(el);
      let bg = parseRGB(cs.backgroundColor);
      // If transparent, check the element itself for distinct color (e.g. circle inside)
      if (!bg || bg.a < 0.5) {
        const innerSat = el.querySelector('[style*="background"], [class*="selected"], [class*="active"], .circle, .indicator');
        if (innerSat) bg = parseRGB(getComputedStyle(innerSat).backgroundColor);
      }
      if (!bg || !isSaturatedBg(bg)) continue;
      const hsl = rgbToHsl(bg.r, bg.g, bg.b);
      colors.push({ el, bg, hsl });
    }
    if (colors.length < 2) continue;

    // ── 1. Multi-hue (3+ distinct hues, Δ > 20°) ─────────────────────────
    const hues = [];
    for (const c of colors) {
      const found = hues.find(h => hueDelta(h.h, c.hsl.h) < 12);
      if (!found) hues.push({ h: c.hsl.h, count: 1 });
      else found.count++;
    }
    if (hues.length >= 3) {
      out.push({
        issueType: 'selectedIndicatorMultiHue', severity: 'medium',
        selector: sel(region), bbox: bb(region),
        description: `Region has ${colors.length} "selected/active" elements using ${hues.length} distinct hues (${hues.map(h => Math.round(h.h) + '°').join(', ')}). Users can't tell which color means "selected" — pick ONE.`
      });
      continue;   // don't double-flag with shade-drift
    }

    // ── 2. Same hue, different shades ────────────────────────────────────
    if (hues.length === 1 && colors.length >= 3) {
      const lightness = colors.map(c => c.hsl.l);
      const saturation = colors.map(c => c.hsl.s);
      const lDelta = Math.max(...lightness) - Math.min(...lightness);
      const sDelta = Math.max(...saturation) - Math.min(...saturation);
      if (lDelta > 12 || sDelta > 12) {
        out.push({
          issueType: 'selectedShadeDriftSameHue', severity: 'low',
          selector: sel(region), bbox: bb(region),
          description: `Region uses ${colors.length} different shades of hue ${Math.round(hues[0].h)}° for "selected" states (L: ${Math.round(Math.min(...lightness))}-${Math.round(Math.max(...lightness))}%, S: ${Math.round(Math.min(...saturation))}-${Math.round(Math.max(...saturation))}%). Standardize to one shade.`
        });
      }
    }

    // ── 3. Fill vs outline mix ───────────────────────────────────────────
    if (selectedEls.length >= 2) {
      let filled = 0, outlined = 0;
      for (const el of selectedEls) {
        const cs = getComputedStyle(el);
        const bg = parseRGB(cs.backgroundColor);
        const hasFill = isSaturatedBg(bg);
        const borderColor = parseRGB(cs.borderTopColor);
        const hasOutline = !hasFill && isSaturatedBg(borderColor) && parseFloat(cs.borderTopWidth) >= 1;
        if (hasFill) filled++;
        if (hasOutline) outlined++;
      }
      if (filled >= 1 && outlined >= 1) {
        out.push({
          issueType: 'selectedFillVsOutlineMix', severity: 'low',
          selector: sel(region), bbox: bb(region),
          description: `Region mixes ${filled} filled-background and ${outlined} outlined "selected" indicators. Pick one visual treatment.`
        });
      }
    }

    // ── 4. Shape mixed in group ──────────────────────────────────────────
    if (selectedEls.length >= 2) {
      const radii = selectedEls.map(el => {
        const cs = getComputedStyle(el);
        const r = parseFloat(cs.borderTopLeftRadius) || 0;
        const rect = el.getBoundingClientRect();
        // Round (circle if border-radius >= 50% of width)
        if (r >= Math.min(rect.width, rect.height) / 2 - 1) return 'circle';
        if (r > 12) return 'pill';
        if (r > 2) return 'rounded-rect';
        return 'rect';
      });
      const shapeSet = new Set(radii);
      if (shapeSet.size >= 3) {
        out.push({
          issueType: 'selectedShapeMixedInGroup', severity: 'low',
          selector: sel(region), bbox: bb(region),
          description: `Region uses ${shapeSet.size} different shapes for "selected" indicators: ${[...shapeSet].join(', ')}. Standardize the indicator shape.`
        });
      }
    }
  }

  return out;
}
```

## Notes

- Bounded: 4 issue types × up to 6 regions = max ~24 findings per cell
- Self-skips: page with no widget regions returns []
- The `selectedIndicatorMultiHue` catches your Calendar widget: today (~270° light purple), month (~250° dark purple), 5 (~210° blue) — 3 distinct hues for "selected" indicators
- Hue clustering (Δ < 20°) prevents false positives for minor color variations
