---
name: phaserjs-build-physics
description: Implement explicitly selected Phaser Arcade or Matter physics with correct body ownership, collision filtering and stepping.
engines: [PHASERJS]
---

# Build Phaser Physics

## When to use

Build Phaser movement/collision, triggers, constraints or physics-aware gameplay adapters.

## Engine and dependencies

Before edits or tool launches, run `resolve-engine.sh` and `resolve-skill.sh phaserjs-build-physics`; require compatibility and honor task override scope. Read the host revision and require an explicit Arcade or Matter choice. Preserve an existing choice unless migration is requested. Do not add middleware or automatically switch solvers when a requested shape is unsupported.

## Workflow

1. Use Arcade for its supported axis-aligned rectangles/circles and lightweight collision model; use Matter for selected rigid-body, rotated/compound shape or constraint needs. `this.physics` and `this.matter` are different plugins; bodies do not collide across their separate worlds.
2. Configure world units, gravity, solver timing, bounds and pause behavior. Choose one stepping owner and a bounded resume policy. Verify the installed plugin's time-scale semantics rather than copying another subsystem's multiplier.
3. For Arcade, declare body sizes/offsets, static versus dynamic groups, `collider` versus `overlap`, and process filters. Refresh static bodies after supported transform changes. For Matter, declare fixtures, collision categories/masks, sensors, constraints and rotation policy through the version's APIs.
4. Physics owns movement of dynamic bodies; avoid competing tweens/direct position writes. Teleport/reset must synchronize body and display state. Navigation/AI submits movement intent to this adapter rather than bypassing collision.
5. Translate contacts into stable entity IDs and bounded simulation events. Protect triggers from duplicate processing, despawn during callbacks and invalid state transitions. Save validated gameplay state rather than plugin object graphs; fixed stepping alone does not guarantee deterministic cross-device replay.
6. Remove owned colliders, constraints and world listeners on shutdown; pooled actors must reset velocity, contacts, flags and body activation before reuse.

## Output and verification

Deliver solver selection, movement/trigger adapters and a runnable collision fixture. Verify grounding, sensors, fast movement, masks, teleports, pooled reuse, pause/resume and restart at varied frame rates. Record solver limits and observed misses. Mock collision callbacks cannot certify physics. Consult the [Arcade contract](https://docs.phaser.io/phaser/concepts/physics/arcade) and selected version's Matter reference.
