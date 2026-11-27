---
name: api-contracts
description: "Review public API contracts for REST, pagination, versioning, ProblemDetails, authentication and compatibility."
---

# API contract review
- List consumers, actors, operations, privacy and tenancy. Identify command intent and read projection boundaries.
- Stable route/resource/verb semantics and problem details error codes; do not return raw exceptions.
- Request validation, bound pagination, deterministic ordering, version strategy, idempotency keys and conditional updates where needed.
- Document auth/authz per operation, quotas/rate limits, failure/retry semantics and OpenAPI examples.
- Add contract tests for known consumer and error flows; security tests including IDOR and tenant crossing.
- Preserve backward compatibility or plan explicit deprecation/migration.
