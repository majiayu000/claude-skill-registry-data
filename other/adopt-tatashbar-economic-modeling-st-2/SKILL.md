---
name: adopt
description: "Brings an existing model or codebase into the studio: inventories it, reverse-documents it and plans validation and migration."
argument-hint: "[path-to-existing-model]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, AskUserQuestion, Task
---

# /adopt — Adopt

**Category:** Onboarding · **Primary agent:** `modeling-methodology-specialist`

Brings an existing model or codebase into the studio: inventories it, reverse-documents it and plans validation and migration.

Arguments: `$ARGUMENTS`

## Purpose
Bring an existing model or codebase into the studio without breaking it: inventory it, reverse-document its equations and assumptions, capture its current outputs as the reference before anything changes, rate its risk, list gaps against studio standards, and propose a prioritized plan to document, test, validate and possibly migrate it. A lego manifest makes its components and interfaces explicit.

**Use it when** an institution's legacy model, an inherited codebase or a published model is to be used or maintained in the studio.

**Do not use it when** the model will be rebuilt from scratch (`/model-spec`).

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - Existing model code/documents at the given path
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `modeling-methodology-specialist` — primary agent; coordinates the work and integrates results
- `reproducibility-engineer` — Guarantees reproducibility
- `technical-documentation-specialist` — Writes technical documentation
- `model-validation-specialist` — Performs independent model validation
- `matlab-dynare-engineer` — Engineers MATLAB, Dynare, IRIS, RISE and Octave codebases; legacy model maintenance and migration

Run these agents as subagents (the `Task` tool), in parallel where the steps are independent. Subagents only write to the paths named in your instructions.

## Workflow
1. Inventory files, languages, dependencies, data and entry points
2. Reverse-document equations, assumptions and parameters from the code; flag undocumented behavior
3. Run the model if possible and capture baseline outputs as the reference
   - Pin the environment in which the reference was produced
4. Rate model risk level and produce a gap list against studio standards
5. Propose a prioritized adoption plan (document, test, validate, migrate)
6. Draft a lego manifest of the existing model (`/lego-map`) so its components, interfaces and simultaneous blocks are explicit before any change

## Checkpoints with the user
- After the inventory: confirm scope
- After the gap list: agree priorities

## Common pitfalls
- Changing code before capturing reference outputs
- Trusting existing documentation over the code
- Migrating before testing

## Output
`docs/models/<model>/adoption-report.md`

The adoption report holds the inventory, reverse documentation, reference outputs and environment, risk rating, gap list, plan and the draft lego manifest. Every run saves its results to `output/<run-id>/` in the model folder, with a run log (`.claude/rules/model-code.md`).

## Gate / verdict
- Baseline outputs are captured before any code is changed
- The environment that produced the reference outputs is recorded

## Suggested next steps
- `/validate-model`
- `/translate-code`
- `/model-card`
