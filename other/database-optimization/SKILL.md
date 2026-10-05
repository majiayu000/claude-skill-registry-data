---
name: database-optimization
description: >
  Use when writing or reviewing database queries, views, indexes, or schema for
  correctness and performance. Invoke whenever you: add or change ANY query (ORM or
  raw), touch an EntitySchema/entity/migration, design an index, build or tune a
  (materialized) view or read model, or investigate "this endpoint/list is slow".
  In a TypeORM project, load this before writing ORM code — it carries live-verified
  gotchas unit tests do not catch. Do NOT use for deciding which service owns a table
  or where logic lives — that's service-architecture; do NOT use for how to run/migrate
  a project locally — that's project-config.
---

# Database Optimization

Goal: queries and schema that are correct AND efficient. Don't ship a query you haven't
reasoned about — and, wherever a real database is reachable, measured. A query that "looks
right" but was never executed against real data is the main source of prod-only failures
in this domain.

## Workflow

Follow in order — each step gates the next.

### 1. Read the prior work for this stack

Check `LEARNINGS.md` beside this skill, when your copy keeps one (and the reference files
below), for the engine, ORM conventions, and known traps before writing anything — most of
this skill's value is already-paid-for lessons. This install's stack: `LOCAL.md` beside
this skill, when your copy keeps one — *Stack*.

### 2. Understand the access pattern before optimizing

Pin down cardinality, filters, joins, sort, expected row counts, and read vs. write
frequency. An index or view chosen without this is a guess — you can't rank the levers
until you know what the query actually does per request.

### 3. Write the query set-based and through the ORM

- **Use the ORM (EntitySchema + repository/query builder), not raw `manager.query`** —
  standing user directive: type-safe, naming-strategy-aware, whitelist-friendly. Drop to
  parameterized raw SQL only when the ORM genuinely can't express it (say why inline).
- **Keep it set-based:** no N+1; batch; push filtering into SQL, not app code.
- **Ownership/scoping checks via `EXISTS (...)`** subqueries, not join-then-distinct.
- **Avoid row explosion:** a one-to-many join then DISTINCT/GROUP BY multiplies rows
  before collapsing them — aggregate in a subquery / `json_agg` / lateral instead.
- **ORM joins first; a view only to amortize a genuinely heavy query** — and if it's
  that heavy, it's usually a *materialized* view (see reference file).
- Check the hard rules below — several correct-looking TypeORM constructions fail only
  at runtime.

### 4. Measure on realistic data

Run `EXPLAIN (ANALYZE, BUFFERS)` (or the engine's equivalent) on realistic data; compare
before/after. Look for seq scans on big tables, nested-loop blowups, sorts spilling to
disk, and row-count explosions. Index the columns in filters/joins/sort (composite/
partial for common predicates), don't over-index write-heavy tables, and verify the
planner actually USES the index — an unused index is pure write cost.

Gate: do not claim a performance win without a before/after measurement, and do not
trust a timing taken on a contaminated local DB (zombie queries from timed-out probes
skew everything; this install's perf-testing hygiene notes: `LOCAL.md` beside this skill,
when your copy keeps one — *view-materialization references*).

### 5. Live-verify the query actually runs

Mocked query-builder doubles execute no SQL, so a whole class of TypeORM bugs passes
unit tests and 500s live. Cheap middle ground: a throwaway ts-node `DataSource` script
running the exact builder against the dev DB (recipe in `LEARNINGS.md` beside this skill,
when your copy keeps one: "Live-verify a TypeORM query WITHOUT booting the app"). Gate: any
new EntitySchema/relation/query-builder work gets a live execution before you call it done.

## Hard rules — TypeORM / Postgres (all live-verified failures)

Each of these passed unit tests and failed against a real database. Details live in
`LEARNINGS.md` beside this skill, when your copy keeps one, unless noted.

1. **Pin a canonical projection for UNIONs.** `SelectQueryBuilder` reorders `.addSelect()`
   output (entity-matched columns group ahead of raw expressions), so hand-built
   `UNION ALL` branches can emit different column orders → type-mismatch errors or silent
   positional misalignment. Wrap each branch in `SELECT <explicit column list> FROM (branch)`.
2. **Ordering a paginated query by a JOINED column via `getMany`/`getRawAndEntities`
   crashes** (`column distinctAlias.<col> does not exist`). Use `getRawMany()` + explicit
   select aliases + a raw-row mapper; don't route the order string through `QueryOrderPipe`.
3. **`REFRESH MATERIALIZED VIEW CONCURRENTLY` requires a unique index on the view's
   grain** — if the view can emit duplicate keys, use `DISTINCT ON (key) … ORDER BY` in
   the view body to guarantee one row per grain (this install's notes: `LOCAL.md`
   beside this skill, when your copy keeps one — *view-materialization references*).
4. **Soft-delete predicate parity:** reads must filter `destroyed_at IS NULL` with the
   same predicate the write path uses — a read that skips it resurrects deleted rows.
   Exception: byte-parity ports reproduce the SOURCE query's actual WHERE (read it; don't
   assume). On a LEFT join, `child.destroyed_at IS NULL` also keeps join-MISS rows — add
   `child.id IS NOT NULL` or inner-join.
5. **`createDate`/`updateDate` EntitySchema flags do NOT add a DB default** — inserts
   into Rails-owned tables (no DB default) violate NOT NULL at runtime. Set
   `createdAt`/`updatedAt` explicitly (`new Date()`) on every write path; a global
   subscriber covers the general case.
6. **Any schema or view change needs a generated TypeORM migration** — publishing the
   model package only updates TS types, never the database (this install's notes:
   `LOCAL.md` beside this skill, when your copy keeps one — *view-materialization
   references*).
7. **Repository/ORM API over raw `manager.query`** (step 3) — including tiny lookups
   like `public_slug → id`.
8. **Write migrations against the DEPLOYED Postgres major, not your local one.** Local
   dev ran PG15+ while staging and prod ran **14**, so a `UNIQUE NULLS NOT DISTINCT`
   migration passed unit tests *and* a real local `migrate`, then failed the staging
   prestart with `syntax error at or near "NULLS"` — and the service **auto-reverted**,
   producing a no-op deploy that looked deployed-but-stale. Whenever the deployed major
   is older than local, ban the newer major's syntax (on 14 that was `MERGE`,
   `NULLS NOT DISTINCT`, FK `SET NULL (col_list)`, and security-invoker views).
   When unsure a migration is portable, `SELECT version()` on the target before trusting
   a local pass. A failed `migrate` task is a **release failure, not a skip**.
9. **A session timezone mismatch silently zeroes timestamptz-vs-naive comparisons.**
   Joining `timestamptz` values against naive `date_trunc(...)` results casts the naive
   side using the **session** timezone, so they match only under UTC. A local cluster
   defaulting to America/New_York made a view read ALL-ZERO across three sessions of
   probing and nearly shipped as a "platform-wide data gap"; under `SET timezone='UTC'`
   the same restore held 1,746 real partner-months. **On any suspicious all-zero read
   from a view mixing timestamptz and naive timestamps, check `SHOW timezone` FIRST**,
   run data-validation probes under `SET timezone='UTC'` for prod parity, and
   `ALTER DATABASE <db> SET timezone='UTC'` on local prod-restores.
10. **Two ORM configs are one registration list.** A TypeORM project typically carries
    both a `data-source.ts` (what the CLI reads) and the app's DI config, each needing
    the same `entities`/`migrations` arrays — and duplicating them guarantees eventual
    drift. **The split hides it:** the CLI drives only `data-source.ts`, both set
    `migrationsRun: false`, so a missing app-side entry is 100% silent — no failing
    test, no boot error — until code relies on it. Export the arrays from ONE shared
    module both configs import, preserving migration order exactly.
11. **Re-verify a migration timestamp slot at the commit you will actually build on,
    immediately before writing the file.** A slot `ls`-ed during research goes stale the
    moment you rebase — one collision came from *another branch of the same person's own
    parallel work* landing in that exact slot hours later. When briefing a slot to anyone
    else, add "verify this yourself; do not trust me": that line is what turns a silent
    divergence into a clean stop.

## Designing a constraint

- **Read the producer, not just the schema.** A `UNIQUE(user_id, cadence, period_start)`
  looked perfectly sensible in isolation, but the workbook parser feeding it keyed
  duplicates on `payDate + '\0' + source` — so two parents on one date from different
  sources were a shape **the source data explicitly permitted and the child table could
  not store** (a real event: an employer change with an overlapping pay date). When
  reviewing a uniqueness or identity constraint, go find the notion of identity used by
  whatever validates, parses, or imports the rows. **If the two disagree, the schema is
  usually the one that's wrong** — the parser was written against reality.
- **A constraint that no current data violates is not proven; it is untested.** That one
  was reachable through the ordinary write path as a raw `QueryFailedError` (500) — the
  back-fill slice merely got there first.
- **Narrow a wrong constraint rather than dropping it globally** — make it partial for
  the subtype that genuinely needs it. ⚠️ In Postgres a partial unique **cannot be a table
  CONSTRAINT**; it must be `CREATE UNIQUE INDEX … WHERE …`
  (`ADD CONSTRAINT … UNIQUE (…) WHERE …` is not valid SQL). TypeORM expresses it as
  `@Index(name, [cols], { unique: true, where: "…" })`. A partial unique *index* violation
  still populates the error's `constraint` field with the index name (SQLSTATE 23505), so
  specs can assert on it exactly as they do for a real constraint.
- **Prefer a lossy-but-safe key over a correct-but-undeployable constraint when prod data
  is unknowable** — one that fails on deploy against duplicates you cannot prove absent is
  worse than a design that degrades quietly. Record the reasoning in the commit so the
  "better" design isn't naively reapplied later.
- **Be honest about rollback.** A `down()` that re-adds a constraint will fail on any
  database that has since stored the now-legal row. Say so rather than implying the
  migration is cleanly reversible.
- **Ask whether the column is read at all before fighting to constrain it.** A field that
  looked like domain state fed nothing; deleting it *dissolved* a "we must query prod
  first" blocker rather than answering it.

## Common failure modes

- **Shipping a query verified only by mocked unit tests** — every hard rule above is a
  bug class mocks cannot see. Live-verify (step 5).
- **Trusting `COUNT(*)` as a proxy for the real read:** the planner prunes unused
  correlated subselects for COUNT but computes them for `SELECT * … LIMIT` — a fast
  count with a hanging page read means materialize, not rewrite (this install's notes:
  `LOCAL.md` beside this skill, when your copy keeps one — *view-materialization
  references*).
- **"Fixing" a slow view by rewriting joins** when the cost is a per-row correlated/
  LATERAL subselect — no rewrite saves it; materialize.
- **Adding a DB view for join convenience** — views are a performance tool; the query
  builder handles multi-table filter/sort fine.
- **Assuming raw rows behave like hydrated entities:** `getRawMany` skips transformers
  (numerics arrive as strings — coerce), and node-pg auto-parses jsonb (don't
  `JSON.parse` twice).
- **Perf-testing against a dirty local DB:** timed-out HTTP probes leave zombie
  server-side queries that contaminate every later timing — clear
  `pg_stat_activity` first.
- **A cast or dedup in a view silently defeats the index** the planner would
  otherwise use — the query stays correct and quietly goes seq-scan. Check the plan,
  not just the result.
- **A delete-and-recreate importer silently drops any column absent from its INSERT.**
  Two provenance columns were nulled on every run for weeks, destroying user-built
  reconciliation links, because they simply weren't listed. The rows looked fine; the
  data they referenced was gone. Audit the insert object against the entity whenever an
  importer rebuilds rows.

## References

Read the matching file before working in its area:

- This install's view/materialized-view notes (when a view change needs a migration,
  build-then-swap, unique grain for CONCURRENT refresh, perf-testing hygiene): `LOCAL.md`
  beside this skill, when your copy keeps one — *view-materialization references*.
- [postgres-tuning.md](postgres-tuning.md) — general engine-level Postgres: server/memory
  config, diagnostics (`pg_stat_statements`, EXPLAIN/BUFFERS), bloat & autovacuum, bulk
  ops, locks, read-replica scaling, pgvector. Consult when the question is general
  Postgres rather than project-specific.

## Before you call this done

- [ ] Access pattern understood (filters, joins, sort, cardinality) — not guessed.
- [ ] ORM-first; any raw SQL is parameterized and justified inline.
- [ ] Checked the hard-rules list; none of the seven apply unhandled.
- [ ] Executed the real query against a real DB (DataSource script, psql, or live app).
- [ ] Perf claims backed by before/after `EXPLAIN (ANALYZE, BUFFERS)` on clean data.
- [ ] Schema/view changes carry their generated migration.

## Related skills

- [tdd-skill](../tdd-skill/SKILL.md): mocked green is necessary, not sufficient; a DB-touching change gets a real-database run.
- [deprecation-and-migration](../deprecation-and-migration/SKILL.md): shared-table expand/contract changes, where old and new code hit the DB at once.
- [data-analytics](../data-analytics/SKILL.md): the metrics and dashboards whose queries this skill makes fast.

## Capturing learnings (session-handoff protocol)

Accumulate query/schema tuning knowledge in `LEARNINGS.md` beside this skill, when your
copy keeps one (project-specific ORM/query-building wins & gotchas), and engine-level
general knowledge in [postgres-tuning.md](postgres-tuning.md). On handoff /
"update skills" / after DB work: record the optimization, the measured effect, the access
pattern, and the reusable rule under a new `##` section in the most relevant file (not this
index). Dedupe/merge, tag by project/engine. If a file outgrows ~250 lines, split it
further. Read the relevant file(s) before DB work. (Where this install files view
learnings: `LOCAL.md` beside this skill, when your copy keeps one — *Capturing
learnings*.)
