---
name: graphql
description: Use when adding or changing a GraphQL type, field, query, mutation, input, enum or scalar in a Polyforms Pothos schema, or deprecating one. The long form of stack rules 09-backend and 11-ops (API evolution).
---

# Change the GraphQL API

Domain first, schema second: the domain is the source of truth.

## Where things go

`server/domain/<domain>/infrastructure/graphql/` holds `enums.ts`, `types.ts`, `inputs.ts`,
`queries.ts`, `mutations.ts`, each imported in order by `server/domain/shared/graphql/schema.ts`
(a lender before a borrower). One endpoint, `POST /graphql`.

## A scalar per brand

```ts
// builder.ts: Scalars: { Quantity: { Input: Quantity; Output: Quantity } }
// scalars.ts
scalar('Quantity', 'How many, 1 to 999. Example: 3.', Quantity)
```

The scalar reuses the brand's constructor: an invalid value is a `BAD_USER_INPUT` before the
resolver runs, and resolvers never call a constructor themselves.

## Types, queries, mutations

```ts
export const OrderType = builder.objectRef<Order>('Order').implement({
  description: 'One order of the signed-in user.',
  fields: (t) => ({
    id: t.expose('id', { type: 'OrderId', description: 'Opaque identifier.' }),
    note: t.exposeString('note', { nullable: true, description: 'Absent when none was written.' }),
  }),
})

builder.mutationField('placeOrder', (t) =>
  t.field({
    type: OrderType,
    description: 'Place an order. Fails with LIMIT_REACHED past the monthly limit.',
    args: { quantity: t.arg({ type: 'Quantity', required: true, description: 'How many.' }) },
    resolve: async (_root, { quantity }, { userId }) =>
      match(await OrderCommand.place(userId, quantity))
        .with('limit-reached', () => domainError('LIMIT_REACHED', 'Monthly limit reached'))
        .with(P.not(P.string), (order) => order)
        .exhaustive(),
  }),
)
```

- Every type, field, argument and enum value has a description: it is the documentation
  the app developer reads.
- Nullability is off by default: a field that may be absent says `nullable: true`.
- Outcomes map with `match().exhaustive()`; `notFound`, `badUserInput`, `forbidden`,
  `domainError(code, message)` from `shared/graphql/errors.ts`. A consultation that finds
  nothing answers `null`.
- Optional inputs pass through `stripNulls` before the domain.
- A nested field that needs another document: denormalise it on the parent, or add a
  per-request loader to the context before shipping it. Never one read per parent row.

## After a change

```bash
bun run generate:graphql      # shared/schema.graphql, committed whole, never hunk-split
bun run schema:check          # refuses a breaking change that was not deprecated
bun run ios:codegen           # when the app uses it
```

## Deprecate, never remove

When the app stops using a field or an argument, in the same commit:

```ts
oldField: t.exposeString('old', {
  deprecationReason: 'since 1.3 (2026-10-21): use newField',
  description: '...',
})
```

The monthly deprecations routine removes it once a build without it has been on sale for
fourteen days and raises the build floor. Never remove by hand, never raise the floor by hand.
Adding a field, a query, a mutation, an optional argument or an enum value needs nothing.
