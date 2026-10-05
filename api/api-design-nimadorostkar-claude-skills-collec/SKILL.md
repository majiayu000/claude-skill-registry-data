---
name: api-design
description: Use when designing or reviewing an HTTP API. Covers resource modeling, status codes, pagination, idempotency, versioning, error formats, and the contract details that break clients when you get them wrong.
metadata:
  category: backend
  version: 1.0.0
  tags: [api, rest, http, openapi, versioning]
---

# API Design

## Purpose

Design HTTP APIs that clients can use correctly without reading your source code, and that you can evolve without breaking them.

## When to Use

- Designing a new API or a new endpoint on an existing one.
- Reviewing an API before it becomes public and therefore permanent.
- Introducing versioning, pagination, or idempotency to an API that lacks them.
- Writing or auditing an OpenAPI specification.

## Capabilities

- Resource and URL modeling.
- Status-code semantics and consistent error payloads (RFC 9457 problem details).
- Pagination strategies and their trade-offs.
- Idempotency for unsafe methods.
- Versioning and deprecation without breaking clients.
- OpenAPI specification as the source of truth.

## Inputs

- The domain operations the API must expose.
- Client types: first-party, third-party, mobile, machine.
- Expected volume, page sizes, and latency requirements.

## Outputs

- An OpenAPI 3.1 specification.
- Consistent error and pagination formats across every endpoint.
- A documented versioning and deprecation policy.

## Workflow

1. **Model resources, not procedures** — `POST /orders/{id}/refunds` rather than `POST /refundOrder`. When an operation genuinely is not a resource, it is fine to say so, but check first.
2. **Fix the status codes** — 200 for a body, 201 with a `Location` for creation, 202 for accepted-but-not-done, 400 for malformed, 401 versus 403 correctly, 409 for conflict, 422 for semantically invalid, 429 with `Retry-After`.
3. **Standardize errors** — One shape, every endpoint. RFC 9457 problem details, with a machine-readable `type` and field-level detail.
4. **Choose pagination deliberately** — Cursor-based for anything that mutates or is large. Offset only for small, static datasets.
5. **Make unsafe methods idempotent** — Accept an `Idempotency-Key` header on POST; return the original response on replay.
6. **Version from day one** — Even if the first version is the only one. Retrofitting a version is far worse than carrying one.

## Best Practices

- Never return a bare array as a top-level response. `{"data": [...], "next_cursor": "..."}` leaves room to add fields; `[...]` does not.
- 200 with `{"error": ...}` is a defect. Clients branch on status codes.
- Field names are permanent. Choose them as carefully as a database column.
- Do not expose internal identifiers or enum integers. Use opaque IDs and string enums.
- Any list endpoint without a limit will eventually be called with a million rows behind it. Cap it, and document the cap.
- Deprecate with headers (`Deprecation`, `Sunset`) and a timeline, not with an announcement nobody reads.

## Examples

**Cursor pagination and problem-details errors:**

```http
GET /v1/orders?limit=50&cursor=eyJpZCI6IjAxSFgifQ HTTP/1.1

200 OK
{
  "data": [ { "id": "ord_01HX...", "total_cents": 4200, "currency": "USD" } ],
  "next_cursor": "eyJpZCI6IjAxSFkifQ",
  "has_more": true
}
```

```http
POST /v1/orders HTTP/1.1
Idempotency-Key: 4f3a2b1c-...

422 Unprocessable Content
Content-Type: application/problem+json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Order validation failed",
  "status": 422,
  "detail": "One or more line items are invalid.",
  "errors": [
    { "field": "items[0].quantity", "code": "min", "message": "must be at least 1" }
  ]
}
```

## Notes

- Cursor pagination is stable under concurrent inserts; offset pagination silently skips and duplicates rows. If the data mutates, offset is a correctness bug, not a performance one.
- Idempotency keys must be stored with the response and a TTL, keyed by (key, endpoint, request-hash). Returning a cached response for a *different* body under the same key is worse than not having idempotency at all.
- URL versioning (`/v1/`) is the least elegant and the most operationally forgiving. Header-based versioning is cleaner and much harder to debug in a proxy log.
