---
name: frontend-ui-engineering
description: Use when building or modifying a non-trivial user-facing interface where interaction semantics, keyboard or focus behavior, responsive behavior, design-system consistency, loading/error/empty states, or accessibility acceptance materially affects the outcome, or when the user explicitly asks for UI, accessibility, responsive, or interaction quality. Do not use for small label, text, class, or attribute edits, settled-plan execution, architecture or ownership decisions, test strategy, browser runtime evidence, or ordinary implementation.
---

# Frontend UI Engineering

Build user interfaces whose observable interaction, accessibility, responsive behavior, and project-specific visual conventions are deliberate. Keep ordinary UI edits lightweight and use this skill only when those concerns materially shape the work.

## First Decision

- Stay in the base flow for a small label, copy, class, attribute, or already-settled pattern edit whose behavior is clear.
- Use this skill for a non-trivial page, component, interaction, responsive layout, design-system application, or explicit accessibility/UI-quality request.
- Use `design-codebase` first when the unresolved question is ownership, component boundaries, interfaces, adapters, or dependency structure. Use `test-strategy` for test level, fixtures, mocks, timing, or acceptance-proof choices. Use a browser-testing owner only when live DOM, console, network, focus, or visual runtime evidence is required and that owner is available.
- Do not infer a framework, component library, state store, breakpoint set, browser matrix, or accessibility standard from examples. Read the project facts that can change the implementation.

## UI Pass

When this skill is active:

1. Read the affected page/component, its existing tests, one nearby project pattern, and the relevant design-system or styling conventions before editing.
2. State the user-visible behavior and the states that matter: initial, loading, success, empty, error, disabled, validation, permission, or unavailable states when they affect the request.
3. Prefer native semantic controls and the project's existing components, tokens, typography, spacing, and interaction patterns. Add composition, abstraction, or shared state only when the current behavior demonstrates that it earns the complexity.
4. Make interactive elements discoverable and operable by the supported input methods. Provide an accessible name, logical and visible focus, sensible keyboard behavior, and a meaningful relationship between labels, controls, status, and errors.
5. Make responsive and visual decisions against the project's actual content, supported viewport/zoom constraints, and design system. Do not apply fixed breakpoints, palettes, aesthetic recipes, or arbitrary component-size rules without project evidence.
6. Implement the smallest complete behavior and keep data, presentation, and state boundaries as simple as the current codebase allows.

## Observable Quality Baseline

Choose only the checks relevant to the affected behavior:

- Semantic elements express the control or structure; non-semantic elements are not used as buttons or links without a demonstrated need and complete equivalent behavior.
- Controls and form fields have clear visible or equivalent accessible names, associated labels, useful errors, and state that is not conveyed by color alone.
- Keyboard users can reach, operate, and leave the interaction; focus order and visibility remain sensible, and overlays restore focus appropriately when the project requires it.
- Loading, empty, error, validation, and dynamic status changes remain understandable and actionable rather than becoming blank or silent states.
- Content remains usable at the project's supported viewport and zoom conditions; responsive changes do not hide required content or operations.
- Existing design-system rules are reused. Do not introduce a generic visual style, arbitrary values, or framework-specific patterns merely because they appeared in the source material.

## Verification And Handoffs

- Select the smallest evidence that proves the changed claim: existing focused tests, static semantic inspection, project-provided accessibility checks, or an authorized runtime observation when the claim requires it.
- Do not automatically launch a browser, DevTools/MCP server, screen reader, accessibility CLI, development server, network request, dependency install, or external service. If the claim needs one, identify the gap and hand it to the applicable owner under its own authorization boundary.
- Test behavior through the most direct observable seam. `test-strategy` owns test design and acceptance proof; `review-and-finish` owns completion judgment.
- Report unsupported visual, browser, screen-reader, or runtime claims as gaps or `UNVERIFIED`; static source inspection is not live UI evidence.

## Boundaries

This skill does not replace:

- `design-codebase` for architecture, component ownership, interface, seam, or dependency-boundary decisions;
- `test-strategy` for test design, TDD, fixtures, mocks, timing, or regression proof;
- a browser-testing owner for live DOM, console, network, screenshot, focus, or performance evidence;
- `review-and-finish` for review feedback or readiness/done judgments;
- ordinary implementation for clear small UI edits;
- `finish-branch` for commit, push, PR, merge, discard, or cleanup actions.

Do not create durable design or context artifacts, alter project rules, or perform branch or external actions merely because this skill is active.
