---
name: frontend-ui-engineering
description: "Build complete, accessible UI flows with explicit states and browser checks."
license: MIT
metadata:
  author: Addy Osmani and Skillz contributors
  source: addyosmani/agent-skills
  source-commit: 1401c8b8030e023baeebb31781a6653fe8e93026
  adaptation: curated-rewrite
  owner: software-factory
  risk: medium
  capabilities: addyosmani,frontend-ui-engineering
---

# Frontend UI engineering

Build complete interactions in the product's existing visual language. Start
with the screen's user, purpose, primary action, and data contract. Preserve
the existing framework and design system; a small visual edit needs a focused
render check, not a new design process.

## Implement the interaction

1. Inspect adjacent components, tokens, content, and responsive conventions.
   Use supplied designs when available. Resolve product choices that materially
   affect the flow; routine implementation choices can proceed within scope.
2. Model the states that the real data flow can reach: loading, empty, populated,
   validation error, request failure, permission denial, pending mutation, and
   confirmed success. Distinguish an empty result from a failed or partial read.
3. Keep state with its owner. Use local state for local interactions, URL state
   for shareable navigation, and the existing server-cache layer for remote
   data. Avoid duplicating server truth in a second global store.
4. Handle stale requests, cancellation, rapid navigation, repeated submission,
   and retries. Preserve entered data after recoverable errors. Prevent stale
   responses from overwriting newer state. Disabling a button does not replace
   server-side idempotency.
5. Use optimistic updates only where reversal is safe and conflicts can be
   reconciled. For payments, permissions, or irreversible actions, show pending
   until authoritative confirmation. A timeout may need a status check instead
   of another submission. Announce the actual outcome without claiming success
   from an HTTP acknowledgment alone.
6. Compose focused components around behavior and reuse. Do not split files
   solely to satisfy an arbitrary line count or introduce a state library for
   a single screen.

## Accessibility and visual finish

Prefer semantic HTML and existing accessible controls. Give icon-only buttons
accessible names, associate errors and labels with inputs, and preserve keyboard
access and visible focus. For modal dialogs, verify focus entry, containment,
escape/close behavior, background interaction, and focus return. Setting the
`open` attribute alone is not a complete modal implementation.

Follow the project's agreed accessibility target. For new web work without a
target, propose WCAG 2.2 AA as the baseline; do not claim compliance from an
automated scan. Check zoom/reflow, contrast, reduced motion, touch targets,
focus obscured by sticky elements, and alternatives to drag-only controls.
Use [the interaction checklist](references/interaction-checks.md) for a changed
flow, selecting the cases that apply.

Use real or representative content to expose wrapping, density, and overflow.
Keep spacing, typography, hierarchy, and feedback consistent with the product.
Aesthetic preferences do not override an approved design.

## Verify in the browser

Exercise the primary journey, failure recovery, keyboard path, and relevant
responsive widths in the actual rendered application. Use available browser
tools; a particular connector is not mandatory. Inspect console and network
failures. Automated component tests complement this inspection.

Report the states and device conditions verified, with screenshots or runtime
evidence when useful. State any unavailable screen-reader or browser testing.

Reference: [WCAG 2.2](https://www.w3.org/TR/WCAG22/).
