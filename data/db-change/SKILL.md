---
name: db-change
description: "Entry point and shared rules for structural changes to the live Matrx database. Use before any DDL: dropping, merging, or renaming a table, changing a function, RPC, trigger, or policy, hunting straggler tables, or starting a deprecated, schema move, or canonicalization (it routes to those skills)."
---

# DB Change — the transition SOP (read first)

> 🚨 **Never remove, narrow, supersede or suppress `platform_admin_read`** — it is our own admin database access (the admin dashboard reads every row through it). Check before and after any policy change: `../common-docs/policies/our-own-admin-database-access.md` (the query must return 0).

## ⚠️ FIRST: is anyone USING the system right now?

**This SOP is written for a scheduled outage** ("the app is ALREADY DOWN"). That assumption is
load-bearing for everything below it — especially rule 5's "no compat views, the old name must
VANISH." **Ask before you start: is the app live, and could a human be mid-session?**

- **Down / no traffic → follow this SOP exactly as written.** Cut clean, no safety nets.
- **LIVE traffic → rule 5 does NOT apply to a rename, and this is not a judgment call.** The old
  name keeps working until the new code is deployed (rename + `CREATE VIEW <old> AS SELECT * FROM
  <new>`, drop the alias once the running SHA carries the new code — or invert the order and
  rename last). See `common-docs/policies/database-changeover-doctrine.md` §8a-2.

**Why this block exists (2026-08-17):** a live rename of `platform.expertise_pack` →
`platform.rulebook` landed while production still ran the old code. The DDL→deploy gap is tens of
minutes, and Arman was inside it dictating expertise. Every tool call died on `42P01`; **11
finished expert rules were lost** and were recoverable only by reading raw tool-call traces out of
the database. A `42P01` is invisible to the human it happens to — the agent above it reports
success in prose. Nothing in this file told that agent to wait, because this file assumes the
lights are off.

## Is this change fixing something broken? If not, it waits.

A wanted change that nothing is failing on — a redundant column, a dead enum value, a name that
lies — is **not applied when noticed.** It goes on the cross-repo
[DB change queue](../../../../common-docs/operations/db-change-queue.md) with its consumer
census, and one session applies the batch end-to-end in a window (Arman, 2026-09-10). Every
change pays the full multi-layer sweep below; batching pays it once.

**Came here from a DB-wide check?** Triage the finding by table first —
[canonical-first triage](../../../../common-docs/policies/canonical-first-triage.md): deprecated is
dead, public is a queue, and a problem that shows only on uncertified tables (while certified ones
are clean) is not a fix — the work is canonicalizing that table (`db-canonicalize-table`).

## 🛑 THE PRIME DIRECTIVE — read this before you touch anything, or you will hurt the project

**This migration is past the point of no return. The app is ALREADY DOWN and stays down until the system is 100% canonical.** There is no safe partial state, nothing to protect, and no going back — the only exit is *forward, completely*. Everything below exists because agents keep half-doing the job and leaving the app in the broken middle. Do not be one of them.

1. **The canonical list is the spec and the authority — not your judgment.** There is a defined target state (the roadmap: where each table starts, its new schema, its new columns, `user_id`→`created_by`, org handling, M2M→associations, where versioning goes). You do not get to decide a canonical requirement is optional, "nice to keep for now," or "better my way." You meet the requirements.

2. **ONE change lands in EVERY layer, in ONE pass — SQL + generated Python + Python usages + Next.js types + Next.js usages + every repo — TOGETHER, before the lights come back on.** If a name changes *everywhere at once*, turning the app on is as if it never changed — clean. If it changes in one layer and not the others, the app is **broken**. **Touching one layer but not all of them ("the circle") is the single thing that has kept this app down for weeks. It is the cardinal sin.** Touch nothing, or touch it ALL — never in between.

3. **Decide EVERYTHING before you start. Never begin a table you will not finish 100% this pass.** Sequence: (a) read the canonical list, (b) look at the ACTUAL table — schema, columns, triggers, dependents, **and the real data (row counts; is it live or just test rows?)**, (c) write a SHORT bullet checklist of every requirement to reach canonical (not a report — a checklist). Then execute the entire checklist without stopping. Starting with open decisions, or starting and silently skipping a requirement, is forbidden.

4. **A canonical requirement that seems wrong for this table is a QUESTION FOR THE HUMAN, made BEFORE you start — never a call you make alone and never a thing you skip quietly.** Not every rule fits every table (versioning, for one, is not right for every table). When you think a requirement shouldn't apply, or you're tempted to keep an old structure: **STATE your opinion out loud, give the fact behind it, and ASK.** *"code_file has a bespoke `code_file_versions` table (20 rows, all test) — canonicalize it onto `history.row_versions`, or drop versioning for this table entirely? I lean X because Y."* **Yes → do it that way. No → follow the rule. No clear/blocking answer → STOP and ask again; do not start.** Your opinion is *wanted* — the human almost always has a fact you don't (that's how a weak "keep it just in case" flips to "those are throwaway rows, kill it"). Keeping the opinion to yourself and acting on the assumption is the exact move that destroys the codebase.

5. **NO safety nets. NO "just in case." NO leaving the old way.** No compat views, no leftover legacy tables "for now," no old columns kept beside new ones, no dormant fallbacks, no "I'll migrate it later." The old name/column/table must VANISH so a stale reference errors loudly and gets fixed this pass. A safety net here is not safety — it silently splits data across two shapes and *is* the bug. **The ONE exception is the live-traffic rename alias in the block at the top of this file** — a deliberately temporary view, dropped the moment the new code is deployed, which is the opposite of "leaving the old way."

6. **SHIP IT — committing and pushing IS the job, not a decision to agonize over.** During a scheduled outage the win condition is: fully canonical + all layers repointed + committed + pushed + lights on. Do not pause to ask "is it OK to release?" — the app is down; the *only* way to lose is to sit on finished work. Commit, push, deploy, in the same pass.

7. **DISCOVERING MORE THAN YOU EXPECTED IS NORMAL — FINISH, NEVER REVERT.** Halfway through you WILL find consumers you didn't know about: a second parallel feature module, a generated wiring hub, a raw-SQL string, a lazy import buried in a function. That is not a signal that "this was a mistake, undo it." It is the migration working — you found a consumer, now repoint it. **Re-adding a dropped table / un-deprecating / reverting a rename to escape a bigger-than-expected blast radius is THE cardinal panic-failure** (it happened on skill.project/skill.resource: the drop was correct, the revert was cowardice, and it cost hours). The moment you're tempted to revert, do the opposite: run the discovery protocol below, list every remaining consumer, and grind through them. The ONLY thing that ever stops you is a genuine human decision (rule 4) — and that is a loud flag with the drop still in place, never a silent revert. "Broken for five minutes while every layer changes" is the migration; a revert is the failure.

**One-line test before you stop:** *If the lights came on right now, would every layer agree and the app work?* If no, you are not done — and you do not stop, hand off, revert, or "leave it for the next pass." You finish.

---

## 🔎 Consumer discovery — find EVERY usage BEFORE you cut (this is where agents keep failing)

A dropped/renamed table or field breaks silently in the places the compiler can't see. **`type-check` / `tsc` / `db/generate.py` are a backstop, NOT the search** — they miss raw-SQL strings, `getattr(row,"field",default)` (returns the default forever — a *silent* wrong value), dynamic `.from("<str>")`, and anything in a generated file that only errors at runtime. Before you drop or rename ANYTHING, enumerate consumers yourself. The recurring misses and how to not repeat them:

1. **Search the SYMBOL in EVERY name format, and inspect each hit — do not trust an import scan.** A field/table/model appears as `foo_bar` · `FooBar` · `fooBar` · `foo_bars`/`FooBars` (plural) · the manager instance (`foo_bars_manager_instance`) · the wire/label alias. Import-graph tools only see top-of-file `import` lines and **completely miss mid-file / lazy / inside-a-function imports** (this is the #1 leak). So grep the raw text across the whole tree and open every hit:
   ```
   rg -n 'foo_bar|FooBar|fooBar|foo_bars|FooBars|foo_bars_manager|"is_public"|\bis_public\b|isPublic'
   ```
   For each hit ask: *is this the same table/field, and does it read/write a column I'm changing?* A wrong-format miss (e.g. `SklResource` when you searched `skill_resource`) is exactly how consumers slip through.
2. **OPEN the auto-generated consumer hubs — they are NOT boilerplate to skip.** These list tables by name and break generation or wiring when stale: aidream `aidream/_generated/package_db_wiring.py`, `db/helpers/auto_config*.py`, every `packages/*/db/db_requirements.py` **manifest** (a dropped table left in a manifest hard-fails `db/generate.py` — this bit skill.resource). FE `types/database.types.ts`; the entity vocabulary in `@ai-matrx/associations` (`pnpm check:entity-types`). Grep them for the name; fix the manifest, then regenerate.
3. **Grep raw-SQL strings for the table AND field names** — `FROM <table>`, `.from("<table>")`, `.eq("<field>"`, `filter_items(<field>=`, `getattr(row,"<field>"`, raw `UPDATE/INSERT/SELECT` literals. The ORM/type system never sees these. `getattr(row,"is_public",False)` is the worst: it silently returns the default when the column is gone — grep `getattr(` for every changed field.
4. **Run the repo discovery tools — they help but DON'T replace the multi-format grep above:**
   - **aidream:** `python db/table_refs.py <table> [token]` (git-grep report, buckets hits incl. `package_integration.py`) · `python db/schema_analysis/check_schema.py --refresh` (live DB vs yaml/models/managers/**raw-SQL string literals**/imports — the import check *does* see lazy/mid-file imports; the raw-SQL check uses an allow-list of roots so it can miss excluded dirs) · `python docs/database/generate_handwritten_sql_inventory.py` (every runtime raw-SQL site) · `python scripts/audit_orm_getattr.py` (the `getattr` silent-column trap) · `python scripts/check_package_wiring.py` (manifest↔generated drift).
   - **matrx-frontend:** `node scripts/db-table-refs.mjs <table> [token]` · `pnpm tsx scripts/schema-check/check-schema.ts` (live DB vs generated types + consumers) · `pnpm check:dead-relations` (bare `.from("<old>")` / `public.<old>` / `Database[...]["<old>"]`) · `pnpm type-check` (typed refs only — the backstop, run LAST).
5. **The workflow:** grep every name-variant → open every hit + every generated hub → fix raw-SQL strings → repoint typed refs → THEN `type-check` / `generate.py` / `check:dead-relations` to confirm you missed nothing. Tools last, not first. "The compiler will catch it" is how the silent misses ship.

**Add the retired relation to `scripts/dead-relations.json` + `db/check_dead_relations.py` BEFORE repointing** — the guard then becomes your live checklist of what's still pointing at the old name.

---

Structural changes to **Matrx Main** (`brsgrqvjdzwihsvnfqkf`) during scheduled downtime. 🚨 **DDL goes through `pnpm db:apply migrations/<file>.sql` — the ONE apply path, downtime included** (CLAUDE.md § Migrations): the whole file in one transaction, and the applier writes the `public._schema_migrations` row with the SHA-256 of the bytes it executed. Never paste DDL into the database tool by hand, and never write that ledger row yourself — on that path a statement you leave out of a payload stays missing while `pnpm check:migrations` reads green. The file is therefore not a convenience: it is the unit that gets applied (a file still changes nothing until applied + verified live). Write it whole and apply it in one call; chunking is what prolongs the outage.

**Before any change, read [`TOOLKIT.md`](./TOOLKIT.md)** (verified live signatures, registry shapes, constants, gotchas) and the rulebook [`db-rules/FEATURE.md`](../../../../common-docs/systems/architecture/database/FEATURE.md) (what a canonical table IS). **Where a table belongs:** [changeover doctrine §7](../../../../common-docs/policies/database-changeover-doctrine.md) (one feature, one schema; `public` keeps no tables) + [PLATFORM-CONVENTIONS §E](../../../../common-docs/systems/human-resources/projects/hr-domain/PLAN.md) (every live schema's purpose, verified 2026-08-25); re-check live with `obj_description(oid,'pg_namespace')` — the `workbench` comment carries the `workbench` (user-constructed materials) vs `projects` (coordination) split. **Where any doc and the live DB disagree, the DB wins** — re-verify with `execute_sql` before betting a migration on it.

## Propose first — for multi-table, data-migrating, or consumer-facing changes
A change is rarely one table. Before executing anything risky (a cluster, a data migration, a schema move, a retire/drop), **do the homework and fill [`PROPOSAL_TEMPLATE.md`](./PROPOSAL_TEMPLATE.md)** — scope the whole cluster, quantify the repoint cost across both repos (+ extend/local) with the `db-table-refs` helpers, list the decisions with recommendations — save it to `docs/db_rebuild/proposals/<slug>.md`, and get a **`go`** before mutating. A single-column tweak or an obviously-safe additive step doesn't need one; anything that could lose data or break a production consumer does.

## THE LAW: zero data loss, always

1. **Never `DROP TABLE` (or `DROP COLUMN` with data) during the transition.** Retirement = `ALTER TABLE … SET SCHEMA deprecated` (reversible). Hard DROP is a separate, later, PITR-gated step.
2. **Additive-first, cut over, then retire.** Add new structure → backfill → dual-write/mirror if needed → repoint consumers → verify counts match → only then retire the old.
3. **Getting a table offline is reversible and is the first priority**; resolving every dependency is required but **must not block the move** — deprecate it, then finish the cleanup. (DROP is what's gated, not the schema move.)
4. **Verify live, not on faith.** After every DDL, `execute_sql` to confirm the object exists and `SELECT count(*)` to confirm no rows were lost. Compare pre/post counts.
5. **Loud recovery.** Any bridge/backfill/mirror you add must scream (RAISE / log) when it fires on data it shouldn't — a silent fallback hides the bug it's papering over.

## THE CUT — no silent shim (read twice; this is the #1 source of disasters)
When a table is MOVED or RETIRED, **the old name MUST stop working — abruptly.** AI agents do not reliably catch lingering references, so a "nice fallback" old table is how reads/writes silently split across two tables and burn a day to debug. **A clean cut + 15 minutes of repointing beats a silent shim every time.**

- **Default = make the old name vanish.** `SET SCHEMA workbench` / `SET SCHEMA deprecated` / rename — the data is preserved at the NEW location, but `public.<old>` no longer resolves, so every stale ref **errors loudly** (PostgREST 404 in the browser console = red; a raised exception in server logs = red). That IS the desired behavior.
- **NEVER leave a compat VIEW or a still-readable old table** that silently passes through. That is the forbidden shim. (Reconciles with Law #1: "data preserved, reversible" ≠ "old name still readable." Deprecated/move preserves data AND kills the old name.)
- **If a table genuinely can't move yet** (consumers can't all be cut in the window), do NOT leave it readable — install a **tripwire**: `select platform.deprecate_relation('public','<t>','<new.ref>','<reason>')` renames the data aside (zero loss) and replaces the old name with a view + INSTEAD-OF triggers that **RAISE on any read or write** with a message naming the new location (TOOLKIT.md §9). A shim that errors loudly is acceptable; one that silently works is not.
- 🚨 **THE EXCEPTION, AND IT IS THE ONE THAT BIT US: a RENAME of a table that LIVE USERS ARE USING RIGHT NOW.** This whole section assumes a downtime window — no traffic, so a hard cut costs a red log line. Outside a window it costs a person their work. **The old name must keep resolving until the new code is DEPLOYED** (`CREATE VIEW old_name AS SELECT * FROM new_name`, dropped once the running SHA has the new code), or the rename goes LAST, after the code is live. A "loud" 42P01 is not loud to the human it happens to: the agent above it reports success in prose and the content simply never existed. **2026-08-17:** `platform.expertise_pack` → `platform.rulebook` landed ahead of the deployed code while an Expert was an hour into dictating his SEO method; five calls died, one carrying 11 finished expert rules (8,773 chars), recovered only because `chat.tool_trace` happens to keep `args`. Full rule: `common-docs/policies/database-changeover-doctrine.md` §8a-2.
- **Light up the terminal RED until refs are gone.** Every move/retire MUST: (1) add the relation to **`scripts/dead-relations.json`** + `platform.deprecated_relations`, and (2) leave **`pnpm check:dead-relations`** green. 🚨 **Nothing runs it for you — there is no pre-commit hook and no CI in this repo; YOU run `pnpm check:dead-relations` (or `:strict`) before you call the move done.** It scans for bare `.from("<old>")`, `public.<old>`, and `Database["public"][…]["<old>"]` and screams until every one is repointed. Add the manifest entry *before* repointing so the guard becomes your checklist. (aidream has the parallel `db/check_dead_relations.py`.)

## Pick the change (route here)

| Task | Skill |
|---|---|
| Take a table offline / retire it (no longer used) | **`db-deprecate-table`** |
| Relocate a table to another schema, references intact | **`db-move-table-schema`** |
| Bring a table/feature onto the platform standard — base cols + FKs, RLS, registry, satellites, versioning (a.k.a. "retrofit" / "base retrofit" / "Wave 3"; take it to certified or stop at the transition floor) | **`db-canonicalize-table`** |
| Drop / merge / modify-logic / find stragglers / anything else | **[`playbooks.md`](./playbooks.md)** |
| Sharing cascade / containment rules / new association edge shape ("share X and its contents come along") | **TOOLKIT.md §3** (`association_types` + `reachability`) + [`docs/db_changes/REACHABILITY-ROLLOUT.md`](../../../docs/db_changes/REACHABILITY-ROLLOUT.md); manage rules via `/administration/relationships`, never raw SQL |

## Constants (full table in TOOLKIT.md §0)
- Project: **Matrx Main** · `project_id` **`brsgrqvjdzwihsvnfqkf`**.
- System org ("Matrx System"): **`39c38960-d30c-4840-b0c1-c9960de95582`** (ownerless-row fallback).
- **Exposed-schema trap:** `pnpm db-types` only pulls `public, context, files, workflow, workspace, app, skill, tool, agent, chat, ai, deprecated`. A FE-read table in any other schema needs its schema added to the `db-types` `--schema` list + PostgREST exposure, or the FE gets no types and 404s.

## Cross-repo finalize (run for EVERY change — TOOLKIT.md §8 has detail)

1. **DB** — write `migrations/<name>.sql` (idempotent) with `-- draft: <you> <what is unfinished>` as its FIRST line (the release sweep ships anything in `migrations/` every 30 minutes; a draft is held — JUDGMENT.md §1c) and remove that line only when the file is done, then **`pnpm db:apply migrations/<name>.sql`** — the ONE apply path: whole file, one transaction, and it writes the `public._schema_migrations` row itself with the SHA-256 of the bytes it executed. Never hand-apply through the MCP and never write that row yourself (CLAUDE.md § Migrations). Then verify live with a read.
2. **Frontend** — `pnpm db-types`; update every usage; `pnpm sync-types`; fix all TS.
3. **aidream** — `python db/generate.py`; new schema → `db/matrx_orm.yaml` (`additional_schemas` + generate block); sub-package table → `aidream/package_integration.py`; `python db/detect_applied.py`; update usages; `python run.py` → clean boot.
4. **matrx-extend / matrx-local** — update if referenced; never block production.
5. **Commit + push `main`** on matrx-frontend and aidream.

## Other playbooks (drop, merge, modify logic, stragglers, anything else)

**Drop a table, merge two tables, modify logic (function / RPC / trigger / policy), find stragglers, or anything else (split, partition, rename, backfill-only) → read [`playbooks.md`](./playbooks.md).**

## Document as you go
Add one line to the **Done log** of the [DB changeover board](../../../../common-docs/operations/db-changeover-board.md) (doctrine §8 step 5) and update the matching `FEATURE.md` for a canonicalized feature — what changed, counts, what's still open. A change that lives only in a chat log will be redone or broken by the next agent.
