---
name: HTTP
slug: http
version: 1.0.0
description: Use HTTP correctly with proper methods, status codes, headers, and caching.
homepage: https://clawic.com/skills/http
metadata:
  clawdbot:
    emoji: 🌐
    os:
    - linux
    - darwin
    - win32
    displayName: HTTP
---

## Redirects (Often Confused)

- 307 vs 308: both preserve method; 307 temporary, 308 permanent—use these for POST/PUT redirects
- 301/302 may change POST to GET (browser behavior)—don't use for API redirects with body
- Include `Location` header with absolute URL—relative may fail in older clients
- Redirect loops: limit to 5-10 follows; infinite loops crash clients

## Caching Combinations

- `Cache-Control: no-store` for sensitive data—never written to disk
- `no-cache` still caches but revalidates every time—not "don't cache"
- `private, max-age=0, must-revalidate` for user-specific, always-fresh content
- `public, max-age=31536000, immutable` for versioned static assets
- `Vary: Accept-Encoding, Authorization` when response depends on these headers—forgetting Vary breaks caching

## Conditional Requests

- `ETag` + `If-None-Match`: prefer for APIs—content hash based
- Strong vs weak ETags: `"abc"` vs `W/"abc"`—weak allows semantically equivalent responses
- `If-Match` for optimistic locking: fail update if resource changed since read
- 412 Precondition Failed when `If-Match` fails—not 409 Conflict

## CORS Preflight Triggers

- Custom headers (anything not Accept, Accept-Language, Content-Language, Content-Type simple values)
- Content-Type other than: application/x-www-form-urlencoded, multipart/form-data, text/plain
- PUT, DELETE, PATCH methods—even to same origin if other conditions met
- ReadableStream body—triggers preflight
- Preflight cached per `Access-Control-Max-Age`—set to 86400 to reduce OPTIONS spam

## Security Headers (Always Set)

- `Strict-Transport-Security: max-age=31536000; includeSubDomains`—HSTS, once set can't easily undo
- `X-Content-Type-Options: nosniff`—prevents MIME sniffing attacks
- `X-Frame-Options: DENY` or `SAMEORIGIN`—prevents clickjacking
- `Content-Security-Policy`—complex but essential; start with report-only mode

## Range Requests

- `Accept-Ranges: bytes` signals support—clients can request partial content
- `Range: bytes=0-1023` requests first 1024 bytes; `bytes=-500` requests last 500
- Return 206 Partial Content with `Content-Range: bytes 0-1023/5000`
- 416 Range Not Satisfiable if range invalid—include `Content-Range: bytes */5000`

## Error Response Best Practices

- Structured JSON errors: `{"error": {"code": "VALIDATION_FAILED", "message": "...", "details": [...]}}`
- Include request ID in error response—enables log correlation
- Don't leak stack traces in production—log server-side, return generic message
- 409 Conflict for business rule violations (duplicate email, insufficient funds)—not just 400

## Retry Patterns

- Retry only idempotent methods by default—GET, PUT, DELETE, HEAD
- POST retry needs idempotency key—`Idempotency-Key: <client-generated-uuid>`
- Exponential backoff: 1s, 2s, 4s, 8s... with jitter—prevents thundering herd
- Respect `Retry-After` header—can be seconds or HTTP date
- Set reasonable timeout (30s typical)—don't wait forever

## Headers Often Forgotten

- `Vary`: must include headers that affect response—CORS without `Vary: Origin` breaks
- `Content-Disposition: attachment; filename="report.pdf"` for downloads
- `X-Request-ID`: generate if not present, propagate to downstream services
- `Accept-Language` for localized responses—respect with graceful fallback

## Connection Behavior

- HTTP/1.1 without `Content-Length` or chunked = connection close after response
- `Transfer-Encoding: chunked` for streaming—can't set Content-Length
- HTTP/2 is binary, multiplexed—no head-of-line blocking at HTTP level
- WebSocket upgrade: GET with `Connection: Upgrade`, `Upgrade: websocket`
