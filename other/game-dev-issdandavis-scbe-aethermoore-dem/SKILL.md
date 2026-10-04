---
name: game-dev
description: Build, prototype, debug, and ship game features across Unity, Unreal, Godot, and web game stacks. Use when requests involve gameplay systems, mechanics implementation, level scripting, input/camera/UI flow, save-load design, multiplayer foundations, performance profiling, content pipelines, or release-readiness planning for game projects.
---

# Game Dev

## Outcome

Deliver production-ready game feature slices that include implementation, validation, and clear next actions.

## Workflow

1. Clarify target player experience, platform, engine, and constraints.
2. Break work into a thin vertical slice that is testable in one session.
3. Implement deterministic core logic before visual polish.
4. Add observability early (logs, debug overlays, simple metrics).
5. Validate with explicit playtest steps and edge-case checks.
6. Report risks, tradeoffs, and follow-up tasks.

## Engine Routing

- Use Unity patterns for component-driven C# gameplay and editor tooling.
- Use Unreal patterns for gameplay framework classes, Blueprint/C++ boundaries, and data assets.
- Use Godot patterns for scene-tree architecture, signals, and GDScript/C# node lifecycles.
- Use web patterns for render loop timing, state isolation, and asset loading constraints.

If the user does not specify an engine, ask once, then proceed with a pragmatic default based on existing repo signals.

## Feature Slice Standard

For each requested gameplay feature:

1. Define the player-facing behavior in one paragraph.
2. Define state model and failure modes.
3. Implement core systems with minimal dependencies.
4. Integrate with input, camera, UI, and persistence as needed.
5. Add quick tuning knobs for designers (constants, data tables, scriptable configs).
6. Add smoke tests or reproducible manual verification steps.

## Debug and Performance Guardrails

- Reproduce bugs with exact deterministic steps before patching.
- Prefer smallest safe fix; avoid broad rewrites unless required.
- Measure frame-time impact for new systems and expensive loops.
- Watch allocation churn, physics/query frequency, and update loop fan-out.
- Keep data flow explicit to avoid hidden coupling between gameplay systems.

## Response Contract

When executing a request, return:

1. What changed and why.
2. Files/systems touched.
3. How to test quickly.
4. Remaining risks and next recommended milestone.
