---
name: session-fixation
description: >
  Detect and exploit session fixation (WSTG-SESS-01, WSTG-SESS-03) and session exposure
  (WSTG-SESS-04) by testing whether the server issues a new session token post-authentication,
  whether pre-login tokens remain valid after login, and whether session IDs are transmitted over
  HTTP or included in GET parameters. Analyze token randomness via Burp Sequencer. Test JSESSIONID,
  ASP.NET Forms Auth cookies. Tools: OWASP ZAP, Burp Suite Repeater/Sequencer, JHijack.
license: MIT
compatibility: Designed for Claude Code. Requires Burp Suite or OWASP ZAP.
metadata:
  category: web
  version: "0.1"
  source: https://owasp.org/www-project-web-security-testing-guide/stable/
  source_types: framework
  wstg: WSTG-SESS-01, WSTG-SESS-03, WSTG-SESS-04
---

# Session Fixation and Session Token Exposure

## What Is Broken and Why

Session fixation occurs when an application authenticates a user but retains the pre-authentication
session token rather than issuing a fresh one. An attacker who plants a known token (via URL
parameter, XSS, or network manipulation) can then authenticate as the victim by using that
same token once the victim logs in. Session token exposure extends the attack surface by allowing
tokens to be harvested from HTTP traffic, proxy logs, browser history, and caches when tokens
are transmitted without encryption or appear in GET request URLs. Predictable session tokens
that can be forged complete the trifecta of session management failures.

## Key Signals

- Application does not set a new `Set-Cookie` header upon successful authentication
- Pre-login session token remains usable in authenticated requests post-login
- Session ID appears in URL query string: `?JSESSIONID=...` or `?session=...`
- Session ID transmitted over HTTP (not HTTPS) at any point
- `Set-Cookie` lacks `Secure` flag on session cookies
- `Set-Cookie` lacks `HttpOnly` flag on session cookies
- Session cookies set without `SameSite` attribute
- Session ID predictable: sequential, timestamp-based, or short (< 50 chars / < 128-bit entropy)
- `Cache-Control` headers on authenticated pages do not include `no-store`
- ASP.NET Forms Authentication cookies (`.ASPXAUTH`) used without server-side session store
- `Set-Cookie: __Host-` or `__Secure-` prefixes absent (weaker binding guarantees)

## Methodology

1. **Pre-auth token capture**: Visit the login page without authenticating; record all cookies
   issued (note `Set-Cookie` headers, cookie names, values).
2. **Authentication with token intact**: Submit valid credentials while preserving the pre-login
   cookie; inspect response for `Set-Cookie` headers.
3. **Fixation test**: If no new session cookie issued, the pre-auth token has been elevated to
   an authenticated session — fixation confirmed.
4. **Forced cookie test**: Using two accounts (attacker + victim), perform the 9-step forced
   cookie scenario: snapshot pre-login cookies, authenticate as victim, restore pre-login snapshot,
   attempt authenticated action, then swap and authenticate as attacker using victim's pre-login
   cookies.
5. **Token randomness analysis**: Collect 50+ session tokens under identical conditions within
   a 50ms window; load into Burp Sequencer for statistical analysis.
6. **Transport exposure**: Force HTTP access after authentication; observe if session cookie
   is transmitted. Check for `Secure` flag.
7. **GET parameter exposure**: Review all URLs and server logs for session IDs in query strings.
8. **Cache exposure**: Check `Cache-Control`, `Pragma`, and `Expires` headers on authenticated
   responses.

## Payloads & Tools

```bash
# Step 1: Capture pre-login token
PRE_TOKEN=$(curl -s -c /tmp/pre_cookies.txt "https://TARGET/login" \
  -D - | grep -i "set-cookie" | grep -i "session\|jsession\|sid")
echo "Pre-login token: $PRE_TOKEN"

# Step 2: Authenticate while keeping pre-login token
curl -s -b /tmp/pre_cookies.txt -c /tmp/post_cookies.txt \
  -X POST "https://TARGET/login" \
  -d "username=VICTIM&password=VICTIM_PASS" \
  -D - | grep -i "set-cookie"

# Step 3: Compare pre and post tokens
echo "=== Pre-login cookies ===" && cat /tmp/pre_cookies.txt
echo "=== Post-login cookies ===" && cat /tmp/post_cookies.txt

# Step 4: Test if pre-login token grants authenticated access
curl -s -b "JSESSIONID=PRE_LOGIN_TOKEN_VALUE" \
  "https://TARGET/account/dashboard" -o /dev/null -w "%{http_code}"

# Transport exposure test
curl -v "http://TARGET/account/profile" \
  -b "SessionID=VALID_TOKEN" 2>&1 | grep -iE "set-cookie|location|HTTP/"

# GET parameter session ID test
curl -s "https://TARGET/page;jsessionid=SESSION_ID_VALUE" \
  -D - | grep -i "set-cookie\|200\|302"

# Cache header audit on authenticated page
curl -sI "https://TARGET/account/dashboard" \
  -b "SessionID=VALID_TOKEN" | grep -iE "cache-control|pragma|expires"

# Token entropy collection for Burp Sequencer
# (In Burp: Proxy > HTTP History > select login response > right-click > Send to Sequencer)
# Collect 100+ tokens, run analysis for effective bits of randomness

# ASP.NET Forms Auth cookie decode (check if user ID is embedded)
python3 -c "
import base64, sys
token = 'TOKEN_VALUE_HERE'
try:
    decoded = base64.b64decode(token + '==')
    print(decoded)
except Exception as e:
    print(f'Error: {e}')
"
```

## Bypass Techniques

- If `__Host-` or `__Secure-` prefixed cookies are absent, attacker can potentially set cookies
  via HTTP subdomain or path injection to fix the session.
- Some frameworks issue a new session ID but keep the old one valid ("soft rotation"); the old
  token remains usable, effectively still allowing fixation.
- ASP.NET Forms Authentication without server-side session state allows restoring old auth cookies
  after logout if the machine key is static and the cookie has not expired.
- Session tokens in URL fragments (`#`) are not sent to servers but may leak via `Referer` headers.

## Exploitation Scenarios

**Scenario 1 — Classic Session Fixation**
Setup: Application issues session token on first visit; does not rotate after login.
Trigger: Attacker tricks victim into visiting `https://TARGET/login?sessionid=KNOWN_VALUE`
(if app accepts session via URL); victim logs in; attacker uses same `KNOWN_VALUE` to access
victim's authenticated session.
Impact: Full account takeover without knowing victim's credentials.

**Scenario 2 — Network Attacker Cookie Forcing**
Setup: Application accepts cookies over HTTP for legacy endpoints; no `__Host-` prefix protections.
Trigger: Attacker on same network injects a known session cookie via HTTP response manipulation;
victim authenticates; attacker uses planted cookie to access authenticated session.
Impact: Session hijacking of any user on the same network segment.

**Scenario 3 — ASP.NET Cookie Restoration After Logout**
Setup: Application uses encrypted Forms Authentication cookie without server-side session store;
machine key is static.
Trigger: Post-logout, attacker restores captured `.ASPXAUTH` cookie (still cryptographically
valid, only blacklisted client-side); sends it to authenticated-only endpoint.
Impact: Session restoration after logout; authentication state bypass.

## False Positives

- A new `Set-Cookie` with the same value as the pre-login token may be a refresh/expiry update,
  not a true rotation; only a different value confirms proper rotation.
- `Cache-Control: private` appears protective but still allows browser-local caching; only
  `no-store` prevents all local caching.
- Session IDs that look short in display may be Base64-encoded 256-bit values; decode before
  judging entropy.

## Fix Patterns

- Invalidate the existing session and issue a new session ID immediately upon successful
  authentication (`session_regenerate_id(true)` in PHP; `Session.Abandon()` + new session in ASP.NET).
- Set `Secure`, `HttpOnly`, and `SameSite=Strict` (or `Lax`) on all session cookies.
- Use `__Host-` prefix for session cookies to enforce secure origin, host-only scope, and `Path=/`.
- Never transmit session IDs in URLs or GET parameters.
- Enforce `Cache-Control: no-cache, no-store` and `Pragma: no-cache` on all authenticated responses.
- Use server-side session stores; do not rely solely on client-side encrypted tokens for auth state.
- Generate session IDs with 256-bit entropy (AES-based); enforce minimum 50-character length.

## Related Skills

Session fixation and [[cookie-attacks]] are two sides of the same session management problem — fixation exploits the lack of rotation on login, while cookie-attacks exploit weak attributes after the session is established. [[csrf]] can be used to fix a session: if a login form accepts a GET with a `sessionid` parameter, a CSRF payload can force the victim's browser to submit it. Missing `__Host-` or `__Secure-` prefixes (covered in [[cookie-attacks]]) are also prerequisites for session fixation via HTTP subdomain injection.
