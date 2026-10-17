---
name: attack-smuggling-te-cl
description: "TE.CL desync — front-end trusts Transfer-Encoding, back-end trusts Content-Length; body-wrapping detection, capture, prefix injection"
category: "web-application"
version: "1.0"
author: "bountyreper-official"
tags:
  - request-smuggling
  - te-cl
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

# TE.CL Smuggling

## Objective

Front-end uses Transfer-Encoding (chunked); back-end ignores it and reads
Content-Length. Your smuggled request lives INSIDE the chunked body — the back-end
reads only the first CL bytes as the request and everything after becomes its next
request.

## Methodology

### 1. Confirm with a differential

```http
POST / HTTP/1.1
Host: TARGET
Content-Length: 4
Transfer-Encoding: chunked

6d
GET /404 HTTP/1.1
X-Ignore: X

0

```

The front-end sees chunked body `6d` + `0` (one request). The back-end reads the first
`4` bytes... wait — CL=4 but body is a chunk-line: tune CL to exactly cover
`6d\r\nGET ` so the back-end request is `GET /404 HTTP/1.1...`. The remainder of the
chunked body becomes the back-end's NEXT request. Differential = two responses.

### 2. Capture the next user's request

```http
POST / HTTP/1.1
Host: TARGET
Content-Length: 4
Transfer-Encoding: chunked

71
GET /response-capture HTTP/1.1
X-Ignore: X

0

```

CL=4 (back-end consumes `71\r\n` + 2 bytes), then the smuggled `GET` + the next user's
request line/headers trail as extra body — set CL to swallow exactly to make the
capture request whole. Iterate lengths; differential proves each step.

### 3. Prefix-injection primitives

- Capture → reflect next victim's headers into your response
- Cache poison → smuggled `GET /` with `X-Header` unkeyed by cache → poisoned entry
- Body-size DoS → CL swallows the next user's ENTIRE request (they hang) — DoS variant,
  lower severity, needs authorization

### 4. Length arithmetic (the hard part)

```text
front (TE) reads:  <hex>\r\n<body><0\r\n\r\n>
back  (CL) reads:  first CL bytes as request 1, remainder as request 2+
```

- CL must be ≥ actual bytes the back-end consumes before the smuggled request starts
- Smuggled request headers MUST each end with `X-Ignore:` filler so lengths are tunable
- Test lengths ±1 byte — off-by-one = front-end 500s (that IS information)

## Proof

- Two-response differential per smuggle
- Captured victim request (credentials REDACTED) with the capture path visible
- Poison: independent client receives poisoned cache entry

## Notes

- Many CDNs reject `chunked` on the front → TE.TE obfuscation (transfer-encoding case/
  spacing variants) is the follow-up — see te-te sub-skill
