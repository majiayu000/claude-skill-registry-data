---
name: web-host-header
description: >
  Host header injection — abuse a trusted Host/X-Forwarded-Host to poison password-reset links,
  routing, and caches. Load when the app builds absolute URLs from the request host, on
  password-reset flows, or behind a proxy/CDN. Signals: reset emails with links, X-Forwarded-Host
  reflected, virtual hosting, cache in front.
domain: web
type: technique
stability: learning
modes: [bugbounty, pentest]
severity: medium
owasp: [A05:2021-Security-Misconfiguration]
cwe: [CWE-644]
tools: [burp]
schema_version: 1
---

# Host header injection

## When it applies
The server trusts the `Host` (or `X-Forwarded-Host`) header to build absolute URLs, decide
routing, or key a cache. Classic impact: password-reset poisoning (the reset link points at your
domain, so the victim's token comes to you).

## Why it works
Frameworks read the request host to construct links (`https://{host}/reset?token=…`). The host is
attacker-controlled, so if it isn't validated against an allowlist, you control where generated
links point — and where secrets in them land.

## Method
1. **Reset poisoning**: trigger a password reset for a victim; intercept and set `Host:
   attacker.com` (or add `X-Forwarded-Host: attacker.com`). If the emailed link uses your host,
   the victim's click sends their reset token to you → account takeover.
2. **Routing/authz**: try `Host:` of an internal vhost (`admin.internal`) to reach restricted apps
   behind the proxy; test `X-Forwarded-Host`, `X-Forwarded-Server`, `X-Host`, dup Host headers.
3. **Cache poisoning**: if the host is reflected into a cached response, combine with
   `web-cache-poisoning` to serve your host to other users.
4. **Validation bypass**: absolute-URL Host (`Host: attacker.com`), `Host: victim.com:@attacker.com`,
   line-wrapping, and duplicate headers (front-end vs back-end pick different ones).

## Gotchas
- Many stacks now validate Host — confirm the generated link/response actually uses your value.
- `X-Forwarded-Host` often wins even when `Host` is validated — always test it separately.
- Reset poisoning needs the app to email a host-derived link; verify by reading the email/link.

## Verify success
A password-reset (or other) link built with your attacker host, or an internal vhost reached, or
a poisoned cached response served to a clean request.

## References
PortSwigger Host header attacks labs; OWASP host-header injection.
