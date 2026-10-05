---
name: explain-interpreter
description: This skill should be used when the user mentions "EXPLAIN", "explain analyze", "query plan", "slow query", "seq scan", "sequential scan", "nested loop", "index scan", "query optimization", "buffers", "why is this query slow", or pastes a query plan to interpret. It provides a methodology for reading Postgres and MySQL query plans and turning them into concrete index or rewrite recommendations.
---

# Explain Interpreter

## Purpose
Provide a standardized way to read a query plan, Postgres or MySQL, text or JSON, and convert it into a plain-language diagnosis and a concrete fix, statically, from pasted output. A plan is a tree of nodes; the database executes the leaves first and passes rows up. The skill is knowing which node is actually eating the time and what that node's presence implies.

## Reading methodology
1. **Identify the format and whether it was analyzed.** `EXPLAIN` alone gives *estimates*; `EXPLAIN ANALYZE` (Postgres) / `EXPLAIN ANALYZE` (MySQL 8) gives *actual* rows, time, and loops. Only actuals prove a bad estimate.
2. **Find the dominant node.** Read inside-out. A node's cost/time includes its children, so compute **self time** = node time − children's time, and for inner nodes of a loop, **multiply by `loops`**. The node with the largest self time (not the root) is the target.
3. **Read the node's meaning** (see `references/postgres-explain-nodes.md` / `references/mysql-explain.md`).
4. **Scan for red flags** (below).
5. **Prescribe** an index (right columns, right order) or a rewrite.

## The single most important number: estimate vs actual
`(cost=... rows=1000)` is the planner's *estimate*; `(actual ... rows=920000 loops=1)` is reality. A large skew (planner thought 1 row, got 900k) means the planner chose the wrong strategy (often a nested loop that would have been a hash join). Causes: stale statistics (`ANALYZE`), correlated predicates the planner assumes independent, or expressions it cannot estimate. Fix the estimate and the plan often fixes itself.

## Red-flag catalog

| Red flag | What the DB is doing | Fix |
|---|---|---|
| `Seq Scan` / `type: ALL` on a big table with a selective `WHERE` | Reading every row to find a few | Index the filter column |
| `rows` estimate ≪ actual (loops) | Planner mis-estimated → wrong join | `ANALYZE`; decorrelate; extended statistics |
| `Nested Loop` with high inner `loops` | Row-by-row inner lookups, N× | Index the inner join key; enable hash join |
| `Sort` → `Sort Method: external merge Disk` | Sort spilled to disk | Index matching `ORDER BY`; raise `work_mem` |
| `Using filesort` / `Using temporary` (MySQL) | Sorting/deduping without an index | Composite index over `WHERE`+`ORDER BY` |
| `Buffers: ... read≫hit` | Cold data, heavy I/O | Fewer rows scanned; covering index |
| Index exists but a Seq Scan is chosen | Predicate not sargable / type mismatch | Rewrite predicate; match types; expression index |
| Wide `width=` with `SELECT *` in an index-only candidate | Heap fetch forced | `INCLUDE`/covering columns |

## From plan to fix
- **Seq scan on a filter** → `CREATE INDEX` on the filter column(s), equality before range.
- **Bad estimate** → `ANALYZE`; consider `CREATE STATISTICS` for correlated columns.
- **Nested-loop blowup** → make the inner side an index lookup, or give the planner better estimates so it picks a hash join.
- **External sort** → index that provides pre-sorted output for the `ORDER BY`.
- **Extra heap fetches** → covering / `INCLUDE` index so it becomes index-only.

## Additional Resources
### Reference Files
- **`references/postgres-explain-nodes.md`**: every common node type, how to read cost/rows/actual/loops/buffers, estimate-vs-actual skew, and per-node red flags and fixes.
- **`references/mysql-explain.md`**: MySQL `EXPLAIN`/`EXPLAIN ANALYZE`/`FORMAT=JSON` columns, access `type` ladder, `Extra` flags, and optimizer hints.
