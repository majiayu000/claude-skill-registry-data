---
name: godot-build-physics
description: Build Godot 2D or 3D physics and character motion with explicit process timing, collision policy, and query ownership.
engines: [GODOT]
---

# Godot Build Physics

## When to use

Build Godot 2D or 3D physics and character motion with explicit process timing, collision policy, and query ownership. Apply this feature only to Godot-owned code and content.

## Activation and prerequisites

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh godot-build-physics` before edits or tool launches. Continue only when the effective engine is `GODOT` and the skill is eligible. Skill selection never selects the engine. Honor validated task override evidence and its permitted isolated output scope.

Identify Godot version, selected physics backend, 2D/3D domain, project language, world scale, physics tick settings, collision layers/masks and movement budgets. Do not replace a selected physics backend implicitly.

## Workflow

1. Choose StaticBody, RigidBody, CharacterBody and Area nodes in the correct dimensional family. Areas detect interactions, dynamic bodies simulate forces, and character bodies require explicit movement code.
2. Run gameplay physics movement in _physics_process or its C# equivalent. CharacterBody velocity has rate units; use move_and_slide according to the installed API without multiplying an already rate-based velocity by delta twice.
3. For RigidBody state adjustments, use supported force APIs and _integrate_forces where needed. Do not fight simulation with arbitrary Transform writes from render updates.
4. Configure layers, masks, shapes, one-way behavior, continuous detection and contact reporting from actual gameplay requirements. Shape resources may be shared; per-instance edits need deliberate resource ownership.
5. Use direct_space_state ray/shape queries in a safe physics phase with explicit masks and exclusions. Bound result counts and handle hit objects being removed before the consumer uses them.
6. Integrate slopes, floor snapping, moving platforms and navigation safe velocities with one movement owner. Keep 2D and 3D navigation/physics maps distinct and validate units.
7. Translate contacts into validated authoritative gameplay events. Effects and haptic feedback consume those events; duplicate callbacks, disappearing objects and scene transitions must not duplicate damage or persistence writes.

## Verification

- Test thin obstacles, high speed, slopes, stairs, moving platforms, initial overlap and body removal during callbacks.
- Compare varied render rates under the same physics configuration, including pause/time scaling and excessive physics load.
- Measure query counts, contact cost and representative body counts using real Godot; document tolerances rather than promising cross-platform deterministic physics.

## Output

Body/collision configuration, movement/query code, timing and transform ownership map, native edge-case fixtures and physics budgets. Record environment, scope, expected and observed results, evidence paths, and blocked or not-run checks separately from passes.

## Boundaries

Do not mix 2D and 3D body assumptions or silently change global tick settings. Headless fixtures establish simulated behavior only within the recorded backend and version. Independent services and tools retain their architecture contracts.

## References

- [Godot physics introduction](https://docs.godotengine.org/en/stable/tutorials/physics/physics_introduction.html). Select the documentation matching the project release.
- [Using CharacterBody2D](https://docs.godotengine.org/en/stable/tutorials/physics/using_character_body_2d.html). Use the matching CharacterBody3D API when the project is 3D, and select documentation for the project release.

