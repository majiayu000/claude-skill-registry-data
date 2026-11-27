---
name: efcore-data
description: "Design and review EF Core persistence, indexing, concurrency, data ownership, migrations, and SQL performance."
---

# EF Core data review
- Read provider/version, DbContext lifetime, mappings, SQL constraints and migration history; do not assume DBMS.
- Validate tenant ownership, unique constraints, FKs, optimistic concurrency and required transaction boundaries.
- For reads: projection, index use, N+1 risk, AsNoTracking as suited, paging order, query translation, split-vs-single query.
- For writes: concurrency token/row version, idempotency, single SaveChanges vs transaction, rollback/side effects.
- For migrations: expand/contract, data backfill, downtime estimate, large table lock, backup/restore and deployment compatibility.
- For data faults: reproduce with real provider and Testcontainers; do not depend only on InMemory EF tests.
- Recommend performance claims only with representative query plans/timings; describe measurement steps when unavailable.
- Reference `knowledge/EFCORE_DATABASES.md`.
