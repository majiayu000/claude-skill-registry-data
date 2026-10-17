---
name: sql-engineering
description: Design and write SQL that scales — schema constraints, indexes, transactions, safe migrations, no N+1.
version: 1
triggers: sql, database schema, indexes, transactions, query, database design
category: Engineering & code
blurb: Design and write SQL that scales — constraints, indexes, transactions and safe migrations.
archetype: knowledge
example: Design this database schema so it stays fast and safe.
---

# SQL Engineering

The database is the last line of correctness: enforce rules in the schema, write set-based queries, and treat migrations like surgery.

## When to use
- Schema design or changes; query writing and performance work.
- Reviewing data-layer code; designing migrations.

## Method
1. **Schema first**: precise types; `NOT NULL` by default; `CHECK`/`FK` constraints in the database — not just in app code; consistent naming (snake_case).
2. **Indexes from queries**: derive from real access patterns; composite column order matters; over-indexing costs writes — measure.
3. **Queries**: explicit column lists (no `SELECT *` in app code); set-based thinking; CTEs and window functions for complex reads; paginate large results.
4. **Avoid N+1**: join, batch, or preload — verify with query counts in tests.
5. **Transactions**: keep them short; know your isolation level; expect and handle deadlocks (retry with backoff).
6. **Safety**: parameterized queries only — never string-built SQL with input; rehearsed, bounded `UPDATE`/`DELETE` (no missing `WHERE`).
7. **Migrations**: forward + rollback scripts; test on a copy; expand→migrate→contract for zero-downtime; one logical change per migration.
8. **Performance**: `EXPLAIN ANALYZE` before and after for heavy changes; watch plan regressions.

## Quality gates
- [ ] New queries use parameters; heavy ones have EXPLAIN evidence.
- [ ] Constraints exist in the schema; migrations carry rollback + were tested.
- [ ] No N+1 patterns introduced (query-count tests).
- [ ] Unbounded scans avoided (limits/pagination).

## Red lines
- No unreviewed migration on live data; no direct-to-prod schema edits.
- No string-concatenated SQL with user input — injection is a firing offense.

## Related
`backend-engineering` · `testing-strategy` · `architecture-decisions`.
