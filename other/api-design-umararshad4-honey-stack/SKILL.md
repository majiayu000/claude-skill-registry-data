---
name: api-design
description: "Design or evolve an API: pick REST/GraphQL/gRPC/tRPC, model resources and status codes, version without breaking, RFC 9457 errors, cursor pagination, idempotency, schema-first OpenAPI/proto/GraphQL contracts."
license: MIT
metadata:
  reviewed: "2026-10-18"
  sources: "honey-stack research 2026-10-18 (RFC 9457, OpenAPI 3.1/3.2, Idempotency-Key draft, Relay connections, Richardson maturity). Details in references/."
---

# api-design

Design an API that's hard to misuse and safe to evolve. Choose the style, model it cleanly, and never break a published contract.

## Pick the style
- **REST** — public/partner APIs, CRUD-ish resources, broad clients, cacheability. Add OpenAPI for the schema.
- **GraphQL** — client-driven read graphs, mobile/BFF, many screens needing different fields. Cost: N+1, hard HTTP caching, per-field auth, depth-limit DoS.
- **gRPC** — internal service-to-service, low latency, streaming, polyglot. Not browser-native (needs grpc-web/Connect).
- **tRPC** — a single TypeScript monorepo wanting end-to-end types with no codegen. TS-only; not a cross-language public contract.

Rule: public/unknown clients → REST+OpenAPI; internal mesh → gRPC; flexible field selection → GraphQL; one TS codebase → tRPC.

## REST done well
Resources are nouns (`/orders/{id}/line-items`), nesting ≤2 levels; non-CRUD actions are command sub-resources (`POST /orders/{id}/cancel`), not `/cancelOrder`. Correct methods and status codes (201+`Location`, 202 async, 204, 400 vs 401 vs 403, 409 conflict, 422 validation, 429+`Retry-After`); never 200-with-error-body. **Cursor/keyset pagination**, not deep offset. Filtering/sorting with documented, validated fields. `references/rest.md`.

## Idempotency & concurrency
GET/PUT/DELETE are idempotent by HTTP semantics. For POST, accept a client-generated **`Idempotency-Key`** header; store key→response for a TTL and replay on retry; the same key with a different payload is a 422. (This is an active IETF draft, not yet an RFC, but Stripe/PayPal-standard.) Optimistic concurrency via `ETag` + `If-Match` → 412 on mismatch.

## Versioning (evolve without breaking)
URL `/v1` (common, cache-friendly), header, or date-based (Stripe-style). Within a version make only **additive** changes — add optional fields/endpoints, never remove/rename/retype a field, never tighten validation or change a default. Expand → migrate clients → contract across a major bump. Deprecate with the `Deprecation` (RFC 9745) and `Sunset` (RFC 8594) headers, a published window, and usage alerting. `references/versioning.md`.

## Error contract — RFC 9457
Use **Problem Details** (`application/problem+json`, RFC 9457, which obsoletes 7807): `type` (stable URI = your machine code), `title`, `status`, `detail`, `instance`, plus `errors[]` for per-field validation and a `trace_id`. One envelope across every endpoint; clients branch on `type`/`code`, never on `title` text. Never leak stack traces, SQL, internal hosts, versions, or whether an account exists.

## Schema-first contracts
- **OpenAPI 3.1** (aligned to JSON Schema 2020-12) is the safe default; design-first, generate clients/servers/validators/mocks (`redocly`/`spectral` lint, `openapi-generator`, Prism mock, Schemathesis). 3.2 (Sept 2025) exists but tooling is uneven.
- **gRPC/protobuf**: fields match by **tag number** — never change or reuse a tag; `reserved` tombstones removed tags/names; adding fields is safe; keep enum `0` = `UNSPECIFIED`.
- **GraphQL**: default nullable, non-null (`!`) only when guaranteed; **Relay Connections** for pagination; **DataLoader** to kill N+1; depth/complexity limits; mutations take one input and return a payload with `userErrors`.
`references/contracts.md`.

## Cross-cutting
Auth (OAuth2/OIDC + PKCE for users, client-credentials for machines; validate JWT `alg`/`iss`/`aud`/`exp`, short TTLs, no secrets in the payload). Rate limit → 429 + `Retry-After` + `RateLimit` headers. CORS: echo specific origins, not `*` with credentials. Validate every input at the boundary. Timestamps RFC 3339 UTC with `Z`. Money as integer minor units or decimal string + ISO-4217 currency, never float. `references/cross-cutting.md`.

## Anti-patterns
Chatty APIs (add composite/expand endpoints or GraphQL); leaking the DB schema as the API (use DTOs); breaking changes without a version bump; verbs in URLs; unbounded list endpoints (always paginate + cap `limit`); inconsistent naming (pick one case, lint it).

Done when: the style fits the clients, the contract (OpenAPI/proto/GraphQL schema) exists, errors follow RFC 9457, lists are cursor-paginated and capped, and any change to a published API is additive or a version bump.
