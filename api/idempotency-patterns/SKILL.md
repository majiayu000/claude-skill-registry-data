---
name: idempotency-patterns
description: This skill should be used when the user mentions "idempotency", "idempotency key", "retries", "exactly once", "double charge", "pagination", "cursor", "offset", "rate limit", "rate limiting", "Retry-After", "safe retries", or making an unsafe HTTP method safe to retry. It provides idempotency-key store recipes, safe-retry semantics for POST/PATCH/DELETE, and cursor/offset pagination plus standard rate-limit headers.
---

# Idempotency Patterns

## Purpose
Provide standardized recipes for the three pieces of API plumbing that clients depend on and servers get subtly wrong: **safe retries** (idempotency keys so a retried mutation applies once), **pagination** (stable, bounded traversal of collections), and **rate limiting** (standard headers so clients back off correctly). All three are static, framework-agnostic patterns, apply them at the boundary, in the handler.

## Why idempotency
HTTP defines `GET`, `HEAD`, `PUT`, and `DELETE` as **idempotent** (repeating them has the same effect as doing them once) and `GET`/`HEAD` as **safe** (no side effects). `POST` is **neither**: and networks retry. A client that times out and retries a `POST /payments` can charge twice. The fix is an **idempotency key**: the client sends a unique `Idempotency-Key` header; the server records key → outcome and, on replay, returns the stored outcome instead of re-executing.

### The idempotency-key algorithm (unsafe methods only)
1. Read the `Idempotency-Key` header. If absent on a create endpoint, either require it (`400`) or proceed without dedup, decide per endpoint.
2. Look up the key (scoped to the authenticated principal + endpoint) in a durable store.
3. **Hit, completed** → return the stored status + body verbatim. Do not re-run.
4. **Hit, in-flight** → the original is still processing: return `409` (or block briefly), never run concurrently.
5. **Miss** → atomically insert the key in an `in-flight` state (unique constraint / `SET NX`), execute the work, store the response, mark `completed`, set a TTL.
6. Guard against **key reuse with a different body**: store a hash of the request; if the same key arrives with a different payload, return `422`.

Apply idempotency **only** to unsafe, non-idempotent methods (`POST`, and non-idempotent `PATCH`). `GET`/`HEAD`/`PUT`/`DELETE` are already idempotent by contract, do not bolt a key onto them. Full store recipes and TTL/window guidance are in `references/idempotency-recipes.md`.

## Pagination in one page
- **Cursor (keyset)** is preferred: `?limit=50&cursor=<opaque>`, ordered by a stable, unique key (usually `(created_at, id)`). O(1) per page, stable under inserts, no deep-offset scan. Return the next cursor (and `hasMore`), not a total.
- **Offset** (`?limit=50&offset=100`) is fine for small, static datasets and jump-to-page UIs, but drifts when rows are inserted/deleted and gets slow at high offsets.
- Always **bound `limit`** (default + max, e.g. 20/100) and **order by a unique key** so the sort is deterministic. Details and encoding in `references/pagination-and-rate-limits.md`.

## Rate-limit headers in one page
Advertise limits with the standard `RateLimit` fields so clients self-throttle instead of hammering you:
- `RateLimit: limit=100, remaining=12, reset=30` (current window) and `RateLimit-Policy: 100;w=60` (the policy).
- On `429 Too Many Requests`, always send `Retry-After` (seconds or an HTTP-date). Use `429` for rate limiting, not `403`.
See `references/pagination-and-rate-limits.md` for the exact header syntax and the legacy `X-RateLimit-*` mapping.

## Golden rules
- Idempotency keys go on **unsafe** methods only; make them **client-supplied**, **durable**, **atomically claimed**, and **TTL-bounded**.
- Never dedup on the request body alone, bodies collide and legitimately repeat; use the explicit key, with a body hash as a mismatch guard.
- Paginate with a **stable unique sort key** and a **bounded limit**; prefer cursors for large or live data.
- Rate limits are a **contract**: publish them in headers and always pair `429` with `Retry-After`.

## Additional Resources
### Reference Files
- **`references/idempotency-recipes.md`**: idempotency-key store schemas (SQL unique-constraint and Redis `SET NX`), the atomic claim, dedup windows/TTLs, request-hash mismatch handling, safe-retry semantics for each HTTP method, and where to store keys.
- **`references/pagination-and-rate-limits.md`**: cursor vs offset design, opaque cursor encoding, stable ordering and tie-breaking, keyset SQL, and the standard `RateLimit`/`RateLimit-Policy`/`Retry-After` headers with the legacy `X-RateLimit-*` mapping.
