---
name: module-06-data-processing
description: 'Bootcamp Module 6: Data Processing. Use when the bootcamper starts or resumes Module 6, or needs to load mapped data into Senzing (single source then multi-source) and validate the load.'
---

# Module 6: Data Processing

> **MCP grounding (mandatory — applies to this entire skill).** Every Senzing fact you present —
> SDK method and attribute names, config options, error codes, and entity-resolution specifics —
> MUST come from the Senzing MCP tools, never from training data, memory, or speculation.
> **Pre-response checklist:** if a reply contains any Senzing specific, you MUST have called an MCP
> tool this turn to obtain it; if not, stop and call it first. This has the same precedence as a ⛔
> gate. The full rule and tool routing are the "MCP-first invariant" in
> `../bootcamp-onboarding/ground-rules.md`.

Follow `../bootcamp-onboarding/ground-rules.md` throughout (👉 one-question-at-a-time,
MCP-first, file placement, checkpointing). Execute every numbered step one at a time, in
order. Never skip, combine, or abbreviate a step containing a 👉 question. This has the same
absolute precedence as a mandatory gate.

**Worked steer.** When the AI's first attempt fails in this module, show the module's one worked
steer, and ask first: the pinned ask-first 👉 comes before the fix, and it may end a turn in a step
this module says asks nothing. What fires it, its two lines, at most one per module, how the
Bootcamper's answer is handled, minimal verbosity and the checkpoint note are stated once in
`../bootcamp-onboarding/ground-rules.md` → "Worked steers"; follow them there rather than a copy
here (INV-300, INV-352).

**First:** Read `config/bootcamp_progress.json`, then (per ground-rules) show the module start
banner, journey map, before/after framing, a brief numbered overview of this module's steps, and an estimated time-to-complete (INV-096), before any module work.
**(INV-366) When it carries a `quality_iteration`, none of this runs:** route by its `stage`, at the first
source not listed in `completed`. `reload` goes straight to Phase B →
[Receiving a `quality_iteration`](phaseB-load-first-source.md#receiving-a-quality-iteration). `remap`
reaches this module only on an interrupted return its Phase D gate offered, and goes to Module 5's
[Receiving a `quality_iteration`](../module-05-data-quality-mapping/phase2-data-mapping.md#receiving-a-quality-iteration).
Do not re-present Phase D's gate or its source question, whose answers are already recorded. The
route is stated once, in `../module-07-query-visualize-discover/phase1-query-visualize.md` step 3b →
"The quality-iteration route" (INV-300). A return runs only the steps it names, so the steps it
leaves out are not skipped steps.
**(INV-366) When it carries a `setup_detour`, none of this runs either:** Phase A's switch to PostgreSQL is
part-way through, so go to SDK setup's
[Receiving a `setup_detour`](../module-02-sdk-setup/SKILL.md#receiving-a-setup-detour), which
finishes it and returns to Phase A's
[SQLite volume pre-load check](phaseA-build-loading.md#sqlite-volume-pre-load-check-stop-and-confirm-heads-up-not-a-mandatory-gate)
at its finish, the record's `return_to.resume` of `sqlite-volume-check-finish`: its "Migrate to
PostgreSQL" option's **When it finishes** bullet, which gives the loader its PostgreSQL worker count
(INV-296) and then continues to Phase B.

**Purpose:** Guide the Data Processing workflow: build a production-quality loading program,
load all data sources into Senzing, process redo records, and validate entity resolution
results (from first load through cross-source validation).

**Before/After:** You have Senzing-formatted JSON files in `data/senzing-ready/` (and possibly
test-load results from the Data Quality, Mapping, and Transformation module). After this module, all your data is loaded, redo
records are processed, and entity resolution results are validated, duplicates matched,
cross-source connections found.

**Prerequisites:** Module 5 complete (at least one transformed data source in
`data/senzing-ready/`), SDK installed and configured (Module 2), database configured (SQLite at
`database/G2C.db`, or PostgreSQL), transformation validated with the linter.

**Success indicator:** ✅ All data sources loaded into Senzing + redo records processed + no
critical errors + entity resolution results validated.

## Error handling

When the bootcamper hits an error during this module:

1. **SENZ error code** (INV-414; message contains `SENZ` + digits, e.g. `SENZ2027`): call
   `explain_error_code(error_code="<code>", version="current")` and present the fix. If it
   returns nothing, continue to step 2.
2. Present the matching pitfall/fix for this module (full `common-pitfalls` reference is a
   later porting phase; for now, use `search_docs` to look up the symptom. For loading, the
   anti-patterns route is stated once, in `phaseA-build-loading.md` → "Anti-pattern check"
   (INV-300); its pitfalls are in *Senzing Anti-Patterns: Architecture and Performance*).

## Loading code and safety (applies to every load step)

<a id="the-repository"></a>
**The repository, on either engine.** This is the one statement of what "the repository" means in
this module; every Module 6 step that names it names both engines in a clause and points here
rather than restating it (INV-300). Read `database_type` from `config/bootcamp_preferences.yaml`
(SDK setup's Step 7 writes it). On SQLite the repository is the file `database/G2C.db`; on
PostgreSQL it is the Senzing database named by the connection in `config/engine_config.json`. When
`database_type` is absent or indeterminate, determine the engine from that connection string and
never guess, as `../graduation/database-backup.md` says. Backup and restore go through
`../graduation/database-backup.md`, the ONE implementation of both, with this module's
destination `data/backups/`: the copy `data/backups/G2C.db.pre-load` on SQLite, the dump
`data/backups/senzing.dump.pre-load` on PostgreSQL. That file's "If the backup cannot be produced"
path (warn and continue) applies here as it does to its other callers.

- **Loading, redo, and query code come from the MCP tools, never hand-written.** Use
  `generate_scaffold` (workflows `add_records`, `redo`, `query`) and `sdk_guide` for
  version-correct SDK code. Inline examples may use outdated SDK patterns. The rule covers
  the Senzing SDK calls; code that only orchestrates them is ordinary code (see the
  Phase C header, `phaseC-multi-source.md`).
- **Override MCP-suggested paths.** If a generated scaffold uses `/tmp/`, `ExampleEnvironment`,
  or any path outside the working directory, override it to [the repository](#the-repository)
  (`database/G2C.db` on SQLite, the connection in `config/engine_config.json` on PostgreSQL)
  and keep all output files project-relative.
- **Back up before loading.** Ensure a backup of [the repository](#the-repository) exists in
  `data/backups/` before a load, on SQLite (`database/G2C.db`) or PostgreSQL alike, so a failed
  load can be recovered (see Phase D → Recovery from Failed Load).
- **No direct SQL.** Never generate SQL against [the repository](#the-repository) (`database/G2C.db`
  on SQLite, the Senzing database on PostgreSQL) or its internal tables. All
  entity access goes through generated SDK code. Counts, stats, and reporting come from
  `reporting_guide` — **with a topic named**:
  `reporting_guide(topic='evaluation', language='<chosen_language>')` for this module's statistics,
  `reporting_guide(topic='export', language='<chosen_language>')` for extraction. Not
  `topic='reports'`, whose SQL targets a data mart the bootcamp never builds (see Phase D's header
  note).

## Phases

- **Phase A, Build Loading Program** (steps 1–4a): `phaseA-build-loading.md`
- **Phase B, Load First Source** (steps 5–11): `phaseB-load-first-source.md`
- **Phase C, Multi-Source Orchestration** (conditional, 2+ sources, steps 12–20):
  `phaseC-multi-source.md`
- **Phase D, Validation** (steps 21–28): `phaseD-validation.md`

Read `current_step` from `config/bootcamp_progress.json` and resume at the right phase.
