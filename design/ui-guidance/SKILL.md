---
name: ui-guidance
description: Baseline overlay for routine graphical UI and frontend changes that preserve the existing design language; use `ui-design-guidance` for redesign, polish-heavy implementation, or deep UX review. Compose with matching implementation guidance. Not for terminal UIs or pure plotting.
---

# UI/Frontend Guidance

This is a composable overlay, not a standalone workflow.
Use alongside the matching principle skill (for example,
`coding-guidance-cpp`) when the change touches UI or frontend code. Add
`project-core-dev` only when repository-specific completion checks still need
to be discovered or reported.

Choose the activity before applying the rules below:

- for implementation, make only the requested UI changes and validate them
- for review, inspect and report prioritized findings with evidence; do not
  edit files or require findings to be fixed unless the user also asks for
  remediation

Use this as the thin default overlay for ordinary UI work.
If the task is redesign-heavy, frontend-polish heavy, or needs a stronger UX
review checklist, prefer `ui-design-guidance`.

Routing examples:

- add a small control that matches nearby components -> use this skill
- fix spacing, labels, or responsive behavior within the existing visual
  language -> use this skill
- redesign a page, introduce a new visual direction, or perform a UX-heavy
  release review -> use `ui-design-guidance`
- product-security or permission-sensitive UI flows -> use `security` first
  when the main risk is trust, identity, or authorization rather than
  presentation; add `security-identity-access` when the security scope centers
  on identity, sessions, recovery, or tenant authorization

## When to use

The repo includes graphical UI or web frontend code — web views, desktop UI,
embedded panels, or rendering layers.

## Not for

Terminal UIs belong to their framework's guidance, including
`coding-guidance-go-tui` for Bubble Tea. Pure data visualization or plotting
without product-interface work is also out of scope.

## Rules

- Preserve the existing design language unless the task explicitly calls for
  redesign. Do not introduce new color palettes, spacing systems, or component
  patterns without justification.
- Accessibility, layout stability, and responsive behavior are part of done —
  not follow-up work.
- UI changes must not bypass the repo's test and build hygiene.
- Verify visual output manually or with snapshot tests if the repo supports
  them.
- If the repo does not document breakpoints, design tokens, or visual test
  tooling, derive them from nearby UI code and record the fallback evidence in
  any implementation or review note you produce.

## Decision Heuristics

- **Design language check:** before adding a new visual element, search the
  codebase for an existing element that serves a similar purpose. Match its
  spacing, color tokens, and component structure unless the task requires
  divergence.
- **Evidence fallback:** when the repo lacks UI docs, use the nearest existing
  component or screen as the baseline and name the files inspected.
- **Accessibility bar:** if the change adds interactive elements, verify
  keyboard navigation and screen reader labels. If the repo has no a11y
  testing, add manual verification to the review checklist.
- **Layout stability:** if the change affects layout, test at the repo's
  supported viewport sizes. If those are undocumented, test at the common
  breakpoints already exercised by nearby code or styles. Flag layout shifts
  that appear on resize or content change.

## Validation

For implementation, a UI change is done when, in addition to the base
implementation skill's validation:

- visual output matches the existing design language or the requested redesign
- interactive elements are keyboard-navigable and expose appropriate names,
  roles, or labels
- layout is stable across supported viewports
- when automated UI verification is absent, any implementation or review note
  you produce names the screenshots, snapshots, or manual checks used as
  evidence

For review, completion means prioritized findings name the affected interaction
or screen, supporting evidence, likely user impact, and any validation gap. Open
findings do not make the review incomplete.
