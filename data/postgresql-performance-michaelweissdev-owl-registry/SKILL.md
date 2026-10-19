---
name: postgresql-performance
description: Diagnose and fix slow PostgreSQL workloads from evidence - find the expensive statements with pg_stat_statements, read EXPLAIN (ANALYZE, BUFFERS) plans, decide whether an index, a rewrite, statistics, or configuration is the right lever, and investigate locks, bloat, autovacuum and connection saturation. Use when a query or endpoint is slow, a plan changed, CPU or I/O on a Postgres server is high, or the user asks how to read EXPLAIN output or what to index. Covers PostgreSQL 14-18 (version-specific options are labelled). Not for schema design, JSONB/RLS/extension feature usage (use postgresql-development), generic SQL authoring (sql-development), schema change rollout (use database-migrations), or non-Postgres engines.
compatibility: Works with any agent that can run psql or read pasted query plans. Examples target PostgreSQL 14-18; options introduced after 14 are marked. Read-only diagnostics need no special privileges beyond pg_monitor/pg_read_all_stats for other users' statements.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "postgresql, performance, explain, pg_stat_statements, indexing, vacuum, locks"
  topics: "query-tuning, observability, databases"
---

# PostgreSQL Performance

Find out where time actually goes, then change one thing and measure again. Most "slow database" reports are one of: a missing or unusable index, stale statistics, a plan that is right for one parameter and wrong for another, lock waits, too many connections, or an application issuing thousands of small queries.

## Scope and boundaries

- This skill: measurement, plan reading, index/rewrite/statistics decisions, vacuum and lock diagnostics.
- `postgresql-development`: schema design, data types, JSONB, RLS, extensions. This skill assumes the schema exists.
- `sql-development`: portable SQL authoring. `database-migrations`: how to roll out an index or schema change safely (lock levels, expand/contract). `redis-caching`: when the fix is to not hit the database. `elasticsearch-search` / `mongodb-development`: other engines.

## Non-negotiable rules

1. **Never run `EXPLAIN ANALYZE` blindly on writes or on a loaded production primary.** `ANALYZE` executes the statement. For `INSERT/UPDATE/DELETE/MERGE`, wrap it: `BEGIN; EXPLAIN (ANALYZE, BUFFERS) ...; ROLLBACK;` (side effects such as sequences, triggers calling external systems, and row locks still occur during the run). Prefer a replica or a restored copy for expensive reads.
2. **Do not reset, `VACUUM FULL`, `REINDEX`, `CLUSTER`, kill sessions, or change settings** without explicit user authorization. `pg_terminate_backend` and `pg_stat_statements_reset` are operational actions, not diagnostics.
3. **Measure on representative data.** A plan on a 1,000-row dev table says nothing about 100M rows. Say so when evidence comes from the wrong environment.
4. **Change one variable at a time** and compare before/after with the same parameters, warm vs cold cache stated.
5. **Treat query text and plans as sensitive.** pg_stat_statements normalises constants to `$n`, but logged statements and `auto_explain` output can contain literals (PII, tokens). Do not paste them into third-party tools without redaction.
6. **Do not recommend an index from the plan alone.** Check write cost, existing overlapping indexes, and whether the planner would use it (see workflow step 5).

## Workflow

### 1. Establish what is slow and since when
Ask for: the query or endpoint, typical vs bad latency, when it began (deploy? data growth? plan flip?), PostgreSQL major version (`SHOW server_version;`), and whether the bad case is one parameter value. If nothing is known, start from the aggregate view (step 2).

### 2. Rank statements with pg_stat_statements
Requires `shared_preload_libraries = 'pg_stat_statements'` (restart) and `CREATE EXTENSION pg_stat_statements;` in the database. `compute_query_id` must be `on` or `auto`.

```sql
SELECT queryid, calls,
       round(total_exec_time::numeric, 1) AS total_ms,
       round(mean_exec_time::numeric, 2)  AS mean_ms,
       rows,
       round(100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0), 1) AS hit_pct,
       left(query, 120) AS query
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 15;
```

Column names above are PostgreSQL 13+ (`total_time` became `total_exec_time` in 13). Interpretation:
- High **total** time with low mean: a frequent cheap query (N+1, missing batching, cache candidate).
- High **mean**: a heavy query; go to EXPLAIN.
- Large `shared_blks_read` or `temp_blks_written`: I/O or spill (sorts/hashes exceeding `work_mem`).
- `stats_since` (PG 17+) tells how long the counters have accumulated; stats are since last reset/restart, so a stale window misleads.
- `track_planning` (off by default) adds planning columns but can add contention; enable only deliberately.
- `queryid` is not stable across major versions.

### 3. Get the plan
```sql
EXPLAIN (ANALYZE, BUFFERS, SETTINGS) SELECT ...;           -- PG 12+ for SETTINGS
EXPLAIN (ANALYZE, BUFFERS, WAL, VERBOSE) ...;              -- WAL: PG 13+, for writes
EXPLAIN (ANALYZE, SERIALIZE) SELECT ...;                   -- PG 17+: includes result conversion/transfer cost
EXPLAIN (ANALYZE, MEMORY) ...;                             -- PG 17+: planner memory
EXPLAIN (GENERIC_PLAN) SELECT * FROM t WHERE id = $1;      -- PG 16+: parameterised plan, no ANALYZE
```
Version notes (checked against the PostgreSQL 18 manual): in PG 18 `BUFFERS` is included automatically with `ANALYZE` (use `BUFFERS OFF` to suppress); on 17 and earlier you must ask for it. `SERIALIZE`, `WAL` and `TIMING` require `ANALYZE`; `GENERIC_PLAN` cannot be combined with `ANALYZE`. Use `FORMAT JSON` only for tools; text is easier to read.

For prepared statements with bad plans for some values, compare `plan_cache_mode` behaviour (`auto`, `force_custom_plan`, `force_generic_plan`) rather than guessing.

### 4. Read the plan with a checklist
See [references/explain-reading.md](references/explain-reading.md) for the full guide. Key moves:
1. Find the node with the largest **exclusive** actual time (remember `actual time` and `loops` multiply: per-loop time x loops).
2. Compare `rows=` (estimate) with `actual rows`. A gap of 10x or more points to statistics or correlated predicates, not to "needs index".
3. Look at `Buffers: shared hit/read`, `temp read/written`; `Sort Method: external merge` or `Batches > 1` means work_mem spill.
4. `Rows Removed by Filter` large with an Index Scan means the index is not selective for the full predicate; `Heap Fetches` high in an Index Only Scan means the visibility map is stale (vacuum).
5. Nested Loop with a large outer side and an inner Seq Scan is the classic missing-index-on-join-key.
6. `Index Searches` (PG 18) shows how many index descents a scan used; many searches signals a skip-scan or `IN` list shape worth examining.

### 5. Choose the lever
| Evidence | Likely lever |
|---|---|
| Seq Scan on big table, selective predicate, no usable index | Index matching the predicate and sort order (btree column order: equality columns first, then range/sort) |
| Index exists but unused | Type/collation/expression mismatch, low selectivity, stale stats, or function wrapping the column; check with `EXPLAIN` after `ANALYZE` |
| Estimate far from actual | `ANALYZE`; raise `default_statistics_target` or per-column `SET STATISTICS`; `CREATE STATISTICS` (dependencies, ndistinct, mcv) for correlated columns |
| Sort/Hash spills to disk | Raise `work_mem` per session for that query (it is per node per worker, not global), or reduce rows earlier |
| Large `OFFSET` | Keyset pagination |
| `IN (subquery)` / `NOT IN` pathologies | `EXISTS` / `NOT EXISTS`; note `NOT IN` with NULLs differs semantically |
| Thousands of identical small queries | Batch, join, or cache (see `redis-caching`) |
| Many rows returned | Fix the query shape; consider `SERIALIZE` cost (PG 17+) and client fetch size |

Index creation on a live table: use `CREATE INDEX CONCURRENTLY` (not inside a transaction block) and follow `database-migrations` for lock and rollout handling. A failed concurrent build leaves an `INVALID` index that still costs writes (`SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid;`): drop it and retry. State the write cost: every index is maintained on each INSERT/DELETE and on UPDATEs of indexed columns, so report its size (`pg_relation_size`) and the table's write rate. Before adding one, check duplicates and usage:

```sql
SELECT relname, indexrelname, idx_scan, pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC, pg_relation_size(indexrelid) DESC
LIMIT 20;
```
`idx_scan = 0` since the last stats reset is a candidate for removal only after a full business cycle and after checking replicas (stats are per node).

### 6. Check the non-query causes
- **Locks and waits**: sessions where `wait_event_type = 'Lock'` in `pg_stat_activity`; find the blocker with `pg_blocking_pids(pid)`. See [references/locks-vacuum-connections.md](references/locks-vacuum-connections.md).
- **Idle in transaction** sessions holding old snapshots stop vacuum from reclaiming rows and cause bloat.
- **Autovacuum**: `n_dead_tup`, `last_autovacuum`, and per-table `autovacuum_vacuum_scale_factor` for huge tables.
- **Connections**: hundreds of active backends thrash CPU; use a pooler (pgBouncer-style transaction pooling has prepared-statement caveats) rather than raising `max_connections`.
- **Checkpoints / WAL / I/O**: a write-heavy system limited by checkpoints shows in `pg_stat_bgwriter`/`pg_stat_checkpointer` (the checkpointer view is PG 17+).

### 7. Verify
Re-run the same `EXPLAIN (ANALYZE, BUFFERS)` and the aggregate query. Report before/after: latency, buffers, rows examined, plan shape. If improvement is only in cold vs warm cache, say so.

## Worked example

Symptom: `GET /orders?customer_id=...` p95 1.8 s. `pg_stat_statements` shows the query at mean 410 ms, 52,000 calls/hour.

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders WHERE customer_id = 42 AND status = 'open' ORDER BY created_at DESC LIMIT 20;
```
Plan: `Index Scan Backward using orders_created_at_idx` ... `Rows Removed by Filter: 9,800,000`, 410 ms, `shared read=61,000`. The planner walks the date index hoping to hit 20 matching rows quickly; the filter rejects almost everything.

Fix candidate: `CREATE INDEX CONCURRENTLY orders_cust_status_created_idx ON orders (customer_id, status, created_at DESC);` (equality, equality, sort). After creation, `ANALYZE orders;` and re-run: `Index Scan using orders_cust_status_created_idx`, 0.3 ms, `shared hit=6`. Cost: one more index to maintain on every insert; check that `orders_created_at_idx` is still needed.

## Anti-patterns

- Indexing every column from a single plan; dropping indexes with `idx_scan = 0` the day after a stats reset.
- Raising `work_mem` or `shared_buffers` globally to fix one query.
- Judging by `cost=` numbers (planner units, not milliseconds) or by a single cold run.
- Disabling planner features (`enable_seqscan = off`) in production rather than diagnosing; acceptable only as a short experiment in one session.
- Running `ANALYZE`-less EXPLAIN and trusting row estimates after bulk loads.
- Treating a lower `total_exec_time` ranking as proof of a fix when traffic simply dropped.

## Verification checklist

- [ ] Version and environment stated; data volume representative or caveat given
- [ ] Slow statement identified from aggregate evidence, not guess
- [ ] Plan read at node level: estimate vs actual, loops, buffers, spills
- [ ] Lever chosen from the table with the evidence it matches
- [ ] Writes explained in a transaction/rollback or run on a replica/copy
- [ ] Index change includes write cost, duplicate check, and a safe rollout path
- [ ] Before/after numbers reported with the same parameters
- [ ] No destructive/ops commands run without authorization

## References

- [references/explain-reading.md](references/explain-reading.md) - node types, estimate errors, buffers, spill signals
- [references/locks-vacuum-connections.md](references/locks-vacuum-connections.md) - diagnostic queries for waits, bloat, connections
- [references/scenarios.md](references/scenarios.md) - activation and execution scenarios
- [references/sources.md](references/sources.md) - official sources and provenance
