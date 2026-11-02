---
name: api-design
description: |-
  Use when designing, reviewing, or planning REST or GraphQL APIs — endpoint structure, schema design, versioning, error handling, pagination, URI naming, or choosing between REST and GraphQL. Also triggers for OpenAPI spec creation and API contract review.
---

# API Design

## When to Use

- Designing new API endpoints or schemas
- Reviewing existing API contracts for consistency
- Choosing between REST and GraphQL for a project
- Planning versioning, pagination, or error handling strategies
- Creating or reviewing OpenAPI/GraphQL specifications
- Naming URIs, fields, or resources
- Reviewing API security posture

**When NOT to use:**

- Framework-specific implementation details (though FastAPI patterns are available as a secondary reference below)
- Database schema design (unless it directly affects the API contract)
- Frontend data fetching code (unless reviewing the API contract it consumes)

## Invocation Notice

- Tell the user when this skill is running: `api-design`.
  Skip the notice when the user asked for the skill by name or slash command; spelling and spacing need not match.
  A phrase from this skill's own trigger list is not a name — naming the work is not naming the skill.

## Universal Principles

These apply regardless of REST or GraphQL:

1. **Prefer design-first for public, cross-team, or governance-heavy APIs.**
   Write the contract (OpenAPI spec or GraphQL schema) before implementation.
   Code-first is the normal workflow for frameworks like FastAPI that generate the contract from code, and is acceptable for rapid prototypes or internal tools with stable requirements.
   The choice is driven by governance needs, not protocol correctness.
2. **Consistency is non-negotiable.**
   Pick conventions and apply them uniformly across every endpoint, field, and error response.
3. **API surface is not database surface.**
   Never mirror internal data models in public contracts.
   Abstract so you can change internals without breaking clients.
   See [rest-design.md § API Surface Is Not Database Surface](references/rest-design.md) for rationale, anti-patterns, and decoupling strategies.
4. **Validate and shape at the boundary.**
   Enforce input constraints and response shaping at the API boundary.
   Authenticate before business logic runs.
   As a strong default, keep fine-grained authorization policy in the domain/business layer — but coarse access control (e.g., "only authenticated users") is legitimately enforced in gateways or middleware before the domain layer.
5. **Evolve without breaking.**
   Hyrum's Law: with enough users, every observable behavior of your API — including undocumented quirks, error message text, and field ordering — becomes a de facto contract someone depends on.
   Design with that in mind: be intentional about what you expose, and treat any change as potentially breaking until proven otherwise.
   Additive changes are usually safe, but verify compatibility against clients — adding a GraphQL enum value is schema-safe yet can surprise clients that assume exhaustive handling.
   Removal, renaming, and type changes require versioning (REST) or deprecation workflows (GraphQL).
6. **Security is structural.**
   HTTPS, authentication, authorization, rate limiting, and input validation are not optional additions — they are part of the design.

Use the references below as scoped guidance.
Some references describe broad consensus, while others document strong defaults or ecosystem-specific patterns.

## Route by Task

| Design Task                          | Reference                                                     | When to Load                                               |
| ------------------------------------ | ------------------------------------------------------------- | ---------------------------------------------------------- |
| REST vs GraphQL decision             | [rest-vs-graphql.md](references/rest-vs-graphql.md)           | Starting a new API or evaluating a paradigm shift          |
| REST endpoint design                 | [rest-design.md](references/rest-design.md)                   | Designing REST resources, methods, status codes            |
| GraphQL schema/query/mutation design | [graphql-design.md](references/graphql-design.md)             | Designing GraphQL types, queries, mutations, subscriptions |
| URI/URL naming                       | [uri-design.md](references/uri-design.md)                     | Naming endpoints, path segments, query parameters          |
| API versioning                       | [versioning.md](references/versioning.md)                     | Planning version strategy, deprecation, migration          |
| Error responses                      | [error-handling.md](references/error-handling.md)             | Designing error formats, status code usage, RFC 9457       |
| Pagination and filtering             | [pagination-filtering.md](references/pagination-filtering.md) | Lists, collections, search results, sorting                |
| FastAPI implementation               | [fastapi-practices.md](references/fastapi-practices.md)       | Building APIs with FastAPI specifically                    |

**How to use this table:** Load only the references relevant to the current task.
For a new API design, start with `rest-vs-graphql.md`, then load the paradigm-specific reference.
For targeted questions (e.g., "how should we version this?"), load only that reference.

## Quick Decision: REST vs GraphQL

- **REST:** simpler caching, lower learning curve, native file uploads, smaller security surface.
- **GraphQL:** client-specified queries, nested data without over-fetching, built-in subscriptions — but requires depth/cost limiting, custom caching, and more schema governance.
- **Hybrid:** can work, but increases operational and governance complexity.
- **Caution:** GraphQL was not designed for file uploads; use multipart workarounds or a separate REST endpoint.
  REST requires careful endpoint design to avoid N+1 orchestration.

For the full decision tree and tradeoff matrix, load [rest-vs-graphql.md](references/rest-vs-graphql.md).

## Common Mistakes

| Mistake                                                    | Fix                                                                                                                                                          |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Verbs in REST URIs (`/getUsers`, `/createOrder`)           | Use nouns + HTTP methods for CRUD; verbs only for [controller resources](references/rest-design.md) (`POST /orders/{id}/cancel`)                             |
| Exposing database IDs/structure in API                     | Abstract with slugs, UUIDs, and [domain-oriented shapes](references/rest-design.md); use a mapping layer, not auto-serialization                             |
| Inconsistent error formats across endpoints                | Define one error schema, use it everywhere                                                                                                                   |
| No pagination on collection endpoints                      | Paginate unbounded or growth-prone collections; small bounded reference data may not need it — always set default and max page sizes when pagination is used |
| Breaking changes without versioning                        | Use additive changes; version when breaking is unavoidable                                                                                                   |
| Generic GraphQL mutations (`updateEntity`)                 | Use specific semantic mutations (`publishPost`, `archiveOrder`)                                                                                              |
| Auth logic in resolvers/handlers instead of business layer | Delegate authorization to domain services                                                                                                                    |
| Nullable everything / non-null everything                  | Be intentional: non-null only when you can guarantee presence                                                                                                |
