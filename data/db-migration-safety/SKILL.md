---
name: db-migration-safety
description: >
  Audit database migration files (Alembic, Django, Drizzle) for prod-safe
  patterns. Blocks + warns on locking DDL, silent data loss, and Nimbus-specific
  cross-repo breakage.

  Trigger this skill when:
  - Edit or read any file matching `**/migrations/*.py`, `**/drizzle/**/*.sql`,
    `**/alembic/versions/*.py`.
  - User says "check this migration", "is this migration safe", or invokes
    `/db-migration-safety`.
  - Before merging a PR that includes migration files.
---

## Universal red flags

| Pattern | Severity | Reason |
|---|---|---|
| `AlterField(... null=False)` on populated column without prior backfill migration | 🔴 | Blocks table lock; may fail on existing NULLs. |
| `AddField(... null=False, default=<value>)` on large table | 🟠 | PostgreSQL 11+ handles the default without rewrite for constant defaults, but check. Django+Alembic 3-pass pattern (AddField nullable → RunPython backfill → AlterField NOT NULL) is safer. |
| `RemoveField` / `DROP COLUMN` on a column read by another service | 🔴 | Silent break at deploy time. |
| `RenameField` / `ALTER COLUMN … RENAME` | 🔴 | Same, plus ORM cache warm-up mismatch. Prefer add-new + backfill + drop-old across releases. |
| `CREATE INDEX` without `CONCURRENTLY` on a large table | 🟠 | Table locked during index build. Use `CREATE INDEX CONCURRENTLY`. |
| `ALTER TYPE` / column retype without USING clause | 🟠 | Silent truncation, PG version differences. |
| DDL + DML in same migration | 🟡 | Long transaction; rollback risk. |
| `RunSQL` with `--` comments only, no reverse | 🟡 | Irreversible without justification. |
| Deletes without `soft-delete` semantics | 🟠 | Nimbus base model has `active`/`hidden` flags; use `deactivate()` instead. |

## Nimbus repo-specific rules

### cidca-platform / `ecg_auto`

**Two lambdas in `cidca-services` bypass the ORM and read/write `ecg_auto`'s Postgres directly.** Migrations touching these tables need explicit coordination:

- **`ecg-gw-iot-lambda`** writes `iot_device` via raw SQL. Any schema change to
  `iot_device` breaks it.
- **`ecg-excel-lambda`** (Go) reads: `api_ecg`, `api_center`, `api_organization`,
  `api_patient`, `api_discounttag`. Any schema change to those tables can break
  the Go lambda silently.

Rules:
- Renaming or retyping columns in these tables → 🔴 critical. Coordinate first.
- Adding columns (nullable) → 🔵 low. Safe.
- Removing columns → 🔴 critical unless coordinated deprecation across services.
- Migration name pattern: `XXXX_<verb>_<table>_<field>.py`.

### cidca-platform / migration numbering

- Current highest: check `ecg_auto/api/migrations/max_migration.txt`.
- Bump both the file number and `max_migration.txt` in the same commit.

### zotea

**NEVER run `pnpm db:migrate` from an agent or feature branch.** Migrations apply
only from `main`, via `.github/workflows/db-migrate.yml`. Drizzle deduplicates by
hash, not by index — running from a feature branch with an incomplete journal
silently skips migrations and creates a hole in prod. Historical incident:
2026-06-08, `registrations.deleted_at does not exist` in prod.

Rules:
- Do not run `pnpm db:migrate` yourself. Ever.
- Verify `packages/db/drizzle/_journal.json` is contiguous with the migrations
  in the directory.
- New migrations must be committed BEFORE opening the PR — Drizzle deduplicates
  by content hash; renaming after merge creates a hash mismatch.

### horus-v2

- Alembic auto-generated migrations must be reviewed for reordering that changes
  intent. Alembic sometimes emits DROP+CREATE where an ALTER would work.
- TimescaleDB hypertables live in `scripts/init_timescaledb.py`, NOT in Alembic
  — don't try to alembic-manage them.

## Behavior

1. Identify migration files staged / edited.
2. Walk each file. For each red flag, emit `<file>:<line>: <severity> <pattern>: <reason>. <fix>.`
3. For cross-repo hot-spots, add a note: `⚠ touches api_ecg — coordinate with ecg-excel-lambda (cidca-services).`
4. End with a decision summary: `SAFE / RISKY / UNSAFE`.
5. If UNSAFE, propose a rewrite (split into 2-3 migrations, use CONCURRENTLY,
   add backfill step).

## Do not

- Don't run the migration to test it. Read only.
- Don't auto-fix migrations unless user says so — they're load-bearing infra.
- Don't invoke this on migrations already merged to `main` / `dev` — those are
  history. Focus on staged/PR migrations.
