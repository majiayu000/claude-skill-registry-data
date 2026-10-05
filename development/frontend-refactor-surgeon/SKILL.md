---
name: frontend-refactor-surgeon
description: 'Perform bounded, behavior-preserving frontend refactors such as component extraction, file moves, prop or interface cleanup, state simplification, and TypeScript tightening. Excludes bugfixes, features, redesign, packages, and unapproved behavior changes.'
id: 'agents.skills.frontend-refactor-surgeon.skill'
title: 'Frontend Refactor Surgeon'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-refactor-surgeon'
tags:
    - 'agents/skill-package'
    - 'frontend/refactor'
    - 'workflow/refactor'
parent: []
related:
    - '[[common/frontend-design-system-rules|Frontend Design System Rules]]'
    - '[[common/component-substitution-rules|Component Substitution Rules]]'
    - '[[common/refactor-safety-rules|Refactor Safety Rules]]'
    - '[[common/approved-patterns|Approved Patterns]]'
    - '[[common/anti-patterns|Common Anti-Patterns]]'
    - '[[common/agent-loop-policy|Agent Loop Policy]]'
    - '[[common/verification-loop-rules|Verification Loop Rules]]'
    - '[[common/bounded-retry-rules|Bounded Retry Rules]]'
    - '[[common/typescript-discipline|TypeScript Discipline]]'
    - '[[common/state-ownership-rules|State Ownership Rules]]'
    - '[[skills/frontend-linter-manager/SKILL|Frontend Linter Manager]]'
    - '[[skills/frontend-visual-qa/SKILL|Frontend Visual QA]]'
    - '[[skills/frontend-quality-reviewer/SKILL|Frontend Quality Reviewer]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Frontend Refactor Surgeon

## Purpose

Refactor frontend code while preserving behavior, rendered output, and public contracts unless the user explicitly approves a behavior change.

Refactor verification may use a bounded loop for related failures, but the refactor must not expand into feature work or broad rewrite.

## When To Use

Use this skill when the user asks to simplify or reorganize frontend code, extract components, hooks, utilities, or styles, tighten TypeScript types, remove duplication within a clear frontend boundary, decompose mixed-responsibility components, or prepare code for a future change without adding the feature yet.

## When Not To Use

Do not use this skill for bugfix-first debugging, new feature implementation, design/spec work, visual QA only, broad rewrites without a boundary, backend refactors, package installation, or testing workflow creation.

Use `frontend-bugfix-debugger` when the primary goal is to fix a defect.

## Required Context

1. Read `AGENTS.md`.
2. Read `common/prompt-intent-routing-rules.md` when workflow level is unclear.
3. Read `common/refactor-safety-rules.md`.
4. Read `common/approved-patterns.md` for component decomposition rules.
5. Read `common/anti-patterns.md` and relevant anti-pattern templates when the refactor touches components.
6. Read `common/verification-loop-rules.md` and `common/bounded-retry-rules.md` when verification repair is in scope.
7. Read `common/typescript-discipline.md`.
8. Read relevant boundary docs such as `common/state-ownership-rules.md` when the refactor touches state.
9. Read project overlays and affected source files needed to define the behavior boundary.

When shared UI or compatible component wrappers are in scope, read
`common/frontend-design-system-rules.md` and
`common/component-substitution-rules.md`. Apply purpose-specific naming from
`common/frontend-implementation-boundaries.md` to changed project-owned code.

## Tool Contract

- May inspect affected source, styles, configs, and project overlays.
- May run existing lint, typecheck, build, or preview commands relevant to the refactor.
- May use Browser or Playwright MCP when rendered output must be checked.
- Activate `openai_platform_docs` only when current OpenAI API or ChatGPT Apps SDK behavior affects the preserved contract.
- Must not install packages, add testing workflows, change build tooling, add UI libraries, or migrate frameworks without explicit approval.
- Must not change production systems, secrets, or production data.

## Workflow

1. Define the refactor boundary and behavior contract.
2. Identify public APIs, rendered output, route behavior, state ownership, accessibility, and TypeScript contracts that must remain stable.
3. Identify whether the refactor requires decomposition.
4. Split the refactor into small mechanical steps.
5. Edit one boundary at a time.
6. Preserve project naming, folder, styling, and state conventions.
7. Do not create or preserve components that mix routing, data access, state orchestration, transformations, form logic, repeated markup, large JSX, and side effects in one file.
8. Do not hide missing decomposition behind `renderXxx`, `xxxRender`, nested array pipelines, component-body JSX preparation, oversized custom hooks, or unnecessary `useCallback`.
9. Run the smallest relevant verification after meaningful edits.
10. If verification fails because of the current refactor, fix related failures using bounded retry rules and keep the behavior contract unchanged.
11. Use `frontend-linter-manager` after code-changing work when a lint command exists.
12. Use `frontend-visual-qa` when rendered UI could have changed.
13. Use `frontend-quality-reviewer` when the refactor is standard or deep, involved retry, or the user asks for review.
14. Stop and ask before behavior change, architecture expansion, dependency changes, or broad rewrite.

## Output Contract

Final response: return only facts that affect the user's understanding, confidence, or next action. Omit empty fields and workflow narration.

```text
Refactor boundary:
Behavior preserved:
Decomposition applied:
Changes made:
Attempts:
Verification:
Rendered QA:
Deferred work:
Risks:
```

## Validation Gates

- The behavior boundary must be explicit before editing.
- Public contracts must remain stable unless approved.
- Refactor must not introduce feature work by default.
- Verification repair must not change behavior to make checks pass.
- Component decomposition rules must be applied regardless of framework, router, state layer, data layer, or styling system.
- Lint verification must run after code changes when a command exists.
- Rendered UI changes or risk must trigger visual QA when applicable.
- No testing workflow, UI library, package install, or framework migration may be introduced by default.

## Trigger Evals

Should trigger:

- "Extract this component while preserving its public behavior."
- "Simplify this state flow in bounded verified steps."

Should not trigger:

- "Fix this runtime bug from its reproduction."
- "Redesign this page."

## Reference Map

- `common/refactor-safety-rules.md`
- `common/approved-patterns.md`
- `common/anti-patterns.md`
- `common/verification-loop-rules.md`
- `common/bounded-retry-rules.md`
- `common/typescript-discipline.md`
- `common/state-ownership-rules.md`
- `project/verification-profile.md`
