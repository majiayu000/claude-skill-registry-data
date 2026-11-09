---
name: threejs-animate-actors
description: Integrate Three.js AnimationMixer clips, actor blending, attachments and animation teardown without handing gameplay authority to playback.
engines: [THREEJS]
---

# Animate Three.js Actors

## When to use

Connect actor clips to gameplay state, blend actions, attach props, or repair animation lifecycle defects.

## Engine and dependencies

Before edits or tool launches, run `resolve-engine.sh` and `resolve-skill.sh threejs-animate-actors`; require compatibility and respect task override scope. Inspect the locked Three.js version, rig/clip contract, movement authority and art pipeline. Integrate authorized assets; do not implicitly select generation or install packages.

## Workflow

1. Validate hierarchy, rest pose, scale, clip names, durations and bindings. Use the installed revision's skeleton-aware cloning approach for skinned actors; independent copies must not accidentally share mutable bone state.
2. Own an `AnimationMixer` per appropriate animation root. Cache `clipAction` results and explicit transitions. Set looping, clamping, weight and time scale deliberately; resetting and cross-fading are distinct operations.
3. Update mixers from the declared presentation clock in seconds. Decide pause, slow motion and offscreen behavior; never advance one mixer from two loops. Interruption cancels pending completion effects and restores a valid pose.
4. Choose in-place motion or an explicit root-motion extraction adapter. Feed extracted intent through authoritative movement/collision and avoid double translation. Three.js supplies playback, not a collision-aware controller.
5. Drive damage, inventory and ability outcomes from simulation. Completion/loop events are presentation signals or validated inputs under the gameplay contract; repeated or stale events cannot duplicate outcomes.
6. Attach equipment to named bones/sockets with declared offsets. On despawn remove listeners, stop actions and release mixer caches with appropriate uncache methods. Release shared assets only after their final owner leaves.

## Output and verification

Deliver a clip manifest, transition adapter, clock/movement ownership and teardown. Test missing clips, interruption, independent copies, pause/resume, spawn/despawn cycles and frame-rate variation. Record foot sliding, prop alignment and blends in the actual browser; mixer-state tests do not prove pose quality. Check the [AnimationMixer API](https://threejs.org/docs/pages/AnimationMixer.html) against the locked version.
