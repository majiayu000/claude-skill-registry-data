---
name: error-envelope
description: This skill should be used when the user mentions "error handling", "problem details", "rfc 9457", "rfc 7807", "request validation", "api errors", "zod", "pydantic", "class-validator", "error response format", "problem+json", "validation error", or making an API return consistent, machine-readable errors. It provides the RFC 9457 Problem Details envelope and idiomatic per-stack request-validation patterns.
---

# Error Envelope

## Purpose
Provide one standardized way to (1) validate a request at the boundary and (2) return every error in a consistent, machine-readable envelope. These are high-volume boilerplate that teams re-implement inconsistently, one endpoint returns `{ "error": "bad" }`, the next returns a 200 with `{ "success": false }`, a third leaks a stack trace. The cure is a single validation layer plus a single error format: **RFC 9457 Problem Details** (`application/problem+json`), which obsoletes RFC 7807 (same wire format, updated reference).

## The RFC 9457 envelope
Every error response is `application/problem+json` with these standard members (all optional, but be consistent):

| Member | Meaning |
|---|---|
| `type` | A URI identifying the problem *kind* (dereferenceable docs, or `about:blank`). The primary identifier. |
| `title` | Short, human-readable, stable summary for that `type`. |
| `status` | The HTTP status code, duplicated in the body. |
| `detail` | Human-readable explanation specific to *this* occurrence. |
| `instance` | A URI for this specific occurrence (e.g. the request path or an error id). |

Add **extension members** for machine use: `errors` (per-field validation failures), `traceId`/`requestId`, `code` (your internal error code), `retryAfter`. See `references/rfc9457.md`.

## Validation → error, at the boundary
Validate params, query, and body **before** business logic. A validator failure is not an exception to leak, map it into the envelope with a `422 Unprocessable Content` (or `400`) and an `errors` array of `{ field, message, code }`. See `references/validation-patterns.md` for the idiomatic validator per stack (Zod, Pydantic, class-validator, Joi, JSON Schema/Ajv, Go validator, Rails strong params) and how to reshape each library's native error into the envelope.

## Golden rules
- **One error handler.** Centralize the envelope in middleware / an exception filter / `@ControllerAdvice` / DRF `exception_handler`: never hand-format errors per route.
- **Status in the status line and the body.** They must match.
- **Never 200-with-error.** An error is a 4xx/5xx; a `200 { success: false }` breaks every generic client and HTTP cache.
- **Reject unknown fields** in strict endpoints (`.strict()`, `forbid_extra`, `additionalProperties: false`) so typos and injected fields fail loudly.
- **Never leak internals.** No stack traces, SQL, file paths, or ORM messages in `detail`; log those server-side and put a `traceId` in the body instead.
- **Stable `type` URIs.** Clients branch on `type`, not on the prose in `title`/`detail`: keep `type` stable even when you reword the message.
- **Content negotiation.** Set `Content-Type: application/problem+json` so clients can distinguish a problem from a normal body.

## Status-code quick map
- `400` malformed syntax (unparseable JSON). `401` unauthenticated. `403` authenticated but forbidden. `404` not found. `409` conflict (idempotency replay mismatch, version conflict). `422` well-formed but semantically invalid (validation). `429` rate-limited (+ `Retry-After`). `5xx` server fault (never include the exception text).

## Additional Resources
### Reference Files
- **`references/rfc9457.md`**: the full Problem Details format: member semantics, a canonical validation-error example, multi-error and extension-member patterns, RFC 7807 → 9457 notes, and the anti-patterns to reject in review.
- **`references/validation-patterns.md`**: idiomatic request validation per stack (Zod, Pydantic, class-validator, Joi, JSON Schema/Ajv, Go `validator`, Rails strong params), each with a schema example and the code that maps its native error into the RFC 9457 `errors` array.
