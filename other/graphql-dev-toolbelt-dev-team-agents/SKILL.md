---
name: graphql
description: GraphQL — schema, resolvers, N+1/DataLoader, pagination.
---

# GraphQL

## Detection Signals

Load this skill when any of the following are present:

| Signal | Location |
|--------|----------|
| `graphql` or `@graphql-tools/*` dependency | `package.json` |
| `.graphql` / `.gql` schema files | anywhere in the repository |
| `apollo-server`, `graphql-yoga`, `mercurius` | `package.json` |
| `strawberry-graphql`, `ariadne`, `graphene` | `pyproject.toml`, `requirements.txt` |
| `gqlgen`, `graphql-go` | `go.mod` |
| `async-graphql`, `juniper` | `Cargo.toml` |
| `webonyx/graphql-php`, `lighthouse` | `composer.json` |
| `GRAPHQL_ENDPOINT` env var | `.env`, `.env.example` |
| `/graphql` route | routing config |
| `ApolloClient`, `urql`, `graphql-request` | frontend dependencies |

---

## Schema-First vs Code-First

**Detect which approach the project uses before writing any schema or resolver:**

| Signal | Approach |
|--------|----------|
| `.graphql` / `.gql` files are the source of truth | Schema-first |
| Schema generated from code annotations / decorators | Code-first |

- **Schema-first**: SDL (Schema Definition Language) files are committed; resolvers implement the contract.
- **Code-first**: resolvers are annotated and the schema is generated at build time.

**Do not mix approaches.** Follow whichever the project already uses.

---

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Types | `PascalCase` | `User`, `OrderItem` |
| Fields | `camelCase` | `createdAt`, `totalAmount` |
| Queries | `camelCase` verb-noun | `user(id)`, `listOrders` |
| Mutations | `camelCase` action-noun | `createUser`, `updateOrder`, `deleteProduct` |
| Subscriptions | `camelCase` event | `orderStatusChanged`, `messageReceived` |
| Enums | `SCREAMING_SNAKE_CASE` values | `ORDER_STATUS_PENDING` |
| Input types | `[Action][Type]Input` | `CreateUserInput`, `UpdateOrderInput` |

**Never expose internal database column names directly** — map them to clean field names in the schema.

---

## Core Rules

These decide the shape of the work. The full patterns and code live in the references below.

| Area | Rule |
|---|---|
| Nullability | Mark a field non-null (`!`) only when the server truly guarantees a value |
| Mutation arguments | Wrap in a single `input` object; return the mutated entity in the payload |
| Business errors | Return them as data (`errors: [UserError!]!`), not as top-level GraphQL errors |
| Related data | Never fetch it in a resolver without a per-request DataLoader — this is the default source of N+1 |
| Collections | Never return an unbounded list; paginate (cursor-based for anything that can grow) |
| Subscriptions | Filter server-side and enforce the same auth rules as queries |
| Query hardening | Depth and complexity limits configured; introspection disabled in production |

---

## References

| File | Load when |
|---|---|
| `references/schema-and-operations.md` | Writing queries, mutations, pagination, or subscriptions — full SDL patterns |
| `references/resolvers-and-errors.md` | Writing or reviewing resolvers — DataLoader batching, error taxonomy, query-level security |

---

## What to Do Before Declaring Done

- [ ] No resolver fetches related data without going through a DataLoader
- [ ] All list fields are paginated
- [ ] Mutation payloads return the mutated entity
- [ ] Business errors use the `errors: [UserError!]!` pattern
- [ ] Subscriptions filter server-side
- [ ] Introspection disabled in production config
- [ ] Depth/complexity limits configured
