---
name: frontend-architecture-planner
description: 'Plan architecture and ownership for standard or deep React/Next.js work across routing, state, data, styling, forms, builds, migrations, and implementation handoff. Skip micro-fixes and unrelated stacks.'
id: 'agents.skills.frontend-architecture-planner.skill'
title: 'Frontend Architecture Planner'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-architecture-planner'
tags:
    - 'agents/skill-package'
    - 'agents/architecture'
    - 'workflow/frontend-architecture'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/target-stack-policy|Target Stack Policy]]'
    - '[[common/prompt-intent-routing-rules|Prompt Intent Routing Rules]]'
    - '[[common/framework-adaptation-policy|Framework Adaptation Policy]]'
    - '[[common/state-ownership-rules|State Ownership Rules]]'
    - '[[common/routing-boundary-rules|Routing Boundary Rules]]'
    - '[[common/data-fetching-boundary-rules|Data Fetching Boundary Rules]]'
    - '[[common/form-boundary-rules|Form Boundary Rules]]'
    - '[[common/build-tool-boundary-rules|Build Tool Boundary Rules]]'
    - '[[common/frontend-integration-boundaries|Frontend Integration Boundaries]]'
    - '[[skills/goal-planner/SKILL|Goal Planner]]'
    - '[[skills/execution-plan-manager/SKILL|Execution Plan Manager]]'
    - '[[skills/frontend-layout-implementer/SKILL|Frontend Layout Implementer]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Frontend Architecture Planner

## Purpose

Plan frontend architecture decisions for React and Next.js projects when a task affects structure, ownership, routing, React state, Redux state, TanStack remote state, Axios data access, CSS Modules styling, form behavior, build/workspace shape, or long-lived conventions.

This skill creates an architecture decision and implementation handoff. It does not implement code by default.

## When To Use

Use this skill after prompt intent routing when the task is `Standard Workflow` or `Deep Workflow`, the project is within the target stack, and architecture decisions matter.

Use this skill when the user asks to:

- plan a new React or Next.js feature that touches multiple modules;
- design a route, screen group, or application section;
- define component boundaries before implementation;
- decide where React, Redux, or TanStack state should live;
- decide how Axios or TanStack data fetching should fit the existing project;
- plan routing changes;
- plan form ownership and validation boundaries;
- plan a frontend refactor before editing code;
- assess architecture risk before implementation;
- define a greenfield React or Next.js architecture before scaffolding.

## When Not To Use

Do not use this skill for:

- one small bug;
- one obvious type error;
- one small styling adjustment;
- one direct file-scope edit;
- unrelated frontend frameworks or app stacks;
- purely visual direction without architecture impact;
- rendered visual QA;
- UI component library selection;
- backend, database, ORM, migrations, or infrastructure work unless the user explicitly changes the scope.

## Required Context

1. Read `AGENTS.md`.
2. Read `common/target-stack-policy.md`.
3. Read `common/prompt-intent-routing-rules.md` when workflow level is unclear.
4. Read the compact goal contract or execution plan when present.
5. Read only relevant boundary rules for the task.
6. Read relevant project overlays when present: stack, architecture, styling, verification, docs, build, workspace, state, and data-fetching profiles.
7. Read affected source files only when architectural boundaries cannot be planned from overlays.
8. Do not read generated `dist/**` during normal runtime.

## Tool Contract

- May use filesystem access to inspect relevant project overlays and affected source files.
- May use `context7` for React, Next.js, Redux, TanStack, Axios, TypeScript, or build-tool documentation when architecture depends on current behavior.
- Activate `openai_platform_docs` only when current OpenAI API or ChatGPT Apps SDK behavior affects the architecture.
- May use MDN for platform constraints that affect architecture, such as forms, browser APIs, accessibility, and CSS behavior.
- Must not install packages, UI libraries, state libraries, data libraries, form libraries, or MCP servers.
- Must not change project source files, configs, package manager files, or build tooling.
- Must not interact with production systems, secrets, or production data.

## Workflow

1. Confirm target stack scope. If the project is outside React, Next.js, CSS Modules, Redux, TanStack, or Axios scope, report unsupported scope.
2. If the prompt is lightweight and no architecture boundary is affected, stop and route to the direct skill.
3. State the architectural question.
4. Inspect current conventions: React/Next.js router, folder/module structure, component ownership, CSS Modules, Redux ownership, TanStack ownership, Axios API layer, form conventions, build/workspace shape, and verification commands.
5. Define only relevant boundaries: route/page, feature/module, shared vs local component, React local state, Redux object state, TanStack remote state, Axios adapter, form state, CSS Modules styling, accessibility, build/workspace, and verification.
6. Choose the smallest architecture that satisfies the goal.
7. Require explicit approval for package installation, framework migration, package manager changes, new state/data/form/styling libraries, global architecture layers, build tooling changes, large refactors, destructive operations, or production access.
8. Create the architecture handoff without editing source files.
9. Define verification strategy using existing project checks and rendered verification where relevant.
10. Hand off to `execution-plan-manager` or the relevant implementation skill.

## Output Contract

Final response: return only facts that affect the user's understanding, confidence, or next action. Omit empty fields and workflow narration.

Return or write a Frontend Architecture Plan with:

```text
Goal
Workflow Level
Target Stack Scope
Architecture Question
Current Project Conventions
Proposed Boundaries
Files Or Surfaces Likely To Change
React State Ownership
Redux Boundary
TanStack Boundary
Axios Boundary
Routing Boundary
Form Boundary
CSS Modules Boundary
Build Or Workspace Boundary
Approval Gates
Implementation Slices
Verification Strategy
Risks
Rejected Alternatives
Next Skill Or Next Step
```

Omit irrelevant sections rather than filling them with generic text.

## Unresolved Experimental Questions

If a material UI or state choice remains unresolved after targeted source and
documentation inspection, hand off one bounded question to
`frontend-prototype-explorer`. Keep this planning skill read-only. Return the
observed decision and its limitations to the existing plan or decision log.

## Validation Gates

- The task actually needed architecture planning.
- The plan is inside the supported target stack or clearly reports unsupported scope.
- The plan follows current project conventions where known.
- Every proposed new boundary has a reason.
- No package, UI library, or MCP install was proposed as default.
- Approval gates are explicit.
- No source files, configs, or package files were changed by this skill.

## Trigger Evals

Should trigger:

- "Plan the frontend architecture for this React analytics section."
- "Where should this feature live in the current Next.js project?"
- "Design the route and Redux/TanStack boundaries before implementation."
- "Plan a safe frontend refactor for this module."
- "Create the architecture plan for a greenfield Next.js app, but do not scaffold yet."

Should not trigger:

- "Fix this TypeScript error."
- "Change this button color."
- "Make this page look less generic."
- "Run visual QA."
- "Install shadcn."

## Reference Map

- `AGENTS.md`.
- `common/target-stack-policy.md`.
- `common/prompt-intent-routing-rules.md`.
- `common/framework-adaptation-policy.md`.
- `common/state-ownership-rules.md`.
- `common/routing-boundary-rules.md`.
- `common/data-fetching-boundary-rules.md`.
- `common/form-boundary-rules.md`.
- `common/build-tool-boundary-rules.md`.
- `common/frontend-integration-boundaries.md`.
- `skills/goal-planner/SKILL.md`.
- `skills/execution-plan-manager/SKILL.md`.
