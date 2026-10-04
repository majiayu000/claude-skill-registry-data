---
name: orbit-uat-forms
description: UAT template + Playwright spec scaffolds for form plugins (Contact Form 7, WPForms, Gravity Forms, Forminator, Fluent Forms, etc.) — form rendering, field validation (client + server), submission flow, success / error notifications, anti-spam, file upload, multi-step, conditional logic, GDPR consent. Use when the user says "form plugin UAT", "test form submission", "spam protection test".
---

# 🪐 orbit-uat-forms — Form plugin UAT

Forms break in subtle ways. Empty submissions, server-side validation gaps, broken success messages, missing anti-spam. This UAT covers them all.

---

## Quick start

```bash
PLUGIN_SLUG=my-forms-plugin npx playwright test --project=uat-forms
```

---

## What the UAT covers

### 1. Form renders without JS errors
```js
const errors = [];
page.on('console', msg => msg.type() === 'error' && errors.push(msg.text()));
await page.goto('/contact/');
await expect(page.locator('form.my-plugin-form')).toBeVisible();
expect(errors).toHaveLength(0);
```

### 2. Field validation — client + server
**Whitepaper intent:** Client-only validation is bypassed by curl. Every required field must validate on the server too. Test both:

```js
// Client validation
await page.click('button[type=submit]');  // submit empty
await expect(page.locator('.error-required')).toBeVisible();

// Server-side: bypass JS, send curl-style POST
const response = await page.request.post('/?form=contact', { form: { name: '' } });
expect(response.status()).toBe(400);
```

### 3. Successful submission
```js
await page.fill('[name=name]', 'Test User');
await page.fill('[name=email]', 'test@example.com');
await page.fill('[name=message]', 'Hello');
await page.click('button[type=submit]');
await expect(page.getByText(/thank you|success/i)).toBeVisible();
```

### 4. Anti-spam (honeypot / CAPTCHA / nonce)
- Honeypot field hidden but present
- CAPTCHA blocks bots (test via missing token)
- Nonce verified server-side

### 5. File upload
```js
await page.setInputFiles('[type=file]', 'tests/fixtures/test.pdf');
await page.click('Submit');
// Verify file uploaded to expected directory + sanitized filename
```

### 6. Multi-step / conditional logic
```js
// Multi-step
await page.click('Next Step');
await expect(page.locator('.step-2')).toBeVisible();

// Conditional: show/hide based on previous answer
await page.selectOption('[name=type]', 'business');
await expect(page.locator('[name=company_name]')).toBeVisible();
```

### 7. Email delivery
```js
// Use a fake-email-server like MailHog or wpmail-debug to verify
await page.goto('/wp-admin/tools.php?page=wp-mail-log');
await expect(page.getByText(/test@example.com/)).toBeVisible();
```

### 8. GDPR consent checkbox
- Required checkbox must block submission if unchecked
- Consent state stored with submission

### 9. Submission storage / DB
After success, verify the row landed in the plugin's submissions table or wherever it stores them.

---

## Output

```markdown
# Form UAT — my-forms-plugin

## 18 tests, 16 passed, 2 failed

❌ "Server-side validation" — empty form returns 200 (should be 400)
   → handler.php validates only on JS, missing PHP-side empty check

❌ "GDPR checkbox required" — submission succeeds with checkbox unchecked
   → Required attribute on checkbox in HTML, but not enforced in PHP

✓ Honeypot — passes (bot-style submissions rejected)
✓ Success message — passes
```

---

## Pair with

- `/orbit-wp-security` — XSS in form output, SQLi in submission storage
- `/orbit-rest-fuzzer` — REST endpoint fuzzing
- `/orbit-ajax-fuzzer` — admin-ajax fuzzing
- `/orbit-gdpr` — consent + data export coverage
- `/orbit-accessibility` — form labels + error association

---

## Sources & Evergreen References

### Canonical docs
- [WP Plugin Handbook — Forms](https://developer.wordpress.org/plugins/security/securing-input/) — input sanitization
- [Honeypot patterns](https://medium.com/@uxoasis/honeypots-arent-broken-46e4ce53f1e2) — anti-spam research
- [reCAPTCHA v3](https://developers.google.com/recaptcha/docs/v3) — score-based
- [hCaptcha](https://docs.hcaptcha.com/) — privacy-friendly alt
- [WCAG Forms](https://www.w3.org/WAI/tutorials/forms/) — a11y patterns

### Rule lineage
- Honeypot pattern — long-standing, still effective for non-AI bots
- reCAPTCHA v3 — Google released 2018, score-based; v4 in beta as of 2026

### Last reviewed
- 2026-04-29 — re-review on reCAPTCHA / hCaptcha API changes
