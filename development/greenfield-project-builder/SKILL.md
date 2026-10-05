---
name: greenfield-project-builder
description: 'Plan a new frontend project or first vertical slice from a product idea, with approval gates before scaffolding. Excludes existing-project micro-fixes, automatic scaffolds, package installation, UI libraries, and test setup.'
id: 'agents.skills.greenfield-project-builder.skill'
title: 'Greenfield Project Builder'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'greenfield-project-builder'
tags:
    - 'agents/skill-package'
    - 'agents/greenfield'
    - 'workflow/frontend-greenfield'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/prompt-intent-routing-rules|Prompt Intent Routing Rules]]'
    - '[[common/framework-adaptation-policy|Framework Adaptation Policy]]'
    - '[[common/build-tool-boundary-rules|Build Tool Boundary Rules]]'
    - '[[common/frontend-integration-boundaries|Frontend Integration Boundaries]]'
    - '[[skills/goal-planner/SKILL|Goal Planner]]'
    - '[[skills/execution-plan-manager/SKILL|Execution Plan Manager]]'
    - '[[skills/frontend-architecture-planner/SKILL|Frontend Architecture Planner]]'
    - '[[skills/mcp-toolchain-manager/SKILL|MCP Toolchain Manager]]'
    - '[[skills/project-onboarding-adapter/SKILL|Project Onboarding Adapter]]'
    - '[[skills/project-context-adapter/SKILL|Project Context Adapter]]'
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules And Skill Author]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Greenfield Project Builder

## Purpose

Plan and execute the first safe steps of a new frontend project without turning a vague product idea into uncontrolled scaffolding.

This skill converts a product idea into a minimal frontend project plan, explicit stack assumptions, approval gates, first vertical slice, and onboarding handoff. It must not scaffold, install packages, or create application files unless the user explicitly approves the exact action.

## When To Use

Use this skill only for `Deep Workflow` tasks.

Use this skill when the user asks to:

- start a new frontend project;
- plan a new frontend app from a product idea;
- create a project structure before scaffolding;
- define the first vertical slice of a new app;
- choose an intended frontend stack before project creation;
- prepare onboarding overlays for an empty or new project;
- turn a broad product concept into a small frontend implementation path.

## When Not To Use

Do not use this skill for:

- existing-project bugfixes;
- one route or component in an existing project;
- purely visual redesign of an existing screen;
- refactoring existing code;
- UI component library setup;
- testing workflows;
- backend, database, ORM, migrations, infrastructure, or production systems;
- package installation by default;
- automatic scaffolding without approval.

Do not use this skill when `frontend-architecture-planner` is enough for an existing project.

## Required Context

1. Read `AGENTS.md`.
2. Read `common/prompt-intent-routing-rules.md`.
3. Confirm the task is `Deep Workflow`.
4. Read `common/framework-adaptation-policy.md` and
   `common/build-tool-boundary-rules.md`.
5. Read the compact goal contract or `project/active-goals.md` when present.
6. Read the compact execution plan or `project/active-plan.md` when present.
7. Read existing project overlays only when this is a new app inside a larger existing workspace:
   - `project/stack-profile.md`;
   - `project/architecture-map.md`;
   - `project/build-profile.md` when present;
   - `project/workspace-profile.md` when present;
   - `project/verification-profile.md` when present.

## Tool Contract

- May inspect the repository root and selected workspace files to determine whether the target is empty, new, or inside an existing workspace.
- Activate `openai_platform_docs` only when the planned product uses OpenAI APIs, ChatGPT Apps SDK, or Codex integration behavior.
- May write local-only `project/**` overlays after approval or during approved onboarding.
- May create a host-root `AGENTS.md` pointer only through `project-onboarding-adapter` rules.
- May propose scaffold commands, but must not run them without explicit approval.
- Must not install packages without explicit approval.
- Must not create app source files, framework configs, package manifests, routes, components, styles, tests, or build scripts without explicit approval.
- Must not introduce UI component libraries or testing workflows.
- Must not access production systems, secrets, or production data.

## Workflow

1. Confirm greenfield status.
   - New standalone project.
   - Empty repository.
   - New app inside existing workspace.
   - Existing project that actually needs architecture planning instead.

2. Define the product goal.
   Route to `goal-planner` first if the product goal is unclear.

3. Define the first vertical slice.
   The first slice should include one user-visible path through the product, not a full architecture.

4. Define intended stack assumptions.
   Include only what is known or explicitly approved:
   - framework;
   - language;
   - routing model;
   - styling approach;
   - package manager;
   - build tool;
   - deployment target if relevant;
   - verification command expectations.

5. Define non-goals.
   Keep backend, database, auth, payments, analytics, UI libraries, tests, and infrastructure out of scope unless explicitly requested and approved.

6. Create a minimal architecture plan.
   Use `frontend-architecture-planner` when route/state/data/styling/build boundaries require deeper planning.

7. Define approval gates.
   Require explicit approval for:
   - scaffold commands;
   - package installation;
   - package manager choice or change;
   - framework choice or change;
   - UI component library;
   - state/data/form/styling libraries;
   - testing setup;
   - build tooling;
   - repository structure changes;
   - destructive file operations.

8. Create onboarding handoff.
   Use `project-onboarding-adapter` to create only the host-root pointer and local-only `project/**` overlays until the user approves actual project scaffolding.

9. Create execution plan.
   Use `execution-plan-manager` for slices after the greenfield plan is accepted.

10. Stop before scaffold unless approved.
    If approval is missing, return a plan and exact approval request instead of creating files.

## Output Contract

Final response: return only facts that affect the user's understanding, confidence, or next action. Omit empty fields and workflow narration.

Return or write a Greenfield Project Plan with:

```text
Product Goal
Workflow Level
Greenfield Status
First Vertical Slice
Intended Stack Assumptions
Non-Goals
Minimal Architecture
Files Or Surfaces To Create After Approval
Approval Gates
Onboarding Overlay Plan
Implementation Slices
Verification Strategy
Risks
Open Questions
Next Approval Request Or Next Step
```

Omit irrelevant sections rather than filling them with generic text.

## Validation Gates

Before finishing, verify:

- the task is genuinely greenfield or empty-project work;
- the first vertical slice is smaller than the whole product;
- no scaffold was run without explicit approval;
- no package was installed without explicit approval;
- no UI component library was introduced;
- no testing workflow was introduced;
- no application source/config/package/build files were created without explicit approval;
- host-project facts stay in `project/**`;
- next approval request is precise if action is blocked.

## Trigger Evals

Should trigger:

- "Start a new frontend project for this product idea."
- "Plan the first version of a new Next app, but do not scaffold yet."
- "Create a greenfield frontend plan and tell me what you need approval for."
- "This repo is empty; prepare the frontend project structure safely."
- "Define the first vertical slice before creating the app."

Should not trigger:

- "Fix this TypeScript error."
- "Add a card to this existing dashboard."
- "Make this existing page look better."
- "Plan the architecture of this existing module."
- "Install shadcn."
- "Create tests."

## Reference Map

- `AGENTS.md` - canonical policy, routing, tool rules, and documentation rules.
- `common/prompt-intent-routing-rules.md` - workflow weight selection and escalation rules.
- `common/framework-adaptation-policy.md` - intended stack adaptation rules.
- `common/build-tool-boundary-rules.md` - build and workspace approval gates.
- `common/frontend-integration-boundaries.md` - frontend integration scope limits.
- `skills/goal-planner/SKILL.md` - product goal contract.
- `skills/execution-plan-manager/SKILL.md` - task slicing and stop/resume planning.
- `skills/frontend-architecture-planner/SKILL.md` - architecture boundary planning.
- `skills/project-onboarding-adapter/SKILL.md` - safe host-root pointer and local-only overlay creation.
- `project/stack-profile.md` - local-only intended or detected stack facts.
- `project/architecture-map.md` - local-only intended or detected architecture facts.
- `project/verification-profile.md` - local-only verification command facts.
