---
name: unreal-build-movement
description: Build Unreal locomotion and network movement through CharacterMovement or an explicitly selected Mover implementation.
engines: [UNREAL]
---

# Unreal Build Movement

## When to use

Implement locomotion modes, collision-aware character movement, root-motion displacement or movement prediction. General rigid-body simulation belongs to physics; input bindings remain controls.

## Activation and prerequisites

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh unreal-build-movement` before edits or tool launches. Require effective engine `UNREAL` and `compatible: true`; revalidate task override evidence and permitted output scope. Skill selection never selects the engine.

Read actor type, engine release, selected movement implementation, animation/root motion, navigation agent and network topology. Mover is an explicit version-qualified selection. Keep observed context/evidence in resolved `.hephaera/.cache/tasks/<task>/`; preserve `ENGINE.md`.

## Workflow

1. Give locomotion one transform authority: existing CharacterMovement or the selected Mover path. Route player and AI intent into it rather than adding a competing transform loop.
2. Specify movement modes/transitions, acceleration/braking, gravity, floor/slope/step behavior and collision shape in project units. Define blocked movement, moving bases, teleport and recovery.
3. Integrate root motion and motion warping through supported animation/movement seams. Distinguish visual pose from authoritative displacement and reconcile interruption or mode change.
4. Extend CharacterMovement saved-move/compressed/network data where required by custom modes. Preserve replay/correction, validate server inputs and bound/quantize custom payloads instead of replicating arbitrary per-frame state.
5. For explicitly selected Mover, inspect plugin maturity, backend, supported features and platform limitations. Resolve migration of input, animation, navigation and multiplayer before replacing an existing system.
6. Cancel owned movement on stun, unpossession, AI abort, death and relevant pause. Clear stale input/path intent so replacement pawns cannot receive previous-generation commands.
7. Profile collision sweeps, movement updates, correction magnitude/frequency and representative crowds against project budgets.

Read [locomotion and prediction boundaries](references/locomotion-prediction-boundaries.md) when extending movement or integrating networking.

## Verification

Exercise slopes/steps, blocked movement, moving bases, root-motion interruption, mode changes and stop/disable behavior. Use separate server/client processes for replay and correction under latency/loss. A standalone sweep is collision evidence, not networking evidence.

## Output

Locomotion ownership/mode graph, native movement configuration/extensions, bounded prediction payloads and separated standalone/network/player evidence. Record environment, expected/observed outcomes and blocked/not-run checks.

## Boundaries

No implicit plugin activation, installation or movement-system migration. Match host headers and target platform. Preserve native asset authoring, budgets and approval/publication gates.
