---
name: sdd-apply
description: >
  Implement SDD tasks from specs and design. Enforces workload budget,
  supports chain strategies, and merges apply-progress across batches.
  Trigger: orchestrator launches apply for one or more change tasks.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "3.0"
  delegate_only: true
---

> **ORCHESTRATOR GATE**: If you loaded this skill via the `skill()` tool, you are
> the ORCHESTRATOR — STOP. Do NOT execute these instructions inline. Delegate to
> the dedicated `sdd-apply` sub-agent. This skill is for EXECUTORS only.

# Skill: sdd-apply

Implementation. Every line of code answers a spec requirement.

## Purpose

You are a sub-agent responsible for IMPLEMENTATION. You receive specific tasks and implement them by writing actual code. Follow specs and design strictly.

## What You Receive

From the orchestrator:
- Change name
- The specific task(s) to implement (e.g., "Phase 1, tasks 1.1-1.3")
- Artifact store mode (`engram | openspec | hybrid | none`)
- Delivery strategy (`ask-on-risk | auto-chain | single-pr | exception-ok`)
- Resolved workload decision (PR slice or `size:exception` when applicable)

## Execution and Persistence Contract

> Follow **Section B** (retrieval) and **Section C** (persistence) from `skills/_shared/sdd-phase-common.md`.

- **engram**: Read `sdd/{change-name}/proposal`, `sdd/{change-name}/spec`, `sdd/{change-name}/design`, `sdd/{change-name}/tasks` (all required). Mark tasks complete via `mem_update`. Save progress as `sdd/{change-name}/apply-progress`.
- **openspec**: Read and follow OpenSpec convention. Update `tasks.md` with `[x]` marks.
- **hybrid**: Follow BOTH conventions — persist to Engram AND update filesystem.
- **none**: Return progress only. Do not update project artifacts.

---

## Step 1: Load Skills

Follow **Section A** from `skills/_shared/sdd-phase-common.md`.

## Step 2: Read Context

Before writing ANY code:
1. Read the specs — understand WHAT the code must do
2. Read the design — understand HOW to structure the code
3. Read existing code in affected files — understand current patterns

### Step 2a: Enforce Review Workload Decision

Before implementing, inspect the tasks artifact for `Review Workload Forecast`.

If the forecast says any of:
- `400-line budget risk: High`
- `Chained PRs recommended: Yes`
- `Decision needed before apply: Yes`

Then confirm the orchestrator provided a resolved delivery path:

1. **auto-chain or chained/stacked PR**: implement only the assigned work-unit slice, keep scope autonomous, report the intended PR boundary.
2. **exception-ok or single PR with exception**: continue only if prompt explicitly says `size:exception`.
3. **single-pr above budget**: continue only after prompt records `size:exception`.

If neither delivery decision nor chain strategy is present, STOP and return `blocked` with: `Workload decision required before apply.`

### Step 2b: Read Previous Apply-Progress (MERGE — if exists)

Before starting work, check for existing apply-progress:

1. `mem_search(query: "sdd/{change-name}/apply-progress", project: "{project}")`
2. If found: `mem_get_observation(id)` → read the full content
3. Parse which tasks are already marked complete
4. Skip those tasks — start from the first incomplete task
5. When saving your apply-progress, **MERGE**: include all previously completed tasks PLUS your newly completed tasks in a single combined artifact

**CRITICAL**: If previous progress exists, you MUST read it. If you overwrite without reading, completed work from prior batches is permanently lost.

## Step 3: Read Testing Capabilities and Resolve Mode

Read testing capabilities to determine implementation mode:

```
Read testing capabilities from:
├── engram: mem_search("sdd-init/{project}") → mem_get_observation(id)
└── Fallback: check project files directly (package.json, pyproject.toml, go.mod, etc.)

Resolve mode:
├── IF strict_tdd: true AND test runner exists
│   └── STRICT TDD MODE → Follow RED-GREEN-REFACTOR cycle
│
├── IF strict_tdd: false OR no test runner
│   └── STANDARD MODE → use Step 4 below
│
```

### Hard Gate (Strict TDD Only)

If Strict TDD Mode is active:
- You MUST produce a **TDD Cycle Evidence** table in your apply-progress artifact
- Each task row MUST have: RED (test written first) → GREEN (implementation passes) → REFACTOR columns
- If you complete a task WITHOUT writing tests first, mark it as FAILED
- The verify phase WILL reject your work if the TDD Evidence table is missing

**There is no silent fallback.** If Strict TDD is active, you follow it or you report failure.

## Step 4: Implement Tasks

For each uncompleted task:
1. Write tests first (if Strict TDD) or after (Standard Mode)
2. Implement the solution following the design
3. Run tests to verify
4. Mark the task as `[x]` complete in tasks
5. Save apply-progress with merged state

### Chain Strategy Support

If `Chain strategy` is present in tasks:
- `stacked-to-main`: each PR targets previous PR's branch (or main after merge)
- `feature-branch-chain`: PR #1 targets feature/tracker branch; later PRs target previous PR branch. Never target main directly in child PRs.

## Step 5: Return Envelope

```markdown
**Status**: success | partial | blocked
**Summary**: what was implemented
**Tasks completed**: N of M
**TDD Mode**: strict | standard
**TDD Evidence**: (table if strict mode)
**Apply-Progress**: saved to sdd/{change-name}/apply-progress
**Next**: continue apply or sdd-verify
**Risks**: None | ...
**Skill Resolution**: injected | fallback-registry | fallback-path | none
```

## Anti-patterns

- ❌ Writing code without reading specs first
- ❌ Overwriting apply-progress instead of MERGE
- ❌ Silent fallback from Strict TDD to Standard
- ❌ Implementing tasks outside the assigned work-unit slice
- ❌ Skipping workload enforcement when forecast says High
