---
name: api-design
description: Define a consumer-facing API contract with consistent behavior. Triggers on "design API", "接口设计".
---

# API and Interface Design

## When to use

- Define a consumer-facing API contract with consistent behavior.

**Not for:** api-testing for contract verification.

## Steps

1. Identify consumers, protocol, operations and trust boundaries; follow project contract tooling.

2. Specify requests, responses, authentication, authorization, validation and errors; distinguish malformed input from semantic invalidity.

3. Define pagination, concurrency, idempotency and evolution only where needed; include normal and failure examples.

4. Update the authoritative schema or approved contract document; validate schemas and consumer examples before human review.

**Output:** Suggested paths, subject to [human audit](../../../references/human-audit.md): `docs/API/*.md` or the authoritative machine-readable contract.

## Verify

- Examples match the schema; authorization, errors and repeat-request behavior are testable.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [human-audit.md](../../../references/human-audit.md) — document consent, readability and human review.
- [references/versioning-strategy.md](references/versioning-strategy.md) — when breaking change is unavoidable: URI/header versioning, sunset/deprecation headers (RFC 8594), dual-version coexistence, sunset timeline
- [references/openapi-lifecycle.md](references/openapi-lifecycle.md) — design-first vs code-first, Spectral/Redocly linting, openapi-generator SDK generation, spec versioning, CI pipeline
