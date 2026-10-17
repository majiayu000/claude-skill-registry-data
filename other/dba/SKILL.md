---
name: dba
description: Postgres-first DBA workflows — run a full database health audit, design and implement schema (tables, constraints, RLS, indexes, migrations + tests), clean up unused indexes / bloat / dead tuples, diagnose and fix slow queries, and investigate live database incidents (high CPU, lock storms, error spikes, connection exhaustion). Use whenever the user says "audit the database", "DB health check", "design a schema", "model this table", "add a table for X", "clean up indexes", "database bloat", "why is this query slow", "optimize this query", "explain analyze this", "investigate the database", "the DB is on fire", "high CPU on Postgres", "connection pool exhausted", or types "/dba" — even when they don't say the word "DBA" or name a specific workflow. Discovers each project's migration, test, and deploy conventions at runtime rather than assuming them.
version: 0.1.0
---

# DBA — Postgres database administration playbooks

You are running an end-to-end DBA workflow: a health audit, a schema design + implementation, a cleanup, a slow-query fix, or a live-incident investigation. This skill teaches the *how* — the sequence, the safety discipline, and the artifacts each workflow must produce. It deliberately does **not** hardcode any one project's conventions: every run starts by discovering how *this* project does migrations, tests, and deploys, and then works inside those conventions.

Two ideas govern everything below:

1. **Databases outlive applications.** App code gets rewritten; schemas and data persist for years. Optimize for clarity, invariants, and recoverability over cleverness.
2. **The database is usually production.** A careless `EXPLAIN ANALYZE` on a DELETE, an index build that blocks writes, a kill command that re-ignites — DBA mistakes are immediate and user-visible. The safety model below is not bureaucracy; it is the job.

## Rules vs. playbooks — delegation

This skill owns *workflows*: how to run an audit start to finish, how to investigate an incident, in what order, with what gates. It does not own rule-level Postgres knowledge (which index type to pick, data-type selection, connection-pool sizing, lock-mode tables, EXPLAIN-node interpretation).

For rule-level detail, check whether the `supabase-postgres-best-practices` skill is available in this session. If it is, defer to it and **cite the rule you applied** (e.g. "per `query-missing-indexes`") instead of restating its content — it covers indexes, schema design, connections, locking, data-access patterns, and monitoring in depth, and restating it here would drift out of sync. If it is *not* available, use `references/postgres-rules-fallback.md` for a condensed fallback — and say that's what you used.

## Step 0 — Discover the project (always first)

Every workflow begins with the same discovery sequence. Don't skip it because the task looks simple — most DBA mistakes are convention mistakes (a migration in the wrong format, a query against the wrong target). Read `references/discover.md` and run the full protocol. In summary:

- **D1. Locate the schema source of truth.** Find the migrations directory and read the naming convention from the actual filenames. Never assume a convention.
- **D2. Read the project's database knowledge.** Project instructions (CLAUDE.md and similar), past incident reports (`docs/pir/` or similar), architecture decision records, PR/merge checklists, test conventions. A project that has burned itself before has written down where — read it before touching anything related.
- **D3. Detect the access method.** Database MCP tools → running local stack → connection string/psql → ask the user. Stop at the first one that works.
- **D4. Establish the target and blast radius.** Know *which* database every statement will hit — local, staging, or production/linked — before running anything. Note the deploy model: if schema deploys are decoupled from code deploys, drift between them is a first-class risk to check.
- **D5. Echo a one-line discovery summary** (conventions found, access method, target, read-only or not) and confirm intent with the user. This single confirmation is what lets the rest of the run proceed without constant interruptions.

## Safety model

These rules are cross-cutting — they apply to every workflow, every time. They exist because each one maps to a real failure mode.

1. **Read-only by default.** Catalog views, `pg_stat_*`, `\d`, plain `EXPLAIN` — none of these mutate. Start there and stay there until a write is both justified and confirmed. Most DBA value (audits, diagnosis, investigation) needs no writes at all.

2. **Show the SQL before running any write or DDL.** Print the exact statement(s), name the target they will hit (local vs. production/linked), and wait for explicit confirmation. Never run a destructive operation (DROP, DELETE, TRUNCATE, table-rewriting ALTER) the user hasn't seen. The point isn't permission theater — it's that the user knows things about their data you don't.

3. **The confirmation gate scales with blast radius.** Local-stack writes: low friction, but still show the SQL. Production/linked writes or DDL: per-operation confirmation — and prefer *emitting a migration file* the user applies through their own deploy path over running DDL live. The project's deploy pipeline exists precisely to make schema changes reviewable and reversible; don't route around it.

4. **EXPLAIN before EXPLAIN ANALYZE.** `EXPLAIN ANALYZE` *executes* the statement. On a SELECT that's usually fine; on an INSERT/UPDATE/DELETE it mutates data. Read the plain `EXPLAIN` first. If you must ANALYZE a write to measure it, wrap it: `BEGIN; EXPLAIN ANALYZE ...; ROLLBACK;` — and say that's what you're doing.

5. **State the lock impact of DDL before proposing it.** Every DDL statement takes a lock; some block all writes (plain `CREATE INDEX`), some rewrite the whole table. When you propose DDL, name the lock cost and prefer the concurrent/online variant (`CREATE INDEX CONCURRENTLY`, `DROP INDEX CONCURRENTLY`, `ADD CONSTRAINT ... NOT VALID` then `VALIDATE CONSTRAINT`). Rule detail lives in the best-practices skill; *your* duty is to surface the cost every time.

6. **Wrap exploratory writes in a transaction.** Any write you run to *measure* rather than to *keep* goes inside `BEGIN; ... ROLLBACK;` unless the user has confirmed a real commit.

7. **Never raise class-40 SQLSTATEs for deterministic rejections.** SQLSTATE is an API contract with infrastructure, not just a label. Class-40 codes (`40001` serialization_failure, `40P01` deadlock) mean "transient — retry me" to retry-aware layers (PostgREST, many drivers and poolers). Raising them for a rejection that will *always* fail (a stale-write guard, a validation) creates an infinite retry loop. A real production incident of exactly this shape (PostgREST retrying a deterministic `40001` rejection forever — millions of rolled-back transactions, hours of outage) is why this rule is here. Use a custom code (e.g. `P0409`-style) for deterministic conflicts.

8. **Failed is not slow.** Statements that *error* never appear in `pg_stat_statements` — it records only successful executions. When top queries don't explain the load, check `xact_rollback` vs `xact_commit` in `pg_stat_database`. A high rollback ratio means the load is failures, and you must hunt them in logs and `pg_stat_activity`, not in the statements view.

## Choose the workflow

Route by what the user is actually asking for, then load the one playbook and follow it. If the request spans workflows (an audit finding becomes a cleanup; a slow query turns out to be an incident), finish the current playbook's artifact first, then offer the next workflow explicitly.

| User intent sounds like | Workflow | Playbook |
|---|---|---|
| "audit the database", "health check", "how's our DB doing", "review the schema" | **Audit** | `references/audit.md` |
| "design a schema for X", "add a table", "model this feature", "implement this migration" | **Design & implement** | `references/design-implement.md` |
| "clean up unused indexes", "bloat", "dead tuples", "reclaim space", "drop stale objects" | **Cleanup** | `references/cleanup.md` |
| "why is this query slow", "optimize this query", "this page times out on a query" | **Slow-query fix** | `references/slow-query.md` |
| "the DB is on fire", "high CPU", "errors spiking", "connections exhausted", "lock storm" | **Investigate** | `references/investigate.md` |

Workflow synopses (for routing sanity — the playbook has the steps):

- **Audit** — read-only sweep across schema integrity, index health, query load, bloat/maintenance, and migration drift. Produces a severity-ranked findings report. Executes nothing; ends by offering to spin findings into cleanup or slow-query runs.
- **Design & implement** — requirements → data model → user confirms → migration + access policies + tests, all in the *discovered* project conventions → applied and tested locally only. Ends with files and a pointer to the project's own deploy path.
- **Cleanup** — measure candidates (never guess), risk-rank them (an unused-looking index may back a constraint), propose SQL with lock costs, gate, execute concurrently, verify with a before/after table.
- **Slow-query fix** — reproduce, capture the plan (EXPLAIN, then ANALYZE where safe), diagnose, propose the fix with lock impact, validate on a safe target with before/after plans, offer the fix as a migration.
- **Investigate** — triage live signals (error rate leads, CPU lags), run the rollback-ratio check, `pg_stat_activity`/`pg_locks` forensics, separate mitigation from root cause, verify the fix held, hand off to `/pir` for the writeup if that skill is available.

The diagnostic SQL these playbooks use lives in `references/queries.md` as a read-only library keyed by ID (Q-IDX-UNUSED, Q-ROLLBACK-RATIO, …). Load it when a playbook cites a query ID.

## Report & artifact conventions

The reporting workflows (audit, cleanup, investigate) share one findings format so results are comparable across runs:

```markdown
| # | Area | Severity | Evidence | Recommendation | Fix (SQL — not executed) |
```

- **Severity**: Critical / High / Medium / Low. Critical = active or imminent harm (data loss risk, security hole, outage mechanism). High = will bite under growth or concurrency. Medium = cost or risk worth scheduling. Low = hygiene.
- **Evidence** is the actual catalog-query result (numbers, names), not an assertion. A finding without evidence is an opinion.
- **Fix SQL is shown, not run.** Executing fixes is a separate, gated step — or a migration file through the project's deploy path.

Implementation workflows (design & implement, cleanup, slow-query) produce **migration files in the discovered directory using the discovered naming convention**, plus tests in the discovered test convention where the project has one. Every workflow ends with:

1. an explicit **verification step** (re-run the measurement, run the tests, re-check the metric), and
2. a one-line **"what I did not touch"** disclosure, so the user knows the boundaries of the run.

## What this skill does not do

- It never runs destructive operations or DDL against a production/linked target without showing the SQL and getting explicit confirmation — no exceptions for "small" changes.
- It does not push schema changes through to production itself when the project has its own deploy path; it produces the migration and points at the project's checklist.
- It does not restate rule-level Postgres guidance that `supabase-postgres-best-practices` already owns — it defers and cites.
- It does not write the post-incident report; the investigation playbook ends with a structured handoff to `/pir` (or the findings timeline, if that skill is absent).
- It does not modify application code beyond what a fix strictly requires (e.g. a query rewrite); broader app changes belong to the normal coding flow.
