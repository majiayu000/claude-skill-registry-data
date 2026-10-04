---
name: db-canonicalize-table
description: "Bringing an existing table onto the platform base standard. Use when asked to canonicalize, retrofit, or 'Wave 3' a table, run apply_rls or an org backfill, retire a bespoke *_versions table, or move it onto platform comments/associations/permissions. NOT for a schema move (use db-move-table-schema)."
---

# Canonicalize a table

> 🚨 **Never remove, narrow, supersede or suppress `platform_admin_read`** — it is our own admin database access (the admin dashboard reads every row through it). Check before and after any policy change: `../common-docs/policies/our-own-admin-database-access.md` (the query must return 0).

Make `<schema>.<table>` (token `<token>`) fully conform to the platform standard. Read [`../db-change/TOOLKIT.md`](../db-change/TOOLKIT.md) (live signatures, gotchas) + [`../db-change/SKILL.md`](../db-change/SKILL.md) first. Project: `brsgrqvjdzwihsvnfqkf`. Order matters — do the steps in sequence.

This is the ONE recipe for getting any table onto the base standard ("retrofit", "base retrofit", "Wave 3", "bring <X> onto the platform base entity"), preserving existing behavior exactly: take it all the way to certified, or stop at the transition-state floor (zero FAIL + only the legacy WARNs — see the certify bar below). Relocating a table → `db-move-table-schema`; retiring one → `db-deprecate-table`.

## 🛑 Before you write one line — obey db-change's PRIME DIRECTIVE (§top of `../db-change/SKILL.md`)

The app is DOWN until fully canonical; there is no safe half-state. So:

- **Meet EVERY canonical requirement for this table in ONE pass across ALL layers** (SQL → `db/generate.py` → Python usages → FE types → Next.js usages → both repos → commit → push). Never start a table you won't finish this pass. Never leave one layer repointed and another not — that broken middle is the whole disaster.
- **First, look at the real table AND its data** (row counts — live or test?). Then write a SHORT bullet checklist of what canonical requires here. Not a report.
- **"Behavior preserved exactly" is NOT a license to skip a canonical requirement.** If preserving today's behavior would keep a non-canonical structure, that is a conflict you RAISE, not resolve on your own.
- **🔴 NO bespoke `*_versions` table survives, and you do NOT get to keep one silently.** Canonical versioning = `history.row_versions` via the `_history` trigger + the generic `version_*` RPCs. A per-entity `*_versions` table (`code_file_versions`, `note_versions`, …) is legacy drift to RETIRE — migrate its rows into `history.row_versions`, repoint `promote_version`→`version_restore` + every reader, then deprecate it. **BUT versioning is not right for every table** — so if you think this table should keep its table, or shouldn't be versioned at all, that is a QUESTION you ask the human BEFORE starting (state your view + the fact, e.g. row count), get an explicit yes/no, and only then proceed. Leaving the old version table because *you* decided it was safer — with no ask — is the exact failure that has cost this project weeks. (Setting `is_versioned=false` to silence the gate while the bespoke table lives on is that same failure in disguise.)
- **Any other requirement you want to deviate from** (skip a drop, keep an old column, defer a repoint) → same rule: ask up front, explicit yes/no, no clear answer = stop and ask again. Decisions are made BEFORE you start, then you execute 100%.

## 📼 Retiring a bespoke `*_versions` table

The one-pass recipe (backfill → capture → repoint the legacy version RPCs → deprecated), its gotchas, and the two live CRACKS in the canonical version system. **Entity carries a per-entity `*_versions` table (or the Prime Directive versioning question above was answered "retire it") → read [retire-versions-table.md](retire-versions-table.md) before Step 5.**

## ⚡ Field realities — read these first, they each cost a round-trip (verified 2026-07-05)

0. **This is where a DB-wide finding on an uncertified table should land.** Under
   [canonical-first triage](../../../../common-docs/policies/canonical-first-triage.md), a problem that
   appears only on uncertified tables is fixed by converting the table here — never by patching the old shape.

1. **A table is usually FAR more canonical than "not started."** A prior "canonicalize + move" migration often already added `created_by`/`visibility`/`deleted_at` + canonical RLS + `_stamp_actor`/`_touch_row`, and left only: the **kill-list columns** (`user_id`/`is_public`/`is_deleted`) undropped + the **base FK constraints** missing. **Run `iam.verify_canonical(s,t,tok)` for EVERY involved table BEFORE writing anything** — it prints the exact remaining gap. Don't assume; the delta is often tiny.
   - **The gate keys on the TOKEN, never the table name — and the token is often singular while the table is plural** (`code_file` ⟷ `code_files`, `code_folder` ⟷ `code_file_folders`). Passing the table name as the token yields a signature TRIO of FALSE fails — `entity_registered` ("no entity_types row for token=…"), `policy_uses_has_access` ("std_select does not call has_access('…')"), `sharing_token` ("registry resource_type=… != token=…"). If you see exactly those three, you passed the wrong token — get it from `platform.entity_types`/`audit.summary`, not by pluralizing the table name. (The admin verify UI now warns on this mismatch.)
2. **`canonical_certify` reads a CACHED snapshot — `audit.refresh()` is MANDATORY before it's truthful.** After you `CREATE OR REPLACE` a broken dependent function or fix anything, `canonical_certify_ok` KEEPS reporting the old `broken_dependent_fn`/finding until you `SELECT audit.refresh();`. A "still broken" you already fixed is the #1 false failure — refresh, then re-check.
3. **A broken dependent function blocks certify even when its breakage is unrelated to your table.** (`promote_version` referenced a deprecated `note_versions` and blocked `code_file` certify.) Fixing it — e.g. neutralizing a dead branch that points at a retired table — is part of "done." Find them with `audit.table_impact(s,t)` (`currently_broken=true`).
4. **Components (`is_component=true`) still need `organization_id` + `version` + `_touch_row` + the base FKs.** The gate FAILs `base_organization_id`/`base_version`/`trg_touch_row`/`base_*_fk` on components too. TWO traps: (a) the moment you ADD `organization_id` to a component, `base_org_not_null` flips SKIP→FAIL (column now exists, nullable) → `SET NOT NULL` after backfilling from the parent; (b) a `soft_delete` WARN blocks `certify` → add `deleted_at` + `UPDATE entity_types SET has_soft_delete=true`.
5. **`is_versioned=true` with no `_history` trigger is now a hard `trg_version_capture` FAIL.** If the table versions via a bespoke `*_versions` table (or doesn't version at all), the honest, behavior-preserving fix is `UPDATE platform.entity_types SET is_versioned=false` — it makes the check SKIP without adding redundant double-capture. Only attach `_history` if you genuinely want it on `history.row_versions`.
6. **`organization_id NOT NULL` and every write names its organization — no trigger fills one.** `public._stamp_org_default` no longer exists (verified live 2026-09-26) and must not come back: a database trigger choosing an organization is the substitution `CLAUDE.md` forbids (`common-docs/systems/architecture/database/projects/no-db-assigned-org/PLAN.md`). An org-forgetting write fails loudly with 23502 at the caller — that is correct.
7. **Service-role (Python) inserts MUST set `created_by` explicitly** — `_stamp_actor` can't fill it without `auth.uid()`/`app.user_id`. A supabase-py service-client insert that dropped `user_id` must now pass `created_by=<owner>` and `organization_id=<owning org>` explicitly. (A JWT/RLS-authed FE write is stamped automatically — drop the owner column there.)
8. **Dropping a column/table is a clean cut, and finding MORE consumers than you expected is NORMAL — grind through them, NEVER revert.** Before you drop, run the full **Consumer discovery protocol** (`../db-change/SKILL.md` §🔎): grep the name in EVERY format (`snake` · `Pascal` · `camel` · plural · manager-instance), open every hit **including lazy/mid-file imports and generated hubs** (`package_db_wiring.py`, `auto_config*.py`, `db_requirements.py` manifests, `database.types.ts`), and fix **raw-SQL strings + `getattr(row,"field",default)`** (the silent-column trap) — `tsc`/`db/generate.py`/`dead-relations` are the LAST-step backstop, not the search. When the blast radius turns out bigger than "this table is fairly new" implied (a second feature module, a whole router, a manifest), that is the migration working — repoint it, do not re-add the table (that panic-revert cost hours on skill.project/resource). The only stop is a genuine human decision (Prime Directive rule 4), flagged with the drop still in place.

## Step 0 — Classify the variant and the level

**The level first** — `platform.entity_types.data_class`, by the law `common-docs/policies/access-ladder.md`: every table starts at `organization` (canonical examples: Agent, Sales deal); `public` only when it is meant to be seen outside the organization without being shared; `confidential` / `private` only with Arman's approval. A component carries no level of its own — it has its parent's. The variant below is the RLS shape, not the level.

- **entity** — independent business object (its own owner/visibility). Most tables.
- **component** — child whose access IS its parent's, full depth (versions, events, line-items). RLS defers to a `composition` parent; no own visibility.
- **ledger** — append-only org-scoped log. No user writes, no version/soft-delete.
- **restricted** — secret-bearing system tables (AI vendor config — `ai.endpoint`/`ai.api`/`ai.offering`). `std_select` = owner OR super-admin **only** — deliberately **no** `iam.has_access` path, because `has_access` would leak viewer access through the global-readable system org.
- **system** — catalog/shared-definition tables. **Requires a `visibility` column.** `std_select` = public-visibility OR owner OR `has_access`.
Check existing columns/policies/triggers first: `\d`-style via `information_schema.columns`, `pg_policy`, `pg_trigger` (see TOOLKIT.md §5–6).

## Step 1 — Base columns (additive, idempotent)
**`public.*` table → use the driver** (adds org/created_by/updated_by/updated_at/version, backfills, attaches `_touch_row`+`_stamp_actor`):
```sql
select platform.retrofit_entity('<table>','<token>',
  '<personal|parent|keep>', '<owner_col>',           -- e.g. 'personal','user_id'
  '<parent_table_or_null>','<parent_fk_or_null>',     -- for 'parent' strategy
  '<legacy_updated_at_trigger_or_null>');             -- dropped so backfill doesn't bump updated_at
```
**Ordering (verified):** `retrofit_entity` backfills created_by + org *before* attaching the triggers, so its backfills don't churn `version`/`updated_at`. The `visibility`/`deleted_at` columns it does NOT add — so add `visibility` and run the `is_public→visibility` / `is_deleted→deleted_at` normalization **before** calling `retrofit_entity` (triggers not yet attached). Doing them after leaves freshly-migrated rows at `version=2` with `updated_at=now()` (looks edited when it was only migrated).
**Schema-homed table (NOT public) → retrofit_entity does NOT work; hand-roll:**
```sql
alter table <schema>.<table> add column if not exists organization_id uuid;
alter table <schema>.<table> add column if not exists created_by uuid;       -- if a non-uuid created_by exists, rename it to created_by_kind first
alter table <schema>.<table> add column if not exists updated_by uuid;
alter table <schema>.<table> add column if not exists updated_at timestamptz not null default now();
alter table <schema>.<table> add column if not exists version int not null default 1;
alter table <schema>.<table> add column if not exists deleted_at timestamptz;
alter table <schema>.<table> add column if not exists metadata jsonb not null default '{}';
alter table <schema>.<table> add column if not exists visibility platform.visibility not null default '<TIER>';  -- entity/shareable only
-- <TIER> is a DECISION, never a reflex (db-rules §6a): 'personal' ONLY for an individual
-- person's own artifacts (chats, DMs — almost nothing qualifies); org work product → 'internal';
-- scraped/derived/catalog content → 'public'. Defaulting to the lowest tier without a
-- personal-artifact justification is the documented anti-pattern that locked out whole orgs.
-- normalize legacy → canonical (guard each on IS NULL so re-runs are no-ops)
update <schema>.<table> set created_by = coalesce(created_by, <owner_col>) where created_by is null;
update <schema>.<table> set visibility = 'public' where <is_public_col> is true and visibility <> 'public';
update <schema>.<table> set deleted_at = <deleted_ts_or_now> where <is_deleted_col> is true and deleted_at is null;
-- backfill org: copy it from the parent, or name the owning organization explicitly per row set.
-- Never pick one from the is_personal flag (being deleted — organizations are equal, access-ladder law).
-- drop legacy updated_at trigger, attach the shared triggers
drop trigger if exists <legacy_updated_at_trigger> on <schema>.<table>;
drop trigger if exists _touch_row on <schema>.<table>;
drop trigger if exists _stamp_actor on <schema>.<table>;
create trigger _touch_row  before insert or update on <schema>.<table> for each row execute function platform._touch_row();
create trigger _stamp_actor before insert or update on <schema>.<table> for each row execute function platform._stamp_actor();
```
Verify **0 null org** and **0 null created_by** (where an owner existed) before continuing. Backend-written tables: ensure the engine writes `created_by` (service role doesn't stamp it — TOOLKIT.md §5).

## Step 1.5 — Base FK constraints + `organization_id NOT NULL` (REQUIRED — nothing else adds these)
**`retrofit_entity` adds the *columns* but NOT the FK constraints or the NOT-NULL, and the gate checks all four.** Skip this and `verify_canonical` returns four hard FAILs — `base_org_fk`, `base_created_by_fk`, `base_updated_by_fk`, `base_org_not_null` (verified live 2026-07-05). Run **after** org is backfilled to 0 nulls:
```sql
alter table <schema>.<table> alter column organization_id set not null;
alter table <schema>.<table> add constraint <table>_org_fk foreign key (organization_id) references iam.organizations(id);
alter table <schema>.<table> add constraint <table>_created_by_fk foreign key (created_by) references auth.users(id);
alter table <schema>.<table> add constraint <table>_updated_by_fk foreign key (updated_by) references auth.users(id);
```
Idempotent guard for re-runs: wrap each in `do $$ begin if not exists (select 1 from pg_constraint where conname='<table>_org_fk') then … end if; end $$;` or check `information_schema.table_constraints` first. `SET NOT NULL` fails if ANY org is null — fix Step 1's backfill, never weaken this. (FK targets: `organization_id → iam.organizations(id)`, `created_by`/`updated_by → auth.users(id)` — these exact targets are what the gate matches.)

**Safety assert (put it at the end of the Steps 1–1.5 migration so the whole thing rolls back on any miss):**
```sql
do $$ begin
  if exists (select 1 from <schema>.<table> where organization_id is null) then raise exception 'null organization_id remains'; end if;
  if not exists (select 1 from pg_trigger where tgrelid='<schema>.<table>'::regclass and tgname='_touch_row') then raise exception '_touch_row not attached'; end if;
  if not exists (select 1 from pg_trigger where tgrelid='<schema>.<table>'::regclass and tgname='_stamp_actor') then raise exception '_stamp_actor not attached'; end if;
end $$;
```

## Step 2 — Register the entity (idempotent)
```sql
insert into platform.entity_types (token, schema_name, table_name, label, default_visibility, is_component, is_versioned, is_active)
select '<token>','<schema>','<table>','<Label>','<TIER>', <is_component:false|true>, <is_versioned:true|false>, true  -- <TIER>: same decision as Step 1 (db-rules §6a)
where not exists (select 1 from platform.entity_types where token='<token>');
```
If **component**, add the composition edge (required before `apply_rls`):
```sql
insert into platform.entity_relationships (child_type, parent_type, fk_column, kind)
select '<token>','<parent_token>','<fk_col>','composition'
where not exists (select 1 from platform.entity_relationships where child_type='<token>' and kind='composition');
```
(Optional `kind='containment'` edges add read-cascade for `visibility>=internal` — additive.)

## Step 3 — Sharing registry (entity is user-shareable)
The registry lives in **`platform.shareable_resource_registry`** — it moved out of `public` in the 2026 reorg (verified live 2026-07-05; a `public.` insert errors with table-not-found).
```sql
insert into platform.shareable_resource_registry
  (resource_type, schema_name, table_name, id_column, owner_column, is_public_column, display_label, url_path_template, rls_uses_has_permission)
values ('<token>','<schema>','<table>','id','created_by','visibility','<Label>','/<path>/{id}',true);
```
`resource_type` MUST equal `<token>` (mismatch → grants silently ignored).

## Step 4 — Canonical RLS (the only policy authority)
Inventory existing policies first (`apply_rls` **drops them all**); fold anything load-bearing into the standard model. Then:
```sql
select iam.apply_rls('<schema>','<table>','<token>','<entity|component|ledger|restricted|system>');
```
(`entity` requires created_by + organization_id present; `component` requires the composition edge; `restricted` is owner-or-super-admin-only with no `has_access` path (secret-bearing system tables); `system` requires a `visibility` column (catalog/shared-definition tables) — see Step 0. There is **no `join` variant** — TOOLKIT.md §2. A pure M2M **join table** (`a_id`+`b_id`, no lifecycle) is best collapsed into `platform.associations` (db-rules §3); if it must stay a table, policy it as `component` (composition edge) or hand-write org-gated policies like `platform.associations` — never invent a `join` variant.)

## Step 5 — Versioning
- **Table already versions** (history/audit today) → put it on the central system: attach the capture trigger.
- **Table does NOT version today** → **ASK the PM (the user) whether to add versioning** at canonicalization. Do not silently add or skip.
```sql
-- when versioned: set is_versioned=true in entity_types AND attach the trigger (registration alone captures nothing)
create trigger _history after insert or update or delete on <schema>.<table>
for each row execute function platform._version_capture('<token>');
```
Confirm the current month's `history.row_versions` partition exists (capture starts only when `_history` is attached — pre-existing rows are NOT auto-backfilled). **Backfilling old versions** (retiring a per-feature `*_versions` table): `history.row_versions` is **monthly RANGE-partitioned**, so first pre-create a partition for EVERY month in the source's date range (`min(created_at)..max`) or the INSERT fails with a no-partition error (verified — `note_versions` spanned 7 months, only 2 partitions existed). Map `row_id`/`version`/`occurred_at`/`actor_id`; stash extra fields under reserved `_*` keys in `row_data`; verify `count(history)=count(source)`. (Optional `_gc` → `platform._gc_entity_associations('<token>')` cleans association edges on delete.)

## Step 6 — Replace the feature's bespoke subsystems with the platform satellites
If the feature has its OWN comments / associations-relationships / categories / activity-log / favorites-pins, **migrate the rows into the platform tables keyed by `(entity_type='<token>', entity_id)`** and deprecate the old tables (use `db-deprecate-table`). Behavior must be identical afterward — verify the UI shows the same comments/tags/relationships. (`platform.comments`, `platform.associations`, `platform.categories`, `platform.activity_log`, `platform.user_entity_state` — shapes in TOOLKIT.md §1.) Permissions/shares → migrate into `iam.permissions` (moved from `public` in the reorg; TOOLKIT.md §3).

## Step 6.5 — Drop the legacy columns (reach zero-WARN)
In downtime, once consumers are repointed, drop `user_id`/`owner_id`, `is_public`, `is_deleted`, `shared_with` to clear the legacy WARNs. **Each drop has couplings — check first (all bit us on `notes`):**
- **Backfill with triggers OFF:** wrap the `is_deleted→deleted_at` / `is_public→visibility` UPDATE in `alter table … disable trigger user; … ; enable trigger user;`, else `_touch_row` churns `version`/`updated_at` and the version/sync/ingest triggers fire on every touched row.
- **Functions/triggers that read the column (the silent killers) — use `audit.table_impact` first, then a text scan:** `select * from audit.table_impact('<schema>','<table>');` returns every dependent function with `dependency` (precise|text), `currently_broken`, and the exact `referenced_columns[]` it touches — the blast radius, purpose-built for this. THEN belt-and-suspenders with a raw scan of ALL functions (`prokind in ('f','p')` to skip aggregates) for BOTH `(from|join|update)\s+<table>` AND `new\.<col>`/`old\.<col>`, because a `FROM/JOIN` scan MISSES trigger functions that read `NEW.<col>` (notify/ingest/sync/version triggers) and **SECURITY DEFINER functions aren't caught by `tsc`**. Verified casualties of skipping this: `_notify_auto_ingest_note` (`NEW.is_deleted` → every note write failed silently) and `get_user_dashboard_metrics` (`is_deleted` → dashboard broke). Patch each to the canonical column **before** dropping.
- **RLS on OTHER tables:** a child policy may reference this column via subquery (`… WHERE notes.user_id = auth.uid()`). `DROP COLUMN` fails `2BP01` and lists them — repoint each to `created_by`; **never blind-`CASCADE`** (it silently drops the policy).
- **Indexes:** `DROP COLUMN` auto-drops indexes that include it. Recreate the useful composites on `created_by` (owner/sync/folder lookups) first.
- **Prove safe first:** `count(*) filter (where created_by is distinct from <owner_col>)=0`, `is_public`/`shared_with` empty — then the drop loses nothing.

## Step 7 — Verify (the two-gate acceptance)
There are **two** gates and you must clear BOTH. `verify_canonical` checks the table's own structure; `canonical_certify` also checks that no dependent function is broken — **it is the "done" gate per db-rules FEATURE.md §11 (nothing is done until `canonical_certify_ok` is `true`).**
```sql
select * from iam.verify_canonical('<schema>','<table>','<token>');    -- read EVERY row
select iam.verify_canonical_ok('<schema>','<table>','<token>');         -- gate 1: no structural FAIL
select * from iam.canonical_certify('<schema>','<table>','<token>');    -- blocking rows = FAIL/WARN + any broken dependent fn
select iam.canonical_certify_ok('<schema>','<table>','<token>');        -- gate 2 (THE done gate): true = done
```
**Bar (verified live 2026-07-05):** these must all reach PASS — `base_org_not_null`, `base_org_fk`, `base_created_by_fk`, `base_updated_by_fk` (Step 1.5), `col_visibility`, `soft_delete`, `timestamps`, plus the registration/RLS/policy checks. **Skip Step 1.5 and you get four `base_*_fk`/`not_null` FAILs.** The three legacy WARNs — **`legacy_owner_col`** (`user_id`/`owner_id`), **`legacy_is_public`**, **`legacy_is_deleted`** — clear only when those columns are dropped (Step 6.5). **Full canonical = both gates `true` with zero FAIL + zero WARN**, achievable in one pass when you do the drops (proven live on a probe + on `notes`+`note_folders`); if the drops must wait, the transition-state floor is zero FAIL + only those legacy WARNs. Don't report "canonical" with any FAIL or a `col_visibility`/`soft_delete` WARN showing, or with `canonical_certify_ok=false`.

Refresh the audit store so the table shows up certified in the platform-wide hit list (drives `audit.summary`; loud + non-blocking in `release.sh`):
```sql
select audit.refresh();                                                 -- rebuilds all snapshots (heavy; runs plpgsql_check over every fn)
select fails, warns, certified from audit.summary where token='<token>';
```
Then impersonate a normal user and confirm they still read their own rows (RLS didn't hide data):
```sql
select set_config('request.jwt.claims', json_build_object('sub','<a real user uuid>')::text, true);
select count(*) from <schema>.<table>;   -- expect their visible rows, not 0
```

## Step 8 — Cross-repo finalize + document
db-change SOP: `pnpm db-types` → update all usages (new columns, `.schema()` if needed, RPC names) → `pnpm sync-types` (fix TS); `python db/generate.py` → update usages + `package_integration.py` → `python db/detect_applied.py` → `python run.py` clean boot. Ledger the migration. Update the feature's `FEATURE.md` + add a line to the Done log in `../common-docs/operations/db-changeover-board.md`. Commit + push `main` on both repos.

## NEVER
- `apply_rls` before org is backfilled (0 nulls) or before `entity_types` (+ composition edge for components) exists.
- Skip Step 1.5 — `retrofit_entity` adds the base *columns* but NOT the FK constraints or `organization_id NOT NULL`; without them the table carries four permanent `base_*` FAILs no matter how clean it looks.
- Trust `verify_canonical_ok` alone — WARNs are unfinished canonicalization, and it does NOT check dependent functions. `iam.canonical_certify_ok=true` is the only "done" signal (db-rules FEATURE.md §11).
- Assume `is_versioned=true` captures history — it doesn't without the `_history` trigger.
- Leave the feature reading its old comments/associations table after migrating the rows — repoint the code, then deprecate the table.
- Change behavior. Canonicalization preserves what the user sees; if anything differs, it's a bug.
- Touch **out-of-scope litter** as if it were legacy tagging: `sch_*` (scheduler), `wf_*`/`workflow`, `code_*`, `wc_*` — their `project_id`/`task_id` columns are real FKs, NOT association litter to migrate. Leave them.
