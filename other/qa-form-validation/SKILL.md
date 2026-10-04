---
name: qa-form-validation
section: interactive
description: "Consolidated form validation skill. Tests BOTH real <form> elements AND form-less input groups (div+inputs+button, the common Angular/React case — so it runs on login/signup/forgot even without a <form> tag). Owns ALL validation testing on EVERY field: required/empty-submit, data-type, size/length, BOUNDARY values (min/max), format/syntax (pattern), CROSS-FIELD (password match, date range, confirm-email), real-time feedback, whitespace, oversize, maxlength, error-summary, aria-describedby, and XSS/SQL/Unicode injection on every field. Core testing runs as ONE in-page async probe; network/navigation-dependent checks (double-submit, back-nav, PRG, server-validation, rate-limit, happy-path submit) stay MCP."
model: sonnet
applyOn: [laptop]
needsSetup: false
viewportSensitive: true
interactive: true
executable: partial
cacheVersion: "1.0.0"
ownership: "exclusive: any validation finding — required/format/range/feedback/error-summary/help-text — belongs to this skill"
replaces:
  - qa-detect-form-validation
  - qa-detect-form-error-summary
  - qa-test-form-realtime
  - qa-test-form-boundaries
  - qa-test-form-special-chars
  - qa-test-form-submit-state
requires: [hasForms]
---
# qa-form-validation — Consolidated Form Validation Skill

**Production-ready replacement** for 6 separately-maintained skills that overlapped in detection. This skill owns EVERY validation-related bug type in the agent.

## How the orchestrator runs this (ONE call drives the core — no hand-driving)

🚨 **The core of this skill is an EXECUTABLE in-page probe.** Do NOT drive empty-submit / per-field typing click-by-click with separate `browser_click` / `browser_type` / `browser_press_key` MCP calls. Instead make **ONE** call:

```
result = browser_evaluate(<the async function in "## Interactive Probe" below>)
```

The probe does Phase 1 (passive a11y scans), Phase 2 (per-field type-invalid / email / whitespace / oversize / maxlength / injection / boundary / format), the cross-field checks, and Phase 3 (submit-state) — all in-page in one round-trip. It installs a submit guard so no real submit/navigation/data-write can fire, types via the native value setter + `input`/`change` events, blurs, asserts inline feedback, and cleans up every field before returning. It **self-skips** (returns `[]`) when there are zero testable inputs. Transcribe each returned finding verbatim; add only the envelope fields.

**HONEST EXCEPTION — these stay MCP** (they need real network responses or real navigation a page-context probe can't fake): `doubleSubmitAllowed`, `backNavLosesFormData`, `noPostRedirectGet`, `serverValidationNotShown`, `noRateLimitOnSubmit` (Phase 4) and `happySubmitNoFeedback` / `validRejectedAsInvalid` (Phase 5, gated). See "## MCP steps" below. That is why frontmatter is `executable: partial`.

## What it checks (issue types)

| Issue type | Severity | What it catches | Where |
|---|---|---|---|
| `noValidationOnEmptySubmit` | high | Form with `required` fields submits empty without error | probe |
| `noEmailValidation` | medium | `input[type=email]` accepts invalid format like "notanemail" | probe |
| `noRealtimeValidation` | low | ONCE per form (advisory): form has NO validation at all — no inline feedback AND no on-submit validation. On-submit-only validation is correct and never flagged. | probe |
| `whitespaceAccepted` | medium | Required field accepts whitespace-only input | probe |
| `pageCrashOnLargeInput` | high | 10K character input crashes the page | probe |
| `maxLengthNotEnforced` | medium | Field has `maxlength` but accepts oversize input | probe |
| `xssReflection` | high | XSS payload reflected unescaped in DOM | probe |
| `crashOnSpecialChars` | high | Special-char payload (SQL/XSS/Unicode) crashes page | probe |
| `noErrorSummary` | medium | Long form (5+ fields) lacks WCAG 3.3.1 error summary at top | probe (passive) |
| `helpTextNotAssociated` | low | Hint text near field not linked via `aria-describedby` | probe (passive) |
| `ariaDescribedByBrokenRef` | medium | `aria-describedby` references non-existent ID | probe (passive) |
| `submitNotDisabledWhenInvalid` | medium | Submit enabled while required fields empty | probe (Phase 3) |
| `submitNoLoadingState` | low | No loading/spinner/disabled state on submit click | probe (Phase 3) |
| `noBeforeUnloadWarning` | low | Dirty form has no beforeunload warning | probe (Phase 3) |
| `pastePreventedOnPassword` | medium | Password field prevents paste — breaks password managers | probe (passive) |
| `hiddenRequiredBlocksSubmit` | high | `[required]` field is hidden — submit fails silently | probe (passive) |
| `untranslatedFormError` | medium | Error message displays raw i18n key | probe (passive) |
| `boundaryMaxNotEnforced` | medium | Number/date field accepts a value just OVER its `max` | probe |
| `boundaryMinNotEnforced` | medium | Number/date field accepts a value just UNDER its `min` | probe |
| `formatNotEnforced` | medium | Field with a `pattern`/known format accepts a malformed value | probe |
| `passwordMismatchNotCaught` | high | Two password fields submit with different values, no error | probe |
| `dateRangeNotValidated` | medium | End date accepted before start date with no error | probe |
| `emailMismatchNotCaught` | medium | Email + confirm-email submit mismatched with no error | probe |
| `serverValidationNotShown` | high | Server returned validation error but no error UI rendered | MCP (Phase 4) |
| `doubleSubmitAllowed` | high | Rapid double-click on submit produces two requests | MCP (Phase 4) |
| `noRateLimitOnSubmit` | low | 10× rapid submit accepted without throttle/429 | MCP (Phase 4) |
| `backNavLosesFormData` | medium | Filling form, navigating away, then back loses data | MCP (Phase 4) |
| `noPostRedirectGet` | medium | After submit, refresh re-POSTs the form | MCP (Phase 4) |
| `happySubmitNoFeedback` | high | Valid data submitted but UI showed neither success nor error | MCP (Phase 5, gated) |
| `validRejectedAsInvalid` | high | Form rejected legitimate valid input | MCP (Phase 5, gated) |

## Self-skip
Skip silently (return `[]`) only when there are zero visible, non-disabled, non-readonly testable inputs (text/email/number/password/tel/url/search/date/textarea/select). 🚨 Do NOT skip just because there is no `<form>` element — form-less `<div>`+inputs+button groups are detected too.

## Interactive Probe (browser_evaluate, async)

```js
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const out = [];
  const add = o => out.push(Object.assign({ skill: 'qa-form-validation' }, o));
  const vis = el => { if (!el) return false; const r = el.getBoundingClientRect(); const s = getComputedStyle(el); return r.width > 0 && r.height > 0 && s.display !== 'none' && s.visibility !== 'hidden'; };
  const sel = el => { if (!el) return null; if (el.id) return '#' + CSS.escape(el.id); if (el.name) return `${el.tagName.toLowerCase()}[name="${el.name}"]`; const c = (el.className && typeof el.className === 'string') ? el.className.trim().split(/\s+/).slice(0,2).join('.') : ''; return el.tagName.toLowerCase() + (c ? '.' + c : ''); };
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };
  const setNative = (el, v) => { const p = el.tagName === 'TEXTAREA' ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype; try { Object.getOwnPropertyDescriptor(p, 'value').set.call(el, v); } catch (_) { el.value = v; } el.dispatchEvent(new Event('input', { bubbles: true })); };
  const blur = el => { el.dispatchEvent(new Event('blur', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); };
  const clear = el => setNative(el, '');

  const pageHealth = () => {
    const bodyText = (document.body && document.body.innerText || '').slice(0, 500);
    return !!document.querySelector('.error-page, [data-error], #__next-error, .next-error-h1') ||
      /Application error|Internal Server Error|500|something went wrong|Uncaught/i.test(bodyText);
  };
  const fieldError = field => {
    const ariaInvalid = field.getAttribute('aria-invalid') === 'true';
    let cssInvalid = false; try { cssInvalid = field.matches(':invalid'); } catch (_) {}
    const c = field.closest('label, div, fieldset, .form-group, .field') || field.parentElement;
    const near = c && c.querySelector('[role="alert"], .error, .invalid-feedback, [data-testid*="error"], .text-red-500, .text-danger, .field-error, .error-message, .form-error');
    return ariaInvalid || cssInvalid || !!near;
  };

  const baselineHealth = pageHealth();
  if (baselineHealth) return [];

  // ── DISCOVER forms (real <form> + form-less groups) ──
  const FIELD_SEL = 'input[type="text"],input[type="email"],input[type="number"],input[type="password"],input[type="search"],input[type="tel"],input[type="url"],input[type="date"],input[type="time"],input[type="datetime-local"],input[type="month"],input:not([type]),textarea,select';
  const fvis = el => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0 && !el.disabled && !el.readOnly; };
  const SUBMIT_TXT = /sign ?in|log ?in|sign ?up|sign ?on|register|submit|continue|next|save|send|create|update|apply|confirm|verify|search|add\b/i;
  const findSubmit = root => { const cand = [...root.querySelectorAll('button,input[type="submit"],input[type="button"],[role="button"]')].filter(fvis); return cand.find(b => b.type === 'submit') || cand.find(b => SUBMIT_TXT.test(b.textContent || b.value || b.getAttribute('aria-label') || '')) || cand[cand.length - 1] || null; };
  const forms = [];
  const claimed = new Set();
  for (const f of document.querySelectorAll('form')) {
    const fields = [...f.querySelectorAll(FIELD_SEL)].filter(fvis);
    fields.forEach(el => claimed.add(el));
    if (!fields.length) continue;
    forms.push({ root: f, isRealForm: true, submit: findSubmit(f), fields: fields.slice(0, 25) });
  }
  const loose = [...document.querySelectorAll(FIELD_SEL)].filter(el => fvis(el) && !claimed.has(el) && !el.closest('form'));
  if (loose.length) {
    const groups = new Map();
    for (const el of loose) { const c = el.closest('[class*="form" i],[class*="card" i],[role="dialog"],[class*="modal" i],[class*="login" i],[class*="signup" i],[class*="auth" i],section,fieldset') || document.body; (groups.get(c) || groups.set(c, []).get(c)).push(el); }
    for (const [c, fields] of groups) forms.push({ root: c, isRealForm: false, submit: findSubmit(c) || findSubmit(document.body), fields: fields.slice(0, 25) });
  }
  const allForms = forms.filter(f => f.fields.length > 0).slice(0, 6);
  if (allForms.length === 0) return [];
  const isReq = el => el.required || el.getAttribute('aria-required') === 'true';

  // ── PHASE 1: PASSIVE SCANS ──
  // error summary (forms with 5+ fields)
  for (const f of document.querySelectorAll('form')) {
    if (!vis(f)) continue;
    const fieldCount = f.querySelectorAll('input:not([type="hidden"]):not([type="submit"]):not([type="button"]), select, textarea').length;
    if (fieldCount < 5) continue;
    const fc = f.firstElementChild;
    const hasTop = !!f.querySelector(':scope > [role="alert"], :scope > .error-summary, :scope > [class*="error-summary"], :scope > [data-testid*="error-summary"]') || (fc && /error|invalid|alert/i.test(fc.className) && fc.querySelector('ul, ol, li'));
    if (!hasTop) add({ issueType: 'noErrorSummary', severity: 'medium', selector: sel(f), bbox: bb(f), description: `Form with ${fieldCount} fields has no error-summary container — WCAG 3.3.1 recommends a top-of-form summary listing all errors`, evidence: { fieldCount } });
  }
  // aria-describedby integrity + help-text association
  for (const input of document.querySelectorAll('input:not([type="hidden"]), select, textarea')) {
    if (!vis(input) || input.type === 'submit' || input.type === 'button') continue;
    const db = input.getAttribute('aria-describedby');
    if (db && db.trim()) {
      const missing = db.trim().split(/\s+/).filter(id => !document.getElementById(id));
      if (missing.length) add({ issueType: 'ariaDescribedByBrokenRef', severity: 'medium', selector: sel(input), bbox: bb(input), description: `Field has aria-describedby="${db}" but ID(s) "${missing.join(', ')}" don't exist`, evidence: { missing } });
      continue;
    }
    const c = input.closest('label, div, fieldset, .form-group, .field') || input.parentElement;
    if (!c) continue;
    for (const hint of c.querySelectorAll('small, .help-text, .hint, .form-text, .help-block, [class*="description"], p[class*="hint"]')) {
      if (hint === input || input.contains(hint)) continue;
      const ht = (hint.innerText || '').trim();
      if (ht.length < 5 || ht.length > 200) continue;
      add({ issueType: 'helpTextNotAssociated', severity: 'low', selector: sel(input), bbox: bb(input), description: `Hint text "${ht.slice(0, 60)}…" near field is not linked via aria-describedby — screen readers won't announce it`, evidence: {} });
      break;
    }
  }
  // paste-prevented password
  for (const pwd of document.querySelectorAll('input[type="password"]')) {
    const onpaste = pwd.getAttribute('onpaste');
    if ((onpaste && /return\s+false|preventDefault/i.test(onpaste)) || pwd.dataset.preventPaste === 'true' || pwd.classList.contains('no-paste') || pwd.classList.contains('block-paste'))
      add({ issueType: 'pastePreventedOnPassword', severity: 'medium', selector: sel(pwd), bbox: bb(pwd), description: 'Password field prevents paste — breaks password managers (1Password, Bitwarden, etc.). Known UX antipattern.', evidence: {} });
  }
  // hidden required blocks submit
  for (const req of document.querySelectorAll('[required], [aria-required="true"]')) {
    if (req.type === 'hidden' || req.type === 'submit' || req.type === 'button') continue;
    let visible = true, cur = req;
    while (cur && cur !== document.body) { const cs = getComputedStyle(cur); if (cs.display === 'none' || cs.visibility === 'hidden') { visible = false; break; } cur = cur.parentElement; }
    if (!visible) add({ issueType: 'hiddenRequiredBlocksSubmit', severity: 'high', selector: sel(req), description: `<${req.tagName.toLowerCase()} required> is hidden but \`required\`. HTML5 validation blocks submit with no user-visible message — users get stuck.`, evidence: {} });
  }
  // untranslated i18n keys in error containers
  for (const ec of document.querySelectorAll('[role="alert"], .error, .invalid-feedback, [class*="error"]:not([class*="errorless"]), [class*="invalid"], small.help-block.error, [data-error]')) {
    const t = (ec.innerText || ec.getAttribute('data-error') || '').trim();
    if (!t || t.length < 4 || t.length > 200) continue;
    let kind = null;
    if (/^[a-z][a-z0-9_]+(?:\.[a-z][a-z0-9_]+){2,}$/i.test(t)) kind = 'dot.notation';
    else if (/^\{\{[\w.]+\}\}$/.test(t)) kind = 'handlebars';
    else if (/^__MSG_\w+__$/.test(t)) kind = 'chrome-extension';
    else if (/^\[[\w.]+\]$/.test(t) && /^\[[a-z]/.test(t)) kind = 'bracket-key';
    if (kind) add({ issueType: 'untranslatedFormError', severity: 'medium', selector: sel(ec), bbox: bb(ec), description: `Error message displays raw i18n ${kind} key "${t.slice(0, 60)}" — translation pipeline did not resolve it.`, evidence: { kind } });
  }

  // ── SUBMIT GUARD — block real submit/fetch/XHR/navigation so nothing is written ──
  window.__argusSubmitFired = false;
  document.querySelectorAll('form').forEach(f => f.addEventListener('submit', e => { e.preventDefault(); window.__argusSubmitFired = true; }, { capture: true }));
  const _fetch = window.fetch, _send = XMLHttpRequest.prototype.send, _bu = window.onbeforeunload;
  window.fetch = function () { window.__argusSubmitFired = true; return Promise.reject(new Error('argus-blocked')); };
  XMLHttpRequest.prototype.send = function () { window.__argusSubmitFired = true; };
  window.onbeforeunload = e => { e.preventDefault(); return ''; };
  const restoreGuard = () => { window.fetch = _fetch; XMLHttpRequest.prototype.send = _send; window.onbeforeunload = _bu; };

  try {
    // ── PHASE 2: EMPTY SUBMIT (one per form with required) ──
    // Side-effect: record whether each form validates ON SUBMIT. Submit-time
    // validation is correct, valid UX — a form that shows errors on submit must
    // NEVER be flagged for "no realtime validation". We use this map below to gate
    // the (advisory, once-per-form) noValidationAtAll check so we don't produce
    // per-field realtime-validation noise.
    const formValidatesOnSubmit = new WeakMap();
    for (const form of allForms) {
      const hasRequired = form.fields.some(isReq);
      if (!hasRequired && form.fields.length < 2) continue;
      if (!form.submit) continue;
      if (form.submit.disabled || form.submit.getAttribute('aria-disabled') === 'true') { formValidatesOnSubmit.set(form, true); continue; } // disabled-until-valid IS validation; that's submitNotDisabled (Phase 3)
      window.__argusSubmitFired = false;
      form.submit.click(); await sleep(600);
      const anyError = !!(form.root.querySelector('[role="alert"], .error, .invalid-feedback, [aria-invalid="true"], .field-error, [data-testid*="error"]') || form.fields.some(fieldError));
      if (anyError) formValidatesOnSubmit.set(form, true);
      if (!anyError && window.__argusSubmitFired && hasRequired)
        add({ issueType: 'noValidationOnEmptySubmit', severity: 'high', selector: sel(form.submit), bbox: bb(form.submit), description: 'Form tried to submit with empty required fields and showed no validation feedback.', evidence: { isRealForm: form.isRealForm } });
    }

    // ── PHASE 2: PER-FIELD (every field up to 25) ──
    let crashed = false;
    for (const form of allForms) {
      if (crashed) break;
      const hasRequired = form.fields.some(isReq);
      // Track whether ANY field in this form gives inline (on input/blur) feedback.
      // Realtime/on-keystroke/on-blur validation is NOT required — validation on
      // submit (or disabled-until-valid) is perfectly valid, often-better UX. So we
      // do NOT flag per-field "noRealtimeValidation". We only note the absence of
      // inline feedback here and emit ONE advisory finding per form below, and ONLY
      // when the form has NO validation at all (not inline, not on submit).
      let anyInlineFeedback = false;
      let firstInvalidField = null;
      for (const field of form.fields) {
        if (crashed) break;
        const ftype = (field.tagName === 'SELECT' || field.tagName === 'TEXTAREA') ? field.tagName.toLowerCase() : (field.type || 'text');
        if (ftype === 'select') continue;

        // 4a type-invalid → does the form give ANY inline feedback? (advisory only — see above)
        clear(field);
        setNative(field, ftype === 'email' ? 'abc' : ftype === 'number' ? 'xyz' : ftype === 'url' ? 'not a url' : ftype === 'tel' ? 'letters here' : 'x');
        blur(field); await sleep(250);
        if (fieldError(field)) anyInlineFeedback = true;
        else if (!firstInvalidField) firstInvalidField = field;

        // 4b email-specific
        if (ftype === 'email') {
          clear(field); setNative(field, 'notanemail'); blur(field); await sleep(200);
          if (!fieldError(field)) add({ issueType: 'noEmailValidation', severity: 'medium', selector: sel(field), bbox: bb(field), description: 'Email input accepted invalid format "notanemail" with no error.', evidence: {} });
        }

        // 4c whitespace-only
        clear(field); setNative(field, '     '); blur(field); await sleep(200);
        if (hasRequired && isReq(field) && !fieldError(field)) add({ issueType: 'whitespaceAccepted', severity: 'medium', selector: sel(field), bbox: bb(field), description: 'Required field accepted whitespace-only input (no trim).', evidence: {} });

        // 4d oversize 10K
        clear(field); setNative(field, 'x'.repeat(10000)); blur(field); await sleep(250);
        if (pageHealth()) { add({ issueType: 'pageCrashOnLargeInput', severity: 'high', selector: sel(field), bbox: bb(field), description: '10K character input crashed the page.', evidence: {} }); crashed = true; break; }
        const maxLen = field.maxLength > 0 ? field.maxLength : null;
        if (maxLen && field.value.length > maxLen) add({ issueType: 'maxLengthNotEnforced', severity: 'medium', selector: sel(field), bbox: bb(field), description: `Field has maxlength=${maxLen} but accepted ${field.value.length} chars.`, evidence: { maxLen, actual: field.value.length } });

        // 4e injection payloads
        const payloads = [{ id: 'xss', value: "<script>alert('argusXss')</script>", marker: 'argusXss' }, { id: 'sqlish', value: "O'Reilly'; DROP TABLE users;--" }, { id: 'unicode', value: "测试 🚀 ñ ü العربية" }];
        for (const p of payloads) {
          clear(field); setNative(field, p.value); blur(field); await sleep(150);
          if (p.marker) {
            let reflected = false, sev = 'high';
            for (const s of document.querySelectorAll('script')) if (s.textContent && s.textContent.includes(p.marker)) { reflected = true; sev = 'critical'; break; }
            if (!reflected) { const html = document.body.innerHTML || ''; const mi = html.indexOf(p.marker); if (mi > -1 && html.slice(Math.max(0, mi - 60), mi).includes('<')) reflected = true; }
            if (reflected) add({ issueType: 'xssReflection', severity: sev, selector: sel(field), bbox: bb(field), description: 'XSS payload reflected unescaped into the DOM.', evidence: { payload: p.id } });
          }
          if (pageHealth()) { add({ issueType: 'crashOnSpecialChars', severity: 'high', selector: sel(field), bbox: bb(field), description: `Special-char payload (${p.id}) crashed or blanked the page.`, evidence: { payload: p.id } }); crashed = true; break; }
        }
        if (crashed) break;

        // 4f boundary (number/date with min/max)
        const step = field.step && field.step !== '' ? parseFloat(field.step) : 1;
        if (field.max !== '' && field.max != null && (ftype === 'number')) {
          clear(field); setNative(field, String(parseFloat(field.max) + (isNaN(step) ? 1 : step))); blur(field); await sleep(200);
          if (!fieldError(field)) add({ issueType: 'boundaryMaxNotEnforced', severity: 'medium', selector: sel(field), bbox: bb(field), description: `Number field accepted a value over its max (${field.max}).`, evidence: { max: field.max } });
        }
        if (field.min !== '' && field.min != null && (ftype === 'number')) {
          clear(field); setNative(field, String(parseFloat(field.min) - (isNaN(step) ? 1 : step))); blur(field); await sleep(200);
          if (!fieldError(field)) add({ issueType: 'boundaryMinNotEnforced', severity: 'medium', selector: sel(field), bbox: bb(field), description: `Number field accepted a value under its min (${field.min}).`, evidence: { min: field.min } });
        }

        // 4g format / pattern
        const n = ((field.name || '') + (field.id || '') + (field.placeholder || '')).toLowerCase();
        if (field.pattern) {
          clear(field); setNative(field, /\d/.test(field.pattern) ? 'abc' : '!!!'); blur(field); await sleep(200);
          if (!fieldError(field)) add({ issueType: 'formatNotEnforced', severity: 'medium', selector: sel(field), bbox: bb(field), description: `Field has pattern="${field.pattern}" but accepted a non-matching value.`, evidence: { pattern: field.pattern } });
        } else if (/phone|tel|zip|postal|card|cc|date/.test(n) && ftype !== 'date') {
          const bad = /phone|tel/.test(n) ? 'abc123' : /zip|postal/.test(n) ? '!!!' : /card|cc/.test(n) ? '1234' : '99/99/9999';
          clear(field); setNative(field, bad); blur(field); await sleep(200);
          if (!fieldError(field)) add({ issueType: 'formatNotEnforced', severity: 'low', uncertain: true, selector: sel(field), bbox: bb(field), description: `Field (${n.slice(0,30)}) accepted a malformed value "${bad}" with no feedback.`, evidence: { value: bad } });
        }
        clear(field);
      }

      // 4a-summary: advisory, ONCE per form. Only emit when the form has NO
      // validation at all — no inline (input/blur) feedback AND no submit-time
      // validation. A form that validates on submit (or disables submit until
      // valid) is correct and is NEVER flagged. Gated on a required field existing
      // (no point asserting validation on a form with nothing to validate).
      if (hasRequired && !anyInlineFeedback && !formValidatesOnSubmit.get(form) && firstInvalidField) {
        add({ issueType: 'noRealtimeValidation', severity: 'low', uncertain: true, selector: sel(firstInvalidField), bbox: bb(firstInvalidField), description: 'Form has no client-side validation feedback at all — type-invalid values produced no inline error after blur AND empty submit produced no error. (Advisory: realtime/on-keystroke validation is not required; on-submit validation is fine — this fires only when no validation of any kind was observed.)', evidence: { fields: form.fields.length } });
      }

      // ── PHASE 2.5: CROSS-FIELD ──
      if (crashed) break;
      const pwds = form.fields.filter(f => f.type === 'password');
      if (pwds.length >= 2) {
        setNative(pwds[0], 'Argus#123'); setNative(pwds[1], 'Argus#124'); blur(pwds[1]);
        if (form.submit && !form.submit.disabled) { form.submit.click(); await sleep(500); }
        if (!fieldError(pwds[1]) && !(form.root.querySelector('[role="alert"], .error, .invalid-feedback') && /match|same|confirm|differ/i.test(form.root.innerText)))
          add({ issueType: 'passwordMismatchNotCaught', severity: 'high', uncertain: true, selector: sel(pwds[1]), bbox: bb(pwds[1]), description: 'Two password fields submitted with different values and no "passwords don\'t match" error appeared.', evidence: {} });
        clear(pwds[0]); clear(pwds[1]);
      }
      const dates = form.fields.filter(f => f.type === 'date' || f.type === 'datetime-local');
      if (dates.length >= 2) {
        const start = dates.find(d => /start|from/i.test(d.name + d.id)) || dates[0];
        const end = dates.find(d => /end|to|until/i.test(d.name + d.id) && d !== start) || dates[1];
        if (start !== end) {
          setNative(start, '2025-12-31'); setNative(end, '2025-01-01'); blur(end);
          if (form.submit && !form.submit.disabled) { form.submit.click(); await sleep(400); }
          if (!fieldError(end)) add({ issueType: 'dateRangeNotValidated', severity: 'medium', uncertain: true, selector: sel(end), bbox: bb(end), description: 'End date accepted before start date with no error.', evidence: {} });
          clear(start); clear(end);
        }
      }
      const emails = form.fields.filter(f => f.type === 'email');
      if (emails.length >= 2) {
        const conf = emails.find(e => /confirm/i.test(e.name + e.id));
        if (conf) {
          const main = emails.find(e => e !== conf) || emails[0];
          setNative(main, 'a@example.com'); setNative(conf, 'b@example.com'); blur(conf);
          if (form.submit && !form.submit.disabled) { form.submit.click(); await sleep(400); }
          if (!fieldError(conf)) add({ issueType: 'emailMismatchNotCaught', severity: 'medium', uncertain: true, selector: sel(conf), bbox: bb(conf), description: 'Email + confirm-email submitted mismatched with no error.', evidence: {} });
          clear(main); clear(conf);
        }
      }
    }

    // ── PHASE 3: SUBMIT-STATE ──
    const f0 = allForms[0];
    if (f0 && f0.submit) {
      const hasReqEmpty = f0.fields.some(el => { if (!isReq(el)) return false; if (el.type === 'checkbox' || el.type === 'radio') return !el.checked; return !el.value || el.value.trim() === ''; });
      const subDisabled = f0.submit.disabled || f0.submit.getAttribute('aria-disabled') === 'true';
      if (hasReqEmpty && !subDisabled)
        add({ issueType: 'submitNotDisabledWhenInvalid', severity: 'medium', selector: sel(f0.submit), bbox: bb(f0.submit), description: 'Submit is enabled while required fields are empty/invalid.', evidence: {} });

      // loading state: fill required, click submit (guarded), check immediate visual state
      for (const el of f0.fields) { if (!isReq(el) || el.value) continue; if (el.type === 'checkbox' || el.type === 'radio') el.checked = true; else if (el.type === 'email') setNative(el, 'argus@example.com'); else if (el.type === 'tel') setNative(el, '5551234567'); else if (el.type === 'url') setNative(el, 'https://example.com'); else if (el.type === 'number') setNative(el, '1'); else setNative(el, 'argus'); }
      if (!subDisabled) {
        f0.submit.click(); await sleep(300);
        const loading = f0.submit.disabled || f0.submit.getAttribute('aria-busy') === 'true' || !!f0.submit.querySelector('.spinner, .loader, [class*="loading"], svg.animate-spin, [data-loading="true"]') || /loading|please wait|submitting|saving|sending/i.test(f0.submit.innerText);
        if (!loading && !f0.submit.disabled)
          add({ issueType: 'submitNoLoadingState', severity: 'low', selector: sel(f0.submit), bbox: bb(f0.submit), description: 'No loading/disabled state on submit — invites double-submit.', evidence: {} });
      }

      // beforeunload warning on dirty form
      const dirtyInput = f0.fields.find(el => el.type === 'text' || el.type === 'email' || el.tagName === 'TEXTAREA');
      if (dirtyInput) {
        setNative(dirtyInput, 'argusDirty'); blur(dirtyInput);
        let handlerFired = false;
        const probe = e => { if (e.defaultPrevented || (typeof e.returnValue === 'string' && e.returnValue !== '')) handlerFired = true; };
        window.removeEventListener('beforeunload', null);
        window.onbeforeunload = _bu; // temporarily restore app handler so we test the app, not our guard
        window.addEventListener('beforeunload', probe, true);
        const evt = new Event('beforeunload', { cancelable: true });
        window.dispatchEvent(evt);
        window.removeEventListener('beforeunload', probe, true);
        window.onbeforeunload = e => { e.preventDefault(); return ''; }; // re-arm guard
        if (!(handlerFired || evt.defaultPrevented))
          add({ issueType: 'noBeforeUnloadWarning', severity: 'low', selector: sel(f0.root === document.body ? dirtyInput : f0.root), bbox: bb(dirtyInput), description: 'Dirty form has no beforeunload warning — accidental data loss possible.', evidence: {} });
      }
    }
  } finally {
    // ── MANDATORY CLEANUP ──
    for (const form of allForms) for (const el of form.fields) { try { if (el.tagName !== 'SELECT' && el.type !== 'checkbox' && el.type !== 'radio') { setNative(el, ''); } } catch (_) {} }
    restoreGuard();
  }

  return out;
}
```

## MCP steps (Phase 4 + Phase 5 — network/navigation-dependent, stay hand-driven)

These genuinely need real network responses or real navigation, which a guarded in-page probe cannot produce. Run them AFTER the probe (skip Phase 4 if the page has no form with a submit button, or `customize.toml [form] enable_phase4 = false`, or the probe emitted `pageCrashOnLargeInput`).

- **`doubleSubmitAllowed`** — fill required validly, install a fetch/XHR counter, `browser_click` submit twice within 100ms, wait 1000ms; if counter ≥ 2 → emit (high).
- **`backNavLosesFormData`** — fill fields with sentinel `argus_test_42`, `browser_navigate` to root, `browser_navigate` back; if sentinel gone → emit (medium).
- **`noPostRedirectGet`** — fill valid, install a response observer, `browser_click` submit; if response is 200 AND `location.href` unchanged → emit (medium).
- **`serverValidationNotShown`** — submit data the server will reject (e.g. `server-reject@argus.test`); if response has `errors`/422 but DOM shows no `[role=alert]/.error/.invalid-feedback` → emit (high). Skip if server accepts (inconclusive).
- **`noRateLimitOnSubmit`** — `browser_click` submit ×10 in 1s; if all 10 returned 2xx with no 429/503 → emit (low). Only if same-origin POST.

### Phase 5 — Happy-path success (GATED — OFF by default)
🚨 Runs ONLY when `customize.toml [safe_testing] allow_form_submit = true` (it creates a real record). Gate check FIRST; if off → skip, emit nothing, record `happyPath: "skipped (gated off)"`.
When enabled: fill every required+visible field with a VALID value by type (`argus.qa+{runId}@example.com`, `+15555550123`, mid-range number, today's date, first non-placeholder select option, `Argus QA test {runId}`), confirm submit enabled, `browser_click` submit, wait 1500ms.
- success toast / confirmation redirect / form-clears → no finding (`happyPath: "success: {signal}"`).
- no success AND no error → `happySubmitNoFeedback` (high).
- validation error on VALID data → `validRejectedAsInvalid` (high); `uncertain: true` if plausibly a real business rule.
- Cleanup: if `cleanup_after_submit = true` and a delete/undo for the `{runId}` record exists, attempt it; never fail the audit on cleanup.

## Hard rules
1. **NEVER click submit without the guard** — the probe installs a `preventDefault` + fetch/XHR block so submit can't navigate or write. Phase 4/5 MCP steps deliberately remove the guard because they MUST exercise the real network — only run them on a dev/sandbox or behind the gate.
2. **ALWAYS run cleanup** — the probe's `finally` block clears every modified field and restores `fetch`/`XHR`/`onbeforeunload` even on crash.
3. **ALWAYS check page health between special-char payloads** — done inside the probe; a crashing payload aborts the field loop.
4. **NEVER emit a finding without `selector`** — bug-filer can't attach evidence otherwise.

## Issues
The complete issueType allowlist this skill can emit.

| issueType | severity | description |
|---|---|---|
| noValidationOnEmptySubmit | high | Required form submitted empty with no error shown |
| noEmailValidation | medium | Email input accepts invalid format |
| noRealtimeValidation | low | Once-per-form advisory: form has no validation at all (no inline AND no on-submit). On-submit validation is correct and never flagged. |
| whitespaceAccepted | medium | Required field accepts whitespace-only input (no trim) |
| pageCrashOnLargeInput | high | 10K character input crashes the page |
| maxLengthNotEnforced | medium | Field has maxlength but accepts oversize input |
| xssReflection | high | XSS payload reflected unescaped into the DOM |
| crashOnSpecialChars | high | SQL/XSS/Unicode payload crashes or blanks the page |
| boundaryMaxNotEnforced | medium | Number/date field accepts a value over its max |
| boundaryMinNotEnforced | medium | Number/date field accepts a value under its min |
| formatNotEnforced | medium | Field with pattern/known-format accepts a malformed value |
| passwordMismatchNotCaught | high | Mismatched password + confirm shows no error |
| dateRangeNotValidated | medium | End date accepted before start date with no error |
| emailMismatchNotCaught | medium | Email + confirm-email mismatch shows no error |
| doubleSubmitAllowed | high | Rapid double-click on submit fires two requests (duplicate records) |
| submitNotDisabledWhenInvalid | medium | Submit enabled while required fields are empty/invalid |
| submitNoLoadingState | low | No loading/disabled state on submit — invites double-submit |
| noBeforeUnloadWarning | low | Dirty form has no beforeunload warning |
| noErrorSummary | medium | No error summary region for screen-reader users |
| ariaDescribedByBrokenRef | medium | aria-describedby points at a missing id |
| helpTextNotAssociated | low | Help text not programmatically tied to its field |
| pastePreventedOnPassword | medium | Password field blocks paste (breaks password managers) |
| hiddenRequiredBlocksSubmit | high | A hidden required field silently blocks submit |
| untranslatedFormError | medium | Validation error shows a raw i18n key, not translated text |
| serverValidationNotShown | high | Server returned validation errors but UI did not display them |
| noRateLimitOnSubmit | low | 10 rapid submits all accepted — no rate limiting |
| backNavLosesFormData | medium | Form blank after browser back-navigation |
| noPostRedirectGet | medium | Submit 200 without redirect — refresh re-POSTs |
| happySubmitNoFeedback | high | Valid submit gave neither confirmation nor error |
| validRejectedAsInvalid | high | Form rejected legitimate valid input |

## Notes on this conversion
- Phase 1 (passive a11y), Phase 2 (per-field: type-invalid, email, whitespace, oversize, maxlength, XSS/SQL/Unicode injection, boundary, format), Phase 2.5 (cross-field password/date/email) and Phase 3 (submit-state) are now ONE in-page async probe instead of ~50 MCP round-trips. The old separate probes (`passiveScan`, `findTestableForms`, `checkValidationVisible`, `checkInlineFeedback`, `checkFieldLength`, `checkXssReflection`, `checkPageHealth`, `clearAllFields`, `findSubmitContext`, `fillRequiredWithMarkers`, `checkSubmitLoadingState`, `makeFormDirty`, `testBeforeUnloadHandler`, `cleanupSubmitTest`) are inlined.
- **Folded:** the unbounded-number heuristic escalation in old Test 4f (try -1/0/huge with `uncertain`) was dropped from the hot path; boundary checks now fire only on explicit `min`/`max`. All named issueTypes preserved.
- **Kept MCP (`executable: partial`):** Phase 4 (`doubleSubmitAllowed`, `backNavLosesFormData`, `noPostRedirectGet`, `serverValidationNotShown`, `noRateLimitOnSubmit`) and Phase 5 gated happy-path (`happySubmitNoFeedback`, `validRejectedAsInvalid`) — these require real network responses / real navigation that the guarded probe cannot fake.
