---
name: safe-migrate
description: Safely creates and applies database migrations with automatic destructive operation detection, backup creation, and rollback generation. This skill should be used when creating database migrations, applying schema changes, or performing any database DDL operations. Essential for preventing data loss.
---

# Safe Migrate

This skill provides a safety wrapper around database migrations to prevent data loss and enable safe rollbacks. Created in response to the `title_content_analysis` data loss incident (2025-11-04).

## When to Use This Skill

- Creating new database migrations
- Applying migrations to staging or production
- Performing any DDL operations (ALTER, DROP, TRUNCATE)
- Rolling back problematic migrations

## Critical Safety Rules

Following the 2025-11-04 data loss incident, these rules are MANDATORY:

1. **NEVER use `DROP TABLE`** for schema changes - use `ALTER TABLE` with data migration
2. **NEVER run destructive migrations** without backup
3. **NEVER skip staging tests** for destructive operations
4. **ALWAYS use this skill** for migration creation and application

## Commands

```
/safe-migrate create add_user_preferences     # Create new migration
/safe-migrate analyze [migration-file]        # Analyze for risks
/safe-migrate apply [migration-file]          # Apply with safety checks
/safe-migrate apply --production              # Apply to production (extra checks)
/safe-migrate rollback [migration-file]       # Generate rollback migration
/safe-migrate backup [table-name]             # Backup specific table
```

## Migration Creation Workflow

### Step 1: Create Migration File

```bash
# Always run from root directory
cd /Users/sungholee/code/kstorybridge

# Create migration with timestamp
npx supabase migration new [migration_name]
```

This creates: `supabase/migrations/[timestamp]_[migration_name].sql`

### Step 2: Analyze for Destructive Operations

Before writing SQL, understand the operation type:

**Safe Operations** (no backup required):
- `CREATE TABLE`
- `CREATE INDEX`
- `ALTER TABLE ... ADD COLUMN`
- `INSERT INTO`
- `CREATE FUNCTION`
- `COMMENT ON`

**Destructive Operations** (backup REQUIRED):
- `DROP TABLE`
- `DROP COLUMN`
- `TRUNCATE`
- `DELETE FROM` (without WHERE or bulk)
- `ALTER TYPE`
- `ALTER COLUMN ... TYPE`
- `UPDATE` (bulk updates)

### Step 3: Write Migration with Safety Header

All migrations should include a safety header:

```sql
-- Migration: [timestamp]_[name].sql
-- Created: YYYY-MM-DD
-- Author: [name]
-- Status: IN_PROGRESS | COMPLETED | DEPRECATED
--
-- Description:
-- [What this migration does]
--
-- Risk Level: LOW | MEDIUM | HIGH | CRITICAL
-- Destructive: YES | NO
--
-- Affected Tables:
-- - [table_name] ([row count] rows)
--
-- Backup Required: YES | NO
-- Backup Created: [backup file path]
--
-- Rollback Procedure:
-- [How to undo this migration]
--
-- Testing:
-- [ ] Tested locally
-- [ ] Tested in staging
-- [ ] Verified row counts
-- [ ] Verified data integrity
```

### Step 4: For Destructive Operations - Create Backup

Before ANY destructive operation:

```bash
# Create backup directory if needed
mkdir -p supabase/backups

# Get row count before backup
psql "$DATABASE_URL" -c "SELECT COUNT(*) FROM [table_name];"

# Export table to backup file
pg_dump "$DATABASE_URL" \
  --table=[table_name] \
  --data-only \
  --format=custom \
  --file=supabase/backups/[table_name]_$(date +%Y%m%d_%H%M%S).dump

# Or using SQL export
psql "$DATABASE_URL" -c "COPY [table_name] TO STDOUT WITH CSV HEADER" \
  > supabase/backups/[table_name]_$(date +%Y%m%d_%H%M%S).csv
```

### Step 5: Generate Rollback Migration

For every migration, create a corresponding rollback:

```sql
-- Rollback: [timestamp]_[name]_rollback.sql
-- Reverts: [timestamp]_[name].sql
--
-- Instructions:
-- 1. Apply this migration to revert changes
-- 2. Verify data integrity after rollback
-- 3. Check application functionality

-- Rollback SQL here
```

## Safe Schema Change Patterns

### Adding a Column (SAFE)

```sql
-- Adding a column is always safe
ALTER TABLE users
ADD COLUMN preferences JSONB DEFAULT '{}';
```

### Renaming a Column (MEDIUM RISK)

```sql
-- Step 1: Add new column
ALTER TABLE users ADD COLUMN new_name TEXT;

-- Step 2: Copy data
UPDATE users SET new_name = old_name;

-- Step 3: Add NOT NULL if needed (after data migration)
ALTER TABLE users ALTER COLUMN new_name SET NOT NULL;

-- Step 4: Drop old column (in SEPARATE migration after verification)
-- ALTER TABLE users DROP COLUMN old_name;
```

### Changing Column Type (HIGH RISK)

```sql
-- NEVER do this directly:
-- ALTER TABLE users ALTER COLUMN age TYPE INTEGER;

-- INSTEAD:
-- Step 1: Add new column with new type
ALTER TABLE users ADD COLUMN age_int INTEGER;

-- Step 2: Migrate data
UPDATE users SET age_int = CAST(age AS INTEGER) WHERE age ~ '^\d+$';

-- Step 3: Verify data
-- SELECT COUNT(*) FROM users WHERE age_int IS NULL AND age IS NOT NULL;

-- Step 4: Rename columns (in SEPARATE migration)
-- ALTER TABLE users RENAME COLUMN age TO age_old;
-- ALTER TABLE users RENAME COLUMN age_int TO age;

-- Step 5: Drop old column (in SEPARATE migration)
-- ALTER TABLE users DROP COLUMN age_old;
```

### Dropping a Table (CRITICAL RISK)

```sql
-- NEVER use DROP TABLE directly!

-- INSTEAD:
-- Step 1: Rename to deprecated
ALTER TABLE old_table RENAME TO _deprecated_old_table;

-- Step 2: Wait 30 days for issues to surface

-- Step 3: Create backup before final drop
-- pg_dump --table=_deprecated_old_table ...

-- Step 4: Drop in separate migration (after 30+ days)
-- DROP TABLE IF EXISTS _deprecated_old_table;
```

## Applying Migrations

### Local Testing

```bash
# Reset local database and apply all migrations
npx supabase db reset

# Check migration status
npx supabase migration list
```

### Staging Application

```bash
# Push to staging (linked project)
npx supabase db push --linked

# Verify application
npx supabase migration list --linked
```

### Production Application

**CRITICAL: Production requires extra verification**

1. **Verify backup exists** for destructive operations
2. **Verify staging test passed**
3. **Get approval** from database admin
4. **Apply during low-traffic window**

```bash
# Push to production
npx supabase db push

# Verify immediately after
npx supabase migration list
```

## Rollback Procedure

If a migration causes issues:

### Immediate Rollback (Within Minutes)

```bash
# If rollback migration exists
npx supabase migration new rollback_[original_name]

# Apply rollback SQL
npx supabase db push
```

### Data Restoration (From Backup)

```bash
# Restore from pg_dump backup
pg_restore --data-only \
  --table=[table_name] \
  --dbname="$DATABASE_URL" \
  supabase/backups/[table_name]_[timestamp].dump

# Or from CSV backup
psql "$DATABASE_URL" -c "\COPY [table_name] FROM 'backup.csv' WITH CSV HEADER"
```

## Analysis Report

When analyzing a migration file, generate this report:

```
## Migration Analysis Report

**File**: 20251225000000_add_preferences.sql
**Lines**: 45

### Risk Assessment

**Risk Level**: MEDIUM
**Destructive Operations**: YES

### Detected Operations

| Line | Operation | Table | Risk |
|------|-----------|-------|------|
| 12 | ALTER TABLE ADD | users | LOW |
| 18 | UPDATE SET | users | MEDIUM |
| 25 | DROP COLUMN | users | HIGH |

### Tables Affected

| Table | Rows | Operation |
|-------|------|-----------|
| users | 1,234 | MODIFY |

### Recommendations

1. CREATE BACKUP before running (users table has 1,234 rows)
2. Test in staging first
3. Consider splitting DROP COLUMN into separate migration
4. Add WHERE clause to UPDATE if possible

### Pre-flight Checklist

- [ ] Backup created for: users
- [ ] Tested locally with `npx supabase db reset`
- [ ] Tested in staging with production-like data
- [ ] Row counts verified before/after
- [ ] Rollback migration prepared
- [ ] Team notified of migration window
```

## Notifications

### Console Output

```
Analyzing migration: 20251225000000_add_preferences.sql

DESTRUCTIVE OPERATIONS DETECTED

  Line 25: DROP COLUMN users.old_field
  Risk: HIGH

BACKUP REQUIRED

Before proceeding, create a backup:
  /safe-migrate backup users

Or run: pg_dump --table=users ...

Continue? (requires --force flag for destructive operations)
```

### Slack Notification

```json
{
  "text": "Migration Applied: 20251225000000_add_preferences.sql",
  "attachments": [
    {
      "color": "warning",
      "fields": [
        {"title": "Risk Level", "value": "MEDIUM", "short": true},
        {"title": "Tables", "value": "users", "short": true},
        {"title": "Backup", "value": "users_20251225.dump", "short": true},
        {"title": "Status", "value": "SUCCESS", "short": true}
      ]
    }
  ]
}
```

## Templates

### Safe Schema Change Template

Use for any schema modifications:

```sql
-- Migration: [timestamp]_[name].sql
-- Risk Level: [LOW/MEDIUM/HIGH]
-- Backup: [path or N/A]

-- Pre-migration verification
DO $$
DECLARE
  row_count INTEGER;
BEGIN
  SELECT COUNT(*) INTO row_count FROM [table_name];
  RAISE NOTICE 'Pre-migration row count for [table_name]: %', row_count;
END $$;

-- Migration statements
[SQL HERE]

-- Post-migration verification
DO $$
DECLARE
  row_count INTEGER;
BEGIN
  SELECT COUNT(*) INTO row_count FROM [table_name];
  RAISE NOTICE 'Post-migration row count for [table_name]: %', row_count;
END $$;
```

### Backup-First Template

Use for destructive operations:

```sql
-- Migration: [timestamp]_[name].sql
-- Risk Level: HIGH/CRITICAL
-- Backup Required: YES
-- Backup Path: supabase/backups/[table]_[timestamp].dump

-- IMPORTANT: Ensure backup exists before running
-- Run: /safe-migrate backup [table_name]

-- Verify backup exists (this will fail if backup is missing)
-- DO $$
-- BEGIN
--   IF NOT EXISTS (SELECT 1 FROM pg_stat_file('supabase/backups/[backup_file]')) THEN
--     RAISE EXCEPTION 'Backup file not found. Create backup before proceeding.';
--   END IF;
-- END $$;

-- Pre-migration state
[verification SQL]

-- Destructive operation
[SQL HERE]

-- Post-migration verification
[verification SQL]

-- Rollback instructions in comments
-- To rollback: pg_restore --table=[table] supabase/backups/[backup_file]
```

## Related Documentation

- [Migration Safety Guide](docs/guides/MIGRATION_SAFETY_GUIDE.md)
- [Migration Testing Protocol](docs/guides/MIGRATION_TESTING_PROTOCOL.md)
- [Migration Documentation Standards](docs/MIGRATION_DOCUMENTATION_STANDARDS.md)

## Related Skills

- `/deploy-functions` - Deploy edge functions after schema changes
- `/gen-types` - Regenerate TypeScript types after migrations
- `/backup-tables` - Create table backups
