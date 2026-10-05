---
name: goal-planner
description: 'Define user goal, scope, constraints, and done criteria before standard or deep frontend work. Skip micro-fixes, obvious type errors, tiny styling changes, and isolated direct edits.'
id: 'agents.skills.goal-planner.skill'
title: 'Goal Planner'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'goal-planner'
tags:
    - 'agents/skill-package'
    - 'agents/planning'
    - 'workflow/goal-contract'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/agent-operating-model|Agent Operating Model]]'
    - '[[common/goal-contract|Goal Contract]]'
    - '[[common/prompt-intent-routing-rules|Prompt Intent Routing Rules]]'
    - '[[templates/goal-contract|Goal Contract Template]]'
    - '[[skills/project-context-adapter/SKILL|Project Context Adapter]]'
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules And Skill Author]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Goal Planner

## Purpose

Create a clear goal contract for standard or deep frontend work before implementation begins.

This skill exists to prevent ambiguous or large requests from turning into unfocused coding. It defines what the user wants, what is in scope, what is out of scope, which constraints apply, and what observable conditions mean the task is done.

## When To Use

Use this skill only after `AGENTS.md` and `common/prompt-intent-routing-rules.md` classify the task as `Standard Workflow` or `Deep Workflow`.

Use this skill when:

- the user asks for a multi-file feature;
- the user asks for a new screen, flow, or frontend capability;
- the user asks for architecture, greenfield project creation, or broad redesign;
- the request is ambiguous enough that implementation would require guessing the goal;
- the task needs a compact goal before execution planning;
- the task needs a durable goal contract because work may span multiple slices.

## When Not To Use

Do not use this skill for `Lightweight Workflow` prompts, including:

- one small bug;
- one obvious typo;
- one obvious type error;
- one small styling adjustment;
- one isolated component change;
- one direct file-scope edit;
- one local refactor with clear boundaries.

Do not use this skill to implement code, install tools, scaffold projects, rewrite architecture, or perform visual QA.

If a lightweight task reveals hidden scope, escalate first using `common/prompt-intent-routing-rules.md`, then use this skill only if the escalated task is standard or deep.

## Required Context

1. Read `AGENTS.md`.
2. Read `common/prompt-intent-routing-rules.md` when task scale is not obvious.
3. Read `common/goal-contract.md`.
4. Confirm the workflow level is `Standard Workflow` or `Deep Workflow`.
5. Read only project overlays that are needed to understand the goal boundary, such as `project/stack-profile.md`, `project/architecture-map.md`, or `project/design-reference-profile.md`.
6. Read affected source files only when the goal cannot be stated without them.

## Tool Contract

- Use filesystem access only when a durable goal contract must be written or an existing one must be updated.
- Do not use MCP installation checks from this skill.
- Do not use Browser, Playwright, Visual Diff, Figma, or design-tool MCP from this skill.
- Do not install packages or tools.
- Do not change application source files.

## Workflow

1. Confirm task scale.
   - If the task is lightweight, stop and route back to the direct skill without creating a goal contract.
   - If the task is standard or deep, continue.

2. Extract the user-facing goal.
   - Describe the desired outcome in product or user terms, not only technical activity.
   - Preserve explicit user constraints.
   - Do not invent business requirements.

3. Define scope.
   - Name what is included.
   - Name what is explicitly out of scope.
   - Identify whether this is existing-project work, greenfield work, design work, architecture work, bugfix work, or review work.

4. Define constraints.
   Include relevant constraints such as:
   - no package installation without approval;
   - no new styling system without approval;
   - no architecture layer without approval;
   - no production systems or production data;
   - follow existing project conventions;
   - keep host-project facts in `project/**`;
   - keep reusable instructions in English.

5. Resolve material ambiguity when needed.
   - Scan only for choices that change scope, critical interaction states,
     data or state ownership, responsive or accessibility behavior, external
     integration or security, or verification.
   - Use the current request, confirmed decisions, host instructions, and
     verified project evidence before asking.
   - Rank candidates by impact and uncertainty, then ask exactly one question
     at a time and no more than three in one goal-definition pass.
   - Prefer mutually exclusive choices or a constrained short answer. Recommend
     an option only when evidence supports it.
   - Stop when material ambiguity is resolved, the user asks to proceed, or the
     limit is reached.
   - If the limit is reached with a material blocker unresolved, record the
     blocker instead of silently guessing.
   - Apply each answer immediately to Scope, Out Of Scope, Constraints, or Done
     When. Keep only a compact Clarifications record for durable goals.
   - Do not ask the user to repeat known information, confirm a verifiable fact,
     choose low-impact styling, or decide safe plan-level implementation detail.

6. Define Done When.
   - Done criteria must be observable outcomes, not implementation activity.
   - For a durable goal, assign stable zero-padded identifiers such as `AC-001`.
   - Do not renumber or reuse durable criterion identifiers after execution begins.
   - Use only criteria relevant to the task.

7. Choose output mode.
   - For standard tasks, output a compact goal contract in the response unless a durable file is genuinely useful.
   - For deep tasks, create or update `project/active-goals.md` when the environment and user-approved workflow allow local file writes.

8. Hand off.
   - For multi-step work, hand off to `execution-plan-manager` when available.
   - For direct standard work, hand off to the relevant frontend skill with the compact goal contract.

## Output Contract

Final response: return only facts that affect the user's understanding, confidence, or next action. Omit empty fields and workflow narration.

Return or write a Goal Contract with:

```text
Goal ID
User Goal
Product Intent
Scope
Out Of Scope
Constraints
Clarifications
Done When
Workflow Level
Current Status
Next Skill Or Next Step
```

Omit Clarifications when no material question was asked. For durable goals,
format Done When as `AC-###` criteria. For compact
response-only contracts, omit `Goal ID` and criterion identifiers only when no
durable tracking, resume state, or multi-slice traceability is needed.

## Domain Terms

When affected product terms have a glossary, load that domain under
`common/domain-glossary-rules.md`. Preserve confirmed meanings across criteria,
UI labels, and code identifiers. Do not silently resolve material ambiguity.

## Validation Gates

Before finishing, verify:

- the task was not a lightweight prompt;
- the goal is stated in user-outcome terms;
- scope and out-of-scope are explicit;
- constraints are not generic filler;
- clarification asks at most three material questions, one at a time, and does
  not repeat known or verifiable information;
- accepted answers are integrated into the goal instead of remaining only in a
  question log;
- Done When is observable;
- durable criteria have unique, stable `AC-###` identifiers;
- no source files were changed;
- no tools or packages were installed;
- persistent project files were created only for genuinely multi-step or resumable work.

## Trigger Evals

Should trigger:

- "Build a new dashboard from this spec and connect it to the existing route."
- "Plan the frontend architecture for a new analytics section."
- "Create a new project structure for this product idea, but do not scaffold yet."
- "This is a big redesign; define the goal and constraints before implementation."
- "Clarify only the decisions that would materially change this checkout flow."

Should not trigger:

- "Fix this TypeScript error."
- "Change this button color."
- "Fix the broken margin in this component."
- "Rename this prop in one file."
- "Run visual QA on this implemented page."
- "Pick any reasonable spacing and continue."

## Reference Map

- `AGENTS.md` - canonical policy, routing, tool rules, and documentation rules.
- `common/prompt-intent-routing-rules.md` - workflow weight selection and escalation/de-escalation rules.
- `common/goal-contract.md` - reusable goal contract rules.
- `templates/goal-contract.md` - durable goal contract template.
- `project/active-goals.md` - optional local-only durable goal contract for deep work.
