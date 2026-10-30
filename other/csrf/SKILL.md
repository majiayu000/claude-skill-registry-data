---
name: csrf
description: Detects forms and state-changing endpoints missing CSRF protection. Use when
  writing HTML forms that submit POST/PUT/DELETE requests, configuring session
  cookies, or setting up CSRF middleware for web applications. Also invoke
  when disabling or bypassing CSRF protections in framework configuration.
---

# Cross-Site Request Forgery Check (A01:2025)

## What this checks

Protects against cross-site request forgery, where an attacker tricks an authenticated
user's browser into submitting a state-changing request the user did not intend.
Exploitation leads to unauthorized fund transfers, account takeover, or privilege
escalation.

## Vulnerable patterns

- HTML form posting a state-changing request with no CSRF token hidden field
- Framework CSRF protection explicitly disabled or exempted on a state-changing endpoint
- Session cookie issued without a `SameSite` attribute (`Lax` or `Strict`)
- Web app with no CSRF middleware registered for cookie-authenticated state-changing routes
- Cookie-authenticated API endpoint accepting POST/PUT/PATCH/DELETE with no token check

## Fix immediately

Flag the vulnerable code and explain the risk. Then suggest a fix that establishes
these properties:

1. **Every state-changing endpoint (POST/PUT/PATCH/DELETE) validates a per-session
   or per-request CSRF token server-side** before any mutation. Use the framework's
   documented CSRF middleware — do not roll your own.
2. **Framework CSRF protection is never disabled or exempted on a state-changing
   route.** If a route legitimately needs to opt out (a pure JSON API authenticated
   by `Authorization: Bearer` headers, not cookies), the opt-out must be explicit
   and the cookie-auth path must remain protected.
3. **Session cookies carry `SameSite=Lax` at minimum, or `SameSite=Strict` for
   sensitive flows**, plus `Secure` and `HttpOnly`. This blocks cross-origin
   cookie attachment on top-level navigations or subrequests that don't need it.
4. **CSRF tokens are not exposed in URLs, logs, or `Referer` headers** — they live
   in a hidden form field or a dedicated request header, never in the query string.
5. **Forms include the token via the framework's template helper**, so the token
   binds to the session and is rotated as the framework intends.

Translate these principles to the audited file's language and framework. Use the
documented CSRF middleware and template helpers for that stack — do not hand-build
token comparison logic.

## Verification

Confirm the following properties hold (language-agnostic):

- [ ] Every state-changing endpoint (POST/PUT/PATCH/DELETE) is protected by a CSRF token validated server-side
- [ ] No framework CSRF middleware is disabled or bypassed on a cookie-authenticated state-changing route
- [ ] Session cookies include `SameSite=Lax` or `SameSite=Strict` attribute
- [ ] CSRF tokens are not leaked in URLs, logs, or Referer headers
- [ ] API-only endpoints using token-based auth (Bearer header) may skip CSRF tokens, but cookie-authenticated endpoints must not

## References

- CWE-352 ([Cross-Site Request Forgery](https://cwe.mitre.org/data/definitions/352.html))
- [OWASP A01:2025 Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
