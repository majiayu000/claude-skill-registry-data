---
name: ramco-journey
description: Generate a deep, gold-quality "journey" JSON for a single Ramco ERP activity (e.g. Create Direct PO, Edit & Approve PO, Maintain Item Basic Information, Generate Supplier Rating, Print PO Register, Purchase Hub) from the Ramco data drop — by parsing the component's Service_details CSV, the stored procedures, the screen objects, and the integration cascade. Use whenever the task is to build, extend, fix, or validate a Ramco activity journey to the depth of the gold po_create_direct reference (14 screens / 197 slots / 146 tools / 493 rules), or to map an activity's screens, slots, SP chains, discriminators, rules, and cross-component (TCAL/VAT/workflow/budget) dependencies.
---

# Ramco Journey Generator

## What a "journey" is

A **journey** is a single, self-contained JSON spec that describes — exhaustively — how an agent (or a human) drives **one Ramco activity** end to end: every screen, every slot the user can fill, every tool (service/SP chain) that can be called, every validation rule, every discriminator that branches behaviour, the cross-component integration dependencies, the document-status outcome, and the termination/commit options.

One **activity** = one row-group in a component's `Service_details_<MODULE>.csv` keyed by `activity_name` (e.g. `PoCrt` = "Create Direct Purchase Order"). That is the unit of a journey. There is exactly **one journey per activity**.

The **gold reference** is `po_create_direct (1).json` (PoCrt): 14 screens, 197 slots, 146 tools, 493 rules, ~25,000 lines. **That depth is the target.** A thin journey is a failed journey.

## The five raw inputs (this drop, nothing else)

Everything is derived from the data drop at the project root (default `/Users/raj/Downloads/Vizuara`) and the feedback set at `/Users/raj/Downloads/Vivek Feedback`. The drop has **5 components** — `GR` (Goods Receipt), `PO` (Purchase Order), `Pur_Qtn` (Purchase Quotation), `Pur_Req` (Purchase Request/RFQ), `SIN` (Supplier Invoice) — each with the **same internal layout**:

| Sub-folder | Feeds | Holds |
|---|---|---|
| `ModelInfo/Service_details_<M>.csv` | **the skeleton** (activity→screen→task→service→method→SP, with `lvl` for integration depth, `ps_sequenceno`/`sequenceno` for order) | the authoritative activity map |
| `ModelInfo/*_Comp_Act_ILBO_Service_Info.xlsx` | cross-check the screen/task hierarchy | component→activity→UI→task→service |
| `ModelInfo/*_Design_Error[_ ]Message.xlsx` | **rule error text** (per `spname` → `Sp_Errorid` → `Error_Message`) | the error catalog |
| `ModelInfo/BPC_Comp_Act_ilbo.*` | journey title / process grouping | process→component→activity→UI human names |
| `SPs/` (or `Sps`/`SPS`) | **rules, writes, status, discriminators, IS calls** | the stored procedures — the real logic |
| `ScreenObjects/<M>/*.htm` + `*_user.js` + `*_State.xml` | **slots, sub-screen nav, action buttons, client rules, locked-on-existing** | the UI screen definitions (older .htm format, NOT EXTJS6 json) |
| `OLH/` | optional slot help text | online help (RoboHelp/WebHelp output) |
| `Table/` | `db_column` grounding, `tables_written` | table DDL |
| `API/` | REST binding for a tool's `binding.api` | OpenAPI specs (a *subset* of services — use highest version) |

> **SPs are shared across components.** A referenced SP may live in another component's folder (e.g. `po_common_vat_sp` lives in `GR/Sps`, not `PO/SPS`). Always resolve an SP by searching **all** `*/SPs|Sps|SPS` folders, never just the activity's own component.

## The non-negotiable pipeline

Generate a journey by running these stages **in order**. Stages 1–4 are deterministic (run the scripts); stages 5–8 mine the SPs/screens for depth; stages 9–10 are the mandatory gates — deterministic first, then the adversarial fleet.

```
0. CLASSIFY      Identify the activity class (genesis / lifecycle / inquiry-report /
                 master-sequence / processing / hub) and its node-kind (A–E).
                 → references/04_activity_classification.md
1. SKELETON      Parse Service_details_<M>.csv → ordered screens → tasks → service →
                 method/SP chain, with the lvl>0 integration sub-chains resolved.
                 → scripts/build_skeleton.py
2. CLASSIFY TASKS For every task, read its SP chain and classify the tool PURPOSE by
                 EMPIRICAL WRITE BEHAVIOUR (commit / report / ui_assist / fetch /
                 init / help_lookup / ui_cascade). Enumerate ALL commits (never collapse).
                 → scripts/classify_sps.py + references/05_sp_parsing_playbook.md
3. SLOTS         Parse every screen's .htm → one slot per control, with control.kind,
                 obligation, fill_behaviour from the CSS class (display-only → never
                 user_entry; *mandatory* class → screen-grounded mandatory).
                 → scripts/extract_slots.py + references/06_screen_extraction.md
4. CROSS-SCREEN  Wire data_flow (entry→main via the grid linkcolumn / header link that
                 carry the doc number) and subflows (forwardlink → sub-screen, each with
                 its OWN commit task). → references/06_screen_extraction.md
5. RULES         Mine EACH SP for validations (error-raising) → rules[]; ground each in
                 spname + error_id (+ Error_Message from the xlsx) + finish_paths.
                 → references/05_sp_parsing_playbook.md
6. DISCRIMINATORS Identify discriminators by SP-layer branching (a value that gates other
                 slots/rules — e.g. po_type, imports_flag), NOT by "it's a combo".
                 → references/05_sp_parsing_playbook.md
7. INTEGRATION   For each commit, follow lvl>0 IS rows + recurse into the bridge SPs
                 (po_common_vat_sp = VAT/TCAL, po_common_wf_sp = workflow). Emit an
                 external_dependency for every called SP/component ABSENT from the drop
                 (this is the TCAL/tax dependency that was previously missed).
                 → references/05_sp_parsing_playbook.md
8. STATUS+FLOW   Build status_determination (Draft/Fresh required_for_fresh tier — the
                 silent, error-less status checklist), flow, termination, prerequisites,
                 post_conditions, variants, intent, provenance.
                 → references/02_journey_schema.md
9. VALIDATE      Run the blind-spots gate (deterministic/structural). Fix every failure.
                 → scripts/validate_journey.py + references/07_blindspots_gate.md
10. ADVERSARIAL   Run the adversarial audit (semantic/source-grounded). A fleet of agents
   AUDIT         tries to PROVE the journey wrong — fabricated ids, templated is_calls,
                 wrong result_states, display-as-mandatory, missing sub-screens/slots —
                 each verdict re-checked by a second skeptic. Resolve every S1/S2 before
                 shipping. → scripts/adversarial_audit_workflow.js + references/08_adversarial_audit.md
```

## How to run a generation

1. **Read `references/03_extraction_pipeline.md`** — the step-by-step operating manual that ties the scripts and references together with exact commands.
2. **Read `references/04_activity_classification.md`** and classify the target activity. This decides which schema blocks dominate and which template adaptations apply.
3. Run the scripts in `scripts/` against the activity to produce the deterministic skeleton + task classification + slots, then mine the SPs/screens for the depth (rules, discriminators, integration, status).
4. Assemble the JSON to the contract in `references/02_journey_schema.md`.
5. **Run `scripts/validate_journey.py`** and read `references/07_blindspots_gate.md`. The gate encodes every defect Ramco's reviews found (commit mis-classification, display-only-as-mandatory, missing data_flow/subflows, create-style elicitation on fetch-first activities, ungrounded discriminators, reports modelled as creates, flattened master sequences, missing integration deps). This is the deterministic/structural gate.
6. **Run the adversarial audit** — `scripts/adversarial_audit_workflow.js` (via the Workflow tool) + read `references/08_adversarial_audit.md`. This is the semantic, source-grounded gate: a fleet of agents tries to *prove the journey wrong* against the raw `.htm`/`.sql`/CSV (fabricated ids, templated `is_calls`, wrong `result_state`s, mis-bound tools, missing sub-screens/slots), and a second skeptic re-checks each verdict. **A journey ships only when both gates pass and every S1/S2 finding is resolved.** Fix file-local findings in the JSON; fix generator-systemic ones in the scripts and regenerate.

## Iron rules (these are why past journeys failed)

1. **Enumerate, never summarise.** Every screen, every control→slot, every SP→its rules, every commit, every IS dependency. Depth is the deliverable. PoCrt has 14 screens / 197 slots / 146 tools / 493 rules; an Edit/Approve journey will be similar order of magnitude.
2. **Classify tools by what the SP WRITES, not by the button label or task name.** A task whose chain writes a MAIN (non-`_tmp`) table is a **commit**; `_rprt_spo` = **report** (terminal, non-persisting); Default / Get-All-Quote-Line-No = **ui_assist**; "Get Details"/search = **fetch**. **An activity has MULTIPLE commits** (Approve + Return; Edit + Edit&Approve + Delete) — list them all in `termination.commit_options`.
3. **Display-only is never user-entry.** Any control whose class is `*displayonly*` (or a label without a `*mandatory*` class) → `fill_behaviour: display_only`, `obligation: optional`. Never `must_fill`. Mandatory is grounded in the **screen** (`*mandatory*` class), preferred over commit-time validation SPs.
4. **Be lifecycle-aware.** Create starts blank (elicit discriminators→header→lines). Edit/Approve/View start by **fetching an existing doc** — model fetch-first, mark fetched fields pre-filled/locked, elicit only the **delta** (or just the decision, for Approve). Never invent mandatory fields on a search/entry screen.
5. **Model sub-screens and their own commits.** "Specify…" `forwardlink`s become `subflows`; each sub-screen is itself transactional with its own Save/Approve task (e.g. *Specify Schedule* `pocrtschtran4`). Capture the conditional trigger (e.g. staggered schedule ⇒ must visit & commit Specify Schedule).
6. **Surface cross-component dependencies, including absent ones.** The tax path (`po_common_vat_sp` → TCAL `tcal_*`) and the workflow path (`po_common_wf_sp` → `WFMTASKBAS`) are integration services. When their target SPs are not in the drop, emit explicit `external_dependency` records — silence here is the exact failure Ramco flagged.
7. **Capture the silent status determination.** The Draft-vs-Fresh decision raises no error code, so it is invisible to error-keyed rule mining. Build the `required_for_fresh` tier separately (see the ~40-condition checklist in `references/02_journey_schema.md`). "Saved" ≠ "Fresh"; only Fresh is approvable.
8. **Ground everything.** Every slot, rule, tool, and dependency carries `evidence[]` pointing at the real `.csv` / `.sql` / `.htm` / `.xlsx` it came from. No claim without a source.
9. **Adversarially audit before shipping.** Structural validation is not enough — auto-generation produces *plausible-but-false* content (fabricated task ids, templated `is_calls`, a `result_state` that reads right but contradicts the SP). Run the adversarial fleet (`references/08_adversarial_audit.md`): assume every authored claim is **guilty until the raw source proves it innocent**, verify existence before semantics, and re-check every verdict with a second skeptic. A fabricated id that a reviewer greps for costs more trust than it costs runtime — find it first.

## Reference & script index

| File | Use it for |
|---|---|
| `references/01_data_map.md` | The drop layout, file→purpose map, casing/quirk catalog |
| `references/02_journey_schema.md` | The exact output contract: every block, every field, the enums, per-class adaptations |
| `references/03_extraction_pipeline.md` | The operating manual — exact commands, stage by stage |
| `references/04_activity_classification.md` | The 6 activity classes + 5 node-kinds + how each shapes the journey |
| `references/05_sp_parsing_playbook.md` | Task types, write-detection heuristic, rule mining, discriminators, integration/TCAL tracing, status mining |
| `references/06_screen_extraction.md` | `.htm` class→slot mapping, forwardlink/transtask, entry→main data_flow |
| `references/07_blindspots_gate.md` | The deterministic validation rubric distilled from all of Ramco's reviews |
| `references/08_adversarial_audit.md` | The adversarial source-grounded gate: the probe catalogue (what each agent must try to disprove), the refute-by-default stance, severity by Chia-impact |
| `scripts/build_skeleton.py` | Deterministic CSV → activity skeleton (screens/tasks/SP chains/IS) |
| `scripts/classify_sps.py` | Read SP bodies → tool purpose + external_dependency detection |
| `scripts/extract_slots.py` | Parse `.htm` screens → slot list with kind/obligation/fill_behaviour |
| `scripts/validate_journey.py` | Run the deterministic blind-spots gate against a generated journey JSON |
| `scripts/adversarial_audit_workflow.js` | Run the adversarial audit fleet (Workflow tool): one agent per probe-group per file tries to prove the journey wrong, a second skeptic re-checks each, synthesised into an S1/S2/S3 defect report |
