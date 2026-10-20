---
name: migrate-git-datastore
description: >-
  Load this skill when a git-backed or file-based JSON store may have to become a real database, or
  to decide whether it is time yet. Trigger on "we have outgrown the file store", "move off files to
  Postgres", "migrate the git datastore", "verify the backfill".
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Requires the git CLI (2.x) on PATH and Python 3.9+ for the bundled `scripts/gitexport.py` and
  `scripts/verify.py`, which are standard library only and connect to no database. Loading the
  export additionally needs the target engine and its client: PostgreSQL with `psql`, or SQLite
  with `sqlite3`. Neither is assumed installed.
license: Apache-2.0
---

# Migrating a git-backed datastore to a database

The git store was a deliberate stage. This is how to leave it without downtime,
without losing writes, and without discovering the data was messier than
expected halfway through a backfill.

The task is done when the "is it time" verdict is stated. If a trigger has fired, it is also done
when `verify.py` passes for every project, each project is cut over, and the archive bundle exists.

Assumed source layout (what `ceh-git-datastore:build-git-datastore` produces):

```
refs/heads/project/<pid>
  meta.json
  collections/<collection>/<record-id>.json
```

A folder-of-JSON-files store works too — commit it to a git repo in this shape
first, then follow the same path. That is a real shortcut, not a detour: it buys
you the pinned snapshots that make the rest of this safe.

## Procedure

### First: is it actually time?

Migrating is a week of work and a permanent increase in operational surface. Run
`scripts/gitexport.py inventory <repo>` and check it against the triggers.

**Migrate now** if any of these hold:

- CAS retries per write are climbing, or write latency is visibly degrading
- More than one app node is needed, or the platform is moving to serverless
- Cross-project queries, reporting, or full-text search are now product
  requirements rather than nice-to-haves
- Records per project are past ~50k, or collection scans dominate response time
- A right-to-erasure obligation has appeared — git history cannot satisfy it
- A third derived index is about to be hand-rolled

**Do not migrate yet** if the honest answer is:

- "It feels unprofessional." Not a reason. It works or it does not.
- "We might scale later." Migrate when the trigger fires, not in anticipation.
- "One query is slow." Measure it. A 700-record scan takes ~220 ms in one batch;
  that is often an N+1 read pattern, not a storage problem.

Say the verdict plainly before planning anything. Telling someone to keep the
git store for another quarter is frequently the correct output of this skill.

### Choosing the target

**SQLite** if the app runs on one node with a persistent disk. It is a file, so
the operational model does not change at all, and it buys real SQL: indexes,
joins, aggregates, constraints, full-text search via FTS5. For a single-node app
this is the right target far more often than people expect, and it is a
one-afternoon migration instead of a one-week one.

**Postgres** if you need multiple app nodes, concurrent write throughput, real
types (`jsonb`, arrays, `timestamptz`), or managed hosting with backups and
failover someone else operates.

**Do not** go to a document store (Mongo, DynamoDB) just because the records are
JSON. The reason to leave is usually querying and constraints, which is exactly
what those give up. If schemaless is genuinely wanted, the git store already did
that more cheaply.

Going git → SQLite → Postgres later is a legitimate path. The interface work is
done once and the second hop is much easier than the first.

### Why this is tractable: pinned snapshots

The property that makes a git source better than any other file store: **a commit
sha is an immutable snapshot of an entire project.**

So the migration is not "copy a moving target". It is:

1. Record the commit each project is at right now (the _pin_).
2. Backfill from those exact commits, with no time pressure — the source cannot
   change underneath you.
3. At cutover, ask git precisely what changed since the pin, and replay only
   that.

Step 3 is exact, not approximate. `git diff --name-status <pin> <current>` gives
adds, modifies, **and deletes**. Deletes are the one that catches people out: a
catch-up that replays only upserts silently resurrects every record deleted
during the migration window. A timestamp-based catch-up cannot see deletes at
all.

`scripts/gitexport.py export` writes the pins to `manifest.json`; `changed`
turns them into the catch-up set. Keep that manifest — it is the contract.

### The sequence

**1. Inventory.** `gitexport.py inventory <repo>` — projects, collections,
record counts, bytes, commit depth, plus a read on what the shape implies.

**2. Profile and design the schema.** `gitexport.py infer <repo>` profiles every
field across every project and proposes DDL. Treat the output as a first draft
to argue with, not an answer. It flags the three things that actually break
backfills: type drift, absent-vs-null, and fields present in only some records.
See `references/schema-design.md` for the column-vs-JSONB decision.

**3. Clean the data at the source.** Fix drift and normalise timestamps _in the
git store_, before exporting — one transaction per project, which means one
commit, which means an instant `update-ref` rollback if it goes wrong. Cleaning
during export instead means the git store and the database disagree forever, and
every future comparison is noise.

**4. Create the schema and export.** Apply the DDL, then
`gitexport.py export <repo> <outdir>` for pinned JSONL plus the manifest.

**5. Backfill.** Load the JSONL with the bulk path for your engine (`COPY` for
Postgres, `.import` or a single transaction for SQLite). Constraints will reject
rows — that is the point, it is finding real problems. Fix them at the source
and re-export rather than loosening the constraint.

**6. Verify.** `scripts/verify.py` compares the git-side export against a dump of
what the database actually returns. Row counts alone are not verification: a
test with a corrupted row and a dropped row had _matching counts_ on both sides
and was still wrong.

**7. Dual-write.** Both backends, git still authoritative. Log divergence rather
than failing requests. Let it run long enough to cover a weekly cycle if you
have one.

**8. Cut over per project.** Because each project is an independent ref, cut over
a few first, verify, then continue. Full detail in `references/cutover.md`.

**9. Archive, do not delete.** `git bundle create archive.bundle --all` gives a
single file with all data and all history. Keep it. It has settled more "was it
always like that?" arguments than any log.

### Files

- `scripts/gitexport.py` — `inventory`, `infer`, `export`, `changed`. Stdlib
  only, no database driver needed.
- `scripts/verify.py` — compares the git export against a database dump; exits
  non-zero on mismatch so it can gate a deploy.
- `references/schema-design.md` — column vs JSONB, keys, indexes, tenancy,
  what to do with history.
- `references/cutover.md` — dual-write, per-project cutover, verification gates,
  rollback, and how to decide it is done.
- `references/postgres.md` and `references/sqlite.md` — engine-specific loading,
  types, and gotchas.

## Rules

### What actually breaks

Each of these was observed on a realistic test store, not hypothesised:

- **Type drift.** A field that is an int in most records and a string in a few
  (`points: int:1138, str:32`). The backfill dies partway with half the rows
  loaded. Find it with `infer`, fix it at the source.
- **Absent vs explicitly null.** A field missing from some records and `null` in
  others. SQL collapses both to NULL and the distinction is gone permanently.
  Decide before, not after.
- **Deletes during the migration window.** Upsert-only catch-up resurrects them.
  Use `--name-status` and handle `D`.
- **Timestamp formats.** Git stored `...T10:00:00.000Z`; Postgres returns
  `...+00:00`. A naive comparison flags every row as different, and a report that
  cries wolf gets ignored. `verify.py` normalises this.
- **Implicit tenancy.** `project_id` lived in the ref name, not the record. If
  the export does not inject it, every row loses its tenant. It must be part of
  the primary key.
- **Duplicate ids across projects.** Ids were unique per project, not globally.
  The primary key is `(project_id, id)`.
- **Reserved words.** A collection called `order` or a field called `user` needs
  quoting or renaming.
- **Empty projects.** Refs with no records. Confirm they are live tenants and not
  abandoned refs before creating rows for them.
- **Missing constraints.** Git enforced only path uniqueness. Adding NOT NULL and
  foreign keys will surface data that has been quietly broken for months. Better
  now than later.

### Working style

Work in phases. Report at each phase what was found,
what it implies, and what needs a decision — the inventory and profile outputs
frequently change the plan, because a store that is 90% one project, or has a
field carrying three types, wants a different sequence. And keep saying the
unwelcome thing when it is true: that the data needs cleaning first, that SQLite
is the better target, or that the migration should wait.

## Stop conditions

- No migration trigger has fired → say the verdict plainly and keep the git store. Do not plan the
  migration.
