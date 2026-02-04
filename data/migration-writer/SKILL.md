---
name: migration-writer
description: Expert guidance for writing database migrations using golang-migrate for the mediaz SQLite database. Covers migration creation, testing, rollback capability, data preservation, and mediaz-specific patterns. Activates when users mention migrations, schema changes, database alterations, or golang-migrate.
---

# Migration Writer Skill

This skill provides comprehensive guidance for writing database migrations using golang-migrate in the mediaz project.

## Core Principles

**Critical Rules for Migration Development**

### 1. Backwards Compatibility First
Every migration MUST be reversible through its `.down.sql` file. Users must be able to roll back to previous versions safely.

### 2. Data Safety
Never lose user data. Use COALESCE, CASE statements, or backups when modifying existing data.

### 3. Both Files Required
Always create both `.up.sql` AND `.down.sql` files. A migration without a down file is incomplete.

### 4. Testing Required
No untested migrations. Every migration must have tests for fresh DB, upgrade scenarios, and rollback.

### 5. Idempotency
Use `IF NOT EXISTS`, `IF EXISTS`, and `INSERT OR IGNORE` to ensure migrations can be safely retried.

**Why This Matters:**
- ✅ Users can roll back safely if issues arise
- ✅ Database schema changes are predictable and reversible
- ✅ Data integrity is maintained through all operations
- ❌ Without these principles, you risk data loss and broken deployments

## Migration System Architecture

### How Migrations Work in Mediaz

**Automatic Execution**: Migrations run on server startup via `cmd/serve.go`
```go
if err := store.RunMigrations(ctx); err != nil {
    log.Fatal("failed to run migrations", zap.Error(err))
}
```

**Embedded Files**: Migrations are embedded at compile time in `pkg/storage/sqlite/migrate.go`
```go
//go:embed migrations/*.sql
var migrationFiles embed.FS
```

**Legacy Database Support**: Existing databases without migrations are baselined to version 1
- Checks for `schema_migrations` table
- If missing but `quality_profile` exists → legacy DB detected
- Forces version to 1 via `m.Force(1)`
- Subsequent migrations apply normally

**State Tracking**: The `schema_migrations` table tracks migration state
```sql
SELECT * FROM schema_migrations;
-- version | dirty
-- 2       | 0
```

### File Naming Convention

Format: `000XXX_descriptive_name.{up,down}.sql`

Examples:
- `000001_initial_schema.up.sql` / `000001_initial_schema.down.sql`
- `000002_quality_profile_upgrade_policy.up.sql` / `000002_quality_profile_upgrade_policy.down.sql`

**Version Numbers**: Sequential 6-digit numbers with leading zeros (000001, 000002, 000003)

**Next Version**: Check existing files to determine the next number
```bash
ls pkg/storage/sqlite/migrations/*.sql | tail -2
# Shows 000002_* files, so use 000003
```

## Creating Migrations

### Step-by-Step Process

#### 1. Determine Next Version Number

```bash
ls pkg/storage/sqlite/migrations/*.sql | tail -2
# Output: 000002_quality_profile_upgrade_policy.{up,down}.sql
# Next version: 000003
```

#### 2. Create Migration File Pair

```bash
touch pkg/storage/sqlite/migrations/000003_add_user_preferences.up.sql
touch pkg/storage/sqlite/migrations/000003_add_user_preferences.down.sql
```

#### 3. Write Up Migration

Template for new table creation:

```sql
-- Migration 000003: Add user preferences table
-- Adds a new table for storing user-specific preferences

CREATE TABLE IF NOT EXISTS "user_preference" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "user_id" INTEGER NOT NULL,
    "preference_key" TEXT NOT NULL,
    "preference_value" TEXT,
    FOREIGN KEY ("user_id") REFERENCES "user" ("id")
);

CREATE UNIQUE INDEX IF NOT EXISTS "idx_user_preference_user_key"
ON "user_preference" ("user_id", "preference_key");
```

#### 4. Write Down Migration    

Always provide complete reversal:

```sql
-- Migration 000003 down: Remove user preferences table

DROP INDEX IF EXISTS idx_user_preference_user_key;
DROP TABLE IF EXISTS user_preference;
```

### Migration Types

**Type 1: Table Creation**
- Up: `CREATE TABLE IF NOT EXISTS`
- Down: `DROP TABLE IF EXISTS` (reverse dependency order)
- Example: See migration 000001

**Type 2: Schema Modification**
- Up: Create new table, copy data, drop old, rename
- Down: Reverse the process with data preservation
- Example: See migration 000002

**Type 3: Data Migration**
- Up: `INSERT`/`UPDATE` with `WHERE` conditions
- Down: Revert data changes (COALESCE for NULL handling)
- Example: See migration 000002 quality profile updates

## SQLite-Specific Patterns

### The Table Recreation Pattern

SQLite has limited `ALTER TABLE` support. To modify columns, use this pattern:

```sql
PRAGMA foreign_keys = OFF;

-- 1. Create new table with desired schema
CREATE TABLE quality_profile_new (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "cutoff_quality_id" INTEGER,  -- Now nullable
    "upgrade_allowed" BOOLEAN NOT NULL
);

-- 2. Copy data from old table
INSERT INTO quality_profile_new (id, name, cutoff_quality_id, upgrade_allowed)
SELECT id, name, cutoff_quality_id, upgrade_allowed
FROM quality_profile;

-- 3. Drop old table
DROP TABLE quality_profile;

-- 4. Rename new table
ALTER TABLE quality_profile_new RENAME TO quality_profile;

-- 5. Recreate indexes
CREATE UNIQUE INDEX IF NOT EXISTS "idx_quality_profile_name"
ON "quality_profile" ("name");

PRAGMA foreign_keys = ON;
```

### PRAGMA foreign_keys Discipline

**Use `PRAGMA foreign_keys = OFF` when:**
- Recreating tables with foreign key constraints
- Modifying tables that other tables reference
- Dropping and recreating multiple related tables

**Critical**: ALWAYS re-enable afterward with `PRAGMA foreign_keys = ON`

**Pattern:**
```sql
PRAGMA foreign_keys = OFF;
-- ... table recreation ...
PRAGMA foreign_keys = ON;
```

### Idempotency Keywords

Always use these for safe reruns:

- `CREATE TABLE IF NOT EXISTS`
- `DROP TABLE IF EXISTS`
- `CREATE INDEX IF NOT EXISTS`
- `DROP INDEX IF EXISTS`
- `INSERT OR IGNORE` (for seed data)

**Why**: If a migration partially fails, these allow safe retry without errors.

## Data Migration Patterns

### Preserving User Modifications

**Problem**: You need to change default data, but users may have customized it.

**Solution**: Use `WHERE` clause to match EXACT original values

```sql
-- Update ONLY unmodified default profiles
UPDATE quality_profile
SET cutoff_quality_id = NULL, upgrade_allowed = FALSE
WHERE
    (id = 1 AND name = 'Standard Definition' AND cutoff_quality_id = 2 AND upgrade_allowed = TRUE)
    OR (id = 2 AND name = 'High Definition' AND cutoff_quality_id = 8 AND upgrade_allowed = TRUE)
    OR (id = 3 AND name = 'Ultra High Definition' AND cutoff_quality_id = 13 AND upgrade_allowed = FALSE);
```

**Why this works**:
- If user changed ANY field (name, cutoff, upgrade_allowed), row won't match
- Only untouched defaults get updated
- User customizations are preserved

### Rollback Data Migrations with COALESCE

**Problem**: Rolling back a nullable column to NOT NULL when some values are NULL

**Solution**: Use COALESCE with intelligent defaults

```sql
INSERT INTO quality_profile_new (id, name, cutoff_quality_id, upgrade_allowed)
SELECT
    id,
    name,
    COALESCE(cutoff_quality_id,
        CASE id
            WHEN 1 THEN 2   -- Original default for profile 1
            WHEN 2 THEN 8   -- Original default for profile 2
            WHEN 3 THEN 13  -- Original default for profile 3
            ELSE 2          -- Safe fallback
        END
    ) as cutoff_quality_id,
    upgrade_allowed
FROM quality_profile;
```

### Inserting Seed Data

Always use `INSERT OR IGNORE` for default/seed data:

```sql
INSERT OR IGNORE INTO quality_definition (
    quality_id, name, preferred_size, min_size, max_size, media_type
)
VALUES
    (1, 'HDTV-720p', 1999, 17.1, 2000, 'movie'),
    (2, 'WEBDL-720p', 1999, 12.5, 2000, 'movie');
```

**Why**: Allows migration reruns without duplicate key errors.

## Testing Migrations

### Required Test Scenarios

Every migration must have tests in `pkg/storage/sqlite/migrate_test.go` for these scenarios:

#### 1. Fresh Database Test

```go
func TestMigration_000003_FreshDatabase(t *testing.T) {
    tmpFile := filepath.Join(t.TempDir(), "test.db")
    ctx := context.Background()

    store, err := New(ctx, tmpFile)
    require.NoError(t, err)

    err = store.RunMigrations(ctx)
    require.NoError(t, err)

    // Verify migration applied correctly
    sqliteStore := store.(*SQLite)
    version, dirty, err := sqliteStore.GetMigrationVersion()
    require.NoError(t, err)
    assert.Equal(t, uint(3), version)
    assert.False(t, dirty)

    // Verify schema/data changes
    // ... your assertions ...
}
```

#### 2. Upgrade from Previous Version

```go
func TestMigration_000003_UpgradeFromV2(t *testing.T) {
    tmpFile := filepath.Join(t.TempDir(), "test.db")
    ctx := context.Background()

    // Create database at previous version
    createV2Database(t, tmpFile)

    // Run migrations to upgrade
    store, err := New(ctx, tmpFile)
    require.NoError(t, err)

    err = store.RunMigrations(ctx)
    require.NoError(t, err)

    // Verify upgrade succeeded
    version, dirty, err := store.(*SQLite).GetMigrationVersion()
    require.NoError(t, err)
    assert.Equal(t, uint(3), version)
}
```

#### 3. User Modification Preservation

```go
func TestMigration_000003_PreservesUserModifications(t *testing.T) {
    tmpFile := filepath.Join(t.TempDir(), "test.db")
    ctx := context.Background()

    createV2Database(t, tmpFile)

    // Make user modifications BEFORE migration
    db, err := sql.Open("sqlite3", tmpFile)
    require.NoError(t, err)
    _, err = db.Exec("UPDATE quality_profile SET name = 'Custom Profile' WHERE id = 1")
    require.NoError(t, err)
    db.Close()

    // Run migration
    store, err := New(ctx, tmpFile)
    require.NoError(t, err)
    err = store.RunMigrations(ctx)
    require.NoError(t, err)

    // Verify user modifications preserved
    // ... assertions ...
}
```

### Helper Function Pattern

Create helpers for database setup at specific versions:

```go
func createV2Database(t *testing.T, dbPath string) {
    migration001Up, err := os.ReadFile("migrations/000001_initial_schema.up.sql")
    require.NoError(t, err)
    migration002Up, err := os.ReadFile("migrations/000002_quality_profile_upgrade_policy.up.sql")
    require.NoError(t, err)

    db, err := sql.Open("sqlite3", dbPath)
    require.NoError(t, err)
    defer db.Close()

    _, err = db.Exec(string(migration001Up))
    require.NoError(t, err)
    _, err = db.Exec(string(migration002Up))
    require.NoError(t, err)
}
```

### Running Tests

```bash
# Run all migration tests
go test ./pkg/storage/sqlite/ -run TestMigration -v

# Run specific migration test
go test ./pkg/storage/sqlite/ -run TestMigration_000003 -v

# Test with race detector
go test -race ./pkg/storage/sqlite/
```

## Rollback (Down Migration) Best Practices

### The Golden Rule

**A down migration must leave the database in a state where the previous version of the application works correctly.**

This sometimes means:
- Reintroducing bugs that existed in previous versions
- Making "best guess" defaults for data that didn't exist before
- Trading data accuracy for compatibility

### Complete Reversal with Data Preservation

Example from migration 000002:

```sql
-- Migration 000002 down: Rollback quality profile upgrade policy changes
-- NOTE: This rollback preserves user modifications but makes best-effort guesses for NULL values
-- WARNING: This reintroduces the foreign key bug (quality_id -> quality_id instead of id)

PRAGMA foreign_keys = OFF;

CREATE TABLE quality_profile_new (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "cutoff_quality_id" INTEGER NOT NULL,  -- Back to NOT NULL
    "upgrade_allowed" BOOLEAN NOT NULL
);

-- Use COALESCE to provide defaults for NULL values
INSERT INTO quality_profile_new (id, name, cutoff_quality_id, upgrade_allowed)
SELECT
    id,
    name,
    COALESCE(cutoff_quality_id,
        CASE id
            WHEN 1 THEN 2
            WHEN 2 THEN 8
            WHEN 3 THEN 13
            ELSE 2
        END
    ) as cutoff_quality_id,
    upgrade_allowed
FROM quality_profile;

DROP TABLE quality_profile;
ALTER TABLE quality_profile_new RENAME TO quality_profile;

PRAGMA foreign_keys = ON;
```

### Documenting Rollback Limitations

Use comments to warn about trade-offs:

```sql
-- NOTE: This rollback preserves user modifications but makes best-effort guesses
-- WARNING: This reintroduces the foreign key bug for backwards compatibility
-- LIMITATION: Preferences added after migration will be lost on rollback
```

### Dependency Order for Table Drops

Always drop in reverse dependency order (children before parents):

```sql
-- Drop child tables first (those with foreign keys)
DROP TABLE IF EXISTS quality_profile_item;

-- Then parent tables (those referenced by foreign keys)
DROP TABLE IF EXISTS quality_profile;
DROP TABLE IF EXISTS quality_definition;
```

See `000001_initial_schema.down.sql` for complete example with 16 tables.

## Common Migration Scenarios

### Scenario 1: Add New Table

**Up Migration:**
```sql
CREATE TABLE IF NOT EXISTS "new_feature" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "created_at" DATETIME DEFAULT CURRENT_TIMESTAMP,
    "parent_id" INTEGER,
    FOREIGN KEY ("parent_id") REFERENCES "existing_table" ("id")
);

CREATE INDEX IF NOT EXISTS "idx_new_feature_parent"
ON "new_feature" ("parent_id");
```

**Down Migration:**
```sql
DROP INDEX IF EXISTS idx_new_feature_parent;
DROP TABLE IF EXISTS new_feature;
```

### Scenario 2: Make Column Nullable

**Up Migration:** (Table recreation required)
```sql
PRAGMA foreign_keys = OFF;

CREATE TABLE table_name_new (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "required_field" TEXT NOT NULL,
    "now_optional_field" TEXT  -- Removed NOT NULL
);

INSERT INTO table_name_new SELECT * FROM table_name;

DROP TABLE table_name;
ALTER TABLE table_name_new RENAME TO table_name;

PRAGMA foreign_keys = ON;
```

**Down Migration:** (Provide defaults for NULLs)
```sql
PRAGMA foreign_keys = OFF;

CREATE TABLE table_name_new (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "required_field" TEXT NOT NULL,
    "now_optional_field" TEXT NOT NULL  -- Back to NOT NULL
);

INSERT INTO table_name_new (id, required_field, now_optional_field)
SELECT id, required_field, COALESCE(now_optional_field, 'default_value')
FROM table_name;

DROP TABLE table_name;
ALTER TABLE table_name_new RENAME TO table_name;

PRAGMA foreign_keys = ON;
```

### Scenario 3: Add Index

**Up Migration:**
```sql
-- Simple index
CREATE INDEX IF NOT EXISTS "idx_movie_title"
ON "movie" ("title");

-- Partial index (with WHERE clause)
CREATE UNIQUE INDEX IF NOT EXISTS "idx_movie_transitions_most_recent"
ON "movie_transition"("movie_id", "most_recent")
WHERE "most_recent" = 1;
```

**Down Migration:**
```sql
DROP INDEX IF EXISTS idx_movie_transitions_most_recent;
DROP INDEX IF EXISTS idx_movie_title;
```

### Scenario 4: Fix Foreign Key Reference

See migration 000002 for full example:
- Recreate both parent and child tables
- Fix FK reference in child table definition
- Copy all data
- Recreate indexes

## Debugging Failed Migrations

### Understanding Dirty State

When a migration fails mid-execution, the database enters "dirty" state:

```go
version, dirty, err := sqliteStore.GetMigrationVersion()
// version=2, dirty=true means migration 2 started but didn't complete
```

### Inspecting Migration State

```sql
SELECT * FROM schema_migrations;
-- version | dirty
-- 2       | 1      (dirty=1 means failed)
```

### Recovery Steps

1. **Identify the problem**: Read error message carefully
2. **Fix the migration file**: Correct SQL syntax or logic
3. **Manual cleanup if needed**: Remove partial changes via SQL
4. **Restart server**: Migrations run on startup

### Common SQLite Errors

**Foreign Key Violation:**
```
Error: FOREIGN KEY constraint failed
```
**Solution**: Ensure parent record exists or use `PRAGMA foreign_keys = OFF` during table recreation

**Table Already Exists:**
```
Error: table "foo" already exists
```
**Solution**: Use `CREATE TABLE IF NOT EXISTS`

**Syntax Error:**
```
Error: near "COLUMN": syntax error
```
**Solution**: SQLite doesn't support `ALTER TABLE DROP COLUMN` - use table recreation pattern

## Integration with Jet ORM

### The Migration → Code Generation Flow

1. **Write migration** (e.g., add new table)
2. **Run migration** (updates database schema)
3. **Regenerate Jet code** (generates Go models/tables from schema)
4. **Update application code** (use new models)

### Regenerating After Schema Changes

```bash
# Apply migration (via server startup)
./mediaz serve

# Regenerate Jet models
go generate ./...
```

This updates:
- `pkg/storage/sqlite/schema/gen/model/*.go` - Struct definitions
- `pkg/storage/sqlite/schema/gen/table/*.go` - Table definitions

### Type Mapping Reference

| SQLite Type | Go Type |
|-------------|---------|
| INTEGER | int64 |
| INTEGER PRIMARY KEY AUTOINCREMENT | int64 |
| TEXT | string |
| BOOLEAN | bool |
| DATETIME | time.Time |
| NUMERIC | float64 |

### Migration-First Workflow

- ❌ DON'T: Change Go models and hope it updates DB
- ✅ DO: Write migration → Apply → Regenerate → Use

## Quick Reference

### Migration Checklist

Before committing a migration, verify:

- [ ] Both `.up.sql` and `.down.sql` files created
- [ ] Migration number is sequential and correct (6 digits with leading zeros)
- [ ] Header comments explain purpose
- [ ] Up migration uses `IF NOT EXISTS` / `IF EXISTS`
- [ ] Down migration completely reverses changes
- [ ] Data migrations preserve user modifications (exact WHERE matching)
- [ ] Tests written for all scenarios (fresh DB, upgrade, preservation, rollback)
- [ ] Tests pass: `go test ./pkg/storage/sqlite/`
- [ ] Foreign key constraints considered (`PRAGMA foreign_keys` discipline)
- [ ] Jet models regenerated if schema changed: `go generate ./...`

### File Locations

| Purpose | Location |
|---------|----------|
| Migrations | `pkg/storage/sqlite/migrations/` |
| Migration logic | `pkg/storage/sqlite/migrate.go` |
| Migration tests | `pkg/storage/sqlite/migrate_test.go` |
| Generated models | `pkg/storage/sqlite/schema/gen/model/` |
| Generated tables | `pkg/storage/sqlite/schema/gen/table/` |

### Common Commands

```bash
# Run migrations (via server)
./mediaz serve

# Run tests
go test ./pkg/storage/sqlite/ -v

# Run specific migration test
go test ./pkg/storage/sqlite/ -run TestMigration_000002 -v

# Regenerate Jet models
go generate ./...
```

### DO vs DON'T

| ✅ DO | ❌ DON'T |
|------|---------|
| Write complete `.down.sql` files | Leave down migration empty or incomplete |
| Use `IF EXISTS`/`IF NOT EXISTS` | Assume clean database state |
| Preserve user data with COALESCE | Delete data without preservation strategy |
| Use `PRAGMA foreign_keys OFF/ON` | Forget to re-enable foreign keys |
| Document limitations in comments | Hide rollback trade-offs from maintainers |
| Create test helper functions | Copy-paste test setup code |
| Use `INSERT OR IGNORE` for seed data | Fail on duplicate seed data |
| Test fresh AND upgrade scenarios | Only test happy path |
| Match ALL fields in WHERE for user preservation | Match only ID in data migration updates |
| Use table recreation for complex ALTER | Try unsupported SQLite ALTER operations |

## Example Migrations (Annotated)

### Example 1: Migration 000001 - Initial Schema

**File**: `000001_initial_schema.up.sql`

**Key Patterns Demonstrated:**
- Multiple table creation with foreign key relationships
- Seed data insertion with `INSERT OR IGNORE`
- Unique indexes for constraint enforcement
- Partial indexes with WHERE clauses

**Highlights:**

```sql
-- Pattern: Create parent table first
CREATE TABLE IF NOT EXISTS "quality_definition" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "quality_id" INTEGER NOT NULL,
    "name" TEXT NOT NULL,
    ...
);

-- Pattern: Create child table with FK
CREATE TABLE IF NOT EXISTS "quality_profile_item" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "profile_id" INTEGER NOT NULL,
    "quality_id" INTEGER NOT NULL,
    FOREIGN KEY ("profile_id") REFERENCES "quality_profile" ("id"),
    FOREIGN KEY ("quality_id") REFERENCES "quality_definition" ("quality_id")
);

-- Pattern: Partial index for conditional uniqueness
CREATE UNIQUE INDEX IF NOT EXISTS "idx_movie_transitions_most_recent"
ON "movie_transition"("movie_id", "most_recent")
WHERE "most_recent" = 1;

-- Pattern: Seed data with INSERT OR IGNORE (idempotent)
INSERT OR IGNORE INTO quality_definition (quality_id, name, ...)
VALUES
    (1, 'HDTV-720p', ...),
    (2, 'WEBDL-720p', ...);
```

**Down Migration** (`000001_initial_schema.down.sql`):

```sql
-- Pattern: Drop in reverse dependency order (children first, parents last)
DROP TABLE IF EXISTS job_transition;      -- Child
DROP TABLE IF EXISTS job;                 -- Parent
...
DROP TABLE IF EXISTS quality_profile_item;  -- Child
DROP TABLE IF EXISTS quality_profile;       -- Parent
DROP TABLE IF EXISTS quality_definition;    -- Root parent
```

### Example 2: Migration 000002 - Quality Profile Upgrade Policy

**File**: `000002_quality_profile_upgrade_policy.up.sql`

**Key Patterns Demonstrated:**
- Table recreation to change column constraints
- Selective data migration preserving user changes
- Foreign key bug fix
- Rollback with data preservation

**Highlights:**

```sql
-- Pattern: Disable FK checks during table recreation
PRAGMA foreign_keys = OFF;

-- Pattern: Create replacement table with schema changes
CREATE TABLE quality_profile_new (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "cutoff_quality_id" INTEGER,  -- Changed from NOT NULL to nullable
    "upgrade_allowed" BOOLEAN NOT NULL
);

-- Pattern: Copy all data unchanged
INSERT INTO quality_profile_new SELECT * FROM quality_profile;

-- Pattern: Atomic table replacement
DROP TABLE quality_profile;
ALTER TABLE quality_profile_new RENAME TO quality_profile;

-- Pattern: Fix foreign key bug
CREATE TABLE quality_profile_item_new (
    ...
    -- FIXED: Now references correct column
    FOREIGN KEY ("quality_id") REFERENCES "quality_definition" ("id")
);

PRAGMA foreign_keys = ON;

-- Pattern: Conditional data migration (preserves user modifications)
UPDATE quality_profile
SET cutoff_quality_id = NULL, upgrade_allowed = FALSE
WHERE
    (id = 1 AND name = 'Standard Definition' AND cutoff_quality_id = 2 AND upgrade_allowed = TRUE)
    OR (id = 2 AND name = 'High Definition' AND cutoff_quality_id = 8 AND upgrade_allowed = TRUE);
    -- Only matches exact original defaults
```

**Down Migration** (`000002_quality_profile_upgrade_policy.down.sql`):

```sql
-- Pattern: WARNING comments for rollback trade-offs
-- WARNING: This reintroduces the foreign key bug for backwards compatibility

-- Pattern: COALESCE to handle NULL values during rollback
INSERT INTO quality_profile_new (id, name, cutoff_quality_id, upgrade_allowed)
SELECT
    id,
    name,
    COALESCE(cutoff_quality_id,
        CASE id
            WHEN 1 THEN 2
            WHEN 2 THEN 8
            ELSE 2  -- Safe fallback
        END
    ) as cutoff_quality_id,
    upgrade_allowed
FROM quality_profile;
```

**Key Takeaway**: This migration demonstrates the full complexity of schema changes with data preservation, bug fixes, and complete rollback capability including trade-offs.

## Workflow Summary

### Creating a New Migration

```bash
# 1. Determine next version
ls pkg/storage/sqlite/migrations/*.sql | tail -2

# 2. Create migration files
touch pkg/storage/sqlite/migrations/000003_add_feature.up.sql
touch pkg/storage/sqlite/migrations/000003_add_feature.down.sql

# 3. Write migration SQL in both files

# 4. Write tests in migrate_test.go

# 5. Test locally
go test ./pkg/storage/sqlite/ -v

# 6. Regenerate Jet models if schema changed
go generate ./...

# 7. Commit
git add pkg/storage/sqlite/migrations/000003_*
git add pkg/storage/sqlite/migrate_test.go
git commit -m "Add migration 000003: add feature"
```

### Testing a Migration

```bash
# Run all migration tests
go test ./pkg/storage/sqlite/ -run TestMigration -v

# Run specific migration
go test ./pkg/storage/sqlite/ -run TestMigration_000003 -v

# With race detector
go test -race ./pkg/storage/sqlite/
```

## Remember

**The Golden Rules:**
1. Every migration must be reversible
2. Test both up and down migrations
3. Preserve user data at all costs
4. Document trade-offs and limitations
5. Use SQLite-specific patterns for ALTER operations

For complete golang-migrate documentation: https://github.com/golang-migrate/migrate
