---
name: frontend-layout-implementer
description: 'Implement approved React/Next.js design specs using existing CSS Modules, Redux, TanStack, and Axios conventions. Route uninspected designs to intake and resolve product decisions before coding. Excludes unrelated stacks and styling systems.'
id: 'agents.skills.frontend-layout-implementer.skill'
title: 'Frontend Layout Implementer'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-layout-implementer'
tags:
    - 'agents/skill-package'
    - 'frontend/implementation'
    - 'frontend/layout'
parent: []
related:
    - '[[skills/design-screenshot-spec/references/product-behavior-review|Product Behavior Review]]'
    - '[[common/frontend-design-system-rules|Frontend Design System Rules]]'
    - '[[common/component-substitution-rules|Component Substitution Rules]]'
    - '[[skills/frontend-layout-implementer/references/implementation-rules|Implementation Rules]]'
    - '[[common/target-stack-policy|Target Stack Policy]]'
    - '[[common/approved-patterns|Approved Patterns]]'
    - '[[common/anti-patterns|Common Anti-Patterns]]'
    - '[[common/css-modules-specificity-rules|CSS Modules Specificity Rules]]'
    - '[[common/form-feedback-rules|Form Feedback Rules]]'
    - '[[common/navigation-ux-rules|Navigation UX Rules]]'
    - '[[common/data-visualization-rules|Data Visualization Rules]]'
    - '[[common/icon-quality-rules|Icon Quality Rules]]'
    - '[[common/mobile-responsive-rules|Mobile Responsive Rules]]'
    - '[[common/agent-loop-policy|Agent Loop Policy]]'
    - '[[common/verification-loop-rules|Verification Loop Rules]]'
    - '[[skills/loop-workflow-planner/SKILL|Loop Workflow Planner]]'
    - '[[skills/design-screenshot-spec/SKILL|Design Screenshot Spec]]'
    - '[[skills/frontend-design-director/SKILL|Frontend Design Director]]'
    - '[[skills/frontend-architecture-planner/SKILL|Frontend Architecture Planner]]'
    - '[[skills/frontend-linter-manager/SKILL|Frontend Linter Manager]]'
    - '[[skills/frontend-quality-reviewer/SKILL|Frontend Quality Reviewer]]'
    - '[[skills/frontend-visual-qa/SKILL|Frontend Visual QA]]'
    - '[[skills/project-context-adapter/SKILL|Project Context Adapter]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Frontend Layout Implementer

## Purpose

Implement a `Design Implementation Spec` or `Design Direction Contract` in a React or Next.js project while respecting existing CSS Modules, Redux, TanStack, Axios, architecture, styling, decomposition, UX gates, and verification conventions.

When the user asks to keep iterating until measurable visual, lint, build, or route acceptance criteria pass, implementation must follow a Loop Workflow Contract or hand off to `loop-workflow-planner` before editing.

## When To Use

- The user asks to build a screen, section, component, or static page from a `Design Implementation Spec`.
- The user supplies screenshot-derived design material and asks for code in the current supported frontend project.
- The implementation target is within React, Next.js, CSS Modules, Redux, TanStack, or Axios scope.

## When Not To Use

- The design intent has not been converted into a spec from supplied links or
  screenshots. Use `design-screenshot-spec` first, then resume requested code work.
- The user asks only for live design inspection, canvas edits, or whiteboard work.
- The project is outside the supported target stack unless the user explicitly changes scope.
- The task is unrelated to frontend rendering or layout.

## Required Context

1. Read `AGENTS.md`.
2. Read `common/target-stack-policy.md`.
3. Confirm the classified task is `frontend-layout`, `feature/development`, `bugfix`, `refactor`, or `optimization` for a rendered React or Next.js surface.
4. Read `common/approved-patterns.md` and relevant anti-pattern rules.
5. Read `common/css-modules-specificity-rules.md` for CSS Modules changes.
6. Read conditional UX rules only when the touched surface needs them: forms, navigation, data visualization, icons, or mobile responsive behavior.
7. Read `common/agent-loop-policy.md` and `common/verification-loop-rules.md` when measurable iteration or bounded retry is required.
8. Read relevant project overlays when present: stack, architecture, styling, verification, state, data-fetching, build, and workspace profiles.
9. Read the `Design Implementation Spec`, `Design Direction Contract`, and supplied visual references.
10. Read affected source files, styles, components, routes, and configs.
11. Read `references/implementation-rules.md` when present.

Do not read generated `dist/**` during normal runtime.

When shared UI or compatible component wrappers are in scope, read
`common/frontend-design-system-rules.md` and
`common/component-substitution-rules.md`. Apply purpose-specific naming from
`common/frontend-implementation-boundaries.md` to changed project-owned code.

## Tool Contract

- Use Project Context MCP when available; otherwise read `project/**` and source files directly.
- Use Design Spec MCP when available; otherwise use the supplied spec text or user-approved local artifact.
- Use Visual Reference MCP when available; otherwise use attached or local image files supplied by the user.
- Use `context7` for React, Next.js, Redux, TanStack, Axios, TypeScript, or build-tool docs when implementation depends on current behavior.
- Activate `openai_platform_docs` only when current OpenAI API or ChatGPT Apps SDK behavior affects the implementation.
- Use `mdn` for current HTML, CSS, Web API, accessibility, and compatibility facts.
- Use rendered visual QA only when screenshot comparison, viewport evidence, overflow checks, or visible state verification are in scope.
- Use Visual Diff MCP when available during final visual comparison.
- Route live design reads through `design-screenshot-spec` and reuse its evidence.
- If a named MCP is unavailable, report the missing capability before using a lower-confidence fallback.

## Workflow

1. Confirm the task is within the supported target stack.
2. Detect React/Next.js routing, CSS Modules ownership, Redux ownership, TanStack usage, Axios API adapter boundaries, and verification commands.
3. Map the spec to existing project components, layout primitives, tokens, assets, styles, and UX patterns.
4. Check component coverage and the spec's product decision register before
   editing. Use `skills/design-screenshot-spec/references/product-behavior-review.md`
   through the owning skill for unresolved design or behavior. Ask the user to
   resolve every needed product choice; implement only confirmed independent
   scope. Do not invent transitions, form opening/dismissal, persistence, hidden
   states, responsive choices, or animation defaults to complete the page.
5. Use `frontend-architecture-planner` before editing when route, state, data, form, build, workspace, or shared component ownership is unclear or material.
6. Use `loop-workflow-planner` before editing when the task requires bounded retry, independent review, loop memory, or measurable iteration beyond one implementation pass.
7. Plan component decomposition before editing.
8. Map structure as information before adding numbers, dividers, badges, labels, grids, metrics, or decorative sections.
9. Identify conditional UX gates: forms, navigation, data visualization, icon quality, and mobile responsiveness.
10. Identify CSS Modules ownership and selector risks before styling.
11. Implement the smallest scoped change that satisfies the spec, design direction, architecture handoff, and decomposition plan.
12. Keep UI state local unless existing React, Redux, or TanStack ownership requires otherwise.
13. Keep styles in CSS Modules by default.
14. Reuse existing Axios clients and API adapters for API-facing changes.
15. Do not add dependencies, global tokens, UI libraries, or new styling systems without explicit approval.
16. Preserve accessibility, semantic structure, keyboard/focus behavior, text wrapping, responsive behavior, and stable layout dimensions.
17. Use `frontend-linter-manager` after code-changing work when a lint command exists.
18. Run relevant project verification commands from `project/verification-profile.md`.
19. Run `frontend-visual-qa` only when the change needs rendered screenshot comparison, viewport evidence, overflow verification, or visible state verification.
20. Use `frontend-quality-reviewer` before final reporting when the user asks for review, the implementation has significant surface area, a loop contract requires independent review, or the plan requires a quality pass.

## Output Contract

Final response: return only facts that affect the user's understanding, confidence, or next action. Omit empty fields and workflow narration.

Report:

- implemented spec scope;
- affected React or Next.js surface;
- decomposition applied or why the touched component remained intentionally small;
- CSS Modules, Redux, TanStack, Axios, or project primitives reused;
- form, navigation, data, icon, and responsive gates considered or skipped as not applicable;
- loop contract followed or why no loop was needed;
- deviations from the design spec;
- lint and verification commands run;
- rendered visual QA result, skipped reason, or blocker.

## Domain Terms

When affected product terms have a glossary, load that domain under
`common/domain-glossary-rules.md`. Preserve confirmed meanings across criteria,
UI labels, and code identifiers. Do not silently resolve material ambiguity.

## Functional Acceptance

For behavior changes, verify the user outcome under
`common/verification-loop-rules.md`. A named browser-dependent functional
criterion permits a scoped browser check under
`common/rendered-visual-verification-policy.md` even without a visual change.
Keep visual QA routed separately; report unverified runtime behavior honestly.

## Validation Gates

- Implementation must follow inspected project conventions.
- The target must be within React, Next.js, CSS Modules, Redux, TanStack, or Axios scope.
- CSS Modules changes must have clear ownership and stable specificity.
- Structural devices must encode meaning instead of decoration.
- Form, navigation, data, icon, and mobile risks must be handled when present.
- Bounded iteration must have measurable criteria, attempt limit, and stop conditions.
- Source evidence and confirmed user decisions must cover the implemented slice;
  unresolved dependent behavior is blocked, not silently filled from conventions.
- No new package, styling system, global token, architecture layer, or UI library may appear without approval.
- Code-changing implementation must run lint when an existing lint command is available.

## Trigger Evals

Should trigger:

- "Implement this Design Implementation Spec in the current React page."
- "Build this approved design direction with the existing CSS Modules."

Should not trigger:

- "Write a visual direction before coding."
- "Compare the rendered page with the screenshot only."

## Reference Map

- `common/target-stack-policy.md`
- `skills/design-screenshot-spec/references/product-behavior-review.md`
- `common/approved-patterns.md`
- `common/anti-patterns.md`
- `common/css-modules-specificity-rules.md`
- `common/form-feedback-rules.md`
- `common/navigation-ux-rules.md`
- `common/data-visualization-rules.md`
- `common/icon-quality-rules.md`
- `common/mobile-responsive-rules.md`
- `common/agent-loop-policy.md`
- `common/verification-loop-rules.md`
- `skills/loop-workflow-planner/SKILL.md`
- `skills/frontend-architecture-planner/SKILL.md`
- `skills/frontend-linter-manager/SKILL.md`
- `skills/frontend-quality-reviewer/SKILL.md`
- `skills/frontend-visual-qa/SKILL.md`
