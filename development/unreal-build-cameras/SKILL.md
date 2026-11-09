---
name: unreal-build-cameras
description: Build Unreal player cameras, view transitions and camera effects with explicit ownership, interruption and accessibility controls.
engines: [UNREAL]
---

# Unreal Build Cameras

## When to use

Implement or revise Unreal gameplay cameras, spectator views, camera rigs, collision, modifiers or camera shakes. Sequencer orchestration belongs to the cinematics capability; this skill owns the player's camera integration and restoration.

## Activation and prerequisites

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh unreal-build-cameras` before writes or tool launches. Require effective engine `UNREAL` and `compatible: true`; respect validated task overrides and every permitted output scope. The skill does not choose an engine.

Inspect the actual engine version, local-player/controller ownership, CameraManager class, possessed actors, camera components, target platforms, motion settings and budgets. Gameplay Cameras and other camera plugins remain explicit, version-qualified selections.

## Workflow

1. Identify the single owner choosing each local player's view target. Separate replicated gameplay orientation and authoritative aiming from local presentation offsets.
2. Define camera states and interruption priority for gameplay, aim, lock-on, spectator, death, UI and cinematic views. Keep handles/identities for temporary claims and restore a valid current fallback when the owning claim ends.
3. Use the selected PlayerCameraManager, CameraComponent and SpringArm arrangement. Set transform/tick order, collision probe/channel, ignored actors, lag and teleports deliberately; read [camera ownership](references/camera-ownership.md) for native API choices.
4. Use declared blend times and clocks. Replaced targets, destroyed actors, possession and travel must cancel obsolete transitions rather than restore stale view targets.
5. Bound CameraModifiers, shakes and FOV changes per player. Remove only owned effects; support reduced motion, intensity and unsupported target behavior. Camera response and haptic feedback never decide gameplay outcomes.
6. If an optional camera framework is selected, adapt to its version and ownership model rather than layering a competing manager. Record plugin/assets, required modules and unsupported paths before implementation.

## Verification

Test rapid view replacement, old-claim cancellation, target destruction, respawn, spectator transitions, split-screen and travel. Check wall probes, slopes, narrow spaces, teleports and frame-rate variation in a native session. Capture horizon stability, occlusion, clipping, aim alignment and accessibility settings on the intended target; headless view-target assertions cannot certify camera comfort.

## Output

Native camera code/assets, ownership and restoration map, selected plugin/version evidence, declared blend/clock/effect limits, lifecycle tests and representative native captures. Record environment, scope, expected/observed behavior and blocked/not-run checks under the active `.hephaera/.cache/tasks/` task.

## Boundaries

Do not select plugins, install tooling or alter art/media contracts implicitly. Author binary camera assets with actual native tools. Retain existing independent art review and promotion gates.

## References

- [Camera ownership](references/camera-ownership.md): API selection, stale claims, collision and native acceptance.
