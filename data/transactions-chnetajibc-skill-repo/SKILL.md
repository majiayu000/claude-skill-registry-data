---
name: transactions
description: "Transactions: multi-table writes atomic, idempotent writes, no check-then-act races. Use pessimistic locking tests with concurrent workers where needed."
---

# transactions

Atomicity is a design choice, not a default: short transactions, explicit isolation, tested concurrency.

## Activate when

- Multi-row writes, money/inventory/booking flows, queue-claim patterns, or any check-then-act logic.

## Do NOT activate for

- Single-row CRUD (still validate, but no ceremony); migration mechanics (see migrations).

## Inspection

Trace the write path: which rows change, what is read-then-written, what runs concurrently, what happens on partial failure.

## Decision rules

- All-or-nothing units in one transaction; keep them short (no network calls inside).
- Check-then-act is a race: use constraints (unique/conditional), atomic updates, or explicit locking (`FOR UPDATE`, advisory locks, `SKIP LOCKED` for queues).
- Idempotency keys on retried mutations so replays are safe.
- Isolation chosen per anomaly tolerated (read-committed default; higher only with measured need); optimistic versioning where contention is low, pessimistic where it is proven.

## Procedure

1. Draw the unit of atomicity; shrink it until short.
2. Replace races with constraints/atomic ops/locks; add idempotency keys.
3. Test with concurrent workers hammering the same rows (double-spend/double-claim must fail).
4. Verify: partial-failure drill (kill mid-transaction → consistent state), concurrency test green, lock waits monitored.

## Failure modes

- Long transactions holding locks across HTTP calls; phantom reads billed twice; queue double-processing; deadlocks from inconsistent lock order.

## Escalation

Engine locking specifics → databases/postgres-operations, mysql; saga/outbox across services → distributed/systems.

## References

- Related: `../database-design/`, `../migrations/`, `../../databases/fundamentals/`.
