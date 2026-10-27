---
name: migrate
description: Run database or schema migrations — up, down, rollback, status, or create a new migration. Reads claude/build.md for migration commands.
---

# Migrate Skill

Run database/schema migrations in non-interactive mode.

## Usage

```
/migrate up             # Run pending migrations
/migrate down           # Roll back last migration
/migrate rollback       # Same as down
/migrate status         # Show migration status
/migrate create name    # Create a new migration file
```

## Instructions

Read `claude/build.md` for the actual migration commands configured for this project.

### Determine action from $ARGUMENTS:

| Argument | Action |
|----------|--------|
| `up` or `migrate` | `{{MIGRATE_UP_CMD}}` |
| `down` or `rollback` | `{{MIGRATE_DOWN_CMD}}` |
| `status` | `{{MIGRATE_STATUS_CMD}}` |
| `create <name>` | `{{MIGRATE_CREATE_CMD}} <name>` |

### ⚠️ Migration Safety Rules:
- NEVER mix DDL and DML in the same migration
- Test rollback after every new migration: run `up` → verify → run `down` → run `up` again
- Column names: `snake_case`, scoped by table, no redundant prefixes
- For irreversible migrations (column drop, type change): require explicit user confirmation
- NEVER run migrations directly on production without a backup confirmation
