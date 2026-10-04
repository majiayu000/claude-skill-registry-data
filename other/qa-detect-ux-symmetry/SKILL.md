---
name: qa-detect-ux-symmetry
section: visual
description: "Measures layout symmetry — left vs right padding of containers, card-row alignment, primary-section balance. Catches visual asymmetry that users see immediately (e.g. content offset to one side, cards with mismatched edges) but no other skill measures. Deterministic, no Sonnet."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: true
---

## What it catches — 6 issue types

| issueType | severity | What |
|---|---|---|
| `containerAsymmetry` | medium | Main content container has left padding very different from right padding (>20% delta) — content appears off-center |
| `cardRowEdgeMismatch` | low | Sibling cards in same row have left edges or right edges misaligned by > 4px |
| `cardWidthInconsistent` | low | Sibling cards in same row have widths differing by > 10% |
| `marginDriftBetweenSections` | low | Adjacent sections have inconsistent left margin (visual "drift") |
| `oneSidedScrollIndicator` | medium | Scrollbar/indicator (`ng-scrollbar`, `.scroll-indicator`) only appears on one side, creating visible left/right imbalance |
| `viewportOffsetLeft` | medium | Main content offset > 24px from horizontal center on viewports where centered layout is expected |

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
  const out = [];
  const visible = el => {
    if (!el || el.nodeType !== 1) return false;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  };

  // ── 1. Container asymmetry — main content padding L vs R ──────────────
  const mains = document.querySelectorAll('main, [role="main"], .main-content, .content-area, .page-content, body > .container, body > div > .container');
  let containerFlagged = 0;
  for (const m of mains) {
    if (containerFlagged >= 2) break;
    if (!visible(m)) continue;
    const cs = getComputedStyle(m);
    const pL = parseFloat(cs.paddingLeft) || 0;
    const pR = parseFloat(cs.paddingRight) || 0;
    if (pL < 8 && pR < 8) continue;
    const delta = Math.abs(pL - pR);
    const max = Math.max(pL, pR);
    if (max > 16 && delta / max > 0.2) {
      containerFlagged++;
      out.push({
        issueType: 'containerAsymmetry', severity: 'medium', selector: sel(m), bbox: bb(m),
        description: `Container padding-left ${pL}px vs padding-right ${pR}px (${Math.round(delta/max*100)}% off). Content appears off-center to users.`
      });
    }
  }

  // ── 2. Card row edges + width consistency ─────────────────────────────
  const cardGroups = document.querySelectorAll('.row, .cards, .card-grid, [class*="grid-row"], [class*="card-row"]');
  let edgeFlagged = 0, widthFlagged = 0;
  for (const grp of cardGroups) {
    if (edgeFlagged + widthFlagged >= 4) break;
    if (!visible(grp)) continue;
    const cards = [...grp.children].filter(visible);
    if (cards.length < 2) continue;
    const rects = cards.map(c => c.getBoundingClientRect()).filter(r => r.top > 0);
    if (rects.length < 2) continue;
    // Only siblings in same row (same top within 4px)
    const firstTop = rects[0].top;
    const sameRow = rects.filter(r => Math.abs(r.top - firstTop) < 6);
    if (sameRow.length < 2) continue;
    const lefts = sameRow.map(r => r.left);
    const rights = sameRow.map(r => r.right);
    const widths = sameRow.map(r => r.width);
    const lDelta = Math.max(...lefts) - Math.min(...lefts);
    const rDelta = Math.max(...rights) - Math.min(...rights);
    const wDelta = Math.max(...widths) - Math.min(...widths);
    if (lDelta > 4 || rDelta > 4) {
      edgeFlagged++;
      out.push({
        issueType: 'cardRowEdgeMismatch', severity: 'low', selector: sel(grp), bbox: bb(grp),
        description: `${sameRow.length} sibling cards have ${lDelta > 4 ? 'left-edge ' + lDelta.toFixed(0) + 'px' : ''}${(lDelta > 4 && rDelta > 4) ? ' and ' : ''}${rDelta > 4 ? 'right-edge ' + rDelta.toFixed(0) + 'px' : ''} drift. Visual misalignment.`
      });
    }
    if (widths.length >= 2 && wDelta / Math.max(...widths) > 0.10) {
      widthFlagged++;
      out.push({
        issueType: 'cardWidthInconsistent', severity: 'low', selector: sel(grp), bbox: bb(grp),
        description: `Sibling cards widths range ${Math.min(...widths).toFixed(0)}-${Math.max(...widths).toFixed(0)}px (${Math.round(wDelta/Math.max(...widths)*100)}% variance). Looks unintentional.`
      });
    }
  }

  // ── 3. Margin drift between adjacent sections ─────────────────────────
  const sections = [...document.querySelectorAll('section, .section, [class*="section-"]')].filter(visible);
  let driftFlagged = 0;
  for (let i = 1; i < sections.length && driftFlagged < 2; i++) {
    const a = sections[i-1].getBoundingClientRect();
    const b = sections[i].getBoundingClientRect();
    const lDrift = Math.abs(a.left - b.left);
    if (lDrift > 8 && lDrift < 200) {
      driftFlagged++;
      out.push({
        issueType: 'marginDriftBetweenSections', severity: 'low',
        selector: sel(sections[i]), bbox: bb(sections[i]),
        description: `Section left edge drifted ${lDrift.toFixed(0)}px from previous section. Vertical "stair-step" visual.`
      });
    }
  }

  // ── 4. One-sided scroll indicator (creates visual imbalance) ──────────
  const scrollEls = document.querySelectorAll('ng-scrollbar, .scroll-indicator, [class*="scrollbar"], [class*="scroll-track"]');
  let scrollFlagged = 0;
  for (const s of scrollEls) {
    if (scrollFlagged >= 1) break;
    if (!visible(s)) continue;
    const r = s.getBoundingClientRect();
    const vpW = window.innerWidth;
    // Only flag if it sits in right 10% of viewport (the asymmetric pattern)
    if (r.left > vpW * 0.85 && r.width < 24) {
      // Check if there's a matching indicator on the left — if not, it's asymmetric
      const leftMatch = [...scrollEls].find(e => {
        const er = e.getBoundingClientRect();
        return er.right < vpW * 0.15 && er.width < 24 && visible(e);
      });
      if (!leftMatch) {
        scrollFlagged++;
        out.push({
          issueType: 'oneSidedScrollIndicator', severity: 'medium',
          selector: sel(s), bbox: bb(s),
          description: 'Scroll indicator visible on right edge but no matching indicator/element on left. Creates visible vertical asymmetry that users perceive as broken layout.'
        });
      }
    }
  }

  // ── 5. Viewport offset — main content not horizontally centered ───────
  const vpW = window.innerWidth;
  // Look for the primary content wrapper
  const wrap = document.querySelector('main, [role="main"], .main-content, .content-area, body > .container');
  if (wrap && visible(wrap)) {
    const r = wrap.getBoundingClientRect();
    const expectedCenter = vpW / 2;
    const actualCenter = r.left + r.width / 2;
    const offset = Math.abs(expectedCenter - actualCenter);
    // Only flag on wide viewports where centering is the convention (>= 1024px)
    if (vpW >= 1024 && offset > 24 && r.width < vpW * 0.95) {
      out.push({
        issueType: 'viewportOffsetLeft', severity: 'medium',
        selector: sel(wrap), bbox: bb(wrap),
        description: `Main content offset ${offset.toFixed(0)}px from viewport center (viewport ${vpW}px, content ${r.width.toFixed(0)}px). Reads as off-balance.`
      });
    }
  }

  return out;
}
```

## Notes

- Bounded: max 2 containerAsymmetry, 4 card edge/width, 2 section drifts, 1 scroll indicator, 1 viewport offset per cell
- Self-skips when no matching containers/cards/sections exist on the page
- Viewport-sensitive: catches the symmetry issues that only manifest at specific widths
- Zero Sonnet cost; runs in batched Haiku call
