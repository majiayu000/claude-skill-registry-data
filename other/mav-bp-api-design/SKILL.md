---
name: mav-bp-api-design
description: API design conventions for projects with API surfaces. Covers REST and GraphQL standards, versioning, error formats, pagination, documentation as code, and backwards compatibility. Applied when designing, implementing, or reviewing APIs.
user-invocable: false
disable-model-invocation: true
---

# API Design Standards

Ensure all APIs (REST, GraphQL, or any other surface) are consistent, predictable, documented as code, and backwards compatible by default.

## Maverick's Rules

- **Backwards compatible by default** — additions are safe; removing/renaming fields, changing types or semantics, making optional fields required, changing URL structure, or removing endpoints requires a version bump. Support at minimum the current and previous version. Deprecate before removal: mark in the spec, send `Deprecation`/`Sunset` headers, log usage, communicate a timeline, remove only at zero usage.
- **One versioning strategy per project** (URL path or Accept header), applied consistently; increment only for breaking changes.
- **Consistent error envelope on every error**: machine-readable `code` (a string constant, not the HTTP status), user-safe `message`, optional field-level `details`, and a `correlationId`. Never expose stack traces, internal paths, or implementation details.
- **Documentation generated from source** — OpenAPI generated from or validated against code; GraphQL via introspection. Never a separately maintained wiki (it drifts). Include examples, auth requirements, rate limits, and error codes.
- **Pagination on every list endpoint** — cursor-based preferred (opaque cursors, `cursor` + `limit` params, documented maximum); offset-based only for small, stable datasets needing random page access.
- **Rate limiting on all public endpoints** — return `429`, include `X-RateLimit-*` and `Retry-After` headers, apply per-tier limits, document them.
- **Idempotency**: `PUT`/`DELETE` idempotent by design; `POST` operations that must be idempotent (e.g., payments) require an `Idempotency-Key` header with cached-response replay and a TTL. Document which endpoints support it.
- **Validate at the boundary** before business logic runs; reject unexpected fields rather than silently ignoring them; enforce size limits. See `mav-bp-application-security`.
- **GraphQL specifics**: fields non-nullable by default (nullable only when absence is a valid state); enforce query depth/complexity limits; DataLoader or equivalent for N+1 prevention; persisted queries in production where possible.

## Project Implementation Lookup

Check for `docs/maverick/skills/api-design/SKILL.md`. If present, read it and follow it — it wins on specifics (library, config, conventions). If missing, proceed with these standards and note the gap in your summary.

## Detecting API Issues in Code Review

When reviewing code, flag these patterns:

| Pattern                                            | Issue                              | Fix                                                    |
| -------------------------------------------------- | ---------------------------------- | ------------------------------------------------------ |
| Verbs in URL paths (`/getUser`, `/createOrder`)    | REST anti-pattern                  | Use nouns with HTTP methods                            |
| `200 OK` returned for error conditions             | Incorrect status code              | Use appropriate 4xx/5xx codes                          |
| No input validation on request handlers            | Security and data integrity risk   | Validate at the boundary                               |
| Stack traces or internal paths in error responses  | Information disclosure             | Use standard error format, log details server-side     |
| Inconsistent field naming (camelCase vs snake_case)| Breaks predictability              | Pick one convention and apply everywhere               |
| Missing pagination on list endpoints               | Performance risk at scale          | Add cursor or offset pagination                        |
| Breaking change without version bump               | Backwards compatibility violation  | Bump version or make the change additive               |
| No rate limiting on public endpoints               | Abuse and availability risk        | Implement rate limiting with appropriate headers       |
| No idempotency on payment/financial endpoints      | Duplicate processing risk          | Require idempotency keys                               |
| API docs maintained separately from code           | Documentation drift                | Generate docs from source (OpenAPI, introspection)     |

<!-- maverick-plugin-version: 4.0.2-dev -->
