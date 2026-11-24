---
name: module-03-system-verification
description: 'Bootcamp Module 3: System Verification. Use when the bootcamper starts or resumes Module 3, asks to run verification (including after skipping it), or needs to verify the Senzing system works end-to-end and produce a verification report. (The Truth Set visualization is a separate, standalone module run next.)'
---

# Module 3: System Verification

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

⚠️ **This module has exactly two 👉 questions** — the Mari prediction at Step 7a of
`phase1-verification.md`, and the module-transition question at the end of
`phase2-report-close.md`. The prediction is the second because it must be asked before the engine
decides (the ground rules' "Predictions before results", INV-357). Every other step is **non-yielding**, so
"one at a time" is a rule about order and completeness, not about turns: the steps run in order
inside the turn that ends on the next of those two questions. See `../bootcamp-onboarding/ground-rules.md` → the 👉 protocol, which defines the
non-yielding step and the single-write checkpoint that follows from it.

⚠️ **That count is a passing run's. A failed run also asks Step 9's retry-or-move-on question**
(`phase2-report-close.md` Step 9 item 7), which ends the turn the report is written in; moving on
runs cleanup and the close, which still end on the transition question. A run whose engine fails
to initialize at Step 1a skips Steps 2–8 and the Mari prediction (`phase1-verification.md` Agent
Rule 4's one exception), so it reaches that question in its first turn.

**First:** Read `config/bootcamp_progress.json`, then (per ground-rules) show the module start
banner, journey map, before/after framing, a brief numbered overview of this module's steps, and an estimated time-to-complete (INV-096), before any module work.

**Language:** Use the bootcamper's chosen language — read `programming_language` from
`config/bootcamp_preferences.yaml` (persisted in Bootcamp preparation) at each code-generation
step — for all code generation and verification scripts. Never fall back to a hardcoded language.

**Prerequisites:** Module 2 complete (SDK installed and configured).

**"Run verification":** a request to run system verification — the phrase the opt-out warning in
`phase1-verification.md` offers — starts this module from its beginning, whenever it comes,
including after it was skipped.

**Before/After:** Before, the SDK is installed but untested end to end. After, your entire
system is verified against **synthetic records**: SDK initialization, code generation,
compilation, data loading, entity resolution, and database operations all confirmed working. (The
interactive Truth Set web-app visualization is a separate, standalone module, run next when selected.)

**Success indicator:** ✅ The **8 installation checks** report "passed" — MCP connectivity
(`mcp_connectivity`), engine initialization (`engine_initialization`), SDK initialization
(`sdk_initialization`), code generation (`code_generation`), build (`build_compilation`), data-source
registration (`data_source_registration`), loading (`data_loading`) and database operations
(`database_operations`) — while **results validation**, which is reported separately
(`results_validation`) and is the only one that is not a statement about the install, reports
`passed` or `expectation_mismatch` and is never required to pass (INV-229); the Verification Report is persisted
to `config/bootcamp_progress.json`; the synthetic `VERIFY` data is purged from the database; and
`system_verification` is added to `modules_completed` (full criteria in `phase1-verification.md`). (The Truth Set visualization module — run next when selected — owns its
own `web_service`/`web_page` checks, snapshot, and cleanup.)

⛔ **Results validation is kept separate on purpose: it compares the engine against a prediction the
guide made, so a mismatch has two candidate causes and only one of them is an install fault.** The
installation checks are unambiguous. A results mismatch that the engine coherently explains — via `why_records`
/ `why_entities` — is an expectation mismatch, **not** a failed verification, and must not be reported
as the bootcamper's system failing. Step 7 in `phase1-verification.md` states the procedure for
telling the two apart.

> **User reference:** detailed background on this module lives in the walkthrough above; a
> standalone `docs/modules/MODULE_3_SYSTEM_VERIFICATION.md` reference is a later porting phase and
> is not created yet.

## Error handling

When the bootcamper hits an error during this module:

1. **SENZ error code** (INV-414; message contains `SENZ` + digits, e.g. `SENZ2027`): call
   `explain_error_code(error_code="<code>", version="current")` and include the explanation in
   the Fix_Instruction. If it returns nothing, continue to step 2.
2. **Known pitfalls** (database lock contention, missing language
   toolchains, MCP proxy connectivity): the full `common-pitfalls` reference is a later porting
   phase; for now use `search_docs` to look up the symptom.
3. **Cross-module resources:** SDK install/config issues -> Module 2 remediation; MCP issues ->
   connectivity troubleshooting; language toolchains -> platform-specific SDK guide via
   `sdk_guide`.
4. **Timeouts:** each step has an explicit timeout (MCP 10s, SDK init 30s, build 120s, data
   loading 120s). On timeout, terminate the process,
   record a fail with a timeout Fix_Instruction, and continue to the next check (no
   short-circuit).

System Verification uses **synthetic records** and never touches the Truth Set. The Truth Set is
acquired, loaded, and visualized exclusively by the separate, standalone **Truth Set visualization**
module (`../module-03b-truthset-visualization/`), which documents its own Truth Set source and
fallback.

## Reconciliation notes

- Entity operations (query, read by entity ID, search by attributes, why/how, relationship
  network, export) are NOT direct tools on this MCP server. Generate the SDK code for them via
  `get_sdk_reference` + `sdk_guide` and run it. Never generate SQL against `database/G2C.db`.
- Counts and statistics come from `reporting_guide` and from the generated SDK export code, never
  from direct SQL.
- System Verification starts **no** web service (INV-087; `phase1-verification.md` → Agent Rules,
  *No orphaned processes*). Any web service belongs to the separate Truth Set visualization module,
  which starts and stops it within its own phases.
- No helper script is bundled for `scripts/progress_utils.py` or
  `scripts/fetch_fallback_truthset.py`; where one is referenced, perform the described action directly (write markers to
  `config/bootcamp_progress.json`, fetch/build inline, etc.).

## Phases

- **Phase 1: Verification Pipeline** (steps 1–8, plus the opt-out gate): `phase1-verification.md`.
  Verifies against **synthetic records** generated in Step 2 — System Verification does not touch
  the Truth Set.
- **Phase 2: Report and Close** (steps 9–11): `phase2-report-close.md`. Records
  `system_verification`, purges the synthetic `VERIFY` data, and transitions to the next selected
  module.

The **Truth Set visualization** is a separate, standalone module
(`../module-03b-truthset-visualization/`, `truthset_visualization`) that runs **after** this one when
selected (always in Core; in Customized only if chosen). System Verification hands off to it after
Phase 2 closes; when it is not selected, the next module is Data collection. It is **not** a sub-step
of System Verification (INV-086/INV-087).

Read `current_step` from `config/bootcamp_progress.json` and resume at the right phase.
