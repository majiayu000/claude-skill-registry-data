---
name: motion-performance-auditor
description: Audit a motion-heavy website for frame pacing, WebGL cost, accessibility, mobile behavior, and lifecycle leaks. Use for diagnosis or pre-launch QA with browser evidence; use motion-choreographer or immersive-3d-web when the main request is implementation.
---

# Motion Performance Auditor

Audit in descending order of user impact: broken usability → loading/interactivity → frame-time/jank → accessibility → visual polish.

## Audit workflow

1. Identify stack and entry points.
2. Run static scan when source is locally available:
   `python scripts/creative_web_static_audit.py <project-path>`
3. Inspect first-load critical path.
4. Inspect scroll/animation lifecycle.
5. Inspect canvas/WebGL render loop and GPU resources.
6. Check mobile and reduced-motion behavior.
7. Rank findings by severity and confidence.
8. Propose fixes with the smallest effective change first.

If another skill supplies a handoff packet, audit against its thesis, rendering boundary, variants, budgets, and acceptance criteria. Preserve expected-versus-observed values in the report. A static scan is evidence discovery, not proof of a runtime defect.

## Severity

- **P0 blocker:** crash, inaccessible critical action, scroll trap, unusable fallback.
- **P1 high:** major CWV/jank risk, runaway render loop, severe mobile issue, missing cleanup causing leaks.
- **P2 medium:** avoidable bundle/render cost, overly long pinning, inconsistent motion, nonessential GPU load.
- **P3 polish:** small timing, minor layout, maintainability, micro-optimization.

## Core Web Vitals targets

Default good thresholds at p75:
- LCP <= 2.5s
- INP <= 200ms
- CLS <= 0.1

Do not confuse lab scores with field data. Use lab tools to reproduce problems and field data when available for actual user experience.

## Motion audit

Check:
- too many simultaneous animations
- layout-affecting properties animated continuously
- repeated measurements inside scroll/RAF loops
- duplicate RAF/ticker loops
- ScrollTriggers/listeners/timelines not cleaned up
- animation objects recreated during renders
- long pin/scrub sequences without narrative value
- scroll smoothing interfering with anchors/touch/keyboard
- reverse scroll state bugs
- hover-only essential interactions

## React/Motion audit

Check:
- React state updates at frame rate
- missing cleanup of subscriptions
- excessive layout animations on large trees
- heavy client boundaries around static content
- animations causing re-render cascades

## Three/R3F audit

Check:
- uncapped DPR
- excessive draw calls/materials/lights/shadows
- repeated geometry/material creation
- mount/unmount churn
- `setState` in `useFrame`
- high-resolution textures with low screen coverage
- too much post-processing
- continuous frameloop for static scenes
- no offscreen pause
- missing disposal for manual resources
- too many transparent layers / overdraw

## Accessibility

Require:
- meaningful `prefers-reduced-motion` handling
- keyboard-visible focus and navigation
- semantic DOM for essential content
- no canvas-only critical text/actions
- no dangerous flashing or unavoidable large repeated motion
- touch alternatives for hover/drag concepts

## Performance budgets

Use `references/budgets.md` as defaults, then adapt to project goals. Budget from user experience backward; do not optimize irrelevant bytes while ignoring a 12MB hero video or full-screen 3D scene.

Every numeric claim must name its test context: viewport, device/profile, network, route/scene, and tool. Mark results as `measured`, `estimated`, or `not tested`; never turn absence of evidence into a passing score.

## Completion gate

Before a launch-ready verdict, require evidence for:
- primary action with keyboard and relevant pointer/touch input
- narrow mobile layout without accidental horizontal overflow
- reduced-motion variant
- hidden/offscreen canvas or animation behavior
- WebGL/WebGPU failure path when applicable
- heaviest first-scene asset and render-resolution policy
- one repeatable performance capture for the riskiest scene

If a check cannot run, record it as residual risk with an exact follow-up command or procedure.

## Showcase audit mode

For an impressive reference site, separate perceived polish from production cost. Record what the reference spends its performance budget on, then identify which parts are essential to the experience and which are optional spectacle.

## Output format

Return:
1. executive summary
2. scorecard: performance / motion / 3D-GPU / accessibility / mobile / maintainability
3. findings grouped P0–P3 with evidence
4. exact fix recommendations
5. quick wins vs structural fixes
6. validation plan after changes

## Examples and showcase calibration

Read `references/examples.md` to calibrate severity, evidence, and fix recommendations. Read `references/showcase.md` when auditing impressive motion/3D sites so visual ambition is evaluated together with runtime, mobile, and accessibility constraints.

## References
- `references/examples.md`
- `references/showcase.md`
- `references/audit-checklist.md`
- `references/budgets.md`
- `references/test-matrix.md`
