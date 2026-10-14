---
name: database-design
description: "Database design: EXPLAIN-first, schema+queries+indexes together, transactions, bounded background work, soft vs hard delete with cascades."
---

# database-design

Schema, queries, and indexes ship together — proven by EXPLAIN, not by intuition.

## Activate when

- Designing tables, indexes, migrations, or reviewing data-layer changes (any engine).

## Do NOT activate for

- Engine operations (see databases/postgres-operations, mysql, redis, mongodb); credential/role design (see databases/database-security).

## Procedure

1. Model access patterns first, then schema; separate domain, persistence, and DTO models.
2. Write the query, EXPLAIN it, add the index the plan needs, re-run to confirm.
3. Transactions: multi-table writes atomic and idempotent; background work in bounded transactions.
4. Deletion: soft when audit/restoration matters, else hard with documented cascades.
5. Migrations: expand→migrate→contract with down-paths (see backend/migrations).
6. Verify: EXPLAIN evidence, migration up+down on scratch, concurrency test where locking is used.

## Failure modes

- Indexes guessed without EXPLAIN; N+1 on the hot path; unbounded pagination; soft-delete breaking uniqueness; migration without a down-path rehearsed on copy.

## Escalation

- Engine specifics → databases/postgres-operations, mysql; roles → databases/database-security.
