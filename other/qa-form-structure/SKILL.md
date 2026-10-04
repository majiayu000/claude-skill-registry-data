---
name: qa-form-structure
section: interactive
description: "Consolidated form structure skill. Owns submit-button presence, input touch-target height on mobile/tablet, full-width form fields on mobile, and structural form HTML. Replaces structural portion of qa-detect-forms."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: true
interactive: false
cacheVersion: "1.0.0"
ownership: "exclusive: any structural finding (form/submit/fieldset/input dimensions) belongs to this skill"
replaces:
  - "portions of qa-detect-forms (formNoSubmit, inputHeightTooSmall, formFieldNotFullWidth)"
requires: [hasForms]
---

# qa-form-structure — Consolidated Form Structure Skill

Single skill owning structural form HTML and physical input dimensions. Separates from accessibility (qa-form-a11y) and content (qa-form-validation). Pure passive — no interaction.

## What it checks (4 issue types)

| issueType | severity | catches |
|---|---|---|
| `inputsNotWrappedInForm` | high | Inputs + a submit button exist with NO `<form>` wrapper — breaks Enter-to-submit and password managers (common Angular/React anti-pattern) |
| `formNoSubmit` | medium | Form has no visible submit affordance — no submit-type button AND no button labelled Save/Update/Add/Submit/… inside the form, its dialog/card footer, or associated via `form=id`. (Label-aware so a SPA "Save" `button type="button"` is not a false positive.) |
| `inputHeightTooSmall` | medium | On mobile/tablet (vw ≤ 1024), input rendered height < 44px (below touch-target minimum) |
| `formFieldNotFullWidth` | medium | On mobile (vw ≤ 768), form input rendered < 70% of parent width AND < 300px wide |
| `nativeSelectHidden` | medium | Native `<select>` is CSS-hidden on mobile and replaced by a custom component without `aria-expanded`/`aria-haspopup` — may not trigger native OS picker and may be inaccessible |

## Self-skip
Return `[]` ONLY if there are **no visible testable inputs** (text/email/password/number/tel/url/search/date/textarea/select). **Do NOT skip on a missing `<form>`** — form-less input groups still get the touch-target/full-width checks AND get flagged as `inputsNotWrappedInForm` below.

## Probe (browser_evaluate)
```js
() => {
  const out = [];
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };
  const skipTypes = new Set(['hidden','submit','reset','button','image','checkbox','radio']);
  const vw = innerWidth;
  const isMobile = vw <= 768;
  const isMobileOrTablet = vw <= 1024;

  // 0. inputsNotWrappedInForm — testable inputs + a submit button, but NO <form> wrapper
  //    (the common Angular/React anti-pattern: breaks Enter-to-submit and password managers)
  const TESTABLE = 'input[type="text"],input[type="email"],input[type="password"],input[type="number"],input[type="tel"],input[type="url"],input[type="search"],input[type="date"],input:not([type]),textarea';
  const loose = [...document.querySelectorAll(TESTABLE)].filter(el => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0 && !el.closest('form'); });
  if (loose.length >= 1) {
    const hasSubmit = [...document.querySelectorAll('button,[role="button"],input[type="submit"]')]
      .some(b => { const r = b.getBoundingClientRect(); return r.width > 0 && /sign ?in|log ?in|sign ?up|submit|register|save|send|continue|next|create|update|apply|verify/i.test(b.textContent || b.value || b.getAttribute('aria-label') || ''); });
    if (hasSubmit) {
      out.push({ issueType: 'inputsNotWrappedInForm', severity: 'high',
        selector: loose[0].id ? `#${loose[0].id}` : (loose[0].name ? `[name="${loose[0].name}"]` : loose[0].tagName.toLowerCase()),
        description: `${loose.length} input(s) plus a submit button are NOT inside a <form> element. Breaks native Enter-to-submit and browser/password-manager autofill. Wrap the group in a <form>.`,
        bbox: bb(loose[0]) });
    }
  }

  // 1. formNoSubmit — a form is "submit-less" ONLY if NO visible submit affordance exists.
  //    Recognize the affordance the way real SPAs build it, so a labelled "Save"/"Update"/"Add"
  //    button is NOT a false positive (the qa-20260615 assignbudget run flagged a page whose
  //    submit IS a "Save" button). Counts: native submit shapes, type="button" buttons whose
  //    text/aria-label matches a save/submit verb, buttons in the form's dialog/card/panel FOOTER
  //    (Angular/React put action buttons OUTSIDE the <form>), and [form=id]-associated buttons.
  const SUBMIT_TXT = /\b(save|submit|update|create|add|new|insert|store|send|apply|confirm|continue|next|finish|done|register|sign ?in|log ?in|sign ?up|ok|post|publish|proceed|search|verify)\b/i;
  const isSubmitAffordance = (b) => {
    if (!b) return false;
    const r = b.getBoundingClientRect();
    if (r.width <= 0 || r.height <= 0) return false;                       // visible only
    if (b.matches('button[type="submit"], input[type="submit"], button:not([type])')) return true;   // native submit
    const t = (b.innerText || b.textContent || b.value || b.getAttribute('aria-label') || b.getAttribute('title') || '').trim();
    return SUBMIT_TXT.test(t);                                             // label-based (Save/Update/Add…) incl. type="button"
  };
  for (const form of document.querySelectorAll('form')) {
    if (out.length >= 6) break;
    const r = form.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    const fid = form.getAttribute('id');
    // search INSIDE the form, in its nearest action container (modal/dialog/card/panel footer),
    // and any button associated via the HTML form= attribute.
    const container = form.closest('[role="dialog"], .modal, .modal-content, .mat-dialog-container, .ant-modal, .card, .panel, .p-dialog') || form.parentElement || form;
    const candidates = [
      ...form.querySelectorAll('button, input[type="submit"], input[type="button"], [role="button"], a[role="button"]'),
      ...container.querySelectorAll('button, [role="button"], a[role="button"]'),
      ...(fid ? document.querySelectorAll(`button[form="${fid}"], input[form="${fid}"]`) : [])
    ];
    if (!candidates.some(isSubmitAffordance)) {
      const sel = `form${form.id ? `#${form.id}` : ''}`;
      out.push({ issueType: 'formNoSubmit', severity: 'medium', selector: sel,
        description: 'Form has no visible submit/save button (no submit-type button, and no Save/Update/Add-labelled button inside the form, its dialog/card footer, or associated via form=id)', bbox: bb(form) });
    }
  }

  // 2. inputHeightTooSmall + 3. formFieldNotFullWidth (per-input)
  if (!isMobileOrTablet && !isMobile) return out;  // skip if desktop-only

  for (const el of document.querySelectorAll('input, textarea, select')) {
    if (out.length >= 24) break;
    if (el.type && skipTypes.has(el.type)) continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    const sel = `${el.tagName.toLowerCase()}${el.id ? `#${el.id}` : ''}${el.name ? `[name="${el.name}"]` : ''}`;

    // inputHeightTooSmall — mobile/tablet only
    if (isMobileOrTablet && r.height < 44) {
      out.push({ issueType: 'inputHeightTooSmall', severity: 'medium', selector: sel,
        description: `Input height ${Math.round(r.height)}px is below 44px touch-target minimum (viewport=${vw}px)`,
        bbox: bb(el) });
    }

    // formFieldNotFullWidth — mobile only
    if (isMobile) {
      const parent = el.closest('.form-group, .field, .form-field, fieldset, form > div, form');
      if (parent) {
        const pr = parent.getBoundingClientRect();
        if (pr.width > 0) {
          const widthRatio = r.width / pr.width;
          if (widthRatio < 0.7 && r.width < 300) {
            out.push({ issueType: 'formFieldNotFullWidth', severity: 'medium', selector: sel,
              description: `Form field ${Math.round(r.width)}px is only ${Math.round(widthRatio*100)}% of parent (${Math.round(pr.width)}px) on mobile — should be full-width`,
              bbox: bb(el) });
          }
        }
      }
    }
  }


  // 4. nativeSelectHidden — native <select> CSS-hidden, replaced by custom component without ARIA (mobile/tablet)
  if (isMobile || isMobileOrTablet) {
    for (const select of document.querySelectorAll('select')) {
      if (out.length >= 24) break;
      const s = getComputedStyle(select);
      const r = select.getBoundingClientRect();
      const isHidden = s.display === 'none' || s.visibility === 'hidden' || parseFloat(s.opacity) === 0 || r.width === 0;
      if (!isHidden) continue; // native select visible — fine
      const parent = select.parentElement;
      if (!parent) continue;
      const customDropdown = parent.querySelector('[role="combobox"],[role="listbox"],[class*="select"],[class*="dropdown"],[class*="combo"]');
      if (!customDropdown) continue;
      const hasAria = customDropdown.hasAttribute('aria-expanded') || customDropdown.hasAttribute('aria-haspopup');
      if (!hasAria) {
        const sel = select.id ? `#${select.id}` : (select.name ? `select[name="${select.name}"]` : 'select');
        out.push({ issueType: 'nativeSelectHidden', severity: 'medium', selector: sel,
          description: `Native <select> is hidden on mobile and replaced by a custom component (${customDropdown.className || customDropdown.tagName}) without aria-expanded/aria-haspopup — mobile users won't get the native OS picker and screen readers may not work`,
          bbox: bb(parent) });
      }
    }
  }

  // 5. duplicateSearchControl — multiple visible search inputs on the same page that
  // appear to serve the same purpose.
  // Classic pattern: a filter panel with "Search Student" + a separate inline search
  // above the table ("Search by student name"). Users don't know which one to use,
  // and both may apply different scopes (filtered vs unfiltered results).
  const SEARCH_RE = /search|find|lookup|query/i;
  const visibleSearchInputs = [...document.querySelectorAll(
    'input[type="search"], input[placeholder], input[name], input[id], input[class]'
  )].filter(el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return false;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return false;
    // Skip inputs inside closed dialogs, inactive tabs, hidden panels
    if (el.closest('[aria-hidden="true"], [hidden], [style*="display:none"]')) return false;
    const ph  = (el.placeholder || el.getAttribute('placeholder') || '').toLowerCase();
    const nm  = (el.name  || '').toLowerCase();
    const id  = (el.id    || '').toLowerCase();
    const cls = (el.className && typeof el.className === 'string' ? el.className : '').toLowerCase();
    return el.type === 'search'
      || SEARCH_RE.test(ph)
      || SEARCH_RE.test(nm)
      || SEARCH_RE.test(id)
      || SEARCH_RE.test(cls);
  });

  if (visibleSearchInputs.length >= 2) {
    // Only flag if inputs are in the same page context — not in different modals,
    // tabs, or panels. Two search inputs inside the same <main> or page scroll area
    // is the real duplicate; one in a modal and one on the page is fine.
    const inSameContext = visibleSearchInputs.every(el =>
      !el.closest('[role="dialog"]:not([open]), [role="tabpanel"][aria-selected="false"]')
    );
    if (inSameContext) {
      const labels = visibleSearchInputs.slice(0, 3).map(el => {
        const ph = el.placeholder || el.getAttribute('placeholder') || el.name || el.id || 'search';
        return `"${ph.slice(0, 40)}"`;
      }).join(', ');
      out.push({
        issueType: 'duplicateSearchControl', severity: 'medium',
        selector: 'page',
        description: `Page has ${visibleSearchInputs.length} search inputs for the same data: ${labels}. Consolidate into one — the filter panel search is sufficient. Duplicate search boxes confuse users (which one applies? do both filter?) and waste vertical space above the table.`,
        bbox: bb(visibleSearchInputs[1])
      });
    }
  }

  return out;
}
```

## Migration

`qa-detect-forms` is the only skill being PARTIALLY replaced — the structural checks move here, the a11y checks (`fieldWithoutLabel`, `passwordNoToggle`) move to `qa-form-a11y`. After cutover, `qa-detect-forms` itself is disabled.

```toml
[detectors]
qa-form-structure  = true   # NEW (formNoSubmit + inputHeightTooSmall + formFieldNotFullWidth)
qa-form-a11y       = true   # NEW (fieldWithoutLabel + passwordNoToggle + 4 more)
qa-detect-forms    = false  # REPLACED entirely (split between qa-form-structure and qa-form-a11y)
```

## Notes
- This skill is INTENTIONALLY small (3 issue types). Form structure is a small ownership boundary.
- Future structural checks (e.g., `formInScrollContainer`, `inputOverlappingLabel`, `inlineFormBreaksOnMobile`) belong here.
- `viewportSensitive: true` — runs per viewport because findings depend on `innerWidth`.
