---
name: graphql
description: Use when designing or operating a GraphQL API. Covers schema design, resolver performance and DataLoader batching, query cost limiting, error handling, and federation.
metadata:
  category: backend
  version: 1.0.0
  tags: [graphql, schema, dataloader, federation, performance]
---

# GraphQL

## Purpose

Design a GraphQL schema that models the domain rather than the database, and operate it without letting a single query take down the service.

## When to Use

- Designing a GraphQL schema from scratch.
- Diagnosing slow queries or N+1 resolver behavior.
- Protecting a public GraphQL endpoint from expensive queries.
- Splitting a schema across services with federation.

## Capabilities

- Schema design: types, interfaces, unions, connections, nullability.
- Resolver architecture and DataLoader batching.
- Query cost analysis, depth limiting, and persisted queries.
- Error handling that distinguishes partial failures from total ones.
- Federation and schema composition.

## Inputs

- The domain model and the client's actual query patterns.
- The data sources behind each field.
- Whether the endpoint is public (untrusted queries) or internal.

## Outputs

- A schema with deliberate nullability and stable field names.
- Resolvers that batch, with no N+1 on any documented query.
- Cost limits and a persisted-query allow-list for public endpoints.

## Workflow

1. **Design for the client, not the tables** — The schema is a product surface. If it mirrors your database, you have built a slower REST API with worse caching.
2. **Get nullability right early** — A nullable field is a permanent client burden; a non-null field that later fails takes down the whole parent object. Non-null for genuine invariants only.
3. **Batch every relation** — Every resolver that fetches by id gets a DataLoader. Without one, `orders { customer { name } }` issues one query per order.
4. **Bound the cost** — Depth limit, complexity limit, and pagination caps. Then persisted queries for first-party clients.
5. **Model errors explicitly** — Expected failures (validation, not found) belong in the schema as union results; unexpected failures go to `errors`.

## Best Practices

- Never expose an unbounded list field. Use the Connection pattern with a `first`/`after` cap.
- `DataLoader` instances are per-request. A shared loader is a cache-poisoning bug across users.
- Changing a field from nullable to non-null is a breaking change for clients that handle null; the reverse is breaking for clients that do not. Get it right before launch.
- Do not version a GraphQL schema. Add fields, deprecate old ones with `@deprecated(reason:)`, and remove them once usage reaches zero.
- Instrument per-field resolver latency. The slow field is never the one you would guess.
- Introspection on a public production endpoint is a reconnaissance gift. Disable it or restrict it.

## Examples

**DataLoader eliminating an N+1:**

```typescript
// Without a loader: 1 query for orders, then N queries for customers.
const resolvers = {
  Order: {
    customer: (order, _args, ctx) => ctx.loaders.customer.load(order.customerId),
  },
};

// The loader batches every customerId requested in the same tick into one query.
export function createLoaders(db: Db) {
  return {
    customer: new DataLoader<string, Customer>(async (ids) => {
      const rows = await db.customers.findMany({ where: { id: { in: [...ids] } } });
      const byId = new Map(rows.map((r) => [r.id, r]));
      return ids.map((id) => byId.get(id) ?? new Error(`Customer ${id} not found`));
    }),
  };
}
```

**Expected failures modeled in the schema:**

```graphql
union CreateOrderResult = Order | ValidationFailed | InsufficientInventory

type Mutation {
  createOrder(input: CreateOrderInput!): CreateOrderResult!
}
```

The client must handle each outcome. Business failures no longer masquerade as transport errors.

## Notes

- Query complexity limits must be tuned against real queries, not guessed. Log the complexity of every production query for a week before enforcing a ceiling.
- Federation solves an organizational problem (independent teams owning parts of the graph), not a technical one. If one team owns the whole schema, a single service is simpler.
- GraphQL over HTTP GET with persisted queries restores CDN caching, which naive POST-based GraphQL throws away.
