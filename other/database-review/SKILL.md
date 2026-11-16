---
name: database-review
description: Design or review relational database schemas and queries. Use when changing tables, indexes, migrations, transactions, access policies, or query performance.
---

# Database Review

Start from data integrity and observed query patterns, not from speculative indexing.

1. Inspect schema, constraints, data volume assumptions, migration history, and real query plans where available.
2. Check keys, nullability, uniqueness, foreign keys, normalization/denormalization trade-offs, and ownership of derived data.
3. Review indexes against query predicates, joins, ordering, cardinality, and write overhead.
4. Examine transactions, isolation, lock duration, retry safety, and concurrent updates.
5. Check authorization at the data boundary, including row-level policies where used; do not assume application checks are sufficient.
6. Plan migrations for existing data, rollback limits, backfills, and mixed-version deployments.
7. Validate changes with representative queries, tests, and `EXPLAIN`/query-plan evidence when possible.

Never run destructive migrations or queries against production without explicit authorization and a verified backup/rollback plan. Do not invent database statistics or performance improvements.
