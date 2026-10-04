---
name: SQL
slug: sql
version: 1.0.4
description: Writes, reviews, and optimizes SQL queries; designs schemas, indexes, and constraints; plans migrations for any relational database. Use when a query is slow, EXPLAIN shows a sequential scan, or an index is ignored; when rows come back duplicated, missing, or with inflated totals after a JOIN; on deadlocks, lock timeouts, "too many connections", or transactions that never commit; when designing tables, keys, and column types, normalizing or denormalizing a model, or deciding between a JSON column and real columns; for ALTER TABLE on a live table, expand-migrate-contract rollouts, backups and restores, replication lag, connection pooling, partitioning, bulk CSV imports, and moving data between engines; for window functions, CTEs, keyset pagination, upserts, full-text search, multi-tenancy, row-level security, and timezone handling in MySQL, SQLite, MariaDB, or SQL Server. Not for PostgreSQL server internals such as vacuum tuning and work_mem sizing, and not for ORM schema modeling inside a framework.
homepage: https://clawic.com/skills/sql
changelog: 'Full coverage pass: deeper guides, situation-named files, and per-user configuration'
metadata:
  clawdbot:
    emoji: 🗄️
    requires:
      anyBins:
      - sqlite3
      - psql
      - mysql
      - sqlcmd
    os:
    - linux
    - darwin
    - win32
    displayName: SQL
    configPaths:
    - ~/Clawic/data/sql/
    - ~/sql/
    - ~/clawic/sql/
  openclaw:
    requires:
      config:
      - ~/Clawic/data/sql/
      - ~/sql/
      - ~/clawic/sql/
---

User preferences and memory live in `~/Clawic/data/sql/` (see `setup.md` on first use, `memory-template.md` for the file format). If you have data at an old location (`~/sql/` or `~/clawic/sql/`), move it to `~/Clawic/data/sql/`, and say in one line that you moved it and from where.

## When To Use

- Writing, reviewing, or optimizing SQL: queries, joins, CTEs, window functions, upserts
- Designing tables, keys, types, indexes, and constraints, or normalizing an existing model
- Diagnosing a slow query, a deadlock, a lock timeout, wrong totals, or duplicated rows
- Planning migrations and DDL that must not take a live database down
- Operating a database: backups, restores, monitoring, pooling, replication, partitioning
- Moving data in or out: CSV loads, dumps, engine-to-engine migrations
- Not for PostgreSQL server internals (vacuum tuning, `work_mem`, xid wraparound) — that is `pg`; not for ORM-level modeling in a framework — that is `prisma`

## Quick Reference

| Situation | Play |
|-----------|------|
| Query slow, cause unknown | `EXPLAIN (ANALYZE, BUFFERS)`, fix the worst node first (→ Reading EXPLAIN, then `performance.md`) |
| Query was fast yesterday | Stats, data growth, or plan flip — the regression chain in `debug.md` |
| Index exists but is not used | Function on the column, type mismatch, wrong column order, or low selectivity (→ Traps, `performance.md`) |
| Totals inflated after adding a JOIN | 1:N fan-out — aggregate before joining (→ Traps) |
| Rows missing after adding a JOIN | `LEFT JOIN` filtered in `WHERE` became an inner join (→ Traps) |
| Paginating past the first few thousand rows | Keyset, never OFFSET (`patterns.md`) |
| Deadlock, lock timeout, or "could not obtain lock" | `transactions.md` — lock ordering and isolation |
| "Too many connections" / app hangs on connect | Pool sizing before `max_connections` (`operations.md`, `orm.md`) |
| Read-modify-write race, job queue | `SELECT ... FOR UPDATE`, add `SKIP LOCKED` for queues (`patterns.md`) |
| Schema change on a live table | Expand → migrate → contract, `lock_timeout` first (`operations.md`) |
| Designing a model from scratch | Keys, cardinality, normal forms, when to denormalize (`modeling.md`) |
| Known shape needed (tenants, tags, audit, state, history) | `schemas.md` |
| Storing or querying JSON / semi-structured data | `json.md` |
| Cohorts, funnels, retention, rollups, materialized views | `analytics.md` |
| Loading a CSV, dump/restore, engine-to-engine move | `data-loading.md` |
| Timestamps off by hours, DST, week/fiscal boundaries | `datetime.md` |
| Statement works on one engine, fails on another | `dialects.md` |
| Grants, least privilege, RLS, PII erasure, encryption | `security.md` |
| Seeding fixtures, isolating tests, testing a migration | `testing.md` |
| ORM emits terrible SQL, N+1, mystery transactions | `orm.md` |
| Single node at its limit: replicas, sharding, caching | `scaling.md` |
| Choosing an engine | SQLite embedded/local · PostgreSQL default for servers · MySQL when the platform dictates it · SQL Server in .NET/Windows shops (`dialects.md`) |
| Anything else | Reproduce on the smallest table that shows it, then: schema-shaped → `modeling.md`/`schemas.md` · query-shaped → `patterns.md` · slow → `performance.md` · ops-shaped → `operations.md` |

## Core Rules

1. **Parameterize values; allowlist identifiers.** Placeholders (`?`, `$1`) stop injection for values, but table/column names cannot be bound — when those are dynamic, check them against a hardcoded allowlist, never interpolate user input. Full attack surface, including `LIKE` and `ORDER BY` injection: `security.md`.
2. **BIGINT (or UUIDv7) primary keys by default.** `INT` overflows at 2,147,483,647 — at a sustained 100 inserts/s that is 2.1B ÷ 100/s ≈ 248 days, and the fix is an outage-grade type change. Random UUIDv4 keys fragment the B-tree; UUIDv7/ULID keep insert locality (`modeling.md`).
3. **Index for the query shape: equality columns first, then range/sort.** `(user_id, created_at)` serves `WHERE user_id = ? AND created_at > ?` and `WHERE user_id = ?` alone — never `created_at` alone. A sequential scan on a filter matching more than roughly 5-10% of rows is the planner being right, not broken.
4. **Index every foreign key column yourself.** MySQL/InnoDB creates the index automatically; PostgreSQL, SQLite, and SQL Server do not. Without it, every join on the FK and every parent `DELETE` (worse with `ON DELETE CASCADE`) scans the whole child table — the slowest delete in most schemas is this one missing index.
5. **Transactions stay short and never wait on the outside world.** No HTTP calls, no user input inside `BEGIN...COMMIT`: open transactions hold locks, and in PostgreSQL they also block vacuum, causing table bloat. Anything open past the >1 min monitoring threshold (`operations.md`) gets investigated.
6. **NULL is three-valued.** `NOT IN (subquery)` returns zero rows if the subquery yields a single NULL — use `NOT EXISTS`. `x = NULL` is never true — use `IS NULL`. `COUNT(col)` skips NULLs; `COUNT(*)` counts rows. Aggregates over zero rows return NULL, not 0 — wrap in `COALESCE` when a chart or invariant expects a number.
7. **Types that avoid the next migration.** Money → `NUMERIC`/`DECIMAL` (float money loses cents in aggregation); timestamps → `TIMESTAMPTZ` stored as UTC (`datetime.md`); strings → `TEXT` in PostgreSQL and SQLite (`varchar(255)` is a cargo-cult limit you will later raise); MySQL charset → `utf8mb4` (MySQL's `utf8` is 3-byte and rejects emoji).
8. **Migrations are additive first.** Rename/retype/drop happens over multiple deploys with both versions live in between (expand-migrate-contract, `operations.md`). A single-deploy column rename breaks every instance still running old code.
9. **Rank before you tune.** `pg_stat_statements` ordered by `total_exec_time` (or the MySQL slow query log digested by `pt-query-digest`) tells you which query costs the most overall — usually not the one someone complained about. Total cost = mean latency × call count: a 5 ms query called 10,000×/min (50 s/min) outranks a 2 s report run hourly. Optimizing an unranked query is guessing.

## Reading EXPLAIN

```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE user_id = 5;  -- PostgreSQL
EXPLAIN ANALYZE SELECT ...;                                         -- MySQL >=8.0.18
EXPLAIN QUERY PLAN SELECT * FROM orders WHERE user_id = 5;          -- SQLite
SET STATISTICS PROFILE ON;                                          -- SQL Server (or the graphical plan)
```

Read actual behavior, not just the plan. Plain `EXPLAIN` shows estimates only, and estimates are the part that lies.

- `Seq Scan` / `type: ALL` on a large table with a selective filter → missing or unusable index (→ Traps for what disables one)
- `Rows Removed by Filter` high → the index found candidates but the filter did the work; extend the index to cover the filter
- Estimated vs actual rows off by **more than 10×** → stale stats: run `ANALYZE tablename;`. Still off → the planner assumes column independence; declare the correlation (`CREATE STATISTICS` on PostgreSQL >=10, histogram on MySQL 8)
- `Buffers: read` large vs `hit` → data is coming from disk; recheck on a warm cache before concluding
- Nested Loop over thousands of outer rows → usually the >10× misestimate above feeding a bad join choice
- Node-by-node interpretation, join algorithms, and what to change for each: `performance.md`

## Index Strategy

```sql
-- Composite: equality columns first, range/sort last (rule 3)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Covering: index-only scan, no heap fetch (PostgreSQL >=11, SQL Server INCLUDE)
CREATE INDEX idx_orders_user ON orders(user_id) INCLUDE (total);

-- Partial/filtered: index only the rows you query (PostgreSQL, SQLite, SQL Server)
CREATE INDEX idx_orders_pending ON orders(user_id) WHERE status = 'pending';

-- Expression: make a function sargable (MySQL >=8.0.13 supports functional indexes)
CREATE INDEX idx_users_email_lower ON users(LOWER(email));
```

- A plain B-tree on a low-cardinality column (`status` with 5 values) rarely helps; a partial index on the rare value you actually query does.
- An index on `(a, b)` already serves `WHERE a = ?` — creating a second index on `(a)` alone adds write cost and reclaims nothing. Check for redundant prefixes before adding.
- PostgreSQL with a non-C locale ignores B-tree indexes for `LIKE 'term%'` — add the `text_pattern_ops` opclass for prefix search.
- Index-only scans still hit the heap for pages not marked all-visible; if `EXPLAIN` shows `Heap Fetches` high, the table needs a `VACUUM` (`operations.md`).
- Every index taxes writes and consumes disk: drop unused ones (`pg_stat_user_indexes` where `idx_scan = 0`), but only after uptime covers a full business cycle — month-end reports use indexes nothing else does.

## Portability

| Feature | PostgreSQL | MySQL | SQLite | SQL Server |
|---------|------------|-------|--------|------------|
| Limit | LIMIT n | LIMIT n | LIMIT n | TOP n / OFFSET-FETCH |
| Upsert | ON CONFLICT | ON DUPLICATE KEY | ON CONFLICT | MERGE |
| Boolean | true/false | 1/0 (TINYINT) | 1/0 | 1/0 (BIT) |
| Concat | \|\| | CONCAT() | \|\| | + or CONCAT() |
| Auto-id | GENERATED / SERIAL | AUTO_INCREMENT | INTEGER PRIMARY KEY | IDENTITY |
| Returning rows from DML | RETURNING | — (MariaDB has it) | RETURNING (>=3.35) | OUTPUT |
| Aggregate FILTER | Yes | CASE only | Yes (>=3.30) | CASE only |
| Transactional DDL | Yes | No (implicit commit) | Yes | Yes |
| Default string compare | Case-sensitive | Case-insensitive (`_ci` collations) | Case-sensitive | Case-insensitive by default |

Date functions, quoting, NULL sort order, collation, and the rest of the divergences: `dialects.md`.

## Output Gates

Before emitting SQL, verify:

- Every value is a placeholder, and every dynamic identifier came from an allowlist?
- `UPDATE`/`DELETE` has a `WHERE`, or the full-table effect is explicitly intended?
- Destructive DML was previewed as the equivalent `SELECT` first?
- No 1:N join feeds an aggregate without pre-aggregation, and no `DISTINCT` is papering over one?
- `LIMIT`/`TOP` has a deterministic `ORDER BY` with a unique tiebreaker?
- New table: primary key type per rule 2, timestamps with zone, uniqueness scoped to the right columns, every FK column indexed (rule 4)?
- DDL against a live table: `lock_timeout` set, and the change is expand-only?
- Every construct used exists in the target engine (→ Portability, `dialects.md`)?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/sql/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| dialect | postgres \| mysql \| mariadb \| sqlite \| sqlserver | postgres | Syntax of every emitted statement and which caveats from Portability and `dialects.md` are surfaced |
| engine_version | text (e.g. `15`, `8.0.35`) | none | Gates features with a version floor (`RETURNING`, functional indexes, `NULLS NOT DISTINCT`); with none set, the conservative form is emitted |
| identifier_style | snake_case \| camelCase \| PascalCase | snake_case | Naming of tables, columns, indexes, and constraints in generated DDL |
| table_naming | plural \| singular | plural | Whether generated tables read `users` or `user` |
| pk_type | bigint-identity \| uuidv7 \| uuidv4 \| natural | bigint-identity | The primary key emitted by every `CREATE TABLE` (rule 2, `modeling.md`) |
| destructive_guard | bool | true | When true, `UPDATE`/`DELETE` without `WHERE`, `DROP`, and `TRUNCATE` are emitted as a transaction-wrapped preview with the matching `SELECT` first |
| migration_tool | text (flyway, alembic, golang-migrate, sqitch, ...) | none | File naming and up/down structure of generated migrations (`operations.md`) |
| timezone_policy | utc \| local | utc | Whether timestamps are stored and compared as UTC and how `datetime.md` examples render |
| lock_timeout | text (duration: `500ms`, `2s`, `10s`) | 2s | The `SET lock_timeout` emitted before every DDL statement against a live table (→ Traps, `operations.md`) |
| batch_size | number (rows, 100-100000) | 5000 | Chunk size for batched `DELETE`/`UPDATE`, backfills, and bulk loads (`patterns.md`, `data-loading.md`, `json.md`) |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied:

- **Tooling** — client (psql, mysql, sqlite3, sqlcmd, a GUI), migration runner, SQL linter/formatter, local database as a container vs installed service — affects `operations.md` and `testing.md` examples
- **Conventions** — index and constraint naming, keyword casing, CTE vs subquery preference, comment style in DDL — affects every emitted statement
- **Platform** — managed service (RDS, Aurora, Cloud SQL, Neon, PlanetScale) vs self-hosted, available extensions, collation and locale — affects which features may be assumed
- **Safety posture** — how much confirmation destructive DDL/DML needs, whether production credentials are ever used directly, read-only-by-default sessions — affects `operations.md` and the `destructive_guard` gate
- **Output format** — full runnable script vs snippet, whether a down/rollback migration accompanies every up, inline comments — affects the shape of every deliverable
- **Work order** — schema-first vs query-first design, review gate before a migration reaches production — affects the sequence in `modeling.md` and `operations.md`
- **Integrations** — ORM in use, warehouse/BI target, monitoring stack — affects `orm.md` and `analytics.md` advice
- **Constraints** — vetoed features (no triggers, no stored procedures, no vendor extensions), compliance regime (retention windows, GDPR erasure) — affects `schemas.md` and `security.md` choices
- **Thresholds** — the operational budgets a shop usually standardizes: `lock_timeout`, `batch_size`, retry cap on deadlock/serialization failures, pool sizing rule, and the alert levels (connection saturation, disk free, transaction age, backup age) — affects `transactions.md` retry loops and the Alert Thresholds table in `operations.md`
- **Cadence** — how often scheduled work runs: restore drills, rollup and materialized-view refresh, the trailing recompute window, data-quality assertion runs, automated partition creation, backup interval — affects `operations.md`, `analytics.md`, `schemas.md`, and `testing.md` schedules

## Traps

| Trap | Why it fails | Do instead |
|------|--------------|------------|
| `WHERE YEAR(created_at) = 2024` | Function on the column hides it from the index | Range: `created_at >= '2024-01-01' AND created_at < '2025-01-01'` |
| `BETWEEN '2024-01-01' AND '2024-01-31'` on a timestamp | Upper bound is midnight — the whole last day is excluded with no error | Half-open range: `>= '2024-01-01' AND < '2024-02-01'` |
| `WHERE varchar_col = 123` | Implicit cast applies to the column, disabling its index | Match types: quote the literal or fix the schema |
| `LEFT JOIN t ... WHERE t.col = x` | WHERE runs after the join and filters the NULL rows out → an INNER JOIN, with no error | Move the predicate into `ON`, or test `t.id IS NULL` for an anti-join |
| Join 1:N then `SUM`/`COUNT` | Fan-out duplicates left-side rows before aggregation | Aggregate in a subquery/CTE, then join the result |
| `DISTINCT` added to make duplicates go away | Hides a fan-out bug and forces a sort of the whole result | Find the join that multiplies rows; `DISTINCT` is a diagnosis, not a fix |
| `LIKE '%term'` | Leading wildcard defeats B-tree ordering | Full-text search (`schemas.md`) or a trigram index (`pg_trgm`) |
| Composite `(a, b)` for `WHERE b = ?` | B-tree is sorted by `a` first; `b` alone is unordered | Separate index on `b`, or reorder if `a` is always filtered |
| `WHERE a = ? OR b = ?` | One index cannot serve two independent predicates; usually a full scan | `UNION ALL` of two indexed queries, deduplicated if needed |
| `LIMIT 10` without `ORDER BY` | Row order is undefined — "top 10" changes between runs and after a vacuum | Always `ORDER BY` with a unique tiebreaker column |
| `ORDER BY random() LIMIT n` | Full scan plus sort of the entire table | `TABLESAMPLE` or a random-key probe (`patterns.md`) |
| `SELECT *` in application code | Blocks index-only scans, fetches columns you drop, breaks on schema change | Name the columns |
| DDL without `lock_timeout` | `ALTER TABLE` queues behind one long query and every new query queues behind it — brief lock, full outage | `SET lock_timeout` (default `2s`, → Configuration) then retry (`operations.md`) |
| Wrapping `TRUNCATE`/DDL in a transaction on MySQL | MySQL commits implicitly on DDL: the rollback you planned does not exist | Take a backup or use a copy table; transactional DDL is PostgreSQL/SQLite/SQL Server only |

## Where Experts Disagree

- **Surrogate vs natural keys.** Surrogate (`BIGINT`/UUID) is the default: natural keys change, and a changing PK cascades into every child row. Natural keys legitimately win on pure junction tables and on immutable code tables (ISO currency, country) where the extra id buys nothing (`modeling.md`).
- **Foreign keys at scale.** Some high-write shops drop FK constraints because they add per-write lock and index cost and complicate online schema-change tooling. Default: keep them — orphan cleanup costs more than the writes saved. Drop only with a measured write bottleneck and integrity enforced elsewhere.
- **Logic in the database.** Triggers and stored procedures give atomicity nothing in the app can match and centralize rules across many clients; they are also invisible to code review, hard to test, and version-controlled poorly. Default: constraints and simple audit triggers in the database, business workflows in the application (`schemas.md`).
- **Soft delete everywhere.** Undo and audit are real requirements, but a `deleted_at` on every table poisons every query and every unique constraint. Default: hard delete plus an audit log; soft-delete only the tables users actually restore (`schemas.md`).

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/sql (install if the user confirms):
- `pg` — PostgreSQL server internals: vacuum, work_mem, wraparound
- `mysql` — MySQL and InnoDB specifics
- `sqlite` — SQLite concurrency, pragmas, and type affinity
- `prisma` — Node.js ORM modeling
- `dbt` — warehouse transformations and tests

## Feedback

- If useful, star it: https://clawic.com/skills/sql
- Latest version: https://clawic.com/skills/sql

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/sql.
