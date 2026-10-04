---
name: api-design
description: Use when designing REST endpoints, defining error envelopes, setting a versioning or deprecation policy, choosing pagination shape, adding idempotency to mutations, reviewing API contracts, or when two services need a stable interface between them.
---

# API Design

## Overview

Define the project's API conventions *before* endpoints proliferate. Output is `.forge/api-design.md` — verbs and status codes, the error envelope schema, versioning + deprecation policy, pagination/filter contract, rate-limiting envelope, auth/authz envelope, idempotency rules for mutations, and the public-vs-internal API boundary. Consumed by `architecture-and-contracts` (per-module contracts inherit these), `incremental-implementation` (endpoints must conform), and `code-review-and-quality` (PR review checklist).

## When to Use

- A new service or new public endpoint is being designed
- Two services need a stable interface and there's no project-wide envelope
- Error shapes vary across endpoints and clients have to special-case each one
- A breaking change is about to ship and there's no versioning policy
- A list endpoint is being added and pagination shape is unclear
- A mutation endpoint will be retried by clients and there's no idempotency story

## When NOT to Use

- A single trivial endpoint is being added to a service that already has documented conventions
- Internal-only RPC inside one service (use module contracts via `architecture-and-contracts`)
- GraphQL or gRPC — adapt the principles but the file should call out the protocol

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "We'll version when we break something" | By then clients are coupled to the unversioned shape. Versioning costs nothing on day one, costs a migration on day 200. |
| "Every endpoint is different, no need to standardize" | Inconsistency is a bug, not flexibility. Every divergent error shape costs clients a special case. |
| "Just return 200 with an error field" | Clients can't distinguish success from failure without parsing the body. Proxies and CDNs cache 200s aggressively. |
| "Internal APIs don't need contracts" | Internal APIs become external APIs the moment a second team touches them. Two consumers = production interface. |
| "PATCH replaces the resource" | RFC 7396 says PATCH merges. Clients that depend on merge semantics will break silently if you replace. |
| "Idempotency keys are only for payments" | Network retries happen on every endpoint. Without idempotency, retries create duplicates everywhere. |

## Red Flags

- Different error shapes per endpoint (`{ error: "..." }` here, `{ message: "..." }` there, raw string elsewhere)
- No version prefix or header anywhere — first breaking change requires a fork
- `200 OK` with `{ "success": false }` in the body
- `PATCH` that replaces the resource entirely
- `POST /payments` with no idempotency key support
- An "internal" endpoint with no auth, reachable from the public internet
- `OFFSET`/`LIMIT` pagination on a feed that will exceed 10k rows
- A field added to a response is the only change — no version bump, no deprecation notice

## Precedence with architecture contracts

`.forge/contracts/<module>.md` is the **authoritative source** for module boundaries, operations, types, and error cases. `api-design.md` is the **subordinate** that defines how those operations map to HTTP (verbs, paths, envelope shape, error codes, versioning).

**Rule:** If `.forge/contracts/` exists, **read every contract first.** Your API design must be consistent with the operations and error types they define. If a contract specifies `RefundError` with cases `TransactionNotFound | RefundWindowExpired | AlreadyRefunded`, the matching HTTP design must surface those exact codes — no inventing new ones, no collapsing them into a generic 400.

If a contract is missing an operation you need to expose (e.g., the PRD calls for refunds but `PaymentService` contract has no `refund`), do NOT add it to `api-design.md` alone — file `/feedback` targeting the contract so it gets updated upstream. Otherwise the two artifacts will diverge and `forge-sync` will flag a CONFLICT.

If no contracts exist yet, `api-design.md` may define the envelope policy in isolation, but the module boundaries it references will be back-filled when `architecture-and-contracts` runs.

## Core Process

### Step 0: Read existing contracts (if any)

Glob `.forge/contracts/*.md`. For each contract found:
- Extract every operation in `Provides`
- Extract input/output types
- Extract error types and their conditions

Hold these as the source of truth. Every endpoint you design must trace back to a contract operation (or be flagged as new and worth a feedback entry).

### Step 1: Define base conventions

- **Verbs:** `GET` (read), `POST` (create or non-idempotent action), `PUT` (replace), `PATCH` (merge per RFC 7396), `DELETE` (remove).
- **Status codes:** `2xx` success only. `4xx` for client errors. `5xx` for server errors. Never `200 OK` with `error: true`.
- **Resource naming:** plural nouns (`/users/{id}`, `/orders`).
- **Snake or camel:** pick one for the wire format and never mix.

### Step 2: Write the error envelope schema

Every error response uses the same shape. Write it in `.forge/api-design.md`:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "User not found.",
    "field": "user_id",
    "request_id": "01HABC...",
    "details": {}
  }
}
```

- `code` — stable, machine-readable, screaming-snake-case. Clients pattern-match on this, never on `message`.
- `message` — human-readable, non-technical when surfaced to end users.
- `field` — populated for validation errors only.
- `request_id` — always populated; matches the correlation ID from `observability`.
- `details` — optional, structured per error code.

Cross-reference the `error-handling-and-resilience` taxonomy (transient / permanent / user-correctable maps to retryable HTTP codes).

### Step 3: Set versioning and deprecation policy

Choose one mechanism (URI `/v1/`, header `Accept: application/vnd.api+json;version=1`, or query `?version=1`) and apply it everywhere. Document:

- How a version is introduced (always start at `v1`, never `v0`).
- When a version is required to bump (any field removed, renamed, or type-changed; status-code semantics changed; required-vs-optional flip).
- Deprecation window (minimum 6 months for public, 30 days for internal-only).
- Deprecation signaling: `Deprecation: <date>` header + warnings in `details`.

### Step 4: Pagination, filtering, sorting

- Pagination: cursor preferred. Standard shape: `{ items: [], next_cursor: string|null, prev_cursor: string|null }`. `OFFSET`/`LIMIT` only allowed for small admin endpoints.
- Filtering: `?status=active` for exact match, `?status=active,pending` for `OR`, `?created_after=...` for ranges. No nested-query DSL unless the product justifies one.
- Sorting: `?sort=field` ascending, `?sort=-field` descending. Multi-sort: `?sort=-created_at,id`.

### Step 5: Idempotency, rate limiting, auth envelopes

- **Idempotency:** every mutation accepts `Idempotency-Key: <client-generated>`. Server stores result keyed by `(endpoint, key)` for at least 24h. Replays return the original response.
- **Rate limiting:** every response includes `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`. `429` on exceedance with `Retry-After`.
- **Auth:** standard `Authorization: Bearer <token>`. Errors use stable codes (`AUTH_MISSING`, `AUTH_EXPIRED`, `AUTH_INVALID`, `FORBIDDEN`). Never leak existence — `403` and `404` for "exists but you can't see it" both return `404` at the public boundary.

### Step 6: Document the public/internal boundary

In `.forge/api-design.md`: list every endpoint as `public` (versioned, deprecation-aware, hardened) or `internal` (faster iteration, still auth-gated, never reachable from internet). Internal endpoints get their own subdomain or VPC routing. Mixing the two on the same hostname guarantees future leaks.

### Step 7: Header

Prepend a `forge:meta` header (`generated_by: api-design`, `generated_at: <ISO 8601 UTC with Z>`, `depends_on: [.forge/architecture.md]` — paths only, never hashes, `generated_from: {.forge/architecture.md: <upstream content_hash AT generation time>}`, `content_hash: <sha256 first 8 of THIS file's body>`). See [forge-dependency-graph](../../references/forge-dependency-graph.md).

## Verification

- [ ] Existing `.forge/contracts/*.md` read (or noted as absent); every endpoint traces back to a contract operation
- [ ] No endpoint invents an error code that contradicts the contract's named errors
- [ ] If a needed operation is missing from contracts, a `/feedback` entry was filed targeting the contract — not silently added here
- [ ] `.forge/api-design.md` written
- [ ] Every endpoint returns errors in the standard envelope (code, message, request_id)
- [ ] Every endpoint has a version (URI, header, or query) — none unversioned
- [ ] Every mutation supports an `Idempotency-Key` header (or has a documented reason it doesn't need one)
- [ ] Every paginated list uses the standard cursor envelope
- [ ] No `200 OK` with `{ "success": false }` anywhere
- [ ] Every response includes `RateLimit-*` headers and a `request_id`
- [ ] Public-vs-internal labels assigned for every endpoint, with separate hostnames
- [ ] Breaking changes have a documented deprecation window before the cut-over
