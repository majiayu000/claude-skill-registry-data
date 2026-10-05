---
name: loop-workflow-planner
description: 'Define a platform-neutral bounded loop for standard or deep work using measurable acceptance criteria, verification, retry limits, independent review, memory, and stop conditions. Skip lookups, tiny edits, and one-off explanations.'
id: 'agents.skills.loop-workflow-planner.skill'
title: 'Loop Workflow Planner'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'loop-workflow-planner'
tags:
    - 'agents/skill-package'
    - 'agents/planning'
    - 'workflow/agent-loop'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/agent-loop-policy|Agent Loop Policy]]'
    - '[[common/stop-criteria-rules|Stop Criteria Rules]]'
    - '[[common/bounded-retry-rules|Bounded Retry Rules]]'
    - '[[common/verification-loop-rules|Verification Loop Rules]]'
    - '[[common/context-compaction-rules|Context Compaction Rules]]'
    - '[[common/independent-review-rules|Independent Review Rules]]'
    - '[[common/worktree-parallelism-rules|Worktree Parallelism Rules]]'
    - '[[templates/loop-workflow-contract|Loop Workflow Contract Template]]'
    - '[[templates/loop-memory|Loop Memory Template]]'
    - '[[skills/execution-plan-manager/SKILL|Execution Plan Manager]]'
    - '[[skills/frontend-quality-reviewer/SKILL|Frontend Quality Reviewer]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Loop Workflow Planner

## Purpose

Create a platform-neutral Loop Workflow Contract for standard or deep work that must iterate until measurable acceptance criteria pass.

This skill does not implement code. It defines objective, scope, verification, retry limits, stop conditions, independent review, and memory update rules so Codex, GPT-based agents, Claude, and generic coding agents can execute the same workflow without depending on Claude-only commands.

## When To Use

Use this skill when the task is `Standard Workflow` or `Deep Workflow` and one or more are true:

- the user asks to continue until lint, typecheck, build, visual QA, CI, or another measurable check passes;
- verification may fail and repair is in scope;
- a repeated failure already happened;
- a bugfix, CI repair, refactor, or UI implementation needs bounded retry;
- independent review should judge completion;
- the work may need resumable memory;
- multiple agents or worktrees are being considered.

## When Not To Use

Do not use for:

- Fast Lookup;
- one obvious typo or type error;
- tiny direct edits;
- pure explanation;
- design-only direction with no iterative verification;
- platform-specific `/goal`, `/loop`, or `/schedule` commands without a platform-neutral contract;
- unbounded autonomous work.

## Required Context

1. Read `AGENTS.md`.
2. Read `common/agent-loop-policy.md`.
3. Read `common/stop-criteria-rules.md`.
4. Read `common/bounded-retry-rules.md`.
5. Read `common/verification-loop-rules.md`.
6. Read `common/context-compaction-rules.md` when stop/resume or memory matters.
7. Read `common/independent-review-rules.md` when review is needed.
8. Read `common/worktree-parallelism-rules.md` only when parallel agents, branches, or worktrees are considered.
9. Read the current Goal Contract, Execution Plan, user request, or `project/active-goals.md` when present.
10. Read the active coverage map and target `S-###` slices when a durable plan exists.
11. Read `project/verification-profile.md` when verification commands matter.

Do not read unrelated skills or generated `dist/**` during normal runtime.

## Tool Contract

- May read project overlays and verification profiles.
- May write or update a durable loop contract only when the task is genuinely resumable or deep.
- May recommend host mappings for Claude, Codex, GitHub, or generic agents, but must not require host-specific commands.
- Must not implement source code.
- Must not run verification commands.
- Must not install packages, tools, MCP servers, UI libraries, or testing workflows.
- Must not create parallel worktrees or branches without explicit user approval and an ownership plan.

## Workflow

1. Confirm task scale. Stop if the task is Fast Lookup or lightweight without repeated failure.
2. Confirm or derive the objective from an existing goal, execution plan, or explicit user request.
3. Reuse the active Goal Contract `AC-###` criteria when present. Otherwise,
   convert vague completion language into measurable acceptance criteria without
   creating a competing set of criteria.
4. Reference the target `S-###` slices when a durable execution plan exists.
   Do not add, reorder, renumber, or mark slices from the loop contract.
5. Define allowed scope and out-of-scope changes.
6. Select loop type: one-pass verification, bounded retry, goal-based loop, or open exploration.
7. Set maximum attempts or turns.
8. Define verification commands, rendered checks, or manual evidence sources.
9. Define retry strategy and what must change after a failed attempt. Every
   durable retry record must name the affected `AC-###` and `S-###`.
10. Define stop and escalation conditions.
11. Decide whether independent review is required.
12. Decide whether loop memory is needed and where it belongs.
13. Decide whether parallel work is safe; default to no parallelism.
14. Produce a Loop Workflow Contract.
15. Hand off to the next smallest relevant skill.

## Output Contract

Final response: return only facts that affect the user's understanding, confidence, or next action. Omit empty fields and workflow narration.

Return or write:

```text
Loop Workflow Contract
Goal ID
Objective
Allowed Scope
Acceptance Criteria
Target Slices
Loop Type
Max Attempts Or Turns
Retry Strategy
Verification
Independent Review
Memory Update
Stop Conditions
Escalation Conditions
Final Evidence
Next Slice
Next Skill Or Next Step
```

When a Goal Contract exists, preserve its `AC-###` identifiers in the loop
contract, verification evidence, retry history, and final report.
When an Execution Plan exists, preserve its `S-###` identifiers in target scope,
retry history, memory, review handoff, and resume state.

Use `templates/loop-workflow-contract.md` for durable loop contracts.

## Validation Gates

- The loop must be bounded.
- Acceptance criteria must be measurable enough for an independent reviewer.
- Existing goal criterion identifiers must be reused instead of redefined.
- Existing slice identifiers must be referenced instead of redefined or mutated.
- Every durable retry attempt must identify its affected criteria and slices.
- Verification must rely on existing project commands or available rendered checks.
- Retry strategy must prevent repeating the same failed approach.
- Independent review must be defined when material risk exists.
- Memory updates must stay in local-only `project/**` files.
- The contract must be executable by Codex/GPT and Claude without requiring platform-specific loop commands.

## Trigger Evals

Should trigger:

- "Fix CI and keep going until it is green, but stop if it needs approval."
- "Repair this visual QA issue and rerun the rendered check until it passes."
- "Refactor this safely in iterations and verify after each slice."
- "Create a loop plan for this multi-step frontend task."
- "Use a goal loop, but keep it compatible with Codex and Claude."

Should not trigger:

- "Where is this component defined?"
- "Explain this function."
- "Fix this typo."
- "Change this button label."
- "Create a visual direction only."

## Reference Map

- `common/agent-loop-policy.md`
- `common/stop-criteria-rules.md`
- `common/bounded-retry-rules.md`
- `common/verification-loop-rules.md`
- `common/context-compaction-rules.md`
- `common/independent-review-rules.md`
- `common/worktree-parallelism-rules.md`
- `templates/loop-workflow-contract.md`
- `templates/loop-memory.md`
- `project/loop-memory.md` optional local-only memory file
