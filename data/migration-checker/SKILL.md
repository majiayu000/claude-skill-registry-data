---
name: migration-checker
description: |
  WHEN: Database migration review, backwards compatibility, rollback safety, data integrity
  WHAT: Migration safety + Rollback validation + Downtime analysis + Data preservation + Lock prevention
  WHEN NOT: Query optimization → sql-optimizer, Schema design → schema-reviewer
---

# Migration Checker Skill

## Purpose
Reviews database migrations for safety, backwards compatibility, rollback capability, and zero-downtime deployment.

## When to Use
- Database migration review
- Schema change safety check
- Rollback plan validation
- Zero-downtime deployment check
- Data migration review

## Project Detection
- `migrations/` directory
- Prisma migrations
- Alembic (Python)
- TypeORM migrations
- Rails migrations
- Flyway/Liquibase

## Workflow

### Step 1: Analyze Migration
```
**Type**: Schema change / Data migration
**Risk Level**: High (adds non-nullable column)
**Tables Affected**: users, orders
**Estimated Rows**: 1M+
```

### Step 2: Select Review Areas
**AskUserQuestion:**
```
"Which areas to review?"
Options:
- Full migration review (recommended)
- Backwards compatibility
- Rollback safety
- Lock and downtime analysis
- Data integrity
multiSelect: true
```

## Detection Rules

### Dangerous Operations
| Operation | Risk | Mitigation |
|-----------|------|------------|
| Add NOT NULL without default | CRITICAL | Add default or multi-step |
| Drop column | HIGH | Ensure no code references |
| Rename column | HIGH | Use multi-step migration |
| Change column type | HIGH | Check data compatibility |
| Add unique constraint | HIGH | Verify no duplicates first |
| Drop table | CRITICAL | Ensure no references |

### Adding Non-Nullable Column

```sql
-- BAD: Direct NOT NULL column (will fail on existing rows)
ALTER TABLE users ADD COLUMN phone VARCHAR(20) NOT NULL;
-- ERROR: column "phone" contains null values

-- GOOD: Multi-step migration
-- Step 1: Add nullable column
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- Step 2: Backfill data (in batches for large tables)
UPDATE users SET phone = 'unknown' WHERE phone IS NULL;

-- Step 3: Add NOT NULL constraint
ALTER TABLE users ALTER COLUMN phone SET NOT NULL;
```

### Renaming Columns (Zero-Downtime)

```sql
-- BAD: Direct rename (breaks running code)
ALTER TABLE users RENAME COLUMN name TO full_name;
-- Old code still uses "name"!

-- GOOD: Multi-step migration

-- Migration 1: Add new column
ALTER TABLE users ADD COLUMN full_name VARCHAR(200);

-- Migration 2: Sync data (application writes to both)
UPDATE users SET full_name = name WHERE full_name IS NULL;

-- Deploy: Update code to read from full_name

-- Migration 3: Drop old column (after code deployment)
ALTER TABLE users DROP COLUMN name;
```

### Index Operations

```sql
-- BAD: Regular CREATE INDEX (blocks writes)
CREATE INDEX idx_orders_user_id ON orders(user_id);
-- Locks table for duration!

-- GOOD: Concurrent index (PostgreSQL)
CREATE INDEX CONCURRENTLY idx_orders_user_id ON orders(user_id);
-- Doesn't block writes, but takes longer

-- Note: CONCURRENTLY cannot be in transaction
-- Must be separate migration without transaction wrapper
```

### Data Migrations

```python
# BAD: Load all data into memory
def migrate():
    users = User.objects.all()  # 1M rows in memory!
    for user in users:
        user.email = user.email.lower()
        user.save()

# GOOD: Batch processing
def migrate():
    batch_size = 1000
    total = User.objects.count()

    for offset in range(0, total, batch_size):
        users = User.objects.all()[offset:offset + batch_size]
        for user in users:
            user.email = user.email.lower()
        User.objects.bulk_update(users, ['email'])

# BETTER: Raw SQL for large tables
def migrate():
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE users
            SET email = LOWER(email)
            WHERE id IN (
                SELECT id FROM users
                WHERE email != LOWER(email)
                LIMIT 10000
            )
        """)
```

### Prisma Migration Safety

```typescript
// schema.prisma

// BAD: Direct non-nullable addition
model User {
  id    Int    @id @default(autoincrement())
  email String
  phone String  // New non-nullable field - will fail!
}

// GOOD: Add with default first
model User {
  id    Int    @id @default(autoincrement())
  email String
  phone String @default("")  // Safe to add
}

// Or nullable first, then make required
model User {
  id    Int     @id @default(autoincrement())
  email String
  phone String?  // Step 1: nullable
}
```

### TypeORM Migration

```typescript
// BAD: Unsafe migration
export class AddUserPhone1234567890 implements MigrationInterface {
    async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(
            `ALTER TABLE users ADD phone VARCHAR(20) NOT NULL`
        );
    }

    async down(queryRunner: QueryRunner): Promise<void> {
        // No rollback!
    }
}

// GOOD: Safe migration with rollback
export class AddUserPhone1234567890 implements MigrationInterface {
    async up(queryRunner: QueryRunner): Promise<void> {
        // Step 1: Add nullable column
        await queryRunner.query(
            `ALTER TABLE users ADD phone VARCHAR(20)`
        );

        // Step 2: Backfill
        await queryRunner.query(
            `UPDATE users SET phone = '' WHERE phone IS NULL`
        );

        // Step 3: Add constraint
        await queryRunner.query(
            `ALTER TABLE users ALTER COLUMN phone SET NOT NULL`
        );
    }

    async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(
            `ALTER TABLE users DROP COLUMN phone`
        );
    }
}
```

### Django Migrations

```python
# BAD: RunPython without reverse
class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(forwards_func),  # No reverse!
    ]

# GOOD: With reverse operation
class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(
            forwards_func,
            reverse_code=backwards_func
        ),
    ]

# BAD: Atomic migration for large data change
class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(update_millions_of_rows),
    ]

# GOOD: Non-atomic for large changes
class Migration(migrations.Migration):
    atomic = False

    operations = [
        migrations.RunPython(update_in_batches),
    ]
```

### Rollback Checklist

```sql
-- Verify rollback for each operation

-- ADD COLUMN → DROP COLUMN
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
-- Rollback: ALTER TABLE users DROP COLUMN phone;

-- ADD CONSTRAINT → DROP CONSTRAINT
ALTER TABLE orders ADD CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id);
-- Rollback: ALTER TABLE orders DROP CONSTRAINT fk_user;

-- CREATE INDEX → DROP INDEX
CREATE INDEX idx_email ON users(email);
-- Rollback: DROP INDEX idx_email;

-- RENAME COLUMN → Complex (need old column back)
-- Better to use add/copy/drop pattern
```

### Lock Analysis

```sql
-- PostgreSQL: Check what operations lock tables
-- https://www.postgresql.org/docs/current/explicit-locking.html

-- ACCESS EXCLUSIVE (blocks everything):
-- - DROP TABLE
-- - ALTER TABLE ... ADD COLUMN with DEFAULT (< PG 11)
-- - ALTER TABLE ... ALTER COLUMN TYPE

-- SHARE UPDATE EXCLUSIVE (blocks DDL, allows DML):
-- - CREATE INDEX CONCURRENTLY
-- - VACUUM

-- Check for blocking locks before migration
SELECT blocked_locks.pid AS blocked_pid,
       blocked_activity.usename AS blocked_user,
       blocking_locks.pid AS blocking_pid,
       blocking_activity.usename AS blocking_user,
       blocked_activity.query AS blocked_statement
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity
    ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks
    ON blocking_locks.locktype = blocked_locks.locktype
WHERE NOT blocked_locks.granted;
```

## Response Template
```
## Migration Review Results

**Migration**: 20240115_add_user_phone
**Type**: Schema change
**Risk Level**: HIGH

### Safety Analysis
| Status | Issue | Impact |
|--------|-------|--------|
| CRITICAL | Non-nullable column without default | Migration will fail |
| HIGH | No rollback operation defined | Cannot revert |
| MEDIUM | Missing concurrent index | Table lock during creation |

### Lock Analysis
| Operation | Lock Type | Duration |
|-----------|-----------|----------|
| ADD COLUMN | ACCESS EXCLUSIVE | Brief |
| CREATE INDEX | ACCESS EXCLUSIVE | Long (use CONCURRENTLY) |

### Rollback Plan
- [ ] Add rollback script
- [ ] Test rollback in staging
- [ ] Document manual rollback steps

### Recommended Changes
```sql
-- Step 1: Add nullable column
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- Step 2: Backfill data
UPDATE users SET phone = '' WHERE phone IS NULL;

-- Step 3: Add NOT NULL
ALTER TABLE users ALTER COLUMN phone SET NOT NULL;

-- Rollback
ALTER TABLE users DROP COLUMN phone;
```

### Pre-Migration Checklist
- [ ] Backup database
- [ ] Test in staging with production data
- [ ] Schedule during low-traffic period
- [ ] Notify team of potential downtime
- [ ] Prepare rollback script
```

## Best Practices
1. **Multi-Step**: Break dangerous operations into steps
2. **Rollback**: Always define down/reverse migration
3. **Concurrent**: Use CONCURRENTLY for indexes
4. **Batching**: Process large data in chunks
5. **Testing**: Test with production-like data volume

## Integration
- `schema-reviewer`: Schema design review
- `sql-optimizer`: Query performance
- `ci-cd-reviewer`: Migration in pipelines
