---
name: api-design-review
description: Design or review HTTP, RPC, or library APIs for stable contracts and predictable behavior. Use when adding endpoints or changing public interfaces.
---

# API Design Review

Review the contract from the perspective of its callers and operators.

1. Define resource/operation semantics, identifiers, input schema, output schema, and expected state transitions.
2. Make validation and error behavior consistent, actionable, and safe to expose.
3. Check authentication, authorization, rate limits, idempotency, pagination, filtering, and concurrency where relevant.
4. Consider backwards compatibility, versioning, deprecation, retries, timeouts, and partial failures.
5. Avoid leaking internal implementation details or sensitive data through responses and logs.
6. Provide examples for success, validation failure, authorization failure, and important boundary cases.
7. Verify the contract against actual implementation and tests.

Prefer stable, boring contracts over clever ones. Do not add fields or endpoints for hypothetical consumers. Distinguish breaking changes from additive changes and identify the migration required for each affected client.
