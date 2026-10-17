---
name: attack-smuggling-h2
description: "HTTP/2 desync — H2.CL and H2.TE downgrade smuggling, 0-length CL injection, client-side desync, browser-triggered attacks"
category: "web-application"
version: "1.0"
author: "bountyreper-official"
tags:
  - request-smuggling
  - http2
  - h2c
  - downgrade
tech_stack:
  - web
cwe_ids:
  - CWE-444
chains_with:
  - attack-request-smuggling
  - attack-cache-poison
prerequisites:
  - attack-request-smuggling
---

# HTTP/2 Smuggling

## Objective

HTTP/2 is binary — no smuggling INSIDE h2. The bug is the DOWNGRADE: h2 front-end
rewrites to HTTP/1.1 for the back-end and mishandles `content-length`/`transfer-encoding`
pseudo-headers in the process (H2.CL / H2.TE), or the back-end accepts h2c.

## Methodology

### 1. Confirm h2 first

```bash
curl -sI --http2 https://TARGET | grep -i "HTTP/2"
# ALPN negotiated h2 = downgrade path exists (front→back h2c or h1 rewrite)
```

### 2. H2.CL (inject content-length pseudo-header)

```http
:method: POST
:authority: TARGET
content-length: 0
content-length: 65
[body]: GET /404 HTTP/1.1
Host: TARGET
X-Ignore: X
```

Two CL headers where the front takes one (or h2 merges) and the back takes the other
→ desync. Send with an h2-capable client (h2 frame-level, not curl h2 - it won't emit
duplicate pseudo-headers). Tool: h2-based smuggler scripts / Burp HTTP/2 smuggler.

### 3. H2.TE (transfer-encoding is illegal in h2 — some stacks forward it anyway)

```http
:method: POST
transfer-encoding: chunked
[body]: smuggled request
```

If the downgrade forwards `transfer-encoding` verbatim to an HTTP/1.1 back-end, you
control the body frame → the back-end parses chunked → desync (same as cl-te playbook).

### 4. 0-length CL + CRLF injection into headers

```http
:method: GET
:authority: TARGET
content-length: 0
referer: x\r\nGET /404 HTTP/1.1\r\nX-Ignore: X
```

Header-value CRLF survives the downgrade → the "header" becomes a smuggled request.

### 5. Client-side desync (browser-triggered)

- Target responds h1-style to some requests (no h2 on that route) while the browser
  pipelines → the VICTIM's browser does the smuggling (no server-side desync needed)
- Delivery: any cross-site request the victim's browser sends on a keep-alive socket
  (fetch/XHR with your crafted body). Impact: CSRF-adjacent ATO — pair with
  attack-account-takeover

## Proof

- h2 evidence required: frames/tooling output, NOT raw h1 nc probes
- Differential responses (front vs back split) as with h1 smuggling
- For client-side desync: victim browser console/capture evidence

## Notes

- Proxies that strip CL from h2 downgrade are NOT vulnerable — try TE forms before
  concluding
- `connection`-related headers in h2 are illegal — some front-ends DO pass them on
  downgrade: that alone is a finding candidate (h2c downgrade) at medium
