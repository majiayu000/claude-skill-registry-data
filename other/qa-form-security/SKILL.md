---
name: qa-form-security
section: interactive
description: "Consolidated form security skill. Owns CSRF tokens, autocomplete attributes on sensitive fields, and captcha presence/visibility. Replaces 3 overlapping security skills."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
interactive: false
cacheVersion: "1.0.0"
ownership: "exclusive: any form security finding (CSRF, autocomplete, captcha) belongs to this skill"
replaces:
  - qa-detect-form-csrf
  - qa-detect-form-autocomplete
  - qa-detect-form-captcha
requires: [hasPasswordField, hasLoginForm]
---

# qa-form-security — Consolidated Form Security Skill

Single skill owning ALL form-security findings. Pure passive detection — no interaction. Single `browser_evaluate` round-trip per cell.

## What it checks (10 issue types — gap-fix 2026-06-03)

### CSRF
| issueType | severity | catches |
|---|---|---|
| `csrfTokenMissing` | high | POST form with no CSRF token (no hidden input, no data attr, no meta tag) |
| `csrfTokenNotRotated` | medium | After successful submit, the CSRF token is unchanged — stale-token replay is possible (Phase 2: interactive) |

### Autocomplete
| issueType | severity | catches |
|---|---|---|
| `autocompleteMissingEmail` | medium | Email field missing `autocomplete="email"` or `"username"` |
| `autocompleteWrongPassword` | medium | Password field wrong autocomplete (should be `current-password` or `new-password`) |
| `autocompleteMissingName` | low | Name field missing `autocomplete="given-name"` / `"family-name"` |
| `autocompleteMissingTel` | low | Phone field missing `autocomplete="tel"` |
| `autocompleteOffAntiPattern` | low | `autocomplete="off"` on credential field — browsers ignore it |

### Captcha
| issueType | severity | catches |
|---|---|---|
| `captchaMissingOnSignup` | medium | Signup/register form has no captcha widget |
| `captchaMissingOnContact` | low | Contact form has no captcha — spam target |
| `captchaContainerHidden` | high | Captcha widget present but its container is hidden — users can't solve it |

## Self-skip
Return `[]` ONLY if the page has **no testable inputs** (`input`/`textarea`, excluding hidden/submit/button) AND no captcha widgets. **Do NOT skip on a missing `<form>`** — the autocomplete checks scan all inputs and the captcha check is page-level, so they run on form-less login/signup groups too. (CSRF detection still applies only to real `<form method=post>` — a form-less group submits via fetch, where the CSRF token would be an HTTP header that isn't visible in the DOM, so CSRF can't be judged there.)

## Phase 2 — Interactive CSRF rotation test (NEW, added 2026-06-03)

Phase 2 runs AFTER the passive probe completes IF:
- A CSRF token was detected (hidden input named `csrf_token`, `_csrf`, `authenticity_token`, OR meta tag).
- The page has a submittable form with valid-looking fields.
- `customize.toml → [form] enable_csrf_rotation_test = true` (default: true).

**Algorithm:**

1. Capture the current CSRF token via `browser_evaluate`:
   ```js
   () => {
     const hidden = document.querySelector('input[type="hidden"][name*="csrf" i], input[type="hidden"][name*="_token" i], input[type="hidden"][name="authenticity_token"]');
     const meta   = document.querySelector('meta[name*="csrf" i]');
     return {
       hidden: hidden ? hidden.value : null,
       meta:   meta   ? meta.getAttribute('content') : null
     };
   }
   ```
   Save as `token_before = { hidden, meta }`.

2. Fill the form with safe valid values and submit (reuse the submit-state Phase from qa-form-validation if available).

3. `browser_wait_for(time = 2000)` to let the server response settle.

4. Re-capture the token via the same probe → `token_after`.

5. Compare:
   - If `token_before.hidden === token_after.hidden` AND both are non-empty → emit:
     ```json
     {
       "issueType": "csrfTokenNotRotated", "severity": "medium",
       "selector": "input[type='hidden'][name*='csrf']",
       "description": "CSRF token (hidden input) is unchanged after submit. Stale token can be replayed in a CSRF attack. Rotate the token on every state-changing request."
     }
     ```
   - Same check for meta tag.
   - If both tokens changed → no finding (good).
   - If token went to null after submit (e.g. page redirected, form disappeared) → no finding (inconclusive).

**Skip Phase 2 if:**
- Passive probe found `csrfTokenMissing` (no point testing rotation of a missing token).
- Form submission would trigger destructive action (heuristic: form action contains `/delete`, `/destroy`, `/cancel-account`, or method is DELETE). In that case skip with a logged note.

## Probe (browser_evaluate)
```js
() => {
  const sel = el => (el.tagName.toLowerCase() + (el.id ? `#${el.id}` : '')).slice(0, 120);
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };
  const formSel = f => f.id ? `#${f.id}` : (f.action ? `form[action="${f.action.slice(0,80)}"]` : `form:nth-of-type(${[...document.querySelectorAll('form')].indexOf(f)+1})`);
  const out = [];

  // ============ 1. CSRF ============
  const metaCsrf = document.querySelector('meta[name*="csrf" i], meta[name="_token"], meta[name*="xsrf" i]');
  const hasGlobalCsrf = !!metaCsrf && metaCsrf.getAttribute('content');

  for (const f of document.querySelectorAll('form')) {
    if (out.length >= 8) break;
    const method = (f.method || 'get').toLowerCase();
    if (method === 'get' || method === '') continue;
    const r = f.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;
    const csrfField = f.querySelector(
      'input[type="hidden"][name*="csrf" i], input[type="hidden"][name="_token"], ' +
      'input[type="hidden"][name="authenticity_token"], input[type="hidden"][name*="xsrf" i]'
    );
    const hasFieldCsrf = !!csrfField && csrfField.value && csrfField.value.length >= 8;
    const dataCsrf = f.dataset && (f.dataset.csrf || f.dataset.csrfToken || f.dataset.token);
    const hasDataCsrf = !!dataCsrf && dataCsrf.length >= 8;
    if (!hasFieldCsrf && !hasDataCsrf && !hasGlobalCsrf) {
      out.push({ issueType: 'csrfTokenMissing', severity: 'high', selector: formSel(f),
        description: `POST form ${formSel(f)} action=${f.action || '(empty)'} has no CSRF token — vulnerable to cross-site request forgery`,
        bbox: bb(f) });
    }
  }

  // ============ 2. AUTOCOMPLETE ============
  const passwordFields = [...document.querySelectorAll('input[type="password"]')];
  const formContext = (document.body && document.body.innerText || '').toLowerCase();
  const isSignup = passwordFields.length >= 2 ||
                    (/sign\s*up|create\s*account|register/.test(formContext) && !/sign\s*in|log\s*in/.test(formContext));

  const inpSel = el => (el.id ? `#${el.id}` : `input[name="${el.name}"]`).slice(0,120);

  for (const input of document.querySelectorAll('input, textarea')) {
    if (out.length >= 20) break;
    const r = input.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    if (input.type === 'hidden' || input.type === 'submit' || input.type === 'button') continue;
    const auto = (input.getAttribute('autocomplete') || '').trim().toLowerCase();
    const type = input.type;
    const name = (input.name || input.id || '').toLowerCase();

    if (type === 'email' || /email/.test(name)) {
      if (!auto || (auto !== 'email' && auto !== 'username')) {
        out.push({ issueType: 'autocompleteMissingEmail', severity: 'medium', selector: inpSel(input),
          description: `Email input has autocomplete="${auto || 'none'}" — should be "email" or "username"`, bbox: bb(input) });
        continue;
      }
    }
    if (type === 'password') {
      const expected = isSignup ? 'new-password' : 'current-password';
      if (auto !== expected) {
        out.push({ issueType: 'autocompleteWrongPassword', severity: 'medium', selector: inpSel(input),
          description: `Password input has autocomplete="${auto || 'none'}" — should be "${expected}" for ${isSignup ? 'signup' : 'login'} flow`, bbox: bb(input) });
      }
      continue;
    }
    if (/first.?name|given.?name|fname/.test(name)) {
      if (auto !== 'given-name' && auto !== 'name') {
        out.push({ issueType: 'autocompleteMissingName', severity: 'low', selector: inpSel(input),
          description: `First name field missing autocomplete="given-name"`, bbox: bb(input) });
      }
      continue;
    }
    if (/last.?name|family.?name|surname|lname/.test(name)) {
      if (auto !== 'family-name') {
        out.push({ issueType: 'autocompleteMissingName', severity: 'low', selector: inpSel(input),
          description: `Last name field missing autocomplete="family-name"`, bbox: bb(input) });
      }
      continue;
    }
    if (type === 'tel' || /phone|mobile|tel/.test(name)) {
      if (auto !== 'tel' && auto !== 'tel-national') {
        out.push({ issueType: 'autocompleteMissingTel', severity: 'low', selector: inpSel(input),
          description: `Phone input missing autocomplete="tel"`, bbox: bb(input) });
      }
      continue;
    }
    if (auto === 'off' && (type === 'email' || type === 'password' || type === 'text')) {
      out.push({ issueType: 'autocompleteOffAntiPattern', severity: 'low', selector: inpSel(input),
        description: `Input uses autocomplete="off" — most browsers ignore this; use specific tokens like new-password instead`,
        bbox: bb(input) });
    }
  }

  // ============ 3. CAPTCHA ============
  const hasRecaptcha = !!document.querySelector('.g-recaptcha, [data-sitekey], iframe[src*="recaptcha"], iframe[title*="reCAPTCHA"]');
  const hasHCaptcha = !!document.querySelector('.h-captcha, [data-hcaptcha-sitekey], iframe[src*="hcaptcha"]');
  const hasTurnstile = !!document.querySelector('.cf-turnstile, iframe[src*="turnstile"]');
  const hasCaptcha = hasRecaptcha || hasHCaptcha || hasTurnstile;
  const bodyText = (document.body && document.body.innerText || '').toLowerCase();
  const looksLikeAuth = /(sign\s*in|log\s*in|sign\s*up|register|create\s*account)/i.test(bodyText) && !!document.querySelector('input[type="password"]');
  const looksLikeContact = /contact\s*us|get\s*in\s*touch|send\s*message/i.test(bodyText) && !!document.querySelector('textarea, input[name*="message" i]');

  if (!hasCaptcha && looksLikeAuth && /(sign\s*up|register|create\s*account)/i.test(bodyText)) {
    out.push({ issueType: 'captchaMissingOnSignup', severity: 'medium', selector: 'form',
      description: 'Signup/register form has no captcha widget — potential bot-account creation vector',
      bbox: { x:0, y:0, w:200, h:80 } });
  }
  if (!hasCaptcha && looksLikeContact) {
    out.push({ issueType: 'captchaMissingOnContact', severity: 'low', selector: 'form',
      description: 'Contact / message form has no captcha widget — likely spam target',
      bbox: { x:0, y:0, w:200, h:80 } });
  }
  for (const c of document.querySelectorAll('.g-recaptcha, .h-captcha, .cf-turnstile')) {
    if (out.length >= 28) break;
    const r = c.getBoundingClientRect();
    const style = getComputedStyle(c);
    if (style.display === 'none' || style.visibility === 'hidden' || (r.width === 0 && r.height === 0)) {
      out.push({ issueType: 'captchaContainerHidden', severity: 'high', selector: sel(c),
        description: `Captcha widget ${sel(c)} present but container hidden (display=${style.display}, w×h=${r.width}×${r.height}) — users can't solve it`,
        bbox: bb(c) });
    }
  }

  return out;
}
```

## Migration
```toml
[detectors]
qa-form-security              = true   # NEW
qa-detect-form-csrf           = false
qa-detect-form-autocomplete   = false
qa-detect-form-captcha        = false
```
