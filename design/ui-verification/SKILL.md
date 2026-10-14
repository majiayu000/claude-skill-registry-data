---
name: ui-verification
description: "Verify UI with rule-keyed Playwright probes: visual states, responsive breakpoints, a11y assertions. Use after building or changing user-facing UI."
---

# ui-verification

Every UI rule gets a probe; every probe maps to the rule it checks.

## Activate when

- New/changed screens, responsive work, or design-system updates need proof, not screenshots alone.

## Do NOT activate for

- Design decisions themselves (see design-systems, responsive-design).

## Procedure

1. Map each Observed rule to a probe id; one probe per rule, named for the rule it checks.
2. Cover states: loading/empty/error/success, hover/focus/disabled, plus 320→1920 widths and reduced-motion.
3. Assert accessibility: roles, labels, focus order, contrast (pair with `../accessibility/`).
4. Run headless in CI; store traces on failure; flake-quarantine with owner and expiry.
5. Verify: green run linked from the PR; failures reproduce locally via the trace.

## What this proves (and does not)

Distinguish four levels — do not claim a higher one than the probes support:

- Functional: states render, interactions respond, console error-free.
- Layout: bounding boxes, no overflow, no overlap, text wraps within containers.
- Responsive: layout holds across the viewport matrix; touch targets adequate.
- Accessibility: semantics, focus, names, contrast asserted programmatically.
- Visual regression (pixel comparison) is NOT implemented here: no screenshot baselines, no pixel-diff thresholds. Say "layout verified by probes," never "pixel-perfect." If pixel comparison is needed, add a dedicated screenshot-baseline tool first.

Concrete probes where a browser tool exists: viewport widths, element bounding boxes, `overflow` computed values, visibility, text wrapping, interaction-state screenshots, console errors, failed network requests.

## References
- Related: `../accessibility/`, `../responsive-design/`, `../component-design/`.
