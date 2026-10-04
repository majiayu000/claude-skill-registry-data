---
name: playwright-visual-qa
description: "Validates rendered UI with browser or Playwright screenshots after implementation, redesign, responsive changes, or visual regressions."
---

# Playwright Visual QA

Verify the rendered UI, not just the build.

## Workflow

1. Read `ui-qa`.
2. Start or identify the local app URL.
3. Capture desktop and mobile screenshots.
4. Compare against the accepted concept, Figma frame, screenshot, or existing
   baseline.
5. Check layout, copy, typography, colors, assets, icons, states, and overflow.
6. Fix material drift when implementation is in scope.

## Output

- URL or app entrypoint
- screenshots/viewports checked
- reference used
- mismatches found
- fixes made or recommended
- remaining deviations

## Rule

Functional tests do not replace visual QA. If screenshots cannot be captured,
state the blocker.
