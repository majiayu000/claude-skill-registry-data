---
name: auth-bypass
description: >
  Bypass authentication via forced browsing to protected URLs, parameter tampering
  (authenticated=yes, debug=true, fromtrustIP=true), session ID prediction from linear/incremental
  cookies, SQL injection on login forms, PHP unserialize() boolean type juggling (b:1 payload),
  and credential transport over HTTP. Detectable with Burp Suite, OWASP ZAP, WebGoat.
license: MIT
compatibility: Designed for Claude Code. Requires Burp Suite or OWASP ZAP.
metadata:
  category: web
  version: "0.1"
  source: https://owasp.org/www-project-web-security-testing-guide/stable/
  source_types: framework
  wstg: WSTG-ATHN-01, WSTG-ATHN-04, WSTG-ATHN-05, WSTG-ATHN-06
---

# Authentication Bypass

## What Is Broken and Why

Authentication logic applied only at the login page leaves all downstream pages unprotected.
Applications relying on client-supplied flags (`authenticated`, `role`, `admin`) to gate access
allow trivial bypass by modifying those values. Predictable session tokens enable forging.
Insecure deserialization in cookie handling allows boolean type juggling to short-circuit
credential verification. Credentials transmitted over HTTP expose them to passive interception.
Browser caching of authenticated responses allows offline credential harvesting from shared machines.

## Key Signals

- Login redirect but direct URL access to `/dashboard`, `/admin`, `/profile` returns 200
- Parameters like `authenticated=`, `isAdmin=`, `role=`, `debug=`, `fromtrustIP=` in GET/POST/cookies
- Session cookies with sequential, time-based, or partially-static values
- Login form accepting `' OR '1'='1` or similar SQL payloads
- Application serializes auth state into cookies (`a:2:{s:11:"autologinid";...}`)
- Login or registration form submitting over `http://` instead of `https://`
- Absence of `Secure` flag on session cookies
- No `Cache-Control: no-store` on pages containing sensitive data
- `Set-Cookie` not issuing new token after successful authentication (session fixation overlap)

## Methodology

1. **Map all authenticated endpoints**: Spider application; note every URL requiring login.
2. **Forced browsing**: Without authenticating, request each protected URL directly. Record any
   that return 200 or partial content.
3. **Parameter tampering**: Intercept login and post-login requests; add or modify boolean
   parameters (`authenticated=yes`, `admin=true`, `debug=true`, `fromtrustIP=true`).
4. **Cookie manipulation**: Decode cookies (base64, URL, serialization); identify role/auth fields;
   modify and re-submit.
5. **Session prediction**: Collect 50+ session tokens under identical conditions; analyze for
   patterns (incrementing integers, timestamp encoding, partial static prefix).
6. **SQL injection on login**: Attempt classic payloads in username/password fields.
7. **Deserialization probe**: If PHP serialized format detected in cookie, craft boolean bypass.
8. **Transport test**: Replace `https://` with `http://` for login, registration, and password
   flows; observe if credentials submit over plain HTTP.
9. **Cache test**: Log in, log out, press Back; reload authenticated pages; check local cache files.

## Payloads & Tools

```bash
# Forced browsing — direct access to protected page
curl -s http://TARGET/admin/dashboard -o /dev/null -w "%{http_code}"

# Parameter tampering via GET
curl "http://TARGET/home?authenticated=yes&admin=true"

# SQL injection on login form
# Username field: ' OR '1'='1'--
# Password field: anything
curl -X POST http://TARGET/login \
  -d "user=' OR '1'='1'--&pass=x"

# PHP unserialize boolean bypass cookie
# Original: a:2:{s:11:"autologinid";s:32:"<hash>";s:6:"userid";s:1:"2";}
# Bypass:   a:2:{s:11:"autologinid";b:1;s:6:"userid";s:1:"2";}
# Encode to base64 and set as cookie value
python3 -c "
import base64
payload = b'a:2:{s:11:\"autologinid\";b:1;s:6:\"userid\";s:1:\"2\";}'
print(base64.b64encode(payload).decode())
"

# Check if login submits over HTTP
curl -v -X POST http://TARGET/login \
  -d "user=admin&pass=PASSWORD" 2>&1 | grep -E "< HTTP|Location:|Set-Cookie"

# Verify Secure flag on session cookie
curl -I https://TARGET/login | grep -i "set-cookie"

# Check cache headers on sensitive pages
curl -I https://TARGET/account/profile | grep -iE "cache-control|pragma|expires"
```

## Bypass Techniques

- If login page redirects to HTTPS but form action is still HTTP, credentials are transmitted
  unencrypted.
- `Cache-Control: private` does NOT prevent local browser caching; only `no-store` does.
- Applications that check `$_GET['authenticated']` but not `$_POST['authenticated']` may be
  bypassed by moving the parameter to the query string.
- PHP type juggling: `"0e123" == "0e456"` evaluates true; password hash comparison bypasses
  possible if hash begins with `0e`.
- Encoded/encrypted cookie values containing auth state may still be decodable if using weak
  schemes (XOR, base64-only, ECB mode).

## Exploitation Scenarios

**Scenario 1 — Forced Browse to Admin Panel**
Setup: Application checks auth only at `/login`; `/admin/` has no server-side session check.
Trigger: Unauthenticated GET to `http://TARGET/admin/users`.
Impact: Full administrative interface accessible without credentials.

**Scenario 2 — PHP Unserialize Boolean Bypass**
Setup: Application stores serialized PHP array in cookie for "remember me" functionality.
Trigger: Replace password hash field with `b:1` (boolean true); server evaluates `true == hash`
as true due to loose comparison.
Impact: Login as any known user ID without knowing their password.

**Scenario 3 — Credential Interception via HTTP**
Setup: Login page loads over HTTPS but form POSTs to `http://TARGET/authenticate`.
Trigger: Passive network capture on shared network (coffee shop, corporate proxy).
Impact: Plaintext username and password captured; full account takeover.

## False Positives

- A 200 response on a forced browse may be the login redirect rendered client-side (SPA),
  not actual unauthorized access to data.
- Debug parameters present in requests may be logged but not processed by server; verify
  actual behavior change, not just parameter acceptance.
- Sequential-looking session IDs may include a cryptographic HMAC suffix that prevents forging.

## Fix Patterns

- Enforce server-side session validation on every protected route, not just at login.
- Never trust client-supplied authentication state flags; derive auth state from server session.
- Use cryptographically random session IDs (256-bit entropy, minimum 50 characters).
- Set `Secure` and `HttpOnly` flags on all session cookies.
- Redirect all HTTP traffic to HTTPS; deploy HSTS.
- Use strict PHP comparison (`===`) to prevent type juggling in authentication checks.
- Set `Cache-Control: no-cache, no-store` and `Pragma: no-cache` on all authenticated responses.

## Related Skills

[[default-credentials]] is the first thing to try once a login form is found — auth bypass and default creds are two paths to the same goal. [[password-reset-flaws]] represents another common bypass vector: a weak reset flow can grant access without ever attacking the login form directly. If a SQL injectable login is found, [[sql-injection]] contains the full methodology for exploiting it. When a session cookie is obtained, validate its security posture using [[cookie-attacks]].
