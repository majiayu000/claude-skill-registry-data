---
name: postgres-patterns
description: PostgreSQL patterns for query optimization, schema design, indexing, RLS, and connection pooling. Use when writing or reviewing SQL against the devskyy Postgres, choosing an index, diagnosing a slow query, or hardening database security. Do NOT use for versioning schema changes (that is database-migrations — Alembic owns every DDL change here), for Redis/cache semantics (redis-patterns), or for the container/compose layer around the database (docker-patterns).
origin: ECC
---

# PostgreSQL Patterns

Quick reference for PostgreSQL best practices. For detailed guidance, use the `database-reviewer` agent.

## When to use

- Writing SQL queries or the DDL that a migration will carry
- Designing database schemas
- Troubleshooting slow queries
- Implementing Row Level Security
- Setting up connection pooling

**When NOT to use:**

- Applying/versioning a schema change → `database-migrations`. This skill decides *what* the index
  or column should be; Alembic is *how* it ships. Hand-running DDL against a live database is
  banned regardless of how correct the SQL is.
- Cache TTLs, locks, rate limits → `redis-patterns`.
- "Postgres won't start" / port conflicts / volumes → `docker-patterns`.
- Any write to a production database — that is STOP-AND-SHOW, not a query-tuning task.

## Inputs

**Absent input = STOP. Never tune a query you cannot run and cannot see the plan for.**

1. **A reachable database and its identity.** Confirm which one before touching anything:
   `docker exec devskyy-postgres sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Atc "SELECT current_database(), version();"'`
   Observed 2026-07-28: `devskyy|PostgreSQL 15.18 … Alpine` `[repro]`. A "slow query" claim against
   an unnamed database is unverifiable.
2. **The actual query text and its real parameters** — not a paraphrase. Plans change completely
   with literal values, so a sanitized example proves nothing.
3. **`EXPLAIN (ANALYZE, BUFFERS)` output** for the before state. Without a before plan there is no
   evidence the after plan is better.
4. **Extension availability, checked not assumed.** `pg_stat_statements` is NOT installed on this
   dev instance (verified below) — every "find slow queries" recipe that reads it will ERROR, and
   an errored query is a dead gate, never a clean result.
5. **Write authority.** Read-only by default. `ALTER SYSTEM`, `CREATE INDEX` on a live table, and
   any `UPDATE`/`DELETE` without a `WHERE` are irreversible-class actions: STOP-AND-SHOW first.

## Procedure

1. Identify the target database (Inputs 1) and record the row counts you are reasoning about
   (`SELECT count(*)` on the tables in the query — an index decision on an unknown table size is a guess).
2. Capture the baseline plan: `EXPLAIN (ANALYZE, BUFFERS) <query>`. Note the node types
   (Seq Scan / Nested Loop), actual rows vs estimate, and total time.
3. Diagnose against the cheat sheets below — index type by predicate shape, composite column order
   (equality first, then range), partial/covering index where the working set is a subset.
4. Check whether the fix already exists: run the unindexed-FK and duplicate-index probes
   (Verification) before adding anything. An unused duplicate index costs writes forever.
5. Apply the change **through a migration** (`database-migrations`), never as ad-hoc DDL. On
   Postgres use `CREATE INDEX CONCURRENTLY`, which cannot run inside a transaction block.
6. Re-run the identical `EXPLAIN (ANALYZE, BUFFERS)` and compare plans, not vibes.
7. Confirm the index is actually being used afterwards (`pg_stat_user_indexes.idx_scan > 0` under
   real traffic); an index the planner ignores is pure write overhead.

## Verification

Each check states its command and pass condition. **A query that ERRORs is not a query that
passed** — the `pg_stat_statements` probe below is the live example of that trap (bug-230). Note
also the scope: results from the local dev container are `[repro]` evidence about *dev*. They are
never `[live]` evidence about production data.

```bash
docker exec devskyy-postgres sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "
SELECT conrelid::regclass AS tbl, a.attname AS fk_col
FROM pg_constraint c
JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = ANY(c.conkey)
WHERE c.contype = '\''f'\''
  AND NOT EXISTS (SELECT 1 FROM pg_index i
                  WHERE i.indrelid = c.conrelid AND a.attnum = ANY(i.indkey));"'
```
**PASS:** `(0 rows)` — every foreign key is indexed. Observed 2026-07-28 on `devskyy`: `(0 rows)`
`[repro]`. Any row returned is a real defect: unindexed FKs turn cascading deletes and joins into
sequential scans.

```bash
docker exec devskyy-postgres sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Atc \
  "SELECT count(*) FROM pg_extension WHERE extname='\''pg_stat_statements'\'';"'
```
**PASS:** returns `1`, meaning the slow-query recipes in this skill can run. Observed 2026-07-28:
`0` `[repro]` — the extension is absent, so `SELECT … FROM pg_stat_statements` fails with
`ERROR: relation "pg_stat_statements" does not exist` (also observed). Report that as **SKIPPED,
owner: whoever can `CREATE EXTENSION`**, never as "no slow queries found".

```sql
-- before and after the change, identical text and parameters
EXPLAIN (ANALYZE, BUFFERS) SELECT … ;
```
**PASS:** the after-plan's total execution time is lower AND the expensive node changed shape
(e.g. `Seq Scan` → `Index Scan`). A lower time with the same plan is noise — re-run 3× and compare
medians. `[repro]`

Prove the FK check can fail (rule 3): in a scratch database, `CREATE TABLE t_child(parent_id bigint
REFERENCES t_parent(id));` with no index, re-run probe 1 — it must return that row — then drop the
table. A probe that returns `(0 rows)` on a schema you know is bad is matching nothing.

Attribute before claiming a finding (rule 4): compare against the pristine schema via
`git archive HEAD alembic/ | tar -x -C <scratch>` and diff the DDL, rather than assuming the index
you see missing was missing before your change. Never `git stash` — shared stack across worktrees.

## Worked example

Real run against the local dev database, 2026-07-28:

```bash
docker exec devskyy-postgres sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Atc "SELECT count(*) FROM pg_stat_statements;"'
docker exec devskyy-postgres sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Atc "SELECT count(*) FROM information_schema.tables WHERE table_schema='"'"'public'"'"';"'
```

Observed `[repro]`:

```
ERROR:  relation "pg_stat_statements" does not exist
LINE 1: SELECT count(*) FROM pg_stat_statements;
7
```

Both lines matter. The first is the anti-pattern this skill's own "Find slow queries" snippet walks
into: the recipe is correct, the extension is not installed, and the query ERRORs. An agent that
runs it, sees no rows of output, and reports "no slow queries" has reported a *dead gate* as a
clean one (bug-230). The honest result is: slow-query analysis SKIPPED — needs
`CREATE EXTENSION pg_stat_statements` plus a `shared_preload_libraries` restart, owner = whoever
administers the container.

The second line says the `public` schema holds 7 tables — small enough that a Seq Scan may
legitimately beat an index, which is exactly why index decisions need row counts (Procedure step 1)
and not just query shape. And because this is the dev container, all of it is `[repro]` evidence
about dev; none of it licenses a claim about production data volumes (bug-287).

## Failure modes

- **An ERRORing probe read as a clean result.** `pg_stat_statements`, `pg_stat_user_tables` on a
  fresh DB, or a typo'd relation all produce "no findings" for the wrong reason. Read stderr.
- **Tuning against the wrong database.** `devskyy` in the container ≠ any production instance.
  State `current_database()` in the report.
- **Adding an index without checking for an existing one** — duplicates slow every write and never
  show up as a query regression.
- **`CREATE INDEX` without `CONCURRENTLY` on a large table** blocks writes for the duration; and
  `CONCURRENTLY` cannot run inside a transaction block, which is why it needs `op.execute("COMMIT")`
  in Alembic.
- **RLS policy without the `(SELECT auth.uid())` wrapper** re-evaluates the function per row — the
  policy is correct and the query is ruinous.
- **`work_mem` raised globally to fix one query** — it is per-sort, per-connection; 100 connections
  × a big sort is how a box OOMs.

## Quick Reference

### Index Cheat Sheet

| Query Pattern | Index Type | Example |
|--------------|------------|---------|
| `WHERE col = value` | B-tree (default) | `CREATE INDEX idx ON t (col)` |
| `WHERE col > value` | B-tree | `CREATE INDEX idx ON t (col)` |
| `WHERE a = x AND b > y` | Composite | `CREATE INDEX idx ON t (a, b)` |
| `WHERE jsonb @> '{}'` | GIN | `CREATE INDEX idx ON t USING gin (col)` |
| `WHERE tsv @@ query` | GIN | `CREATE INDEX idx ON t USING gin (col)` |
| Time-series ranges | BRIN | `CREATE INDEX idx ON t USING brin (col)` |

### Data Type Quick Reference

| Use Case | Correct Type | Avoid |
|----------|-------------|-------|
| IDs | `bigint` | `int`, random UUID |
| Strings | `text` | `varchar(255)` |
| Timestamps | `timestamptz` | `timestamp` |
| Money | `numeric(10,2)` | `float` |
| Flags | `boolean` | `varchar`, `int` |

### Common Patterns

**Composite Index Order:**
```sql
-- Equality columns first, then range columns
CREATE INDEX idx ON orders (status, created_at);
-- Works for: WHERE status = 'pending' AND created_at > '2024-01-01'
```

**Covering Index:**
```sql
CREATE INDEX idx ON users (email) INCLUDE (name, created_at);
-- Avoids table lookup for SELECT email, name, created_at
```

**Partial Index:**
```sql
CREATE INDEX idx ON users (email) WHERE deleted_at IS NULL;
-- Smaller index, only includes active users
```

**RLS Policy (Optimized):**
```sql
CREATE POLICY policy ON orders
  USING ((SELECT auth.uid()) = user_id);  -- Wrap in SELECT!
```

**UPSERT:**
```sql
INSERT INTO settings (user_id, key, value)
VALUES (123, 'theme', 'dark')
ON CONFLICT (user_id, key)
DO UPDATE SET value = EXCLUDED.value;
```

**Cursor Pagination:**
```sql
SELECT * FROM products WHERE id > $last_id ORDER BY id LIMIT 20;
-- O(1) vs OFFSET which is O(n)
```

**Queue Processing:**
```sql
UPDATE jobs SET status = 'processing'
WHERE id = (
  SELECT id FROM jobs WHERE status = 'pending'
  ORDER BY created_at LIMIT 1
  FOR UPDATE SKIP LOCKED
) RETURNING *;
```

### Anti-Pattern Detection

```sql
-- Find unindexed foreign keys
SELECT conrelid::regclass, a.attname
FROM pg_constraint c
JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = ANY(c.conkey)
WHERE c.contype = 'f'
  AND NOT EXISTS (
    SELECT 1 FROM pg_index i
    WHERE i.indrelid = c.conrelid AND a.attnum = ANY(i.indkey)
  );

-- Find slow queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
WHERE mean_exec_time > 100
ORDER BY mean_exec_time DESC;

-- Check table bloat
SELECT relname, n_dead_tup, last_vacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;
```

### Configuration Template

```sql
-- Connection limits (adjust for RAM)
ALTER SYSTEM SET max_connections = 100;
ALTER SYSTEM SET work_mem = '8MB';

-- Timeouts
ALTER SYSTEM SET idle_in_transaction_session_timeout = '30s';
ALTER SYSTEM SET statement_timeout = '30s';

-- Monitoring
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Security defaults
REVOKE ALL ON SCHEMA public FROM public;

SELECT pg_reload_conf();
```

## Related

- Agent: `database-reviewer` - Full database review workflow
- Skill: `clickhouse-io` - ClickHouse analytics patterns
- Skill: `backend-patterns` - API and backend patterns

---

*Based on Supabase Agent Skills (credit: Supabase team) (MIT License)*
