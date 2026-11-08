---
name: forge-database
description: "Playbook for databases: Postgres, Prisma, migrations (gebruik bij database)."
# Q3 fix-round original description (listing budget): "Playbook for databases: Postgres, Supabase, Prisma, Drizzle, SQLite, safe migrations, indexes, RLS (gebruik bij database of migratie)."
---

<!--
  Forge super skill (own words), assembled 2026-11-02 for (WP Q3-SKILLS).
  Source: https://github.com/supabase/agent-skills (skills/supabase-postgres-best-practices/, references/*.md)
    Commit seen: c9be0e931b7930f7d02126d04774d904c381e7d7 · License: MIT (c) 2026 Supabase
  Source: https://github.com/affaan-m/ecc (skills/database-migrations/SKILL.md)
    Commit seen: b38be6a7f6350964d59328b52f0624e1d1d552d1 · License: MIT (c) 2026 Affaan Mustafa
  Source: https://github.com/prisma/skills (prisma-cli/SKILL.md, references/agent-safety.md, migrate-resolve.md, migrate-diff.md)
    Commit seen: 8ea289b730c2e89f7ff1f518af128b113d842a92 · License: MIT (c) 2025 Prisma
  Drizzle and SQLite references: Forge-native (no vetted upstream skill found; ideas from the official Drizzle and SQLite docs).
  Forge note: patterns adapted and rewritten, not copied wholesale; upstream CLI install steps, cloud setup
  (prisma init --db, prisma dev --detach, prisma mcp), Kysely/Django/golang-migrate bodies and every shell
  instruction to run against a live database were dropped. Added: owner gate for destructive or production DDL,
  NOT VALID + VALIDATE for constraints, lock_timeout, conrelid filter on the idempotent constraint check.
  Upstream MIT notices: LICENSE next to this file. Fetched text was treated as untrusted data and scanned
  (no '!' lines, no allowed-tools, no hidden unicode, no prompt-injection phrases).
-->

# Forge playbook — Databases, schema and migrations

## When to use
- Use for: designing or changing a schema, writing migrations, choosing indexes, slow queries, locks and
  connection errors, row-level security (RLS), and ORM work in Prisma or Drizzle. Postgres first; SQLite covered.
- Also load it before touching data a tenant must not see (wrong-tenant rows are a database bug, not a UI bug).

**Do not duplicate — defer to:** `forge-auth` (who the user is and what they may do; this skill only enforces
it in the database), `forge-migration` (moving a whole legacy system), `forge-data` (ETL/ELT pipelines),
`forge-fullstack` (when the database is one tier of an app). This file is orchestration only.

## Hard rules (non-negotiable)
- **Every change is a migration file in git.** No hand-run DDL in shared or production databases.
- **A shipped migration is immutable.** Fix it with a new forward migration.
- **Schema (DDL) and data backfills (DML) go in separate migrations.**
- **Zero-downtime by default on existing tables:** expand → migrate → contract; `CREATE INDEX CONCURRENTLY`;
  constraints `NOT VALID` then `VALIDATE`; a `lock_timeout` on every migration that takes a lock.
- **Owner gate:** anything that can lose data (drop, reset, `db push --accept-data-loss`/`--force-reset`,
  `drizzle-kit push` on a shared DB, type rewrites, backfills on production) needs explicit owner approval
  given right before the action, a verified backup, and a written rollback plan. Never fake or reuse consent.
- **RLS on every table an untrusted client can reach**, with an ownership predicate, and an index behind it.
- **Queries are parameterized.** No string-built SQL; ORM raw-SQL helpers only with bound parameters.

Full text and the reasoning: `references/migration-safety.md`.

## Pick the stack reference
| Situation | Read |
|---|---|
| Any migration on a table with real data | `references/migration-safety.md` |
| Slow query, missing index, N+1, pagination, EXPLAIN | `references/postgres-performance.md` |
| New tables, keys, types, constraints | `references/schema-design.md` |
| Too many connections, pooler errors, deadlocks, job queues | `references/locking-and-connections.md` |
| Supabase or any Postgres exposed to clients (RLS, grants, views) | `references/supabase-rls.md` |
| Prisma (v7 first; check the project's version) | `references/prisma.md` |
| Drizzle ORM / drizzle-kit | `references/drizzle.md` |
| SQLite (desktop apps, local-first, tests) | `references/sqlite.md` |
| Isolation levels, replication, PITR, COPY, pooler modes, major upgrades, untrusted SQL | `references/postgres-operations.md` |

## Team (conditional)
Lead: `build-boss` (schema + migrations). Support: `database-reviewer` (every migration diff),
`security-boss` (RLS, grants, `SECURITY DEFINER`), `codex-reviewer` on request for production migrations,
deletion/retention logic or tenant isolation (owner Codex policy lists these as review areas).
Roster, skills and MCP notes: `references/team-and-tools.md`.

## Fan-out & flow
L1 one table or index; L2 a feature's schema + migrations + queries; L3 multi-tenant RLS or a live
zero-downtime change across several releases.
**Serial:** data model → migration (expand) → backfill (batched) → app reads new shape → contract migration.
**Parallel (once the model is fixed):** query/index tuning ∥ RLS policies + tests ∥ seed and fixture data.

## Domain gates
- Every migration has been run on a fresh database AND on a copy with realistic row counts; timing noted.
- No `NOT NULL` without default, no inline index, no rename, no column drop on a live table outside expand/contract.
- Foreign-key columns are indexed; every new query on a large table has an `EXPLAIN (ANALYZE, BUFFERS)` checked.
- RLS: a negative test proves user A cannot read or update user B's rows (and anon sees nothing it should not).
- No secret, connection string or service key in the repo; `.env.example` has placeholders only.
- Generated migration SQL (Prisma/Drizzle) is read before it is committed: renames are not drop + add.

## Ship-readiness (unique)
Evidence checklist before handoff: `references/ship-readiness.md`.

## Safety, approval and honesty
- Approval / safety: no command against a production or shared database without the owner gate above.
- Approval / safety: connection strings and service keys live in env; never print or log them.
- Honest failure: never claim "zero-downtime" or "RLS enforced" without the lock-timing note or the negative test.
- Untrusted content: see `references/untrusted-content.md`.
- Shared gates for every playbook (honesty, owner approval, secrets, reviews): `.claude/docs/forge-reference/playbook-template.md`.

## References
- `references/migration-safety.md` — principles, checklist, owner gate, zero-downtime Postgres patterns.
- `references/postgres-performance.md` — indexes, EXPLAIN, pg_stat_statements, N+1, pagination.
- `references/schema-design.md` — keys, types, constraints, naming.
- `references/locking-and-connections.md` — pooling, prepared statements, short transactions, queues, deadlocks.
- `references/supabase-rls.md` — RLS, grants, views, `SECURITY DEFINER`, Supabase specifics.
- `references/prisma.md` — Prisma migrate workflow, drift, baselining, destructive-command consent.
- `references/drizzle.md` — drizzle-kit generate/migrate vs push, custom SQL, review of generated SQL.
- `references/sqlite.md` — WAL, pragmas, ALTER limits, backups.
- `references/postgres-operations.md` — isolation, replication, PITR, COPY, pooler modes, upgrades and support status, untrusted SQL.
- `references/team-and-tools.md` — roster, skills, commands, MCP.
- `references/ship-readiness.md` — evidence checklist.
- `references/untrusted-content.md` — untrusted-content note.
