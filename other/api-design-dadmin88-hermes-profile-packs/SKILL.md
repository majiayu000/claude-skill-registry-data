---
name: api-design
description: Design or evolve a backend API with explicit contracts, protocol semantics, compatibility, authorization boundaries, failure behavior, and consumer validation.
---
# API Design

Use when adding, changing, or reviewing an API or service interface owned by the backend.

## Procedure
1. Identify the consumers, the user or system capability being exposed, the current contract, and any compatibility constraints before choosing endpoint shapes.
2. Model the operation in domain terms first. Do not let transport objects become the domain model by accident.
3. Follow the repository's established protocol and conventions unless there is a concrete reason to change them. For HTTP, GraphQL, RPC, events, or another protocol, use that protocol's semantics rather than forcing REST conventions everywhere.
4. Specify inputs, outputs, authentication context, authorization expectations, validation, error semantics, and observable side effects. Mark optionality and nullability explicitly.
5. For collections or long-running operations, define pagination or streaming, ordering, filtering, idempotency, concurrency behavior, cancellation, and status retrieval where they matter.
6. Define failure behavior deliberately. Separate client errors, authorization failures, conflicts, dependency failures, retryable failures, and unexpected server failures without leaking secrets or internal implementation details.
7. Evaluate compatibility from the consumer's perspective. Treat field additions, default changes, ordering changes, error changes, and timing changes as potentially breaking when consumers can observe them.
8. Record the contract using the project's normal mechanism such as OpenAPI, GraphQL schema, protobuf/IDL, typed interfaces, examples, or contract fixtures.
9. Validate representative success, boundary, unauthorized, invalid, conflict, and dependency-failure cases. Use contract or consumer tests when the interface crosses a meaningful ownership boundary.

## Decision rules
- Prefer a small coherent interface over exposing persistence models or internal implementation structure.
- Do not invent a new version merely to avoid thinking through compatibility, and do not assume an additive change is automatically safe.
- Make retry and idempotency semantics explicit for operations that can be repeated or partially fail.
- If the change creates a new trust boundary or authorization model, hand the security decision to `agency-security-engineer` and implement the accepted design.

## Quality gate
The API is ready when a consumer can implement against the contract without hidden assumptions, important failure and compatibility behavior is explicit, and executable validation proves the contract that matters.