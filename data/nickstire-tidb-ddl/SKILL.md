---
name: nickstire-tidb-ddl
description: Use when adding or altering a column, table, status value, or index in the nickstire database (apps/nickstire/drizzle/). TiDB rejects several things MySQL allows, and one of them loses the row silently instead of erroring.
triggers: tidb, drizzle, column, table, index, status value, ddl, nickstire database, altering a column, schema change, mysql, silent row loss
---

# nickstire-tidb-ddl

nickstire runs on TiDB Cloud (MySQL wire protocol, not MySQL semantics).
Migrations are **hand-applied** — there is no auto-migrate. The traps below
have each cost a session at least once.

## The rule that loses data

**TiDB runs with `STRICT_TRANS_TABLES`: a write whose value does not fit the
column is REJECTED and the row is LOST** — not truncated, not defaulted.

Two ways to hit it:

1. **Out-of-enum write.** Any value not in the `ENUM(...)` list is rejected.
2. **Over-width VARCHAR.** `published_partial` (17 chars) went into a
   `varchar(16)` and was rejected, wedging rows — see the comment in
   `drizzle/0091_content_runs.sql`.

Both are worse inside a failure handler: the handler tries to record
`status = 'failed_<reason>'`, the write is rejected, and the job is left in
its previous state with no error recorded.

## Do this instead

- **Never `ENUM` for a value set that will grow.** Use `VARCHAR` + app-level
  validation. `drizzle/0099_revenue_opportunity_queue.sql` states the standing
  reason: out-of-enum writes lose the row, and ENUM evolution needs ALTERs.
- **Size status columns at `varchar(32)` or wider.** `content_runs` does this
  deliberately after the 0091 incident.
- **Before adding a status value, check the column width.** Compute the longest
  value you will ever write, not the longest one today.

### Known narrow column

`reel_jobs.status` is **`varchar(20)`** ([drizzle/schema.ts:3249](../../../apps/nickstire/drizzle/schema.ts)) —
the narrowest status column in the schema, and an outlier against the
`varchar(32)` convention.

**Do not size against the column's own doc comment.** It lists eight values
topping out at `assets_ready` (12), which suggests 8 characters of headroom.
The code writes values the comment omits — `publish_ambiguous` (17) is set at
`server/cron/jobs/dailyReelPost.ts:381`, alongside `assembled`, `needs_review`
and `review_ready`. **Real headroom is 3 characters.**

Nothing currently written exceeds the limit (verified 2026-08-03: the longest
status reaching any column is 17 chars). But `publish_ambiguous` is itself a
failure path, so the margin is thinnest exactly where a rejected write costs
the most — the job is parked with no state recorded. Enumerate the values the
**code** writes, not the ones the comment lists, and widen the column in the
same migration that adds a longer one.

## Shipping `schema.ts` AHEAD of the hand-applied DDL

Migrations are hand-applied, so there is always a window where the CODE knows
about a column the DATABASE does not. Two rules make that window survivable:

- **Grep `.from(<table>)` for projection-less `select()` reads and pin each to
  the pre-migration column set.** A bare `db.select().from(t)` enumerates every
  column in the drizzle definition, so adding a column to `schema.ts` silently
  rewrites those queries to name a column prod lacks. Adding the 0110 ledger
  columns to `audit_log` would have 500'd three such reads
  (`services/adminAudit.ts`, `services/snapApplications.ts`,
  `services/complianceLog.ts`) until the DDL landed.
- **New-column WRITES must be conditional** — build the insert values object
  and attach each new key only when the caller supplied it, so every
  pre-existing call site emits byte-identical SQL. `services/auditTrail.ts`
  does this deliberately.

The inverse of this class already cost an outage: the bridge-send guard queried
a column that did not exist and failed CLOSED for months (#1485). Same window,
opposite direction — the code and the schema disagreeing about what is real.

## DDL that TiDB accepts

- **Additive, idempotent, `INFORMATION_SCHEMA`-guarded** — follow the existing
  `scripts/migrations/*` pattern. Re-running a migration must be a no-op.
- **TiDB needs two separate `ALTER`s where MySQL allows one combined.** Split
  them.
- **TiDB rejects `ALTER`-add of a STORED generated column.** Achieve the same
  result with an application-side normalized column plus a unique index (this
  is what the customer-dedup work had to do).
- **TiDB rejects `CREATE TABLE … AS SELECT`** — `ERROR 1105: 'CREATE TABLE ...
  SELECT' is not implemented yet` (witnessed 2026-08-12 backing up
  `__drizzle_migrations`). The backup idiom that DOES work is two statements:
  `CREATE TABLE bak LIKE orig;` then `INSERT INTO bak SELECT * FROM orig;`.
  Count the rows in the copy before trusting it — and note this failure mode is
  benign only because a backup runs BEFORE the mutation it protects; put the
  backup first so a rejected copy aborts the run instead of orphaning it.

## Applying

Prod DDL runs through Railway, which injects the real connection string:

```bash
railway run --service MAINnicks-tire-auto -- node <script.cjs>
```

`apps/nickstire/docs/operations/SCHEMA_DRIFT_RUNBOOK.md` is the full procedure.
Read [prod-db-guard](../prod-db-guard/SKILL.md) before running anything that
writes — `.env` binds the production database.

**Before writing an `ALTER TABLE`, prove the table exists in production**
(`INFORMATION_SCHEMA.TABLES`, read-only). Raw SQL in a cron can name a table
no migration ever created and no Drizzle declaration knows: 2026-09-02, the
first apply of `0114` failed on statement 1 with `ER_NO_SUCH_TABLE estimates`
— the `estimate-followup` job had queried a phantom for its whole life and the
audit had called it a missing column. The migration was rewritten to its valid
half and the job retired. **Do not apply through `pnpm db:migrate`** for a
scoped change: it has no dry run and applies every unrecorded file — use the
scoped runner shape in prod-db-guard ("Applying migrations in scope").

**When the DDL ships INSIDE `handleRunMigrations`, read the live commit before
the one-tap runner.** The runner only knows the migration list of the container
that serves the tap. Before tapping, `GET /api/health` must report
`deploy.commit` = the merge SHA, and the result's `total` must match the new
list's length: a stale container reports "none failed" too. Witnessed
2026-10-02: the tap at 15:46Z ran on the old container (`62087aa2`) while the
merge was still BUILDING and applied nothing; the tap at 15:53Z did the work
(176 steps).

## Grouped queries: prove the SQL Drizzle renders

Drizzle renders a column unqualified in `SELECT` but qualified in `GROUP BY`,
and TiDB `only_full_group_by` rejects the pair. It cost NICKSTIRE-1
(2026-09-08) and then the customerIntelligence queries again (2026-10-09 to
2026-10-20, PR 3189); typecheck and unit tests passed both times because no
test rendered the real SQL. For any grouped query, render the real Drizzle
builder over a recording fake mysql2 client and assert the `SELECT` and
`GROUP BY` column forms match.

After applying, re-run `pnpm run check` from `apps/nickstire/` — `tsc` fails
against the schema until the migration is actually applied.
