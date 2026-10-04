---
name: qa-detect-ux-required-state
section: visual
description: "Detects ambiguous required-field state: required field with red border on load (looks like error), required indicated only by color with no text or programmatic marker (WCAG 1.4.1), required-only-marked-by-asterisk (no programmatic indicator), error class without message text, asterisk without legend."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
requires: [hasForms, hasRequiredFields]
---

## What it catches — 6 issue types

| issueType | severity | What |
|---|---|---|
| `requiredFieldErrorOnLoad` | high | Required field (`required`/`aria-required`) has red border on page load while empty — looks like a validation error before user has done anything |
| `requiredByColorOnly` | high | Field uses red border as the **sole** required indicator — no `*`, no `required` attr, no `aria-required` (WCAG 1.4.1 — color must not be the only means of conveying information). Exactly what the Issue Budget "Title" field does. |
| `requiredMarkerOnlyAsterisk` | medium | Field labeled with `*` but has no `required` attribute, no `aria-required="true"` — assistive tech can't detect it as required |
| `requiredAsteriskNoLegend` | low | Page has fields marked with `*` but no visible legend ("Required field", "* indicates required") explaining the convention |
| `errorClassNoErrorMessage` | medium | Field has class matching `error`/`invalid`/`ng-invalid` styling but no visible error message text near it — ambiguous (is something wrong? what?) |
| `errorBorderNoAriaInvalid` | low | Field visually styled as error but no `aria-invalid="true"` — screen-reader users have no signal |

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
  function isReddishBorder(rgb) {
    if (!rgb || rgb.a < 0.3) return false;
    // Reddish: r dominates, r >= 150, g/b < 100
    return rgb.r >= 150 && rgb.r > rgb.g + 50 && rgb.r > rgb.b + 50;
  }
  const out = [];

  // ── 1. Required field with error border on initial load ─────────────
  let errorOnLoadFlagged = 0;
  // Page-just-loaded heuristic: focused element is body OR no element has aria-activedescendant
  // The user hasn't interacted if no input has value AND not focused
  const requiredInputs = [...document.querySelectorAll('input[required], select[required], textarea[required], [aria-required="true"]')].filter(visible);
  for (const inp of requiredInputs) {
    if (errorOnLoadFlagged >= 3) break;
    if (inp.disabled || inp.readOnly) continue;
    const value = (inp.value || '').trim();
    if (value.length > 0) continue;     // user has typed
    // Has the field been touched? Heuristic: Angular adds .ng-touched, .ng-dirty
    const cls = (inp.className || '').toString();
    if (/\bng-touched\b|\btouched\b|\bdirty\b/.test(cls)) continue;
    // Check border color
    const cs = getComputedStyle(inp);
    const borderColor = parseRGB(cs.borderTopColor) || parseRGB(cs.borderBottomColor) || parseRGB(cs.borderLeftColor) || parseRGB(cs.borderRightColor);
    if (isReddishBorder(borderColor)) {
      errorOnLoadFlagged++;
      out.push({
        issueType: 'requiredFieldErrorOnLoad', severity: 'high',
        selector: sel(inp), bbox: bb(inp),
        description: `Required field has red/error border (rgb ${borderColor.r},${borderColor.g},${borderColor.b}) on initial load while empty. Looks like an error before user has done anything — use a neutral border + asterisk for required, reserve red for actual validation errors after submit.`
      });
    }
    // Also check the container (mat-form-field, .form-group, etc.)
    const container = inp.closest('.mat-form-field-wrapper, .form-group, .form-field, .field, .mat-mdc-form-field');
    if (container && visible(container)) {
      const ccs = getComputedStyle(container);
      const containerBorder = parseRGB(ccs.borderTopColor) || parseRGB(ccs.borderLeftColor);
      const containerOutline = parseRGB(ccs.outlineColor);
      if (isReddishBorder(containerBorder) || isReddishBorder(containerOutline)) {
        if (errorOnLoadFlagged < 3) {
          errorOnLoadFlagged++;
          out.push({
            issueType: 'requiredFieldErrorOnLoad', severity: 'high',
            selector: sel(container), bbox: bb(container),
            description: `Form field container has reddish border with empty required input. Pre-submit error state — not a real error.`
          });
        }
      }
    }
  }

  // ── 2. Required by color only (WCAG 1.4.1) ──────────────────────────
  // Field has reddish border on load but NO required attr and NO aria-required.
  // Color is the sole required indicator — invisible to colorblind users and screen readers.
  // Note: both requiredByColorOnly (high) and requiredMarkerOnlyAsterisk (medium) may fire on the
  // same element when a framework like Angular Material auto-injects * into the label DOM.
  // The dedup layer (cross_family_at_same_element=true) merges them and surfaces requiredByColorOnly
  // as winner (higher severity). No asterisk exclusion here.
  let colorOnlyFlagged = 0;
  const candidateInputs = [...document.querySelectorAll('input, select, textarea')].filter(visible);
  for (const inp of candidateInputs) {
    if (colorOnlyFlagged >= 5) break;
    if (inp.type === 'hidden' || inp.disabled || inp.readOnly) continue;
    // Skip fields that already have a programmatic required marker — they belong to check 1
    if (inp.hasAttribute('required') || inp.getAttribute('aria-required') === 'true') continue;
    const value = (inp.value || '').trim();
    if (value.length > 0) continue;
    const cls = (inp.className || '').toString();
    if (/\bng-touched\b|\btouched\b|\bdirty\b/.test(cls)) continue;

    // Check reddish border on the input itself
    const cs = getComputedStyle(inp);
    let borderRGB = parseRGB(cs.borderTopColor) || parseRGB(cs.borderBottomColor)
                  || parseRGB(cs.borderLeftColor) || parseRGB(cs.borderRightColor)
                  || parseRGB(cs.outlineColor);

    // Also check Angular Material / Bootstrap / generic component containers
    if (!isReddishBorder(borderRGB)) {
      const ctr = inp.closest('mat-form-field, .mat-mdc-form-field, .mat-form-field-wrapper, .form-group, .form-field, .field');
      if (ctr) {
        const ccs = getComputedStyle(ctr);
        borderRGB = parseRGB(ccs.borderTopColor) || parseRGB(ccs.borderLeftColor)
                  || parseRGB(ccs.outlineColor) || parseRGB(ccs.borderColor);
      }
    }
    if (!isReddishBorder(borderRGB)) continue;

    colorOnlyFlagged++;
    out.push({
      issueType: 'requiredByColorOnly',
      severity: 'high',
      selector: sel(inp),
      bbox: bb(inp),
      description: `Field appears required via red border (rgb ${borderRGB.r},${borderRGB.g},${borderRGB.b}) but has no required attribute, no aria-required="true", and no asterisk in its label — color is the sole required indicator (WCAG 1.4.1 violation). Add a visible * to the label AND set required/aria-required="true" so colorblind users and screen readers know this field is mandatory.`
    });
  }

  // ── 3. Asterisk-only required (no required attribute) ──────────────
  let asteriskOnlyFlagged = 0;
  const labels = document.querySelectorAll('label');
  for (const lbl of labels) {
    if (asteriskOnlyFlagged >= 3) break;
    if (!visible(lbl)) continue;
    const text = (lbl.innerText || '').trim();
    if (!/\*/.test(text)) continue;
    // Find associated input
    let inp = null;
    if (lbl.htmlFor) {
      inp = document.getElementById(lbl.htmlFor);
    }
    if (!inp) {
      inp = lbl.querySelector('input, select, textarea');
    }
    if (!inp || !visible(inp)) continue;
    const hasRequired = inp.hasAttribute('required');
    const hasAriaRequired = inp.getAttribute('aria-required') === 'true';
    if (!hasRequired && !hasAriaRequired) {
      asteriskOnlyFlagged++;
      out.push({
        issueType: 'requiredMarkerOnlyAsterisk', severity: 'medium',
        selector: sel(inp), bbox: bb(inp),
        description: `Label "${text.slice(0, 30)}" shows * but field has no required / aria-required="true". Screen readers don't announce it as required.`
      });
    }
  }

  // ── 4. Asterisks present without explanatory legend ─────────────────
  const asteriskCount = [...labels].filter(l => visible(l) && /\*/.test((l.innerText || '').trim())).length;
  if (asteriskCount >= 2) {
    // Look for an explanatory note
    const allText = document.body.innerText || '';
    const hasLegend = /\* ?(indicates|marks|denotes|is) ?required|required field|all fields marked with \*/i.test(allText);
    if (!hasLegend) {
      out.push({
        issueType: 'requiredAsteriskNoLegend', severity: 'low',
        selector: 'body',
        description: `Page has ${asteriskCount} fields marked with * but no visible legend explaining the convention. Add "* indicates required field" near the form.`
      });
    }
  }

  // ── 5. Error class but no error message text ────────────────────────
  let noMsgFlagged = 0;
  const errorFields = document.querySelectorAll('.ng-invalid.ng-touched, .invalid, .error, [aria-invalid="true"], .mat-form-field-invalid');
  for (const ef of errorFields) {
    if (noMsgFlagged >= 3) break;
    if (!visible(ef)) continue;
    // Find error message — usually a sibling
    const container = ef.closest('.form-field, .mat-form-field, .form-group, .field') || ef.parentElement;
    if (!container) continue;
    const msg = container.querySelector('.error-message, .invalid-feedback, .field-error, .mat-error, [class*="error-text"], [role="alert"]');
    if (msg && visible(msg) && (msg.innerText || '').trim().length > 2) continue;   // has message
    noMsgFlagged++;
    out.push({
      issueType: 'errorClassNoErrorMessage', severity: 'medium',
      selector: sel(ef), bbox: bb(ef),
      description: `Field has error styling (class or aria-invalid) but no visible error message nearby. Users see red but don't know what's wrong.`
    });
  }

  // ── 6. Error border but no aria-invalid ─────────────────────────────
  let noAriaFlagged = 0;
  const allInputs = document.querySelectorAll('input, select, textarea');
  for (const inp of allInputs) {
    if (noAriaFlagged >= 3) break;
    if (!visible(inp)) continue;
    const cs = getComputedStyle(inp);
    const borderColor = parseRGB(cs.borderTopColor) || parseRGB(cs.borderBottomColor);
    if (!isReddishBorder(borderColor)) continue;
    if (inp.getAttribute('aria-invalid') === 'true') continue;
    // Also check parent for mat-form-field-invalid class
    const matInvalidParent = inp.closest('.mat-form-field-invalid, .ng-invalid');
    if (matInvalidParent && matInvalidParent.getAttribute('aria-invalid') === 'true') continue;
    noAriaFlagged++;
    out.push({
      issueType: 'errorBorderNoAriaInvalid', severity: 'low',
      selector: sel(inp), bbox: bb(inp),
      description: `Input visually styled as error (red border rgb ${borderColor.r},${borderColor.g},${borderColor.b}) but no aria-invalid="true". Screen-reader users have no signal.`
    });
  }

  return out;
}
```

## Notes

- Bounded: 3 error-on-load + 5 color-only + 3 asterisk-only + 1 legend + 3 no-msg + 3 no-aria = max ~18
- Self-skips: page with no inputs / no reddish borders / no asterisks returns []
- `requiredByColorOnly` and `requiredMarkerOnlyAsterisk` may both fire on the same element (e.g. Angular Material auto-injects `*` into labels via `mat-mdc-form-field-required-marker`). The dedup layer (`cross_family_at_same_element=true`) merges them and surfaces `requiredByColorOnly` (high) as winner
- `requiredFieldErrorOnLoad` fires when field HAS `required` attr + red border on load (pre-submit error styling); `requiredByColorOnly` fires when NO `required` attr at all (color is the complete indicator)
