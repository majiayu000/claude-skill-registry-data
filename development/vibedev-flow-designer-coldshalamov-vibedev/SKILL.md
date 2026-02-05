---
name: vibedev-flow-designer
description: Use when translating a program/app idea into a VibeDev MCP Job (deliverables, definition of done, invariants, and a small step plan) and preparing it to transition to READY without implementing features yet
---

# VibeDev Flow Designer (Job Builder)

## Goal

Turn a short “what I want to build” description into a **real VibeDev job in the Store** by using the VibeDev MCP planning tools.

This skill is for **PLANNING mode only**: you are producing planning artifacts that compile into steps. You are not implementing code changes.

## Canonical Reference (don’t duplicate the spec)

When you need authoritative schema/behavior, open these repo docs instead of guessing:

- `docs/07_doc_map.md` (index)
- `docs/00_overview.md` (two-thread workflow + behavioral contract)
- `docs/02_step_canvas_spec.md` (conceptual StepTemplate)
- `docs/03_gates_and_evidence.md` (gate catalog + EvidenceSchema)
- `docs/04_flow_graph_and_loops.md` (retry/diagnose/escalate loop)

When you need what the MCP tools actually accept today (Pydantic models), open:

- `vibedev_mcp/server.py` (tool input shapes, defaults)
- `vibedev_mcp/conductor.py` (planning interview phases + required keys)

## Workflow (PLANNING → READY)

### 0) Decide the minimal job shape

Collect (from the user request or a short follow-up):

- **Title**: short and specific
- **Goal**: 1–2 sentences, outcome-focused
- **Repo context**: existing repo vs greenfield
- **Target environment**: OS, runtimes, constraints (e.g., “Windows + Python 3.11”, “Node 20”)
- **Out of scope**: explicit bullets (prevents creep)

### 1) Create the job (`conductor_init`)

Call `conductor_init` with:

- `title`
- `goal`
- `repo_root` only if there is an existing repo and you know the absolute path
- optional `policies`

Recommended policies for reliable gating (safe defaults):

- `evidence_schema_mode: "strict"` (forces `criteria_checklist` when steps have acceptance criteria)
- keep `enable_shell_gates: false` unless the human explicitly opts in (command gates are powerful)

### 2) Drive the planning interview (`conductor_next_questions` / `conductor_answer`)

The conductor phases are enforced by required keys (see `vibedev_mcp/conductor.py`).

Answer questions by calling `conductor_answer` with an `answers` object containing keys like:

- Phase 1 (Intent & Scope):
  - `repo_exists`: boolean
  - `out_of_scope`: bullets (string or list; be consistent)
  - `target_environment`: string
  - `timeline_priority`: string (“MVP”, “robust”, etc.)
  - `user_constraints` (optional): string
- Phase 2 (Deliverables):
  - `deliverables`: `list[str]`
  - `definition_of_done`: `list[str]`
  - `tests_expected` (optional): string or list of commands
- Phase 3 (Invariants):
  - `invariants`: `list[str]` (use `[]` explicitly if none)
- Phase 4 (Repo context; only if `repo_exists=true`):
  - `repo_root`: absolute path string
  - `key_files` (optional)
  - `entrypoints` (optional)

Tip: For deliverables / DoD / invariants, you can also call dedicated tools:
`plan_set_deliverables`, `plan_set_definition_of_done`, `plan_set_invariants`.

### 3) Compile a small, verifiable plan (`plan_propose_steps`)

Build an ordered list of **small** steps. Each step should be “one reviewable diff” maximum.

Each step is a `StepSpec` (see `vibedev_mcp/server.py`), with fields:

- `title`: short
- `instruction_prompt`: the executor prompt for that step (execution runway; keep it precise)
- `expected_outputs`: list of concrete things produced in that step (files/commands/notes)
- `acceptance_criteria`: list of checkable statements (“X exists”, “tests pass”, “no changes outside Y”)
- `required_evidence`: list of evidence keys required for this step (e.g., `changed_files`, `commands_run`)
- `gates` (optional): list of `{type, parameters, description}`
- `remediation_prompt`: what to do if rejected (retry guidance)
- `context_refs`: optional list of context block IDs (if you stored any via `context_add_block`)

#### How to write good steps (practical)

- Prefer **3–7 steps** for most jobs; each step must be independently verifiable.
- Every step must include:
  - **Scope boundaries** (allowed paths / forbidden actions)
  - **A success checklist** (acceptance_criteria)
  - **Evidence requirements** (required_evidence)
- If you include **command gates** (`command_exit_0`, `command_output_contains`, `command_output_regex`):
  - You MUST set job policies:
    - `enable_shell_gates: true`
    - `shell_gate_allowlist: ["<pattern1>", "<pattern2>", ...]`
  - Otherwise the gate will deterministically fail as “blocked by policy”.

#### Default step skeleton (copy pattern)

Use this structure inside `instruction_prompt`:

1. Objective: (one sentence)
2. Non-negotiables: (repeat key invariants + step-specific constraints)
3. Allowed change surface: (paths / allowlist)
4. Tasks: (numbered, minimal)
5. Evidence required: (exact keys you will submit)
6. If stuck: (remediation)

### 4) Refine without replacing (`plan_refine_steps`)

After an initial plan, prefer targeted edits with `plan_refine_steps`:

- `update` a step’s prompt/criteria
- `insert_before` / `insert_after` to add a missing checkpoint
- `delete` to remove redundant steps

This keeps diffs small and avoids accidental plan churn.

### 5) Transition to READY (`job_set_ready`)

Once required artifacts exist (deliverables, invariants, DoD, steps + step order), call `job_set_ready`.

If it fails, inspect missing fields and go back to the planning interview or step proposal.

## Common Failure Modes (and fixes)

- **Command gates failing immediately**: you included command gates but didn’t opt in via `enable_shell_gates` + `shell_gate_allowlist`.
- **Steps too big**: split into smaller steps and add a checkpoint step (e.g., “run tests + summarize evidence”).
- **No real definition of done**: rewrite DoD into checkable items (tests/commands/files).
- **Invariants vague**: rewrite as enforceable rules (“No changes outside X”, “No new deps”, “No refactors”).

## Output Standard

When you finish planning, output a compact summary:

- `job_id`
- Deliverables (bullets)
- Definition of done (bullets)
- Invariants (bullets)
- Step list: step_id + title + one-line objective per step

