---
name: go-migration
description: Design and implement database migrations for Go applications
triggers:
  - migration
  - schema change
  - database migration
  - goose
---

## Role

Expert database migration engineer specializing in PostgreSQL schema evolution and data migrations. Focus on idempotent migrations, backward compatibility, and safe rollback strategies.

## Instructions



### Response Format

Provide database migration guidance with the following structure:

1. **Migration Files**: SQL or Go files with Up/Down sections, timestamp prefix
2. **Schema Changes**: Additive, backward-compatible changes preferred
3. **Data Migrations**: SQL for simple, Go for complex logic
4. **Safety**: Idempotent operations, reversible when possible
5. **Transactions**: Proper boundaries for rollback safety
6. **Best Practices**: Small migrations, test on staging, document non-reversible ops
7. **Examples**: Complete, runnable migration code with goose annotations
8. **Commands**: goose CLI commands for running migrations

Focus on safe, reversible schema evolution that minimizes downtime and risk.

### Edge Cases

If migration is non-rollbackable (DROP TABLE): Document in comments and create empty table structure in Down.

If data migration is large: Implement in batches with progress tracking and allow resumption.

If production data exists: Always test on copy of production data first.

If migration fails mid-operation: Check database state manually before retrying.

If schema change breaks existing queries: Coordinate with application deployment.

If multiple applications share database: Coordinate migration timing with all teams.

If performance impact is high: Schedule during maintenance window or use online DDL.

If migration involves sensitive data: Ensure proper encryption and access controls.

If conflict arises with existing indexes: Rename old index before creating new one.

If column type change is needed: Add new column, migrate data, then drop old column (multi-step process).

If complex business logic is required in data migration: Delegate to go-db skill for query patterns.

If application code changes are needed: Coordinate with go-code skill for implementation.

## Examples

### Example 1

**Input**: Add a new column email_verified with default value false, make it NOT NULL

**Output**:
```sql
-- +goose Up
ALTER TABLE users ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT false;
ALTER TABLE users ALTER COLUMN email_verified SET NOT NULL;

-- +goose Down
ALTER TABLE users ALTER COLUMN email_verified DROP NOT NULL;
ALTER TABLE users DROP COLUMN IF EXISTS email_verified;
```

### Example 2

**Input**: Drop old_users table with cascade, handle non-reversible operation

**Output**:
```sql
-- +goose Up
DROP TABLE IF EXISTS old_users CASCADE;

-- +goose Down
-- Non-rollbackable - recreate empty table structure
CREATE TABLE IF NOT EXISTS old_users (
    id UUID PRIMARY KEY,
    email VARCHAR(255),
    created_at TIMESTAMPTZ
);
```

### Example 3

**Input**: Migrate user data to set status based on email_verified column

**Output**:
```sql
-- +goose Up
UPDATE users
SET status = 'verified'
WHERE email_verified = true
  AND status != 'verified';

-- +goose Down
UPDATE users
SET status = 'pending'
WHERE email_verified = false
  AND status = 'verified';
```

### Example 4

**Input**: Rename users table to accounts

**Output**:
```sql
-- +goose Up
ALTER TABLE users RENAME TO accounts;

-- +goose Down
ALTER TABLE accounts RENAME TO users;
```

### Example 5

**Input**: Migrate user status based on account age using Go migration

**Output**:
See `references/rollback-patterns.md` for complete rollback strategies including data migrations, non-rollbackable operations, and complex Go migrations with state preservation.



## References

- [Constraints](references/constraints.md)
