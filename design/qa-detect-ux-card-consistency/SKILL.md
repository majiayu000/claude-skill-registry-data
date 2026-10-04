---
name: qa-detect-ux-card-consistency
section: visual
description: "Detects inconsistencies BETWEEN cards on the same page: mixed border-radius values, some cards with shadow and some without, different border colors, different background tones, mismatched widths in same row, mismatched heights with similar content. Catches the 'these cards look like they're from different design systems' bug class."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
requires: [hasCards]
---

## What it catches — 7 issue types

| issueType | severity | What |
|---|---|---|
| `cardBorderRadiusMixed` | medium | Cards on same page use 3+ distinct `border-radius` values (e.g. 4px, 8px, 16px) — pick one |
| `cardShadowMixed` | medium | Some cards have `box-shadow`, others don't — inconsistent visual depth |
| `cardBorderColorMixed` | low | Some cards bordered, others borderless, OR cards use different border colors |
| `cardBackgroundToneMixed` | low | Cards use 3+ different background tones (e.g. `#fff` vs `#f8fafc` vs `#fafafa`) — looks unintentional |
| `cardWidthMismatchInRow` | medium | Sibling cards in same row have widths differing by > 10% — visual asymmetry |
| `cardHeightMismatchInRow` | low | Sibling cards in same row have visibly different heights (> 20% delta) when content density is similar — uneven appearance |
| `cardInternalAsymmetry` | medium | Single card has > 25% difference between left padding and right padding (your Students > Navigator screenshot — extra space on left edge of form card) |

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
  function colorDelta(a, b) {
    if (!a || !b) return 999;
    return Math.abs(a.r - b.r) + Math.abs(a.g - b.g) + Math.abs(a.b - b.b);
  }
  const out = [];

  // Find card-like elements (have border / shadow / background, taller than a button)
  const cardSel = '.card, .panel, .mat-card, [class*="card"]:not([class*="card-header"]):not([class*="card-body"]):not([class*="card-footer"]):not([class*="card-title"]), [class*="panel"]:not([class*="panel-header"]):not([class*="panel-body"]), .surface, .tile, .box';
  let cards = [...document.querySelectorAll(cardSel)].filter(visible);
  // Deduplicate: only keep outermost cards (not nested card-inside-card)
  cards = cards.filter((c, i, arr) => !arr.some(o => o !== c && o.contains(c)));
  // Filter out trivially small cards (< 100px wide or < 40px tall)
  cards = cards.filter(c => {
    const r = c.getBoundingClientRect();
    return r.width >= 100 && r.height >= 40;
  });

  if (cards.length < 2) {
    // Even with 1 card, check internal asymmetry
    if (cards.length === 1) {
      const c = cards[0];
      const cs = getComputedStyle(c);
      const pL = parseFloat(cs.paddingLeft) || 0;
      const pR = parseFloat(cs.paddingRight) || 0;
      if (pL > 8 || pR > 8) {
        const delta = Math.abs(pL - pR);
        const maxP = Math.max(pL, pR);
        if (maxP > 0 && delta / maxP > 0.25 && delta > 8) {
          out.push({
            issueType: 'cardInternalAsymmetry', severity: 'medium',
            selector: sel(c), bbox: bb(c),
            description: `Card padding-left ${pL}px vs padding-right ${pR}px (${Math.round(delta/maxP*100)}% asymmetry). Content visually offset to one side.`
          });
        }
      }
    }
    return out;
  }

  // Collect style profiles
  const profiles = cards.map(c => {
    const cs = getComputedStyle(c);
    const r = c.getBoundingClientRect();
    return {
      el: c,
      radius: parseFloat(cs.borderTopLeftRadius) || 0,
      shadow: cs.boxShadow && cs.boxShadow !== 'none' ? cs.boxShadow : null,
      borderColor: parseFloat(cs.borderTopWidth) > 0 ? cs.borderTopColor : 'none',
      borderWidth: parseFloat(cs.borderTopWidth) || 0,
      bg: parseRGB(cs.backgroundColor),
      width: Math.round(r.width),
      height: Math.round(r.height),
      top: Math.round(r.top),
      paddingL: parseFloat(cs.paddingLeft) || 0,
      paddingR: parseFloat(cs.paddingRight) || 0
    };
  });

  // ── 1. Border-radius variance ───────────────────────────────────────
  const radii = [...new Set(profiles.map(p => Math.round(p.radius)))];
  if (radii.length >= 3 && Math.max(...radii) - Math.min(...radii) >= 4) {
    out.push({
      issueType: 'cardBorderRadiusMixed', severity: 'medium', selector: 'body',
      description: `Cards on page use ${radii.length} different border-radius values: ${radii.join('px, ')}px. Pick one corner radius for all cards.`
    });
  }

  // ── 2. Shadow variance ─────────────────────────────────────────────
  const withShadow = profiles.filter(p => p.shadow).length;
  const withoutShadow = profiles.length - withShadow;
  if (withShadow >= 1 && withoutShadow >= 1) {
    out.push({
      issueType: 'cardShadowMixed', severity: 'medium', selector: 'body',
      description: `Page has ${profiles.length} cards: ${withShadow} with box-shadow, ${withoutShadow} without. Inconsistent depth — apply shadow to ALL cards or NONE.`
    });
  }

  // ── 3. Border color / treatment variance ───────────────────────────
  const borderTreatments = new Set(profiles.map(p => p.borderWidth > 0 ? p.borderColor : 'none'));
  if (borderTreatments.size >= 3) {
    out.push({
      issueType: 'cardBorderColorMixed', severity: 'low', selector: 'body',
      description: `Cards use ${borderTreatments.size} different border treatments. Standardize border color + width or remove borders entirely.`
    });
  }

  // ── 4. Background tone variance ────────────────────────────────────
  // Cluster bg colors that are close to each other (within ΔRGB < 10)
  const bgClusters = [];
  for (const p of profiles) {
    if (!p.bg || p.bg.a < 0.3) continue;
    const matched = bgClusters.find(c => colorDelta(c, p.bg) < 10);
    if (!matched) bgClusters.push({ r: p.bg.r, g: p.bg.g, b: p.bg.b });
  }
  if (bgClusters.length >= 3) {
    out.push({
      issueType: 'cardBackgroundToneMixed', severity: 'low', selector: 'body',
      description: `Cards use ${bgClusters.length} different background tones (${bgClusters.slice(0,4).map(c => `rgb(${c.r},${c.g},${c.b})`).join(', ')}). Use one card background.`
    });
  }

  // ── 5 + 6. Width/Height mismatch in same row ───────────────────────
  // Group by top (within 12px = same row)
  const rows = {};
  for (const p of profiles) {
    const bin = Math.round(p.top / 12) * 12;
    if (!rows[bin]) rows[bin] = [];
    rows[bin].push(p);
  }
  let rowFlagged = 0;
  for (const top of Object.keys(rows)) {
    if (rowFlagged >= 2) break;
    const row = rows[top];
    if (row.length < 2) continue;
    const widths = row.map(p => p.width);
    const heights = row.map(p => p.height);
    const wMax = Math.max(...widths), wMin = Math.min(...widths);
    const hMax = Math.max(...heights), hMin = Math.min(...heights);
    if ((wMax - wMin) / wMax > 0.10 && wMax - wMin > 30) {
      rowFlagged++;
      out.push({
        issueType: 'cardWidthMismatchInRow', severity: 'medium',
        selector: sel(row[0].el), bbox: bb(row[0].el),
        description: `${row.length} cards in same row have widths ${wMin}-${wMax}px (${Math.round((wMax-wMin)/wMax*100)}% variance). Use a grid with equal columns.`
      });
    } else if ((hMax - hMin) / hMax > 0.20 && hMax - hMin > 40) {
      rowFlagged++;
      out.push({
        issueType: 'cardHeightMismatchInRow', severity: 'low',
        selector: sel(row[0].el), bbox: bb(row[0].el),
        description: `${row.length} cards in same row have heights ${hMin}-${hMax}px (${Math.round((hMax-hMin)/hMax*100)}% variance). Use align-items: stretch on the row.`
      });
    }
  }

  // ── 7. Internal padding asymmetry per card ─────────────────────────
  let asymFlagged = 0;
  for (const p of profiles) {
    if (asymFlagged >= 2) break;
    if (p.paddingL < 8 && p.paddingR < 8) continue;
    const delta = Math.abs(p.paddingL - p.paddingR);
    const maxP = Math.max(p.paddingL, p.paddingR);
    if (maxP > 8 && delta / maxP > 0.25 && delta > 8) {
      asymFlagged++;
      out.push({
        issueType: 'cardInternalAsymmetry', severity: 'medium',
        selector: sel(p.el), bbox: bb(p.el),
        description: `Card padding-left ${p.paddingL}px vs padding-right ${p.paddingR}px (${Math.round(delta/maxP*100)}% asymmetric). Content visually offset to one side.`
      });
    }
  }

  return out;
}
```

## Notes

- Bounded: max ~10 findings per cell
- Self-skips: page with 0 cards returns []
- Single-card pages still get the internal-asymmetry check (your Students > Navigator screenshot)
- The `cardInternalAsymmetry` catches the red-box bug in your Students > Navigator screenshot
- The other 6 issue types catch broader card inconsistencies you've shown on other pages
