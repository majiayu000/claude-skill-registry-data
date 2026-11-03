---
name: postgresql
description: PostgreSQL gotchas and version-gated facts - indexing (B-tree, GIN, GiST, BRIN, partial, expression), JSONB, EXPLAIN ANALYZE and tuning, row-level security and multi-tenancy, full-text search, partitioning, connection pooling, extensions, logical replication, pgvector and RAG. Use when designing tables or indexes for PostgreSQL, writing or reviewing raw SQL, diagnosing a slow query, or choosing a PostgreSQL feature. For EF Core query performance use the optimizing-ef-core-queries skill; for migrations follow the ef-migrations rule.
---

# PostgreSQL

Each reference lists what models get wrong about one area, with version gates and anti-hallucination rules. Read only the reference that matches the task; read several when the task spans them (a slow JSONB query needs both `jsonb-patterns` and `query-performance`).

| Task | Reference |
|---|---|
| Choosing or reviewing an index | [references/postgresql-advanced-indexing.md](references/postgresql-advanced-indexing.md) |
| Slow query, reading `EXPLAIN ANALYZE`, server settings | [references/postgresql-query-performance.md](references/postgresql-query-performance.md) |
| JSONB columns, operators, indexing, updates | [references/postgresql-jsonb-patterns.md](references/postgresql-jsonb-patterns.md) |
| Row-level security, tenant isolation | [references/postgresql-row-level-security.md](references/postgresql-row-level-security.md) |
| Full-text search (`tsvector`, `tsquery`, ranking) | [references/postgresql-full-text-search.md](references/postgresql-full-text-search.md) |
| Partitioning large tables | [references/postgresql-table-partitioning.md](references/postgresql-table-partitioning.md) |
| Connection pooling, exhaustion, timeouts | [references/postgresql-connection-management.md](references/postgresql-connection-management.md) |
| Installing or upgrading extensions | [references/postgresql-extensions.md](references/postgresql-extensions.md) |
| Logical replication | [references/postgresql-replication.md](references/postgresql-replication.md) |
| Vector similarity search with pgvector | [references/postgresql-vector-search.md](references/postgresql-vector-search.md) |
| RAG, hybrid search | [references/postgresql-genai-rag.md](references/postgresql-genai-rag.md) |

- Check the server version (`SELECT version();`) before recommending a version-gated feature.
- Schema changes (indexes, extensions, RLS policies, partitions) go through EF Core migrations, raw SQL in `migrationBuilder.Sql(...)` where EF has no API, following the `ef-migrations` rule. Don't apply DDL directly to a database.
