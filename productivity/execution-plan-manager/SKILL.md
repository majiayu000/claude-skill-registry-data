---
name: execution-plan-manager
description: 'Create, resume, analyze, or converge standard and deep frontend execution plans with traceable slices, evidence, and stop/resume state. Skip lightweight isolated edits.'
id: 'agents.skills.execution-plan-manager.skill'
title: 'Execution Plan Manager'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'execution-plan-manager'
tags:
    - 'agents/skill-package'
    - 'agents/planning'
    - 'workflow/execution-plan'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[skills/goal-planner/SKILL|Goal Planner]]'
    - '[[skills/loop-workflow-planner/SKILL|Loop Workflow Planner]]'
    - '[[common/planning-rules|Planning Rules]]'
    - '[[common/planning-analysis-rules|Planning Analysis Rules]]'
    - '[[common/convergence-rules|Convergence Rules]]'
    - '[[common/execution-loops|Execution Loops]]'
    - '[[common/agent-loop-policy|Agent Loop Policy]]'
    - '[[common/token-budget-rules|Token Budget Rules]]'
    - '[[common/checkpoint-rules|Checkpoint Rules]]'
    - '[[templates/execution-plan|Execution Plan Template]]'
    - '[[templates/loop-workflow-contract|Loop Workflow Contract Template]]'
    - '[[common/prompt-intent-routing-rules|Prompt Intent Routing Rules]]'
    - '[[skills/project-context-adapter/SKILL|Project Context Adapter]]'
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules And Skill Author]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Execution Plan Manager

## Purpose

Create, resume, analyze, and converge execution plans for standard or deep frontend work after the goal is defined.

This skill prevents large tasks from becoming unbounded development sessions. It splits work into small verified slices, selects the minimum useful context budget, records stop/resume state when needed, and decides whether a slice needs a one-pass check, bounded retry loop, goal-based loop, independent review, or durable memory handoff.

## When To Use

Use this skill only after `AGENTS.md` and `common/prompt-intent-routing-rules.md` classify the task as `Standard Workflow` or `Deep Workflow`.

Use this skill when:

- a goal contract exists or the user goal is already explicit;
- the task needs more than one implementation slice;
- the task may need stop/resume state;
- the task has dependencies, blockers, or ordered phases;
- the task should be split before coding;
- the user asks to continue an existing large task;
- the agent needs to compare completed work with the plan;
- the task may require measurable iteration and should be handed to `loop-workflow-planner`.

## When Not To Use

Do not use this skill for `Lightweight Workflow` prompts, including one small bug, one obvious typo, one obvious type error, one small styling adjustment, one isolated component change, one direct file-scope edit, or one local refactor with clear boundaries.

Do not use this skill to implement code, install tools, scaffold projects, rewrite architecture, create tests, or perform visual QA.

If a lightweight task reveals hidden scope or repeated failure, escalate first using `common/prompt-intent-routing-rules.md`, then use this skill only if the escalated task is standard or deep.

## Required Context

1. Read `AGENTS.md`.
2. Read `common/prompt-intent-routing-rules.md` when task scale is not obvious.
3. Read `common/planning-rules.md`.
4. Read `common/planning-analysis-rules.md` only in `analyze` mode.
5. Read `common/convergence-rules.md` only in `converge` mode.
6. Read `common/checkpoint-rules.md` when durable stop/resume state is needed.
7. Read `common/agent-loop-policy.md` when the plan may need measurable iteration.
8. Confirm the workflow level is `Standard Workflow` or `Deep Workflow`.
9. Read the current goal contract from the response, user request, or `project/active-goals.md` when present and relevant.
10. Read only project overlays needed to slice the task safely, such as `project/stack-profile.md`, `project/architecture-map.md`, `project/styling-profile.md`, or `project/verification-profile.md`.
11. Read affected source files only when slicing, analysis, or convergence cannot be done safely without them.

## Tool Contract

- Use filesystem access only when a durable execution plan, progress log, loop contract, or stop/resume state must be written or updated. In `converge` mode, write only the append-only active-plan section allowed by `common/convergence-rules.md`.
- Do not use MCP installation checks from this skill.
- Do not use Browser, Playwright, Visual Diff, Figma, or design-tool MCP from this skill.
- Do not install packages or tools.
- Do not change application source files.
- Do not create testing workflows or testing files.

## Workflow

1. Confirm task scale. If lightweight, stop and route back to the direct skill without creating an execution plan.
2. Confirm goal. Use an existing Goal Contract when available. If no goal exists and the task is ambiguous, route to `goal-planner` first.
3. Choose one explicit mode:
   - `create`: make a new compact or durable plan;
   - `resume`: continue the existing plan without changing stable identifiers;
   - `analyze`: run the read-only pre-implementation checks in
     `common/planning-analysis-rules.md`;
   - `converge`: compare completed implementation and evidence with confirmed
     intent under `common/convergence-rules.md`.
4. In `analyze` mode, inspect the confirmed goal, plan, decisions, scope
   boundaries, and minimum affected context. Return deterministic findings and
   stop the implementation handoff for `blocking` or `high` severity. Do not
   edit files or remediate findings. Then finish this skill.
5. In `converge` mode, first reconcile any changed current request in `create`
   or `resume` mode. Otherwise compare only active intent with implementation
   and verification evidence, return stable `F-###` findings, and never change
   implementation files. For a durable plan, append one convergence pass only
   when actionable findings exist; with zero findings, preserve it byte-for-byte.
   Then finish this skill.
6. In `create` or `resume` mode, choose compact response-only planning for
   standard tasks that can finish in one or two slices, or durable planning for
   deep or resumable tasks.
7. Choose context budget: `Glance`, `Scoped`, or `Deep`.
8. Split into small independently verifiable slices.
   - For durable plans, assign stable zero-padded `S-###` identifiers.
   - Map each slice to one or more `AC-###` criteria.
   - Label a non-criterion slice `ENABLER` and name the approved downstream
     slices it unlocks.
   - Do not renumber or reuse slice identifiers after execution begins.
   - For feature slices, record Scenario, blocked_by, and Demonstrates under
     `common/planning-rules.md`; carry them through resume and analyze.
9. Add verification per slice using the smallest relevant check already available in the project or active skill.
10. Build the coverage map for durable plans.

    - Map every active `AC-###` to at least one `S-###` and one verification source.
    - Use only `planned`, `in-progress`, `verified`, `blocked`, or `superseded`.
    - Do not treat a completed slice as verification evidence.
    - Keep `ENABLER` slices linked through their downstream dependencies instead
      of using them as criterion coverage.

11. Decide whether a loop contract is needed. Use `loop-workflow-planner` when a slice must repeat until measurable acceptance criteria pass, when verification failure repair is in scope, when repeated failure already happened, when independent review should judge completion, or when loop memory is needed.
12. Add stop/resume state for durable plans, including current phase, last completed slice, next exact step, files to inspect next, checks to run next, loop contract or retry limit when relevant, blockers, and risks.
13. Hand off to the smallest relevant skill. Route measurable iteration to `loop-workflow-planner` before implementation.

## Output Contract

Final response: return only facts that affect the user's understanding, confidence, or next action. Omit empty fields and workflow narration.

Return or write an Execution Plan with:

```text
Goal
Done When
Workflow Level
Context Budget
Current Phase
Task Slices
Allowed Files Or Surfaces
Tools Allowed
Verification Per Slice
Coverage
Loop Needed
Loop Handoff
Blockers
Risks
Stop Point
Next Skill Or Next Step
```

Durable task slices use `S-### [AC-###]`. A justified enabling slice uses
`S-### [ENABLER -> S-###]`. Compact response-only plans may omit identifiers
only when they contain at most two direct slices and need no resume state.
Durable coverage maps reference criterion and slice identifiers, verification
evidence, and one canonical coverage state without duplicating criterion prose.
An append-only convergence review of unrequested work may use `S-### [F-###]`
under `common/convergence-rules.md`; it never counts as criterion coverage.

For durable plans, write or update:

```text
project/active-plan.md
project/progress-log.md
project/decision-log.md
project/loop-memory.md when loop memory is required
```

only when the task is genuinely multi-step, iterative, or resumable.

In `analyze` mode, return only:

```text
Analysis Mode: read-only
Plan Readiness: ready | ready-with-risk | blocked
Findings: PA-### | Category | Severity | Source | Evidence | Recommendation
Finding Summary
Implementation Handoff: proceed | stop
```

Limit the table to 20 rows and aggregate the remainder. Do not write analysis
results into the durable plan or application files.

In `converge` mode, return only:

```text
Convergence Status: aligned | gaps-found | intent-reconciliation-required
Findings: F-### | Type | Severity | Source | Evidence | Remaining Work
Plan Update: unchanged | appended Convergence Pass N
Next Step
```

For response-only work, report findings without creating a plan file. For
durable work, add new slices only through the append-only convergence contract.

## Validation Gates

Before finishing, verify:

- the task was not a lightweight prompt;
- a goal exists or the task was routed to `goal-planner`;
- exactly one plan mode was selected;
- `analyze` mode made no writes, used stable findings, checked every required
  analysis category, and stopped handoff for blocking or high findings;
- `converge` mode used current intent, cited evidence, made no implementation
  changes, preserved finding identity, and did not replace independent review;
- zero convergence findings left the durable plan byte-for-byte unchanged;
- actionable durable convergence appended one pass, allocated identifiers after
  the current maximum, and preserved all prior plan content;
- `create` and `resume` slices are small and independently verifiable;
- durable `create` and `resume` slices have stable identifiers and map to criteria or justified
  downstream work;
- every active durable criterion has slice and verification coverage;
- `verified` coverage has actual evidence and `blocked` coverage names the
  blocker;
- context budget is explicit;
- loop handoff is explicit when bounded retry or measurable iteration is required;
- persistent files were created only for durable standard or deep work;
- no source files were changed;
- no tools or packages were installed;
- no testing workflow was introduced;
- next step is precise enough for another agent run to resume.

## Trigger Evals

Should trigger:

- "Break this dashboard implementation into small steps."
- "Continue the previous big frontend task and tell me exactly where to resume."
- "Create an execution plan for this redesign after the goal is clear."
- "We need to implement this feature in slices without losing progress."
- "Plan the task and decide whether it needs a bounded loop."
- "Analyze this plan for gaps before implementation without changing it."
- "Compare the finished implementation with the active plan and append only the remaining work."

Should not trigger:

- "Fix this TypeScript error."
- "Change this button color."
- "Fix the broken margin in this component."
- "Rename this prop in one file."
- "Define the goal first."
- "Run visual QA on this page."

## Reference Map

- `AGENTS.md` - canonical policy, routing, tool rules, and documentation rules.
- `common/prompt-intent-routing-rules.md` - workflow weight selection and escalation/de-escalation rules.
- `common/planning-rules.md` - context budget and task slice rules.
- `common/planning-analysis-rules.md` - read-only pre-implementation plan checks and finding contract.
- `common/convergence-rules.md` - post-implementation comparison and append-only plan update contract.
- `common/checkpoint-rules.md` - stop/resume state rules.
- `common/agent-loop-policy.md` - bounded loop policy.
- `templates/execution-plan.md` - durable execution plan template.
- `templates/loop-workflow-contract.md` - durable loop contract template.
- `skills/goal-planner/SKILL.md` - goal contract producer for standard or deep work.
- `skills/loop-workflow-planner/SKILL.md` - loop contract producer for measurable iteration.
- `project/active-plan.md` - optional local-only durable execution plan for deep or resumable work.
- `project/progress-log.md` - optional local-only progress log.
- `project/decision-log.md` - optional local-only decision log.
- `project/loop-memory.md` - optional local-only loop memory.

## Delegated Slice Handoff

When existing routing justifies delegation, use `common/subagent-handoff-rules.md`
and `templates/subagent-task.md` to export the current slice, exact interfaces,
global constraints and remaining attempt budget. Keep the canonical plan and
stable identifiers authoritative. Task packets and reports are plan-scoped
local artifacts; they do not create a second plan. Lightweight work bypasses
this handoff as it bypasses durable planning.
