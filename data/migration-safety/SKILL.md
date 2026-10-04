---
name: migration-safety
description: Write, review or apply a database schema migration without destroying data. Use for any task that creates or modifies a migration file (Alembic, Prisma, Django, Rails, Flyway, raw SQL), and before applying one to a shared environment.
---

# Migration safety

## Treat every environment as production

Staging and demo environments hold real data more often than anyone admits, and a migration
that destroys data in staging demonstrates that the same operation would run in production.
There is no "it's just staging" exception. **Never write a migration that could silently
destroy existing data.**

## Destructive operations — stop and surface to the human

Do not generate these autonomously. Describe what you intend and why, and wait for
confirmation before writing the file:

- `DROP TABLE`, `DROP COLUMN`, `TRUNCATE` — destroys rows or values permanently.
- `ALTER COLUMN … TYPE` with a lossy cast — the database rewrites the column; values that
  cannot be cast are lost.
- Removing `NOT NULL` and then dropping the column — same as above.
- `DELETE FROM` inside a migration — data loss with no recovery short of a backup.

## Safe patterns

**Adding a column.** Add it nullable first, even if the final intent is `NOT NULL`. Backfill in
a separate migration or deploy step. Add the constraint only after the backfill is confirmed.
Three small migrations beat one that rewrites data and adds a constraint at once.

**Renaming a column.** Never rename in a single deploy. Expand-contract: add the new column
nullable; write to both; backfill new from old; switch reads; drop the old column in a later
release once confirmed safe.

**Changing a type.** Lossless (`VARCHAR` → `TEXT`) may proceed with a note in the migration
comment. Lossy (`TEXT` → `INTEGER`, shrinking a `VARCHAR`) stops and asks.

**Removing a column.** Only after confirming no deployed code reads or writes it, and a backup
exists or the column is confirmed empty. In the migration direction that removes it, archive
and verify row counts and retained values while the column still exists, before the drop. A
downgrade cannot archive a column an earlier upgrade already removed:

```sql
CREATE SCHEMA IF NOT EXISTS archive;
CREATE TABLE IF NOT EXISTS archive.<table>_<revision>_before_drop AS
  SELECT id, <dropped_column> FROM <table>;
```

The archive is retained indefinitely; nobody drops it without explicit sign-off.

**Additive first.** Adding a column or table is always safer than modifying one. If the goal
can be reached by adding, add.

## Checklist before committing a migration file

- `upgrade()` contains no `DROP TABLE`, `DROP COLUMN`, `TRUNCATE` or `DELETE FROM` without
  explicit human sign-off recorded in the PR.
- Any new `NOT NULL` column either has a server default or is added nullable with a separate
  backfill.
- You read the generated file. Never rely on autogenerate output alone.
- `downgrade()` is implemented, or is an explicit no-op with a comment saying why rollback is
  impossible for this change.

## Never edit an applied migration

Once a migration has been applied to any shared environment, it is immutable. Create a new
migration to correct mistakes.

## Collapse work-in-progress migrations before review

If iterating on one logical change produced several files, collapse them into one before
opening the PR — delete and regenerate, which is safe while nothing has been applied to a
shared environment. This is different from the deliberate add-nullable → backfill → constrain
sequence, which stays as separate migrations by design.

## After merging the main branch into a feature branch

Long-lived branches frequently produce two divergent heads even without a content conflict.
Check immediately after merging (`alembic heads`, or the equivalent for the tool) and reconcile
with a no-op merge revision before running tests or committing.
