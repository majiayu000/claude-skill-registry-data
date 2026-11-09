---
name: unity-build-physics
description: Build Unity 2D or 3D physics and movement using explicit simulation ownership, collision policy, and measured limits.
engines: [UNITY]
---

# Unity Build Physics

## When to use

Build Unity 2D or 3D physics and movement using explicit simulation ownership, collision policy, and measured limits. Use this feature only for Unity-owned project code and assets.

## Activation and prerequisites

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh unity-build-physics` before edits or tool launches. Continue only when the effective engine is `UNITY` and this skill is eligible. A requested skill never selects its engine. Honor the resolved task override evidence and permitted output scope when an isolated prototype is selected.

Identify Unity version, classic 2D versus explicitly selected Physics Core versus 3D physics, world units, fixed timestep, layer matrix, movement authority, collision budgets and target hardware. Read existing body/controller conventions before changing movement. Consult [simulation and diagnostics](references/simulation-diagnostics.md) before API selection or sleep/collision fixes.

## Workflow

1. Select one physics domain for each interaction. Rigidbody/Collider, classic Rigidbody2D/Collider2D and any explicitly selected newer Physics Core world have distinct APIs and ownership. Do not assume cross-world contacts or port older 2D examples by renaming types.
2. Choose dynamic, kinematic or controller movement by gameplay requirements. Apply forces, velocity or supported move methods in the intended simulation phase; avoid competing Transform writes that fight a dynamic body.
3. Define fixed-step input consumption, maximum catch-up policy, interpolation and camera sampling. A fixed timestep improves scheduling but does not establish cross-platform deterministic physics.
4. Configure collision layers, triggers, contact material, mass, constraints and continuous collision detection from measured use cases. Ensure trigger callbacks and contact events are safe when either object is removed mid-frame.
5. Use raycasts, shape casts and overlaps with explicit masks, trigger policy and bounded result handling. Detect buffer saturation instead of interpreting truncated query results as a complete answer.
6. Build grounded movement, slopes, steps and moving-platform behavior against the selected body/controller approach. Keep navigation and animation suggestions subordinate to the same motion owner.
7. Represent gameplay impact and damage as validated authoritative events; camera shake, sound and haptic feedback consume those events without determining whether a hit occurred.

## Verification

- Test fast objects, thin obstacles, slopes, stairs, moving platforms, spawn overlap, stacked bodies and objects disabled during callbacks.
- Compare behavior across representative render rates and fixed-step pressure, including pause/resume and time scaling; measure physics CPU cost and query allocations.
- Run native player checks on target hardware. Document tolerances and any replay/network nondeterminism rather than claiming exact lockstep.

## Output

Physics configuration and movement components, collision/query contract, fixed-step ownership diagram, representative native fixtures and measured budgets. Record environment, expected and observed results, evidence paths, and blocked or not-run checks separately from passes.

## Boundaries

Do not alter global timestep or layer settings to conceal a local controller bug. Switching physics dimensions or movement authority requires migration evidence. Engine guidance applies to engine-owned code; independent services retain their architecture contracts.

## References

- [Unity physics concepts](https://docs.unity3d.com/6000.0/Documentation/Manual/PhysicsSection.html). Use the documentation matching the installed project version.
- [Unity 2D physics](https://docs.unity3d.com/6000.0/Documentation/Manual/Physics2DReference.html). Use the documentation matching the installed project version.

