---
name: api-design
description: This skill should be used when designing or building an API — endpoints, routes, request/response shapes, error formats, pagination, versioning, or deciding REST vs GraphQL. Trigger phrases include "design the API", "build an endpoint", "REST or GraphQL", "how should I structure my routes", "API error format", "paginate results", "version my API", "validate env vars", "idempotency", "what should this endpoint return". It applies proven REST conventions and a clear REST-vs-GraphQL decision, with env-config validation.
---

# API Design

This skill turns "I need an endpoint" into an API that is consistent, predictable, and safe to evolve. It encodes the conventions that the best public APIs (Stripe, Microsoft, GitHub) share.

Analogy: an API is the menu of a restaurant. A good menu is consistent — every dish described the same way, prices where you expect, no surprises. A messy menu makes every order a negotiation.

## Discovery (max 3 questions, only if unknown)

1. Who consumes this — your own React SPA only, or also mobile / partners / the public?
2. Is it mostly simple CRUD, or deeply nested reads across many relations?
3. Is it public-facing (needs versioning + stability) or internal?

## Step 1 — REST vs GraphQL (decide first)

**Default to REST.** Reach for **GraphQL only when**: clients need flexible, deeply nested reads across many relations; you have multiple divergent clients (web + mobile + partners); or you're composing several backend services. For a single React SPA on one Postgres DB, REST (or tRPC for end-to-end TS types) is simpler and cacheable.

If you do choose GraphQL:
- **Solve N+1 from day one with DataLoader** (batch + cache per request).
- Design the schema around the domain graph, not DB tables.
- Paginate every list field (Relay-style `edges/node/pageInfo`); enforce depth/complexity limits.
- Mutations return the mutated object so clients update cache without a refetch.

## Step 2 — REST conventions (the defaults)

- **Resources are plural nouns**: `/invoices`, `/invoices/{id}/lines`. Verbs are HTTP methods, not paths. Non-CRUD actions: `/invoices/{id}:send`.
- **Version from day one**: URI versioning `/v1/...`, even with only a v1.
- **Cursor-based pagination by default** (opaque `cursor` + `has_more`), not offset — stays consistent on insert, avoids slow `OFFSET` scans. Default page 25, max 100.
- **One consistent error envelope** with the correct HTTP status:
  ```json
  { "error": { "type": "validation_error", "code": "invalid_email", "message": "…", "param": "email" } }
  ```
  Never return `200` on failure.
- **Status codes**: `201 + Location` on create, `204` on delete, `409` conflict, `422` validation, `429 + Retry-After` rate limit.
- **Idempotency**: require an `Idempotency-Key` header on unsafe POSTs (payments, signups). Store key→response for 24h; replay returns the original — no double-charge on retry. GET/PUT/DELETE are idempotent by spec.
- **Consistency**: ISO-8601 UTC timestamps, one field-casing convention (snake_case or camelCase) across the whole API.
- **Filtering over endpoint sprawl**: `?status=open&fields=id,total` instead of a new endpoint per view.

## Step 3 — Validate env config at the boundary

Every API needs config, and a missing var should fail loudly at boot, not silently in prod:

- **Validate all env vars at startup with a `zod` schema** (or `t3-env` on Vite/Next). Fail fast on a missing/malformed var.
- Separate server secrets from client config: on Vite, **only `VITE_`-prefixed vars reach the browser** — never put a secret there.
- Commit `.env.example` (names + dummy values); never commit real `.env*`. (Secrets handling lives in the `secure-coding` skill.)

## Handoff

API shape decided here feeds the `data-modeling` skill (the schema behind it), the `auth` skill (who can call each endpoint), and `secure-coding` (validation + rate limits on each handler).

## Output

Deliver: the REST-vs-GraphQL call with reason, the route list with methods + status codes, the error envelope, the pagination scheme, and a `zod` env schema for the service.

## Reference

microsoft/api-guidelines (~23k⭐), Stripe API design + idempotency docs, donnemartin/system-design-primer (~352k⭐), graphql/dataloader (~13k⭐), t3-oss/t3-env (~4k⭐), colinhacks/zod (~43k⭐).
