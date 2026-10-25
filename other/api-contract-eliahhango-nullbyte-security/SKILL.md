---
name: api-contract
description: Design or change an HTTP or RPC API with explicit resources, errors, idempotency, authorization, versioning and contract tests.
---

# API contract: design the stable boundary first

- Model resources and operations before writing handlers. Name the stable identifiers, ownership rules and lifecycle transitions.
- Define success and error shapes once. Use consistent status codes and a machine-readable error code; do not leak stack traces.
- Make retries safe: idempotency keys for creates, predictable pagination, and no side effects on GET.
- Specify authentication and object-level authorization for every operation, including list and export paths.
- Version compatibility deliberately. Additive changes first; deprecate with a window and a migration path.
- Write contract tests against the schema and the authorization matrix, not just the happy-path response.
- Document limits, timeouts and rate-limit behaviour where clients can observe them.

---

_NullByte skill pack. Original guidance for this tool; no third-party skill text is bundled._
