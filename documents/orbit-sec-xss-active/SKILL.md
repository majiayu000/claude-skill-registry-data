---
name: orbit-sec-xss-active
description: Active XSS probing for a WordPress plugin — sends DOM-based / reflected / stored XSS payloads to every form field, URL parameter, REST endpoint, AJAX action; checks if the payload renders unescaped or is reflected back. Use when the user says "XSS test", "active XSS", "stored XSS", "reflected XSS", "test for cross-site scripting".
---

# 🪐 orbit-sec-xss-active — Active XSS probing

`/orbit-wp-security` is static review. This skill is **active** — sends real payloads, checks responses. Catches what static analysis misses (e.g. dynamic-output paths only triggered at runtime).

---

## Quick start

```bash
WP_TEST_URL=http://localhost:8881 \
PLUGIN_SLUG=my-plugin \
  bash ~/Claude/orbit/scripts/xss-probe.sh
```

Output: `reports/xss-probe-<timestamp>.md`.

---

## What it probes

### 1. Reflected XSS (URL parameters echoed back)
```bash
# Payloads sent to every URL parameter:
?search=<script>alert(1)</script>
?search=<img onerror=alert(1) src=x>
?search=javascript:alert(1)
?search=<svg onload=alert(1)>
?search="><script>alert(1)</script>
```

If the response HTML contains the payload unescaped → reflected XSS.

### 2. Stored XSS (form submission rendered later)
```bash
# Submit to every form field:
field=<script>alert(1)</script>
# Then visit the page where that field renders. Check if payload executes.
```

### 3. DOM-based XSS (JavaScript reads + writes URL hash / params)
Send `?param=<script>...</script>` and inspect via headless browser:
```js
const violations = await page.evaluate(() => {
  // Hook into innerHTML / document.write / location.assign
  return window.__xssViolations || [];
});
```

### 4. SVG-based XSS
SVG can contain JS. Plugins that allow SVG upload then render the SVG inline are vulnerable:
```html
<svg xmlns="http://www.w3.org/2000/svg" onload="alert(1)" />
```

### 5. JSON response XSS
```php
// ❌ JSON header missing — browser may interpret as HTML
echo $json_string;

// ✅
header( 'Content-Type: application/json' );
echo wp_json_encode( $data );
```

### 6. AJAX response XSS
Specifically test AJAX handlers — they often forget escaping because "it's JSON, what could go wrong" — but the result gets rendered into DOM.

---

## Payload library (subset)

```
<script>alert(1)</script>
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
<a href="javascript:alert(1)">click</a>
<iframe srcdoc="<script>alert(1)</script>">
"><script>alert(1)</script>
';alert(1);//
{{constructor.constructor('alert(1)')()}}    (template engines)
```

The full list (200+ payloads, evolves with new browser features) lives in `config/xss-payloads.json` and is fetched from PortSwigger / OWASP cheatsheet on every run.

---

## Output

```markdown
# Active XSS Probe — my-plugin

## URLs probed: 47
## Payloads sent: 320 per URL = 15,040 total

## Findings: 3

### 1. Reflected XSS (CRITICAL)
Endpoint: /wp-admin/admin.php?page=my-plugin&search=...
Payload: `<script>alert(1)</script>`
Response: payload appears unescaped at line 1247 of HTML
Fix: `echo esc_html( $_GET['search'] )`

### 2. Stored XSS (HIGH)
Endpoint: /?form=contact (subject field)
Payload: `<img src=x onerror=alert(1)>`
Where rendered: /wp-admin/admin.php?page=my-plugin-submissions
Fix: `wp_kses( $sub->subject, [] )` or `esc_html()`

### 3. DOM XSS (HIGH)
URL: /?param=<script>alert(1)</script>
Source: assets/js/handler.js:42 — `document.querySelector('.x').innerHTML = location.search`
Fix: use textContent, or sanitise via DOMPurify
```

---

## Pair with

- `/orbit-wp-security` — static source review
- `/orbit-rest-fuzzer` / `/orbit-ajax-fuzzer` — endpoint-specific
- `/orbit-cve-check` — known CVE patterns

---

## Sources & Evergreen References

### Canonical docs
- [OWASP XSS Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html) — defence
- [PortSwigger XSS Lab](https://portswigger.net/web-security/cross-site-scripting) — payload library
- [WP Escaping Functions](https://developer.wordpress.org/apis/security/escaping/) — official WP guidance

### Last reviewed
- 2026-04-29 — payload list is fetched live from OWASP / PortSwigger feeds
