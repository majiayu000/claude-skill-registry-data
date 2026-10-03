---
name: codex-visual-quality-gate
description: Use after UI implementation for mechanical source checks and a rendered or fresh-eyes review.
load_priority: on-demand
version: "18.1.0"
---

## TL;DR
Mechanical checks are source evidence, not aesthetic scores. A valid approval requires complete route × viewport × state capture evidence and a recorded review of every stitched page and source slice. Missing browser, screenshots, coverage, provenance, or review is `DEGRADED`; high-confidence defects or gaps fail.

## Activation
Substantial UI delivery or `$visual-gate`. Skip backend-only work.

## Gate workflow

1. Exercise every UX-contract flow and declared route/state, including important interaction/error/empty/success paths. Check keyboard/focus, labels, contrast, semantic structure, and reduced motion as applicable.
2. Run `scripts/capture_responsive_matrix.mjs` with the project route/state manifest. It warms lazy content and makes overlapping viewport-sized screenshots, full-page composites, exact viewport dimensions, and a 320–2560 px width scan. Horizontal overflow, browser errors, and off-viewport interactive controls cause width-specific capture; off-viewport controls are review signals, not automatic defects.
3. Open and inspect every stitched image **and every original slice**. Evaluate the screenshot at its stated route, state, and viewport; record reviewer, summary, checked capture keys, and evidence-linked findings in `visualReview`. Record exercised flows, route/state checks, and functional/accessibility results in `functionalReview`.
4. Run `scripts/visual_quality_gate.py --project-root <app> --capture-manifest <manifest> --format json`. It checks all routes/flows/states, seven anchor profiles, breakpoint edges, PNG dimensions, continuous overlapping slice coverage, responsive sweep samples, overflow, provenance, and visual/functional/accessibility review completeness.
5. Fix or justify high-confidence findings; perform at most two inspect/fix rounds. Unresolved blocking/P0/P1 findings fail. Missing coverage or image inspection is `DEGRADED`.

Viewport anchors (CSS px at device scale 1): 1280×800, 1440×900, 1920×1080; 768×1024, 1024×768; 390×844, 844×390. These are browser emulations, not physical-device certification.

## References
- `../codex-frontend-design/references/anti-slop.md`
- `../codex-frontend-design/references/composition.md`
- `../codex-frontend-design/references/responsive-evidence.md`
