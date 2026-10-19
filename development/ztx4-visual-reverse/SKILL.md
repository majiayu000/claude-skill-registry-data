---
name: ztx4-visual-reverse
description: "Deep implementation master for Visual Reverse Engineering with 16 targeted Codex skills, code, tests and no MCP. Additive to all existing Perfect_AI versions."
---

# Visual Reverse Engineering

Reconstruct behavior from permitted references while distinguishing observable evidence from missing proprietary implementation.

## Mandatory sequence
1. Obtain reference screenshots or access with user permission; record viewport, font readiness and state.
2. Capture a state matrix for top/quarter/middle/bottom scroll, hover, focus, menu and reduced motion.
3. Measure boxes, spacing, radii, font metrics, SVG paths and dynamic transform changes from evidence.
4. Rebuild independent structure; do not claim unknown source code or assets are identical.
5. Compare deterministic screenshots, compute differences, triage and iterate until agreed tolerance.

## Skill routing
Choose only technique files needed for this project from `DEEP-IMPLEMENTATION-v2/references/visual-reverse.md`. Never indiscriminately load all 300+ skills into context.

## Runbook
Inputs: user-supplied or permitted reference, screenshots/recordings, viewport states and asset rights.

Implementation: measure layout, sample scroll/time states, document observed vs inferred, build independent semantic DOM, perform deterministic screenshot diff.

Tests: same DPR/fonts/viewport/time, pixel difference and layout deviation, reverse scroll, keyboard, record unknown proprietary details.

## Acceptance gates
1. Reference evidence logged by viewport/interaction state.
2. Inferred unknown geometry/code called out rather than claimed exact.
3. Screenshot comparisons reproducible under same font/viewport/time.

## Runnable assets
`extensions/DEEP-IMPLEMENTATION-v2/examples` and `tools` (installed main package). See `RUNBOOK-FA.md`.

## Sources
- [playwright](https://playwright.dev/docs/test-snapshots)
- [mdn-containers](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Container_queries)
- [wcag](https://www.w3.org/TR/WCAG22/)
