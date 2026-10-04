---
name: db-move-table-schema
description: "Relocating a live, still-used table to another Postgres schema with every reference intact. Use when asked to move or rehome a table into a schema, or to pull a table out of public into a domain schema. NOT for retiring a table (use db-deprecate-table)."
---

# Move a table to a new schema

> Moving an uncertified `public` table into its feature schema is the useful response to a database finding on it — not patching the finding in place: [canonical-first triage](../../../../common-docs/policies/canonical-first-triage.md).

Relocate `public.<table>` → `<new>.<table>` with references intact. Postgres moves most things for you; the misses are predictable. Read [`../db-change/TOOLKIT.md`](../db-change/TOOLKIT.md) + [`../db-change/SKILL.md`](../db-change/SKILL.md) first. Project: `brsgrqvjdzwihsvnfqkf`. Retiring a dead table → `db-deprecate-table`; bringing a table onto the platform standard → `db-canonicalize-table`.

## What `ALTER TABLE … SET SCHEMA` carries automatically
The table's columns, PK, indexes, CHECK/UNIQUE/FK constraints (its own **and** inbound FK constraints — cross-schema FKs keep working), **RLS policies, triggers, and owned sequences** all follow. You do **not** re-create these.

**What does NOT follow:** schema-level **`USAGE`** and the schema's default privileges — these belong to the *schema*, not the table. The moved table's grants come along but are **dead without schema USAGE**: every `authenticated`/`anon` access throws `permission denied for schema <new>`, which wrapper RPCs swallow into a **silent null** (the `cx_canvas_upsert returned null` class). Step 2 grants it; Step 3 verifies it.

## What you MUST update by hand
1. **Registry rows** — `platform.entity_types.schema_name` and `platform.shareable_resource_registry.schema_name` for this token.
2. **Hardcoded `public.<table>` references** in functions/RPCs and views (unqualified refs follow `search_path`; schema-qualified ones break). Find them, `CREATE OR REPLACE` repointed.
3. **FE access = TWO separate doors.** (a) **PostgREST exposure + FE types** — the target schema must be exposed to PostgREST and added to the `pnpm db-types` `--schema` list (TOOLKIT.md §0 trap), else the FE loses types and 404s. (b) **Schema `USAGE` grant** (Step 2) — `SET SCHEMA` does not grant it. A schema can be **exposed yet USAGE-denied**, which surfaces as a *silent null*, not a 404. Both are required. supabase-js calls change from `.from('<table>')` to `.schema('<new>').from('<table>')`.
4. **aidream ORM** — the target schema must be in `db/matrx_orm.yaml` `additional_schemas` with a generate block; the model regenerates into that schema's `models_<schema>.py`. If a sub-package consumes the table, update `aidream/package_integration.py`.

## Step 1 — Pre-flight discovery
```sql
-- functions & views referencing the qualified name
select n.nspname, p.proname from pg_proc p join pg_namespace n on n.oid=p.pronamespace
where pg_get_functiondef(p.oid) ilike '%public.<table>%' or pg_get_functiondef(p.oid) ilike '%<table>%';
select schemaname, viewname from pg_views where definition ilike '%<table>%';
-- inbound FKs (will keep working, but note them)
select conrelid::regclass as referencing, conname from pg_constraint where confrelid='public.<table>'::regclass and contype='f';
-- current policies/triggers (confirm they follow after the move)
select polname from pg_policy where polrelid='public.<table>'::regclass;
select tgname from pg_trigger where tgrelid='public.<table>'::regclass and not tgisinternal;
```
Grep both repos for `<table>` usages (FE `.from`, Python models/managers, package wiring).

## Step 2 — Ensure the target schema is ready (the EXPOSURE BLOCKER)
`create schema if not exists <new>;` then — **always, even if the schema already existed** (this is the step that gets skipped when the schema is pre-existing, and it's what broke canvas/code/legal/scraper) — `GRANT USAGE ON SCHEMA <new> TO authenticated, anon, service_role;` plus `ALTER DEFAULT PRIVILEGES IN SCHEMA <new> GRANT … TO …` for future tables · add it to the `db-types` `--schema` list · add to aidream `matrx_orm.yaml`.
> ⛔ **You CANNOT expose a new schema via the MCP.** Supabase's PostgREST exposed-schema list is **platform config**, not a role GUC (verified: nothing on `authenticator.rolconfig`), so no SQL you can run reaches it — not `pnpm db:apply`, not a read through the database tool. It must be added via the **dashboard (Settings → API → Exposed schemas)** or the **management API** (`PATCH /v1/projects/{ref}/postgrest`, preserving the existing list). **A FE-read table moved into an unexposed schema 404s for every user the instant it moves.** So: get the schema exposed FIRST (ask the user / use the mgmt API), confirm, *then* move. Don't blind-`ALTER ROLE authenticator SET pgrst.db_schemas` — you don't know the full current list and will silently un-expose other schemas.

## Step 3 — Move + verify it followed
```sql
alter table public.<table> set schema <new>;
select count(*) from <new>.<table>;                                    -- unchanged
select polname from pg_policy where polrelid='<new>.<table>'::regclass; -- policies followed
select tgname  from pg_trigger where tgrelid='<new>.<table>'::regclass and not tgisinternal; -- triggers followed
select has_schema_privilege('authenticated','<new>','USAGE'),
       has_schema_privilege('anon','<new>','USAGE');                   -- MUST be true (Step 2); SET SCHEMA does NOT grant it
```
Repo-wide audit for this whole class — any schema with table grants but no USAGE (run after every move):
```sql
select n.nspname,
  count(*) filter (where has_table_privilege('authenticated', format('%I.%I',n.nspname,c.relname),'SELECT')) as granted_tables,
  has_schema_privilege('authenticated',n.nspname,'USAGE') as usage
from pg_namespace n join pg_class c on c.relnamespace=n.oid and c.relkind in ('r','p','v','m')
where n.nspname not like 'pg_%' and n.nspname<>'information_schema'
group by n.nspname
having not has_schema_privilege('authenticated',n.nspname,'USAGE')
   and count(*) filter (where has_table_privilege('authenticated', format('%I.%I',n.nspname,c.relname),'SELECT'))>0;
-- expected leftovers: cron, deprecated (internal/retired — correctly NO usage). Anything else FE-facing = bug.
```

## Step 4 — Repoint the misses
Update the registry `schema_name` rows; `CREATE OR REPLACE` any function/view that named `public.<table>`; re-verify those RPCs run.

## Step 5 — Cross-repo finalize
db-change SOP: `pnpm db-types` (schema added) → swap `.from('<table>')` → `.schema('<new>').from('<table>')` everywhere → `pnpm sync-types` (fix TS). aidream: `python db/generate.py` → update imports to the new model module + `package_integration.py` → `python db/detect_applied.py` → `python run.py` clean boot. Ledger the migration. Commit + push `main` on both repos.

## Clean cut — no silent shim (SKILL `db-change` → THE CUT)
The move makes `public.<t>` vanish, so every stale ref **errors** — that's correct and desired; do NOT soften it. **Register the move FIRST** in `scripts/dead-relations.json` + `platform.deprecated_relations`, then repoint using `pnpm check:dead-relations` as your checklist until it's green (it catches the raw-SQL/comment/Python refs `tsc` can't). If a table genuinely can't move in the window, **tripwire it** (`platform.deprecate_relation`), never a passthrough view.

## NEVER
- **Leave a compat VIEW at the old `public.<t>` name** (the silent shim — the #1 disaster: reads/writes split silently across two tables). The old name must error or tripwire-RAISE, never pass through.
- Move a FE-read table into a schema that isn't exposed + in the `db-types` list (silent 404s), **or that lacks schema `USAGE` for `authenticated`/`anon`** (silent null — `SET SCHEMA` does not grant it).
- Forget the registry `schema_name` rows — `verify_canonical`/`has_access` resolve schema from `entity_types`, so a stale `schema_name` breaks RLS resolution.
- Recreate policies/triggers/constraints by hand — they moved with the table; recreating them risks drift.
