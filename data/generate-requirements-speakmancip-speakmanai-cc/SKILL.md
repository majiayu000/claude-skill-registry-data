---
name: generate-requirements
description: Phase 2 of the SPEAKMAN.AI pipeline — run requirements engineering / domain modeling (MCP_REQUIREMENTS_ENGINEERING_V1) to produce the coding contracts Phase 3 consumes
---

# generate-requirements — SPEAKMAN.AI Phase 2 Requirements Engineer

You are executing Phase 2 of the SPEAKMAN.AI delivery pipeline. You orchestrate the
`MCP_REQUIREMENTS_ENGINEERING_V1` workflow — seeded from Phase 1 (Solution Architecture)
output — and save the resulting coding contracts to disk in the exact layout Phase 3
(`generate-speakmanai-code`) reads. You drive the workflow's human-in-the-loop gates; you do
not invent the contract content yourself.

The output of this phase is the `raw/` contract set: domain model, naming dictionary, use
case catalog, API schema, database schema, test strategy, and (optionally) the field
definitions catalog.

---

## Step 0 — Collect Inputs

Ask the user:

> "Where is the Phase 1 (Solution Architecture) output?
>  - **On disk** → provide the path to the SAD output directory that contains a `raw/` folder
>    (e.g. `D:\git\tutorial\outputs\2026-06-15_my-project`)
>  - **A SPEAKMAN.AI session** → provide the Phase 1 session ID and I'll fetch the outputs via
>    `get_output` (uses the public MCP API — never a DB session-mapping bypass)
>  - **Neither** → paste / point me at a business description and I'll run Phase 2 from that alone
>    (lower quality — Phase 1 context is strongly recommended)"

> "Where should the Phase 2 outputs be written? Provide the parent directory (e.g. `D:\git\tutorial\outputs` or the project root). I'll create `outputs/YYYY-MM-DD_{slug}/raw/` under it."

Store:
- **PHASE1_SOURCE**: a local SAD dir path, a Phase 1 session ID, or raw business text
- **OUTPUT_PARENT**: parent directory for the Phase 2 output folder

> **Handoff rule (do not violate):** Passing a session ID so this skill can call
> `get_output(session_id, agent_id)` via the SPEAKMAN.AI MCP client is the intended, allowed
> path. Do NOT design or request any mechanism that reads another session's raw DB records
> server-side without going through `get_output` — that crosses an internal platform boundary.

---

## Step 1 — Load Phase 1 Context

Choose the branch based on PHASE1_SOURCE.

### Branch A — Local SAD files on disk

If PHASE1_SOURCE is a directory, read these Phase 1 files from its `raw/` folder (skip any that
are absent):

| File | Variable | Contains |
|---|---|---|
| `business_context_clarifier.txt` | P1_CONTEXT | Business goal, drivers, outcomes, scope (in/out), risks, detected intent |
| `business_analyst.txt` | P1_REQUIREMENTS | Personas + goals, process flow, data entities, functional/non-functional/compliance requirements |
| `business_application_architect.txt` | P1_COMPONENTS | Logical components, data flows, user interactions |
| `technical_solution_architect.txt` | P1_TECH | Infrastructure decisions, deployment strategy, ADRs — the source of the tech stack |

### Branch B — Fetch from a Phase 1 SPEAKMAN.AI session

If PHASE1_SOURCE is a session ID:
1. `get_outputs(PHASE1_SOURCE)` for the manifest.
2. `get_output(PHASE1_SOURCE, agent_id)` for each of: `MCP_BUSINESS_CONTEXT_CLARIFIER_V1`
   (→ P1_CONTEXT), `MCP_BUSINESS_ANALYST_V1` (→ P1_REQUIREMENTS),
   `MCP_BUSINESS_APPLICATION_ARCHITECT_V1` (→ P1_COMPONENTS),
   `MCP_TECHNICAL_SOLUTION_ARCHITECT_V1` (→ P1_TECH).
   Do not fetch the compliance, visualization, or technical-writer outputs — Phase 2 does not need them.

### Branch C — Business text only

If PHASE1_SOURCE is raw text, set P1_REQUIREMENTS to that text and leave the others empty.
Warn the user: "Running Phase 2 without Phase 1 architecture context — requirement and tech-stack
quality will be lower than a full pipeline run."

---

## Step 2 — Build the Seed Description

Compose **SEED_DESCRIPTION**: a condensed but rich brief for the Phase 2 workflow, drawn from
P1_CONTEXT + P1_REQUIREMENTS (+ P1_COMPONENTS highlights). Include, in this order:

- Business goal and the problem being solved
- Every user persona **with its primary goal** (these drive use-case coverage downstream — do not drop any)
- Key data entities and their relationships
- The functional, non-functional, and compliance requirements (IDs + one-line each)
- In-scope / out-of-scope boundaries
- Target scale / KPIs

**Use the headroom.** The `start_session` description limit is 10,000 characters — forward a
genuinely complete brief (aim 6,000–9,000 chars), not a 3,000-char summary. Lossy condensing
here is the historical cause of thin requirements downstream. Do NOT put the tech stack in the
description — it goes in the Step 3 tech-stack gate.

Derive **TECH_STACK** separately from P1_TECH (platform, runtime, framework, database, payment
/ external integrations, auth, messaging, infra services). Hold it for the Step 3 gate.

Show the user the SEED_DESCRIPTION and the derived TECH_STACK, and say:
"This is what I'll feed Phase 2. Confirm, or tell me what to change." Proceed on confirmation.

---

## Step 3 — Run the SPEAKMAN.AI Session

### 3a — Start

Call `start_session`:
- `workflow_id`: `MCP_REQUIREMENTS_ENGINEERING_V1`
- `title`: short title derived from the project (max 60 chars)
- `description`: **SEED_DESCRIPTION**

Poll `poll_workflow(session_id)` every 30–60s. The workflow has multiple human-in-the-loop
gates; handle each `AWAITING_INPUT` as it arrives, then keep polling until `COMPLETED`.

### 3b — Handle each AWAITING_INPUT gate

On every `AWAITING_INPUT`, read `input_required.agent_id`, `prompt`, `schema`, and `context`,
then respond via `submit_response(session_id, response)` (also pass `executed_by`: the name of your tool and your model, for example `Claude Code, claude-opus-5-5` (say what you actually are and do not guess; it is recorded with the output)):

- **`RE_TECH_STACK_PROVIDER_V1`** — submit TECH_STACK from Step 2, formatted to the gate's
  `schema`. Name concrete technologies (e.g. payment SDK, database engine, auth provider,
  messaging). Present the draft to the user and submit on confirmation.
- **Any `*_HITL_V1` gate** (`RE_USE_CASE_HITL_V1`, `RE_DOMAIN_STRUCTURE_HITL_V1`,
  `RE_DOMAIN_EVENTS_HITL_V1`, `RE_FIELD_DEFINITIONS_HITL_V1`, `RE_NAMING_HITL_V1`,
  `RE_API_TYPES_HITL_V1`, `RE_API_ENDPOINTS_HITL_V1`, and any other agent ending `_HITL_V1`) —
  `context` holds the content under review. Surface it to the user. The response is NOT a
  direct edit — it's `{"status": "Approved"}` to continue, or
  `{"status": "Update", "feedback": "describe exactly what to change and why"}` to send it
  back for regeneration. On `Update` the origin agent regenerates and the same gate re-presents
  the new version for another look, up to that agent's configured retry limit (usually 3
  rounds) before the workflow advances regardless. If the user defers, approve as-is but
  report it in Step 5.
- **Any other gate** — present `prompt` + `context` to the user, collect the answer, submit.

HITL gates are where stack-specific corrections are made — via feedback text describing the
change, not a direct edit. Carry the user's intent through faithfully in the feedback you
submit — do not silently soften or reinterpret it.

Continue polling until `status = COMPLETED` (the full run takes ~10–15 minutes).

---

## Step 4 — Download and Save Contracts

`get_outputs(session_id)` for the manifest, then `get_output(session_id, agent_id)` for each
contract below. Create `OUTPUT_PARENT/outputs/YYYY-MM-DD_{slug}/raw/` (slug = lowercase-hyphenated
title, date = today) and save each with the **Write** tool under the exact filename Phase 3
Branch A reads — do not use bash/Python to write:

| Agent ID | Save as |
|---|---|
| `RE_DOMAIN_MODEL_SYNTHESIS_V1` | `domain_model.txt` |
| `RE_USE_CASE_ANALYST_V1` | `use_case_catalog.txt` |
| `RE_API_SCHEMA_SYNTHESIS_V1` | `api_schema.txt` |
| `RE_DATABASE_SCHEMA_DESIGNER_V1` | `database_schema.txt` |
| `RE_TEST_STRATEGIST_V1` | `test_strategy.txt` |
| `RE_NAMING_CONVENTION_ARCHITECT_V1` | `naming_dictionary.txt` |
| `RE_FIELD_DEFINITIONS_CATALOG_V1` | `field_definitions.txt` |

`RE_DOMAIN_MODEL_SYNTHESIS_V1` and `RE_API_SCHEMA_SYNTHESIS_V1` are synthesis aggregators — each merges two upstream sub-agents (domain structure + domain events; API types + API endpoints) back into the single combined document shape these filenames have always held. Fetch them the same way as any other agent; the merge already happened server-side.

`RE_NAMING_CONVENTION_ARCHITECT_V1` and `RE_FIELD_DEFINITIONS_CATALOG_V1` already carry the human-approved content directly (both agents have their own HITL revision gate) — no separate "reviewed" agent ID to prefer.

If any of the six core contracts (all except `field_definitions.txt`, which is optional) is
absent from the manifest, stop and report which are missing — do not save a partial set as if complete.

---

## Step 5 — Report

```
Phase 2 — Requirements Engineering
Session ID   : {session_id}
Credits used : {session_cost}   (only if a tool reported a cost; leave this line out otherwise)
Phase 1 src  : {Branch A dir | Branch B session | business text only}
Outputs      : outputs/YYYY-MM-DD_{slug}/raw/
  - domain_model.txt
  - naming_dictionary.txt        ({reviewed | unreviewed})
  - use_case_catalog.txt
  - api_schema.txt
  - database_schema.txt
  - test_strategy.txt
  - field_definitions.txt        ({reviewed | unreviewed | absent})
```

Report any reviewer gate the user deferred on, and any contract that came back `[INFERRED]` or
flagged `[DECISION REQUIRED]`.

Then say: "Phase 2 complete. Run Phase 3 with `/generate-speakmanai-code` and point it at
`outputs/YYYY-MM-DD_{slug}` (Branch A reads these files directly — no credits)."

---

## Rules

- **Handoff stays on the public API.** Session IDs are used only via `get_output`. Never bridge
  internal DB records server-side.
- **Forward complete Phase 1 context.** Use the 10,000-char description headroom; do not
  hand-condense to a thin summary — that starves downstream coverage.
- **Drive every gate; invent nothing.** Tech stack comes from Phase 1 + user confirmation;
  contract content comes from the workflow agents.
- **Save the reviewed versions.** Naming and field definitions must be the human-approved
  outputs the downstream designers actually consumed.
- **Filenames are a contract with Phase 3.** Save exactly the names in Step 4 so
  `generate-speakmanai-code` Branch A consumes them with zero glue.
- **Never advance a partial set.** If a core contract is missing, stop and report.
