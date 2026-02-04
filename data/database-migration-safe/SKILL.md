---
name: database-migration-safe
description: "Use when creating database migrations. Prevents data loss, downtime, and performance issues. Supports PostgreSQL, MySQL, SQLite. Python 3.8+"
author: "Claude Code Learning Flywheel Team"
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob"]
version: 1.0.0
last_verified: "2026-01-01"
tags: ["database", "migrations", "safety", "operations"]
related-skills: []
---

# Skill: Safe Database Migrations

## Purpose
Database changes are high-risk operations. This skill acts as a safety harness to prevent data loss, downtime, and performance issues during schema migrations.

## 1. Negative Knowledge (Critical Blockers)

> **🛑 STOP:** Do not proceed if your plan involves any of these patterns.

| Dangerous Operation | Why It Fails | Safe Alternative |
| :--- | :--- | :--- |
| Renaming columns | Causes downtime, breaks running app | Add new column → backfill → switch code → drop old |
| Renaming tables | Breaks all running queries | Create view → migrate code → rename later |
| Adding NOT NULL without default | Fails on large tables | Add as nullable → backfill → add constraint |
| Default values on large tables | Locks entire table | Add default in application layer first |
| Dropping columns immediately | Breaks running app instances | Deprecate → remove from code → wait → drop |
| Changing column types | Can lose data, slow migration | Add new column → migrate data → drop old |
| Adding indexes on large tables | Locks table for minutes/hours | Use CONCURRENTLY (PostgreSQL) or equivalent |
| Foreign key constraints without index | Slow queries, lock contention | Create index first, then constraint |

## 2. Verified Migration Patterns

### Pattern 1: Renaming a Column (Safe)

**❌ Dangerous Approach:**
```sql
ALTER TABLE users RENAME COLUMN name TO full_name;
```
**Problem:** All running app instances crash immediately.

**✅ Safe Approach (Multi-Step):**

**Step 1: Add new column**
```sql
ALTER TABLE users ADD COLUMN full_name VARCHAR(255);
```

**Step 2: Backfill data**
```sql
UPDATE users SET full_name = name WHERE full_name IS NULL;
-- For large tables, batch this:
-- UPDATE users SET full_name = name WHERE id >= X AND id < Y AND full_name IS NULL;
```

**Step 3: Update application code**
```typescript
// Old code: user.name
// New code: user.full_name || user.name  (supports both)
```
Deploy this version.

**Step 4: Make new column NOT NULL (after backfill complete)**
```sql
ALTER TABLE users ALTER COLUMN full_name SET NOT NULL;
```

**Step 5: Update code to only use new column**
```typescript
// New code: user.full_name
```
Deploy this version.

**Step 6: Drop old column (in separate migration, days/weeks later)**
```sql
ALTER TABLE users DROP COLUMN name;
```

### Pattern 2: Adding NOT NULL Column (Safe)

**❌ Dangerous:**
```sql
ALTER TABLE products ADD COLUMN category_id INT NOT NULL;
```
**Problem:** Fails if table has existing rows.

**✅ Safe:**

**Step 1: Add as nullable with default**
```sql
ALTER TABLE products ADD COLUMN category_id INT;
```

**Step 2: Backfill data**
```sql
UPDATE products SET category_id = 1 WHERE category_id IS NULL;
-- Or more complex logic based on business rules
```

**Step 3: Add NOT NULL constraint (after verification)**
```sql
ALTER TABLE products ALTER COLUMN category_id SET NOT NULL;
```

### Pattern 3: Adding Index Without Locking (PostgreSQL)

**❌ Dangerous:**
```sql
CREATE INDEX idx_users_email ON users(email);
```
**Problem:** Locks table for duration of index creation.

**✅ Safe:**
```sql
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
```
**Benefit:** Allows reads/writes during index creation.

**Note:** For MySQL, use `ALGORITHM=INPLACE, LOCK=NONE` (5.6+)

### Pattern 4: Dropping a Column (Safe)

**✅ Safe Multi-Step Process:**

**Step 1: Stop writing to column**
```typescript
// Remove all code that sets this field
// Keep reads for backwards compatibility
```
Deploy.

**Step 2: Wait for all instances to deploy (1-7 days)**

**Step 3: Remove reads from code**
Deploy.

**Step 4: Drop column in migration**
```sql
ALTER TABLE users DROP COLUMN deprecated_field;
```

## 3. Verified Procedure for All Migrations

### Pre-Migration Checklist

- [ ] **Backup:** Ensure automated backups are working
- [ ] **Test locally:** Run migration against production-like dataset
- [ ] **Validate:** Run migration validator script:
  ```bash
  python .claude/skills/database-migration-safe/scripts/validate_migration.py <migration_file>
  ```
- [ ] **Size check:** If table > 1M rows, verify CONCURRENTLY or batching strategy
- [ ] **Rollback plan:** Document how to revert (within transaction if possible)
- [ ] **Timing:** Schedule during low-traffic window if risky

### Migration Execution

**Step 1: Generate migration file**
```bash
# TypeORM
npm run migration:generate -- -n AddUserEmailIndex

# Sequelize
npx sequelize-cli migration:generate --name add-user-email-index

# Prisma
npx prisma migrate dev --name add-user-email-index
```

**Step 2: Audit migration**
```bash
python .claude/skills/database-migration-safe/scripts/validate_migration.py \
  migrations/20260101_add_user_email_index.sql
```

**Step 3: Apply locally**
```bash
npm run migration:up
# Verify schema with: npm run migration:show
```

**Step 4: Test application**
```bash
npm test
npm run dev  # Manual verification
```

**Step 5: Commit migration**
```bash
git add migrations/
git commit -m "feat(db): add index on users.email for faster lookups"
```

**Step 6: Apply to staging**
```bash
# On staging environment
npm run migration:up
# Verify no errors, check performance
```

**Step 7: Apply to production**
```bash
# On production environment
npm run migration:up
# Monitor logs, database metrics
```

### Post-Migration Verification

- [ ] Check application logs for errors
- [ ] Verify query performance (EXPLAIN ANALYZE)
- [ ] Monitor database metrics (CPU, I/O, locks)
- [ ] Test critical user flows
- [ ] Confirm no data loss (row counts, checksums)

## 4. Zero-Context Scripts

### validate_migration.py

Located at: `.claude/skills/database-migration-safe/scripts/validate_migration.py`

**Purpose:** Automated detection of dangerous migration patterns.

**Usage:**
```bash
python .claude/skills/database-migration-safe/scripts/validate_migration.py <migration_file>
```

**Returns:**
- Exit code 0: Safe migration
- Exit code 1: Dangerous patterns detected
- JSON report of findings

## 5. Failed Attempts (Negative Knowledge Evolution)

### ❌ Attempt: Rename column in single migration
**Context:** Renamed `user.email` to `user.email_address` in one step
**Failure:** All running app instances crashed, 15min downtime
**Learning:** Always use multi-step rename pattern with dual-read period

### ❌ Attempt: Add NOT NULL column with default on 10M row table
**Context:** `ALTER TABLE orders ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'pending'`
**Failure:** Table locked for 45 minutes, application unavailable
**Learning:** Add as nullable, backfill in batches, then add constraint

### ❌ Attempt: Create index during peak traffic
**Context:** Added index on production during business hours
**Failure:** Query timeouts, cascade failures across services
**Learning:** Use CONCURRENTLY and schedule during low-traffic windows

### ❌ Attempt: Drop column referenced by running code
**Context:** Removed column that was still read by some services
**Failure:** Services crashed until rollback
**Learning:** Multi-step deprecation: stop writes → deploy → stop reads → deploy → drop column

## 6. Database-Specific Guidance

### PostgreSQL
- ✅ Use `CONCURRENTLY` for index creation
- ✅ Use `ADD COLUMN IF NOT EXISTS` for idempotency
- ✅ Wrap DDL in transactions (except CONCURRENTLY operations)
- ✅ Use `pg_stat_activity` to check for locks before migration

### MySQL
- ✅ Use `ALGORITHM=INPLACE, LOCK=NONE` for online DDL (5.6+)
- ✅ Use `pt-online-schema-change` for large tables (Percona Toolkit)
- ⚠️ Be aware of metadata locks and long-running transactions

### SQLite
- ⚠️ Limited ALTER TABLE support (can't drop columns in older versions)
- ✅ Use table recreation pattern: create new → copy data → rename
- ✅ Always use transactions

## 7. Migration Naming Conventions

**Format:** `YYYYMMDDHHMMSS_descriptive_name.sql`

**Examples:**
- ✅ `20260101120000_add_index_users_email.sql`
- ✅ `20260101120100_create_orders_table.sql`
- ✅ `20260101120200_add_not_null_users_created_at.sql`
- ❌ `migration.sql`
- ❌ `update_db.sql`

## 8. Rollback Strategy

### Transactional Migrations (Preferred)
```sql
BEGIN;

-- Migration code here
ALTER TABLE users ADD COLUMN age INT;

-- Verification
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'users' AND column_name = 'age'
  ) THEN
    RAISE EXCEPTION 'Column not created';
  END IF;
END $$;

COMMIT;
```

### Non-Transactional Operations
For operations that can't be in a transaction (e.g., `CREATE INDEX CONCURRENTLY`):
- Document manual rollback steps
- Create a companion "down" migration file
- Test rollback locally before production

## 9. Governance
- **Token Budget:** ~480 lines (within 500 limit)
- **Dependencies:** Database-agnostic patterns (examples in PostgreSQL)
- **Critical:** Failure here causes data loss and downtime
- **Maintenance:** Update as new database versions add features
- **Verification Date:** 2026-01-01
