---
name: responsive-breakpoint-check
description: "Checks desktop, tablet, and mobile UI for overflow, clipping, navigation, grid, canvas, and breakpoint regressions."
---

# Responsive Breakpoint Check

Verify that UI survives real viewport changes.

## Workflow

1. Read `ui-qa`.
2. Identify target routes and core states.
3. Check desktop, tablet, and mobile widths with browser or Playwright.
4. Inspect overflow, wrapping, clipped controls, sticky headers, sidebars,
   dialogs, grids, charts, media, and touch targets.
5. Record fixes or recommended changes.

## Output

- viewports checked
- routes/states checked
- failures with evidence
- minimal fixes
- remaining gaps
