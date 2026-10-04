---
name: detailed-execution-planner
description: Creates and updates detailed execution plans as markdown checklists. Use when the user asks to create, refine, expand, or update a plan. Invoke only when explicitly called by user. Intended only for Cursor (*.plan.md) or CAI plans.
user-invocable: true
disable-model-invocation: false
---
# Detailed Execution Planner

## Skill Purpose

Write detailed execution plans that are specific, test-gated, and aligned with requirements and technical specifications.

## Use This Skill When

- The user asks to create a plan.
- The user asks to update or refine an existing plan.
- A task needs a step-by-step implementation sequence before coding starts.
- A workstream must explicitly follow BDD/TDD with functional testing.

## Before Building Plan

Ask the user detailed questions about anything on which you are not 100% certain.
Ask questions one at a time.
Continue asking questions until you are sure you have all needed information and there are zero ambiguities.

## Cursor Plan Frontmatter (Required)

Every generated plan **must** begin with YAML frontmatter that matches the **Cursor plan** shape so plans can be imported and tracked as todos.

- `name`: short human-readable plan title (string).
- `overview`: multi-line summary of goal, scope, and approach (YAML `|` block string).
- `todos`: ordered list of steps; **one todo per execution step**, in the same order as the checklist under `## Execution Plan` (see below).

Each todo entry must include:

- `id`: stable unique id for that step (e.g. `my-plan-step-001`, incrementing).
- `content`: same intent as the matching markdown checkbox line; **must be as specific as the checkbox** (commands, paths, test names - not shortened into vague summaries).
- `status`: `pending` or `completed` (use `pending` for new plans unless the user marks work done).
- `dependencies`: optional; for a **linear** plan, each step after the first should list the **previous** step's `id` so ordering is explicit.
- For parallel work, use the same dependency pattern only when the user asks for it.

### Synchronization Rule

The number of items in `todos`, their order, and their meaning must match **every** `- [ ]` / `- [x]` line under `## Execution Plan` (only those lines; section headings are not steps).

When you update the plan body, update `todos` in lockstep.

## Flat Checklist Only: No Nested Step Bullets

Use a **single flat list** of top-level checkboxes for all work.

**Do not** nest checklist items under other checklist items.

### Anti-Pattern Examples

```markdown
- [ ] Higher-level step:
  - [ ] Sub-step 1
  - [ ] Sub-step 2
```

### Preferred Pattern

Split into separate top-level steps (same content, no hierarchy under a parent checkbox):

```markdown
- [ ] Higher-level step - sub-step 1 (describe concrete action).
- [ ] Higher-level step - sub-step 2 (describe concrete action).
```

Section headings (`###`, `####`) still group work; only the **checkbox list** stays flat.

## Explicit Step Wording (Required)

Every step (checkbox line and matching `todos[].content`) must be **specific enough that an executor never has to guess** what to run, open, or change.

### What Each Step Must Name (When Applicable)

- **Commands**: the exact invocation (e.g. `just e2e`, `go test ./package/...`, `npx markdownlint-cli2 path`), not "run tests" or "run the suite".
- **Scopes**: package paths, directories, or file globs (repo-relative paths in backticks).
- **Tests**: concrete test names, files, modules, tags, or BDD scenario titles - not "all tests", "the failing tests", or "all 3 tests" without naming which three.
- **Code or docs**: files or symbols to edit, or a clear discovery sub-step that lists them first.
- **Artifacts**: outputs to produce (e.g. report path, migration name) when the step is not obvious from the command alone.

If the exact names are unknown at plan time, the step must say **how** they will be identified (e.g. "list failing tests from `go test ./...` output and add each as its own step in the next plan revision") - not leave a vague single step in place of that work.

### Ambiguous Wording to Avoid

- Steps that rely on unstated context: "Run all 3 tests", "run the new tests", "fix the handler", "update as needed".
- Counts or groups without identifiers: "run every E2E", "run the integration tests" (unless the repo has a single documented target and the step names it, e.g. `just integration`).

### Explicit Wording for Steps

Use imperative text plus **identifiers**: paths, commands, test IDs, or scenario names so the step is self-contained.

## Core Rules

1. Treat requirements as the source of truth, then technical specs, then current implementation.
2. Before planning, read the relevant requirements, tech specs, and implementation context.
3. If requirements or specs are missing, ambiguous, or contradictory, stop and call out the gap.
4. Write the plan in markdown, using **only top-level** `- [ ]` / `- [x]` lines for steps and headings to group them (see [Flat Checklist Only: No Nested Step Bullets](#flat-checklist-only-no-nested-step-bullets)).
5. Make the plan executable: each checkbox must be a concrete action with explicit scope, not a vague intention (see [Explicit Step Wording (Required)](#explicit-step-wording-required)).
   Prefer short, imperative step text that still names **what** and **where**, and be explicit about files, tests, commands, and artifacts.
   Vague phrases like "run all targeted tests" are not enough unless the plan already lists those targets by path or name.
6. Use BDD/TDD explicitly:
   - add or update behavior specs first
   - write failing tests before implementation
   - implement the smallest change to make tests pass
   - refactor only after tests are green
7. Include additional functional tests for user-facing or API-facing behavior.
8. **Task independence**: each task has its own Requirements and Specifications list, Discovery steps, and Testing, so tasks can be read and executed independently with all steps needed to complete that task.
9. Add validation gates after each task (within that task's Testing sub-section) and require them to pass before moving on.
10. Do not allow a later task to start until the current task's validation steps are complete, and include explicit hold points that say so (e.g. "do not proceed until this passes", "do not start the next task until ...").
11. Include [Cursor Plan Frontmatter (Required)](#cursor-plan-frontmatter-required) with `todos` mirroring every checkbox under `## Execution Plan`.
12. Avoid filler sections and generic advice.
13. When updating an existing plan, preserve completed work where possible and revise only what is still pending or invalidated.

## Planning Workflow

Follow these phases in the order given when producing or revising a plan.

### Gather Inputs

- Identify the user goal.
- Identify the relevant requirement documents.
- Identify the relevant technical specifications.
- Identify the current code, tests, and docs that will likely change.
- Identify missing information, assumptions, dependencies, and risks.

### Define Scope and Constraints

Record the following:

- what must change
- what must not change
- required parity, compatibility, or migration constraints
- required test types
- completion criteria

### Build the Execution Sequence

Order the plan as a sequence of **tasks** (phases of work).
Each task is **self-contained** and independently executable: it has its own discovery, implementation, and testing sub-sections so that the work in that task can be completed and validated without relying on later tasks.

Within each task, use this shape:

1. **Requirements and Specifications**: include in the plan a list of the canonical requirement and spec documents for this task (so executors do not need to guess).
2. **Discovery steps**: gather current implementation and context for this task (e.g. read the listed specs, inspect code and tests, identify gaps).
3. **Red phase**: add or update specs and failing tests for this task.
4. **Green phase**: implement the smallest change to make those tests pass.
5. **Refactor phase**: refine implementation without changing behavior; keep tests green.
6. **Testing**: validation gate for this task (targeted tests, lint, etc.); do not proceed until they pass.
7. **Closeout (Task N)**: generate a **task completion report** (what was done, what passed, any deviations or notes), then mark all completed steps in the plan with `- [x]` as the **last step** in the task before starting the next task.

Add a final **documentation and closeout** task for cross-cutting docs and follow-up.

### Add Mandatory Test Gates

The plan must explicitly require, **within each task**:

- spec or behavior definition updates before implementation (Discovery / Red)
- failing automated tests before code changes (Red)
- functional test coverage when behavior is user-facing or API-facing (Red)
- targeted validation in that task's Testing sub-section before moving to the next task
- **closeout for each task**: mark completed steps with `- [x]` and generate a task completion report before starting the next task
- final verification in the last task (or a dedicated closeout task) before the plan is complete, including a final plan completion report

### Update Plans Carefully

When updating an existing plan:

- read the whole current plan first
- keep completed items checked unless they are now invalid
- insert new steps at the correct point in sequence (within the right task and sub-section)
- update validation steps if scope or task boundaries changed
- ensure the revised plan still enforces task ordering and per-task validation
- update YAML `todos` so it stays aligned with every checkbox line under `## Execution Plan`

## Default Plan Template

Use [`assets/plan-template.md`](assets/plan-template.md) unless the user asks for a different structure.
Read it before drafting, and follow its task shape: every task carries its own Requirements and Specifications list, Discovery steps, Red, Green, Refactor, Testing, and Closeout, so it can be executed and validated on its own.

**After drafting the body**, fill in `todos` so each entry's `content` matches one checkbox line in order (same specificity; do not shorten to vague summaries).
Set `dependencies` to chain linear steps (step N depends on step N-1) unless the user needs parallel tracks.

## Quality Bar

Before finalizing a plan, verify that it:

- includes valid **YAML frontmatter** with `name`, `overview`, and `todos` per [Cursor Plan Frontmatter (Required)](#cursor-plan-frontmatter-required)
- has **one `todos` entry per** `- [ ]` / `- [x]` line under `## Execution Plan`, in the same order, with ids and dependencies consistent with that sequence
- uses **only flat** checklist lines (no nested `- [ ]` under another `- [ ]`)
- is detailed enough for an executor to execute without guessing
- uses **explicit step wording** everywhere: no ambiguous shortcuts like "run all N tests" without naming which tests, files, or commands (see [Explicit Step Wording (Required)](#explicit-step-wording-required))
- includes in each task a **Task N Requirements and Specifications** list so executors do not need to guess (or calls out that they still need to be identified)
- includes BDD/TDD and functional testing where applicable
- **gives each task its own Requirements and Specifications, Discovery steps, Testing, and Closeout** (task completion report, then mark completed steps as the last step) so tasks are independently executable
- enforces validation within each task before the next task starts
- uses checkbox steps throughout the execution section
- stays concise and avoids unnecessary narrative
