---
name: unreal-animate-actors
description: Integrate Unreal skeletal animation, montages, and root motion with safe gameplay-event and interruption ownership.
engines: [UNREAL]
---

# Unreal Animate Actors

## When to use

Integrate Unreal skeletal animation, montages, and root motion with safe gameplay-event and interruption ownership. Use this feature for Unreal-owned game code and content.

## Activation and prerequisites

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh unreal-animate-actors` before edits or tool launches. Continue only when the effective engine is `UNREAL` and `compatible: true`. Skill selection never selects the engine. Honor any validated task override and its permitted isolated output scope.

Record Unreal version, skeleton and retargeting configuration, clips, Animation Blueprint ownership, movement/replication model, target platforms and animation budgets. Optional Control Rig or animation plugins remain explicit choices.

## Workflow

1. Inspect Skeleton compatibility, retargeting, mesh scale, bone hierarchy, sockets and imported clips. Preserve source identity and verify root bone behavior before wiring gameplay.
2. Define the Animation Blueprint's state machines, Blend Spaces, linked layers and parameters around a stable gameplay snapshot. Keep thread-safe animation evaluation distinct from game-thread UObject access. Use the [animation integration reference](references/animation-integration.md) when choosing evaluation, retargeting or action ownership.
3. Use Animation Montages, slots, sections and blend settings for directed actions. Track playback identity, completion and interruption; delayed callbacks from replaced montages must not complete the current action.
4. Choose in-place, extracted or movement-integrated root motion intentionally. Coordinate CharacterMovement and the selected network mode; animation displacement must not bypass collision or duplicate movement.
5. Treat AnimNotifies and notify states as lifecycle-bound event sources. Critical rules need authoritative validation if notifies are skipped, repeated, blended or interrupted; presentation-only timing must not decide damage.
6. Define IK, attachments and procedural rig evaluation order. Handle mesh changes, offscreen update policy, LOD and skeletal visibility without leaving stale equipment or frozen authoritative state.
7. Coordinate audio, particles, camera and bounded haptic feedback through event identities and explicit clocks. Preserve pause/slow-motion ownership and provide reduced-motion alternatives.
8. Adopt Pose Search/Motion Matching, Choosers, Control Rig or Motion Warping only when selected and supported by the actual project. Record database/rig dependencies, motion extraction assumptions and measured cost; do not add them as mandatory locomotion infrastructure.

## Verification

- Inspect blend seams, feet, sockets and root displacement in native captures at slow and normal playback.
- Test montage replacement, cancel, death, network correction and actor removal during notify windows.
- Profile representative skeletal counts and LOD/culling behavior on target hardware; compile Animation Blueprints and test a packaged actor.

## Output

Animation Blueprints/montages/rig setup, movement and event ownership contract, interruption tests, native visual captures and performance evidence. Record environment, scope, expected and observed results, evidence paths, and blocked or not-run checks separately from passes.

## Boundaries

An imported skeleton is not animation readiness. Do not create binary animation assets by text fabrication or enable rigging plugins silently. Independent tools and services retain their own architecture contracts.

## References

- [Unreal Animation Blueprints](https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-blueprints-in-unreal-engine). Match the documentation version to the project.
- [Unreal root motion](https://dev.epicgames.com/documentation/en-us/unreal-engine/root-motion-in-unreal-engine). Match the documentation version to the project.
- [Animation integration](references/animation-integration.md): evaluation ownership, montage cancellation, optional systems and native acceptance.

