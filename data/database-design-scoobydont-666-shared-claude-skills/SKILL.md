---
name: database-design
description: >
  Schema design, migration strategy, index planning, and data lifecycle for SQL databases
  (PostgreSQL, SQLite). Covers table design, normalization, foreign keys, migration tooling
  (Alembic, raw SQL), index optimization, retention policies, and schema review.
  Trigger on: "design schema", "database migration", "add table", "schema review",
  "index strategy", "data model", "retention policy", "normalize".
---

# Database Design & Schema Management

## When to Use

- Designing a new database schema or adding tables
- Reviewing an existing schema for correctness, performance, or security
- Planning migrations (especially for production data)
- Designing indexes for query patterns
- Defining retention/deletion policies for sensitive data
- Evaluating SQLite vs PostgreSQL for a given use case

## SQLite vs PostgreSQL Decision

| Factor | SQLite | PostgreSQL |
|--------|--------|------------|
| Single-user/process | Yes | Overkill |
| Multi-tenant | No | Yes |
| Multi-process writes | No (WAL helps reads) | Yes |
| Sensitive data needing RBAC | No | Yes (row-level security) |
| Schema migrations needed | Manual/limited | Alembic, full ALTER support |
| Production deployment | Embedded only | Always appropriate |
| Full-text search | FTS5 (basic) | tsvector/tsquery (rich) |
| JSON queries | json_extract (basic) | jsonb (rich, indexed) |

**Rule:** If multi-tenant or handling financial/PII data → PostgreSQL. No exceptions.

## Schema Design Checklist

### 1. Table Design
```
□ Every table has a clear, singular purpose
□ Primary key defined (prefer INTEGER AUTOINCREMENT or UUID, not natural keys)
□ Foreign keys declared with ON DELETE behavior (CASCADE, SET NULL, RESTRICT)
□ NOT NULL on every column that should never be empty
□ DEFAULT values for columns with sensible defaults
□ No VARCHAR without length limit on user-facing input
□ Created_at and updated_at timestamps on every mutable table
□ No redundant data that can be derived from joins
```

### 2. Naming Conventions
```
□ Tables: plural snake_case (users, audit_events, context_chunks)
□ Columns: singular snake_case (user_id, created_at, token_count)
□ Foreign keys: {referenced_table_singular}_id (user_id, blob_hash)
□ Indexes: idx_{table}_{columns} (idx_users_email, idx_chunks_hash_index)
□ Constraints: {type}_{table}_{columns} (uq_aliases_alias_namespace, fk_chunks_hash)
```

### 3. Normalization
- **1NF:** No repeating groups, no arrays in columns (use junction tables)
- **2NF:** Every non-key column depends on the full primary key
- **3NF:** No transitive dependencies (column A → column B → column C)
- **Denormalize intentionally** only for proven performance needs, document why

### 4. Index Strategy
```
□ Primary keys are automatically indexed
□ Foreign keys need explicit indexes (PostgreSQL does NOT auto-index FK columns)
□ Add indexes for WHERE, JOIN, ORDER BY columns in hot queries
□ Composite indexes: leftmost column must be the most selective
□ Covering indexes for read-heavy queries (include all SELECT columns)
□ Partial indexes for queries that filter on a constant (WHERE status = 'active')
□ Do NOT index columns with low cardinality (boolean, enum with 3 values)
□ Do NOT index columns that are rarely queried
```

### 5. Multi-Tenant Isolation
```
□ Tenant ID column on every tenant-scoped table
□ Every query includes WHERE tenant_id = ? (no exceptions)
□ Composite unique constraints include tenant_id: UNIQUE(alias, tenant_id)
□ Row-level security (PostgreSQL) or application-level enforcement
□ Test: Tenant A cannot read Tenant B's data (explicit cross-tenant test)
□ Indexes include tenant_id as prefix for tenant-scoped queries
```

### 6. Sensitive Data
```
□ PII columns identified and documented
□ Encryption-at-rest for SSN, EIN, account numbers (application-level Fernet or PG pgcrypto)
□ No PII in indexes (encrypted columns cannot be indexed — use blind index pattern)
□ Retention policy defined: how long, auto-delete mechanism, audit trail for deletions
□ Audit log table: who accessed what, when, from where (append-only, no DELETE permission)
□ Backup encryption for database dumps containing PII
```

## Migration Strategy

### Alembic (Python/SQLAlchemy)
```bash
# Initialize
alembic init alembic

# Create migration from model changes
alembic revision --autogenerate -m "add user_roles table"

# Apply
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Migration Safety Rules
```
□ Never DROP COLUMN in production without a deprecation period
□ Add columns as NULLABLE first, backfill, then add NOT NULL constraint
□ Rename via: add new column → copy data → drop old column (not ALTER RENAME)
□ Large data migrations: batch in chunks (1000-10000 rows) to avoid lock contention
□ Always test migration AND rollback on a copy of production data
□ Migrations must be idempotent (safe to run twice)
□ No data-dependent migrations in the same transaction as schema changes
```

### SQLite Migrations (No Alembic)
SQLite has limited ALTER TABLE support. For schema changes:
1. Create new table with desired schema
2. Copy data from old table
3. Drop old table
4. Rename new table to old name
5. Recreate indexes and triggers

Wrap in a transaction. Test on a copy first.

## Schema Review Protocol

When reviewing an existing schema:

1. **Read the migration files or CREATE TABLE statements**
2. **Map entity relationships** — draw the FK graph mentally
3. **Check for missing indexes** on FK columns and WHERE clause columns
4. **Check for missing constraints** — can invalid data be inserted?
5. **Check tenant isolation** — is tenant_id on every tenant-scoped table? In every query?
6. **Check for PII** — is sensitive data identified and protected?
7. **Check for orphans** — can rows exist without their parent? (missing ON DELETE CASCADE)
8. **Check for N+1 patterns** — are related entities fetched in loops instead of JOINs?
9. **Output:** findings table with severity (Critical/High/Medium/Low) and recommended fix

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Fix |
|-------------|-------------|-----|
| EAV (Entity-Attribute-Value) | Unqueryable, no type safety | Proper columns or JSONB |
| Soft deletes everywhere | Accumulates garbage, complicates queries | Hard delete + audit log |
| UUID primary keys on large tables | 4x storage, worse cache locality | BIGINT + UUID as alternate key |
| Storing JSON blobs for structured data | No referential integrity | Normalize into tables |
| Missing ON DELETE behavior | Orphaned rows | Explicit CASCADE/RESTRICT |
| Composite primary keys on 3+ columns | Awkward FK references, join complexity | Surrogate key + unique constraint |

## Integration

- **tdd:** Write schema tests first (can I insert valid data? rejected invalid data?)
- **code-quality:** N+1 queries and missing indexes are performance findings
