---
name: unreal-build-physics
description: Build Unreal Chaos bodies, collision queries and constraints with measured stability and one transform authority.
engines: [UNREAL]
---

# Unreal Build Physics

## When to use

Build Unreal Chaos bodies, collision queries and constraints with measured stability and one transform authority. Use this feature for Unreal-owned game code and content.

## Activation and prerequisites

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh unreal-build-physics` before edits or tool launches. Continue only when the effective engine is `UNREAL` and `compatible: true`. Skill selection never selects the engine. Revalidate any task override and its permitted isolated output scope before writes. Record observed context and evidence only in the resolved `.hephaera/.cache/tasks/<task>/`; `ENGINE.md` remains the selector.

Identify Unreal version, Chaos settings, target hardware, world scale, movement components, collision channels, fixed/substep configuration and required stability budgets. Separate gameplay collision requirements from rendering detail.

## Workflow

1. Choose simulated rigid bodies, kinematic movement or CharacterMovement for each actor. Assign one transform authority; avoid setting actor transforms every frame while also expecting unconstrained dynamic simulation.
2. Define object channels, trace channels, profiles, blocking and overlap responses. Query and physics collision settings must match intended interaction; overlap events need explicit registration and teardown ownership.
3. Configure masses, center of mass, constraints, physical materials, CCD and sleep behavior from representative objects. Use simple versus complex collision according to supported simulation/query paths and measured cost.
4. Integrate impulses, forces and movement requests in the correct engine phase. If substepping or asynchronous physics is selected, use version-supported synchronization and avoid accessing unsafe UObject state from physics work.
5. Use sweeps, traces and overlaps with explicit channel, query parameters and ignored actors. Validate hit results and owner lifetime; process callback multiplicity without duplicate damage or item transactions.
6. Integrate locomotion through the dedicated movement owner; floors, slopes, moving bases, root motion and prediction belong to that path. General body simulation must not become a competing character transform authority.
7. Keep cosmetic impact responses separate from authoritative hit outcomes. Ragdoll transitions, recovery and collision handoff must explicitly transfer ownership instead of leaving two controllers active.

## Verification

- Test high velocity versus thin obstacles, initial penetration, moving platforms, constraints, ragdoll recovery and world teardown during callbacks.
- Exercise varied render rates and physics load, pause and time scaling; record tolerances and target CPU cost.
- Measure collision complexity and query counts in real engine fixtures. Chaos operation does not imply deterministic cross-platform lockstep.

## Output

Collision profiles, body/constraint/movement setup, transform and timing ownership map, stress fixtures and target physics measurements. Record environment, scope, expected and observed results, evidence paths, and blocked or not-run checks separately from passes.

## Boundaries

Do not change project-wide Chaos or timing settings to mask a local issue. Experimental physics features require explicit version and risk acceptance. Independent tools and services retain their own architecture contracts.

## References

Read [Chaos query ownership](references/chaos-query-ownership.md) when configuring timing, collision or handoff behavior.

- [Unreal physics](https://dev.epicgames.com/documentation/en-us/unreal-engine/physics-in-unreal-engine). Match the documentation version to the project.
- [Character movement](https://dev.epicgames.com/documentation/en-us/unreal-engine/character-movement-component-in-unreal-engine). Match the documentation version to the project.

