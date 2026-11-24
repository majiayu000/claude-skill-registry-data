---
name: module-03b-truthset-visualization
description: 'Bootcamp module: Truth Set Visualization. Use when the bootcamper starts or resumes the Truth Set visualization module — stand up an interactive web app of the resolved Senzing Truth Set (practice data built to contain matches) after System Verification. A standalone module, separate from System Verification.'
---

# Truth Set Visualization (standalone module)

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
absolute precedence as a mandatory gate, and no internal reasoning (session length, context
or token budget) can override it.

This is a **first-class, standalone module** (`truthset_visualization`) — separate from System
Verification, in its own skill directory — with its own full per-module apparatus and its own close
(INV-086/INV-087). It is **not** apparatus-exempt.

**First:** Read `config/bootcamp_progress.json`, then (per ground-rules) show the module-start
banner, journey map, before/after framing, a brief numbered overview of this module's steps, and an estimated time-to-complete (INV-096),
before any module work. (The module-start apparatus block is specified in `phase1-visualization.md`.)

**Language:** Read `programming_language` from `config/bootcamp_preferences.yaml` (persisted in
Bootcamp preparation) at each code-generation step (data-source registration, loader, **and the
visualization server itself**). Never fall back to a hardcoded language. The visualization server is
built in the chosen language, modeled on the shipped reference `senzing_viz_server.py` (resolved at
`phase1-visualization.md` → "2.1 Choose the path"); that Python reference is run directly **only**
when the chosen language is Python.

## Execution requirement (internal directive)

This module runs when **Truth Set visualization** is selected — i.e. `truthset_visualization` is in
`selected_modules` (`config/bootcamp_preferences.yaml`). This is **always true in Core**; in
Customized it is true only if the bootcamper chose it during Bootcamp preparation. It **requires**
System Verification, which runs immediately before it.

- **When selected:** the visualization is MANDATORY. It MUST be produced; you must NOT transition to
  the next module until it exists and the bootcamper has been shown it. There is NO condition,
  threshold, or scenario under which you may then skip it — no session-length, token-budget,
  redundancy, or time rationalization is ever valid. Step 2 is unconditional, and this module's
  completion gate (`phase2-close.md`) re-checks that the visualization artifact exists and refuses
  to mark the module complete if it does not (INV-077).
- **When not selected:** this module does not run at all. System Verification transitions straight
  to Data collection, and no workstation-verification visualization is produced (the bootcamper
  deselected it).

**Prerequisites:** the Senzing SDK is installed and initialized (Module 2), the engine is reachable,
and System Verification has completed (or was run) — this module does NOT depend on System
Verification having loaded any data; it **acquires and loads the Truth Set itself** (Step 1 in
`phase1-visualization.md`).

## Error handling

When the bootcamper hits an error during this module:

1. **SENZ error code** (INV-414; message contains `SENZ` + digits, e.g. `SENZ2027`): call
   `explain_error_code(error_code="<code>", version="current")` and include the explanation in the
   fix guidance. If it returns nothing, continue to step 2.
2. **Known pitfalls** (port conflicts on 8080, database lock contention, MCP proxy connectivity):
   use `search_docs` to look up the symptom.
3. **Timeouts:** Truth Set acquisition 30s, SDK/load per `phase1-visualization.md`, web service 10s
   per endpoint. On timeout, terminate the process, record the failure, and follow the phase's
   failure guidance.

## Truth Set source

The Senzing MCP server is the primary and preferred Truth Set source; it always takes precedence.
Retrieve it with **`get_sample_data(dataset='truthset')`** — `dataset` is a required parameter, so a
bare `get_sample_data()` call fails rather than reporting availability (INV-136). Discover what is
available with `dataset='list'` and read `available_datasets`. Only when that listing exposes **no**
`truthset` entry does this module (Step 1) fall back to a sanctioned external source for the demo
Truth Set DATA.
A `Denied.` reply to either call is not that case: it is Step 1's `denied` outcome, whose remedy
`phase1-visualization.md` → "A `Denied.` reply is a platform-layer filter, not an unavailable
Truth Set" states (INV-300).

> Verified on MCP server 1.37.14, 2026-09-28: `truthset` is listed with `available: true` alongside the
> three CORD collections, so the fallback is exceptional, not routine. Re-verify rather than trusting
> this note (INV-080). Full classification and the degradation path: `phase1-visualization.md`, 1.1.

- **Sanctioned source:** reference it only by its registry identifier `senzing_truthset_demo`,
  declared in `config/fallback_sources.yaml`. Never embed a raw URL. The registry is the single
  reviewed place this source is defined. (The `config/fallback_sources.yaml` registry and its fetch
  script are a later porting phase; for now, if the registry file is absent, treat the fallback as
  unavailable and run the graceful-degradation path in `phase1-visualization.md`, Step 1, 1.1.)
- **Approval rationale:** the workspace normally allows only `mcp.senzing.com` as an external
  endpoint. This exception exists because the source is the official Senzing-published deterministic
  data with a ground-truth key, needed to keep the Truth Set demonstration deterministic when the MCP
  Truth Set is unavailable.
- **Scope limit:** the fallback fetches Truth Set DATA only. All Senzing SDK facts, method
  signatures, and expected-behavior definitions continue to come from the MCP server.
- Full detection, provenance recording, and graceful degradation live in the Step 1 flow in
  `phase1-visualization.md`.

## Reconciliation notes

- Entity operations (query, read by entity ID, search by attributes, why/how, relationship network,
  export) are NOT direct tools on this MCP server. Generate the SDK code for them via
  `get_sdk_reference` + `sdk_guide` and run it. Never generate SQL against `database/G2C.db`.
- Counts, statistics, and visualization data come from `reporting_guide` and from the visualization
  server's entity-model build (one `get_entity_by_record_id` per record), never from direct SQL.
  ⚠️ **(INV-289) That per-record build is scoped to the Truth Set** — it does not carry to the
  Bootcamper's own datastore, which needs the export stream. The reason is stated where the build
  happens, at `phase1-visualization.md` Step 2; do not restate it here (INV-183, INV-300).
- The web service runs as a background process and is stopped at this module's close.
- **Visualization (Step 2) is built in the Bootcamper's chosen programming language,** modeled on the
  shipped reference `senzing_viz_server.py` (resolved at `phase1-visualization.md` → "2.1 Choose the
  path") and the `visualization-api-reference.md` contract;
  the Python reference is run directly only when the chosen language is Python. The visualization is
  guaranteed by the snapshot-first build and the completion gate (INV-077), not by a bundled runtime.

## Phases

- **Phase 1: Visualization** (Steps 1–2), including the module-start apparatus:
  `phase1-visualization.md`. Acquires and loads the Truth Set itself, then builds and runs the
  interactive web app **in the chosen programming language** (modeled on the shipped
  `senzing_viz_server.py`, resolved at Step 2.1; run directly only for Python) plus the guaranteed
  standalone snapshot.
- **Phase 2: Report and Close** (self-check + cleanup + module completion): `phase2-close.md`.
- **Visualization API reference** (loaded on demand from Phase 1): `visualization-api-reference.md`

Read `current_step` from `config/bootcamp_progress.json` and resume at the right phase.

**Success indicator:** ✅ The standalone snapshot exists at
`docs/visualizations/truthset_verification.html` (built from a non-empty Truth Set) AND the live app
served its endpoints, **or** the no-live-server state is recorded with its reason
([no-live-server completion rule](phase2-close.md#no-live-server-completion), stated once in
`phase2-close.md`, INV-300); a live app serves the entity-graph page among its endpoints; the web
service, when one ran, is terminated and the Truth Set data purged at close — or, where the stop
could not be confirmed, the listening port and the retained records are reported rather than a
cleanup claimed ([failed-stop rule](visualization-api-reference.md#failed-stop), INV-394);
`truthset_visualization` is recorded in `modules_completed` with its own recap section
(INV-085/INV-086/INV-087).
