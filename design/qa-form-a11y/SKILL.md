---
name: qa-form-a11y
section: interactive
description: "Consolidated form accessibility skill. Owns labels, aria, fieldset legend, error announcement, required-field indication, focus order, password show/hide. Replaces qa-detect-form-a11y plus a11y-portions of qa-detect-forms."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
interactive: false
cacheVersion: "1.0.0"
ownership: "exclusive: any accessibility finding on a form input/label/error/fieldset belongs to this skill"
replaces:
  - qa-detect-form-a11y
  - "portions of qa-detect-forms (fieldWithoutLabel, passwordNoToggle)"
requires: [hasForms, hasInputs]
---

# qa-form-a11y — Consolidated Form Accessibility Skill

Single skill owning ALL form-related accessibility findings. No other skill emits a11y findings on form elements.

## What it checks (6 issue types)

| issueType | severity | catches |
|---|---|---|
| `fieldWithoutLabel` | high | Input/textarea/select with no label, aria-label, aria-labelledby, title, or placeholder |
| `errorNotAnnounced` | high | Error container missing `role="alert"` or `aria-live` — screen readers don't announce |
| `requiredNotIndicated` | medium | Required field (by `required` attr OR by red border on load) with no visible asterisk AND no `aria-required="true"` — covers both explicit-required and color-only-required fields |
| `fieldsetNoLegend` | medium | `<fieldset>` without `<legend>` — radio/checkbox group label invisible |
| `focusOrderMismatch` | medium | Tab focus order does not match visual top-to-bottom order |
| `passwordNoToggle` | medium | Password field has no show/hide toggle nearby |

## Self-skip
Single passive `browser_evaluate`. Returns `[]` if no forms / inputs / errors found.

## Probe (browser_evaluate)
```js
() => {
  const sel = el => (el.tagName.toLowerCase() + (el.id ? `#${el.id}` : '')).slice(0,120);
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };
  const out = [];
  const skipTypes = new Set(['hidden','submit','reset','button','image','checkbox','radio']);

  // Detect floating/contextual labels used by UI component libraries.
  // These libraries position a <label> visually inside the input (looks like placeholder),
  // which floats up on focus. The label IS there — just not always linked via for/id.
  // Without this check, every MUI / Ant Design / Chakra / Vuetify input fires a false positive.
  const hasContextualLabel = el => {
    // 1. MUI: <FormControl class="MuiFormControl-root"><label class="MuiFormLabel-root">...</label>...<input>
    const muiControl = el.closest('.MuiFormControl-root, .MuiTextField-root, .MuiInputBase-root');
    if (muiControl) {
      const lbl = muiControl.closest('.MuiFormControl-root, .MuiTextField-root');
      if (lbl) {
        const label = lbl.querySelector('.MuiFormLabel-root, .MuiInputLabel-root');
        if (label && label.innerText.trim()) return true;
      }
    }
    // 2. Ant Design: <Form.Item><label class="ant-form-item-label">...</label>...<input>
    const antItem = el.closest('.ant-form-item');
    if (antItem && antItem.querySelector('.ant-form-item-label label, .ant-form-item-label')) return true;
    // 3. Chakra UI: <FormControl class="chakra-form-control"><FormLabel class="chakra-form__label">
    const chakra = el.closest('.chakra-form-control');
    if (chakra && chakra.querySelector('.chakra-form__label')) return true;
    // 4. Vuetify: <v-text-field> renders <label class="v-label">
    const vuetify = el.closest('.v-input, .v-field');
    if (vuetify && vuetify.querySelector('.v-label, .v-field-label')) return true;
    // 5. Angular Material: <mat-form-field><mat-label> or <label class="mdc-floating-label">
    const matField = el.closest('mat-form-field, .mat-mdc-form-field, .mat-form-field');
    if (matField && matField.querySelector('mat-label, .mdc-floating-label, .mat-mdc-floating-label')) return true;
    // 6. Bootstrap 5 floating labels: <div class="form-floating"><input><label>
    const bsFloat = el.closest('.form-floating');
    if (bsFloat && bsFloat.querySelector('label')) return true;
    // 7. PrimeReact / PrimeFaces: <span class="p-float-label"><input><label>
    const prime = el.closest('.p-float-label, .p-inputwrapper');
    if (prime && prime.querySelector('label')) return true;
    // 8. Quasar: <q-input> renders <label class="q-field__label">
    const quasar = el.closest('.q-field, .q-input');
    if (quasar && quasar.querySelector('.q-field__label')) return true;
    // 9. Generic: any wrapping element with a <label> that has text
    const genericWrap = el.closest('.form-group, .form-field, .field, .input-wrapper, .input-group');
    if (genericWrap) {
      const lbl = genericWrap.querySelector('label');
      if (lbl && lbl.innerText.trim()) return true;
    }
    return false;
  };

  // Proximity label: a VISIBLE short text sitting immediately beside the field in the same
  // container (e.g. "Records Per Page: <select>"). It's not linked via for/aria, so a screen
  // reader still misses it — but a sighted user clearly sees the label, so this is NOT a
  // high "field has NO label" defect. Suppresses the false positive on labelled-by-proximity
  // controls (records-per-page selects, inline filters) while still flagging truly bare fields.
  const visText = n => { const t = (n.innerText != null ? n.innerText : n.textContent || '').trim(); return t.length >= 2 && t.length <= 40 ? t : ''; };
  const hasProximityLabel = el => {
    // (a) a preceding ELEMENT sibling with short visible text
    let prev = el.previousElementSibling;
    for (let i = 0; prev && i < 3; i++, prev = prev.previousElementSibling) { if (prev.offsetParent !== null && visText(prev)) return true; }
    // (b) a short text NODE before the field inside the same parent ("Records Per Page: <select>")
    const par = el.parentElement;
    if (par) {
      for (const node of par.childNodes) { if (node === el) break; if (node.nodeType === 3) { const t = node.textContent.trim(); if (t.length >= 2 && t.length <= 40) return true; } }
      // (c) climb one wrapper (e.g. <gf-input>) and re-check its preceding sibling
      let pp = par.previousElementSibling;
      for (let i = 0; pp && i < 2; i++, pp = pp.previousElementSibling) { if (pp.offsetParent !== null && visText(pp)) return true; }
    }
    return false;
  };

  // Inline reddish-border helpers (r dominant: r≥150, r>g+50, r>b+50, alpha≥0.3)
  const parseColor = s => { const m = s && s.match(/rgba?\((\d+)\s*,\s*(\d+)\s*,\s*(\d+)(?:[\s,]+([\d.]+))?/); return m ? { r:+m[1], g:+m[2], b:+m[3], a:m[4]!==undefined?+m[4]:1 } : null; };
  const isReddish = s => { const c = parseColor(s); return !!(c && c.a >= 0.3 && c.r >= 150 && c.r > c.g + 50 && c.r > c.b + 50); };
  const fieldBorderColor = el => { const cs = getComputedStyle(el); return cs.borderTopColor || cs.borderBottomColor || cs.borderLeftColor || cs.borderRightColor || ''; };

  // Helper: is this <select> a "Records Per Page" / "Rows per page" / page-size selector?
  // Pattern signatures (any ONE qualifies):
  //  (a) ≤ 6 numeric options whose values look like page sizes (5, 10, 15, 20, 25, 30, 50, 100…)
  //  (b) name/id/class contains "page-size", "pageSize", "perPage", "rows-per", "records-per"
  //  (c) the visible text within ~150 chars of the select's location contains "per page"
  //      (case-insensitive) — covers "Records Per Page", "Rows per page", "Items per page", etc.
  // Page-size selectors are universally understood from context; requiring a <label for>
  // association is noise the user has explicitly called out (Departments page, 2026-06-11).
  const PAGE_SIZE_VALUES = new Set([5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150, 200, 250, 500, 1000]);
  const isPageSizeSelect = (el) => {
    if (el.tagName !== 'SELECT') return false;
    // (a) numeric-only options that look like page sizes
    const opts = [...el.options || []];
    if (opts.length > 0 && opts.length <= 6) {
      const allNumericPageSizes = opts.every(o => {
        const v = parseInt((o.value || o.text || '').trim(), 10);
        return !Number.isNaN(v) && PAGE_SIZE_VALUES.has(v);
      });
      if (allNumericPageSizes) return true;
    }
    // (b) name/id/class hints
    const hint = ((el.name || '') + ' ' + (el.id || '') + ' ' + (el.className && typeof el.className === 'string' ? el.className : '')).toLowerCase();
    if (/page[-_]?size|per[-_]?page|rows[-_]?per|records[-_]?per|items[-_]?per/.test(hint)) return true;
    // (c) parent / ancestor text contains "per page" / "rows per page" within 150 chars
    let scope = el.parentElement;
    for (let i = 0; scope && i < 3; i++, scope = scope.parentElement) {
      const t = (scope.innerText || '').trim().toLowerCase();
      if (t.length > 0 && t.length <= 200 && /per\s+page|page\s*size|rows\s+per|records\s+per|items\s+per|show\s+\d|show\s+per/.test(t)) return true;
    }
    return false;
  };

  // Shared full-visibility check used by fieldWithoutLabel and other checks below.
  // An element must be:
  //  (a) non-zero dimensions
  //  (b) inside the viewport bounds — not below/above/left/right of the visible area
  //  (c) not hidden by an ancestor (display:none / visibility:hidden / opacity:0)
  //  (d) not clipped inside an overflow:hidden ancestor that puts it out of view
  // Without (b) and (c), ghost elements rendered off-screen by framework components
  // (PrimeNG paginator jump-to-page input, hidden Angular form fields, off-canvas drawers)
  // produce annotations that appear in empty space below/outside page content.
  const vw = window.innerWidth, vh = window.innerHeight;
  const isVisibleInViewport = el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return false;
    // Entirely outside viewport in any direction
    if (r.right <= 0 || r.bottom <= 0 || r.left >= vw || r.top >= vh) return false;
    // Ancestor visibility walk
    let node = el.parentElement;
    while (node && node !== document.documentElement) {
      const s = getComputedStyle(node);
      if (s.display === 'none' || s.visibility === 'hidden' || s.opacity === '0') return false;
      // Clipped by overflow:hidden ancestor — check if element is outside ancestor's rect
      if (s.overflow === 'hidden' || s.overflowY === 'hidden' || s.overflowX === 'hidden') {
        const pr = node.getBoundingClientRect();
        if (r.bottom <= pr.top || r.top >= pr.bottom || r.right <= pr.left || r.left >= pr.right) return false;
      }
      node = node.parentElement;
    }
    return true;
  };

  // Dashboard/report period-filter selects (e.g. "This Year", "Last Month", "All Time").
  // These <select> elements live outside <form> tags in dashboards/reports and are entirely
  // self-described by their option values — requiring a <label> is noise.
  const PERIOD_KEYWORDS = /this\s+year|last\s+year|this\s+month|last\s+month|this\s+week|last\s+week|this\s+quarter|last\s+quarter|all\s+time|today|yesterday|ytd|mtd|year|month|week|quarter/i;
  const isDashboardFilter = el => {
    if (el.tagName !== 'SELECT') return false;
    // Must NOT be inside a <form> — dashboard filters are standalone controls
    if (el.closest('form')) return false;
    // Check option texts for period/date keywords
    const opts = [...(el.options || [])];
    const optText = opts.map(o => o.text || o.value || '').join(' ');
    if (PERIOD_KEYWORDS.test(optText)) return true;
    // Check the select's own value / id / name / class
    const hint = [el.value, el.id, el.name, typeof el.className === 'string' ? el.className : ''].join(' ');
    if (PERIOD_KEYWORDS.test(hint)) return true;
    // Check id/name for generic filter signals (period, date-range, year, timeframe)
    if (/period|date[-_]?range|timeframe|year|month|fiscal/i.test(el.id + ' ' + el.name)) return true;
    return false;
  };

  // 1. fieldWithoutLabel
  for (const el of document.querySelectorAll('input, textarea, select')) {
    if (out.length >= 16) break;
    if (el.type && skipTypes.has(el.type)) continue;
    // Use full visibility check — not just zero-dimensions.
    // Catches ghost inputs positioned below viewport (PrimeNG paginator jump-to-page,
    // hidden Angular reactive form fields, off-canvas inputs) that have non-zero BBox
    // but are never visible to the user. Without this, annotations appear in empty space.
    if (!isVisibleInViewport(el)) continue;
    // Search/filter inputs are self-descriptive — their placeholder IS their label in context.
    // type="search" and inputs whose placeholder or surrounding text contains search-related
    // words are a well-understood pattern; requiring a <label> would be noise for list-page filters.
    if (el.type === 'search') continue;
    // Page-size selectors (records per page / rows per page) are universally understood
    // from option values + surrounding text; requiring a <label for> is noise.
    if (isPageSizeSelect(el)) continue;
    // Dashboard period/date-range filter selects ("This Year", "Last Month", etc.) outside forms
    // are self-described by their option values — skip them.
    if (isDashboardFilter(el)) continue;
    const ph = (el.placeholder || el.getAttribute('placeholder') || '').trim().toLowerCase();
    if (/search|filter|find|lookup|query|zoek|recherche/i.test(ph)) continue;
    // Also check if the nearest visible text node or sibling says "search" — covers Angular inputs
    // where placeholder is rendered via attribute binding and reads back as '' on el.placeholder.
    const nearText = (() => {
      const par = el.parentElement;
      if (!par) return '';
      // check placeholder attribute directly (covers Angular [placeholder] binding)
      const attrPh = el.getAttribute('placeholder') || '';
      if (/search|filter|find|lookup|query/i.test(attrPh)) return attrPh;
      // check mat-label / label sibling text
      const lbl = par.querySelector('label, mat-label, .mat-mdc-floating-label, .mdc-floating-label');
      return lbl ? (lbl.innerText || lbl.textContent || '') : '';
    })();
    if (/search|filter|find|lookup|query/i.test(nearText)) continue;
    const lbByText = el.getAttribute('aria-labelledby') ? (document.getElementById(el.getAttribute('aria-labelledby'))?.textContent?.trim() || '') : '';
    const labelled = (el.labels && el.labels.length > 0) ||
      (el.getAttribute('aria-label') || '').trim() ||
      lbByText ||
      el.title ||
      el.placeholder ||
      el.getAttribute('placeholder') ||
      hasContextualLabel(el) ||
      hasProximityLabel(el);
    if (!labelled) {
      out.push({ issueType:'fieldWithoutLabel', severity:'high', selector:sel(el),
        description:'Form field has no label, aria-label, aria-labelledby, title, or placeholder', bbox: bb(el) });
    }
  }

  // 2. errorNotAnnounced
  for (const e of document.querySelectorAll('.error, .invalid-feedback, .field-error, .error-message, .form-error, [class*="error-msg"]')) {
    if (out.length >= 20) break;
    if (!isVisibleInViewport(e)) continue;
    const role = e.getAttribute('role');
    const ariaLive = e.getAttribute('aria-live');
    if (role !== 'alert' && role !== 'status' && !ariaLive) {
      out.push({ issueType:'errorNotAnnounced', severity:'high', selector:sel(e),
        description:`Error container ${sel(e)} missing role="alert" or aria-live — screen readers won't announce the error`, bbox: bb(e) });
    }
  }

  // 3. requiredNotIndicated
  // Part A: field has required attr but is missing visual asterisk or aria-required
  for (const input of document.querySelectorAll('input[required], textarea[required], select[required]')) {
    if (out.length >= 24) break;
    if (input.type === 'hidden') continue;
    if (!isVisibleInViewport(input)) continue;
    const hasAriaRequired = input.getAttribute('aria-required') === 'true';
    const label = (input.labels && input.labels[0]) || input.closest('label') || (input.id && document.querySelector(`label[for="${input.id}"]`));
    const labelText = label ? label.innerText : '';
    const hasAsterisk = /\*|\(required\)/i.test(labelText);
    if (!hasAriaRequired && !hasAsterisk) {
      out.push({ issueType:'requiredNotIndicated', severity:'medium', selector:sel(input),
        description:`Required field ${sel(input)} has no visual asterisk AND no aria-required — users can't tell it's required`, bbox: bb(input) });
    }
  }

  // Part B: field uses red border as the ONLY required indicator (no required attr, no aria-required, no asterisk)
  // Covers forms that rely solely on color to communicate required state (WCAG 1.4.1).
  // Example: Issue Budget "Title" field — red border on load, no * and no required attribute.
  for (const input of document.querySelectorAll('input, textarea, select')) {
    if (out.length >= 28) break;
    if (input.type === 'hidden') continue;
    if (!isVisibleInViewport(input)) continue;
    if (input.disabled || input.readOnly) continue;
    // Skip fields already covered by Part A
    if (input.hasAttribute('required') || input.getAttribute('aria-required') === 'true') continue;
    const value = (input.value || '').trim();
    if (value.length > 0) continue;
    const cls = (input.className || '').toString();
    if (/\bng-touched\b|\btouched\b|\bdirty\b/.test(cls)) continue;

    // Check for reddish border on the input or its component container
    let hasRedBorder = isReddish(fieldBorderColor(input));
    if (!hasRedBorder) {
      const ctr = input.closest('mat-form-field, .mat-mdc-form-field, .mat-form-field-wrapper, .form-group, .form-field, .field');
      if (ctr) {
        const ccs = getComputedStyle(ctr);
        hasRedBorder = isReddish(fieldBorderColor(ctr)) || isReddish(ccs.outlineColor);
      }
    }
    if (!hasRedBorder) continue;

    out.push({ issueType: 'requiredNotIndicated', severity: 'medium', selector: sel(input),
      description: `Field appears required (red border on load) but has no required attribute, no aria-required="true", and no text marker — screen-reader users and colorblind users have no signal this field is mandatory`,
      bbox: bb(input) });
  }

  // 4. fieldsetNoLegend
  for (const fs of document.querySelectorAll('fieldset')) {
    if (out.length >= 28) break;
    if (!isVisibleInViewport(fs)) continue;
    const legend = fs.querySelector(':scope > legend');
    if (!legend || !legend.innerText.trim()) {
      out.push({ issueType:'fieldsetNoLegend', severity:'medium', selector:sel(fs),
        description:`Fieldset ${sel(fs)} has no <legend> — radio/checkbox groups lack a screen-reader-announced group label`, bbox: bb(fs) });
    }
  }

  // 5. passwordNoToggle
  for (const pwd of document.querySelectorAll('input[type="password"]')) {
    if (out.length >= 30) break;
    if (!isVisibleInViewport(pwd)) continue;
    const parent = pwd.closest('div, fieldset, form');
    const toggle = parent && parent.querySelector('[aria-label*="show" i], [aria-label*="hide" i], [data-testid*="toggle"]');
    if (!toggle) {
      out.push({ issueType:'passwordNoToggle', severity:'medium', selector:sel(pwd),
        description:'Password field has no show/hide toggle button', bbox: bb(pwd) });
    }
  }

  // 6. focusOrderMismatch
  const focusables = [...document.querySelectorAll(
    'input:not([disabled]):not([type="hidden"]), select:not([disabled]), textarea:not([disabled]), button:not([disabled]), a[href], [tabindex]:not([tabindex="-1"])'
  )].filter(el => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; }).slice(0, 10);
  if (focusables.length >= 3) {
    let violations = 0;
    for (let i = 1; i < focusables.length; i++) {
      const prev = focusables[i-1].getBoundingClientRect();
      const curr = focusables[i].getBoundingClientRect();
      if (curr.top + 8 < prev.top) violations++;
    }
    if (violations >= 2) {
      out.push({ issueType:'focusOrderMismatch', severity:'medium', selector:'form',
        description:`Tab focus order does not match visual top-to-bottom — ${violations} elements appear above their DOM-previous sibling`,
        bbox: { x:0, y:0, w:200, h:80 } });
    }
  }

  return out;
}
```

## Migration
```toml
[detectors]
qa-form-a11y           = true   # NEW
qa-detect-form-a11y    = false  # REPLACED entirely
# qa-detect-forms retains the structural checks (formNoSubmit, inputHeightTooSmall, formFieldNotFullWidth) → moved to qa-form-structure
```
