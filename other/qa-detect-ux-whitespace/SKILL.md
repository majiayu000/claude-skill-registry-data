---
name: qa-detect-ux-whitespace
section: visual
description: "Detects layouts that waste horizontal space — forms rendered in less than 50% of available width, content blocks with huge empty side margins, main areas occupying less than 60% of viewport width on desktop. Catches the 'why is half my screen empty' bug class your Fee Navigator and Add Item screenshots show."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: true
---

## What it catches — 5 issue types

| issueType | severity | What |
|---|---|---|
| `formUsesLessThanHalfWidth` | medium | Form occupies < 50% of available container/viewport width with no visible decoration on the empty side (no chart, no side panel) — wasted screen space (your Add Item screenshot) |
| `contentLowViewportOccupancy` | low | Main content block occupies < 60% of viewport width on a desktop/laptop viewport (≥ 1024px) — content feels cramped in a wide screen |
| `excessiveLeftMargin` | medium | Main container has > 25% empty space on the left side (no sidebar, no chrome) — content visually offset right |
| `excessiveRightMargin` | medium | Main container has > 25% empty space on the right side (no panel, no sidebar) — content visually offset left (your Fee Navigator screenshot) |
| `formFieldsStackedNarrow` | low | Form fields stacked vertically when they would naturally fit 2 or 3 per row at current viewport width — wasted horizontal space |

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
  const out = [];
  const vpW = window.innerWidth;

  // ── 1. Form uses < 50% of available container width ──────────────────
  let formFlagged = 0;
  const forms = [...document.querySelectorAll('form, [role="form"], .form, .mat-dialog-content form')].filter(visible);
  for (const f of forms.slice(0, 3)) {
    if (formFlagged >= 2) break;
    const fr = f.getBoundingClientRect();
    if (fr.width < 100 || fr.height < 60) continue;
    // Find the form's container (immediate parent or nearest card)
    const wrap = f.closest('.card, .card-body, .panel, .dialog-content, [class*="dialog"], main, [role="main"], .content') || f.parentElement;
    if (!wrap || !visible(wrap)) continue;
    const wr = wrap.getBoundingClientRect();
    if (wr.width < 200) continue;
    const ratio = fr.width / wr.width;
    if (ratio < 0.5 && wr.width - fr.width > 100) {
      // Check the empty side isn't filled with anything meaningful.
      // Look for visible elements whose bbox sits ENTIRELY within the empty area
      // (not overlapping with the form).
      const emptySpaceLeft = fr.left - wr.left;
      const emptySpaceRight = wr.right - fr.right;
      const biggerEmpty = Math.max(emptySpaceLeft, emptySpaceRight);
      const emptyOnLeft = emptySpaceLeft > emptySpaceRight;
      const emptyRect = emptyOnLeft
        ? { left: wr.left, right: fr.left, top: wr.top, bottom: wr.bottom }
        : { left: fr.right, right: wr.right, top: wr.top, bottom: wr.bottom };
      let hasContentInEmpty = false;
      // Scan all elements with text in the wrap
      const candidates = [...wrap.querySelectorAll('img, button, a, h1, h2, h3, h4, h5, h6, p, table, [class*="chart"], [class*="panel"], [class*="aside"]')]
        .filter(e => visible(e) && !f.contains(e) && e !== f);
      for (const c of candidates) {
        const r = c.getBoundingClientRect();
        // Element bbox entirely inside emptyRect
        if (r.left >= emptyRect.left - 4 && r.right <= emptyRect.right + 4 &&
            r.top >= emptyRect.top - 4 && r.bottom <= emptyRect.bottom + 4) {
          hasContentInEmpty = true;
          break;
        }
      }
      if (!hasContentInEmpty) {
        formFlagged++;
        out.push({
          issueType: 'formUsesLessThanHalfWidth', severity: 'medium',
          selector: sel(f), bbox: bb(f),
          description: `Form occupies ${fr.width.toFixed(0)}px of ${wr.width.toFixed(0)}px container (${Math.round(ratio*100)}%) — ${biggerEmpty.toFixed(0)}px empty side with no other content. Expand form to fill or place useful content beside it.`
        });
      }
    }
  }

  // ── 2. Main content low viewport occupancy ──────────────────────────
  if (vpW >= 1024) {
    const main = document.querySelector('main, [role="main"], .main-content, .content-area, body > .container');
    if (main && visible(main)) {
      const r = main.getBoundingClientRect();
      if (r.width > 100) {
        const ratio = r.width / vpW;
        if (ratio < 0.6) {
          out.push({
            issueType: 'contentLowViewportOccupancy', severity: 'low',
            selector: sel(main), bbox: bb(main),
            description: `Main content uses only ${r.width.toFixed(0)}px of ${vpW}px viewport (${Math.round(ratio*100)}%). On wide screens, expand main or add complementary content beside it.`
          });
        }
      }
    }
  }

  // ── 3 + 4. Excessive left/right margin on main containers ───────────
  const mainCandidates = [...document.querySelectorAll('main, [role="main"], .main-content, .content-area, .page-content, .container, body > div')]
    .filter(visible)
    .slice(0, 5);
  let leftMarginFlagged = 0, rightMarginFlagged = 0;
  for (const m of mainCandidates) {
    if (leftMarginFlagged + rightMarginFlagged >= 2) break;
    const cs = getComputedStyle(m);
    const pL = parseFloat(cs.paddingLeft) || 0;
    const pR = parseFloat(cs.paddingRight) || 0;
    const mL = parseFloat(cs.marginLeft) || 0;
    const mR = parseFloat(cs.marginRight) || 0;
    // Look at the container's child content area
    const childContent = [...m.children].filter(visible)[0];
    if (!childContent) continue;
    const mr = m.getBoundingClientRect();
    const cr = childContent.getBoundingClientRect();
    if (mr.width < 400) continue;
    const leftGap = cr.left - mr.left;
    const rightGap = mr.right - cr.right;
    // Skip if there's a sidebar in the gap
    const leftHasSidebar = leftGap > 100 && document.elementFromPoint(mr.left + leftGap/2, mr.top + 100) !== document.body;
    const rightHasSidebar = rightGap > 100 && document.elementFromPoint(mr.right - rightGap/2, mr.top + 100) !== document.body;

    if (leftMarginFlagged < 1 && leftGap > mr.width * 0.25 && leftGap > 80 && !leftHasSidebar) {
      leftMarginFlagged++;
      out.push({
        issueType: 'excessiveLeftMargin', severity: 'medium',
        selector: sel(m), bbox: bb(m),
        description: `Container has ${leftGap.toFixed(0)}px empty space on left (${Math.round(leftGap/mr.width*100)}% of width) with no visible sidebar or decoration. Content visually offset right.`
      });
    }
    if (rightMarginFlagged < 1 && rightGap > mr.width * 0.25 && rightGap > 80 && !rightHasSidebar) {
      rightMarginFlagged++;
      out.push({
        issueType: 'excessiveRightMargin', severity: 'medium',
        selector: sel(m), bbox: bb(m),
        description: `Container has ${rightGap.toFixed(0)}px empty space on right (${Math.round(rightGap/mr.width*100)}% of width) with no visible sidebar or decoration. Content visually offset left.`
      });
    }
  }

  // ── 5. Form fields stacked when they could be side-by-side ──────────
  if (vpW >= 768) {
    let stackedFlagged = 0;
    for (const f of forms) {
      if (stackedFlagged >= 1) break;
      if (!visible(f)) continue;
      const fields = [...f.querySelectorAll('.form-field, .mat-form-field, .form-group, .field, input:not([type="hidden"])')]
        .filter(visible);
      if (fields.length < 4) continue;
      // Compute average field width and form width
      const fr = f.getBoundingClientRect();
      if (fr.width < 600) continue;   // narrow form is fine
      const widths = fields.map(x => x.getBoundingClientRect().width).filter(w => w > 60);
      if (widths.length < 4) continue;
      const avgW = widths.reduce((a,b) => a+b, 0) / widths.length;
      // If fields are tall (stacked one per row) AND would fit 2-3 per row
      const couldFitPerRow = Math.floor(fr.width / (avgW + 24));
      const fieldsPerRow = (() => {
        const tops = new Set(fields.map(x => Math.round(x.getBoundingClientRect().top)));
        return fields.length / Math.max(tops.size, 1);
      })();
      if (couldFitPerRow >= 2 && fieldsPerRow < 1.5) {
        stackedFlagged++;
        out.push({
          issueType: 'formFieldsStackedNarrow', severity: 'low',
          selector: sel(f), bbox: bb(f),
          description: `Form has ${fields.length} fields stacked vertically but viewport (${vpW}px) and field width (~${avgW.toFixed(0)}px) would fit ${couldFitPerRow} fields per row. Use a 2-column or 3-column layout.`
        });
      }
    }
  }

  return out;
}
```

## Notes

- Bounded: 2 form-narrow + 1 viewport + 2 margin + 1 stacked = max ~6 findings per cell
- Self-skips: page with no forms / no main container returns []
- Viewport-sensitive — different bugs appear at mobile/tablet/laptop/desktop
- The `formUsesLessThanHalfWidth` catches your Add Item screenshot (form on left half only)
- The `excessiveLeftMargin` / `excessiveRightMargin` catch your Fee Navigator screenshot (red vertical bars on sides)
