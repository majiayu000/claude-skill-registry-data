---
name: csrf
description: >
  Cross-Site Request Forgery (CSRF) tricks authenticated users into submitting forged requests to a target application by exploiting browser automatic cookie attachment. Detect via missing or predictable CSRF tokens in state-changing requests (POST/PUT/DELETE), absent `SameSite` cookie attributes, and JSON endpoints accepting `text/plain` Content-Type. Test using HTML auto-submitting forms, XHR requests, and CORS-enabled fetch. Tools: Burp Suite (Generate CSRF PoC), OWASP ZAP.
license: MIT
compatibility: Designed for Claude Code. Requires Burp Suite or OWASP ZAP, HTML PoC hosting.
metadata:
  category: client-side
  version: "0.1"
  source: https://owasp.org/www-project-web-security-testing-guide/stable/
  source_types: framework
  wstg: WSTG-SESS-05
---

# Cross-Site Request Forgery (CSRF)

## What Is Broken and Why
CSRF exploits the browser's automatic inclusion of credentials (cookies, HTTP Basic auth) with every request to a given origin. An attacker-controlled page on a different origin can cause the victim's browser to send authenticated requests to the target application. Since the browser automatically attaches the session cookie, the server cannot distinguish the forged request from a legitimate one — unless it validates a secret token that only the legitimate page would know. Absent CSRF tokens, `SameSite=Strict/Lax` cookie attributes, or origin validation, any state-changing operation is potentially exploitable.

## Key Signals
- State-changing requests (account settings, password change, fund transfer, email change) without a CSRF token
- CSRF token present but predictable, static, or not validated server-side
- Cookie lacks `SameSite=Strict` or `SameSite=Lax` attribute
- `Content-Type: application/json` endpoints that also accept `text/plain` (allows form-based CSRF)
- API endpoints not verifying `Origin` or `Referer` headers
- WebSocket handshakes without origin validation

## Methodology
1. Identify all state-changing requests (POST, PUT, PATCH, DELETE) in the application.
2. Check for CSRF token in request parameters or headers (`X-CSRF-Token`, `_token`, `csrf_token`).
3. If token is present: test whether it is validated (remove it, use an invalid value, reuse an old token, use another user's token).
4. If no token: confirm the action is exploitable by crafting a PoC HTML page.
5. Check `SameSite` attribute of session cookie; `Lax` provides partial protection (GET only, top-level nav).
6. Test JSON endpoints: try submitting the same payload as `text/plain` or `application/x-www-form-urlencoded`.
7. Test whether `Referer` header is validated and if it can be stripped or spoofed.
8. Use Burp's "Generate CSRF PoC" feature (right-click on request in Proxy history).

## Payloads & Tools
```html
<!-- GET-based CSRF (auto-loads on page visit) -->
<img src="TARGET/action?param=value" style="display:none">
<link rel="stylesheet" href="TARGET/action?param=value">

<!-- POST-based CSRF (auto-submitting form) -->
<html>
<body onload="document.forms[0].submit()">
<form action="TARGET/change-email" method="POST">
  <input type="hidden" name="email" value="attacker@controlled.com">
</form>
</body>
</html>

<!-- POST-based with multiple fields -->
<form action="TARGET/transfer" method="POST" id="csrfForm">
  <input type="hidden" name="amount" value="1000">
  <input type="hidden" name="destination" value="ATTACKER-ACCOUNT">
  <input type="hidden" name="currency" value="USD">
</form>
<script>document.getElementById('csrfForm').submit();</script>

<!-- JSON CSRF via text/plain Content-Type -->
<form action="TARGET/api/update" method="POST" enctype="text/plain">
  <input name='{"email":"attacker@controlled.com","x":"' value='"}'>
</form>
<!-- Results in body: {"email":"attacker@controlled.com","x":"="} -->

<!-- CSRF token bypass — test without token -->
POST /change-password HTTP/1.1
Host: TARGET
Cookie: session=TOKEN

new_password=attacker123

<!-- CSRF token bypass — use invalid token -->
POST /change-password HTTP/1.1
csrf_token=AAAAAAAAAAAAAAAA

<!-- CSRF via XHR (requires CORS misconfiguration) -->
<script>
var xhr = new XMLHttpRequest();
xhr.open('POST', 'TARGET/change-email', true);
xhr.withCredentials = true;
xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
xhr.send('email=attacker@controlled.com');
</script>

<!-- Burp Suite — Generate CSRF PoC -->
<!-- Right-click on request in Proxy -> Engagement tools -> Generate CSRF PoC -->
```

## Bypass Techniques
- Remove CSRF token entirely (some servers skip validation when token is absent)
- Submit empty/null CSRF token value
- Reuse a valid token from another session (if tokens are not per-user)
- Use attacker's own valid CSRF token for victim's request (if not tied to session)
- Strip Referer header via `<meta name="referrer" content="no-referrer">` or HTTPS → HTTP downgrade
- For `SameSite=Lax`: exploit GET-based state changes; or use top-level navigation (window.open)
- JSON endpoint: attempt `Content-Type: text/plain` with JSON body shaped as `name=value` form data
- Subdomain takeover → subdomain can set/read parent domain cookies (bypasses SameSite in some configs)
- Flash-based CSRF (legacy): Flash objects bypass SameSite for cross-origin requests in old browsers

## Exploitation Scenarios
**Scenario 1 — Account Email Takeover**
Setup: `/account/change-email` accepts POST with `email` parameter; no CSRF token; session cookie lacks SameSite.
Trigger: Victim visits attacker page containing auto-submitting form POSTing to the email change endpoint.
Impact: Victim's email changed to attacker's address; attacker uses "forgot password" to gain full account control.

**Scenario 2 — Fund Transfer via JSON Endpoint**
Setup: Banking app's transfer API accepts JSON but does not enforce `Content-Type` (accepts `text/plain`).
Trigger: Attacker hosts page with form using `enctype="text/plain"` where input name contains valid JSON prefix.
Impact: Victim unknowingly authorizes fund transfer; attacker receives funds.

**Scenario 3 — Admin Action via GET Request**
Setup: Admin panel uses GET requests for user deletion: `/admin/delete-user?id=123`; no CSRF protection.
Trigger: Attacker embeds `<img src="TARGET/admin/delete-user?id=456">` on a page the admin visits.
Impact: Target user account deleted when admin loads attacker's page.

## False Positives
- CSRF token present and properly validated server-side (even if not obvious from request format)
- `SameSite=Strict` cookie attribute preventing cross-site requests in all modern browsers
- Application accepting requests only with `Content-Type: application/json` (form-based CSRF blocked)
- `Origin` or `Referer` header properly validated server-side before processing
- Read-only GET endpoints that appear to change state but actually do not persist changes

## Fix Patterns
- Implement synchronizer token pattern: per-session or per-request CSRF tokens in hidden form fields and custom headers
- Use `SameSite=Strict` for session cookies; `SameSite=Lax` provides partial protection for top-level navigation
- Validate `Origin` and `Referer` headers for state-changing requests; reject mismatches
- Double-submit cookie pattern: send token in cookie and request body; verify they match
- For APIs: require `Content-Type: application/json` and reject `text/plain`; verify with CORS policy
- Use custom request headers (e.g., `X-Requested-With`) which cannot be set by simple cross-origin forms
- Framework built-in CSRF protection: Django `{% csrf_token %}`, Laravel `@csrf`, Rails `authenticity_token`

## Related Skills

[[cors-misconfig]] enables reading CSRF tokens cross-origin, completely undermining the synchronizer token pattern — check CORS before concluding CSRF is mitigated. [[xss-stored]] or [[xss-reflected]] on the same origin bypasses SameSite cookies and can directly forge CSRF-protected requests since the script runs in the target origin. [[clickjacking]] is a user-tricked CSRF variant where the victim is manipulated into clicking a hidden button rather than being silently redirected. CSRF on a login form can be used to plant a known session and enable [[session-fixation]].
