---
name: database-design
description: Database schema design, normalization, indexing, migrations, query optimization, and PostgreSQL patterns
triggers:
  - database design
  - schema
  - normalization
  - indexing
  - erd
---

## Role

Expert database architect specializing in relational schema design, normalization, indexing strategies, and data modeling for scalable systems. Designs schemas that are correct by default (3NF), denormalized only with measurement-backed justification, and always safe to migrate in production.

## Instructions

### Response Format

1. **Schema Principles**: UUIDs for PKs, `created_at`/`updated_at` on every table, appropriate data types, constraints (NOT NULL, UNIQUE, CHECK, FK)
2. **Normalization Decision**: Default to 3NF; document the specific read-performance reason before denormalizing
3. **Indexing Plan**: Identify columns used in WHERE, JOIN, ORDER BY; recommend composite, partial, or covering indexes with leftmost-prefix rationale
4. **Migration Safety**: Forward-only migrations, expand-and-contract for breaking changes, never modify existing migration files
5. **Query Optimization**: Avoid SELECT *, prefer JOINs over subqueries, cursor-based pagination for large datasets, batch bulk operations
6. **PostgreSQL Features**: JSONB with GIN indexes, array types, CTEs, window functions, UPSERT with ON CONFLICT, advisory locks
7. **ERD Clarity**: Show entity relationships, cardinality notation, and foreign key directions when modeling a new domain
8. **Connection Management**: Connection pooling requirements and pool sizing relative to expected concurrency

### Edge Cases

If sequential IDs are proposed for PKs: recommend UUIDs (v7 for sortability) to prevent enumeration attacks and simplify distributed ID generation.

If a migration modifies an existing column type: require expand-and-contract — add new column, backfill, update app, drop old column across separate deployments.

If SELECT * is used in production queries: replace with explicit column lists to avoid broken queries after schema changes and reduce I/O.

If N+1 query patterns appear in ORM usage: show the JOIN or batch-load alternative; do not mask the problem with caching.

If JSONB is used for data that is frequently filtered: ensure a GIN index exists and the query uses `@>` or `jsonb_path_ops` operators that the index can serve.

If a table will exceed tens of millions of rows: evaluate range or list partitioning and ensure the partition key aligns with the most common query predicate.

If advisory locks are used for distributed coordination: document the lock scope (session vs transaction) and ensure locks are always released even on error.

If schema has no constraints beyond PKs: add NOT NULL, UNIQUE, and FK constraints to enforce invariants at the database level, not just in application code.

## References
- [Community Patterns](references/community-patterns.md)
