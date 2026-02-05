---
name: create-migration
description: Create, apply, and rollback database migrations using goose
---

# Create Migration Skill

Use this skill when making database schema changes.

---

## Scope

- Adding new tables
- Modifying columns or constraints
- Creating or dropping indexes
- Any DDL operation

## Creating a New Migration

### Step 1: Generate Migration File

```bash
task migrate:create -- your_migration_name
```

**Naming conventions:**
- Use snake_case
- Be descriptive but concise
- Use prefixes: `add_`, `create_`, `drop_`, `modify_`, `update_`

**Examples:**
```bash
task migrate:create -- add_weapon_stats_table
task migrate:create -- add_index_on_trader_offers
task migrate:create -- modify_item_properties_column
```

This creates a timestamped file in `migrations/`:
```
migrations/YYYYMMDDHHMMSS_your_migration_name.go
```

### Step 2: Write the Migration

The generated file will have this structure:

```go
package migrations

import (
    "database/sql"
    "github.com/pressly/goose/v3"
)

func init() {
    goose.AddMigrationContext(upYourMigrationName, downYourMigrationName)
}

func upYourMigrationName(ctx context.Context, tx *sql.Tx) error {
    // This code is executed when the migration is applied.
    return nil
}

func downYourMigrationName(ctx context.Context, tx *sql.Tx) error {
    // This code is executed when the migration is rolled back.
    return nil
}
```

**In the `up` function:**
- Write SQL to apply the change
- Use `tx.ExecContext(ctx, "SQL HERE")`

**In the `down` function:**
- Write SQL to reverse the change
- Make it possible to rollback safely

**Example:**

```go
func upAddWeaponStatsTable(ctx context.Context, tx *sql.Tx) error {
    _, err := tx.ExecContext(ctx, `
        CREATE TABLE weapon_stats (
            id SERIAL PRIMARY KEY,
            weapon_id VARCHAR(255) NOT NULL,
            recoil_vertical INT NOT NULL,
            recoil_horizontal INT NOT NULL,
            ergonomics INT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        );
        CREATE INDEX idx_weapon_stats_weapon_id ON weapon_stats(weapon_id);
    `)
    return err
}

func downAddWeaponStatsTable(ctx context.Context, tx *sql.Tx) error {
    _, err := tx.ExecContext(ctx, `DROP TABLE IF EXISTS weapon_stats;`)
    return err
}
```

### Step 3: Apply the Migration

```bash
# Recommended for DevContainer (assuming database is running)
task migrate:up

# Use if database needs to be started via Docker Compose
task migrate:up:docker
```

**What it does:**
1. `migrate:up`: Builds the migration binary and runs migrations against the existing database.
2. `migrate:up:docker`: Ensures PostgreSQL is running via Docker Compose, then applies migrations.

**Verify migration applied:**
```bash
docker compose exec postgres psql -U $POSTGRES_USER -d $POSTGRES_DB -c "\dt"
```

### Step 4: Test the Migration

**Test the migration works:**
```bash
# Apply migration
task migrate:up

# Run integration tests
task test:integration
```

**Test rollback works:**
```bash
# Rollback the migration
task migrate:down

# Verify database is in previous state
docker compose exec postgres psql -U $POSTGRES_USER -d $POSTGRES_DB -c "\dt"

# Reapply
task migrate:up
```

## Migration Best Practices

### DO:
- ✅ Keep migrations small and focused (one logical change per migration)
- ✅ Provide a `down` function that reverses the change when feasible
- ✅ Test both `up` and `down` migrations before merging
- ✅ goose wraps migrations in transactions automatically
- ✅ Add indexes for foreign keys and frequently queried columns
- ✅ Use `IF NOT EXISTS` / `IF EXISTS` for safety when appropriate

### DON'T:
- ❌ Modify existing migration files after they're merged (create a new migration instead)
- ❌ Use application code in migrations (keep them SQL-only)
- ❌ Make data changes that can't be reversed in `down`
- ❌ Forget to handle the error return value
- ❌ Create huge migrations that change many things at once

## Common Migration Patterns

### Add a Table

```go
func upCreateTableName(ctx context.Context, tx *sql.Tx) error {
    _, err := tx.ExecContext(ctx, `
        CREATE TABLE table_name (
            id SERIAL PRIMARY KEY,
            field1 VARCHAR(255) NOT NULL,
            field2 INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT NOW()
        );
    `)
    return err
}

func downCreateTableName(ctx context.Context, tx *sql.Tx) error {
    _, err := tx.ExecContext(ctx, `DROP TABLE IF EXISTS table_name;`)
    return err
}
```

### Add a Column

```go
func upAddColumnToTable(ctx context.Context, tx *sql.Tx) error {
    _, err := tx.ExecContext(ctx, `
        ALTER TABLE table_name 
        ADD COLUMN new_column VARCHAR(255);
    `)
    return err
}

func downAddColumnToTable(ctx context.Context, tx *sql.Tx) error {
    _, err := tx.ExecContext(ctx, `
        ALTER TABLE table_name 
        DROP COLUMN IF EXISTS new_column;
    `)
    return err
}
```

### Add an Index

```go
func upAddIndexOnTable(ctx context.Context, tx *sql.Tx) error {
    _, err := tx.ExecContext(ctx, `
        CREATE INDEX idx_table_column ON table_name(column_name);
    `)
    return err
}

func downAddIndexOnTable(ctx context.Context, tx *sql.Tx) error {
    _, err := tx.ExecContext(ctx, `
        DROP INDEX IF EXISTS idx_table_column;
    `)
    return err
}
```

## Troubleshooting

**Migration fails with "docker": executable file not found:**
- This happens if you try to run `task migrate:up:docker` in an environment without Docker (like a devcontainer).
- Use `task migrate:up` instead if your database is already running.

**Migration fails to apply:**
- Check SQL syntax
- Verify table/column names exist
- Check if migration was already partially applied
- View database logs: `docker compose logs postgres`

**Can't rollback migration:**
- Check if `down` function properly reverses the `up` function
- Some operations (like dropping columns with data) might need manual intervention
- Consider if rollback is safe with existing data

**Migration applied but tests fail:**
- Verify the schema change matches your model expectations
- Check if indexes are created correctly
- Ensure foreign key constraints are correct

**"goose: no migrations to run" but migration file exists:**
- Ensure the file is in `migrations/` directory
- Check the filename format: `YYYYMMDDHHMMSS_name.go`
- Verify the file has `package migrations` at the top
- Rebuild: `task migrate:build`

## Viewing Migration Status

```bash
# See applied migrations in database
docker compose exec postgres psql -U $POSTGRES_USER -d $POSTGRES_DB -c "SELECT * FROM goose_db_version;"

# See migration files
ls -la migrations/
```

## CI/CD

In CI, migrations run via:
```bash
task migrate:ci
```

This skips the `compose:postgres:up` dependency (database already running in CI).
