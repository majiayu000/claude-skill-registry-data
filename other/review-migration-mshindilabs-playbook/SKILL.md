---
name: review-migration
description: >
  Analyze a database migration file for safety, reversibility, locking risks,
  and data-loss potential before it runs in production. Use when the user asks
  "is this migration safe", "will this lock the table", "can I roll this
  back", "will this cause downtime", or wants a schema migration reviewed
  before merging — CREATE TABLE, ADD COLUMN, DROP COLUMN, ALTER COLUMN, or an
  index or constraint change. Distinct from check-query-safety, which reviews
  runtime application queries (N+1s, unbounded scans, injection) rather than
  schema migration files — use that skill instead when the concern is query
  performance, not a migration.
---

# review-migration

## You are a database migration reviewer. Your job is to identify risks in a schema migration before it runs in production. Be precise and conservative — a bad migration can cause downtime, data loss, or irreversible damage.

## Step 1 — Locate the migration and schema context

Find the migration to review:

- otherwise search for recently modified migration files in common locations: `prisma/migrations/`, `db/migrate/`, `migrations/`, `src/database/migrations/`, `knex/migrations/`

Also read:

- the current schema file (`prisma/schema.prisma`, `schema.rb`, `models.py`, or equivalent) for table structure context
- any adjacent migration files to understand the sequence and baseline state

---

## Step 2 — Parse and categorize each operation

For every statement in the migration, classify it by risk:

| Operation                                                | Risk Level  | Notes                                                                                                |
| -------------------------------------------------------- | ----------- | ---------------------------------------------------------------------------------------------------- |
| `CREATE TABLE`                                           | Low         | Safe unless it references constraints on large tables                                                |
| `ADD COLUMN` (nullable, no default)                      | Low         | No rewrite needed                                                                                    |
| `ADD COLUMN` (NOT NULL with default)                     | Medium–High | Rewrites entire table in older Postgres (<11); safe in Postgres 11+ with volatile-default exceptions |
| `ADD COLUMN` (NOT NULL, no default)                      | **High**    | Will fail on existing rows                                                                           |
| `DROP COLUMN`                                            | **High**    | Destructive and irreversible without a backup                                                        |
| `DROP TABLE`                                             | **High**    | Irreversible                                                                                         |
| `RENAME COLUMN`                                          | **High**    | Breaking for any app code not yet deployed                                                           |
| `RENAME TABLE`                                           | **High**    | Breaking for all references                                                                          |
| `ALTER COLUMN` (type change)                             | **High**    | May fail or silently truncate data                                                                   |
| `ALTER COLUMN` (type widening, e.g., VARCHAR(50) → TEXT) | Medium      | Usually safe but verify                                                                              |
| `CREATE INDEX` (inline)                                  | Medium      | Takes `SHARE` — blocks writes for the whole build; reads keep working                                |
| `CREATE INDEX CONCURRENTLY`                              | Low         | Takes `SHARE UPDATE EXCLUSIVE` — writes keep working; cannot run inside a transaction                |
| `ADD CONSTRAINT` (CHECK, UNIQUE, FK)                     | Medium–High | May scan entire table; FK adds lock                                                                  |
| `ADD CONSTRAINT NOT VALID`                               | Low         | Skips historical row validation                                                                      |
| `VALIDATE CONSTRAINT`                                    | Medium      | Scans table but takes `SHARE UPDATE EXCLUSIVE`                                                       |
| Backfill `UPDATE` on large table                         | **High**    | One long transaction holding a row lock per matched row; heavy WAL and bloat — batch it              |
| `TRUNCATE`                                               | **High**    | Destructive                                                                                          |

---

## Step 3 — Check for locking risks

Name the lock each operation actually takes. Do not label every lock risk
`ACCESS EXCLUSIVE` — the lock type is what tells the reader whether reads survive,
and the wrong name points them at the wrong remedy.

`ACCESS EXCLUSIVE` — blocks reads **and** writes:

- `ALTER TABLE` (most variants)
- `ADD CONSTRAINT` (non-NOT VALID)
- `DROP COLUMN` / `RENAME COLUMN` / `DROP TABLE` / `TRUNCATE`

The lock type is not the finding on its own — how long it is held is. A nullable
`ADD COLUMN`, or an `ADD COLUMN` with a non-volatile default on Postgres 11+, takes
`ACCESS EXCLUSIVE` only for the catalogue update: milliseconds, no scan, no rewrite.
Do not report those as lock risks. Report the lock when the statement holds it
across a table scan or a full rewrite — a type change, a constraint validation, an
index build — and say which of the two it is.

`SHARE` — blocks writes for the whole build, reads keep working:

- `CREATE INDEX` without `CONCURRENTLY`

`SHARE UPDATE EXCLUSIVE` — reads and writes both keep working:

- `CREATE INDEX CONCURRENTLY`
- `VALIDATE CONSTRAINT`

A bulk `UPDATE` or `DELETE` takes only `ROW EXCLUSIVE` on the table, so it does not
block readers or writers of rows it does not touch. The risk is the row locks it
holds until commit, plus WAL volume, table bloat, and replication lag — so the fix
is batching, not a maintenance window. The mild lock does not make it a mild
finding: on a large table an unbatched backfill stays **high** severity, as the risk
table above rates it. Do not downgrade it just because it is not lock-blocking.

For each lock risk:

- name the table that will be locked and the lock type it takes
- estimate whether the table is likely large (look for seed data, existing data comments, or history of backfills in adjacent migrations)
- suggest the safe alternative where one exists (e.g., `CREATE INDEX CONCURRENTLY`, `ADD CONSTRAINT ... NOT VALID` + `VALIDATE CONSTRAINT` separately)

Note: `CREATE INDEX CONCURRENTLY` cannot run inside a transaction block. If the migration framework wraps everything in a transaction, this must be split out.

---

## Step 4 — Check reversibility

Determine whether a `down` migration exists and is correct:

- if the migration has a `down`/`revert` method, read it carefully
- verify that each `up` operation is correctly reversed in `down` (e.g., `DROP COLUMN` reversal requires re-adding with the correct type and default)
- flag `down` migrations that are empty, use `raise ActiveRecord::IrreversibleMigration`, or are missing entirely for destructive operations
- note that `DROP TABLE` in `up` cannot be safely reversed without data

If no `down` exists and the `up` is destructive, flag as a **high-severity reversibility gap**.

---

## Step 5 — Check for missing backfill logic

Identify operations that add constraints or requirements to existing data without filling that data first:

- `ADD COLUMN NOT NULL` without a `DEFAULT` or a preceding `UPDATE` to populate values
- `ADD CONSTRAINT CHECK` without verifying existing rows satisfy the condition
- `ADD CONSTRAINT FOREIGN KEY` without verifying existing values reference valid rows
- `ALTER COLUMN` type narrowing (e.g., `TEXT` → `VARCHAR(50)`) without a check that all existing values fit

For each case, indicate whether a backfill is needed and suggest the safe two-step pattern:

1. add column as nullable (or constraint as NOT VALID)
2. backfill existing rows
3. add NOT NULL constraint (or VALIDATE CONSTRAINT)

---

## Step 6 — Check for missing index coverage

Identify new foreign key columns that do not have a corresponding index. In most databases, foreign keys are not automatically indexed.

Look for:

- `ADD COLUMN` that adds a foreign key without a subsequent `CREATE INDEX`
- `ADD CONSTRAINT FOREIGN KEY` without a supporting index on the referencing column

---

## Step 7 — Report findings

Structure the report from highest to lowest risk:

```text
Migration: <filename>

Data-loss risks
1. [high] <operation> — <table>
   <why this risks data loss and what to do instead>

Lock risks
1. [high/medium] <operation> — <table>
   <expected lock type, duration concern, suggested alternative>

Reversibility gaps
1. [high/medium] <what cannot be reversed and why>

Missing backfills
1. [medium] <column or constraint> — <table>
   <what existing data is affected and the safe two-step pattern>

Missing indexes
1. [low] <foreign key column> — <table>
   <suggested index statement>

Summary
<overall verdict: safe to run / needs changes before running / blocks deployment>
```

If the migration is safe with no issues, say so explicitly.
