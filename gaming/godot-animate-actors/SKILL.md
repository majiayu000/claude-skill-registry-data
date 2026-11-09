---
name: godot-animate-actors
description: Integrate Godot AnimationPlayer and AnimationTree with movement, event lifetimes, and safe interruption behavior.
engines: [GODOT]
---

# Godot Animate Actors

## When to use

Integrate Godot AnimationPlayer and AnimationTree with movement, event lifetimes, and safe interruption behavior. Apply this feature only to Godot-owned code and content.

## Activation and prerequisites

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh godot-animate-actors` before edits or tool launches. Continue only when the effective engine is `GODOT` and the skill is eligible. Skill selection never selects the engine. Honor validated task override evidence and its permitted isolated output scope.

Read Godot version, project language, source clips and skeletons, animation import settings, AnimationPlayer/AnimationTree ownership, root-motion policy and actor budgets. Preserve the project's chosen 2D or 3D approach.

## Workflow

1. Inspect imported clip names, tracks, skeleton compatibility, scale and looping. Identify property tracks that mutate shared Resources and make per-instance ownership deliberate before runtime editing.
2. Use AnimationPlayer for authored timelines and AnimationTree for selected blending/state-machine control. When AnimationTree drives playback, avoid a second independent controller issuing conflicting AnimationPlayer play commands.
3. Define parameters, transitions, blend positions and AnimationNodeStateMachinePlayback travel behavior around stable gameplay state. Expose a bounded animation adapter instead of allowing every component to write blend parameters.
4. Integrate extracted root motion with the chosen physics controller explicitly. Track position/rotation deltas in the right space and handle loops; movement must not apply both animation displacement and independent locomotion.
5. Define event identity and ownership for method/audio tracks, animation_finished and state callbacks. Looping, interruption and blended tracks can alter callback behavior; critical gameplay rules require authoritative validation.
6. Specify cancellation, transition restoration, pause behavior and node teardown. A queued callback or awaited completion from a freed/replaced actor must not complete the new actor's action.
7. Coordinate attachments, IK or selected procedural systems in their correct evaluation phase, and feed audio/VFX/camera/haptic requests from bounded events with explicit clock ownership.

## Verification

- Review blending, loop seams, root displacement and attachments in native captures with representative 2D/3D actors.
- Test interruption, death, state re-entry, missing clips, paused trees and animation owner removal.
- Measure animation work and imported resources at representative actor counts; verify offscreen processing choices do not control authoritative state.

## Output

AnimationPlayer/AnimationTree and resource changes, parameter/root-motion/event ownership contracts, interruption fixtures and native visual/performance evidence. Record environment, scope, expected and observed results, evidence paths, and blocked or not-run checks separately from passes.

## Boundaries

Do not introduce rigging plugins, claim an imported skeleton is a finished animation system or translate animation scripts to another project language. Independent services and tools retain their architecture contracts.

## References

- [Godot AnimationTree](https://docs.godotengine.org/en/stable/tutorials/animation/animation_tree.html). Select the documentation matching the project release.
- [Godot AnimationPlayer](https://docs.godotengine.org/en/stable/classes/class_animationplayer.html). Select the documentation matching the project release.

