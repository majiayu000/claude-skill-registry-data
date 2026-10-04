---
name: migrate
description: Safely apply pending database migrations. Backup first, list pending, apply in order, verify schema, report. Rollback on failure. Use when user says /migrate, "apply migrations", "pending migrations", "run the SQL", or when PARTIAL items are blocked on unapplied migrations.
---

# MIGRATE (Apply Pending Database Migrations)

## Purpose

Safely apply pending SQL migrations with backup, verification, and rollback capability.

## Procedure

### Phase 1: Discover Pending

1. Glob `database/migrations/*.sql`
2. Check which have been applied (query `drizzle_migrations` table or equivalent)
3. List pending migrations in timestamp order
4. Report: "N pending migrations found"

If zero pending: "All migrations applied. Nothing to do."

### Phase 2: Review

For each pending migration, show:

```
### Migration: [filename]
- Tables affected: [list]
- Operations: [CREATE/ALTER/INSERT/etc]
- Destructive: YES/NO
- Reversible: YES/NO
```

If ANY migration contains DROP, DELETE, TRUNCATE, or column type changes:
**STOP. Show the SQL. Ask for explicit approval.**

### Phase 3: Backup

1. Run `scripts/backup-db.sh` or equivalent
2. Verify backup file exists and has reasonable size
3. Record backup path and timestamp
4. Report: "Backup saved to [path] ([size])"

### Phase 4: Apply

For each pending migration (in order):

1. Apply the SQL
2. Verify it succeeded (no errors)
3. If error: STOP immediately, report which migration failed and why
4. Log: "Applied [filename] successfully"

### Phase 5: Verify Schema

1. Run `npx drizzle-kit generate` or schema check to confirm ORM matches DB
2. Run `npx tsc --noEmit --skipLibCheck` to confirm types still valid
3. If schema drift detected, report it

### Phase 6: Report

```
## Migration Report [date]
| # | Migration | Status | Tables |
|---|-----------|--------|--------|
| 1 | 20260517000001_foo.sql | APPLIED | events, clients |
| 2 | 20260517000002_bar.sql | APPLIED | menus |

Backup: [path]
Schema check: PASS/FAIL
TypeScript: PASS/FAIL
```

## Rollback Protocol

If a migration fails mid-batch:

1. Do NOT continue with remaining migrations
2. Report which migration failed and the error
3. Ask: "Restore from backup? (backup at [path])"
4. If yes: run `scripts/restore-backup.sh [path]`

## Constraints

- NEVER apply migrations without backup first
- NEVER run `drizzle-kit push` (that's a different, more dangerous operation)
- NEVER apply destructive migrations without showing SQL and getting approval
- Always apply in timestamp order, never skip
- Production data safety is highest priority
