---
name: add-db-table
description: >-
  Add or change a Greenhouse database table end to end: core tables in packages/db (schema with
  _columns helpers + ids prefix, domain service, provider registration, drizzle-kit generate into
  packages/db/migrations, pnpm db:migrate, db-schema.md, *.db.test.ts) or plugin tables in
  plugins/<id> (own schema, service bag, NNNN_name.sql lane file). Use for: add a table / column /
  migration / service, 新增表, 加个表, 建张表, 加字段要迁移, 写个 service. Red lines: migrate never
  push, never edit an applied migration, no repository classes or interface mirrors, types are
  inferred, core never gets plugin tables or plugin FKs.
---

# Add a database table

Source of truth: packages/db/src/AGENTS.md (rules) and packages/db/src/db-schema.md (tables, FKs, logical links); plugin lanes: EXTENDING.md "Database ownership and migrations". On conflict those files win.

## Decide first
- Core or plugin: only governance-core data (identity, conversations, runs, Files, notifications, usage, OAuth, settings…) goes in packages/db; everything else lives in plugins/<id>/ and its lane.
- Reuse first: check db-schema.md for an existing table to extend; a second table for the same job needs its reason in the relevant AGENTS.md.
- Relationships: FK with onDelete for strong ownership inside one domain; audit, usage, notification and cross-domain references stay logical (no FK), recorded in db-schema.md.
- Core never acquires an FK to a plugin table; plugin tables may reference core (users).

## Core table
1. Schema: packages/db/src/schema/<domain>.ts (update the file's table list), exported from schema/index.ts; Row type `typeof table.$inferSelect` at the bottom.
2. Columns only from schema/_columns.ts: id(), at(), day(), createdAt(), updatedAt(), json(name, fallback), jsonOrNull(), oneOf(), searchColumns().
3. Enums: `text('col', { enum: VALUES })` plus `oneOf('chk_<table>_<col>', col, VALUES)`; floats doublePrecision(); counts and money `bigint({ mode: 'number' })`.
4. Every table declares its indexes; names `idx_*`, `uq_*`, `chk_*`; never order by id (use created_at, seq, position, sort_order).
5. Ids: register a three-letter prefix in ID_PREFIX (packages/db/src/ids.ts); services write `newId(kind)`, or `stableId(kind, seed)` when the id must be recomputable.
6. Service: packages/db/src/services/<domain>.ts exporting `createXxxService(db: Db)` that returns an object literal (`const service = {...}; return service;`, no this).
7. Register it in packages/db/src/provider.ts and export input types from the package root (packages/db/src/index.ts); DatabaseProvider is inferred.
8. Generate at the repo root: `pnpm drizzle-kit generate` (drizzle.config.ts → packages/db/migrations/NNNN_*.sql plus meta snapshot).
9. Review the SQL: casts missing USING, NOT NULL without DEFAULT on populated tables, renames generated as drop + add (hand-edit to RENAME), backfills.
10. Apply: `DATABASE_URL=<your own local db> pnpm db:migrate`; never bare `drizzle-kit migrate` (the config falls back to the main DB) and never push to a persistent or shared DB.
11. Fast-growing tables get a window in RETENTION_POLICY (packages/db/src/services/retention.ts) and the db-schema.md retention section.
12. Update db-schema.md: purpose, key columns, FK table, logical links, diagram.

## Service rules
- Business code (routes, tools, CLI) never writes SQL; it calls `getDb().<domain>.<method>()`.
- Types are inferred: Row = $inferSelect, union aliases = `XxxRow['col']`, parameter types beside the service; no hand-written mirrors.
- No interface layers, repository classes or multi-backend abstractions.
- Query-builder jsonb reads are parsed, raw `db.execute(sql…)` reads are text: read both with safeJsonParse (@greenhouse/utils/json); raw writes use `${JSON.stringify(v)}::jsonb`.
- Raw COUNT/SUM/bigint results are strings: wrap in Number().
- Write timestamps with nowIso() (@greenhouse/utils/date); set updated_at explicitly on update.
- Secrets live in `_enc` columns (PROVIDER_TOKEN_ENCRYPTION_KEY); anything hashable stores only SHA-256.

## Plugin table
- Schema in plugins/<id>/api/schema.ts using the kit's column helpers (at, createdAt, id, json, oneOf, updatedAt, users from @greenhouse/api/extension-kit).
- New plugins name tables `ext_<id>_*`; official plugins keep their existing names.
- Services: a factory passed as `services:` in defineExtension and a typed accessor over getExtensionServices (plugins/memory/api/services.ts); plugin services are absent from DatabaseProvider.
- Lane: `migrations: { dir: extensionPath(import.meta.url, '../migrations') }`; files are plugins/<id>/migrations/NNNN_name.sql separated by `--> statement-breakpoint`, checksummed in extension_migrations.
- Draft SQL with the plugin's own config (`pnpm drizzle-kit generate --config plugins/<id>/drizzle.config.ts`), then keep only the reviewed delta as the next NNNN_name.sql; the lane runs every *.sql in the folder, so remove any other generated output.
- Guard DDL with IF NOT EXISTS where a 3.x database may already hold the table (see plugins/*/migrations/0001_adopt.sql).
- Never edit an applied lane file or create a core-owned table in a lane.
- Register owned tables in resetTables; retention goes in the plugin's `retention: [{ table, column, days }]`.
- Table-backed data-source creates need an id field with a database-generated key or default.
- Document the table in plugins/<id>/db-schema.md and the plugin README.

## Tests
- DB tests are `*.db.test.ts` (tests/db/ for core, plugins/<id>/api/__tests__/ for plugins); each test runs in a rolled-back transaction.
- Call initDatabase() in beforeEach, never in beforeAll or module scope; never resetSchema().
- Create members with tests/helpers/internal-user.ts; narrow one with moveToRestrictedRole() (tests/helpers/restricted-role.ts).
- Assert only rows this test created; take ids from create's return value.
- `*.db-commit.test.ts` only for cross-connection visibility, DDL or locks, with `@db-commit-reason` in the header; DDL and lifecycle fixtures use tests/helpers/isolated-db.ts.
- tests/db/schema-equivalence.db-commit.test.ts must keep passing (fresh 4.0 + all official plugins = bridged 3.x); record intended differences in INTENTIONAL_DIFFERENCES.

## Gate
```bash
pnpm typecheck
pnpm lint
TEST_DATABASE_URL=<loopback db named *test*> pnpm test:db   # focused
TEST_DATABASE_URL=<loopback db named *test*> pnpm test      # before handoff
./node_modules/.bin/drizzle-kit check                       # core journal and snapshots agree
```
Plugin lanes also run `pnpm plugins:sync --check` and `pnpm test:core` (see quality-gate).

## Red lines
- Never edit 0000_v4_baseline.sql, migrations/archive-3x/ or any applied migration bytes.
- Never push a schema to a persistent or shared database; migrations are the only source of truth.
- Never run migrations from a worktree against the main database; always set DATABASE_URL explicitly.
- No organizations table or org_id column; no columns "for later".
- Deleted features do not come back as compatibility tables.

## Checklist
- [ ] Core vs plugin decided; reuse considered and recorded
- [ ] Schema with helpers, indexes and CHECKs; prefix registered (core)
- [ ] Service factory registered (provider.ts or plugin services)
- [ ] Migration generated or written, reviewed, applied to your own DB
- [ ] Retention decided; db-schema.md (core or plugin) updated
- [ ] DB tests at the right layer; schema-equivalence green; gate green
