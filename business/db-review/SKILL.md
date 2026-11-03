---
name: db-review
description: Review database schemas, queries, and migrations for correctness, performance, and safety. Always use this skill when designing a schema, writing or optimizing a query, planning a migration, choosing indexes, or when the user asks about query performance, index strategy, ALTER TABLE safety, migration locking, composite indexes, or says "review this schema", "is this query efficient", "is this migration safe", "will this lock the table", "what index should I add", or "help me design this table". Read this skill before recommending any schema change or index.
---

# DB Review

Database decisions are expensive to reverse. A bad schema survives for years; a migration that locks a table in production wakes someone up at 2am. Get these right up front.

## Schema design

**Name things precisely.** Table names are plural nouns (`users`, `orders`). Column names are unambiguous: `created_at` not `date`, `user_id` not `id` (when it's a foreign key). Avoid abbreviations: disk is cheap, confusion is expensive.

**Every table needs:**

- A surrogate primary key (auto-increment integer or UUID). Use UUID if records will be referenced across services or exported. Use integer if joins and index size matter more.
- `created_at` timestamp (non-nullable, defaulting to `now()`)
- `updated_at` timestamp if records are ever modified

**Nullable columns are a code smell when overused.** A nullable column says "this might not have a value"; make sure that's true semantically, not just a convenience for lazy inserts. Nullable foreign keys often signal a model problem.

**Soft deletes (`deleted_at`)**: use them when you need an audit trail or the ability to restore. Be aware that every query now needs a `WHERE deleted_at IS NULL` clause. This is easy to forget and must be enforced at the ORM/query layer, not ad hoc.

**Normalization**: start normalized (3NF). Denormalize only when you have a measured query performance problem that normalization is causing, not in anticipation of one.

## Indexing strategy

Indexes speed up reads and slow down writes. Don't add indexes speculatively; add them when you have evidence a query is slow and the index would help.

**Always index:**

- Foreign keys (the database does not do this automatically in most engines)
- Columns used in `WHERE`, `ORDER BY`, or `JOIN` conditions for frequent queries

**Index composition:** a composite index `(a, b, c)` supports queries filtering on `a`, `a+b`, or `a+b+c`, but not `b` alone. Put the most selective column first, unless a range condition on another column makes a different order faster.

**Partial indexes**: when you frequently query a subset of rows (e.g., `WHERE status = 'pending'`), a partial index on that subset is much smaller and faster than a full-column index.

**Unique constraints vs unique indexes**: use a unique constraint to enforce business rules (the database enforces it regardless of application logic). A unique index gives you the same enforcement with slightly different semantics; prefer the constraint.

**Watch for index bloat on high-write tables.** Indexes on frequently-updated or frequently-deleted tables accumulate dead entries. VACUUM (Postgres) or equivalent maintenance matters.

## Query review

**Read EXPLAIN ANALYZE output, not just EXPLAIN.** `EXPLAIN` shows the plan; `EXPLAIN ANALYZE` shows what actually happened, including rows scanned vs rows estimated. Surprises between estimated and actual row counts often indicate stale statistics.

**What to look for in a query plan:**

- Sequential scan on a large table: almost always means a missing index
- Nested loop join on large result sets: can be catastrophic; consider hash join or restructuring
- High row estimate errors: run `ANALYZE` to update statistics
- Sort operations without an index: consider an index on the ORDER BY columns

**N+1 queries**: the classic ORM trap. If you load 100 orders and then execute a query per order to get line items, you've done 101 queries instead of 2. Detect by logging query counts per request. Fix with eager loading or a JOIN.

**Avoid `SELECT *`** in application code. It retrieves columns you don't need (wasting bandwidth and memory), and silently breaks when columns are added or reordered in some ORMs.

**Transactions and lock scope**: keep transactions short. A transaction that holds a lock while waiting for user input, a slow external call, or a long computation will cause contention. Do the work, then commit.

## Migration safety

This is where production incidents live. A migration that works fine on a development database can lock a 500M-row table in production for minutes.

**The lock question**: DDL statements (adding columns, adding indexes, altering types) acquire table locks in most databases. On a large table under traffic, this can cause a request queue to pile up behind the lock.

Safe patterns (Postgres):

- **Add a nullable column**: safe, no table rewrite, no lock beyond metadata
- **Add a column with a default**: in Postgres 11+, adding a nullable column with a constant default is safe (stored in metadata, not written row-by-row). Older versions: add nullable first, backfill, then add default.
- **Add an index**: use `CREATE INDEX CONCURRENTLY`. Takes longer but doesn't block reads or writes.
- **Drop a column**: mark it ignored in the application first (stop reading/writing it), deploy, then drop. Never drop a column the running application is still referencing.
- **Rename a column**: this is a breaking change. The safe path is to add the new column, dual-write to both, migrate reads to the new column, deploy, then drop the old one. Four steps, not one.
- **Change a column type**: almost always requires a table rewrite. Plan for a maintenance window or use a shadow-column approach.

**Backward compatibility**: after a migration deploys, the old app version is still running (rolling deploys, multiple instances). The schema must work with both the old and new code simultaneously until all instances are updated. A column the old code writes to must still exist; a column the new code reads must be present before the new code deploys.

**Rollback plan**: every migration needs one. "Re-run the old binary" is not a rollback plan if the migration already ran. For additive migrations (new columns, new tables), rollback is dropping the addition. For destructive migrations (dropping columns, changing types), rollback requires restoring from backup or a shadow-column approach.

**Test migrations on a production-like dataset.** A migration that takes 10ms on 10k rows can take 45 minutes on 500M rows. Run `EXPLAIN` on the migration SQL and time it on a data sample before touching production.

## Data integrity

**Use database constraints, not just application validation.** Constraints are enforced even when the application has bugs, when someone runs a migration script directly, or when a new service starts writing to the same table.

Essential constraints:

- `NOT NULL` on columns that must always have a value
- `FOREIGN KEY` with appropriate `ON DELETE` behavior (`CASCADE`, `RESTRICT`, or `SET NULL`; be deliberate)
- `UNIQUE` on columns or combinations that must be unique
- `CHECK` constraints for simple domain rules (e.g., `price > 0`, `status IN ('active', 'inactive')`)

**Enum types vs lookup tables**: enum columns are fast but painful to extend (adding a value is a DDL operation). A lookup table is more flexible and can store metadata. Use enums for truly stable, small sets; lookup tables for anything that might grow.
