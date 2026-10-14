---
name: api-design
description: "Implement backend APIs: REST/GraphQL/gRPC/WebSocket/SSE/webhooks, auth, pagination, idempotency, retries, versioning, docs. Use when building or changing endpoints. Contract theory lives in architecture/api-design."
---

# api-design

Implement the contract: correct semantics per protocol, hardened edges, documented and tested behavior.

## Activate when

- Building or modifying endpoints, handlers, webhooks, or streaming APIs.

## Do NOT activate for

- Contract shaping/versioning policy — see `../../architecture/api-design/`.
- Authorization review — see `../api-security/`.

## Procedure

1. Protocol: REST by default; GraphQL for client-shaped reads, gRPC for service-to-service, WebSocket/SSE for push, webhooks for outbound events (idempotent receivers, signed, retried with backoff).
2. Semantics: correct status codes, ETags/conditional requests where caching matters, cursor pagination per contract.
3. Edges: runtime validation at boundaries, authn/authz on every route, rate limits, timeouts; retries with jitter + budgets, circuit breakers on dependencies.
4. Compatibility: additive changes; breaking changes versioned with migration notes and contract tests.
5. Docs: OpenAPI (or schema registry for GraphQL/gRPC) generated from code, with examples; every error `type` documented.
6. Verify: protocol-level tests (happy, validation, authz-cross-user, pagination, idempotent-retry, webhook-replay) green; docs render.
