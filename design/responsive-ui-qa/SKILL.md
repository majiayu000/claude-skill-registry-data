---
name: responsive-ui-qa
description: Inspect, diagnose, fix, and verify responsive frontend defects across routes, states, containers, and input modes. Use for mobile or desktop QA, overflow, overlap, broken navigation, unstable grids, clipped text, blank media, viewport regressions, screenshot comparison, and post-implementation visual verification.
---

# Responsive UI QA

Find root causes, not screenshot-specific patches. Produce evidence that the reported state works after the fix.

## Workflow

1. Read the repository's run and testing instructions. Start the app with its normal command.
2. Build a compact test matrix:
   - critical routes or components;
   - default, loading, empty, error, long-content, and interactive states;
   - narrow mobile, mobile, tablet or narrow container, desktop, and wide desktop as relevant.
3. Reproduce the exact reported defect before editing. Capture the viewport, route, state, and interaction.
4. Inspect layout mechanics: containing block, grid/flex constraints, intrinsic size, min-width, wrapping, positioning, stacking, overflow, and fixed/sticky offsets.
5. Classify severity:
   - **Blocker** - action or content is inaccessible;
   - **Major** - interaction or comprehension is materially impaired;
   - **Minor** - visible polish defect without task failure.
6. Fix the underlying constraint with the smallest coherent change. Avoid viewport-specific offsets unless the design genuinely changes there.
7. Test content stress: long labels, unbroken strings, localization expansion, missing/large media, validation text, and dynamic lists.
8. Test input and preference modes: keyboard, touch-sized targets, focus visibility, zoom when feasible, and reduced motion.
9. Re-run the failed case plus adjacent widths and states. Check that no new horizontal scroll or hidden content was introduced.
10. Report evidence, remaining risks, and anything not testable locally.

## Fix Rules

- Prefer intrinsic layout, wrapping, `minmax()`, `min-width: 0`, `max-width`, `aspect-ratio`, and container-aware rules.
- Change information architecture at breakpoints when reflow alone is insufficient.
- Do not "fix" overflow by globally hiding it or shrinking text below readability.
- Reserve fixed dimensions for controls and media with a real size contract.
- Keep fixed or sticky UI from covering focused elements and anchored content.
- Verify canvas, WebGL, video, charts, maps, and embeds by inspecting rendered pixels and resize behavior.
- Preserve behavior at the exact state that triggered the bug.

## Delivery Contract

Return:

1. **Matrix tested** - route/state/viewport/input.
2. **Findings** - severity, reproduction, and root cause.
3. **Fixes** - files changed and why the constraint is correct.
4. **Evidence** - before/after screenshots or explicit browser observations.
5. **Residual risk** - untested browsers, data states, or environments.

## Reference

Read [references/qa-checklist.md](references/qa-checklist.md) for the final cross-viewport and interaction pass.
