---
name: migrations-api-reference
description: Use when working with database migrations in pgdbm - provides complete AsyncMigrationManager API with all methods and migration file format
---

# pgdbm Migrations API Reference

## Overview

**Complete API reference for AsyncMigrationManager and migration file format.**

All signatures, parameters, return types. No documentation lookup needed.

## AsyncMigrationManager

### Initialization

```python
from pgdbm import AsyncMigrationManager

migrations = AsyncMigrationManager(
    db_manager: AsyncDatabaseManager,
    migrations_path: str = "./migrations",
    migrations_table: str = "schema_migrations",
    module_name: Optional[str] = None,
)
```

**Parameters:**
- `db_manager`: AsyncDatabaseManager instance (schema already set)
- `migrations_path`: Directory containing .sql migration files
- `migrations_table`: Table name for tracking migrations (default: "schema_migrations")
- `module_name`: CRITICAL - Unique identifier for this module's migrations

**IMPORTANT:**
- DO NOT pass `schema` parameter (doesn't exist, schema comes from db_manager)
- ALWAYS specify `module_name` to prevent conflicts
- For dual-mode libraries: `module_name=f"mylib_{schema}"` (include schema)

### Core Methods

```python
# Apply all pending migrations
result = await migrations.apply_pending_migrations(
    dry_run: bool = False
) -> dict[str, Any]
# Returns: {
#     "status": "success" | "up_to_date" | "dry_run" | "error",
#     "applied": [{"filename": "001_...", "execution_time_ms": 123.4}, ...],
#     "skipped": ["001_already_applied.sql", ...],
#     "total": 5,
#     "total_time_ms": 456.7  # Only if status="success"
# }

# Get applied migrations
applied = await migrations.get_applied_migrations() -> dict[str, Migration]
# Returns: {"001_users.sql": Migration(...), ...}

# Get pending migrations
pending = await migrations.get_pending_migrations() -> list[Migration]
# Returns: [Migration(...), Migration(...)]

# Find migration files on disk
files = await migrations.find_migration_files() -> list[Migration]
# Returns: All .sql files in migrations_path

# Apply single migration
execution_time = await migrations.apply_migration(
    migration: Migration
) -> float
# Returns: Execution time in milliseconds

# Get migration history (recent migrations)
history = await migrations.get_migration_history(
    limit: int = 10
) -> list[dict[str, Any]]
# Returns: Recent migrations with timestamps, checksums

# Ensure migrations table exists
await migrations.ensure_migrations_table() -> None
# Creates schema_migrations table if doesn't exist
```

### Development Methods

```python
# Create new migration file
filepath = await migrations.create_migration(
    name: str,
    content: str,
    auto_transaction: bool = True
) -> str
# Returns: Path to created file

# Example
path = await migrations.create_migration(
    name="add_users_table",
    content="CREATE TABLE {{tables.users}} (id SERIAL PRIMARY KEY)",
    auto_transaction=True  # Wraps in BEGIN/COMMIT
)
# Creates: migrations/20251025_120000_add_users_table.sql

# Rollback migration (removes from tracking, doesn't undo changes)
await migrations.rollback_migration(filename: str) -> None
# Marks migration as not applied
# WARNING: Doesn't undo the migration, just removes tracking
```

## Migration File Format

### File Naming

Must match one of these patterns:
- `001_description.sql` (numeric prefix)
- `V1__description.sql` (Flyway pattern)
- `20251025120000_description.sql` (timestamp)

**Examples:**
```
migrations/
├── 001_create_users.sql
├── 002_add_profiles.sql
├── 003_create_sessions.sql
└── 004_add_indexes.sql
```

### Template Syntax

Always use templates for schema portability:

```sql
-- All template placeholders
{{tables.tablename}}   -- Table with schema qualification
{{schema}}             -- Schema name only
```

**Example migration:**

```sql
-- migrations/001_create_users.sql
CREATE TABLE IF NOT EXISTS {{tables.users}} (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS users_email
    ON {{tables.users}} (email);

CREATE INDEX IF NOT EXISTS users_created
    ON {{tables.users}} (created_at DESC);

-- Trigger using schema placeholder
CREATE OR REPLACE FUNCTION {{schema}}.update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_updated_at
    BEFORE UPDATE ON {{tables.users}}
    FOR EACH ROW
    EXECUTE FUNCTION {{schema}}.update_updated_at();
```

### Transaction Handling

**Automatic:** Migrations run in transactions by default

**Manual control:**
```sql
-- migrations/002_manual_transaction.sql
BEGIN;

CREATE TABLE {{tables.posts}} (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL
);

-- If this fails, whole migration rolls back
CREATE INDEX posts_title ON {{tables.posts}} (title);

COMMIT;
```

**Non-transactional operations:**
```sql
-- migrations/003_create_index_concurrently.sql
-- CREATE INDEX CONCURRENTLY cannot run in transaction

CREATE INDEX CONCURRENTLY users_email_concurrent
    ON {{tables.users}} (email);
```

## Complete Usage Examples

### Basic Setup

```python
from pgdbm import AsyncDatabaseManager, AsyncMigrationManager, DatabaseConfig

# Create database manager
config = DatabaseConfig(connection_string="postgresql://localhost/myapp")
db = AsyncDatabaseManager(config)
await db.connect()

# Create migration manager
migrations = AsyncMigrationManager(
    db,
    migrations_path="./migrations",
    module_name="myapp"  # REQUIRED
)

# Apply all pending
result = await migrations.apply_pending_migrations()

if result["status"] == "success":
    print(f"Applied {len(result['applied'])} migrations")
    for mig in result["applied"]:
        print(f"  - {mig['filename']} ({mig['execution_time_ms']:.1f}ms)")
```

### Dry Run

```python
# Check what would be applied without applying
result = await migrations.apply_pending_migrations(dry_run=True)

if result["status"] == "dry_run":
    print(f"Would apply {len(result['pending'])} migrations:")
    for filename in result["pending"]:
        print(f"  - {filename}")
```

### Check Migration Status

```python
# Get applied migrations
applied = await migrations.get_applied_migrations()
print(f"Applied: {list(applied.keys())}")

# Get pending migrations
pending = await migrations.get_pending_migrations()
print(f"Pending: {[m.filename for m in pending]}")

# Get history
history = await migrations.get_migration_history(limit=5)
for entry in history:
    print(f"{entry['applied_at']}: {entry['filename']} ({entry['execution_time_ms']:.1f}ms)")
```

### Creating Migrations Programmatically

```python
# Create new migration
path = await migrations.create_migration(
    name="add_users_avatar",
    content="""
        ALTER TABLE {{tables.users}}
        ADD COLUMN avatar_url VARCHAR(500);
    """,
    auto_transaction=True  # Wraps in BEGIN/COMMIT
)

print(f"Created migration: {path}")
# Output: migrations/20251025_143022_add_users_avatar.sql
```

### Development: Rollback Migration Record

```python
# Remove migration from tracking (doesn't undo changes!)
await migrations.rollback_migration("003_add_column.sql")

# Migration can now be re-applied
result = await migrations.apply_pending_migrations()
# Will apply 003_add_column.sql again
```

**WARNING:** `rollback_migration` only removes tracking record. It does NOT undo the migration's database changes. For true rollback, write a down migration.

## Migration Class

Used internally, but can be accessed:

```python
class Migration:
    filename: str
    checksum: str
    content: str
    applied_at: Optional[datetime]
    module_name: Optional[str]

    @property
    def is_applied(self) -> bool

    @property
    def version(self) -> str
```

## Complete Method Summary

| Method | Parameters | Returns | Use Case |
|--------|------------|---------|----------|
| `apply_pending_migrations` | dry_run=False | dict | Apply all pending |
| `get_applied_migrations` | - | dict[str, Migration] | Check what's applied |
| `get_pending_migrations` | - | list[Migration] | Check what's pending |
| `find_migration_files` | - | list[Migration] | List files on disk |
| `apply_migration` | migration | float | Apply single migration |
| `ensure_migrations_table` | - | None | Create tracking table |
| `create_migration` | name, content, auto_transaction | str | Create new file |
| `rollback_migration` | filename | None | Remove tracking (dev only) |
| `get_migration_history` | limit=10 | list[dict] | Recent migrations |

## Migration Best Practices

### 1. Always Use Templates

```sql
-- ✅ CORRECT
CREATE TABLE {{tables.users}} (...);
CREATE INDEX users_email ON {{tables.users}} (email);

-- ❌ WRONG
CREATE TABLE users (...);
CREATE TABLE myschema.users (...);
```

### 2. Make Migrations Idempotent

```sql
-- ✅ CORRECT - Can run multiple times safely
CREATE TABLE IF NOT EXISTS {{tables.users}} (...);
CREATE INDEX IF NOT EXISTS users_email ON {{tables.users}} (email);

-- ❌ WRONG - Fails if already exists
CREATE TABLE {{tables.users}} (...);
```

### 3. Use Unique module_name

```python
# ✅ CORRECT - Unique per module
AsyncMigrationManager(db, "migrations", module_name="users")
AsyncMigrationManager(db, "migrations", module_name="orders")

# ❌ WRONG - Default module name causes conflicts
AsyncMigrationManager(db, "migrations")  # module_name="default"
AsyncMigrationManager(db, "migrations")  # Same default - conflict!
```

### 4. For Dual-Mode Libraries: Include Schema in module_name

```python
# ✅ CORRECT - Can use same library multiple times
module_name = f"mylib_{schema}"  # "mylib_tenant1", "mylib_tenant2"

# ❌ WRONG - Conflicts if library used twice
module_name = "mylib"  # Always the same
```

## Migration File Examples

### Basic Table Creation

```sql
-- migrations/001_initial_schema.sql
CREATE TABLE IF NOT EXISTS {{tables.users}} (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS {{tables.posts}} (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES {{tables.users}}(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Adding Indexes

```sql
-- migrations/002_add_indexes.sql
CREATE INDEX IF NOT EXISTS users_email
    ON {{tables.users}} (email);

CREATE INDEX IF NOT EXISTS posts_user_id
    ON {{tables.posts}} (user_id);

CREATE INDEX IF NOT EXISTS posts_created
    ON {{tables.posts}} (created_at DESC);
```

### Schema-Qualified Functions

```sql
-- migrations/003_add_triggers.sql
CREATE OR REPLACE FUNCTION {{schema}}.update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_timestamp
    BEFORE UPDATE ON {{tables.users}}
    FOR EACH ROW
    EXECUTE FUNCTION {{schema}}.update_timestamp();
```

### Data Migrations

```sql
-- migrations/004_seed_data.sql
INSERT INTO {{tables.users}} (email, full_name)
VALUES
    ('admin@example.com', 'Admin User'),
    ('support@example.com', 'Support User')
ON CONFLICT (email) DO NOTHING;
```

## Checksum Validation

**Migrations are checksummed** to detect modifications:

```python
# If migration file changes after being applied
result = await migrations.apply_pending_migrations()
# Raises: MigrationError(
#     "Migration '001_users.sql' has been modified after being applied!"
#     "Expected checksum: abc123..."
#     "Current checksum: def456..."
# )
```

**Why:** Prevents silent schema divergence. Applied migrations must not change.

**If you need to modify:** Create a new migration instead.

## Migration Table Schema

Migrations tracked in `schema_migrations` table:

```sql
CREATE TABLE schema_migrations (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    checksum VARCHAR(64) NOT NULL,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    execution_time_ms REAL,
    module_name VARCHAR(255),
    UNIQUE(filename, module_name)
);
```

**Key points:**
- `filename`: Migration file name
- `checksum`: SHA256 of file contents
- `module_name`: Isolates migrations per module
- UNIQUE constraint on (filename, module_name)

**This allows:**
- Same filename in different modules (e.g., both "001_initial.sql")
- Each module tracks its own migrations
- No conflicts when modules share database

## Error Handling

```python
result = await migrations.apply_pending_migrations()

if result["status"] == "error":
    print(f"Failed on: {result['failed_migration']}")
    print(f"Error: {result['error']}")
    print(f"Successfully applied: {result['applied']}")

elif result["status"] == "success":
    print(f"Applied {len(result['applied'])} migrations")

elif result["status"] == "up_to_date":
    print("No pending migrations")
```

## Common Patterns

### Standard Application Setup

```python
# In application startup (FastAPI lifespan, etc.)
from pgdbm import AsyncDatabaseManager, AsyncMigrationManager, DatabaseConfig

config = DatabaseConfig(connection_string="postgresql://localhost/myapp")
db = AsyncDatabaseManager(config)
await db.connect()

migrations = AsyncMigrationManager(
    db,
    migrations_path="./migrations",
    module_name="myapp"
)

result = await migrations.apply_pending_migrations()

if result["status"] != "success" and result["status"] != "up_to_date":
    raise RuntimeError(f"Migration failed: {result}")
```

### Multi-Service Setup

```python
# Each service runs its own migrations
services = [
    (users_db, "migrations/users", "users"),
    (orders_db, "migrations/orders", "orders"),
    (payments_db, "migrations/payments", "payments"),
]

for db, path, name in services:
    migrations = AsyncMigrationManager(db, path, module_name=name)
    result = await migrations.apply_pending_migrations()

    if result["status"] == "success":
        print(f"{name}: Applied {len(result['applied'])} migrations")
```

### Dual-Mode Library

```python
class MyLibrary:
    async def initialize(self):
        # Library ALWAYS runs its own migrations
        migrations = AsyncMigrationManager(
            self.db,
            migrations_path=str(Path(__file__).parent / "migrations"),
            module_name=f"mylib_{self.db.schema}"  # Include schema!
        )

        result = await migrations.apply_pending_migrations()
```

## Advanced Usage

### Custom Migrations Table

```python
# Use different table name (e.g., for multi-tenant)
migrations = AsyncMigrationManager(
    db,
    migrations_path="tenant_migrations",
    migrations_table="tenant_migrations",  # Custom table name
    module_name=f"tenant_{tenant_id}"
)
```

### Pre-Flight Checks

```python
# Check pending before applying
pending = await migrations.get_pending_migrations()

if pending:
    print(f"Found {len(pending)} pending migrations:")
    for mig in pending:
        print(f"  - {mig.filename}")

    # Ask user confirmation
    if input("Apply? (y/n): ") == "y":
        result = await migrations.apply_pending_migrations()
else:
    print("Schema is up to date")
```

### Development Workflow

```python
# 1. Create migration
path = await migrations.create_migration(
    name="add_user_roles",
    content="""
        CREATE TABLE {{tables.roles}} (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL
        );

        ALTER TABLE {{tables.users}}
        ADD COLUMN role_id INTEGER REFERENCES {{tables.roles}}(id);
    """
)

# 2. Apply it
result = await migrations.apply_pending_migrations()

# 3. If something wrong, rollback the record
await migrations.rollback_migration("20251025_143022_add_user_roles.sql")

# 4. Fix the file, re-apply
result = await migrations.apply_pending_migrations()
```

## Common Mistakes

### ❌ Passing schema Parameter

```python
# WRONG - schema parameter doesn't exist
migrations = AsyncMigrationManager(
    db,
    "migrations",
    schema="myschema"  # TypeError!
)
```

**Fix:** Schema comes from db_manager:
```python
db = AsyncDatabaseManager(pool=pool, schema="myschema")
migrations = AsyncMigrationManager(db, "migrations", module_name="myapp")
```

### ❌ Not Specifying module_name

```python
# WRONG - Uses "default" module name
migrations = AsyncMigrationManager(db, "migrations")
```

**Fix:** Always specify unique module_name:
```python
migrations = AsyncMigrationManager(db, "migrations", module_name="myservice")
```

### ❌ Same module_name for Different Schemas

```python
# WRONG - Conflict if library used twice
migrations = AsyncMigrationManager(db1, "migrations", module_name="mylib")
migrations = AsyncMigrationManager(db2, "migrations", module_name="mylib")
```

**Fix:** Include schema in module_name:
```python
migrations = AsyncMigrationManager(db1, "migrations", module_name=f"mylib_{schema1}")
migrations = AsyncMigrationManager(db2, "migrations", module_name=f"mylib_{schema2}")
```

### ❌ Hardcoding Table Names

```sql
-- WRONG
CREATE TABLE users (...);
CREATE TABLE myschema.users (...);
```

**Fix:** Use templates:
```sql
-- CORRECT
CREATE TABLE {{tables.users}} (...);
```

### ❌ Modifying Applied Migrations

```sql
-- You applied 001_users.sql yesterday
-- Today you edit it and add a column
-- Next deploy: ERROR - checksum mismatch!
```

**Fix:** Never modify applied migrations. Create new migration:
```sql
-- migrations/002_add_user_column.sql
ALTER TABLE {{tables.users}} ADD COLUMN new_field VARCHAR(255);
```

### ❌ Not Making Migrations Idempotent

```sql
-- WRONG - Fails if run twice
CREATE TABLE {{tables.users}} (...);
```

**Fix:** Use IF NOT EXISTS:
```sql
-- CORRECT
CREATE TABLE IF NOT EXISTS {{tables.users}} (...);
CREATE INDEX IF NOT EXISTS users_email ON {{tables.users}} (email);
```

## Migration History

```python
# Get recent migration history
history = await migrations.get_migration_history(limit=10)

for entry in history:
    print(f"""
Migration: {entry['filename']}
Module: {entry['module_name']}
Applied: {entry['applied_at']}
Time: {entry['execution_time_ms']}ms
Checksum: {entry['checksum']}
    """)
```

## Quick Checklist

Before running migrations:

- [ ] All migrations use `{{tables.}}` syntax
- [ ] All migrations are idempotent (IF NOT EXISTS)
- [ ] Unique `module_name` specified
- [ ] Migration files follow naming pattern (001_name.sql)
- [ ] No modifications to already-applied migrations
- [ ] For dual-mode libraries: module_name includes schema

## Related Skills

- For patterns: `pgdbm:using-pgdbm`, `pgdbm:choosing-pattern`
- For implementation: `pgdbm:shared-pool-pattern`, `pgdbm:dual-mode-library`
- For complete API: `pgdbm:core-api-reference`
