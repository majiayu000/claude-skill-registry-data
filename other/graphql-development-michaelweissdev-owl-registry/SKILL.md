---
name: graphql-development
description: >
  Architect, implement, secure, and optimize production GraphQL APIs using Schema Definition
  Language (SDL), resolver design, DataLoader batching for N+1 prevention, cursor-based
  pagination, input validation, and defensive complexity controls. Use when designing
  GraphQL schemas, building query and mutation resolvers, eliminating N+1 database queries,
  implementing Relay Connection pagination, handling errors with extensions, or defending
  against denial-of-service through query depth and complexity limiting.
compatibility: >
  Agent Skills-compatible coding agents implementing or querying GraphQL APIs with Node.js, TypeScript, Python, or Go tooling. Tooling is required only for executable validation.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "graphql, api, sdl, dataloader, relay-pagination, resolvers, backend, security"
  topics: "software-development"
---

# GraphQL API Architecture & Engineering

GraphQL is a strongly typed query language and runtime for APIs that lets clients request precisely the data they need. Unlike REST, GraphQL executes queries against a single endpoint through hierarchical resolvers, making predictable execution plans, batching, schema evolution, and query safety critical engineering priorities.

## Purpose & Overview

This skill guides the design, implementation, and hardening of production GraphQL services. It covers schema-first vs code-first workflows, resolver construction, elimination of N+1 query cascades via DataLoader, Relay-compliant cursor pagination, custom scalar validation, structured error reporting, and defensive depth/complexity limits against malicious queries.

---

## Core Principles & Rules

1. **Eliminate N+1 queries with DataLoader**: Never perform database or downstream HTTP lookups inside child field resolvers without batching. Every relation traversal must use a request-scoped DataLoader.
2. **Schema-first SDL or code-first with strict typing**: Keep schema definitions and resolver types aligned. In code-first (e.g., Pothos, Nexus, Strawberry), generate SDL artifacts for review. In schema-first, use code-generation tools (e.g., GraphQL Code Generator) to produce strict TypeScript/Go types.
3. **Favor cursor-based pagination for collections**: Follow the Relay Connection specification (`edges`, `node`, `cursor`, `pageInfo`) for lists that change or scale. Avoid offset/limit pagination on mutable or large datasets.
4. **Mutations must return structured payloads**: Never return a bare boolean or single primitive from a mutation. Always return a payload object containing the modified entity, client mutation ID, and user-facing validation errors (`userErrors`).
5. **Never expose raw database or internal errors**: Catch database and system errors before they reach the GraphQL execution engine. Return domain errors with structured `extensions` (code, field, timestamp) and mask internal stack traces in production.
6. **Enforce query depth and complexity limits**: GraphQL APIs expose arbitrary graph traversals. Always validate query ASTs against maximum depth limits (e.g., 6–10 levels) and cost complexity budgets before execution.
7. **Input validation belongs at the edge**: Use custom scalars (`DateTime`, `EmailAddress`, `PositiveInt`) and input schema validators (Zod, Class-Validator, Pydantic) to reject invalid input before invoking business logic.

---

## Standard Workflows & Procedures

### Workflow 1: Schema-First Design with Code Generation

1. Define canonical types, queries, and mutations in `.graphql` SDL files.
2. Define custom scalars for domain-specific primitives.
3. Configure code generation (e.g., `@graphql-codegen/cli`) to generate resolver signatures and TypeScript models.
4. Implement root and field resolvers matching the generated contracts.

### Workflow 2: Request-Scoped DataLoader Wiring

1. Instantiate DataLoaders inside the per-request GraphQL context function (never as singletons across concurrent requests to avoid cross-tenant data leaks and stale cache poisoning).
2. Wire batch loading functions using primary keys or foreign keys.
3. Pass the dataloader collection via `context.loaders`.

### Workflow 3: Defensive Query Protection Pipeline

1. Install query depth limiting (`graphql-depth-limit`) on the schema validation phase.
2. Calculate query complexity scores based on field weights and list multipliers before execution.
3. Set execution timeouts (e.g., 5 seconds) to terminate runaway resolvers.
4. Disable introspection (`introspection: false`) and schema exploration in public production environments unless explicitly required.

---

## Real-World Examples & Patterns

### 1. Schema Definition Language (SDL) & Mutation Payloads

```graphql
scalar DateTime
scalar EmailAddress

enum OrderStatus {
  PENDING
  PROCESSING
  SHIPPED
  DELIVERED
  CANCELLED
}

interface Node {
  id: ID!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

type OrderEdge {
  cursor: String!
  node: Order!
}

type OrderConnection {
  edges: [OrderEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type User implements Node {
  id: ID!
  email: EmailAddress!
  name: String!
  orders(first: Int = 20, after: String): OrderConnection!
  createdAt: DateTime!
}

type Order implements Node {
  id: ID!
  user: User!
  status: OrderStatus!
  amountInCents: Int!
  createdAt: DateTime!
}

input CreateOrderInput {
  userId: ID!
  amountInCents: Int!
}

type UserError {
  field: [String!]
  message: String!
  code: String!
}

type CreateOrderPayload {
  order: Order
  userErrors: [UserError!]!
}

type Query {
  user(id: ID!): User
  order(id: ID!): Order
}

type Mutation {
  createOrder(input: CreateOrderInput!): CreateOrderPayload!
}
```

### 2. DataLoader Pattern to Eliminate N+1 Queries (TypeScript)

```typescript
import DataLoader from 'dataloader';
import { db } from './database';

export interface GraphQLContext {
  userId?: string;
  loaders: {
    userLoader: DataLoader<string, UserRecord | null>;
    ordersByUserIdLoader: DataLoader<string, OrderRecord[]>;
  };
}

// Request context factory (instantiated per incoming HTTP request)
export function createContext(): GraphQLContext {
  return {
    loaders: {
      userLoader: new DataLoader<string, UserRecord | null>(async (userIds) => {
        const users = await db.users.findMany({
          where: { id: { in: [...userIds] } },
        });
        const userMap = new Map(users.map((u) => [u.id, u]));
        return userIds.map((id) => userMap.get(id) ?? null);
      }),

      ordersByUserIdLoader: new DataLoader<string, OrderRecord[]>(async (userIds) => {
        const orders = await db.orders.findMany({
          where: { userId: { in: [...userIds] } },
          orderBy: { createdAt: 'desc' },
        });
        const grouped = new Map<string, OrderRecord[]>();
        for (const order of orders) {
          const list = grouped.get(order.userId) ?? [];
          list.push(order);
          grouped.set(order.userId, list);
        }
        return userIds.map((id) => grouped.get(id) ?? []);
      }),
    },
  };
}

// Resolvers leveraging DataLoader
export const resolvers = {
  Order: {
    user: async (parent: OrderRecord, _args: unknown, ctx: GraphQLContext) => {
      const user = await ctx.loaders.userLoader.load(parent.userId);
      if (!user) {
        throw new Error(`User ${parent.userId} not found for Order ${parent.id}`);
      }
      return user;
    },
  },
  User: {
    orders: async (parent: UserRecord, args: { first?: number; after?: string }, ctx: GraphQLContext) => {
      const allOrders = await ctx.loaders.ordersByUserIdLoader.load(parent.id);
      return paginateArray(allOrders, args.first ?? 20, args.after);
    },
  },
};
```

### 3. Cursor-Based Pagination Implementation

```typescript
export function paginateArray<T extends { id: string }>(
  items: T[],
  first: number,
  after?: string
) {
  const limit = Math.min(Math.max(first, 1), 100);
  let startIndex = 0;

  if (after) {
    const decodedId = Buffer.from(after, 'base64').toString('utf-8');
    const index = items.findIndex((item) => item.id === decodedId);
    if (index !== -1) {
      startIndex = index + 1;
    }
  }

  const sliced = items.slice(startIndex, startIndex + limit);
  const edges = sliced.map((item) => ({
    cursor: Buffer.from(item.id).toString('base64'),
    node: item,
  }));

  const hasNextPage = startIndex + limit < items.length;
  const hasPreviousPage = startIndex > 0;

  return {
    edges,
    totalCount: items.length,
    pageInfo: {
      hasNextPage,
      hasPreviousPage,
      startCursor: edges[0]?.cursor ?? null,
      endCursor: edges[edges.length - 1]?.cursor ?? null,
    },
  };
}
```

### 4. Structured Error Handling with Extensions

```typescript
import { GraphQLError } from 'graphql';

export class DomainValidationError extends GraphQLError {
  constructor(message: string, field: string, code = 'BAD_USER_INPUT') {
    super(message, {
      extensions: {
        code,
        field,
        timestamp: new Date().toISOString(),
      },
    });
  }
}

export class UnauthorizedError extends GraphQLError {
  constructor(message = 'Authentication required') {
    super(message, {
      extensions: {
        code: 'UNAUTHENTICATED',
        http: { status: 401 },
      },
    });
  }
}

// In Resolver:
export const mutationResolvers = {
  createOrder: async (_root: unknown, { input }: { input: CreateOrderInput }, ctx: GraphQLContext) => {
    if (!ctx.userId) {
      throw new UnauthorizedError();
    }
    if (input.amountInCents <= 0) {
      return {
        order: null,
        userErrors: [{
          field: ['input', 'amountInCents'],
          message: 'Order amount must be greater than zero.',
          code: 'INVALID_AMOUNT',
        }],
      };
    }
    const order = await db.orders.create({ data: input });
    return { order, userErrors: [] };
  },
};
```

### 5. Query Depth & Complexity Limiting

```typescript
import depthLimit from 'graphql-depth-limit';
import { createComplexityLimitRule } from 'graphql-validation-complexity';
import { ApolloServer } from '@apollo/server';

const MAX_QUERY_DEPTH = 6;
const MAX_QUERY_COMPLEXITY = 1000;

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [
    depthLimit(MAX_QUERY_DEPTH),
    createComplexityLimitRule(MAX_QUERY_COMPLEXITY, {
      onCost: (cost) => console.log(`Calculated query cost: ${cost}`),
      formatErrorMessage: (cost) =>
        `Query cost ${cost} exceeds maximum allowed complexity of ${MAX_QUERY_COMPLEXITY}`,
    }),
  ],
});
```

---

## Common Anti-Patterns & Pitfalls

| Anti-Pattern | Why It Fails | Remediated Practice |
|---|---|---|
| **Global DataLoader instance** | Shares cached database records across separate HTTP requests, leaking tenant data and serving stale writes. | Always instantiate DataLoaders inside the per-request context factory function. |
| **Offset/Limit on large collections** | Performance degrades with high offsets (`OFFSET 100000`) and yields duplicate/skipped items on write-heavy tables. | Use Relay-style cursor-based pagination backed by indexed keyset filters (`WHERE id > :cursor`). |
| **Direct database queries in child resolvers** | A query requesting 50 authors and their books issues 51 sequential queries (N+1 cascade), exhausting the pool. | Batch foreign-key lookups through DataLoader batch functions. |
| **Exposing raw internal exceptions** | Database constraint names, SQL statements, and internal server IPs are leaked in the `errors` payload. | Sanitize errors in the formatting pipeline, returning friendly messages and typed `userErrors`. |
| **Unbounded list arguments (`first: 100000`)** | Allows malicious clients to exhaust memory and CPU by fetching entire tables in one query. | Enforce maximum bounds on list arguments (e.g. `Math.min(first, 100)`). |
| **Unprotected recursive schemas** | Circular relationships (`user -> posts -> author -> posts`) enable malicious denial-of-service queries. | Attach query depth limiting and complexity estimation rules to schema validation. |

---

## Verification Checklist

- [ ] Every relation resolver uses a request-scoped DataLoader batch function.
- [ ] DataLoaders are created inside the per-request context, never as modules or singletons.
- [ ] Schema defines custom scalars for dates, emails, and bounded numbers.
- [ ] All collections support cursor-based pagination with `edges`, `node`, `pageInfo`, and an upper limit on `first`.
- [ ] Mutations return a payload type containing the subject entity and a `userErrors` collection.
- [ ] Query depth limiting rule is registered (maximum depth between 5 and 8).
- [ ] Query complexity rule is configured with field weights and array multipliers.
- [ ] Production servers mask internal stack traces and database error messages.
- [ ] Introspection is disabled or secured behind authenticated admin access in production.

---

## Tooling & Reference Guides

- **Schema Tools**: `graphql-tag`, `@graphql-tools/schema`, `@graphql-codegen/cli` for automated TypeScript generation.
- **Batching & Resolvers**: `dataloader` (JavaScript/TypeScript), `strawberry-graphql` with dataloaders (Python), `gqlgen` with dataloaders (Go).
- **Security & Complexity**: `graphql-depth-limit`, `graphql-validation-complexity`, `graphql-armor` for layered defense.
- **Standards**: [GraphQL Specification](https://spec.graphql.org/), [GraphQL Cursor Connections Specification (Relay)](https://relay.dev/graphql/connections.htm).
