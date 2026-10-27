---
name: postgresql-expert
description: "PostgreSQL performance optimization, EXPLAIN ANALYZE, vacuuming strategies, connection pooling, and JSONB indexing."
---

# PostgreSQL Performance & Tuning Protocol

1. Use pg_stat_statements to identify slowest queries.
2. Create GIN indexes for JSONB queries: CREATE INDEX idx_meta ON items USING gin (metadata);
3. Configure connection pooling (PgBouncer) to prevent connection exhaustion.
