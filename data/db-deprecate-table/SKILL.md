---
name: db-deprecate-table
description: "Retiring a dead table by moving it to the deprecated schema and clearing every reference in both repos. Use when asked to deprecate or retire a table, when a table is no longer used, or to take a table offline without dropping it. NOT for relocating a still-used table (use db-move-table-schema)."
---

# Deprecate a table

> Once a table is here it is dead to every database check: findings on deprecated tables are never reported or fixed — [canonical-first triage](../../../../common-docs/policies/canonical-first-triage.md).

Goal: get the table **offline and reversible** (`SET SCHEMA deprecated`, never `DROP`), then erase every reference. **Getting it offline is priority #1; reference cleanup follows and must not block the move.** Read [`../db-change/TOOLKIT.md`](../db-change/TOOLKIT.md) + [`../db-change/SKILL.md`](../db-change/SKILL.md) first. Project: `brsgrqvjdzwihsvnfqkf`.

## Step 1 — Discover every reference (this is the real work)

**🚨 THE ORACLE FIRST — `audit.relation_usage(schema, table)` (built 2026-08-20, deprecated-sweep postmortem).** One call returns EVERY DB-side mention: inbound/outbound FKs, dependent views/matviews **recursively** (each dependent view joins the closure, so its consumers are found too), triggers on it, every function/procedure body (qualified vs bare matches labeled), RLS policy expressions on other tables, trigger string-arguments (`_version_capture` tokens, org-inherit args), cron jobs, realtime publications, and the entity/shareable/deprecation registries.

```sql
select * from audit.relation_usage('<schema>', '<table>') order by via, kind, ref;
```

The transitive hop is the whole point: single-hop name searches missed `deprecated.prompt_builtins` → `public.context_menu_unified_view` → `get_ssr_shell_data` (a LIVE session hydrator) in the 2026-08-20 sweep — the table name appears nowhere in the function, only the view's name does. Never substitute a plain `pg_proc ilike` scan for this call. `function_body_bare` rows can be same-named objects in another schema — read each; `function_body_qualified` rows are certain.

Two checks the oracle does not cover:

```sql
-- is anything still actually reading it? (needs pg_stat_statements)
select calls, query from pg_stat_statements where query ~* '\m<table>\M' order by calls desc limit 20;
```
Code (both repos): grep `<table>` for `.from('<table>')`, `.schema(...).from('<table>')`, generated type names, Python model/manager names (`aidream/db/models*.py`, `db/managers/**`), package wiring in `aidream/package_integration.py`, **and raw SQL strings** (`from <table>`, `SELECT 1 FROM <table>` ACL joins in `.py`/`.sql`). **Also grep for every `ref` the oracle returned** — a dependent view or RPC it surfaces can be called from code by ITS name with the table name appearing nowhere in the repo.

> **A 0-row table can still be LIVE.** Verified: `note_shares` had 0 rows but was joined by RAG-search ACL (`matrx-rag/search.py: SELECT 1 FROM public.note_shares`) — deprecating it turned an empty result into a missing-relation error, breaking search. **Row count ≠ usage.** The query string is what breaks; grep it before you move. (Recovery: `alter table deprecated.<t> set schema public` — reversible, which is why we never `DROP`.)

## Step 2 — Confirm it's truly dead
If reads remain: repoint or delete those consumers if quick; otherwise deprecate now (reversible) and **track the remaining cleanup** in the Open items queue of `../common-docs/operations/db-changeover-board.md` (the tracker that replaced the deleted `docs/db_rebuild/CHANGEOVER_PROGRESS.md`). Do not block the move on a long repoint — but never deprecate a table with live, load-bearing reads you haven't accounted for.

## Step 3 — Resolve FKs in BOTH directions

**Inbound** (tables that point AT this one): a cross-schema FK keeps working after the move, so the move won't *break* — but a dead table shouldn't be referenced. Drop or repoint inbound FK constraints that shouldn't exist. If an inbound FK represents real data you can't yet sever, that table isn't dead — reconsider.

🚨 **Outbound** (this table pointing at LIVE tables) — **the step that gets forgotten, and it breaks live pages.** `SET SCHEMA` carries every outbound FK along, so the retired table keeps advertising itself in `pg_constraint` as a child of live tables. Any catalog-walking function then discovers it and queries it **as the signed-in user**, who has no `USAGE` on `deprecated` → `42501 permission denied for schema deprecated`, and the whole call dies. That is exactly how every `/projects/<id>` page broke on 2026-08-13: `get_project_references` walked the FKs into `projects.projects` and hit two retired flashcard tables. Always finish the move with the idempotent sweep — **it is safe and expected to re-run**:
```sql
do $$ declare r record; begin
  for r in select conname, conrelid::regclass as from_table from pg_constraint
    where contype='f' and conrelid::regclass::text like 'deprecated.%'
      and confrelid::regclass::text not like 'deprecated.%'
  loop execute format('alter table %s drop constraint %I', r.from_table, r.conname); end loop;
end $$;
```
`migrations/drop_graveyard_to_live_fks.sql` is this sweep. It was run ONCE (2026-07-28) and treated as done; every table retired afterwards re-created the problem — 78 such FKs had accumulated by 2026-08-13. It is not a one-time migration, it is a **post-condition of every deprecated move**.

## Step 4 — Deactivate the registration FIRST (enforced, 2026-08-12)
`platform._enforce_entity_is_table` now ERRORs when an ACTIVE `entity_types` row ends up
pointing at `deprecated` — the DDL-sync trigger repoints `schema_name` during your `SET SCHEMA`,
so **moving a still-active registered table into deprecated fails with a check_violation.**
Deactivate before you move (this is the guard doing its job, not a bug):
```sql
update platform.entity_types set is_active=false where token='<token>';   -- or delete the row
```

## Step 5 — Move it (idempotent, verify no data lost)
```sql
do $$ begin
  if to_regclass('public.<table>') is not null then
    execute 'alter table public.<table> set schema deprecated';
  end if;
end $$;
select count(*) from deprecated.<table>;   -- equals the pre-move count
```

## Step 6 — De-register the rest
Remove the remaining platform footprint so nothing resolves to it:
```sql
delete from platform.entity_relationships where child_type='<token>' or parent_type='<token>';
delete from platform.shareable_resource_registry where table_name='<table>';
```
Leave satellite rows (`associations`/`comments`/…) keyed by the token in place unless they're now orphaned — sweep separately; they're harmless and reversible.

## Step 7 — Cross-repo cleanup + finalize
`deprecated` IS in the `db-types` schema list, so the table still appears under the `deprecated` schema in FE types — that's fine; the point is to **delete every code usage**. Then run the finalize SOP (db-change/SKILL.md): `pnpm db-types` → remove FE usages → `pnpm sync-types` (fix TS); `python db/generate.py` → remove aidream usages + `package_integration.py` entry → `python db/detect_applied.py` → `python run.py` clean boot. Record the migration in the ledger. Commit + push `main` on both repos.

## Clean cut — no silent shim (SKILL `db-change` → THE CUT)
`SET SCHEMA deprecated` makes `public.<t>` vanish → stale refs error (correct). **Register it** in `scripts/dead-relations.json` + `platform.deprecated_relations` and clear `pnpm check:dead-relations` (it finds the raw-SQL/Python/comment refs `tsc` misses). Never leave a readable old table or a compat view as a "fallback"; if it can't be moved yet, **tripwire it** (`platform.deprecate_relation` — data preserved, reads/writes RAISE).

## NEVER
- `DROP TABLE` — `SET SCHEMA deprecated` only (DROP is a separate PITR-gated step).
- Leave the old name readable as a silent fallback — move it (vanishes → errors) or tripwire it (RAISES). Never a passthrough view.
- Deprecate a table that still has live reads you haven't repointed or tracked.
- Leave a generated type / Python model / `package_integration.py` reference pointing at the moved table.
