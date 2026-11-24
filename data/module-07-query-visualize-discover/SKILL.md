---
name: module-07-query-visualize-discover
description: 'Bootcamp Module 7: Query, Visualize and Discover. Use when the bootcamper starts or resumes Module 7, or needs to query resolved entities, visualize them, and explore results against the business problem.'
---

# Module 7: Query, Visualize and Discover

> **MCP grounding (mandatory — applies to this entire skill).** Every Senzing fact you present —
> SDK method and attribute names, config options, error codes, and entity-resolution specifics —
> MUST come from the Senzing MCP tools, never from training data, memory, or speculation.
> **Pre-response checklist:** if a reply contains any Senzing specific, you MUST have called an MCP
> tool this turn to obtain it; if not, stop and call it first. This has the same precedence as a ⛔
> gate. The full rule and tool routing are the "MCP-first invariant" in
> `../bootcamp-onboarding/ground-rules.md`.

Follow `../bootcamp-onboarding/ground-rules.md` throughout (👉 one-question-at-a-time,
MCP-first, no direct SQL, file placement, checkpointing). Execute every numbered step and
sub-step one at a time, in order. Never skip, combine, or abbreviate a step containing a 👉
question. This has the same absolute precedence as a ⛔ mandatory gate.

**Worked steer.** When the AI's first attempt fails in this module, show the module's one worked
steer, and ask first: the pinned ask-first 👉 comes before the fix, and it may end a turn in a step
this module says asks nothing. What fires it, its two lines, at most one per module, how the
Bootcamper's answer is handled, minimal verbosity and the checkpoint note are stated once in
`../bootcamp-onboarding/ground-rules.md` → "Worked steers"; follow them there rather than a copy
here (INV-300, INV-352).

**First:** Read `config/bootcamp_progress.json`, then (per ground-rules) show the module start
banner, journey map, before/after framing, a brief numbered overview of this module's steps, and an estimated time-to-complete (INV-096), before any module work.
**(INV-366) When it carries a `quality_iteration`, none of this runs:** the Bootcamper chose step 3b's return
and is part-way through it. Route by its `stage`, at the first source not listed in `completed`:
`remap` goes to Module 5's
[Receiving a `quality_iteration`](../module-05-data-quality-mapping/phase2-data-mapping.md#receiving-a-quality-iteration),
and `reload` goes to Module 6's
[Receiving a `quality_iteration`](../module-06-data-processing/phaseB-load-first-source.md#receiving-a-quality-iteration).
Do not re-present the step-3b question, whose answer is already recorded. The route is stated once,
in `phase1-query-visualize.md` step 3b → "The quality-iteration route" (INV-300).

**Before/After:** Your data is loaded and entities are resolved, but you haven't examined the
results yet. After this module you'll have query programs that answer your business questions,
visualizations of your resolved entities, and (optionally) a tour of Senzing's advanced
discover capabilities (why, how, relationship networks).

**Where the bootcamp peaks.** This module carries the bootcamp's "wow moment": the Bootcamper's own
data, resolved, shown first as the headline entity at the end of step 1 and then in the results app
(step 3c). The Truth Set module was the practice run on data built to contain matches.

**Prerequisites:**

- ✅ Module 6 complete (all sources loaded, single or multi-source).
- ✅ No critical loading errors.

**Success indicator:** ✅ Query programs created and tested + queries answer the business
problem + the single interactive visualization app offered (the entity graph and every results
view are tabs within it) + Discover phase completed or explicitly skipped + the data-discoveries
deliverable (`docs/bootcamp_data_discoveries.md` and `.pdf`) produced on every path + every saved
query requirement answered in its `## Your question, answered` section (the Query Completeness
Gate's item 5).

## No direct SQL (module-critical)

This module is all about examining resolved entities. NEVER generate direct SQL against the
Senzing database (`database/G2C.db`) or its internal tables (`RES_ENT`, `OBS_ENT`,
`DSRC_RECORD`, `LIB_FEAT`, `RES_REL`, etc.). Every entity operation goes through the SDK:

- **Search, get entity, why-matched, how-built, network, path** → generate SDK code via
  `get_sdk_reference` (flags, method signatures, **and response structures** — topics `flags`
  and `response_schemas`, narrowed with `filter='<method>'`) plus `sdk_guide` /
  `reporting_guide` (topic `entity_views` for get/why/how patterns, topic `graph` for
  network/path patterns). Look up the response shape **before** writing code that parses it
  (INV-115); a wrong field name renders blank rather than raising.
- **Counts, stats, quality, reporting and visualization data** → `reporting_guide` (topics
  `reports`, `quality`, `evaluation`, `dashboard`, `graph`).

Reconciliation note: `search_by_attributes`, `get_entity`,
`why_entities`, `how_entity`, `why_records`, `find_network`, `find_path`, and
`get_entity_by_record_id` are not callable tools. The current Senzing MCP server does
NOT expose direct entity-query tools. These are SDK **methods**: the agent generates SDK code
that calls them, sourcing flags and signatures from `get_sdk_reference` and code patterns from
`sdk_guide` / `reporting_guide`. Never fabricate SDK method names; always confirm via MCP.

## Error handling

When the bootcamper hits an error during this module:

1. **SENZ error code** (INV-414; message contains `SENZ` + digits, e.g. `SENZ2027`): call
   `explain_error_code(error_code="<code>", version="current")` and present the explanation and
   recommended fix. If it returns nothing, continue to step 2.
2. Look up the symptom via `search_docs`, then present the matching fix (the full
   `common-pitfalls` reference and its Troubleshooting-by-Symptom table are a later porting
   phase).

## Phases

- **Phase 1: Query and Visualize** (steps 1–3c): `phase1-query-visualize.md`
- **Phase 2a: Discover, Part A** (steps 4a–4c): `phase2-discover.md`
- **Phase 2b: Discover, Part B** (step 4d, and step 4e, the export for the systems named in
  Module 1, which runs on every path): `phase2b-discover.md`

Read `current_step` from `config/bootcamp_progress.json` (an integer, or a sub-step string like
`"3b"` or `"4a"`) and resume at the right phase and sub-step. Do not re-run completed steps.
For the Discover phase, also check `module_7_query.steps.<key>` for which 4x sub-steps are
already checkpointed.

## Module position

Module 7 is the last content module before graduation, and it is **required in every path**
(INV-076). The Query Completeness Gate at the end of Phase 1 is this module's transition: once it is
satisfied, the visualization server teardown runs as its own turn when a server was started, then
module completion and the graduation offer. Preserve that gate exactly.

⛔ **Bootcamp graduation always follows — there is no path that ends here.** It is a Required module
in both Core and Customized (`../bootcamp-preparation/SKILL.md` → module list), so never tell the
bootcamper this is where the bootcamp may stop. A bootcamper who wants to keep exploring before
graduating is welcome to; the offer is simply re-presented when they are ready (INV-014 permits only
*requested* skips, and graduation cannot be deselected). The retired A/B/C "track" model that once
allowed a short path ended here was superseded by the Core-vs-Customized path choice (INV-076
supersedes INV-025).
