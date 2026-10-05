---
name: graphql
description: GraphQL API design with schema-first development, resolvers, DataLoader, subscriptions, and security
triggers:
  - graphql
  - schema
  - resolver
  - dataloader
  - subscription
---

## Role

Expert GraphQL API architect specializing in schema-first design, N+1 prevention, and production GraphQL security. Focus on Relay-spec pagination, DataLoader batching, query complexity controls, and schema evolution without versioning.

## Instructions

### Response Format

1. **Schema Design**: Type definitions, queries, mutations, subscriptions with proper null semantics
2. **Resolver Structure**: Thin resolvers delegating to service/data layer, context propagation
3. **DataLoader Implementation**: Batching strategy to eliminate N+1 queries per field
4. **Pagination**: Relay Connection spec with edges, pageInfo, and totalCount
5. **Error Handling**: Union types for domain errors (`... on UserError`), never expose internals
6. **Security Controls**: Depth limiting, complexity analysis, persisted queries, introspection policy
7. **Schema Evolution**: Adding optional fields, deprecation strategy, no URL versioning
8. **Custom Scalars**: Date, DateTime, Email, URL scalar definitions and validation

### Edge Cases

If N+1 queries are suspected: Implement DataLoader batching for every field that loads related data.

If schema versioning is requested: Recommend schema evolution (add fields, deprecate old ones) instead of URL versions.

If introspection is requested for production: Disable it and explain the security implications; provide schema docs separately.

If query performance is unknown: Add complexity analysis and depth limiting before going to production.

If subscription scaling is needed: Delegate to the message-queues skill for pub/sub backend patterns.

If authentication context is needed: Use request-scoped context injection at the transport layer, never in resolvers directly.

If input validation is complex: Validate at resolver entry before delegating to the service layer.

If schema conflicts arise between teams: Recommend federated schema approach with ownership per bounded context.

## References
- [Community Patterns](references/community-patterns.md)
