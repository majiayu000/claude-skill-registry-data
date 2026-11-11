---
name: visual-qa
description: Visual QA setup and browser screenshot review workflow. Use when the user asks for visual QA, visual review, screenshot-based design review, or project documentation for rendering UI before visual review.
---

# Visual QA

Use this skill to establish and run a reliable project-specific visual QA flow.
The goal is to review **real rendered UI**, not an invented harness.

## Source of truth

Prefer a root `VISUAL_QA.md`. If it is missing, the Orchestrator should set up
or ask for this documentation before delegating to `@visual-qa`.

Also read root `UX.md` and relevant `docs/ux/*` when present. `UX.md` is the
durable project-wide UX source of truth. Existing UI patterns are useful
evidence, but do not override documented UX rules unless the user confirms a
pattern change or exception.

`@visual-qa` should only run when one of these is available:

- `VISUAL_QA.md` with enough detail to run the UI;
- an explicit URL/dev-server command from the user;
- a clearly documented Storybook/Ladle/Histoire/component-test setup;
- existing project docs that define equivalent visual QA steps.

## `VISUAL_QA.md` template

```markdown
# Visual QA

## How to run

- Install/setup command:
- Dev server command:
- Default URL:
- Component explorer command/URL, if any:

## What to review

- Routes/components:
- Required UI states:
- Viewports:
- Themes/modes:

## UX sources

- Root UX doc: `UX.md` / none
- Flow UX docs:
- Design tokens/component patterns:
- Known visual exceptions:

## App providers

- Theme/provider setup:
- Router/data/query/i18n setup:
- MUI or component-library notes:

## Auth and data

- Is login required?
- Safe automation login/session flow, if any:
- Seed/mock data requirements:

## Visual QA checklist

- Visual consistency gate:
- Intentional visual restraint gate:
- Layout/spacing/alignment:
- Typography/readability:
- Color/contrast/theme consistency:
- Interaction states:
- Responsive behavior:
- Overflow/truncation behavior:
- Accessibility risks:
```

## Setup workflow for Orchestrator

When visual QA is requested and no usable docs exist:

1. Inspect the project for existing run paths:
   - package scripts (`dev`, `start`, `storybook`, `ladle`, `histoire`);
   - README/AGENTS/docs instructions;
   - `UX.md` and `docs/ux/*`;
   - app routes and component explorer configuration;
   - provider/theme setup, especially MUI theme providers;
   - design tokens and existing component patterns.
2. Ask only for missing critical details:
   - target route/component/state;
   - auth/session expectations;
   - preferred app route vs component explorer;
   - required theme/provider/data setup.
   - intended exceptions to UX docs, tokens, or existing visual patterns.
3. Create or update `VISUAL_QA.md` when the user wants the workflow persisted.
4. Delegate to `@visual-qa` only after the run flow is explicit.

Do **not** ask `@visual-qa` to invent a React server, raw-render MUI
components, bypass login, or guess data fixtures.

## Execution workflow for `@visual-qa`

1. Read `VISUAL_QA.md` and any referenced docs.
2. Read `UX.md`, relevant `docs/ux/*`, design tokens, and documented component
   patterns when present.
3. Load the `agent-browser` skill and its current CLI workflow.
4. Start only documented commands and navigate only documented URLs/routes.
5. Capture screenshots for the requested viewport(s), state(s), and theme(s).
6. Evaluate the actual rendered UI against the checklist and the gates below.
7. Return a concise, screenshot-grounded report with concrete fixes.

If the flow is blocked by missing docs, auth, unavailable data, or missing
browser tooling, report the blocker instead of guessing.

## Visual consistency gate

Use this as a strict fundamentals checklist. Mark each relevant item as `Pass`,
`Issue`, `Needs decision`, or `Not applicable`:

- Row alignment and icon/control centerlines.
- Spacing scale: related elements closer, unrelated groups farther apart.
- Regional edge alignment across cards, fields, headers, and actions.
- One clear primary action per screen or major region.
- Typography hierarchy, readable line lengths, and scan-friendly contrast.
- Responsive wrap/stack behavior for rows, filters, nav, forms, and actions.
- Overflow/truncation behavior for long labels, values, chips, URLs, and dense
  actions.
- Component consistency for repeated roles.
- Visual accessibility basics: contrast, focus visibility, target size, labels.
- State clarity: default, hover/active, disabled, loading, error, selected.
- Color semantics for error, warning, success, destructive, and primary actions.
- Density and breathing room so dense UIs still have grouping and hierarchy.

## Intentional visual restraint gate

Flag these as `Issue` unless they are explicitly justified by the user,
`UX.md`, design tokens, or a consistent existing pattern:

- Unexplained gradients, aurora blobs, neon glows, glassmorphism, rainbow washes.
- Prominent shadows, hover-lift everywhere, floating cards, unnecessary
  cardification.
- Large pill shapes or oversized rounded containers without semantic need.
- Bento grids, centered hero stacks, fake dashboards, arbitrary stat cards.
- Oversized hero type, gradient/glowing buttons, icon-stuffed controls.
- Vague filler copy, fake-perfect metrics, fake testimonials, fake avatars.
- Decorative stock imagery, floating icons, 3D blobs, emoji filler.
- Decorative motion, shimmer everywhere, confetti for ordinary actions.

## Report shape

- **Scope reviewed:** route/component, viewport, state, screenshots.
- **UX docs used:** `UX.md`, `docs/ux/*`, design tokens, or none found.
- **Verdict:** Pass / Needs polish / Fails visual QA.
- **Visual consistency check:** compact gate results.
- **Intentional visual restraint check:** compact gate results and justified exceptions.
- **Top issues:** prioritized and tied to observed screenshots.
- **Recommended fixes:** concrete design or implementation changes.
- **Blockers:** missing docs, auth, data, or tooling.
