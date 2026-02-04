---
name: ecto-migration-helper
description: Create, manage, and safely run Ecto database migrations with proper rollback handling and best practices. Use when working with database schema changes, adding columns, or modifying constraints.
allowed-tools: Bash, Read, Edit, Write
---

# Ecto Migration Helper

This skill helps create and manage Ecto migrations safely with proper patterns and rollback support.

## When to Use

- Creating new migrations
- Modifying existing tables
- Adding/removing indexes
- Changing constraints
- Data migrations
- Rolling back migrations

## Creating Migrations

### Generate Empty Migration
```bash
mix ecto.gen.migration add_email_to_users
```

Creates: `priv/repo/migrations/TIMESTAMP_add_email_to_users.exs`

### Migration Naming Conventions
- `create_table_name` - Creating new table
- `add_field_to_table` - Adding column
- `remove_field_from_table` - Removing column
- `add_index_to_table_on_field` - Adding index
- `modify_field_in_table` - Changing column type
- `add_constraint_to_table` - Adding constraint

## Common Migration Patterns

### Adding a Column
```elixir
defmodule MyApp.Repo.Migrations.AddEmailToUsers do
  use Ecto.Migration

  def change do
    alter table(:users) do
      add :email, :string
    end
  end
end
```

### Adding Column with Default
```elixir
def change do
  alter table(:users) do
    add :active, :boolean, default: true, null: false
  end
end
```

### Adding Column with Index
```elixir
def change do
  alter table(:users) do
    add :email, :string
  end

  create unique_index(:users, [:email])
end
```

### Adding Foreign Key
```elixir
def change do
  alter table(:posts) do
    add :user_id, references(:users, on_delete: :delete_all), null: false
  end

  create index(:posts, [:user_id])
end
```

### Removing a Column
```elixir
def change do
  alter table(:users) do
    remove :old_field
  end
end
```

**WARNING**: Removing columns is irreversible with `change`. Use `up`/`down`:

```elixir
def up do
  alter table(:users) do
    remove :old_field
  end
end

def down do
  alter table(:users) do
    add :old_field, :string
  end
end
```

### Modifying Column Type
```elixir
def change do
  alter table(:products) do
    modify :price, :decimal, precision: 10, scale: 2
  end
end
```

### Renaming Column
```elixir
def change do
  rename table(:users), :username, to: :name
end
```

### Adding Composite Index
```elixir
def change do
  create index(:posts, [:user_id, :published_at])
end
```

### Adding Unique Constraint
```elixir
def change do
  create unique_index(:users, [:email])
  create unique_index(:users, [:organization_id, :email])  # Composite unique
end
```

### Adding Check Constraint
```elixir
def change do
  create constraint(:products, :price_must_be_positive, check: "price > 0")
end
```

## Safe Migration Patterns

### Making Columns NOT NULL

**WRONG** (will fail if existing NULLs):
```elixir
def change do
  alter table(:users) do
    modify :email, :string, null: false  # FAILS!
  end
end
```

**RIGHT** (two-step approach):
```elixir
# Migration 1: Add default, fill NULLs
def change do
  # Set default for new rows
  alter table(:users) do
    modify :email, :string, default: "unknown@example.com"
  end

  # Fill existing NULLs
  execute(
    "UPDATE users SET email = 'unknown@example.com' WHERE email IS NULL",
    ""  # No rollback needed
  )
end

# Migration 2: Add NOT NULL constraint
def change do
  alter table(:users) do
    modify :email, :string, null: false
  end
end
```

### Removing Columns Safely

**Step 1**: Deploy code that doesn't use the column
**Step 2**: Run migration to remove column (after deployment)

```elixir
# Deploy this migration AFTER code no longer references the field
def up do
  alter table(:users) do
    remove :old_field
  end
end

def down do
  alter table(:users) do
    add :old_field, :string  # Specify type for rollback
  end
end
```

### Large Data Migrations

Use batching to avoid locking:
```elixir
def up do
  execute """
  UPDATE users
  SET status = 'active'
  WHERE status IS NULL
  AND id IN (SELECT id FROM users WHERE status IS NULL LIMIT 1000)
  """

  # Repeat in batches or use recursive function
end
```

## Data Migrations

### Backfilling Data
```elixir
defmodule MyApp.Repo.Migrations.BackfillUserDefaults do
  use Ecto.Migration
  import Ecto.Query
  alias MyApp.Repo
  alias MyApp.Accounts.User

  def up do
    # Use application code in migrations carefully
    User
    |> where([u], is_nil(u.status))
    |> Repo.update_all(set: [status: "active"])
  end

  def down do
    # Usually no rollback for data migrations
    :ok
  end
end
```

### Complex Data Migration (Separate Module)
```elixir
defmodule MyApp.Repo.Migrations.MigrateUserData do
  use Ecto.Migration

  def up do
    MyApp.ReleaseTasks.migrate_user_data()
  end

  def down do
    :ok
  end
end

# In lib/my_app/release_tasks.ex
defmodule MyApp.ReleaseTasks do
  def migrate_user_data do
    # Complex logic here
  end
end
```

## Running Migrations

### Development
```bash
# Run all pending migrations
mix ecto.migrate

# Run to specific version
mix ecto.migrate --to 20250101120000

# Rollback last migration
mix ecto.rollback

# Rollback last 3 migrations
mix ecto.rollback --step 3

# Rollback to specific version
mix ecto.rollback --to 20250101120000
```

### Test Environment
```bash
# Create test database
MIX_ENV=test mix ecto.create

# Run migrations in test
MIX_ENV=test mix ecto.migrate

# Reset test database (drop, create, migrate)
MIX_ENV=test mix ecto.reset
```

### Production
```bash
# Run on production (typically via release task)
bin/my_app eval "MyApp.ReleaseTasks.migrate()"

# Or if mix is available
MIX_ENV=prod mix ecto.migrate
```

## Migration Status

```bash
# Check migration status
mix ecto.migrations

# Output shows:
# Status    Migration ID    Migration Name
# --------------------------------------------------
# up        20250101120000  create_users
# up        20250101130000  add_email_to_users
# down      20250101140000  add_profile_to_users
```

## Reversible vs Non-Reversible

### Reversible (use `change`)
- Adding columns
- Creating tables
- Adding indexes
- Adding references

### Non-Reversible (use `up`/`down`)
- Removing columns (data loss)
- execute() with SQL
- Data transformations
- Dropping tables

## Best Practices

### 1. One Logical Change Per Migration
```bash
# Good: Focused migration
mix ecto.gen.migration add_email_to_users

# Bad: Multiple unrelated changes
mix ecto.gen.migration update_users_and_posts_and_comments
```

### 2. Always Add Indexes for Foreign Keys
```elixir
add :user_id, references(:users)
create index(:posts, [:user_id])  # Always add this!
```

### 3. Specify on_delete for Foreign Keys
```elixir
# Be explicit about cascade behavior
add :user_id, references(:users, on_delete: :delete_all)  # Cascade
add :user_id, references(:users, on_delete: :nilify_all)  # Set NULL
add :user_id, references(:users, on_delete: :restrict)    # Prevent delete
add :user_id, references(:users, on_delete: :nothing)     # No action
```

### 4. Use Precision for Decimals
```elixir
# Good
add :price, :decimal, precision: 10, scale: 2

# Bad (database decides precision)
add :price, :decimal
```

### 5. Make Constraints Explicit
```elixir
# Email should be unique and not null
add :email, :string, null: false
create unique_index(:users, [:email])
```

### 6. Test Rollbacks Locally
```bash
# After creating migration
mix ecto.migrate
mix ecto.rollback
mix ecto.migrate
```

## Troubleshooting

### Migration Fails

**Column already exists:**
```bash
# Check current schema
mix ecto.migrations

# Drop and recreate if in development
mix ecto.drop && mix ecto.create && mix ecto.migrate
```

**Can't rollback:**
- Check if migration uses `change` vs `up`/`down`
- Review the migration for non-reversible operations
- May need to write custom `down` function

**Lock timeout:**
```elixir
# Add timeout to migration
@disable_ddl_transaction true  # For operations that can't run in transaction
@disable_migration_lock true   # For long-running migrations

def change do
  # Migration code
end
```

### Data Migration Issues

**Timeout on large tables:**
- Use batching
- Consider running outside of migration (Rails-style rake task)
- Use `@disable_ddl_transaction true`

**References to application code:**
- Be careful with schema changes
- Application code might change, migration won't
- Consider using raw SQL for data migrations

## Advanced Patterns

### Concurrent Index Creation (PostgreSQL)
```elixir
@disable_ddl_transaction true

def change do
  create index(:posts, [:user_id], concurrently: true)
end
```

### Conditional Migrations
```elixir
def change do
  if function_exported?(MyApp.Repo, :__adapter__, 0) do
    # Migration code
  end
end
```

### Timestamps Helper
```elixir
create table(:users) do
  add :name, :string
  timestamps()  # Adds inserted_at and updated_at
end
```
