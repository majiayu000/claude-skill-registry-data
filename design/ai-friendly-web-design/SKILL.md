---
name: ai-friendly-web-design
description: Build, review, and refactor web interfaces that are easy for humans, screen readers, browser automation, Playwright tests, and AI agents to understand and operate. Use for UI components, forms, frontend features, semantic HTML, ARIA, stable locators, URL state, accessibility reviews, and agent-friendly web design.
---

# AI-Friendly Web Design

## Purpose

Use this skill to make web interfaces easier to discover, operate, test, and review across human users, assistive technology, browser automation, and AI agents.

## When To Use

Use this skill when the task involves any of the following:

- Designing a new UI flow, screen, component, or form
- Implementing or refactoring frontend UI
- Reviewing existing UI for accessibility, automation, or operability issues
- Writing Playwright or browser automation tests
- Deciding semantic HTML, ARIA, locator, or URL state patterns

## Task Modes

Choose one primary mode before acting.

### 1. Design New UI

- List the core user tasks before proposing components.
- Define the UI contract in user-facing terms: actions, fields, states, and outcomes.
- Cover loading, error, empty, and success states explicitly.
- Decide which state should be reproducible through the URL.
- Mark which critical controls need stable locators.

### 2. Implement UI

- Prefer native HTML elements before custom widgets.
- Add ARIA only when native semantics are not enough.
- Ensure every critical control has an accessible name.
- Keep critical state readable as visible or programmatically associated text.
- Add stable locator hooks only for critical actions, fields, and status.

### 3. Review Existing UI

- Output findings as High, Medium, and Low severity.
- Prefer the display format `🔴 High`, `🟡 Medium`, and `🟢 Low` when the output surface supports emoji.
- Explain how each issue affects accessibility, automation, or agent operability.
- Prioritize blockers on critical user flows.
- Give concrete fixes instead of abstract advice.
- If a suggested fix would change hover, click, close, focus, expand, or layout behavior, present it as a behavior-change proposal requiring confirmation rather than a direct recommendation.
- Avoid unrelated redesign or architecture churn.

### 4. Refactor Existing UI

- Prefer the smallest patch that fixes operability.
- Preserve the current visual design unless the user asked for redesign.
- Preserve existing interaction paths and visible layout by default, including hover, click, outside-click-close, blank-area-close, Esc-close, expand/collapse, and focus return, unless the user explicitly approves a behavior change.
- Preserve the existing design system and component boundaries where practical.
- Fix the parts that break semantics, state clarity, or stable interaction.
- Do not use this work as an excuse to rewrite the stack.

### 5. Generate Tests

- Prefer user-facing locators such as role, label, and text.
- Avoid CSS selectors unless there is no stable user-facing alternative.
- Cover critical flows plus loading, error, and success states.
- Use stable custom locators only when the UI needs them.
- Write tests around observable behavior, not implementation details.

## Non-Negotiables

- Use semantic HTML before ARIA.
- Prefer native browser controls before custom widgets.
- Critical actions must not be hover-only.
- Critical flows must not depend on popup-only, drag-only, or canvas-only interaction.
- Every critical control needs an accessible name.
- Loading, error, empty, and success states must be readable text.
- Critical actions and fields need stable ways to locate them.
- Search, filter, sort, pagination, and selected tab state should usually be reflected in the URL.
- Do not add CAPTCHA, agent manifests, or automation-specific APIs unless the user asks or the project already needs them.

## Reference Routing

Read only the files needed for the current task.

- For core goals, severity, and review judgment: `references/principles.md`
- For semantic HTML, native control choices, and interaction anti-patterns: `references/semantic-html-first.md`
- For stable locators and URL state: `references/locator-and-state.md`
- For review deliverables and AI-readable content notes: `references/review-output-format.md`
- For quick implementation or review guidance on common components: `references/component-recipes.md`

## Output Rules

- State the chosen task mode before substantial action when the mode is not obvious from context.
- Keep recommendations tied to critical user tasks and observable UI behavior.
- When reviewing, use the review format in `references/review-output-format.md`.
- When reviewing, use severity labels `🔴 High`, `🟡 Medium`, and `🟢 Low` when possible. If emoji rendering is unavailable, use `High`, `Medium`, and `Low` exactly.
- When implementing or refactoring, explain any non-native control choice and why native HTML was not sufficient.
- When adding custom locators, keep naming stable and domain-oriented.

## Boundaries

- Do not turn this skill into a full WCAG summary.
- Do not recommend experimental agent manifests as a default path.
- Do not add locator hooks to every element.
- Do not prefer ARIA-heavy custom UI over native HTML without a clear reason.
- Do not assume visual polish alone makes a UI operable.

Agent manifests such as `.well-known/ai.json` are experimental and not required. Mention them only when the user is explicitly designing machine-readable app metadata or the project already uses such a convention.
