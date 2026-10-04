---
name: SQL Explain
description: Analyze a SQL or SQLAlchemy query, explain its execution plan, and identify slow joins, sequential scans, and missing indexes. Triggers on phrases like 'sql explain', 'why is this query slow', 'analyze this query', or when reviewing repository methods under `api/src/db/` or `api/src/services/`. Reports cost estimates, hot spots, and concrete index recommendations.
---

## Purpose

Give backend engineers a fast, deterministic read on a query's plan and likely bottlenecks before they ship it. Simpler-grants-gov runs Postgres in FedRAMP-Moderate; queries on `opportunity`, `application`, and `agency` are read-hot and sensitive to plan regressions.

## When to Invoke

- A repository method or service query is added or modified under `api/src/db/` or `api/src/services/`.
- A developer asks "why is this query slow" or "explain this query".
- Before merging a PR that introduces a new ORM `select` against a large table.
- During a performance investigation, paired with logs.

## When NOT to Invoke

- For migrations — pair with `skill-migration-safety-check`.
- For trivial primary-key lookups.
- As a substitute for production `EXPLAIN ANALYZE`.

## Inputs

- **target**: a raw SQL string, a path to a file containing a SQLAlchemy `select`, or the active editor selection.
- **mode** (optional): `static` (default — no DB) or `live` (run `EXPLAIN` against the local dev DB).

## Procedure

1. Resolve target. If a SQLAlchemy expression, render it via `str(query.compile(dialect=postgresql.dialect(), compile_kwargs={'literal_binds': True}))`.
2. In `static` mode, parse the rendered SQL and run heuristic checks:
   - Tables referenced (extract `FROM`/`JOIN`).
   - Filterable columns (extract `WHERE`/`ON`).
   - For each table, cross-reference `api/src/db/models/` for declared indexes; flag any filter column without an index.
   - Detect `SELECT *` (warn).
   - Detect `OR` across columns of different tables (often defeats indexes).
   - Detect `LIKE '%...%'` leading wildcard (no btree index usage).
   - Detect missing `LIMIT` on user-facing queries (risk of unbounded result sets).
   - Detect N+1 patterns: `for ... in ...: session.execute(select(...))` in the surrounding 30 lines.
3. In `live` mode, additionally execute `EXPLAIN (FORMAT JSON, BUFFERS, ANALYZE OFF)` against `local-db`. Parse:
   - Top-level cost
   - Any `Seq Scan` on tables > 10k rows
   - Any nested loop with > 1000 outer rows
4. Cross-reference `documentation/rules/api-*.md` for project query patterns.
5. Emit the Output Format. Do not modify files or write to the DB.

## Outputs

```
SQL Explain — api/src/services/opportunities/search_service.py::search_opportunities

Rendered SQL:
  SELECT opportunity.id, opportunity.title, agency.name
  FROM opportunity
  JOIN agency ON agency.id = opportunity.agency_id
  WHERE opportunity.posted_date >= '2026-01-01'
    AND opportunity.title ILIKE '%grant%'
  ORDER BY opportunity.posted_date DESC

Static findings (3):
  [WARN]  Leading-wildcard ILIKE on `opportunity.title` defeats btree index
          Fix:  use Postgres trigram (pg_trgm) GIN index, or full-text search
  [WARN]  No LIMIT clause on user-facing query
          Fix:  add `.limit(50)` and pagination cursor
  [INFO]  `opportunity.posted_date` filter — index present? yes (idx_opportunity_posted_date)

Live plan (mode=live):
  Total cost: 14823.42
  Hot spot: Seq Scan on opportunity (cost=0..14000, rows=120000)
  Cause:    leading-wildcard ILIKE forces seq scan despite posted_date index

Recommendations:
  1. Add GIN index: CREATE INDEX CONCURRENTLY idx_opportunity_title_trgm ON opportunity USING gin (title gin_trgm_ops);
  2. Add LIMIT + cursor pagination.
  3. Consider promoting search to OpenSearch (already provisioned).

Block merge: no (advisory)
```

## Safety

- Never executes `INSERT`/`UPDATE`/`DELETE`/`DDL`.
- Live mode runs `EXPLAIN` only — never `EXPLAIN ANALYZE` (which executes the query).
- Never connects to staging or prod DBs.
- Never logs query parameter values that may contain PII.
- Static mode is the default; live mode requires explicit opt-in.

## Examples

**Example 1 — Leading wildcard**
Author writes `ILIKE '%grant%'` against `opportunity.title`. Skill flags the seq-scan risk and recommends pg_trgm.

**Example 2 — N+1 detection**
A list endpoint loops over results and re-queries `agency` per row. Skill flags the pattern and recommends `selectinload(Opportunity.agency)`.

**Example 3 — Live plan confirmation**
In `mode=live`, skill confirms a `Seq Scan` and quotes the cost; recommends a concurrent index.

## Related

- `.cursor/skills/skill-migration-safety-check/` — for the index-creation migration that follows.
- `.cursor/skills/skill-impact-analysis/` — find other call sites of the slow query.
- `documentation/rules/performance.mdc` — query budget guidance.
