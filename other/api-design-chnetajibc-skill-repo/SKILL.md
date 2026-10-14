---
name: api-design
description: "API contract design: resources, error envelopes, pagination, versioning, evolution. Use when shaping a new API surface or reviewing contract changes. Implementation protocols live in backend/api-design."
---

# api-design

Contracts first: one canonical resource model, one error envelope, versioning with an evolution policy.
## Inspection

List endpoints, resources, error shapes, pagination schemes, versioning in use, and who calls them (internal teams, external clients, future-you).

## Decision rules

Contract-first for shared surfaces; additive evolution by default; version only on breaking change; one error envelope and one pagination scheme repo-wide.


## Activate when

- Designing or reviewing an API surface, error model, pagination, or versioning strategy.

## Do NOT activate for

- Transport implementation (REST/GraphQL/gRPC/SSE/webhooks, retries, breakers) — see `../../backend/api-design/`.
- Access-control review — see `../../backend/api-security/`.

## Procedure

1. Resources: nouns not verbs; one canonical URL per resource; nesting max two levels.
2. Errors: single RFC-7807-shaped envelope repo-wide; clients branch on stable `type`, never on `detail` text.
3. Pagination: cursor-based for mutable/large datasets (opaque cursor + `next_cursor`); offset only for small immutable lists.
4. Idempotency: mutation endpoints accept idempotency keys where retries are possible.
5. Evolution: additive first; version (`/v1`, headers, or negotiation) with deprecation headers, sunset dates, and migration notes; apply Hyrum's Law — every observable behavior is a dependency.
6. Verify: contract tests for envelope + pagination + version negotiation; changelog entry for any surface change.

## Failure modes

Second error shape; offset pagination on mutable datasets; version bump without migration notes; convenience aliases multiplying auth surface.

## Escalation

Compat disputes → backend/api-design; access-control review → backend/api-security.
