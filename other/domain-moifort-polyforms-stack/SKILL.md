---
name: domain
description: Use when creating or changing a backend domain (types, primitives, command, query, repository, business rules, use case, migration) in a Polyforms Nitro + Firestore project. The long form of stack rule 09-backend.
---

# Create or change a domain

The `user` domain under `server/domain/user/` is the reference: copy its shape.

## 1. Files

```
server/domain/<domain>/
  types.ts            branded types and the aggregate; the file IS the spec of the model
  primitives.ts       one Zod constructor per brand
  command.ts          writes, bare exported functions
  query.ts            reads, bare exported functions
  business-rules.ts   optional: pure functions, no I/O, full coverage
  use-case.ts         optional: orchestration across domains, no business logic of its own
  infrastructure/
    repository.ts     the only file that touches Firestore
    graphql/{enums,types,inputs,queries,mutations}.ts
```

Callers import a module under the domain's name: `import * as OrderCommand from
'~/domain/order/command'`, then `OrderCommand.place(...)`. Never a TypeScript `namespace`.

## 2. Types and primitives

```ts
// types.ts
import type { Brand } from 'ts-brand'
import type { UserId } from '~/domain/shared/types'

export type OrderId = Brand<string, 'OrderId'>
export type Quantity = Brand<number, 'Quantity'>

export type Order = {
  id: OrderId
  userId: UserId          // every private document names its owner
  quantity: Quantity
  note?: string           // absence is an optional field, never null
  createdAt: Date
}

// primitives.ts
export const Quantity = (value: unknown) =>
  make<QuantityType>()(z.number().int().min(1).max(999).parse(value))
```

Never `as Quantity` on untrusted input: the constructor. Generic brands (`UserId`, `Count`,
`Eur`, `Year`, `Day`) come from `~/domain/shared`.

## 3. Repository

```ts
const orders = () => db().collection('orders').withConverter(genericDataConverter<Order>())

export const findAllByUser = (userId: UserId): Promise<Order[]> =>
  memoizedPerRequest(`order:all:${userId}`, async () =>
    (await orders().where('userId', '==', userId).get()).docs.map((doc) => doc.data()),
  )

export const save = async (order: Order) => {
  await orders().doc(order.id).set(withoutAbsentFields(order))
  evictFromRequestCache(`order:all:${order.userId}`)
  return order
}
```

- Flat collections, `userId` on every private document, every query filters on it.
- A memoised read is evicted or revised by every write under its key.
- Several writes: `atomically(batch => ...)`; read-modify-write: `transactionally(tx => ...)`;
  mass delete: `deleteInBatches`.
- Filter, sort and page in Firestore. A new composite query adds its index to
  `firestore.indexes.json` in the same commit.

## 4. Query and command

```ts
// query.ts
export const byId = async (userId: UserId, id: OrderId) => {
  const order = await repository.findBy(userId, id)
  if (!order) return 'not-found' as const
  return order
}

// command.ts
export const place = async (userId: UserId, quantity: Quantity) => {
  if (await isOverLimit(userId)) return 'limit-reached' as const
  return repository.save({ id: OrderId(randomUUID()), userId, quantity, createdAt: new Date() })
}
```

One literal per expected failure, `as const`; `throw` only for an impossible state. A
function's name is the business concept (`place`, not `createOrder`, never `handleX`).

## 5. Account deletion

A domain with private documents exports `deleteAllForUser(userId)` from its command and adds
it to the parallel block of `server/domain/user/use-case.ts`.

## 6. Tests

| File | What it proves |
|---|---|
| `primitives.unit.test.ts`, `business-rules.unit.test.ts` | Every rule, every boundary |
| `command.int.test.ts`, `query.int.test.ts` | Through the real repository against the fake Firestore; read budgets with `fake.docReads` and `fake.queryReads` |
| `infrastructure/graphql/*.feat.test.ts` | The API contract: answer shape and values, error codes, read budget |

```ts
mock.module('~/system/firebase', () => ({ db: fakeDb }))
const OrderCommand = await import('~/domain/order/command')
```

Dates are asserted with `toEqual` on the field, never inside `toMatchObject`. Run the three
families separately.

## 7. Migration

Renaming, restructuring, changing enum values or removing data needs a migration:
`server/system/migration/migrations/NNN-<what-it-does>.ts` exporting a `Migration`
(`version`, `name`, `migrate({ db })` returning `{ ok: true, transformed }`), its
`.int.test.ts` against the fake Firestore, and its line in `migrations/index.ts`. Idempotent:
run twice, it changes nothing the second time. The Deploy workflow runs it; never by hand.

## Checklist

- [ ] Types branded, absence optional, `userId` on private documents
- [ ] One constructor per brand, one GraphQL scalar per brand (graphql skill)
- [ ] Repository private, memoised reads evicted on write
- [ ] Outcomes as literals, mapped exhaustively in the resolver
- [ ] `deleteAllForUser` wired into account deletion
- [ ] Indexes added for new queries
- [ ] Unit, int and feat tests, read budgets asserted
- [ ] `bun run generate:graphql`, `bun run schema:check`, preflight green
