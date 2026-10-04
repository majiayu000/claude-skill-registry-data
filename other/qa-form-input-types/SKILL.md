---
name: qa-form-input-types
section: interactive
description: "Consolidated input-widget testing. Owns every input-type-specific bug: date/time pickers, file upload, OTP boxes, comboboxes, tag inputs, formatted (credit card / phone / CVV), masked inputs, inline-edit, password rules. Replaces 9 overlapping widget skills. All in-page widget tests run as ONE async probe; the file-upload-with-real-file check stays MCP."
model: sonnet
applyOn: [laptop]
needsSetup: false
viewportSensitive: true
interactive: true
executable: partial
cacheVersion: "1.0.0"
ownership: "exclusive: any bug specific to an input WIDGET (date, file, OTP, combobox, tag, mask, formatted, inline-edit, password) belongs to this skill"
replaces:
  - qa-test-form-datetime
  - qa-test-form-file-upload
  - qa-test-form-otp
  - qa-test-form-combobox
  - qa-test-form-tag-input
  - qa-test-form-formatted-inputs
  - qa-test-form-input-mask
  - qa-test-form-inline-edit
  - qa-test-form-password-rules
requires: [hasInputs]
---
# qa-form-input-types — Consolidated Input-Widget Skill

Single skill owning every widget-specific bug type. Replaces 9 overlapping skills.

## How the orchestrator runs this (ONE call drives all in-page widgets)

🚨 **The widget tests are an EXECUTABLE in-page probe.** Do NOT hand-drive each widget with separate `browser_click` / `browser_type` / `browser_press_key` calls. Instead make **ONE** call:

```
result = browser_evaluate(<the async function in "## Interactive Probe" below>)
```

The probe discovers every widget type, then drives each one in-page — date min/max + past-date + range, OTP auto-advance/backspace/paste, combobox open/filter/select/escape/aria, tag add/paste/remove, formatted card/expiry/cvv/phone/number, masked pattern/format/backspace, inline-edit click/focus/escape/enter, password strength/confirm — asserting each result and returning `findings[]`. It does its own waits via in-page `setTimeout`, self-skips per type when absent, and runs idempotent cleanup before returning. It returns `[]` when no widgets exist at all. Transcribe each returned finding verbatim.

**HONEST EXCEPTION — file upload with a real file stays MCP** (`fileNoSelectionFeedback`) because choosing a real file requires the OS file dialog via `browser_file_upload`, which a page-context probe cannot open. The file *attribute* checks (`fileAcceptMissing`, `fileSizeHintMissing`) and the *progress/cancel UI* checks (`uploadNoProgressUI`, `uploadNoCancelButton`) ARE in the probe (passive). That is why frontmatter is `executable: partial`.

## What it checks (35 issue types — see table at bottom). Self-skip: probe returns `[]` if zero widgets of every type.

## Interactive Probe (browser_evaluate, async)

```js
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const out = [];
  const add = o => out.push(Object.assign({ skill: 'qa-form-input-types' }, o));
  const vis = el => { if (!el) return false; const r = el.getBoundingClientRect(); const s = getComputedStyle(el); return r.width > 0 && r.height > 0 && s.display !== 'none' && s.visibility !== 'hidden'; };
  const fvis = el => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0 && !el.disabled && !el.readOnly; };
  const sel = el => { if (!el) return null; if (el.id) return '#' + CSS.escape(el.id); if (el.name) return `${el.tagName.toLowerCase()}[name="${el.name}"]`; const c = (el.className && typeof el.className === 'string') ? el.className.trim().split(/\s+/).slice(0,2).join('.') : ''; return el.tagName.toLowerCase() + (c ? '.' + c : ''); };
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };
  const setNative = (el, v) => { const p = el.tagName === 'TEXTAREA' ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype; try { Object.getOwnPropertyDescriptor(p, 'value').set.call(el, v); } catch (_) { el.value = v; } el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); };
  const key = (el, k) => { ['keydown','keyup'].forEach(t => el.dispatchEvent(new KeyboardEvent(t, { key: k, code: k, bubbles: true }))); };
  const hasError = el => { if (!el) return false; const ai = el.getAttribute && el.getAttribute('aria-invalid') === 'true'; let ci = false; try { ci = el.matches(':invalid'); } catch (_) {} const c = el.closest('label, div, fieldset, .form-group, .field') || el.parentElement; const near = c && c.querySelector('[role="alert"], .error, .invalid-feedback, [data-testid*="error"], .text-red-500, .text-danger'); return ai || ci || !!near; };
  const esc = () => document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', keyCode: 27, bubbles: true }));

  // tracking attrs we add (cleaned at end)
  const tracked = { otp: [], cb: [], tag: [], mask: [], ie: [] };

  // ── DISCOVERY ──
  const dateInputs = [...document.querySelectorAll('input[type="date"], input[type="time"], input[type="datetime-local"]')].filter(fvis).slice(0, 4);
  const fileInputs = [...document.querySelectorAll('input[type="file"]')].filter(el => !el.disabled).slice(0, 2);
  const otpCands = [...document.querySelectorAll('input[maxlength="1"], input[inputmode="numeric"][maxlength="1"], input[type="tel"][maxlength="1"]')].filter(fvis);
  const cbCands = [...document.querySelectorAll('[role="combobox"], input[role="combobox"], [class*="select"][class*="search"]:not(select), [class*="autocomplete"]:not(select), [class*="typeahead"]:not(select), div[class*="Select"]:not(select), [data-testid*="combobox"], [data-testid*="select"]:not(select)')].filter(el => vis(el) && el.tagName.toLowerCase() !== 'select' && !el.disabled && el.getAttribute('aria-disabled') !== 'true').slice(0, 3);
  const tagCands = [...document.querySelectorAll('[class*="tag"][class*="input"], [class*="chip"][class*="input"], [class*="multiselect"], [class*="MuiAutocomplete"], [role="combobox"][aria-multiselectable="true"], [data-testid*="tag-input"], [data-testid*="chip-input"]')].filter(el => { const inp = el.querySelector('input[type="text"], input:not([type])'); return vis(el) && inp && !inp.disabled; }).slice(0, 3);
  const ieCands = [...document.querySelectorAll('[contenteditable="true"], [contenteditable=""], [data-editable], [data-inline-edit], [role="gridcell"][tabindex], [class*="editable"]:not(input):not(textarea), [class*="inline-edit"]:not(input):not(textarea)')].filter(vis).slice(0, 3);
  const pwds = [...document.querySelectorAll('input[type="password"]')].filter(fvis);
  const fieldsBy = pred => [...document.querySelectorAll('input, textarea')].filter(fvis).filter(pred).slice(0, 1);
  const cardF = fieldsBy(el => { const ac = el.getAttribute('autocomplete') || ''; const n = (el.name + el.id).toLowerCase(); return ac.includes('cc-number') || /card.?number|cardnumber|cc.?num/.test(n); })[0];
  const expF = fieldsBy(el => { const ac = el.getAttribute('autocomplete') || ''; const n = (el.name + el.id).toLowerCase(); return ac.includes('cc-exp') || /expir|cc.?exp/.test(n); })[0];
  const cvvF = fieldsBy(el => { const ac = el.getAttribute('autocomplete') || ''; const n = (el.name + el.id).toLowerCase(); return ac.includes('cc-csc') || /cvv|cvc|csc|security.?code/.test(n); })[0];
  const phoneF = fieldsBy(el => el.type === 'tel' || /phone|mobile|tel|whatsapp/.test((el.name + el.id).toLowerCase()))[0];
  const numF = [...document.querySelectorAll('input[type="number"]')].filter(fvis).slice(0, 1).map(el => { const ctx = (el.name + el.id + (el.labels && el.labels[0] ? el.labels[0].innerText : '')).toLowerCase(); return { el, positiveOnly: /price|amount|cost|age|quantity|qty|count|total/.test(ctx), integerOnly: !el.step || el.step === '1' || el.step === '' }; })[0];
  const maskCands = [];
  for (const el of [...document.querySelectorAll('input[type="text"], input[type="tel"], input[type="search"]')].filter(fvis)) {
    if (maskCands.length >= 2) break;
    const ph = el.placeholder || '', n = (el.name + el.id).toLowerCase(), ac = (el.getAttribute('autocomplete') || '').toLowerCase();
    const hasFormatPh = /[_(){}-]\s*[_({}\-)]|\(?___?\)?|####|####\s*####|XX\s*\/\s*XX|\d{2}\s*\/\s*\d{2}/.test(ph);
    const isPhone = /phone|mobile|tel/.test(n) || el.type === 'tel' || ac.includes('tel');
    const isCard = /card|cc.?num/.test(n) || ac.includes('cc-number');
    if (!hasFormatPh && !isPhone && !isCard && !/iban|account.?number|postal|zip/.test(n)) continue;
    maskCands.push({ el, maskHint: isPhone ? 'phone' : isCard ? 'card' : 'generic' });
  }

  if (!dateInputs.length && !fileInputs.length && otpCands.length < 4 && !cbCands.length && !tagCands.length && !ieCands.length && !pwds.length && !cardF && !expF && !cvvF && !phoneF && !numF && !maskCands.length) return [];

  try {
    // ── FILE (passive only: accept / size-hint / progress / cancel UI) ──
    for (const f of fileInputs) {
      const container = f.closest('label, div, fieldset, .form-group, .upload, .file-upload, .file-input, .drop-zone, .dropzone') || f.parentElement;
      const txt = container ? container.innerText : '';
      if (!(f.hasAttribute('accept') && (f.getAttribute('accept') || '').trim())) add({ issueType: 'fileAcceptMissing', severity: 'medium', selector: sel(f), bbox: bb(f), description: 'File input has no accept= attribute — any file type accepted.', evidence: {} });
      if (!(/max(imum)?\s*\d+\s*(kb|mb|bytes?)/i.test(txt) || /up\s*to\s*\d+\s*(kb|mb)/i.test(txt))) add({ issueType: 'fileSizeHintMissing', severity: 'low', selector: sel(f), bbox: bb(f), description: 'No visible "max N MB" hint near the file input.', evidence: {} });
      if (container) {
        if (!container.querySelector('progress, [role="progressbar"], .progress, .progress-bar, [class*="upload-progress"], [class*="upload-bar"], [data-testid*="progress"]')) add({ issueType: 'uploadNoProgressUI', severity: 'medium', selector: sel(f), bbox: bb(f), description: 'File input has no <progress>/[role=progressbar] in its container — large uploads appear frozen.', evidence: {} });
        if (!container.querySelector('button[class*="cancel" i], button[class*="abort" i], [aria-label*="cancel" i], [data-testid*="cancel"], .cancel-upload')) add({ issueType: 'uploadNoCancelButton', severity: 'low', selector: sel(f), bbox: bb(f), description: 'File input has no cancel/abort control near it — users stuck on bad uploads.', evidence: {} });
      }
    }

    // ── DATE ──
    for (const el of dateInputs) {
      const ctx = ((el.name || el.id || '') + ' ' + (el.labels && el.labels[0] ? el.labels[0].innerText : '')).toLowerCase();
      const futureOnly = /expir|due|appointment|schedule|reservation|booking|deliver|deadline/.test(ctx);
      if (futureOnly && !el.hasAttribute('min') && !el.hasAttribute('max')) add({ issueType: 'dateInputNoMinMax', severity: 'low', selector: sel(el), bbox: bb(el), description: 'Future-only date field has no min/max attribute.', evidence: { ctx: ctx.slice(0,40) } });
      if (futureOnly) { setNative(el, el.type === 'date' ? '2020-01-01' : '2020-01-01T00:00'); el.dispatchEvent(new Event('blur', { bubbles: true })); await sleep(200); if (!hasError(el)) add({ issueType: 'dateAllowsPastForFutureField', severity: 'medium', selector: sel(el), bbox: bb(el), description: 'Future-only field accepted a past date (2020-01-01) with no error.', evidence: {} }); setNative(el, ''); }
    }
    const rangeDates = [...document.querySelectorAll('input[type="date"], input[type="datetime-local"]')].filter(fvis);
    if (rangeDates.length >= 2 && rangeDates[0].form && rangeDates[0].form === rangeDates[1].form) {
      const s = rangeDates[0], e = rangeDates[1];
      setNative(s, '2025-12-31'); setNative(e, '2025-01-01'); e.dispatchEvent(new Event('blur', { bubbles: true })); await sleep(250);
      const c = e.closest('form') || e.parentElement; const anyErr = c && c.querySelector('[role="alert"], .error, .invalid-feedback, [data-testid*="error"]');
      if (!(e.getAttribute('aria-invalid') === 'true' || (anyErr && /(end|after|before|range|date)/i.test(anyErr.innerText || '')))) add({ issueType: 'dateRangeEndBeforeStart', severity: 'high', selector: sel(e), bbox: bb(e), description: 'Date range pair accepted end < start with no error.', evidence: {} });
      setNative(s, ''); setNative(e, '');
    }

    // ── OTP ──
    if (otpCands.length >= 4) {
      const boxes = otpCands.slice(0, 6);
      const dx = Math.abs(boxes[1].getBoundingClientRect().left - boxes[0].getBoundingClientRect().left);
      if (dx <= 200) {
        boxes.forEach((b, i) => { b.setAttribute('data-argus-otp', String(i)); tracked.otp.push(b); });
        boxes[0].focus(); setNative(boxes[0], '1'); key(boxes[0], '1'); await sleep(250);
        const focusedIdx = document.activeElement && document.activeElement.getAttribute('data-argus-otp');
        if (focusedIdx === null || parseInt(focusedIdx, 10) <= 0) add({ issueType: 'otpNoAutoAdvance', severity: 'medium', selector: sel(boxes[0]), bbox: bb(boxes[0]), description: 'Typing in an OTP box did not auto-advance focus to the next box.', evidence: {} });
        // backspace return
        const b2 = boxes[1]; b2.focus(); setNative(b2, ''); key(b2, 'Backspace'); await sleep(200);
        const fb = document.activeElement && document.activeElement.getAttribute('data-argus-otp');
        if (fb !== '0') add({ issueType: 'otpBackspaceNoReturn', severity: 'low', selector: sel(b2), bbox: bb(b2), description: 'Backspace on an empty OTP box did not return focus to the previous box.', evidence: {} });
        // paste distribution
        boxes.forEach(b => setNative(b, ''));
        boxes[0].focus();
        const dt = new DataTransfer(); dt.setData('text/plain', '123456'.slice(0, boxes.length));
        boxes[0].dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true, cancelable: true }));
        await sleep(250);
        let filled = 0; for (const b of boxes) if (b.value && b.value.length === 1) filled++;
        if (filled < boxes.length) add({ issueType: 'otpPasteNotDistributed', severity: 'medium', selector: sel(boxes[0]), bbox: bb(boxes[0]), description: 'Pasting a full code did not fill all OTP boxes.', evidence: { filled, total: boxes.length } });
        boxes.forEach(b => setNative(b, ''));
      }
    }

    // ── COMBOBOX ──
    cbCands.forEach((el, i) => { el.setAttribute('data-argus-cb', String(i)); tracked.cb.push(el); });
    for (const el of cbCands) {
      const hasAria = el.getAttribute('role') === 'combobox' || el.hasAttribute('aria-expanded') || el.hasAttribute('aria-haspopup') || !!el.querySelector('[role="combobox"]');
      if (!hasAria) add({ issueType: 'comboboxNoAria', severity: 'medium', selector: sel(el), bbox: bb(el), description: 'Combobox missing role=combobox / aria-expanded / aria-haspopup.', evidence: {} });
      const listVisible = () => { for (const c of document.querySelectorAll('[role="listbox"]:not([aria-hidden="true"]), [class*="menu"][class*="open"], [class*="dropdown"][class*="open"], [class*="listbox"]:not([hidden]), [data-state="open"][role="listbox"]')) { const r = c.getBoundingClientRect(); if (r.width > 50 && r.height > 20 && vis(c)) return true; } return false; };
      el.click(); await sleep(350);
      if (!listVisible()) { add({ issueType: 'comboboxWontOpen', severity: 'high', selector: sel(el), bbox: bb(el), description: 'Clicking the combobox did not open its listbox.', evidence: {} }); esc(); continue; }
      const optsBefore = [...document.querySelectorAll('[role="option"]:not([aria-hidden="true"])')].filter(vis).length;
      const input = el.querySelector('input') || (el.tagName.toLowerCase() === 'input' ? el : null);
      if (input) { input.focus(); setNative(input, 'a'); await sleep(350); const optsAfter = [...document.querySelectorAll('[role="option"]:not([aria-hidden="true"])')].filter(vis).length; if (optsAfter === optsBefore && optsBefore > 1) add({ issueType: 'comboboxNoTypeFilter', severity: 'medium', selector: sel(el), bbox: bb(el), description: 'Typing in the combobox did not filter the options.', evidence: { optsBefore, optsAfter } }); setNative(input, ''); await sleep(200); }
      const valBefore = input ? input.value : (el.innerText || '').trim().slice(0, 80);
      key(el, 'ArrowDown'); await sleep(150); (input || el).dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', keyCode: 13, bubbles: true })); await sleep(300);
      const valAfter = input ? input.value : (el.innerText || '').trim().slice(0, 80);
      if (valAfter === valBefore && optsBefore > 0) add({ issueType: 'comboboxEnterNoSelect', severity: 'high', selector: sel(el), bbox: bb(el), description: 'Enter on a highlighted option did not select it.', evidence: {} });
      el.click(); await sleep(250); // reopen to test escape
      if (listVisible()) { esc(); await sleep(250); if (listVisible()) add({ issueType: 'comboboxEscapeNoClose', severity: 'medium', selector: sel(el), bbox: bb(el), description: 'Escape did not close the combobox (keyboard trap).', evidence: {} }); }
      esc();
    }

    // ── TAG INPUT ──
    tagCands.forEach((el, i) => { el.setAttribute('data-argus-tag', String(i)); tracked.tag.push(el); });
    for (const container of tagCands) {
      const input = container.querySelector('input[type="text"], input:not([type])');
      if (!input) continue;
      const chipCount = () => [...container.querySelectorAll('[class*="chip"], [class*="tag"]:not(input), [role="button"][aria-label*="remove" i], [data-tag]')].filter(c => vis(c) && c.tagName.toLowerCase() !== 'input').length;
      const base = chipCount();
      input.focus(); setNative(input, 'argusTag1'); input.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', keyCode: 13, bubbles: true })); input.dispatchEvent(new KeyboardEvent('keyup', { key: 'Enter', keyCode: 13, bubbles: true })); await sleep(300);
      if (chipCount() <= base) add({ issueType: 'tagInputEnterNoAdd', severity: 'high', selector: sel(input), bbox: bb(container), description: 'Pressing Enter after typing did not create a chip.', evidence: { base } });
      const beforePaste = chipCount();
      input.focus(); const dt = new DataTransfer(); dt.setData('text/plain', 'argusA, argusB, argusC');
      input.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true, cancelable: true }));
      await sleep(150);
      if (!input.value && chipCount() === beforePaste) { setNative(input, 'argusA, argusB, argusC'); input.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true })); await sleep(200); }
      await sleep(200);
      if (chipCount() < beforePaste + 3) add({ issueType: 'tagInputPasteNoSplit', severity: 'medium', selector: sel(input), bbox: bb(container), description: 'Pasting "a, b, c" did not create 3 separate chips.', evidence: { added: chipCount() - beforePaste } });
      // remove
      const chips = [...container.querySelectorAll('[class*="chip"], [class*="tag"]:not(input), [data-tag]')];
      const ours = chips.find(c => /argus/i.test(c.innerText || ''));
      if (ours) { const beforeRemove = chipCount(); const rm = ours.querySelector('[aria-label*="remove" i], [class*="close"], [class*="remove"], button, svg'); try { (rm || ours).click(); } catch (_) {} await sleep(250); if (chipCount() >= beforeRemove) add({ issueType: 'tagInputRemoveBroken', severity: 'high', selector: sel(input), bbox: bb(container), description: 'Clicking X on a chip did not remove it.', evidence: {} }); }
    }

    // ── FORMATTED INPUTS ──
    if (cardF) { setNative(cardF, '1234567890123456'); cardF.dispatchEvent(new Event('blur', { bubbles: true })); await sleep(200); if (!hasError(cardF)) add({ issueType: 'cardAcceptsInvalidLuhn', severity: 'high', selector: sel(cardF), bbox: bb(cardF), description: 'Card field accepted a Luhn-fail number "1234567890123456".', evidence: {} }); setNative(cardF, ''); }
    if (expF) { setNative(expF, '01/20'); expF.dispatchEvent(new Event('blur', { bubbles: true })); await sleep(200); if (!hasError(expF)) add({ issueType: 'expiryAcceptsPastDate', severity: 'high', selector: sel(expF), bbox: bb(expF), description: 'Expiry field accepted a past date "01/20".', evidence: {} }); setNative(expF, ''); }
    if (cvvF) { setNative(cvvF, 'ab'); cvvF.dispatchEvent(new Event('blur', { bubbles: true })); await sleep(200); if (!hasError(cvvF) && /[a-z]/i.test(cvvF.value)) add({ issueType: 'cvvAcceptsLetters', severity: 'medium', selector: sel(cvvF), bbox: bb(cvvF), description: 'CVV field accepted letters instead of digits.', evidence: { value: cvvF.value } }); setNative(cvvF, ''); }
    if (phoneF) { setNative(phoneF, 'abc'); phoneF.dispatchEvent(new Event('blur', { bubbles: true })); await sleep(200); if (!hasError(phoneF) && /[a-z]/i.test(phoneF.value)) add({ issueType: 'phoneAcceptsLetters', severity: 'medium', selector: sel(phoneF), bbox: bb(phoneF), description: 'Phone field accepted letters "abc".', evidence: { value: phoneF.value } }); setNative(phoneF, ''); }
    if (numF && numF.positiveOnly) { setNative(numF.el, '-1'); numF.el.dispatchEvent(new Event('blur', { bubbles: true })); await sleep(200); if (!hasError(numF.el) && numF.el.value === '-1') add({ issueType: 'numberAcceptsNegative', severity: 'medium', selector: sel(numF.el), bbox: bb(numF.el), description: 'Positive-only number field accepted -1.', evidence: {} }); setNative(numF.el, ''); }
    if (numF && numF.integerOnly) { setNative(numF.el, '1.5'); numF.el.dispatchEvent(new Event('blur', { bubbles: true })); await sleep(200); if (!hasError(numF.el) && /\./.test(numF.el.value)) add({ issueType: 'numberAcceptsDecimal', severity: 'medium', selector: sel(numF.el), bbox: bb(numF.el), description: 'Integer (step=1) number field accepted 1.5.', evidence: {} }); setNative(numF.el, ''); }

    // ── MASKED INPUTS ──
    maskCands.forEach((m, i) => { m.el.setAttribute('data-argus-mask', String(i)); tracked.mask.push(m.el); });
    for (const m of maskCands) {
      const el = m.el;
      if (el.pattern) { setNative(el, /\d/.test(el.pattern) ? 'abc' : '!!!'); el.dispatchEvent(new Event('blur', { bubbles: true })); await sleep(200); if (!hasError(el)) add({ issueType: 'patternNotEnforced', severity: 'medium', selector: sel(el), bbox: bb(el), description: `pattern="${el.pattern}" present but a non-matching value was accepted.`, evidence: {} }); setNative(el, ''); }
      setNative(el, '1234567890'); await sleep(250);
      if (!/[\s().\-\/]/.test(el.value) && el.value.length >= 10) add({ issueType: 'maskNotApplied', severity: 'medium', selector: sel(el), bbox: bb(el), description: `${m.maskHint} mask did not apply format separators to raw digits.`, evidence: { value: el.value } });
      const lenBefore = el.value.length;
      el.focus(); for (let i = 0; i < 3; i++) { setNative(el, el.value.slice(0, -1)); key(el, 'Backspace'); await sleep(60); }
      if (lenBefore - el.value.length < 3) add({ issueType: 'maskBackspaceStuck', severity: 'low', selector: sel(el), bbox: bb(el), description: 'Backspace inside the mask got stuck on a separator char.', evidence: { lenBefore, lenAfter: el.value.length } });
      setNative(el, '');
    }

    // ── INLINE EDIT ──
    ieCands.forEach((el, i) => { el.setAttribute('data-argus-ie', String(i)); el.__argusOrig = (el.innerText || el.textContent || '').trim().slice(0, 200); tracked.ie.push(el); });
    for (const cell of ieCands) {
      const orig = cell.__argusOrig;
      cell.click(); await sleep(300);
      const inEdit = () => { if (cell.getAttribute('contenteditable') === 'true' && document.activeElement === cell) return { editing: true, focused: true }; const input = cell.querySelector('input:not([type="hidden"]), textarea'); if (input) return { editing: true, focused: document.activeElement === input, input }; if (/editing|active|focused/i.test(cell.className) || cell.getAttribute('data-state') === 'editing') return { editing: true, focused: !!cell.querySelector(':focus') }; return { editing: false, focused: false }; };
      const st = inEdit();
      if (!st.editing) { add({ issueType: 'inlineEditClickFails', severity: 'high', selector: sel(cell), bbox: bb(cell), description: 'Clicking the cell did not enter edit mode.', evidence: {} }); continue; }
      if (!st.focused) add({ issueType: 'inlineEditNoAutoFocus', severity: 'low', selector: sel(cell), bbox: bb(cell), description: 'Inline-edit input was not auto-focused.', evidence: {} });
      const target = st.input || cell;
      if (st.input) setNative(target, 'argusEditTest'); else { target.textContent = 'argusEditTest'; target.dispatchEvent(new Event('input', { bubbles: true })); }
      await sleep(150); key(target, 'Escape'); await sleep(250);
      const textNow = (cell.innerText || cell.textContent || '').trim().slice(0, 200);
      if (/argusEditTest/.test(textNow)) add({ issueType: 'inlineEditEscapeCommits', severity: 'high', selector: sel(cell), bbox: bb(cell), description: 'Escape did not cancel the edit — the modified value persisted.', evidence: {} });
      // re-enter + Enter commits / exits editing
      cell.click(); await sleep(250);
      const st2 = inEdit();
      if (st2.editing) { const t2 = st2.input || cell; if (st2.input) setNative(t2, orig || 'argusKeep'); t2.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', keyCode: 13, bubbles: true })); t2.dispatchEvent(new KeyboardEvent('keyup', { key: 'Enter', keyCode: 13, bubbles: true })); await sleep(250); if (inEdit().editing) add({ issueType: 'inlineEditEnterNoCommit', severity: 'medium', selector: sel(cell), bbox: bb(cell), description: 'Enter did not commit — the cell stayed in editing mode.', evidence: {} }); }
      key(cell, 'Escape'); await sleep(100);
    }

    // ── PASSWORD ──
    if (pwds.length > 0) {
      const primary = pwds[0];
      setNative(primary, '123'); primary.dispatchEvent(new Event('blur', { bubbles: true })); await sleep(250);
      let hasStrength = false;
      const strengthEls = document.querySelectorAll('[class*="strength"], [data-testid*="strength"], [aria-label*="strength" i], [class*="password-meter"], [role="progressbar"][aria-label*="password" i]');
      if (strengthEls.length) hasStrength = true;
      else { const c = primary.closest('label, div, fieldset, .form-group, .field') || primary.parentElement; if (c && c.querySelector('[role="alert"], .error, .invalid-feedback, [data-testid*="error"], .text-danger, .password-error')) hasStrength = true; }
      if (!hasStrength) add({ issueType: 'passwordNoStrengthFeedback', severity: 'medium', selector: sel(primary), bbox: bb(primary), description: '"123" accepted with no password strength indicator or weak-password feedback.', evidence: {} });
      if (pwds.length >= 2) {
        const confirm = pwds[1];
        setNative(primary, 'Argus#123'); setNative(confirm, 'Argus#124'); confirm.dispatchEvent(new Event('blur', { bubbles: true })); await sleep(250);
        const c = confirm.closest('label, div, fieldset, .form-group, .field, form') || confirm.parentElement;
        const err = c && c.querySelector('[role="alert"], .error, .invalid-feedback, [data-testid*="error"], .text-danger, .field-error');
        if (!(confirm.getAttribute('aria-invalid') === 'true' || (err && /match|same|confirm|differ/i.test(err.innerText || '')))) add({ issueType: 'confirmPasswordNoMismatchError', severity: 'high', selector: sel(confirm), bbox: bb(confirm), description: 'Mismatching primary + confirm password shows no error.', evidence: {} });
        setNative(confirm, '');
      }
      setNative(primary, '');
    }
  } finally {
    // ── MANDATORY IDEMPOTENT CLEANUP ──
    esc();
    for (const el of tracked.otp) { try { setNative(el, ''); el.removeAttribute('data-argus-otp'); } catch (_) {} }
    for (const el of tracked.cb) { try { el.removeAttribute('data-argus-cb'); } catch (_) {} }
    for (const el of tracked.tag) { try { const chips = [...el.querySelectorAll('[class*="chip"], [class*="tag"]:not(input), [data-tag]')]; for (const c of chips) if (/argus/i.test(c.innerText || '')) { const rm = c.querySelector('[aria-label*="remove" i], [class*="close"], [class*="remove"], button, svg'); try { (rm || c).click(); } catch (_) {} } el.removeAttribute('data-argus-tag'); } catch (_) {} }
    for (const el of tracked.mask) { try { setNative(el, ''); el.removeAttribute('data-argus-mask'); } catch (_) {} }
    for (const el of tracked.ie) { try { el.removeAttribute('data-argus-ie'); delete el.__argusOrig; } catch (_) {} }
    for (const el of document.querySelectorAll('input[type="date"], input[type="time"], input[type="datetime-local"]')) { try { setNative(el, ''); } catch (_) {} }
    for (const p of document.querySelectorAll('input[type="password"]')) { try { setNative(p, ''); } catch (_) {} }
  }

  return out;
}
```

## MCP steps (for file upload with a real file — `fileNoSelectionFeedback` only)

Choosing a real file needs the OS dialog, which a probe can't open. Run this when a file input exists AND a fixture file is available at `{plugin-root}/.tmp/qa-fixtures/tiny.txt`:

```
1. browser_file_upload({ paths: ['{plugin-root}/.tmp/qa-fixtures/tiny.txt'] })   // targets the focused/visible file input
2. browser_wait_for(time = 600)
3. r = browser_evaluate(probe.checkFilenameDisplayed, { expectedName: 'tiny.txt' })
4. If !r.displayed → emit fileNoSelectionFeedback (medium)
     description: 'After selecting a file, no UI shows the file name.'
5. browser_evaluate(probe.resetFileInputs)   // cleanup
```

```js
// probe.checkFilenameDisplayed — args: { expectedName }
({expectedName}) => {
  const input = document.querySelector('input[type="file"]');
  if (!input) return { displayed: false };
  const inputHasFile = input.files && input.files.length > 0 && input.files[0].name.includes(expectedName);
  const container = input.closest('label, div, fieldset, .form-group, .upload, .file-input, form') || input.parentElement;
  const text = container ? container.innerText : '';
  return { displayed: inputHasFile && text.includes(expectedName), inputHasFile, visibleFileName: text.includes(expectedName) };
}
```

```js
// probe.resetFileInputs
() => { for (const el of document.querySelectorAll('input[type="file"]')) { try { el.value = ''; el.dispatchEvent(new Event('change', { bubbles: true })); } catch (_) {} } return { ok: true }; }
```

## Issues
| issueType | severity | description |
|---|---|---|
| dateInputNoMinMax | low | Date input missing min/max attrs in future-only context |
| dateAllowsPastForFutureField | medium | Future-only field accepted a past date |
| dateRangeEndBeforeStart | high | Date range pair accepted end < start |
| datePickerKeyboardTrap | medium | Date picker opens but keyboard nav doesn't move through cells |
| fileAcceptMissing | medium | No accept= attribute — any file type accepted |
| fileSizeHintMissing | low | No visible "max N MB" hint near file input |
| fileNoSelectionFeedback | medium | After upload, no UI shows the file name (MCP) |
| uploadNoProgressUI | medium | No progress element near the file input |
| uploadNoCancelButton | low | No cancel/abort control near the file input |
| otpNoAutoAdvance | medium | Keystroke does not advance focus to next box |
| otpBackspaceNoReturn | low | Backspace on empty box doesn't return to previous |
| otpPasteNotDistributed | medium | Pasting full code doesn't fill all boxes |
| comboboxWontOpen | high | Click doesn't open listbox |
| comboboxNoTypeFilter | medium | Typing doesn't filter options |
| comboboxEnterNoSelect | high | Enter on highlighted option doesn't select |
| comboboxEscapeNoClose | medium | Escape doesn't close (keyboard trap) |
| comboboxNoAria | medium | Missing role=combobox / aria-expanded / aria-haspopup |
| tagInputEnterNoAdd | high | Enter after typing doesn't create chip |
| tagInputPasteNoSplit | medium | Pasting "a, b, c" doesn't create 3 chips |
| tagInputRemoveBroken | high | Click X on chip doesn't remove it |
| cardAcceptsInvalidLuhn | high | Card field accepted Luhn-fail number |
| expiryAcceptsPastDate | high | Expiry field accepted past date |
| cvvAcceptsLetters | medium | CVV field accepted letters |
| phoneAcceptsLetters | medium | Phone field accepted letters |
| numberAcceptsNegative | medium | Positive-only number accepted -1 |
| numberAcceptsDecimal | medium | Integer-only number accepted 1.5 |
| patternNotEnforced | medium | pattern= present but non-matching value accepted |
| maskNotApplied | medium | Mask didn't apply format separators |
| maskBackspaceStuck | low | Backspace stuck on separator char |
| inlineEditClickFails | high | Click cell doesn't enter edit mode |
| inlineEditNoAutoFocus | low | Edit input not auto-focused |
| inlineEditEscapeCommits | high | Escape doesn't cancel — modified value persists |
| inlineEditEnterNoCommit | medium | Enter doesn't commit — cell stuck editing |
| passwordNoStrengthFeedback | medium | "123" accepted without strength indicator |
| confirmPasswordNoMismatchError | high | Mismatching primary + confirm shows no error |

## Migration
```toml
[detectors]
qa-form-input-types        = true   # NEW
qa-test-form-datetime      = false
qa-test-form-file-upload   = false
qa-test-form-otp           = false
qa-test-form-combobox      = false
qa-test-form-tag-input     = false
qa-test-form-formatted-inputs = false
qa-test-form-input-mask    = false
qa-test-form-inline-edit   = false
qa-test-form-password-rules = false
```

## Notes on this conversion
- 8 of 9 widget types (date, OTP, combobox, tag, formatted, masked, inline-edit, password) + the file PASSIVE checks now run as ONE in-page async probe instead of one discovery + dozens of per-widget MCP round-trips. All the old per-probe helpers (`discoverAllWidgets`, `checkDateError`, `findDateRangePair`, `checkRangeError`, `checkOtpFocused`, `simulateOtpPaste`, `checkOtpAllFilled`, `checkListboxVisible`, `snapshotComboboxOptions`, `getActiveOptionText`, `getComboboxValue`, `countTagChips`, `simulateTagPaste`, `removeArgusTagChip`, `checkInputError`, `checkPatternRejection`, `getMaskedValue`, `checkInlineEditMode`, `checkInlineCellText`, `checkPasswordStrengthIndicator`, `checkConfirmPasswordMismatchError`, and all cleanup probes) are inlined; cleanup runs in a `finally` block.
- **Folded out:** `datePickerKeyboardTrap` — its recipe needs a real native picker opened via `Alt+ArrowDown` / OS calendar focus traversal that a probe can't reliably exercise; the issueType is preserved in the table but is not emitted by the probe (re-add as MCP steps if a custom (non-native) picker needs it).
- **Kept MCP (`executable: partial`):** `fileNoSelectionFeedback` — selecting a real file requires `browser_file_upload` (OS file dialog). All other file checks are in the probe.
- All 35 issueType names preserved exactly.
