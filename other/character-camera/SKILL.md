---
name: character-camera
description: First-person look and third-person orbit cameras for a walking character in Three.js 0.187.0, with drag or pointer-lock steering, scroll zoom and smoothed follow. Use when a scene needs a player camera attached to a moving body. Ships character-camera.js.
---

# Character camera

Target: Three.js 0.187.0 WebGPU. `scripts/character-camera.js` exports
`createCameraManager`, `createFirstPersonCamera` and `createThirdPersonCamera`. They
depend only on `three/webgpu` and on an input object that provides
`consumeMouseDelta()` (see `character-input`).

## Model

A camera manager owns the `PerspectiveCamera` and one active controller function
`(camera, dt) => void`. The two controllers are factories that keep their own state
(yaw and pitch) and return a bound controller when given the input and a target getter.
Switching views is `manager.setController(...)`; nothing else changes.

```js
const manager = createCameraManager(camera, { fov: 75 });
const fp = createFirstPersonCamera({ sensitivity: 0.003 });
const tp = createThirdPersonCamera({ distance: 3, height: 0.5, sensitivity: 0.003 });
manager.setController(fp.bind(input, () => opts));            // first person
manager.setController(tp.bind(input, getAnchor, () => opts)); // third person
manager.update(dt); // once per frame, before the wish direction is computed
```

`getAnchor` returns the point the orbit looks at: the character's capsule centre plus
45 % of the model height from the feet (chest height), as a shared object.

## First person

- Yaw and pitch in an `Euler` with order `'YXZ'`, applied as the camera quaternion.
- Pitch clamped to ±(π/2 − 0.01): looking straight up or down must not flip.
- Sensitivity 0.002–0.003 rad per pixel; invert is a sign on pitch only.
- Position is set by the wiring layer from the capsule: `centre.y + eyeHeight − radius`
  where eye height is 1.6 m standing, 0.9 m crouched, eased.
- The visible model is hidden in first person.

## Third person

- Spherical orbit around a smoothed target: the target follows the anchor with a
  16 /s exponential rate, which hides physics jitter without lag you can feel.
- Pitch range 0.1 to π/2 − 0.05 rad: never under the ground plane, never straight down.
- Distance 3 m default, scroll in 0.45 m steps between 1.2 and 14 m.
- Height 0.5 m above the anchor.
- Facing of the model follows the wish direction at 18 /s, not the camera, so the
  character turns to where it walks while the camera stays where the player left it.
- No collision with walls in this kit; if walls are common, cast a ray from target to
  camera and shorten the distance to the hit.

## Switching views

Carry the yaw across: entering third person copies the first-person yaw into the orbit
and sets the model facing to the camera forward; entering first person copies the orbit
yaw back. The player never has to re-find the direction they were looking.

## Vehicles and follow targets

To attach the camera to something else (a vehicle, a cutscene subject), replace the
anchor getter and hide the model; `aimOrbitBehind(subjectYaw)` puts the orbit behind the
subject with a 0.32 rad pitch. Restoring the player's anchor restores the view.

## Pitfalls

- Consume the pointer delta exactly once per frame, in the camera update. Reading it
  elsewhere steals the look.
- Keep `camera.up` at +Y in the orbit and call `lookAt` after setting the position.
- Update the projection matrix only when the fov actually changes.
