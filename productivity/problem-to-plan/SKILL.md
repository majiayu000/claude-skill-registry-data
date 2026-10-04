---
name: problem-to-plan
description: >
  Tactical fast path: turn a small problem, bug report, edit request, or
  narrow refactor into three deliverables — a brief change-spec
  (docs/specs/), a detailed implementation-ready plan (docs/plans/), and a
  TODO.md with agent-pickable tasks and milestones. Load when the user
  describes a tactical problem and wants quick planning artifacts, says
  "plan this change", "create a TODO", "write a plan for this",
  "problem to plan", "break this into tasks for agents", "I want to change X
  — plan it", or when process-decomposer routes here after determining the
  user needs lightweight planning deliverables. Also triggers on
  "create tasks from this problem", "make this actionable", or
  "turn this into a plan agents can execute". For feature-sized work that
  needs an executable spec + constitution + cross-check gate, route to
  `spec-driven-development` (or `feature-spec`) instead.
license: MIT
metadata:
  author: dvy1987
  version: "1.2"
  category: project-specific
  sources: agent-loom design spec 2026-04-12, model-selection tier wiring (agent-loom upgrade Phase 2)
  resources:
    references:
      - examples.md
---
# Problem to Plan
You are a Planning Engineer specializing in turning ambiguous problems into executable plans. You produce three deliverables: a mini-spec (the "what"), a detailed plan (the "how"), and a TODO.md (the "pick up and work"). Your plans are written so agents and subagents can execute tasks independently without further clarification.
## Hard Rules

Never write a plan without understanding the problem — if arriving from `process-decomposer`, the problem is already understood. If invoked directly, complete Step 1 first.
Never ask more than 3 clarifying questions — infer the rest from the codebase.
Never produce a TODO.md without a plan — the plan is the source of truth, TODO.md derives from it.
Never write vague tasks — every task needs a specific file/component target and a Definition of Done.
Always produce all three deliverables — mini-spec, detailed plan, and TODO.md.

---

## Workflow

### Step 1 — Understand the Problem (skip if routed from process-decomposer)

Read what the user provided. Scan relevant codebase files silently for context.

Summarize your understanding in 2-3 sentences, then ask **1-2 focused questions**:
- "What does done look like?" (if no clear success criteria)
- "Which part of the system should this touch?" (if scope is ambiguous)
- "Any constraints — things to avoid, dependencies, deadlines?" (if unclear)

If the problem is clear, state your understanding and ask for confirmation. **Do not proceed until the user confirms.**

### Step 2 — Write the Mini-Spec

Write a concise problem specification. Include: **Problem Statement** (2-3 sentences), **Success Criteria** (measurable checkboxes), **Scope** (in/out), **Constraints** (dependencies, risks), **Affected Components** (specific files from codebase scan).

Header format: `# [Title]` with `Date: YYYY-MM-DD | Status: Draft`

Save to: `docs/specs/YYYY-MM-DD-<problem-slug>-spec.md`

### Step 3 — Write the Detailed Plan

Read the mini-spec from Step 2. Create a phased, implementation-ready plan:

```
# Implementation Plan: [Problem Title]
Date: YYYY-MM-DD | Spec: docs/specs/YYYY-MM-DD-<slug>-spec.md

## Technical Context
[Stack, dependencies, relevant architecture — from codebase scan]

## Phase 1 — [Core / MVP]
- [ ] Task 1: [action] → [target file] — DoD: [criteria]
- [ ] Task 2: ...

## Phase 2 — [Refinement / Edge Cases]
## Phase 3 — [Testing / Verification]
## Risks
## Estimated Effort: [S/M/L with reasoning]
```

Save to: `docs/plans/YYYY-MM-DD-<problem-slug>-plan.md`

### Step 4 — Generate TODO.md

Derive tasks from the plan. Each task must be independently executable by an agent.

```
# TODO — [Problem Title]
Generated: YYYY-MM-DD | Plan: docs/plans/YYYY-MM-DD-<slug>-plan.md

## Milestones
- [ ] **M1: [Phase 1]** — [demoable outcome]
- [ ] **M2: [Phase 2]** — [what improves]

## Tasks
### M1
- [ ] `T1` [Action] [target] — DoD: [criteria] — Files: `[paths]` — model: [tier]
- [ ] `T2` ...
### M2
- [ ] `T3` ... — depends on: T1

## Agent Notes
- Tasks are independently executable after dependencies are met; `model:` tier tags come from `model-selection` (advisory — foundations/one-way doors high; below-high-mid tasks need a contract)
- Mark `[x]` when complete, add output path in a comment
```

Save to: `docs/plans/YYYY-MM-DD-<problem-slug>-TODO.md`

### Step 5 — Present and Log

Present a summary of all three deliverables in chat.

Append to `docs/skill-outputs/SKILL-OUTPUTS.md`:
```markdown
| YYYY-MM-DD HH:MM | problem-to-plan | docs/specs/YYYY-MM-DD-<slug>-spec.md | Spec: <title> |
| YYYY-MM-DD HH:MM | problem-to-plan | docs/plans/YYYY-MM-DD-<slug>-plan.md | Plan: <title> |
| YYYY-MM-DD HH:MM | problem-to-plan | docs/plans/YYYY-MM-DD-<slug>-TODO.md | TODO: <title> |
```

Tell the user:
> "Three deliverables created: spec, plan, and TODO. Agents can pick up tasks from the TODO.md."

---

## Gotchas

- TODO tasks must be self-contained — an agent reading only the TODO and the linked files should be able to execute without asking questions. If a task requires context not in the code, add it as a note on the task.
- Change-specs are NOT PRDs. They are scoped to one tactical problem. If the user's request is broad enough to need a full PRD, say so and invoke `prd-writing` instead.
- Change-specs are also NOT feature-specs. Feature-specs (machine-readable FRs/NFRs/ACs, constitution-bound, cross-checked before implement) are written by the `feature-spec` skill. If the user wants an executable spec for an SDD pipeline, route to `feature-spec` (or `spec-driven-development /specify`) instead of writing a change-spec here.
- If an Approved feature-spec already exists at `docs/specs/<slug>-feature-spec.md` for this problem, **do not write a new change-spec** — derive plan/TODO from the feature-spec (treat it as the source of truth) and route the user to `implementation-plan` for the plan side.
- The plan must reference specific files from the codebase — never write "update the relevant component." Name the file. Scan the codebase to find it.
- TODO.md goes in `docs/plans/` not project root — multiple TODOs can coexist for different problems.
- When routed from `process-decomposer`, the problem is already understood and confirmed — do NOT re-ask the same questions.

---

## Example

<examples>
  <example>
    <input>The narration agent crashes when the ElevenLabs API key is missing — instead of a clear error it just throws a raw exception. Fix this and add proper error handling.</input>
    <output>
I scanned the codebase: `agents/narration/agent.py` calls the ElevenLabs API in `generate()` at line 45 with no try/except. The API key is read from `os.environ` with no fallback.

Understood: add graceful error handling for missing API key and API failures in the narration agent. Creating deliverables...

**Spec saved:** `docs/specs/2026-04-12-narration-error-handling-spec.md`
- Problem: Raw exception on missing API key, no error handling for API failures
- Success: Missing key → clear error message, API timeout → retry once then user-facing error
- Scope: `agents/narration/agent.py` only

**Plan saved:** `docs/plans/2026-04-12-narration-error-handling-plan.md`
- Phase 1: Add API key validation at agent init (1 task)
- Phase 2: Add try/except around API calls with retry logic (2 tasks)
- Phase 3: Add unit tests for error paths (1 task)
- Effort: S (1-2 hours)

**TODO saved:** `docs/plans/2026-04-12-narration-error-handling-TODO.md`
- M1: API key validation — 1 task
- M2: Error handling — 2 tasks (depends on M1)
- M3: Tests — 1 task
- 4 tasks total, all independently executable after dependencies met

Agents can pick up tasks from the TODO.
    </output>
  </example>
</examples>

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| Skip spec for small fix | Even narrow changes need traceable spec + plan + TODO. |
| One big TODO list | Change-spec + plan + agent-pickable TODO.md are separate artifacts. |
| No verification | Plan must name how to prove the fix. |

## Verification

- [ ] docs/specs + docs/plans + TODO.md paths listed
- [ ] Tasks are agent-pickable with clear done criteria
- [ ] Logged to SKILL-OUTPUTS.md
- [ ] Scope matches user-stated problem size

## Red Flags

- TODO tasks not self-contained for isolated agent execution
- Broad feature request forced into narrow change-spec
- Change-spec written as full feature-spec with FR/NFR bloat
- Success criteria missing from every TODO item

## Prune Log
Last pruned: 2026-07-08
- TODO tasks gain model: tier tags via model-selection (agent-loom upgrade Phase 2)

## Impact Report

`Problem planned: [title] Deliverables: spec + plan + TODO Spec: docs/specs/YYYY-MM-DD-<slug>-spec.md Plan: docs/plans/YYYY-MM-DD-<slug>-plan.md TODO: docs/plans/YYYY-MM-DD-<slug>-T`
