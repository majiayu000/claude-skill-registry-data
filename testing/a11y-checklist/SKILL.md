---
name: a11y-checklist
description: WCAG 2.2 AA checklist and severity classification used by a11y-auditor and the @a11y Playwright/axe-core scans. a11y-auditor loads this skill automatically.
paths: ["src/components/**", "src/routes/**", "tests/e2e/a11y.spec.ts"]
---

## Severity classification (drives the gate — critical/serious block, minor does not)

- **critical/serious** (blocks `verify-gate.sh`): missing accessible name on an interactive
  control, keyboard trap, focus not moved/trapped correctly in a modal dialog, insufficient
  color contrast on body text, missing form label association, content that only conveys
  meaning via color.
- **minor** (reported, does not block): redundant `alt` text, non-ideal heading hierarchy on a
  page that is still navigable, a `title` attribute duplicating visible text.

## Mechanical checks (axe-core catches these — a11y-auditor just triages severity)

- Every interactive element has an accessible name (button text, `aria-label`, or associated
  `<label>` — see the email input in `SubscribeDialog.tsx`).
- Every image conveying information has `alt` text; every decorative image has `alt=""`.
- Focus is visible on every interactive element (`focus-visible:ring-*`, never `outline-none`
  alone — see `component-conventions` skill).
- Radix `Dialog` primitives handle focus trap and `aria-modal` automatically — do not
  reimplement focus trapping manually; a hand-rolled dialog is a common source of critical
  findings.
- Color contrast meets WCAG AA (4.5:1 normal text, 3:1 large text) — check new `@theme` tokens
  against both light and dark rendering, not just one.

## Judgment calls (a11y-auditor escalates these to `model: sonnet` instead of guessing)

- Whether `alt` text is _meaningful_ (not just present).
- Whether a complex widget's `aria-*` roles fully match its actual keyboard behavior.
- Whether reading order (DOM order vs visual order) creates a confusing experience for screen
  reader users, even if no individual axe rule fires.
