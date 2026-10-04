---
name: game-3d-development
description: Plan, implement, debug, and review real-time 3D game development work. Use when Codex is asked to build or improve 3D gameplay, cameras, controllers, physics interactions, animation integration, spatial UI, scene architecture, composition/component architecture, performance, rendering, Three.js, Unity, Unreal, Godot, or custom-engine 3D systems.
license: MIT
---

# Game 3D Development

## Core Workflow

1. Identify the engine/runtime, target device, input methods, camera style, and performance budget before designing the implementation.
2. Inspect the existing project patterns first: scene graph ownership, update loop, asset loading, physics layer, animation system, ECS/component conventions, and build tooling.
3. Prefer composition for scalable gameplay entities: one script/component has one job, entities "have" capabilities instead of inheriting every behavior from broad base classes, and a small orchestrator coordinates components when needed.
4. Prefer proven engine or library primitives for physics, animation, navigation, collision queries, and asset loading. Hand-roll only when the feature is small, intentionally custom, or the project has no suitable dependency.
5. Build the smallest playable slice that proves camera, controls, collision, feedback, and failure states together.
6. Verify visually and behaviorally. For browser/WebGL projects, use browser screenshots and canvas checks. For engine projects, run the available editor, playmode, unit, or build checks when possible.

## Implementation Priorities

- Controls: support the expected input devices, define dead zones and sensitivity, avoid frame-rate dependent movement, and handle focus/pause states.
- Camera: specify follow target, damping, collision avoidance, field of view, occlusion handling, and motion-sickness risks.
- Physics: use fixed-step simulation, clear collision layers, explicit units, stable mass/force values, and predictable trigger behavior.
- Scene architecture: keep spawn/despawn, pooling, asset lifetime, save state, and cross-scene dependencies explicit.
- Component composition: split health, input, movement, attack, interaction, inventory, hurtbox, hitbox, and camera behaviors into reusable components when they can stand alone.
- Animation: define source of truth between animation and gameplay state; avoid hidden animation events for critical game rules unless that is the established pattern.
- Performance: watch draw calls, shader cost, texture memory, skeleton count, physics query volume, allocations in hot loops, and asset streaming stalls.
- Tooling: create debug views, tunable constants, gizmos, or inspector fields when iteration speed matters.

## Design Before Code

For substantial 3D features, write a compact feature contract before editing:

- Player-facing behavior
- Success and failure states
- Control scheme and camera behavior
- Required assets and placeholders
- Simulation rules and edge cases
- Performance assumptions
- Verification steps

## Freshness Rule

Verify current engine/framework documentation before making version-sensitive recommendations about Unity, Unreal, Godot, Three.js, physics libraries, animation systems, asset import pipelines, rendering APIs, or platform build settings.

## Deliverable Shape

For 3D development work, provide:

- Engine/runtime and target platform assumptions
- Player-facing behavior
- Scene/entity/component structure
- Camera, controls, physics, animation, and asset integration notes
- Performance budget or likely bottlenecks
- Implementation plan or patch summary
- Verification steps and residual risks

## Composition Pattern

Use composition when an object needs mix-and-match capabilities, when scripts are growing into large player/enemy managers, or when the same behavior should work on players, enemies, props, items, projectiles, or environmental actors.

- Keep components single-purpose and context-light. A health component owns life, death, damage, and healing; it should not know whether it belongs to a player, skeleton, chest, or destructible wall.
- Let components communicate through signals, events, messages, or narrow typed interfaces instead of reaching deeply into each other.
- Use an orchestrator for entity-level state. A player, enemy, or vehicle script can coordinate input, movement, attack, animation, and lockout states without doing their internal work.
- Prefer editor/inspector-wired references, typed exports, serialized fields, node references, or dependency injection over fragile path/name lookups where the engine supports them.
- Test reusable components in isolated scenes or minimal harnesses before attaching them to complex entities.
- Avoid over-fragmenting behavior that changes together every time. Composition is useful when the pieces can be reused, tested, swapped, disabled, or reasoned about independently.

For Godot-style projects, treat child nodes as components when that matches the project style: use `class_name` for reusable component types, exported typed references for explicit wiring, signals for decoupled notifications, and scene-unique names only where appropriate. For Unity-style projects, map the same principle to focused `MonoBehaviour` components and serialized references. For Unreal, map it to Actor Components, interfaces, events, and Blueprint/C++ ownership boundaries.

## References

- Read `references/3d-review-checklist.md` when reviewing or finishing a 3D feature, especially before claiming it is playable or production-ready.
- Read `references/composition-architecture.md` when a gameplay entity, Godot scene, Unity prefab, Unreal actor, or custom-engine object is becoming hard to extend because too much behavior lives in one script or inheritance tree.
