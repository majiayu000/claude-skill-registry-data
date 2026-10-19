---
name: database-migrations
description: Plan, write, review and roll out relational database schema and data migrations without downtime or data loss - expand/contract sequencing, lock-level analysis, batched backfills, rollback and forward-fix plans, migration-tool hygiene. Concrete lock and rewrite rules for PostgreSQL 14-18 (CREATE INDEX CONCURRENTLY, NOT VALID constraints, lock_timeout), with general guidance for MySQL and other engines. Use when adding, renaming or dropping columns or tables, changing types, adding indexes, constraints or foreign keys, splitting tables, backfilling data, or reviewing a migration file or pull request. Not for query tuning (postgresql-performance), schema design or JSONB/RLS (postgresql-development), SQL authoring (sql-development), or document/search stores (mongodb-development, elasticsearch-search).
compatibility: Tool-agnostic (Flyway, Liquibase, Alembic, Rails, Prisma, golang-migrate, plain SQL). Lock tables verified against the PostgreSQL 18 ALTER TABLE and CREATE INDEX manuals; the same rules hold for 14-17 except where marked. Never run against production without explicit authorization.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "migrations, schema, postgresql, zero-downtime, expand-contract, backfill, locks"
  topics: "databases, deployment, release-engineering"
---

# Database Migrations

A migration is a production change that cannot be recompiled away. The two questions for every statement: **what lock does it take and for how long**, and **can the previous application version still run against the new schema**.

## Scope and boundaries

- This skill: changing schema/data safely and reviewing migrations.
- `postgresql-performance`: deciding *which* index to add and why. `postgresql-development`: schema design. `sql-development`: SQL authoring. `release-engineering`: deploy pipelines in general. `secrets-management`: connection credentials.

## Non-negotiable rules

1. **Do not execute migrations against production, staging shared by others, or any database the user has not named.** Produce files and a runbook; run only against a local/disposable database unless explicitly authorized. Never print connection strings or credentials.
2. **No destructive step (DROP COLUMN/TABLE, TRUNCATE, type narrowing, deleting rows) without a verified backup/restore path and a separate, later release** after nothing reads the object. State the data-loss consequence in the migration comment and the PR.
3. **Every migration states its lock and duration risk.** On PostgreSQL set `lock_timeout` for DDL so a blocked statement fails fast instead of queueing behind a long transaction and then blocking all traffic behind itself.
4. **One concern per migration file**, immutable once merged/applied anywhere. Fix mistakes with a new migration, never by editing history.
5. **Schema and data changes are separate steps.** Large backfills run outside the DDL transaction, in batches, resumable and idempotent.
6. **Application and schema deploy in compatible order** (expand, migrate, contract). Both the old and new code must work against the intermediate schema.

## Workflow

### 1. Classify the change
| Change | Risk | Pattern |
|---|---|---|
| New nullable column | Low | Add, deploy code, backfill |
| New NOT NULL column | Medium | Add nullable (+default), backfill, add constraint safely |
| Rename column/table | High (breaks old code) | Expand/contract with dual-write or view; avoid direct RENAME |
| Change type | High (rewrite) | New column, backfill, switch, drop later |
| Add index | Medium (lock/IO) | `CREATE INDEX CONCURRENTLY` |
| Add FK / CHECK / NOT NULL | Medium (scan under lock) | `NOT VALID` then `VALIDATE` |
| Drop column/table | High (irreversible) | Stop reads/writes first; drop in a later release |
| Large backfill | Medium (load, bloat, replication lag) | Batched job |

### 2. Know the PostgreSQL lock rules (PG 14-18)
From the manual (PG 18 ALTER TABLE page): unless stated, `ALTER TABLE` takes `ACCESS EXCLUSIVE`, which blocks reads and writes; with several subcommands the strictest lock wins.

- `ADD COLUMN` with a **non-volatile** default (including `now()`, constants): metadata only, no rewrite (PG 11+). A **volatile** default (`random()`, `clock_timestamp()`), an identity column, or a stored generated column forces a full table rewrite. Virtual generated columns (PG 18) never rewrite.
- `ALTER COLUMN TYPE`: normally rewrites table and indexes and may need up to double the disk space; no rewrite only for binary-coercible changes without `USING` (the manual's example is `text` to `varchar`; narrowing a length limit still scans). Run `ANALYZE` afterwards. Rewriting forms are not MVCC-safe for old snapshots.
- `ADD CONSTRAINT ... NOT VALID` (CHECK): takes `ACCESS EXCLUSIVE` briefly but skips the scan. `ADD FOREIGN KEY ... NOT VALID`: `SHARE ROW EXCLUSIVE` on both tables. `VALIDATE CONSTRAINT`: `SHARE UPDATE EXCLUSIVE` (plus `ROW SHARE` on the referenced table for FKs), so reads and writes continue while it scans.
- `SET NOT NULL` scans the table unless a valid `CHECK (col IS NOT NULL)` exists; use the check-then-set trick (below). PG 18 also accepts `NOT NULL ... NOT VALID`.
- `CREATE INDEX` (non-concurrent): `SHARE` lock, blocks writes. `CREATE INDEX CONCURRENTLY`: does not block writes; two table scans; cannot run inside a transaction block; one concurrent build per table; unsupported directly on partitioned tables. Recipe: `CREATE INDEX parent_idx ON ONLY parent (col);` (creates an invalid parent index, no build), then `CREATE INDEX CONCURRENTLY part_idx ON part1 (col);` on each partition, then `ALTER INDEX parent_idx ATTACH PARTITION part_idx;` for each; the parent index becomes valid once every partition has one attached. On failure it leaves an `INVALID` index that still costs writes: drop it and retry, or `REINDEX INDEX CONCURRENTLY`.
- `DETACH PARTITION ... CONCURRENTLY`: two transactions, cannot run in a transaction block, not allowed with a default partition; finish an interrupted one with `FINALIZE`.
- `DROP COLUMN` is fast (marks dropped) but takes `ACCESS EXCLUSIVE` and breaks any reader still selecting it.
- `NOT ENFORCED` constraints (PG 18) skip verification and cannot be validated; do not use as a substitute for a real constraint.

Full table, with MySQL notes: [references/lock-cheatsheet.md](references/lock-cheatsheet.md).

### 3. Use expand / migrate / contract
1. **Expand**: add the new structure (nullable column, new table, new index) - additive, backwards compatible.
2. **Dual-write / read-new-fallback-old**: deploy application code that writes both and reads the new with fallback. A trigger can mirror writes if the application cannot be changed yet; remove it in contract.
3. **Backfill** existing rows in batches (step 5).
4. **Switch reads**, verify equality with a query, monitor.
5. **Contract**: after at least one full release in which nothing references the old object, drop it in its own migration.

Rename example: add `full_name`, dual-write, backfill, switch reads, later drop `name`. A direct `RENAME COLUMN` is only safe when no running code version references the old name.

### 4. Write the migration defensively (PostgreSQL)
Most migration tools wrap each file in one transaction, and locks are held until commit. If `ADD CONSTRAINT ... NOT VALID` and `VALIDATE CONSTRAINT` run in the same transaction, the brief `ACCESS EXCLUSIVE` lock from the first statement is still held during the scan of the second, which defeats the pattern. Put each step in its own transaction (separate migration files, or one file with transaction wrapping disabled and autocommit between statements).
```sql
-- File 1: 20261015_01_add_orders_status_check.sql  (illustrative)
SET lock_timeout = '3s';          -- fail fast rather than queue
-- Brief ACCESS EXCLUSIVE, no scan; commits immediately
ALTER TABLE orders ADD CONSTRAINT orders_status_nn CHECK (status IS NOT NULL) NOT VALID;

-- File 2: 20261015_02_validate_orders_status_check.sql
SET lock_timeout = '3s';
SET statement_timeout = '15min';  -- bound the scan deliberately
-- Scan under SHARE UPDATE EXCLUSIVE; writes continue
ALTER TABLE orders VALIDATE CONSTRAINT orders_status_nn;

-- File 3: 20261015_03_orders_status_set_not_null.sql
SET lock_timeout = '3s';
-- ACCESS EXCLUSIVE but no full scan, because the valid CHECK proves it
ALTER TABLE orders ALTER COLUMN status SET NOT NULL;
-- optional cleanup of the redundant CHECK (same file is fine)
ALTER TABLE orders DROP CONSTRAINT orders_status_nn;
```
Index in its own file/transaction-free migration (many tools need a flag to disable the wrapping transaction, for example `-- +goose NO TRANSACTION`, Flyway `executeInTransaction=false`, Alembic `autocommit_block()`; check your tool's current docs):
```sql
SET lock_timeout = '3s';
CREATE INDEX CONCURRENTLY IF NOT EXISTS orders_customer_idx ON orders (customer_id);
-- verify: SELECT indexrelid::regclass, indisvalid FROM pg_index WHERE indexrelid = 'orders_customer_idx'::regclass;
```
Retries after `lock_timeout` failures are expected: retry off-peak, and check for long-running transactions first (`pg_stat_activity`, see `postgresql-performance`).

### 5. Backfill in batches
Requirements: idempotent, resumable, bounded batch size, sleeps/throttles on replication lag, runs outside the DDL transaction, progress logged.

```sql
-- repeat until 0 rows updated; run from a job, not one giant statement
UPDATE orders SET status_v2 = status
WHERE id IN (
  SELECT id FROM orders
  WHERE status_v2 IS NULL AND status IS NOT NULL   -- rows with a NULL source never match, so the loop can end
  ORDER BY id LIMIT 5000 FOR UPDATE SKIP LOCKED
);
```
Notes: one massive UPDATE bloats the table (dead tuples, needs vacuum), holds locks, and can lag replicas. Keep the predicate (`status_v2 IS NULL`) indexed or iterate by primary-key ranges. Without the `status IS NOT NULL` guard, rows whose source is NULL would be selected forever (the update leaves `status_v2` NULL), so the loop would never reach 0 rows. Autovacuum may need tuning for the duration. Verify with counts and checksums before switching reads.

### 6. Plan rollback honestly
- Additive changes: rollback is dropping them (still safe only before code depends on them).
- Destructive or lossy changes have **no rollback**; the plan is backup restore or forward-fix. Say that in the PR.
- Down migrations that were never exercised are fiction. Test up, down (if you ship one) and re-up on a copy.
- Prefer feature flags for behaviour, migrations for structure.

### 7. Test and review
- Run all migrations from scratch on an empty database and from the last release's schema on a production-shaped copy; time the risky steps on realistic row counts.
- Compare resulting schema with the intended (schema dump diff). Check indexes valid, constraints validated.
- Review checklist below. Ask: what happens if this blocks for 60 seconds? If the app rolls back mid-way? If the migration is run twice?

## Worked example: make `users.email` NOT NULL and unique, case-insensitively

1. Expand: `ALTER TABLE users ADD COLUMN email_norm text;` (nullable, metadata-only).
2. Deploy code that writes `email_norm = lower(email)` on every insert/update.
3. Backfill in 5,000-row batches by id range; log progress.
4. Detect conflicts before the unique index: `SELECT email_norm, count(*) FROM users GROUP BY 1 HAVING count(*) > 1;` Resolve duplicates with the product owner (merging users is a data decision, not a migration decision).
5. `CREATE UNIQUE INDEX CONCURRENTLY users_email_norm_key ON users (email_norm);` (a uniqueness violation makes the build fail and leave an INVALID index: drop and retry after fixing data).
6. Add the NOT NULL via CHECK NOT VALID, VALIDATE, SET NOT NULL, each in its own transaction (separate files; see step 4 of the workflow).
7. Switch lookups to `email_norm`. Later release: drop old index/column if superseded.

## Anti-patterns

- Editing an applied migration, or "squashing" history that production has already run.
- `ALTER TABLE ... ADD COLUMN ... DEFAULT <volatile>` or `SET NOT NULL` on a huge hot table in one step.
- `CREATE INDEX` without CONCURRENTLY on a live table; CONCURRENTLY inside a transaction (it errors).
- No `lock_timeout`: a blocked `ACCESS EXCLUSIVE` request queues behind a long transaction and every later query queues behind it.
- Data migration and schema migration in one transaction; unbounded `UPDATE`.
- Auto-generated ORM migrations applied without reading the SQL they emit.
- Dropping in the same release that stops using the object.
- Migrations that import application models/code (they break when the models change); use frozen SQL or minimal local definitions.
- Claiming a down migration works when it was never run.

## Verification checklist

- [ ] Each statement's lock mode and rewrite behaviour identified for the stated engine/version
- [ ] `lock_timeout` set (PostgreSQL) and retry plan documented
- [ ] Old and new application versions both work at every intermediate state
- [ ] Index builds concurrent, outside transaction wrappers, validity checked afterwards
- [ ] Constraints added NOT VALID then validated, with ADD, VALIDATE and SET NOT NULL in separate transactions, or justified otherwise
- [ ] Backfill batched, idempotent, resumable, throttled, verified
- [ ] Destructive steps deferred to a later release with backup/restore noted
- [ ] Tested from scratch and on production-shaped data; timings recorded
- [ ] Not executed against production without explicit authorization

## References

- [references/lock-cheatsheet.md](references/lock-cheatsheet.md) - PostgreSQL lock modes per operation, MySQL/InnoDB notes
- [references/scenarios.md](references/scenarios.md) - evaluation scenarios
- [references/sources.md](references/sources.md) - sources and provenance
