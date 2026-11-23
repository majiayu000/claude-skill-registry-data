---
name: qfai-configure
title: QFAI Configure (Tune qfai.config.yaml)
description: "Analyze the repository and tune qfai.config.yaml test globs and project overrides. Use when asked to configure QFAI for a repository, or to fix test globs that match the wrong files or none."
argument-hint: "[--auto]"
allowed-tools: [Read, Glob, Write, Edit, TodoWrite, Task, Agent]
mode: evidence-focused
---

<!--
QFAI Skill Body (SSOT)
- This file is intended to be referenced by tool-specific wrappers (e.g., GitHub/Claude/Codex skills).
- Keep wrappers thin and route users to this skill body.
-->

## /qfai-configure - Configure QFAI for this repository

## User Questions (AskUserQuestion Protocol)

Follow `.qfai/assistant/rule/shared-skill-operating-baseline.md#user-questions-askuserquestion-protocol`.

Skill-specific examples:

- configuration decisions
- glob pattern confirmation

Both examples are clarifications and count against the Article VI budget: at
most 5 per invocation of this skill, after which the remaining choices are taken
as labelled assumptions and recorded in the config diff — see
`.qfai/assistant/rule/constitution.md` Article VI. The `hard-required`
inputs in Default Autopilot Policy are the exception: they are never assumed,
and a missing one blocks the run until it is provided — but only where this run
consumes it; one this run never reads is not asked for at all. The stops this
skill declares — Step 4's zero-match glob, and an ambiguous tooling choice or
runnable path — are `hard-required` inputs, not clarifications to assume, so
both outlive an exhausted budget.

## FORMAT SSOT

- Follow `.qfai/assistant/rule/shared-skill-operating-baseline.md#format-ssot`.

- Before writing or editing any `.qfai/**` artifact, read the relevant skill-local reference or template:
  - `.qfai/assistant/skill/qfai-sdd/references/spec-traceability-rules.md`
  - `.qfai/assistant/skill/qfai-sdd/references/contract-artifact-rules.md`

## Inputs Priority (Preflight)

When unsure, read inputs in this order:

- P1: `.qfai/assistant/rule/*`
- P2: Read `.qfai/assistant/rule/agent-selection.md`, the cards under `.qfai/assistant/agent/`, and project context under `.qfai/spec/01_policy/` and `.qfai/spec/03_contract/`.
- P3: `.qfai/spec/decisions.md` (Decision Records; if no decision exists, state "not applicable").
- P4: the business flows, stories, contracts, tests, and evidence relevant to the configuration.

- Before an agent decision, search the records for a turned-down option, as
  `.qfai/assistant/rule/references/deliberation-record.md` says.

## Sub-agent Delegation

Follow `.qfai/assistant/rule/shared-skill-delegation-baseline.md`.

### Work Orders Summary (evidence)

Use the shared schema.

### Stage Minimum Roles

- Author: the session agent writes the artifacts itself.
- Integrate: the session agent presents the result to the user for confirmation.
- Gate: a reviewer that did not author the work returns only `PASS` or `REVISE`. The session agent never approves its own work.

### Reviewer Gate

- Follow `.qfai/assistant/rule/shared-skill-delegation-baseline.md#reviewer-gate-baseline`.
- Reviewer checks:
  - no reviewer authored what it reviewed;
  - doctor evidence exists: `npx qfai doctor --fail-on error` completed without failing checks;
  - Drift Protocol enforced;
  - test-layer policy enforced against `.qfai/assistant/rule/test-layers.md`;
  - tool-count heuristics are signals, not gates.
- The reviewer is `implementation-reviewer`, briefed as the delegation baseline
  states.
- Do not declare DONE or handoff until every finding of its one review is fixed or answered.

### Work order template (copy/paste)

Use the shared template.

### Reviewer response template

Use the shared template.

- Required field: `Status (PASS/REVISE/PENDING)`. `PENDING` marks a gate that could not be run (see the baseline's reviewer-budget branch); it never counts as `PASS`.

## Policy check

Follow `.qfai/assistant/rule/shared-skill-operating-baseline.md#policy-check`.

- Fill policy from verifiable repository evidence first; when evidence is missing, mark the field `TBD` and name the gap in the final report.

## Rejected Option Guard

Follow `.qfai/assistant/rule/shared-skill-operating-baseline.md#rejected-option-guard`.

## Hard Constraints (Read First)

- Only update `qfai.config.yaml` and project-owned policy and contract files under `.qfai/spec/` unless explicitly asked.
- Run the mandatory checks listed below and record outcomes.
- Stop and escalate if tooling choices or runnable path remain ambiguous. This stop is a `hard-required` input, not a clarification, so it outlives an exhausted Article VI budget — with the budget spent and the ambiguity unresolved, escalate rather than picking a runner.
- Completion must be approved by a reviewer who did not modify the config.

## Completion Contract (Shared)

Follow `.qfai/assistant/rule/shared-skill-operating-baseline.md#completion-contract-shared`.
The smallest applicable smoke check is one terminating command from the documented runnable path plus `npx qfai doctor --fail-on error`.
Require `traceability.testGlobs` to report `[ok]`; exit 0 with a warning or truncated scan does not prove test discovery.
Also run `npx qfai validate --fail-on error` and inspect `issues` by code in the result it wrote: the configured `output.validateJsonPath` with `-full` before the extension (default `.qfai/report/validate-full.json`), once its `generatedAt` is no earlier than the run's start.
Where another `full` run can overlap on the same tree, read the run's own `run-*/validator.json` instead, in the directory its `run-log:` line names.
Resolve config and test-glob errors this skill owns, including `QFAI-SCAN-002`; report `QFAI-STORY-006` through `QFAI-STORY-009` uncovered obligations to the testing stage.
A path recorded but never executed is UNRUN.
Follow `.qfai/assistant/rule/shared-skill-operating-baseline.md#gate-failure-autorepair-protocol` for validate, doctor, and quality-gate failures.

## Goal

Analyze the repository and update `qfai.config.yaml` so traceability checks are actionable, with a documented minimum runnable path.

Note: /qfai-sdd includes a preflight step that bootstraps missing config/policy when run directly after init.
/qfai-configure remains the recommended way to tune `qfai.config.yaml` early with a clean, minimal diff.

## Success Criteria (Definition of Done)

- `qfai.config.yaml` is updated with a **minimal diff** focused on traceability globs.
- `validation.traceability.testFileGlobs` reflects the real test layout.
  - `npx qfai init` ships this empty on purpose. Detect the stack before setting it — `pyproject.toml` / `setup.cfg` (Python), `go.mod` (Go), `pom.xml` / `build.gradle` (JVM), `Cargo.toml` (Rust), `package.json` (JS/TS), `Gemfile` (Ruby), `composer.json` (PHP) — and derive globs from the test paths that actually exist, not from the language's convention alone.
  - Cross-check the matched files against the business flows, acceptance criteria, and examples under `.qfai/spec/02_business-flow/`. BF needs E2E coverage, AC needs integration or API coverage, and EX needs a selected non-E2E test.
  - The final report must show at least one matched file per declared test layer (unit / integration / api / e2e / component as applicable). A layer with zero matched files is a blocking gap, not a note.
  - A scan failure is `QFAI-SCAN-002`; the run is not done until the configured selection scans completely. `QFAI-STORY-006` through `QFAI-STORY-009` report uncovered BF, AC, and EX obligations for the testing stages.
- `validation.traceability.testFileExcludeGlobs` is added only when needed.
- A validation checklist with evidence (sample matched files) is produced.
- Project-owned policy and contract files are filled or refreshed from evidence, or marked `TBD` when evidence is missing. Keep quality-gate commands solely in `03_contract/tech.md` under Standard commands.
- Completion is approved by a reviewer who did not modify the config.

## Mandatory checks

- Tool selection rationale is recorded (per layer if applicable).
- A minimum runnable path is described (dev server, db, env, commands).

## Not-done criteria

- Tool selection rationale missing.
- Minimum runnable path missing or unverifiable.

## Final report

The final report includes:

- chosen tools per layer (E2E/API/Integration/Component/Unit)
- the Standard commands section in `03_contract/tech.md` and the commands actually executed
- the proposed include and exclude globs, with 5 to 15 sample matched files, or every matched file when fewer than five match
- the minimum runnable path
- the files changed
- gaps and open risks ("none" is acceptable if justified)
- the final status (PASS/FAIL) and who confirmed it

## Working principles

Read `references/principles.md` when a choice is not settled by a step below.
It holds the seven principles the steps follow: the specification is the
source of truth, traceability, evidence over confidence, minimal scope without
hidden gaps, quality gates, runnable output, and the user's time. A choice a step
settles needs no reading of it.

## README Rule

Do not create `.qfai/**/README.md` files as scaffold or format documentation; keep artifact guidance in skill references/templates.

- READMEs are reference guides. Follow their structure, templates, and checklists.

## Absolute Rule - Output Language

**Write all outputs in the user's working language for this session.**

- If the user writes in Japanese, output Japanese.
- If the user writes in English, output English.
- If the user mixes languages, prefer the dominant language unless explicitly instructed otherwise.  
  This rule overrides all other stylistic preferences.

## Who does the work

The session agent analyzes the repository and writes the configuration itself.
The one sub-agent is `implementation-reviewer`, which reviews what the session
wrote; the delegation baseline says how it is briefed.

## Completion Separation

- The session agent's configuration change and its approval are separate: the
  reviewer approves, never the session agent.
- The reviewer confirms the evidence sampling before approval.

## Context Refresh (long tasks)

Every 5 major actions, pause and restate:

- DoD and prohibited "done" criteria
- Evidence samples collected vs missing
- Config changes and policy updates completed

## Constraints

- Do **not** modify tests or source code.
- Avoid overly broad globs (e.g., `**/*`).
- Exclude generated/output directories (`node_modules`, `.git`, `.qfai`, `dist`, `build`, `coverage`, `.next`, `out`, etc.).
- Write no `validation.require` key; the sections of a story-tree document come from the shipped schemas.

## Step 0 - Load Context (always)

1. Read relevant **project policy** (if present):
   - `.qfai/spec/01_policy/objective.md`
   - `.qfai/spec/01_policy/initiative.md`
   - `.qfai/spec/03_contract/tech.md`
   - `.qfai/assistant/rule/agent-selection.md`, and
   - the acting role's card under `.qfai/assistant/agent/`.

2. Read **project constitution / instructions** (if present):
   - `.qfai/assistant/rule/constitution.md`
   - `.qfai/assistant/rule/workflow.md` (or equivalent)
   - `.qfai/assistant/rule/quality.md` for general gate policy. Reconcile
     project commands against the toolchain detected in step 3, and record
     them only under `<paths.contractsDir>/tech.md#standard-commands-copy-paste`.

3. Inspect repo conventions:
   - package manager (pnpm/npm/yarn), test runner, lint/typecheck scripts, CI definitions
   - existing test patterns (unit/integration/e2e)

4. Inspect project-owned policy and contract files for placeholders.

## Step 0 - Project Analysis

Before editing config, **thoroughly analyze the current project**:

- background and goals
- directory structure and conventions
- chosen technologies and versions (runtime, package manager, test runner)
- test locations (unit/integration/e2e)
- existing test naming rules (`*.test.*`, `*.spec.*`, `*_test.*`, etc.)

If analysis cannot be performed (missing access), clearly state what could not be verified and proceed with minimal-risk assumptions.

## Step 1 - Identify test frameworks and locations

1. Inspect `package.json` and config files (e.g., `vitest.config.*`, `jest.config.*`, `playwright.config.*`, `pytest.ini`, `go.mod`).
2. Enumerate directories that contain tests (e.g., `tests/`, `src/`, `e2e/`, `integration/`).
3. Note naming rules and extensions that indicate test files.
4. Inspect the story tree and its tests to identify which BF, AC, and EX layers are present.

## Step 2 - Propose glob patterns

Propose the smallest set of **include globs** that covers every test observed
in Step 1, however few or many that is. Step 4 checks the files they match
against those tests.

- Prefer explicit patterns (e.g., `src/**/*.test.ts`, `tests/**/*.spec.ts`).
- Include src-colocated tests if they exist.

Provide **exclude globs** only when necessary (beyond the default exclusions).

## Step 3 - Update project context (evidence-first)

Fill policy templates with repo evidence.

- Keep existing content when already accurate.
- When evidence is missing, write `TBD` and record what is missing.
- Do not invent facts.
- Fill `03_contract/tech.md` in its template's shape: a Stack row for the runtime, the platform and each tool detected, with one row per test layer whose Choice names the tool, the files it was observed in, and why it fits; each runtime dependency with its reason, and the quality-gate commands under Standard commands, one labelled item each. It holds no rule and no constraint; a constraint goes to `01_policy/constraint.md`.
- Fill `## Architecture` of `03_contract/tech.md` from the codebase: one row per layer the module layout shows, what it is responsible for, and the layers its imports reach, or `-`. Name layers, never paths. Implementation places new code by this table and reviewers judge a change against it, so write the import directions the code has.
  - A layer is a group of modules whose imports point one way: an upper layer uses the layers below it, and a lower layer never imports an upper one.
  - Draw the layers first, as one `mermaid` `flowchart TD` with a node per layer and an `Upper --> Lower` edge per import direction. Then write the table rows from the uppermost layer down, so each Depends on names only rows below it. `npx qfai validate` reports a diagram and a table that disagree.

## Step 4 - Evidence sampling (before writing)

Match the proposed globs against the repository before `qfai.config.yaml` is
touched. Sample 5-15 actual test files that match the proposed globs, or every
match when fewer than five exist. The matched set covers the tests Step 1
observed and holds nothing that is not a test.

- If zero matches exist, stop and ask for clarification. Under `--auto` do not ask:
  zero matches leave nothing to assume from, so stop with the empty match set reported
  as a blocker. `testFileGlobs` stays as it was, since Step 5 has not run.
  This stop is **not subject to the Article VI budget** — it is a `hard-required`
  input this run consumes, so it survives clarification-exhausted mode. Do not
  assume a glob and do not write the key; report the unresolved glob as the
  blocker.
- If some directories are ambiguous, list them as Open Questions.

## Step 5 - Update `qfai.config.yaml` (minimal diff)

Write the globs Step 4 matched. Edit:

- `validation.traceability.testFileGlobs`
- `validation.traceability.testFileExcludeGlobs` (only if needed)
- `uiux.surfacePaths`: the repository-relative globs of the paths observed to render a user-visible surface, or `[]` when the repository renders none. Keep an existing value unless the user asks to change it. An absent key leaves the UI impact decision unevaluable.

Keep all other config keys unchanged. Add no key the package already defaults, `paths.specsDir` included; a value the project set stays.

## Output

Provide:

1. Updated `qfai.config.yaml` (diff or full file, as appropriate).
2. Updated project-owned policy and contract files (diff or summary).
3. A short summary of changes and rationale.
4. Validation checklist with sampled files.
5. Open questions (blocking vs non-blocking).

Suggest next step: `/qfai-discussion` (or rerun `/qfai-configure` if configuration is not ready).

## DONE Declaration

When you declare DONE, include:

- Referenced inputs: instructions, project context, `decisions.md`, and any applicable story.
- DEC IDs referenced (or "none" when no decision applies).
- Confirmation that no rejected option was reintroduced.

## Completion Checklist

Check it last; the deliverables themselves are listed in Final report.

- [ ] Repository analysis completed (frameworks, test layout, naming rules).
- [ ] BF, AC, and EX test layers inspected.
- [ ] Project-owned policy and contract files updated with evidence or `TBD`.
- [ ] Standard commands recorded only in `03_contract/tech.md`.
- [ ] Include and exclude globs proposed with rationale, and their matches sampled before `qfai.config.yaml` was written (minimal diff).
- [ ] Hard Constraints followed, and all mandatory checks executed and recorded.
- [ ] The final report is complete, and no untracked gaps remain (or they are explicitly documented).
- [ ] Completion approved by a reviewer who did not modify the config.
- [ ] Open questions that place a **new obligation on the product** were routed to the owner phase (`/qfai-sdd`) as an advisory / proposed specification change per `.qfai/assistant/rule/drift-protocol.md#reviewer-originated-obligations`; questions about this skill's own inputs or settings stay in its own output for the user to answer. This skill does not write `open-questions.md`.
- [ ] The completion message was presented to the user, with next actions for all available options.

## Completion Message & Next Actions

When this skill is complete, provide a final user-facing completion message and enumerate all actionable next steps.

- Proceed (recommended): `/qfai-discussion`.
  Action: run it to formalize requirements from the configured project context.
- Discussion needs more input: rerun `/qfai-discussion`.
  Action: collect missing scope, constraints, and assumptions first.
- Configuration needs refinement: rerun `/qfai-configure`.
  Action: provide additional include/exclude evidence and update `qfai.config.yaml`.

## Default Autopilot Policy

The skill collapses avoidable per-session prompts to 0-1 by classifying every decision into one of three named buckets:

- auto-decide:
  - output formatting
  - ID / sequence numbering
  - append-vs-create on subject overlap
  - equivalent-option pick
- ask-user:
  - CREATE / DELETE / SPLIT / MERGE / SUPERSEDE / UPDATE:REMOVE triage operations (each with a prompt template that names the target and rationale)
  - destructive operations (rm / overwrite / force-push)
  - version-pin changes (`package.json#version`, branch pin)
  - scope expansions outside the active envelope
- hard-required:
  - brand intent
  - a business-flow ID when the user requests flow-scoped configuration and the target cannot be inferred
  - a `testFileGlobs` proposal that matches at least one real file (Step 4)
  - a resolved tooling choice with a runnable path (Hard Constraints)
    — neither this nor the proposal above has a defensible default, and a guess
    is saved as if it were evidence

project_memory:

- qfai-configure is the user-facing entrypoint for editing `qfai.config.yaml`: the test globs, `uiux.surfacePaths` and the other values a project may override.
- Each agent card under `.qfai/assistant/agent/` is the sole definition of that role. Edit the card to change its mission or other role metadata.
- Run after every major workflow change to refresh the consuming project to the current QFAI baseline. Do NOT edit `qfai.config.yaml` directly when the skill is available.
