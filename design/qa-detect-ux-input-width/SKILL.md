---
name: qa-detect-ux-input-width
section: visual
description: "Detects input/select/textarea fields that are too narrow relative to available container width: small input in a wide container, sibling fields with mismatched widths, textarea with same height as a single-line input. Catches the 'why are my inputs so tiny when there's space' bug class."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: true
requires: [hasInputs]
---

## What it catches — 5 issue types

| issueType | severity | What |
|---|---|---|
| `inputNarrowVsContainer` | medium | Input/select is < 50% of its container's content width AND container is > 200px wide (your Issue Date* field in narrow form when right side is empty) |
| `inputFixedWidthAtMobile` | medium | Input has a CSS `width` value > viewport width on mobile, or fixed `width: 200px` in a flexible container — overflow or under-fill |
| `siblingInputsWidthMismatch` | low | Sibling inputs in the same row have widths differing by > 20% — visual asymmetry |
| `textareaSingleRow` | low | `<textarea>` rendered as 1-row height (< 50px) — looks like an input but won't show multi-line content |
| `numberInputTooWideForDigits` | low | `input[type="number"]` rendered > 200px wide when typical value is < 8 digits — wasted horizontal space |

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

  // ── 1. Input narrow vs container ─────────────────────────────────────
  let narrowFlagged = 0;
  const inputs = [...document.querySelectorAll('input:not([type="hidden"]):not([type="checkbox"]):not([type="radio"]):not([type="submit"]):not([type="button"]), select, textarea')]
    .filter(visible);
  for (const inp of inputs) {
    if (narrowFlagged >= 4) break;
    if (inp.disabled || inp.readOnly) continue;
    const r = inp.getBoundingClientRect();
    if (r.width < 50) continue;
    // Find the nearest field-container or form
    const container = inp.closest('.form-field, .mat-form-field, .mat-mdc-form-field, .form-group, .field, .field-container, .input-group, .field-row, .mb-3, .mb-4, [class*="field-container"], [class*="form-control-wrapper"], [class*="input-wrapper"]');
    if (!container || !visible(container)) continue;
    const cr = container.getBoundingClientRect();
    if (cr.width < 200) continue;   // small container — narrow input is fine
    const ratio = r.width / cr.width;
    if (ratio < 0.5 && cr.width - r.width > 100) {
      // Make sure the container isn't a flex row with multiple fields side by side
      const siblings = [...(container.parentElement || document).children].filter(c => visible(c) && c !== container && (c.tagName === 'DIV' || c.tagName === 'LABEL'));
      let isSideBySide = false;
      for (const s of siblings) {
        const sr = s.getBoundingClientRect();
        if (Math.abs(sr.top - cr.top) < 8 && sr.left > cr.right - 10) {
          isSideBySide = true; break;
        }
      }
      if (isSideBySide) continue;
      narrowFlagged++;
      const labelTxt = (container.querySelector('label') || container).innerText.trim().slice(0, 30);
      out.push({
        issueType: 'inputNarrowVsContainer', severity: 'medium',
        selector: sel(inp), bbox: bb(inp),
        description: `Input "${labelTxt}" is ${r.width.toFixed(0)}px wide in a ${cr.width.toFixed(0)}px container (${Math.round(ratio*100)}%). Expand input to fill (width: 100% on the input or remove fixed widths).`
      });
    }
  }

  // ── 2. Input with fixed width that overflows or misaligns ────────────
  let fixedFlagged = 0;
  for (const inp of inputs) {
    if (fixedFlagged >= 2) break;
    const cs = getComputedStyle(inp);
    const inlineWidth = inp.style.width || '';
    const computedW = parseFloat(cs.width) || 0;
    const r = inp.getBoundingClientRect();
    // Fixed px width AND overflows viewport
    if (inlineWidth.endsWith('px') || /\d+px/.test(cs.width)) {
      const px = parseFloat(cs.width);
      if (px > vpW + 4) {
        fixedFlagged++;
        out.push({
          issueType: 'inputFixedWidthAtMobile', severity: 'medium',
          selector: sel(inp), bbox: bb(inp),
          description: `Input has fixed width: ${px}px but viewport is only ${vpW}px. Use width: 100% or max-width: 100% so it adapts.`
        });
      }
    }
  }

  // ── 3. Sibling inputs in row with mismatched widths ─────────────────
  let mismatchFlagged = 0;
  // Find rows of fields (siblings in same horizontal band)
  const containers = [...document.querySelectorAll('.row, .field-row, .form-row, [class*="row-grid"]')].filter(visible);
  for (const c of containers) {
    if (mismatchFlagged >= 2) break;
    const fields = [...c.querySelectorAll('input, select, textarea')].filter(visible);
    if (fields.length < 2) continue;
    const widths = fields.map(f => f.getBoundingClientRect().width).filter(w => w > 40);
    if (widths.length < 2) continue;
    const tops = fields.map(f => f.getBoundingClientRect().top);
    const sameBand = tops.every(t => Math.abs(t - tops[0]) < 8);
    if (!sameBand) continue;
    const maxW = Math.max(...widths);
    const minW = Math.min(...widths);
    if ((maxW - minW) / maxW > 0.2) {
      mismatchFlagged++;
      out.push({
        issueType: 'siblingInputsWidthMismatch', severity: 'low',
        selector: sel(c), bbox: bb(c),
        description: `Sibling inputs in same row have widths ${Math.round(minW)}-${Math.round(maxW)}px (${Math.round((maxW-minW)/maxW*100)}% variance). Use flex: 1 or fixed columns.`
      });
    }
  }

  // ── 4. Textarea rendered as single row ───────────────────────────────
  let textareaFlagged = 0;
  for (const ta of document.querySelectorAll('textarea')) {
    if (textareaFlagged >= 2) break;
    if (!visible(ta)) continue;
    const r = ta.getBoundingClientRect();
    if (r.height < 50) {
      textareaFlagged++;
      out.push({
        issueType: 'textareaSingleRow', severity: 'low',
        selector: sel(ta), bbox: bb(ta),
        description: `<textarea> rendered at ${r.height.toFixed(0)}px tall — looks like a single-line input. Set rows="3" or min-height: 80px to show it accepts multi-line input.`
      });
    }
  }

  // ── 5. Number input too wide for its typical use ────────────────────
  let numberWideFlagged = 0;
  for (const inp of document.querySelectorAll('input[type="number"]')) {
    if (numberWideFlagged >= 2) break;
    if (!visible(inp)) continue;
    const r = inp.getBoundingClientRect();
    const maxVal = inp.getAttribute('max');
    const expectedDigits = maxVal ? maxVal.length : 8;
    if (r.width > 200 && expectedDigits <= 8) {
      numberWideFlagged++;
      out.push({
        issueType: 'numberInputTooWideForDigits', severity: 'low',
        selector: sel(inp), bbox: bb(inp),
        description: `Number input is ${r.width.toFixed(0)}px wide but typical value is ${expectedDigits} digits. Constrain width to ~${expectedDigits * 12 + 24}px for balanced layout.`
      });
    }
  }

  return out;
}
```

## Notes

- Bounded: 4 narrow + 2 fixed + 2 mismatch + 2 textarea + 2 number = max ~12 findings per cell
- Self-skips: page with no inputs returns []
- Viewport-sensitive — narrowness shows up most clearly at desktop/laptop widths
- The `inputNarrowVsContainer` catches your Issue Date* field that's narrow while container has wide empty side
