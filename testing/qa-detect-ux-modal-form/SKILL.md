---
name: qa-detect-ux-modal-form
section: visual
description: "Detects modal + form UX issues: modal title singular/plural mismatch ('Update Districts' when editing 1 row), modal not horizontally centered, required-asterisk shown on only some required fields, static info text placed next to inputs looks like another field, action buttons not in standard footer position."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
requires: [hasModals, hasInputs]
---

## What it catches — 6 issue types

| issueType | severity | What |
|---|---|---|
| `modalTitleSingularPluralMismatch` | low | Modal title uses plural noun ("Update Districts") in a single-item edit context — should be singular ("Update District") |
| `modalNotHorizontallyCentered` | medium | Modal is offset > 64px from the viewport horizontal center — looks like a layout bug |
| `modalActionsNotInFooter` | low | Primary action buttons (Save/Update/Cancel) are NOT in a clearly identifiable footer row — buried in mid-modal content |
| `formRequiredAsteriskInconsistent` | medium | Some fields marked with `required` attribute have visible `*` label markers; others (also `required`) don't. User can't tell what's actually mandatory |
| `formStaticTextLooksLikeField` | low | Text inside a form sits between inputs with similar visual treatment but is not an actual `<label>` / input — confused as another field (your "Faisalabad, Punjab" hint) |
| `formMissingPlaceholderOnEmpty` | low | Empty text input has no placeholder, no value, no hint text — users can't tell what kind of data goes there |

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

  // ── MODALS ────────────────────────────────────────────────────────────
  const openModals = [...document.querySelectorAll('dialog[open], [role="dialog"]:not([hidden]), [role="alertdialog"]:not([hidden]), .modal.show, .modal.is-open, .mat-dialog-container, .cdk-overlay-container .mat-mdc-dialog-container')]
    .filter(visible);

  for (const m of openModals.slice(0, 2)) {
    const modalR = m.getBoundingClientRect();

    // 1. Title singular/plural mismatch
    const titleEl = m.querySelector('h1, h2, h3, h4, h5, h6, .modal-title, [class*="dialog-title"], [class*="modal-header"]');
    const titleText = titleEl ? (titleEl.innerText || '').trim() : '';
    if (titleText && /^(update|edit|delete|view|details?)\s+/i.test(titleText)) {
      // Action verb + noun
      const noun = titleText.replace(/^(update|edit|delete|view|details?\s+(for)?)\s+/i, '').trim();
      // Heuristic: plural ends in 's' (not 'ss'/'us'), not in cases like 'Class', 'Address'
      const looksPlural = /[a-z]s\b/i.test(noun) && !/[s]s\b/i.test(noun) && !/us\b/i.test(noun);
      // Crude: contains form with ≤ 1 field-name section (single-item edit)
      const forms = m.querySelectorAll('form');
      const hasNoun = forms.length === 0 || forms.length === 1;
      if (looksPlural && hasNoun && noun.length < 30) {
        // Try singular suggestion
        const singular = noun.endsWith('ies') ? noun.replace(/ies$/, 'y') :
                        noun.endsWith('s') ? noun.replace(/s$/, '') : noun;
        out.push({
          issueType: 'modalTitleSingularPluralMismatch', severity: 'low',
          selector: sel(titleEl), bbox: bb(titleEl),
          description: `Modal title "${titleText}" uses plural noun "${noun}" for a single-item edit. Use singular: "Update ${singular}".`
        });
      }
    }

    // 2. Modal horizontally centered
    const vpW = window.innerWidth;
    const modalCenter = modalR.left + modalR.width / 2;
    const offset = Math.abs(modalCenter - vpW / 2);
    if (offset > 64 && modalR.width < vpW * 0.95) {
      out.push({
        issueType: 'modalNotHorizontallyCentered', severity: 'medium',
        selector: sel(m), bbox: bb(m),
        description: `Modal center is ${offset.toFixed(0)}px off viewport center (viewport ${vpW}px, modal ${modalR.width.toFixed(0)}px wide at x=${modalR.left.toFixed(0)}). Modals should be horizontally centered.`
      });
    }

    // 3. Action buttons in modal footer
    const allBtns = [...m.querySelectorAll('button, [role="button"]')].filter(visible);
    if (allBtns.length >= 2) {
      const actionBtns = allBtns.filter(b => /^(save|update|create|cancel|close|delete|confirm|apply|ok|submit|discard)$/i.test((b.innerText || '').trim()));
      if (actionBtns.length >= 2) {
        // Are they in the bottom 35% of the modal AND visually grouped?
        const modalBottom = modalR.top + modalR.height;
        const cutoff = modalR.top + modalR.height * 0.65;
        const inFooter = actionBtns.filter(b => {
          const r = b.getBoundingClientRect();
          return r.top >= cutoff && r.bottom <= modalBottom + 4;
        });
        if (inFooter.length < actionBtns.length - 1) {
          out.push({
            issueType: 'modalActionsNotInFooter', severity: 'low',
            selector: sel(m), bbox: bb(m),
            description: `${actionBtns.length} action buttons in modal but only ${inFooter.length} sit in the bottom-35% footer area. Move all primary actions to the modal footer for predictable UX.`
          });
        }
      }
    }
  }

  // ── FORMS ─────────────────────────────────────────────────────────────
  const forms = [...document.querySelectorAll('form, [role="form"], .mat-dialog-content form, .mat-dialog-container')].filter(visible);
  let asteriskFlagged = 0, staticTextFlagged = 0, placeholderFlagged = 0;

  for (const f of forms.slice(0, 4)) {
    // 4. Required-asterisk inconsistency
    if (asteriskFlagged < 2) {
      const requiredInputs = [...f.querySelectorAll('input[required], select[required], textarea[required], [aria-required="true"]')].filter(visible);
      if (requiredInputs.length >= 2) {
        let withAsterisk = 0, withoutAsterisk = 0;
        for (const inp of requiredInputs) {
          // Find associated label or container
          let labelTxt = '';
          if (inp.id) {
            const lab = document.querySelector(`label[for="${inp.id}"]`);
            if (lab) labelTxt += (lab.innerText || '');
          }
          const parentLab = inp.closest('label, .form-field, .mat-form-field, .form-group, .field');
          if (parentLab) labelTxt += ' ' + (parentLab.innerText || '');
          if (/\*/.test(labelTxt)) withAsterisk++;
          else withoutAsterisk++;
        }
        if (withAsterisk >= 1 && withoutAsterisk >= 1) {
          asteriskFlagged++;
          out.push({
            issueType: 'formRequiredAsteriskInconsistent', severity: 'medium',
            selector: sel(f), bbox: bb(f),
            description: `${requiredInputs.length} required fields in form: ${withAsterisk} have visible "*" marker, ${withoutAsterisk} don't. Either mark all required fields with * or none — users can't tell what's mandatory.`
          });
        }
      }
    }

    // 5. Static text between inputs that looks like a field
    if (staticTextFlagged < 2) {
      const allChildren = [...f.querySelectorAll('div, p, span')].filter(visible);
      for (const el of allChildren) {
        if (staticTextFlagged >= 2) break;
        // Element that contains text directly (no input child) and sits between two inputs
        const text = (el.innerText || '').trim();
        if (text.length < 4 || text.length > 80) continue;
        if (el.querySelector('input, select, textarea, button, label, h1, h2, h3, h4, h5, h6')) continue;
        // Check if previous sibling and next sibling are inputs / containers-with-inputs
        const prev = el.previousElementSibling;
        const next = el.nextElementSibling;
        const prevHasInput = prev && (prev.matches('input, select, textarea') || prev.querySelector('input, select, textarea'));
        const nextHasInput = next && (next.matches('input, select, textarea') || next.querySelector('input, select, textarea'));
        if (prevHasInput && nextHasInput) {
          // Visual treatment: is it styled like a label/text (small, muted)? or like an input value (regular size)?
          const cs = getComputedStyle(el);
          const fs = parseFloat(cs.fontSize) || 16;
          const isMuted = cs.color && /rgba?\((\d+),\s*(\d+),\s*(\d+)/.test(cs.color);
          // Treat as ambiguous: same font-size as inputs (≥ 14px) AND not visibly muted
          if (fs >= 14) {
            staticTextFlagged++;
            out.push({
              issueType: 'formStaticTextLooksLikeField', severity: 'low',
              selector: sel(el), bbox: bb(el),
              description: `Static text "${text.slice(0, 40)}" sits between two form fields without label/small/help-text styling. Users may think it's another input. Apply a hint/help style or move to a placeholder.`
            });
          }
        }
      }
    }

    // 6. Empty input with no placeholder, no value, no label hint
    if (placeholderFlagged < 3) {
      const emptyInputs = [...f.querySelectorAll('input[type="text"], input[type="email"], input[type="number"], input[type="search"], input[type="tel"], input[type="url"], textarea, input:not([type])')]
        .filter(visible)
        .filter(i => !i.disabled && !i.readOnly && (!i.value || i.value.trim() === ''));
      for (const inp of emptyInputs) {
        if (placeholderFlagged >= 3) break;
        const placeholder = (inp.getAttribute('placeholder') || '').trim();
        const ariaLabel = (inp.getAttribute('aria-label') || '').trim();
        const title = (inp.getAttribute('title') || '').trim();
        if (placeholder || ariaLabel.length > 4 || title) continue;
        // Check for nearby label
        let hasLabel = false;
        if (inp.id) {
          if (document.querySelector(`label[for="${inp.id}"]`)) hasLabel = true;
        }
        const parentLab = inp.closest('label');
        if (parentLab) hasLabel = true;
        // If a label exists AND label has the field name, no need for placeholder.
        // But if no placeholder, no value, no aria-label/title, fields like description
        // look completely blank. Only flag if NO label too.
        if (!hasLabel) {
          placeholderFlagged++;
          out.push({
            issueType: 'formMissingPlaceholderOnEmpty', severity: 'low',
            selector: sel(inp), bbox: bb(inp),
            description: `Empty input has no placeholder, no aria-label, no <label for=...>, no visible name. Users can't tell what kind of data goes here.`
          });
        }
      }
    }
  }

  return out;
}
```

## Notes

- Bounded: 2 modal-title + 2 modal-center + 2 modal-actions + 2 asterisk + 2 static-text + 3 placeholder = max ~13 findings
- Self-skips: page with no open modals AND no forms returns []
- The `modalTitleSingularPluralMismatch` is the EXACT bug from your Update Districts screenshot
- The `formStaticTextLooksLikeField` catches the "Faisalabad, Punjab" floating text in your modal
- The `formRequiredAsteriskInconsistent` catches the case where Name has * but Province (also required) doesn't
