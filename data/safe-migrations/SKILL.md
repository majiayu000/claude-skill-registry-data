---
name: safe-migrations
description: This skill should be used when the user mentions "migration", "schema change", "zero downtime", "add column", "alter table", "add index", "lock", "expand contract", "backfill", "ALTER COLUMN", "NOT NULL", "CREATE INDEX", or rewriting a DDL change to avoid downtime. It provides the expand-contract (parallel-change) methodology and a per-dialect catalog of which DDL operations take blocking locks and their safe alternatives.
---

# Safe Migrations

## Purpose
Provide a standardized, static methodology for turning a hazardous schema migration into a safe, reversible, zero-downtime change, without a database connection. The core idea: most outages come from a DDL statement that takes a long-held **ACCESS EXCLUSIVE** (Postgres) or table-copy (MySQL) lock and blocks all traffic while it rewrites the table. The fix is almost always the same shape, so this skill encodes it once.

## The Expand-Contract (Parallel-Change) Principle
Never change a schema object in place while the app runs. Instead, evolve in additive steps so old and new code both work at every moment:

1. **Expand**: add the new structure (nullable column, new index built concurrently, `NOT VALID` constraint) without touching existing behavior.
2. **Migrate**: backfill data in bounded batches; dual-write from the app so old and new stay consistent.
3. **Contract**: once all deploys read the new structure, remove the old one in a *later* deploy.

Each step is independently deployable and reversible. A rename or type change is never one migration, it is a sequence spanning multiple deploys.

## The Golden Rules
- Add columns **nullable**; never `NOT NULL DEFAULT <volatile>` in one shot on a large table.
- Build indexes **concurrently** (Postgres) or **in place, lock-free** (MySQL); otherwise use an online-DDL tool.
- Add constraints as **`NOT VALID`** first, then **`VALIDATE`** in a separate statement (short lock, then a scan that does not block writes).
- **Backfill in batches** with a bound and a throttle, never one unbounded `UPDATE`.
- Set **`lock_timeout`** so a migration that cannot acquire its lock fails fast instead of queuing behind long transactions and blocking everything behind *it*.
- Every migration ships a working **DOWN**; splits ship in the correct **order**.

## Quick Hazard Reference

| Operation | Postgres lock | Safe alternative |
|---|---|---|
| `ADD COLUMN` (nullable, no default) | Brief `ACCESS EXCLUSIVE`, metadata-only | Safe as-is |
| `ADD COLUMN NOT NULL DEFAULT <volatile>` | Full rewrite under `ACCESS EXCLUSIVE` | Nullable add → backfill → `NOT VALID` check → validate |
| `CREATE INDEX` | `SHARE` (blocks writes) | `CREATE INDEX CONCURRENTLY` |
| `ALTER COLUMN TYPE` | Full rewrite under `ACCESS EXCLUSIVE` | New column → dual-write → backfill → swap |
| `ADD FOREIGN KEY` | `SHARE ROW EXCLUSIVE`, scans child | `... NOT VALID` then `VALIDATE CONSTRAINT` |
| `SET NOT NULL` | `ACCESS EXCLUSIVE` + full scan | Backing `CHECK ... NOT VALID` + validate, then set |
| Rename / drop column | `ACCESS EXCLUSIVE` + breaks old code | Multi-deploy expand-contract |

## Additional Resources
### Reference Files
- **`references/postgres-locks.md`**: the full Postgres DDL → lock-level → safe-alternative catalog, including `NOT VALID`/`VALIDATE`, `CONCURRENTLY`, and `lock_timeout`/`statement_timeout` guidance.
- **`references/mysql-locks.md`**: MySQL/InnoDB online-DDL `ALGORITHM`/`LOCK` matrix, when to reach for gh-ost / pt-online-schema-change, and how it differs from Postgres.
- **`references/expand-contract-patterns.md`**: step-by-step multi-deploy recipes: add-not-null-column, rename-column, change-type, split-table, and batched backfill.
