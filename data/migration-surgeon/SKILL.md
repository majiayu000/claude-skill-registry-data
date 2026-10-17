---
name: migration-surgeon
description: "Schema migration surgeon: diffs two schema states (SQL DDL or Prisma), then generates the complete package nobody writes by hand - forward migration, rollback, pre/post validation queries and a risk protocol with explicit data-loss warnings. NEVER executes anything against a database; generates files only. Trigger: /migrate"
trigger: /migrate
---
# /migrate

Schema migrations are open-heart surgery. This one comes with
rollback, validation and a risk protocol - as a generated file package,
never as execution.

## What this is for

- From two schema states the package emerges that nobody writes by hand:
  forward migration, tested rollback, validation queries,
  risk protocol with explicit data-loss warnings.

## PROTECTION RULE - never execute, never copy into target project without approval

**This skill NEVER executes a migration against a database.** It
generates files exclusively. No access to live databases.

The migration package is ALWAYS first created in `migration-<date>/` in the
current **working directory** and shown to the user - never written directly
into the target project. Only after explicit user approval may the package
additionally be copied into the target project (edit action, no script).

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/migrate -help` or `/migrate -h` (without further arguments) is invoked:
output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-OldSchema` + `-NewSchema` (files or directories) and the
SQL dialect (postgres|mysql|sqlite|mssql - required, ask if unknown; for
Prisma read from the `datasource` block). Get confirmation.

### Step 3 - Diff

```powershell
& "<SKILL_DIR>/scripts/schema-diff.ps1" -OldSchema "<old>" -NewSchema "<new>"
```

Format mix (errors, exit code != 0): forward message, stop. Identical
schemas (0 changes): report "No changes" - **do not generate an empty package**.

### Step 4 - Rename clarification

Present each `renameCandidate` to the user individually (rename = data preserved;
drop+add = data lost - that is the entire difference). Without user response:
treat as drop+add, but mark RED in the risk protocol.

### Step 5 - Risk classification

Classify each change:

- **lossless**: add table/column/index, widen column.
- **lossy**: remove column/table, narrow type, add NOT NULL on existing data,
  add UNIQUE on existing data.
- **lock-risky**: operations that can hold long locks on large tables
  (name dialect-specifically).

### Step 6 - Generate package (5 files, `migration-<date>/`)

1. **`01-forward.sql`**: constraint-safe order (columns first, then FKs;
   drops last). Lossy steps individually, with
   comment-block WARNING before each. NOT NULL introduction as three-step
   (nullable column + backfill placeholder + SET NOT NULL), backfill as marked
   TODO with suggestion.
2. **`02-rollback.sql`**: exact reversal in reverse order. Non-reversible
   steps (dropped data) comment as such - rollback restores the schema, data
   only via backup (notice block at top).
3. **`03-validate-pre.sql`**: counts before migration, checks for new
   constraints (how many existing rows violate the future
   NOT NULL/UNIQUE NOW - run before migration), orphan checks for
   new FKs.
4. **`04-validate-post.sql`**: counts after migration for comparison.
5. **`00-protocol.md`**: diff summary, classification of each change
   with evidence (diff entry), data-loss section PROMINENT (even if empty:
   explicitly state "no lossy operations detected"),
   recommended order (pre-validate -> backup -> forward -> post-validate),
   open questions (renames without answer, unparsed statements).

`unparsed` not empty: read the raw texts of both states and diff manually,
mark as "manually checked" in the protocol instead of ignoring.

Dialect feature missing (e.g. sqlite cannot `DROP COLUMN` before 3.35):
generate dialect-specific alternative (e.g. table rebuild) or mark as
manual work.

Evidence requirement: each generated migration line must be traceable to a
diff entry - generate nothing that the diff does not show.

### Step 7 - Summarize

State the package path, summarize the risk protocol,
ALWAYS explicitly mention data-loss warnings (even if none exist).

## Usage

```
/migrate                              # interactive
/migrate <old> <new> <dialect>        # diff + generate package
/migrate -help
```


