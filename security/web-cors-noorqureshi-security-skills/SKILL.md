---
name: web-cors
description: >
  Exploit CORS misconfiguration to read cross-origin responses (data theft). Load when an API
  reflects Origin into Access-Control-Allow-Origin, allows credentials cross-origin, or trusts
  null/subdomains. Signals: ACAO reflects your Origin, ACAC: true, `Origin`-dependent responses.
domain: web
type: technique
stability: learning
modes: [bugbounty]
severity: medium
owasp: [A05:2021-Security-Misconfiguration]
cwe: [CWE-942]
tools: [curl, burp]
schema_version: 1
---

# CORS misconfiguration

## When it applies
An endpoint returns sensitive data and sets CORS headers that let an attacker origin read the
response with the victim's credentials.

## Why it works
CORS lets a server opt-in to cross-origin reads. If it reflects the request `Origin` into
`Access-Control-Allow-Origin` *and* sets `Access-Control-Allow-Credentials: true`, any site can
make the victim's browser send an authenticated request and read the response — cross-origin data theft.

## Method
1. **Probe**: send requests with `Origin: https://evil.com` and inspect response headers.
   Vulnerable if ACAO echoes your origin (or `null`) AND ACAC is `true`.
2. **Test weak allowlists**: `Origin: https://evil.com` vs `https://sub.target.com.evil.com`,
   `https://targetevil.com`, `null` (via sandboxed iframe), and non-TLS variants — many regexes are sloppy.
3. **Exploit**: host JS on your origin that `fetch(url, {credentials:'include'})` the sensitive
   endpoint and exfils the response to you; load it as the victim.

## Gotchas
- `ACAO: *` **without** credentials can't read authed data — only origin-reflection + `ACAC:true` (or a same-site secret) is impactful.
- `null` origin is reachable from sandboxed iframes/data: URLs — a real bypass, not theoretical.
- Prove it reads *sensitive* data (tokens, PII); reflecting on a public endpoint is informational.

## Verify success
Your attacker-origin page reads a victim-authenticated response it should not be able to (e.g.
the victim's API key/PII exfiltrated to your server).

## References
PortSwigger CORS labs; OWASP CORS guidance.
