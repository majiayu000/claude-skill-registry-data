---
name: qa-detect-ux-spacing
section: visual
description: "Catches inconsistent vertical/horizontal spacing — adjacent form fields with different gaps, card groups with mismatched padding, button rows with uneven spacing, headings inconsistently spaced from following content. Detects design-system breakage at the pixel level."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
---

## What it catches — 5 issue types

| issueType | severity | What |
|---|---|---|
| `formFieldGapInconsistent` | medium | Adjacent form fields in the same form use different vertical gaps (e.g. 8px between some, 24px between others) — visual rhythm broken |
| `buttonGroupGapUneven` | low | Button group has uneven horizontal gaps between buttons (some 4px, some 12px) |
| `cardGroupPaddingInconsistent` | low | Sibling cards in same group have different internal padding values |
| `headingFollowedNoBreathingRoom` | low | Heading immediately followed by content with margin-top < 4px — visual cramming |
| `headingOversizedBreathingRoom` | low | Heading followed by huge gap > 80px before content — disconnected visually |

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

  // ── 1. Form field gap inconsistency ───────────────────────────────────
  let formFlagged = 0;
  for (const form of document.querySelectorAll('form, [role="form"]')) {
    if (formFlagged >= 2) break;
    if (!visible(form)) continue;
    // Get visible field rows
    const fields = [...form.querySelectorAll('.form-group, .form-field, .field, .input-group, .mat-form-field, label, input:not([type="hidden"])')]
      .filter(visible);
    if (fields.length < 3) continue;
    // Compute vertical gaps between consecutive sibling fields
    const gaps = [];
    for (let i = 1; i < fields.length; i++) {
      const prev = fields[i-1].getBoundingClientRect();
      const cur = fields[i].getBoundingClientRect();
      if (cur.top <= prev.top) continue;   // wrapping or columned layout
      const gap = Math.round((cur.top - prev.bottom) / 2) * 2;
      if (gap > 0 && gap < 80) gaps.push(gap);
    }
    if (gaps.length < 3) continue;
    const unique = [...new Set(gaps)];
    if (unique.length >= 3) {
      const spread = Math.max(...gaps) - Math.min(...gaps);
      if (spread >= 6) {
        formFlagged++;
        out.push({
          issueType: 'formFieldGapInconsistent', severity: 'medium',
          selector: sel(form), bbox: bb(form),
          description: `Form field gaps range ${Math.min(...gaps)}-${Math.max(...gaps)}px across ${gaps.length} pairs (${unique.length} distinct values). Visual rhythm broken — pick one base spacing.`
        });
      }
    }
  }

  // ── 2. Button group gap unevenness ────────────────────────────────────
  let btnGroupFlagged = 0;
  for (const grp of document.querySelectorAll('.button-group, .btn-group, .actions, .button-row, [class*="btn-group"]')) {
    if (btnGroupFlagged >= 2) break;
    if (!visible(grp)) continue;
    const btns = [...grp.querySelectorAll('button, a.btn, [role="button"]')].filter(visible);
    if (btns.length < 3) continue;
    const rects = btns.map(b => b.getBoundingClientRect());
    const firstTop = rects[0].top;
    const sameRow = rects.filter(r => Math.abs(r.top - firstTop) < 6);
    if (sameRow.length < 3) continue;
    const gaps = [];
    for (let i = 1; i < sameRow.length; i++) {
      const gap = Math.round((sameRow[i].left - sameRow[i-1].right) / 2) * 2;
      if (gap > 0 && gap < 60) gaps.push(gap);
    }
    if (gaps.length < 2) continue;
    const spread = Math.max(...gaps) - Math.min(...gaps);
    if (spread > 4) {
      btnGroupFlagged++;
      out.push({
        issueType: 'buttonGroupGapUneven', severity: 'low',
        selector: sel(grp), bbox: bb(grp),
        description: `Button gaps in row: ${gaps.join(', ')}px. Uneven spacing — set consistent gap (e.g. 8px or 12px).`
      });
    }
  }

  // ── 3. Card group padding inconsistency ───────────────────────────────
  let cardPaddingFlagged = 0;
  for (const grp of document.querySelectorAll('.card-group, .row, .cards, .grid, [class*="grid"]')) {
    if (cardPaddingFlagged >= 2) break;
    if (!visible(grp)) continue;
    const cards = [...grp.querySelectorAll(':scope > .card, :scope > [class*="card"]')].filter(visible);
    if (cards.length < 2) continue;
    const paddings = cards.map(c => {
      const cs = getComputedStyle(c);
      return Math.round(parseFloat(cs.padding) || parseFloat(cs.paddingTop) || 0);
    }).filter(p => p > 0);
    if (paddings.length < 2) continue;
    const unique = [...new Set(paddings)];
    if (unique.length >= 2) {
      const spread = Math.max(...paddings) - Math.min(...paddings);
      if (spread >= 6) {
        cardPaddingFlagged++;
        out.push({
          issueType: 'cardGroupPaddingInconsistent', severity: 'low',
          selector: sel(grp), bbox: bb(grp),
          description: `Sibling cards have different padding: ${unique.join('px, ')}px. Use consistent padding for visual coherence.`
        });
      }
    }
  }

  // ── 4 + 5. Heading-content spacing ───────────────────────────────────
  let headingFlagged = 0;
  const headings = [...document.querySelectorAll('h1, h2, h3, h4, h5, h6')].filter(visible);
  for (const h of headings) {
    if (headingFlagged >= 3) break;
    const next = h.nextElementSibling;
    if (!next || !visible(next)) continue;
    const hr = h.getBoundingClientRect();
    const nr = next.getBoundingClientRect();
    if (nr.top <= hr.bottom) continue;   // overlap
    const gap = Math.round(nr.top - hr.bottom);
    const fontSize = parseFloat(getComputedStyle(h).fontSize) || 16;
    if (gap < 4) {
      headingFlagged++;
      out.push({
        issueType: 'headingFollowedNoBreathingRoom', severity: 'low',
        selector: sel(h), bbox: bb(h),
        description: `${h.tagName} "${(h.innerText || '').trim().slice(0, 30)}" has only ${gap}px before following content. Add margin-bottom (typically 0.5em-1em).`
      });
    } else if (gap > 80 && gap > fontSize * 5) {
      headingFlagged++;
      out.push({
        issueType: 'headingOversizedBreathingRoom', severity: 'low',
        selector: sel(h), bbox: bb(h),
        description: `${h.tagName} "${(h.innerText || '').trim().slice(0, 30)}" has ${gap}px before following content (${(gap/fontSize).toFixed(1)}× font-size). Heading reads as disconnected.`
      });
    }
  }

  return out;
}
```

## Notes

- Bounded: 2 form + 2 button-group + 2 card-padding + 3 heading = max ~9 findings
- Viewport-sensitive — spacing issues often manifest only at certain widths
- Skips wrapping/columned layouts safely (only flags actual vertical/horizontal sibling drift)
