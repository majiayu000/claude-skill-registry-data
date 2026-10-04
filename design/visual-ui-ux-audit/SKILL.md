---
name: visual-ui-ux-audit
description: Audit web and app interfaces using visual evidence. Use when Codex is asked to critique UI/UX, polish a design, inspect a localhost app, compare screenshots, find visual hierarchy/layout/typography/color/spacing/state/responsiveness/accessibility issues, or provide annotated design feedback grounded in browser screenshots.
license: MIT
---

# Visual UI UX Audit

## Core Workflow

1. Inspect the actual interface when possible, not only code. Use browser screenshots, responsive viewports, and interaction states.
2. Define the task, user, viewport, primary workflow, and quality bar before critiquing.
3. Capture key states: initial screen, primary flow, empty/loading/error/success, mobile, desktop, and any modal/menu/dropdown states.
4. Identify issues by evidence: where it appears, why it hurts the user, and what change would improve it.
5. Prioritize fixes by user impact and effort. Separate polish from blockers.
6. If editing, re-check screenshots after changes.

## Tooling Rule

When the interface is local or browser-accessible, prefer actual browser inspection through the available browser tooling. Capture desktop and mobile states when relevant. If a browser cannot be used, disclose that the audit is based on code or static artifacts only.

## Audit Dimensions

- Visual hierarchy: focal point, contrast, scan order, CTA prominence.
- Layout: alignment, spacing, density, grouping, rhythm, responsive behavior.
- Typography: size, line length, weight, contrast, truncation, overflow.
- Color: contrast, semantic meaning, palette consistency, state differentiation.
- Interaction states: hover, focus, active, disabled, loading, error, success.
- Information architecture: labels, grouping, navigation, progressive disclosure.
- Accessibility: keyboard flow, focus visibility, readable contrast, motion, hit targets.
- Craft: AI-generic styling, nested cards, accidental gradients, inconsistent radius/shadows, clutter.

## Output Contract

- Screens/states inspected
- Prioritized findings with evidence
- Recommended changes
- Quick wins
- Larger redesign risks
- Verification steps

## References

- Read `references/visual-audit-checklist.md` when performing a visual UI/UX critique.
