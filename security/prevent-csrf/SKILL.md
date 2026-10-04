---
name: prevent-csrf
description: Use when building any server-side endpoint that performs state-changing operations (POST, PUT, PATCH, DELETE) and is accessible by a browser session.
source: 'OWASP Cross-Site Request Forgery Prevention Cheat Sheet (owasp.org/www-project-cheat-sheets); OWASP Top 10 2021 A01; CWE-352'
tags: [security, owasp, csrf, cross-site-request-forgery, web, developer]
---

# Prevent CSRF

Protect state-changing endpoints from cross-site request forgery using synchronizer tokens, SameSite cookies, or origin verification — ensuring requests originate from your own application.

## Why This Is Best Practice

**Adopted by:** Django, Rails, Laravel, Spring Security, and ASP.NET all include CSRF protection by default. OWASP Top 10 2021 (A01:Broken Access Control) covers CSRF. PCI DSS v4.0 Requirement 6.2.4 requires protection against CSRF. GitHub, Google, and Stripe use SameSite cookies as the primary defense.
**Impact:** CSRF allows attackers to perform unauthorized actions on behalf of authenticated users — fund transfers, email changes, password resets — by tricking them into visiting a malicious page. Twitter, Netflix, and YouTube have all had critical CSRF vulnerabilities. Proper implementation eliminates the entire attack class.
**Why best:** The Synchronizer Token Pattern and SameSite cookies are complementary defenses that cover different attack vectors. Relying on `Referer` header alone fails because it can be stripped by browsers or proxies.

Sources: OWASP CSRF Prevention Cheat Sheet; CWE-352; OWASP Top 10 2021

## Steps

1. **Set `SameSite=Lax` (or `Strict`) on all session cookies** — this is the primary defense for modern browsers. `Lax` blocks CSRF for POST/PUT/DELETE while allowing cross-site GET navigation (e.g., following links). `Strict` blocks all cross-site requests including GET.

   ```http
   Set-Cookie: session=abc123; SameSite=Lax; Secure; HttpOnly; Path=/
   ```

   Use `Strict` when your app is not embedded in other sites. Use `Lax` for general-purpose apps.

2. **Add a Synchronizer CSRF Token for defense-in-depth** — generate a random, unpredictable token per session (or per request for high-security actions), store server-side, validate on every state-changing request.

   ```html
   <!-- Include in every HTML form -->
   <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
   ```

   ```python
   # On submit: verify token matches session
   if request.form['csrf_token'] != session['csrf_token']:
       abort(403)
   ```

3. **For SPAs using JSON APIs** — use the Double Submit Cookie pattern or a custom request header:
   - Set a non-`HttpOnly` cookie with a random value.
   - Read it in JavaScript and send it as a custom header (e.g., `X-CSRF-Token`).
   - Server verifies the header matches the cookie.
   - Cross-origin requests cannot set custom headers without CORS preflight, so origin is implicitly verified.

   ```javascript
   fetch('/api/transfer', {
     method: 'POST',
     headers: { 'X-CSRF-Token': getCookie('csrf') },
     body: JSON.stringify(data)
   });
   ```

4. **Verify `Origin` or `Referer` header as a secondary check** — reject requests where `Origin` doesn't match your site's origin. Do not use this as the sole defense (it can be absent).

   ```python
   allowed_origins = {'https://app.example.com'}
   if request.headers.get('Origin') not in allowed_origins:
       abort(403)
   ```

5. **Apply CSRF protection to all state-changing endpoints** — POST, PUT, PATCH, DELETE, and any GET endpoint that performs side effects. Explicitly exempt read-only GET/HEAD/OPTIONS.

6. **Use framework-provided CSRF middleware** — don't implement from scratch. Django: `CsrfViewMiddleware` (enabled by default). Rails: `protect_from_forgery`. Spring: `CsrfFilter`. Laravel: `VerifyCsrfToken`.

## Rules

- Tokens must be unpredictable (cryptographically random, ≥128 bits), not user IDs or sequential values.
- Per-request tokens (regenerated after each state change) are stronger than per-session tokens — use them for high-value actions (fund transfers, account deletion).
- CORS is not a CSRF defense — it controls what cross-origin JS can *read*, not what it can *send*.

## Common Mistakes

- **Using `SameSite=None` without understanding the implications** — required for embedded iframes or cross-site widgets, but eliminates SameSite CSRF protection.
- **Protecting forms but not AJAX endpoints** — both require CSRF tokens.
- **Storing the CSRF token in `localStorage`** — fine, but XSS can steal it; `HttpOnly` cookies protect session tokens but not CSRF tokens (by design).
