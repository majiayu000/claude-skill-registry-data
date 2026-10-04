---
name: stock-operation-scaffold
description: Use when adding or modifying a stock-mutating operation in services/app/src/modules/stock (or any new module that reads/writes stock_movements balance) — new movement type, new transfer-like flow, new perishable/batch handling, or touching entries.ts/exits.ts/transfers.ts/sales.ts/nfe-import.ts. Also use when reviewing a PR that adds a function calling tx.stockMovement.create or nextBalanceAfter.
---

# Stock Operation Scaffold

## Overview

Every operation in `services/app/src/modules/stock` that reads the current stock balance and
then writes a new `stock_movements` row follows one exact shape:
`withTenant(tenantId, tx => { lockStockRow FIRST; business logic; recordAudit; return result })`.
This is not stylistic — it is the fix for CR-1, a Critical lost-update/TOCTOU race this project's
HARDEN pass found and fixed (see `services/app/src/modules/stock/balance.ts` header comment and
`tests/integration/stock-concurrency.test.ts`). Skipping `lockStockRow` reintroduces that exact
bug: two concurrent requests both read the same stale balance before either commits, so both can
"succeed" while the derived balance ends up wrong, and both can pass a stock-sufficiency check
that should have failed the second one (oversell).

## When to Use

- Adding a new stock movement type (new file in `modules/stock/`, or a new function in an
  existing one like `entries.ts`/`exits.ts`/`transfers.ts`).
- Adding stock mutation to a new module outside `modules/stock` (e.g. a future returns/adjustment
  flow) that will call `tx.stockMovement.create` or read balance via `getCurrentStock`.
- Reviewing any diff that touches `nextBalanceAfter`, `tx.stockMovement.create`, or `tx.batch.*`.

## The Pattern (evidence: entries.ts, exits.ts, transfers.ts)

```ts
import { recordAudit, withTenant } from "@estoque-saas/shared";
import { lockStockRow, nextBalanceAfter } from "./balance";

export async function doSomeStockOp(tenantId: string, userId: string, input: SomeInput) {
  return withTenant(tenantId, async (tx) => {
    // 1. LOCK FIRST -- before any read of the current balance, before any sufficiency check.
    //    pg_advisory_xact_lock(hashtext(tenantId || productId || storeId)) -- auto-released on
    //    commit/rollback, never needs manual unlock. Serializes only operations on the SAME
    //    (tenant, product, store) triple; different products/stores never block each other.
    await lockStockRow(tx, tenantId, input.productId, input.storeId);

    // 2. Business logic -- sufficiency checks, batch/FEFO resolution (resolveExitLines for
    //    perishables per ADR-006), whatever this operation needs. Safe now: no other transaction
    //    can be mid-flight on this same (tenant, product, store) triple.
    const balanceAfter = await nextBalanceAfter(tx, input.productId, input.storeId, delta);

    // 3. Write the movement -- balance_after is stored ON the row (stock isn't materialized in
    //    its own table; current balance = balance_after of the most recent movement for that
    //    (product, store) pair -- see balance.ts's getCurrentStock doc comment).
    const movement = await tx.stockMovement.create({ data: { tenantId, productId: input.productId, storeId: input.storeId, type: "...", quantity: delta, createdBy: userId, balanceAfter } });

    // 4. ALWAYS recordAudit -- every stock mutation is audited (ADR-007, immutable audit log:
    //    no UPDATE/DELETE grant on audit_log, enforced at the DB role level, verified in
    //    tests/integration/audit-log.test.ts).
    await recordAudit(tx, { tenantId, userId, entityType: "stock_movement", entityId: movement.id, action: "create", after: { /* ... */ } });

    return { movementId: movement.id, balanceAfter };
  });
}
```

## Multi-Store Operations: Deterministic Lock Ordering

If the operation touches TWO (product, store) pairs in the same transaction (transfers are the
only current example, `transfers.ts` `transferOneItem`), lock BOTH before doing anything else,
in a **deterministic order independent of which store is "origin" vs "destination"** -- sort by
`storeId` and lock the lexicographically smaller one first:

```ts
const [firstStoreId, secondStoreId] =
  originStoreId < destinationStoreId ? [originStoreId, destinationStoreId] : [destinationStoreId, originStoreId];
await lockStockRow(tx, tenantId, item.productId, firstStoreId);
await lockStockRow(tx, tenantId, item.productId, secondStoreId);
```

Locking in caller-supplied order (origin-then-destination always) deadlocks: two concurrent
transfers between the same two stores in opposite directions would each hold one lock and wait
on the other's. Sorting by a fixed key makes every transaction acquire locks in the same global
order.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Calling `getCurrentStock`/sufficiency check before `lockStockRow` | Lock is ALWAYS the first line inside `withTenant`'s callback -- even before "cheap" reads |
| Locking origin-then-destination in caller order for a two-store op | Sort by `storeId` (or any fixed key) so all callers lock in the same global order |
| Writing `stock_movements` without `recordAudit` | Every mutation is audited -- copy the `recordAudit` call shape from `entries.ts` |
| Adding a new balance read outside `balance.ts`'s helpers | Reuse `getCurrentStock`/`getCurrentStockForProducts` (batched, HI-1 N+1 fix) -- don't hand-roll `DISTINCT ON` queries elsewhere |
| Forgetting `resolveExitLines`/FEFO for perishable products | Any outbound movement (exit/transfer/sale) for a perishable product must go through `resolve-batches.ts`'s FEFO resolution (ADR-006), not decrement an arbitrary batch |
