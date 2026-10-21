---
name: api-testing
description: Verify API contracts against a real controlled service. Triggers on "test API", "API 测试".
---

# API Testing Patterns

## When to use

- Verify API contracts against a real controlled service.

**Not for:** api-design for defining contracts; e2e-testing for UI journeys.

## Steps

1. Identify protocol, contracts, authorized environment, isolated data and tooling.

2. Exercise actual requests, authentication, ownership, invalid input and lifecycle; check GraphQL transport and operation errors.

3. Test relevant pagination, concurrency and repeated requests using the contract idempotency mechanism, not tracing headers.

4. Run, inspect logs and clean only test-owned state; determine whether failures violate tests or implementation from contract evidence.

## Verify

- Real service success and failure match contracts; cleanup is scoped and mock results are not labelled integration.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [references/templates/api-test-scaffold.md](references/templates/api-test-scaffold.md) — REST API test scaffold template (Jest/Supertest)
