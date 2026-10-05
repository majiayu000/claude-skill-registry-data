---
name: rest-api-design
description: Conventions for designing clean, consistent, evolvable REST APIs — resource modeling, HTTP semantics, status codes, pagination, filtering, error envelopes, versioning, idempotency, and security. A deep reference with worked examples and runnable checks.
type: skill
version: 2.0.0
updated: 2026-06-28
---
# REST API Design

A good REST API is **guessable**: once a consumer learns one endpoint, they can predict the rest. This
skill is the deep reference for designing one — the principles, the decisions, the trade-offs, and the
mistakes to avoid. Heavy detail lives in `references/`; copy-paste material in `examples/`; a runnable
contract check in `scripts/`.

## Mental model

Design the API around **resources** (nouns) and use HTTP **verbs** to act on them. The protocol already
gives you a rich vocabulary — methods, status codes, headers, caching — so lean on it instead of
inventing your own conventions on top.

| Concern | REST answer |
|---|---|
| What | a resource, named as a plural noun (`/orders`) |
| Action | the HTTP method (GET/POST/PUT/PATCH/DELETE) |
| Outcome | the status code (200/201/404/409…) |
| Shape | a consistent response envelope |
| Change | an explicit versioning strategy |

## 1. Resource modeling

1. Name collections as **plural nouns**: `/users`, `/orders`. Never verbs in the path (`/getUsers` is wrong — the verb is `GET`).
2. Nest to show ownership, but only **one level deep**: `/users/{id}/orders` is fine; `/users/{id}/orders/{id}/items/{id}/...` is a smell — link instead.
3. Model real-world actions that aren't CRUD as sub-resources or controller endpoints: `POST /orders/{id}/refunds` rather than `POST /refundOrder`.
4. Keep identifiers stable and opaque to clients; don't leak DB internals (prefer UUIDs/ULIDs over auto-increment IDs where enumeration is a risk).

## 2. HTTP method semantics

| Method | Use | Safe | Idempotent |
|---|---|---|---|
| GET | read | yes | yes |
| POST | create / non-idempotent action | no | no |
| PUT | full replace | no | yes |
| PATCH | partial update | no | no* |
| DELETE | remove | no | yes |

Respect these contracts — clients, proxies, and caches rely on them. A `GET` must never mutate state.
See `references/status-codes.md` for the full status-code decision guide.

## 3. Status codes

Return the **accurate** code; never `200 OK` with an error body (it breaks every client's error handling).

```http
201 Created        Location: /orders/101      # after a successful POST
204 No Content                                  # successful DELETE, no body
400 Bad Request                                 # malformed/invalid input
401 Unauthorized   # not authenticated      403 Forbidden  # authenticated, not allowed
404 Not Found      409 Conflict   422 Unprocessable Entity   429 Too Many Requests
```

Full guidance and edge cases (404 vs 403 to avoid leaking existence, 409 vs 422) live in
`references/status-codes.md`.

## 4. The response envelope

Standardize one shape across **every** endpoint so clients parse uniformly. See
`examples/error-envelope.json` and validate any payload with `scripts/check-envelope.mjs`.

```json
{
  "data": [ { "id": 101, "status": "open" } ],
  "meta": { "nextCursor": "eyJpZCI6MTIwfQ", "limit": 20 },
  "error": null
}
```

On error, the same shape with `data: null` and a populated `error` (see §6).

## 5. Pagination, filtering, sorting

Every collection endpoint **must** paginate — an unbounded list is a latent outage. Prefer **cursor**
pagination for large or frequently-changing data (offset pagination scans and skips rows, getting slower
the deeper you go, and double-counts when rows are inserted mid-scan).

```http
GET /v1/orders?status=open&sort=-created_at&limit=20&cursor=eyJpZCI6MTAwfQ
```

The full comparison, cursor encoding, and pitfalls are in `references/pagination.md`.

## 6. Error model

One error shape, everywhere. A machine-readable `code`, a human `message`, and optional field-level
`details`:

```json
{ "data": null, "error": {
    "code": "validation_failed",
    "message": "The request was invalid.",
    "details": [ { "field": "email", "issue": "must be a valid email" } ]
} }
```

Rules and the full catalogue of codes are in `references/error-handling.md`.

## 7. Versioning & evolution

APIs are forever once published. Version explicitly (`/v1/...` in the path is the most operationally
clear) and treat additive changes as backward-compatible; breaking changes require a new version.
Strategy and a deprecation playbook: `references/versioning.md`.

## 8. Idempotency, concurrency, security

- **Idempotency:** accept an `Idempotency-Key` header on `POST` so client retries don't double-create
  (the server stores key → result and replays it). Essential for payments.
- **Concurrency:** use `ETag` + `If-Match` for optimistic locking on updates to prevent lost writes.
- **Security:** authenticate every request, authorize every action server-side (guard against IDOR by
  checking ownership, not just authentication), rate-limit (return `429` + `Retry-After`), and validate
  all input. Pairs with the `security-auditor` agent and the `owasp-top10` skill.

## Common pitfalls (anti-patterns)

- **`200 OK` with `{"success": false}`** — breaks HTTP error handling; use real status codes.
- **Verbs in URLs** (`/createUser`) — the method is the verb.
- **Unbounded list endpoints** — always paginate; a `/users` that returns 2M rows is a DoS on yourself.
- **Inconsistent shapes** — one endpoint returns an array, another an object; clients can't generalize.
- **Leaking existence** via 404-vs-403 to unauthorized users — be deliberate (see status-codes ref).
- **Breaking changes without a version bump** — renaming/removing a field silently breaks consumers.

## When NOT to use REST

REST isn't always the right tool. Prefer **GraphQL** when clients need flexible, nested selections and
you want to avoid over/under-fetching; prefer **gRPC** for low-latency internal service-to-service
calls; prefer **webhooks/event streams** for server-push. REST shines for resource-oriented public
HTTP APIs where cacheability and ubiquity matter.

## Files in this package

- `references/status-codes.md` — full status-code decision guide + edge cases
- `references/pagination.md` — cursor vs offset, encoding, pitfalls
- `references/versioning.md` — versioning strategies + deprecation playbook
- `references/error-handling.md` — error shape, codes, validation details
- `examples/orders-api.openapi.yaml` — a complete OpenAPI snippet
- `examples/error-envelope.json` — canonical success/error payloads
- `scripts/check-envelope.mjs` — runnable Node check that a payload matches the envelope

Pairs with the `api-designer` agent, the `api-documenter` agent, and the `webhook-design` skill.
