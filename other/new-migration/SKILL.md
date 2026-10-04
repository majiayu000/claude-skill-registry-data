---
name: new-migration
description: Create and validate an Alembic migration safely. Use when changing the database schema.
argument-hint: "[description] e.g. add-index-on-enrollments-status"
disable-model-invocation: true
allowed-tools: Bash(alembic *), Bash(python *), Read, Edit
---

Create a safe Alembic migration for: $ARGUMENTS

## Step 1 — Verify current state
```bash
alembic current
alembic history --verbose
```

## Step 2 — Generate migration
```bash
alembic revision --autogenerate -m "$ARGUMENTS"
```

## Step 3 — Review the generated file
Read the generated migration file carefully. Check:
- [ ] `upgrade()` does exactly what's needed
- [ ] `downgrade()` properly reverses the upgrade
- [ ] No accidental table drops or column removals
- [ ] ForeignKey constraints have correct `ondelete` rules
- [ ] Indexes are created for all FK columns and frequently filtered columns
- [ ] Enum types are handled correctly for MySQL

## Step 4 — Test upgrade
```bash
alembic upgrade head
```

## Step 5 — Test downgrade
```bash
alembic downgrade -1
alembic upgrade head
```

## Step 6 — Confirm
Report:
- Migration file path
- What it does (upgrade)
- What it undoes (downgrade)
- Any manual steps needed (e.g. data migration)

**IMPORTANT:** Never modify a migration that has already been applied to staging or production. Create a new migration instead.

$ARGUMENTS
