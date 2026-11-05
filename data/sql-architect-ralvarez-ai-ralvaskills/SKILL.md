---
name: sql-architect
version: 1.0.1
description: SQL standards — UUID v7 PKs, snake_case, soft delete, forward-only migrations, parameter binding, N+1 prevention, EXPLAIN-driven indexing. PostgreSQL 18 primary; MySQL 9 and SQLite 3.53 noted. Use when designing schemas, writing queries, or auditing a database layer.
---

# SQL Architecture & Database Standards

Targets **PostgreSQL 18** as the primary engine; MySQL 9 and SQLite 3.53 noted where they differ. See [STACK.md](STACK.md) for pinned tool versions.

## 1. Schema design

- **Primary key:** `id UUID PRIMARY KEY DEFAULT uuidv7()` on every table. UUID v7 is sortable, distributed-friendly, and doesn't leak counts via URLs. PG 18 has native `uuidv7()`; on earlier engines use an extension or app-generated UUID v7.
- **Natural identifiers stay UNIQUE:** the surrogate `id` is for joins; domain meaning lives in `UNIQUE` constraints (`email`, `slug`, `iso_code`).
- **Foreign keys:** always declared at the DB level (`REFERENCES other(id) ON DELETE RESTRICT` by default). Never enforce relationships in app code alone.
- **NOT NULL by default.** Make NULL an explicit, justified choice — every nullable column should have a documented reason.
- **CHECK constraints:** push invariants into the DB (`CHECK (price >= 0)`, `CHECK (status IN (...))`). They survive bad code paths.
- **Audit columns (opt-in):** `created_at` + `updated_at` (`timestamptz NOT NULL DEFAULT now()`) on tables whose rows change after creation. Skip on pure lookup tables (`countries`, `currencies`) and event/log tables (where `event_at` alone is enough).
- **Soft delete (default):** `deleted_at timestamptz NULL`. Filter via partial indexes (`CREATE INDEX ... WHERE deleted_at IS NULL`) so queries stay fast. Use **hard delete** only when GDPR/compliance requires it, or for append-only event tables where deletion never makes sense.

## 2. Naming conventions

- **Tables:** `snake_case`, **plural** (`users`, `order_items`).
- **Columns:** `snake_case`, **singular** (`email`, `created_at`).
- **PK:** always `id`.
- **FKs:** `<reftable_singular>_id` (`user_id`, `order_id`).
- **Indexes (PostgreSQL):** `<table>_<cols>_idx`; unique `<table>_<cols>_key`; partial `<table>_<cols>_active_idx` — matches Postgres's own auto-generated names. MySQL and SQLite differ — see [ENGINES.md](ENGINES.md).
- **Constraints:** `<table>_<purpose>_check`, `<table>_<purpose>_fkey`.
- **Sequences:** PG generates them; rename only if necessary, never reference manually — UUID v7 PKs avoid the need.

## 3. Indexing strategy

- **Index every FK column** — JOINs without indexes are silent killers.
- **B-tree** is the default. **GIN** for arrays / JSONB containment. **GiST** for ranges / geometry. **BRIN** for huge append-only tables sorted by time.
- **Composite index column order:** most-selective column first, then by query pattern. The same composite index can serve `WHERE a = ?` and `WHERE a = ? AND b = ?` — but not `WHERE b = ?` alone.
- **Partial indexes** for soft-deleted rows (`... WHERE deleted_at IS NULL`) and other common filters.
- **Don't over-index.** Each index slows writes and consumes RAM. Add one only when `EXPLAIN ANALYZE` proves a real query needs it.
- **Drop unused indexes.** PG: query `pg_stat_user_indexes` periodically; remove any with `idx_scan = 0`.

## 4. Query patterns

- **Parameter binding always.** `WHERE id = $1` — never string-concatenate user input.
- **Explicit columns.** `SELECT id, email, created_at FROM users` — never `SELECT *` in production code (breaks on schema additions, returns extra bytes).
- **`RETURNING` on writes.** `INSERT ... RETURNING id, created_at` saves a round-trip and surfaces server defaults.
- **`ON CONFLICT` for upserts.** `INSERT ... ON CONFLICT (email) DO UPDATE SET ...` — atomic, no race.
- **Pagination = cursor, not OFFSET.** `WHERE (created_at, id) < ($1, $2) ORDER BY created_at DESC, id DESC LIMIT 20`. OFFSET is O(N) on every page.
- **CTEs (`WITH`) for readability**, but be aware PG ≤ 11 materializes them (perf cliff). PG 12+ inlines unless `MATERIALIZED` is forced.

## 5. JOINs & N+1 prevention

- **N+1 is the single most common perf bug.** One query that fetches parents followed by N queries for children = always wrong.
- **Detect it:** log every SQL statement in dev with timings; any list endpoint emitting more than 2–3 queries per request is suspect.
- **Fix it:** single JOIN, or batched `WHERE id IN (...)` for the children, or DataLoader-style batchers if behind an API layer.
- **JOIN vs subquery:** different shapes, similar plans in modern PG — let `EXPLAIN ANALYZE` decide. Prefer JOINs when both sides return many rows; correlated subqueries when the inner table is small or you want a scalar.
- **`LEFT JOIN` only when you genuinely need rows from the left without a match.** A `LEFT JOIN` filtered by `WHERE right.x = ?` silently becomes an INNER JOIN — clearer to write it that way.

## 6. Transactions & isolation

- **Wrap related writes in a transaction.** Anything that must succeed or fail together.
- **Isolation default:** `READ COMMITTED` (PG default). Bump to `REPEATABLE READ` for multi-statement reads that need a consistent snapshot, and `SERIALIZABLE` when reads-then-writes need true linearizability — handle `40001` (serialization failure) by retrying.
- **Keep transactions short.** Holding a transaction across a network call or user input is a deadlock waiting to happen.
- **Advisory locks** (`pg_advisory_lock`) for distributed coordination that doesn't fit a row-level lock — singleton workers, leader election, idempotent jobs.
- **Roll back explicitly on error.** Application drivers should bracket every transaction in begin/commit/rollback — never leak open transactions.

## 7. Migrations

- **Forward-only.** No `down` migrations in production. Revert by writing a new forward migration. Down migrations rot fast and lie about what they restore.
- **Idempotent where possible:** `CREATE TABLE IF NOT EXISTS`, `ADD COLUMN IF NOT EXISTS`. Lets a half-applied migration re-run safely.
- **One change per migration.** Easier to review, easier to revert, atomic in CI.
- **Naming:** `NNNNNN_snake_case_description.sql` (e.g. `000023_add_orders_paid_at_index.sql`). Number monotonically; pad enough to last.
- **Large-table changes:** add column as nullable first, backfill in batches (separate migration or async job), then add `NOT NULL` / index. Single `ALTER TABLE ... NOT NULL` on a billion-row table will lock writes for minutes.
- **Tools:** `golang-migrate` (Go) and `alembic` (Python) — both run raw `.sql` files. STACK.md pins versions.

## 8. Security

- **Parameter binding always.** Restated because it's the single most common SQL injection vector.
- **Least-privilege roles.** The app's runtime role can `SELECT/INSERT/UPDATE/DELETE` but should not `CREATE/DROP/ALTER`. Migrations run as a separate, elevated role.
- **Row-Level Security (PG)** for multi-tenant: `ENABLE ROW LEVEL SECURITY` + policies keyed on a session variable holding `tenant_id`. Defense in depth against app-layer mistakes.
- **No secrets in connection strings stored in repo.** Pull from env / secret manager. PG supports `~/.pgpass` for local dev.
- **Encrypted at rest** is a deployment concern, but flag it: enable at the volume / disk layer.

## 9. Performance & EXPLAIN

- **`EXPLAIN ANALYZE` is the only honest perf tool.** Don't optimize without it.
- **Read the plan top-to-bottom.** Look for `Seq Scan` on large tables (missing index?), high `actual rows` vs `plan rows` (stale stats — run `ANALYZE`), nested loops over huge inputs (wrong index).
- **Slow query logging:** `log_min_duration_statement = 200` (ms) in dev. Tighter in prod, but at least log the 99th percentile offenders.
- **Connection pooling.** Postgres pays a real cost per connection. Use `pgbouncer` (transaction-mode for OLTP) in front; in-app pools (e.g. `pgx`, `psycopg`) for finer control.
- **`VACUUM ANALYZE`** runs automatically (autovacuum) — be aware of bloat on heavy `UPDATE`/`DELETE` tables and tune autovacuum thresholds for them.

## 10. JSON columns — when (and when not)

- **Use JSONB only for genuinely schemaless payloads:** raw webhook bodies, opaque third-party event blobs, user-defined opaque config.
- **Never for structured domain data.** If you find yourself querying `data->'order'->>'status'` repeatedly, it's a column, not a JSON field. Normalize.
- **Index with GIN** if you must query JSONB: `CREATE INDEX ... USING GIN (data jsonb_path_ops)` for containment queries.

## 11. Engine-specific guidance

PostgreSQL 18 is the primary target. Per-engine references are split out to keep this skill focused:

- **PostgreSQL-specific types and features** (timestamptz, text, citext, generated columns, partitioning, RLS, native `uuidv7()`, etc.) — see [POSTGRES.md](POSTGRES.md).
- **MySQL 9 and SQLite 3.53 notes** (charset, primary key strategies, JSON support, concurrency caveats) — see [ENGINES.md](ENGINES.md).
