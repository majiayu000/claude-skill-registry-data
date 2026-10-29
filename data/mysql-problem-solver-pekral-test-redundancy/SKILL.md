---
name: mysql-problem-solver
description: Use when analyze real MySQL query and schema problems using code
  inspection, schema review, and EXPLAIN when available
license: MIT
metadata:
  author: Petr Král (pekral.cz)
---

## Constraints
- Apply @rules/sql/optimalize.md
- If the current project uses Laravel, also apply `@rules/laravel/laravel.md`, `@rules/laravel/architecture.md`, `@rules/laravel/filament.md`, and `@rules/laravel/livewire.md`
- Be practical and direct
- Prefer investigation over assumptions
- Do not invent schema, indexes, or runtime behavior
- Do not recommend index changes without explaining why they help
- Apply `@rules/sql/optimalize.md` "Performance Non-Regression on Query Changes" — every proposed query rewrite must be at least as fast as the original (ideally faster); a proposal that is slower must carry the documented reason and the remaining optimization options
- If DB access is unavailable, continue with static analysis and state the limitation clearly

## Scope
Investigate real MySQL performance or query design problems in existing applications.

Focus on:
- the actual query
- real schema and index usage
- EXPLAIN-based diagnosis when possible
- safe, justified optimizations

## Modes

- **Default (no `MODE`)** — investigate a reported problem and answer with the full analysis report below.
- **`MODE=cr-report`** — the code-review report the `casey` agent writes (`agents/casey.md`, `@skills/code-review/references/specialized-reviews.md` *MySQL report — the `casey` agent*). The review itself never runs this skill inline. In this mode the skill:
  - runs against a **locally started database only** — never a shared, staging, or production host. With no local database, it analyses statically and says so;
  - is **read-only** — it never writes a migration, an index, a query, or a configuration change, and never runs a statement that changes data or schema. Plain `EXPLAIN` and `SHOW` only; `EXPLAIN ANALYZE` (MariaDB `ANALYZE`) executes the statement, so run it on a `SELECT` only — never on `INSERT` / `UPDATE` / `DELETE`;
  - is **diff-scoped** — every item anchors to a `file:line` the diff added or modified; a pre-existing query the diff does not touch is out of scope;
  - reports **critical items only** — a full scan, `filesort`, or `temporary` on a realistically large table on a hot path, a per-row query in a loop, an N+1 on a list, a DDL that blocks writes during a deploy, or a comparable outage or data-loss risk. A non-critical observation is omitted, never downgraded into the report;
  - gives each item its evidence (`file:line`, the reconstructed SQL, the `EXPLAIN` baseline when DB access exists, or the stated limitation when it does not) and one proposed optimization held against *Performance Non-Regression on Query Changes* in `@rules/sql/optimalize.md`;
  - answers `No critical MySQL item in this diff.` when nothing qualifies.

**In a code review this skill owns query performance and its plan, never the shape of a schema feature.** When the CR's schema-feature trigger fires on the same diff (`@skills/code-review/references/specialized-reviews.md` *Specialized Reviews*), `@skills/mysql-patterns/SKILL.md` with `MODE=cr` runs in the review beside this skill's `casey` report and owns whether an upsert is one statement over a backing unique index, whether a JSON path is indexed through a generated column, whether the partition key matches the predicate, whether `sticky` survives a read-after-write path, and whether a concurrent transaction carries a deadlock retry.
Raise one point per violation: keep index usage, rows examined, `EXPLAIN` shape, and the non-regression gate here, and never restate a schema-shape finding in your own words. The schema-pattern findings stay in the review's `## Database Analysis` section; this skill's items stay in the `casey` report.

The same division holds against the CR's latency lens. When `@skills/latency-critical-systems/SKILL.md` with `MODE=cr` runs over the same diff, it owns **the budget of the path and the freshness of its data** — the stated p50 / p95 / p99 target, the mapped hot path, the staleness window on a cached or broadcast read, and the backpressure that bounds queue depth. This skill keeps the query and its plan, including N+1. The two divide the *dimensions* of a hot-path change, never its lines: a `foreach` issuing a query per row on a queue path carries this skill's query-plan finding, and the latency lens speaks on the same change only when it also leaves the path with no stated budget or no freshness window — a different defect, never this skill's finding restated.

## Execution

### 1. Identify the Query
- Find the actual SQL or reconstruct it from Laravel/Eloquent/query builder code
- Include filters, joins, ordering, grouping, pagination, and subqueries

### 2. Inspect Schema
- Inspect relevant tables and indexes using:
    - schema output
    - migrations
    - model relationships
    - DB tools when available

### 3. Run EXPLAIN
- If MySQL access is available, run `EXPLAIN` on the query and read its plan.

### 4. Diagnose the Problem
Look for:
- full scans
- weak join strategy
- existing index bypassed — query could hit a covering index already in the schema but the column order, a wrapping function, or extra projected columns prevent it. Preferred fix is a query rewrite (column re-ordering, SARGable rewrite, covering projection), not a new index (see `@rules/sql/optimalize.md` "Reuse existing indexes first").
- missing or ineffective indexes
- non-SARGable filters
- poor sort/group plans
- offset pagination on large datasets
- N+1 behavior from application code
- per-row queries inside loops — per-row `update()` / `create()` / `delete()` or single-row reads driven by a `foreach` (distinct from N+1 eager-loading: this is application code intentionally writing or reading row-by-row when a single batch query would suffice)
- redundant or overlapping indexes
- schema changes that block during a deploy — a DDL statement that names no `ALGORITHM` / `LOCK` and may silently fall back to a table copy, or a data backfill executed inside the migration itself instead of a separate chunked command (see `@rules/sql/optimalize.md` "Deploy-safe schema changes")

### 5. Propose Optimizations

Before recommending any rewrite, capture the **baseline** of the original query (`EXPLAIN` / `EXPLAIN ANALYZE` — `type`, `key`, `rows`, `filtered`, `Extra`, measured latency when DB access is available). Every proposal must then be held against that baseline per `@rules/sql/optimalize.md` "Performance Non-Regression on Query Changes":

- The rewritten query must be **equal or better** on rows examined, access `type`, index usage, `filesort` / `temporary` avoidance, and latency.
- If a proposal is unavoidably **slower** than the original (e.g. a correctness fix that widens the row set), do not present it as a clean win — state **why it is slower**, list the **remaining optimization options** (or state that none exist and why), and the **trade-off that justifies it**.

Recommend only justified changes, such as:
- query rewrite to reuse an existing schema index (preferred — verify which indexes already exist via migrations / `SHOW INDEX` before proposing a new one; reorder `WHERE` / `JOIN` / `ORDER BY` columns to match an existing composite index, drop functions wrapping indexed columns, and project only columns the index already covers)
- query rewrite (general)
- Eloquent/query builder rewrite
- eager loading change
- pagination change
- batching per-row loops into a single bulk operation — ModelManager batch methods (`batchUpdate`, `batchInsert`), `whereIn(...)->delete()` for deletes, or one bulk read keyed in memory for lookups (see `@rules/sql/optimalize.md` "Batch over per-row operations")
- index addition or replacement (only when the existing schema cannot cover the query and EXPLAIN confirms the gap after the rewrite alternative has been ruled out)
- redundant index removal
- splitting one query into smaller ones
- online schema change for a blocking DDL statement — name `ALGORITHM=INPLACE, LOCK=NONE`, or route the statement through `pt-online-schema-change` / `gh-ost` when it cannot run online, and move any backfill into its own chunked, re-runnable command

Explain trade-offs:
- write overhead
- duplicate indexes
- over-indexing
- complexity vs benefit

## Laravel-Specific Checks
When the input is Laravel code, also inspect:
- `with()` / eager loading
- `whereHas()` / nested filters
- `withCount()`
- `chunk()` vs `cursor()` vs pagination
- scopes hiding query complexity
- repeated queries in loops

## Terminal Guidance
When terminal access is available, inspect DB connection details from:
- `.env`
- `config/database.php`
- docker/dev setup

Use MySQL tools when possible for:
- `SHOW CREATE TABLE`
- `SHOW INDEX`
- `EXPLAIN`

If access fails, continue statically and say so.

## Output Format

Use the template defined in `templates/analysis-report.md`. In `MODE=cr-report`, use `templates/cr-report.md` instead.
---

## Principles

- Focus on the real bottleneck, not generic SQL advice
- Prefer evidence from EXPLAIN over assumptions
- Validate schema and index usage before proposing changes
- Avoid unnecessary or duplicate indexes
- Explain trade-offs (read vs write cost, complexity vs benefit)
- Be concise, practical, and explicit about limitations

## Output Humanization
- Use [blader/humanizer](https://github.com/blader/humanizer) for all skill outputs to keep the text natural and human-friendly.
