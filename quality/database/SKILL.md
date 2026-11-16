---
name: database
description: "Design schemas, write safe/online migrations, add indexes, fix slow queries and N+1, get transactions and concurrency right. Postgres-first. Use when touching schema, migrations, indexing, query perf, or locking."
license: MIT
metadata:
  reviewed: "2026-10-18"
  sources: "honey-stack research 2026-10-18 (PostgreSQL 18 docs, EXPLAIN/pg_stat_statements, expand-contract migrations, isolation levels). Details in references/."
---

# database

Model data, change it safely on a live system, and make queries fast. Default engine is **Postgres**; the method carries to others. Push invariants into the database (constraints) — it's the one layer nothing bypasses.

## Confirm before (never on your own)
- Running **any migration against production**, especially one that locks, rewrites a table, or drops a column/table.
- `EXPLAIN ANALYZE` or a backfill on prod that **mutates data** (wrap in a transaction and roll back, or use a prod-sized copy).
- Dropping an index/column/table, or a destructive data fix.

## Schema design
- Normalize to 3NF first; denormalize only with a measured read-pattern reason, recorded in the migration.
- **Primary key:** `bigint GENERATED ALWAYS AS IDENTITY` for internal tables (smallest, best index locality); **UUIDv7** (`uuidv7()` on PG18, else app-generated) when IDs are exposed, client-generated, or merged across shards — time-ordered, so unlike UUIDv4 it keeps insert locality. Store as native `uuid`, never `varchar`.
- Default `NOT NULL`; NULL means "unknown" and breaks `=`. Use it only when absence is meaningful.
- Constraints: `FOREIGN KEY` (and **index the FK column** — Postgres doesn't auto-index them), `UNIQUE`, `CHECK`, `EXCLUDE`. Name them.
- JSONB only for genuinely schemaless/sparse blobs; use real columns for anything you filter, join, or constrain on. Index queried JSONB with GIN.
- Soft-delete (`deleted_at`) when you need audit/recovery (add a partial index `WHERE deleted_at IS NULL`); hard-delete for GDPR or volume.

Detail: `references/schema.md`.

## Indexing
B-tree (default), GIN (JSONB/arrays/full-text/trigram `LIKE '%x%'`), GiST (geo/range), BRIN (huge append-only). Composite order: equality columns first, then range/sort; the left prefix must match the query. Covering index with `INCLUDE` for index-only scans; partial index for skewed predicates. Every index slows writes — keep write-heavy tables lean. Read plans with `EXPLAIN (ANALYZE, BUFFERS)`; find unused/missing indexes via `pg_stat_user_indexes`/`pg_stat_user_tables`. Detail: `references/indexing.md`.

## Query performance & N+1
Detect N+1 by the same parametrized query running N times (test query-count assertions, APM span counts). Fix with eager/batch loading (Prisma `include`, SQLAlchemy `selectinload`, Django `select_related`/`prefetch_related`, GraphQL **DataLoader**). Find the worst queries with `pg_stat_statements` ordered by `total_exec_time`; enable `log_min_duration_statement`. Use **keyset/cursor pagination**, not deep `OFFSET`. Select explicit columns, never `SELECT *`. Batch writes (`COPY`, multi-row `INSERT`). Detail: `references/queries.md`.

## Safe / online migrations
**Expand–contract**: add new (nullable column / table / index) → backfill in batches + dual-write → switch reads → drop the old thing in a *later* deploy. Never rename in place on a live table. Always `CREATE INDEX CONCURRENTLY`; set `lock_timeout` so a blocked migration fails fast instead of queuing behind every query; add NOT NULL via a `NOT VALID` check then `VALIDATE CONSTRAINT` (no full-table exclusive lock). Tools: Prisma, Drizzle, Flyway, Alembic, Atlas (`atlas migrate lint` flags unsafe changes). Detail: `references/migrations.md`.

## Transactions & concurrency
Know the isolation levels and what each allows: READ COMMITTED (default; allows lost updates, read skew), REPEATABLE READ (snapshot; allows write skew), SERIALIZABLE (prevents all, may abort with `40001` → retry). Optimistic locking (version column) for low contention; `SELECT … FOR UPDATE` (+ `SKIP LOCKED` for queues) for high contention/money. Prevent deadlocks by locking in a consistent order and keeping transactions short; retry on `40P01`/`40001`. Make retried operations idempotent (unique idempotency key + `ON CONFLICT DO NOTHING`). Detail: `references/transactions.md`.

Done when: the schema/query/migration change is made, its plan or query count is checked (and shown), and any prod-affecting step was confirmed with the user and is reversible.
