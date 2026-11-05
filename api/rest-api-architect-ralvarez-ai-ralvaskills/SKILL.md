---
name: rest-api-architect
version: 1.1.1
description: Cross-language REST conventions — resource URLs, method semantics, status codes, URL-prefix versioning, cursor pagination, snake_case JSON, ISO 8601 timestamps, RFC 9457 errors, Idempotency-Key, ETag/If-Match, OpenAPI as source of truth. Framework-agnostic. Use when designing or auditing REST endpoints.
---

# REST API Architecture

Cross-language conventions for HTTP/JSON REST APIs. Framework-agnostic. Pair with [fastapi-architect](../../frameworks/fastapi-architect/SKILL.md) or [gin-architect](../../frameworks/gin-architect/SKILL.md) for implementation. See [STACK.md](STACK.md) for the specs this skill is built on.

## 1. URL & resource design

- **Plural nouns for collections:** `/v1/users`, `/v1/orders`. Never verbs in URLs (`/v1/createUser` is wrong — the method is the verb).
- **Resource ID in the path:** `/v1/users/{user_id}`, never as a query parameter.
- **Nest only one level deep** for true containment: `/v1/orders/{order_id}/items`. Beyond one level, use IDs and filter queries instead — deeper hierarchies turn brittle the moment relationships change.
- **`snake_case` in URLs and query params.** Consistent with the JSON casing below.
- **Sub-resources expose hierarchy, not actions.** `/v1/orders/{id}/cancellation` (PUT to create) instead of `POST /v1/orders/{id}/cancel`. The state change is *what is created*, not a verb on the parent.

## 2. HTTP method semantics

| Method | Purpose | Idempotent | Safe |
|---|---|---|---|
| `GET` | Read | Yes | Yes (no side effects) |
| `POST` | Create (server assigns ID) **or** action that doesn't fit elsewhere | **No** | No |
| `PUT` | Replace entire resource (client supplies full state) | Yes | No |
| `PATCH` | Partial update | **No** (unless body is itself idempotent — usually not) | No |
| `DELETE` | Remove | Yes | No |

- **`PUT` requires the full resource representation.** A `PUT` with only some fields is a bug — that's `PATCH`'s job.
- **`PATCH` body uses JSON merge patch** (RFC 7396) — flat field-set means "change these, leave the rest". Don't invent your own dialect.
- **`POST` is also for actions that don't map to CRUD** — e.g. `/v1/payments/{id}/refunds` (creates a refund). The resource is the action's outcome.

## 3. Status codes

Use the right code for the situation. The full table — every code, when to use it, the common confusions (401 vs 403, 404 vs 410, 422 vs 400) — is in [STATUS_CODES.md](STATUS_CODES.md).

**One hard rule:** never `200 OK` for errors. Returning `{"success": false, "error": ...}` with a 200 status is wrong and breaks every HTTP-aware tool.

## 4. Versioning — URL prefix

- **Path prefix only:** `/v1/users`, `/v2/users`. No header-based versioning, no query-param versioning.
- **Bump the version when a breaking change ships.** Additive changes (new optional field, new endpoint) stay in the same version.
- **Run versions side-by-side** until clients migrate. Deprecate with `Deprecation` and `Sunset` response headers (RFC 8594) before removing.
- **Internal microservices** can skip versioning until an external consumer appears — but it's cheap to start with `/v1/` from day one.

## 5. Pagination — cursor, not offset

Cursor pagination is stable under concurrent writes and O(1) per page; offset is O(N) and reads can shift between pages. Request/response shape + rules in [PAYLOADS § 1](PAYLOADS.md#1-cursor-pagination).

## 6. Filtering, sorting, searching

- **Filtering:** `?status=paid&customer_id=01J9...`. Equality only by default — operator syntax (`?price[gte]=100`) is fine for richer endpoints but document each operator in OpenAPI.
- **Sorting:** `?sort=-created_at,name` — comma-separated, prefix `-` for descending. Document allowed sort fields.
- **Searching:** `?q=alice` for free-text search across documented columns. Don't expose raw SQL `LIKE` patterns from clients.
- **Sparse fieldsets:** `?fields=id,email,created_at` to limit response payload — useful for list endpoints. Validate against the schema.

## 7. Error contracts — RFC 9457 Problem Details

Every error response uses `application/problem+json`. Canonical shape + rules in [PAYLOADS § 2](PAYLOADS.md#2-rfc-9457-problem-details); structured `422` validation shape in [PAYLOADS § 3](PAYLOADS.md#3-validation-errors-422).

Key rules:

- **`type` is a stable URL** — clients switch on it. Never change once published.
- **One shape for every error.** Don't mix RFC 9457 with framework defaults.
- **`correlation_id` required on `5xx`** so support can match server logs.

## 8. Idempotency — `Idempotency-Key` mandatory

Every `POST` and `PATCH` requires an `Idempotency-Key` header. Without it the server returns `400 Bad Request`. The server caches the response keyed by `(caller_id, method, path, key)` for 24h and replays on retry; `GET`/`PUT`/`DELETE` are already idempotent by HTTP semantics and don't need it.

Full implementation reference — cache shape, TTL choice, concurrent-request handling, storage options, client guidance, common mistakes — in [IDEMPOTENCY.md](IDEMPOTENCY.md).

## 9. Concurrency control — `ETag` + `If-Match` mandatory

Every editable resource exposes an `ETag` on read. Every `PUT` and `PATCH` requires `If-Match` matching the current ETag, or returns `412 Precondition Failed`. `If-None-Match` on `GET` enables `304 Not Modified` caching for free.

Full implementation reference — where the ETag value comes from (default: monotonic version column), strong vs weak, the 412 retry flow, common mistakes — in [CONCURRENCY.md](CONCURRENCY.md).

## 10. Auth & security headers

- **Authentication via `Authorization: Bearer <token>`.** No tokens in query params (they leak into logs and referrer headers).
- **`401`** for missing/invalid credentials; **`403`** for valid credentials lacking permission. Mixing these confuses clients debugging access issues.
- **HTTPS always.** Reject plaintext in production at the load balancer; redirect at the edge.
- **CORS:** explicit allow-list of origins; never `Access-Control-Allow-Origin: *` for authenticated endpoints.
- **Security headers** (added at the gateway or app layer): `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, `Content-Security-Policy` (if serving HTML), `Referrer-Policy: no-referrer`.
- **No PII in URLs.** Emails, names, IDs that map to PII go in headers or bodies — URLs end up in access logs, browser histories, and proxy caches.

## 11. Authentication patterns

Two patterns cover almost every API: **in-house OAuth2 + JWT** for single-service deployments, **external IdP** (Keycloak / Auth0 / Cognito / Entra) for multi-service, MFA, social login, or SSO/compliance needs. Full reference — Argon2id, HS256→RS256 switching, refresh-token rotation + reuse detection, JWKS verification with cached keys, mandatory `aud`/`iss` checks, when to switch A→B, per-endpoint authorization — in [AUTH_PATTERNS.md](AUTH_PATTERNS.md).

Framework-specific implementation:

- [fastapi-architect §6](../../frameworks/fastapi-architect/SKILL.md#6-authentication--authorization) — `OAuth2PasswordBearer` + `pyjwt` + `argon2-cffi`
- [gin-architect §7](../../frameworks/gin-architect/SKILL.md#7-authentication--authorization) — `golang-jwt/jwt/v5` + `argon2`
- [nethttp-architect §8](../../frameworks/nethttp-architect/SKILL.md#8-authentication--authorization) — same Go libs, stdlib middleware shape

## 12. Content negotiation & encoding

- **`Content-Type: application/json; charset=utf-8`** for request and response bodies.
- **`Accept: application/json`** assumed; servers may return `application/problem+json` for errors regardless of `Accept`.
- **JSON field names: `snake_case`.** Matches Python and Go server conventions; client-side translation is trivial.
- **Timestamps: ISO 8601 with timezone**, always as a string. `"2026-05-20T14:23:00Z"` or `"2026-05-20T14:23:00+00:00"`. Never Unix epoch numbers — they're ambiguous about units (seconds vs ms) and harder to log-grep.
- **Decimals as strings** for money (`"99.99"`) — JSON numbers are floats and lose precision.
- **UUIDs as canonical hex strings with dashes** (`"01j9x...-..."`). UUID v7 by default (sortable, distributed) — matches [sql-architect](../../databases/sql-architect/SKILL.md).
- **`null` is intentional absence; missing field is "not provided"** — these mean different things in `PATCH`. Document the distinction.

## 13. Caching

- **`Cache-Control` on every response.** Defaults: `private, no-store` for authenticated user data; `public, max-age=300` for genuinely public reference data (e.g. countries).
- **ETag enables conditional GET** (§9) — clients automatically reuse cached responses with a `304`.
- **`Vary: Authorization, Accept-Encoding`** when responses differ by these — without `Vary`, intermediaries serve the wrong cached entry to a different user.

## 14. Rate limiting

- **`429 Too Many Requests`** when the limit is hit.
- **`RateLimit-Limit` / `RateLimit-Remaining` / `RateLimit-Reset`** on every response; **`Retry-After`** on `429` and `503`. Header reference in [PAYLOADS § 4](PAYLOADS.md#4-rate-limit-headers).
- **Limit per *caller*** (API key, user id), not per IP — IPs aren't reliable identity.

## 15. OpenAPI as the source of truth

- **OpenAPI 3.1** spec is the contract. Every endpoint, every model, every error code, every header documented.
- **Generated from the code, not hand-written** — frameworks (FastAPI, gin-openapi, etc.) emit it from the route definitions. Hand-written specs rot the day after they ship.
- **CI snapshot-tests the spec** — diff against `openapi.snapshot.json` on every PR; any change is reviewed.
- **CI lints the spec with `redocly lint`** — catches missing descriptions, broken `$ref`s, and style violations before the diff review even starts.
- **Spec is published** at a stable URL (e.g. `/v1/openapi.json`) and consumed by client-SDK generators, Postman collections, and API documentation tooling.
- **Rendered docs UI is project-dependent** — [Scalar](https://github.com/scalar/scalar) is a good modern default (open-source, fast, themeable), but Redoc, Swagger UI, or a generated static site are equally valid depending on the project's constraints.
- **Examples on every model and parameter.** They drive the rendered docs and seed mock servers.

## What this skill does NOT cover

- **Framework specifics** (`Depends`, `gin.Context`, middleware ordering) — see the framework architect skills.
- **Auth scheme deep dives** (OAuth2 flows, OIDC, IdPs) — see the framework auth sections.
- **Database access patterns** — see [sql-architect](../../databases/sql-architect/SKILL.md).
- **HATEOAS / HAL / JSON-API** — out of scope; this skill defines plain JSON REST.
