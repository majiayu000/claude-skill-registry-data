---
name: data-migration-safety
description: Schema, stored-data, and wire-format change discipline — old data lives forever, expand→migrate→contract, idempotent dry-run batched bounded backfills, count reconciliation, rollback plan first. Use for adding/renaming/removing columns, tables, or persisted fields; changing stored JSON or enum values; backfills and one-off data-fix scripts; API/event schema changes; anything under a migrations directory; requests to "fix the data" or "clean up old records".
---

# Data Migration Safety

Weak migration work ships the schema change and the code change in one deploy, runs the backfill as a single UPDATE, and calls it done when the script exits 0. Strong migration work enumerates every reader and writer first, sequences so no running code ever meets data it cannot handle, and is done when before and after counts reconcile.

## The prime rule: old data lives forever

Every row/document/event written under the old shape still exists after your deploy. Reads must tolerate missing new fields (default them), present old fields (ignore or map), and malformed historical values (degrade per record; one bad record must never take down the collection). New required fields are required for new writes only.

## 0. Enumerate readers and writers first

Grep the field/column/table name across app code, raw queries, serializers, reports, ETL jobs, fixtures, and any other service sharing the store. Record the list. A rename is a drop plus an add for every reader on that list.

## Expand → migrate → contract (never in one step)

1. **Expand**: add the new column/field/shape alongside the old. Code writes both (or writes new, reads either). Deploy. Nothing depends on the new shape yet.
2. **Migrate**: backfill old records to the new shape. Reconcile counts.
3. **Contract**: only after every reader uses the new shape and the backfill is reconciled — remove the old field/writes. Separate deploy, days later, not minutes.

Collapsing these creates the window where old code meets new schema (or new code meets old data). The same sequencing applies to API/event contracts: additive first, consumers migrate, then remove — coordinate with every consumer on your list and assume one you missed.

## Backfill / data-fix scripts

- **Idempotent**: filter to unmigrated rows; upsert, never blind-insert. Scripts die mid-run; re-runnability is the recovery plan.
- **Dry run first**: a mode that reports what WOULD change (counts + sample IDs) without writing. Compare the count to expectation before the real run — "expected ~2k, script says 1.4M" is the disaster caught early.
- **Batched with progress**: chunked commits, logged progress, resumable. One giant transaction locks the table and loses everything on failure.
- **Bounded**: an explicit WHERE clause scoping exactly the intended records.
- **Before-image** of affected rows (backup table, export) when the change is destructive — that is the rollback.

## Where it runs is a decision, not a default

Never execute a migration or data script against a shared or production store on your own initiative. Run it locally or against a copy first; then state the target (host/database name), the dry-run counts, and the rollback path, and wait for explicit go-ahead. For schema migrations, run up → down → up locally before committing: a down that has never run is not a rollback.

## Verification gates

Before: count the affected set; back it up if destructive. After: recount — migrated + remaining + errored must equal the before-count — spot-check sample IDs end-to-end through the real read path (app code, not just SQL), and watch error rates after deploy. Done means the numbers reconcile, not that the script exited 0.

## Rollback thinking

Write down, before running: "if this is wrong, how do I get back?" Acceptable: restore from the before-image; the old field still exists (expand/contract); a tested inverse script. If the honest answer is "we can't", get explicit sign-off before proceeding.

## Repo-reality check

Migrations live wherever THIS project keeps them (some repos gitignore the migrations dir — then the commit message/docs carry the SQL). Match the project's migration tooling and naming; never apply ad-hoc schema changes that bypass the migration history.

## Report

When the deliverable is a review of someone else's migration, do the arithmetic on their own numbers (row counts, batch sizes, a staging rate scaled to production volume, a log's final count against the before-count) and report the result as a finding. A count that does not reconcile or a duration that does not fit the window is the finding; "might be slow on prod" is not.

Include: the reader/writer list, before-count, dry-run count, after-count reconciliation (migrated/remaining/errored), sample IDs verified through the read path, where it ran, and the rollback path.
