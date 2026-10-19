---
name: web-request-smuggling
description: >
  HTTP request smuggling (CL.TE/TE.CL/TE.TE/CL.0) — desync front-end and back-end to poison
  other users' requests. Load behind a proxy/CDN/load-balancer, on "smuggling/desync", or when
  Content-Length vs Transfer-Encoding handling differs. Signals: front-end + back-end chain,
  timing anomalies, HTTP/1.1 keep-alive.
domain: web
type: technique
stability: learning
modes: [bugbounty]
severity: high
owasp: [A05:2021-Security-Misconfiguration]
cwe: [CWE-444]
tools: [burp, http-request-smuggler]
schema_version: 1
---

# HTTP request smuggling (desync)

## When it applies
Requests pass through a front-end (proxy/CDN/LB) to a back-end, and the two disagree on where
one request ends and the next begins (Content-Length vs Transfer-Encoding parsing).

## Why it works
If the front-end and back-end compute request boundaries differently, part of your request is
interpreted by the back-end as the *start of the next* request — which belongs to another user.
That lets you prepend data to victims' requests: bypass controls, capture their requests, or poison caches.

## Method
1. **Detect safely with timing**: use Burp's **HTTP Request Smuggler** / the desync toolkit —
   send a CL.TE / TE.CL probe crafted to make the back-end wait, and watch for the tell-tale delay.
2. **Confirm** by smuggling a prefix that changes a following request's response (e.g. a
   controlled 404→ redirect on the victim's path) without harming users.
3. **Exploit (in scope, carefully)**: bypass front-end auth/routing, capture other users'
   requests (steal cookies/tokens), or web-cache poisoning via the smuggled prefix.
4. **CL.0 / H2 desync**: also test HTTP/2 downgrade and CL.0 variants on modern stacks.

## Gotchas
- This attacks *other users* — on bug bounty, prove it with a benign, self-targeted signal; never
  capture real user data or disrupt service beyond the minimum PoC. Respect RoE strictly.
- Timing detection has false positives — confirm with a request-influence PoC before reporting.
- Use HTTP/1.1 with keep-alive; many CDNs normalize — the desync is in the specific pair.

## Verify success
A smuggled prefix demonstrably affects a subsequent request/response (a controlled, self-owned
victim request shows your injected effect) — proving front/back-end desync.

## References
James Kettle "HTTP Desync Attacks"; PortSwigger smuggling labs & Smuggler extension.
