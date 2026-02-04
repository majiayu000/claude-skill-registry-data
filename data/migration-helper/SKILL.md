---
name: migration-helper
description: Assists in creating database migrations for Polibase. Activates when creating migration files, modifying database schema, or adding tables/columns/indexes. Ensures sequential numbering, proper naming, and mandatory addition to 02_run_migrations.sql to prevent inconsistent database states.
---

# Migration Helper

## Purpose
Assist in creating database migrations following Polibase conventions and ensure proper integration with the migration system.

## When to Activate
This skill activates automatically when:
- Creating new migration files
- Modifying database schema
- Adding tables, columns, indexes, or constraints
- User mentions "migration", "schema", or "database change"

## ⚠️ CRITICAL: Mandatory Steps

**NEVER skip these steps when creating a migration:**

1. **Find Latest Number**: Check `database/migrations/` for highest number
2. **Create Migration File**: `database/migrations/XXX_description.sql`
3. **⚠️ UPDATE RUN SCRIPT**: Add to `database/02_run_migrations.sql` (MANDATORY!)
4. **Test Migration**: Run `./reset-database.sh` to verify

**Skipping step 3 causes inconsistent database states!**

## Quick Checklist

Before completing a migration:

- [ ] **Sequential Number**: Incremented from latest migration
- [ ] **File Created**: In `database/migrations/XXX_description.sql`
- [ ] **⚠️ Run Script Updated**: Added to `database/02_run_migrations.sql`
- [ ] **Idempotent**: Uses `IF NOT EXISTS`/`IF EXISTS`
- [ ] **Comments**: Header and column comments included
- [ ] **Indexes**: Created for foreign keys and query columns
- [ ] **Tested**: Ran `./reset-database.sh` successfully

## Migration Naming

Format: `{number}_{description}.sql`

Examples:
- `013_create_llm_processing_history.sql`
- `014_add_email_to_politicians.sql`
- `015_create_index_on_speakers_name.sql`

Guidelines:
- Use descriptive names with action verbs
- Use snake_case
- Keep concise but clear

## Common Patterns

### Add Table
```sql
CREATE TABLE IF NOT EXISTS table_name (
    id SERIAL PRIMARY KEY,
    ...
);
```

### Add Column
```sql
ALTER TABLE table_name
    ADD COLUMN IF NOT EXISTS column_name type;
```

### Add Index
```sql
CREATE INDEX IF NOT EXISTS idx_table_column
    ON table_name(column_name);
```

See [examples.md](examples.md) for detailed patterns.

## Templates

Use templates in `templates/` directory for:
- New table creation
- Column addition
- Index creation
- Foreign key addition
- Enum type creation

## Detailed Reference

For comprehensive migration patterns and SQL details, see [reference.md](reference.md).

## Testing

```bash
# Reset database with all migrations
./reset-database.sh

# Verify migration applied
docker compose -f docker/docker-compose.yml [-f docker/docker-compose.override.yml] exec postgres \
    psql -U sagebase_user -d sagebase_db \
    -c "\d table_name"
```

## Common Pitfalls

1. **❌ Forgetting 02_run_migrations.sql**: Most common mistake!
2. **❌ Non-idempotent SQL**: Use `IF NOT EXISTS`
3. **❌ Missing data migration**: Update existing rows before adding NOT NULL
4. **❌ Breaking foreign keys**: Drop constraints before dropping tables

See [reference.md](reference.md) for detailed pitfall explanations.
