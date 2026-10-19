---
name: web-ssrf
description: >
  Discover and escalate Server-Side Request Forgery. Load when the app fetches a URL you
  influence: webhooks, "import from URL", link/image preview, PDF/HTML render, avatar-by-URL,
  URL health-checks, XML/SVG parsers. Signals: params like url=, uri=, dest=, callback=,
  image=, feed=, or a request that reaches out on your behalf.
domain: web
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: high
owasp: [A10:2021-SSRF]
cwe: [CWE-918]
tools: [burp, collaborator, interactsh]
schema_version: 1
---

# Server-Side Request Forgery (SSRF)

## When it applies
The server makes an outbound request to a destination you control or influence. Even a
"blind" fetch (no response shown) is useful if you can see the callback and reach internal
services.

## Why it works
The request originates from inside the trust boundary, so it bypasses network ACLs and hits
things you can't reach directly: cloud metadata, internal admin panels, databases, other
microservices — often unauthenticated because they "only accept internal traffic".

## Method
1. **Confirm** with an out-of-band beacon: point the param at your `interactsh`/Collaborator
   host and watch for the DNS/HTTP hit. DNS-only hit = blind SSRF (still valuable).
2. **Map internal reach**: try `http://127.0.0.1:<port>/`, `http://localhost`, and the
   cloud metadata IP `169.254.169.254`. Fuzz ports to find live internal services.
3. **Escalate by target**:
   - **Cloud metadata** → steal IAM creds (see `cloud-imds-ssrf`).
   - **Internal line-protocol service** (Redis/6379, memcached) → RCE via `gopher://`
     (see `web-ssrf-gopher-redis-rce`).
   - **Internal HTTP admin** → hit unauthenticated actions.
4. **Bypass filters** blocking `localhost`/private IPs: decimal/octal/hex IPs
   (`http://2130706433/`), `[::]`, `127.0.0.1.nip.io`, DNS-rebinding, `@`-tricks
   (`http://expected.com@attacker.com`), and redirect chains (allowed host 302s to internal).

## Gotchas
- Allowlist on scheme/host is often only on the *first* request — a 30x redirect slips past.
- SSRF via SVG/`<image>`/PDF renderers and via `Location`/webhook retries is easy to miss.
- No response body ≠ no vuln: timing and OOB confirm blind SSRF.

## Verify success
OOB callback from the target's egress IP, or a response revealing an internal-only resource
(metadata JSON, an internal 200/redirect you shouldn't reach).

## References
PortSwigger SSRF labs; Orange Tsai "A New Era of SSRF".
