---
name: character-kit
description: Put a playable walking character into any Three.js 0.187.0 WebGPU scene. Use when a scene, game or simulation needs a first or third person character that walks, runs, crouches and jumps over level geometry. Parents character-walking, character-camera, character-model and character-input.
---

# Character kit

Target: Three.js 0.187.0, WebGPU renderer (`three/webgpu`), TSL (`three/tsl`), Jolt 1.1.0
(`jolt-physics` WASM) for the capsule. No WebGL fallback, no GLSL, no model files.

A playable character is four independent pieces and a thin wiring layer. Keep them
separate: each is reusable on its own, and the wiring is the only place that knows
about the scene.

| Piece | Skill | Owns |
| --- | --- | --- |
| input | `character-input` | which keys mean which actions, pointer deltas, edge presses |
| walking | `character-walking` | the physics capsule and how it moves |
| camera | `character-camera` | where the camera is and where it looks |
| model | `character-model` | the visible figure and its animation |

The wiring layer (about 120 lines in the recipe below) reads input, decides a wish
direction from the camera yaw, moves the capsule, steps physics, then places the camera
or the model from the capsule's new position.

## Measurements

These are the numbers that make a character feel right on a metric level. Change them
only for a different genre.

| Quantity | Value |
| --- | --- |
| standing height | 1.8 m |
| crouch height | 1.0 m |
| capsule radius | 0.35 m |
| eye height standing / crouched | 1.6 m / 0.9 m |
| walk / run / crouch speed | 4 / 7 / 2 m/s |
| jump impulse | 8 m/s (about 1.6 m apex at g = 18) |
| gravity | 18 m/s² (stronger than Earth; makes jumps snappy) |
| max slope | 45° |
| step up | 0.55 m (one stair riser with margin) |
| stick to floor | 0.5 m (keeps feet down over bumps and down slopes) |
| crouch ease | 10 /s exponential |
| turn rate (third person facing) | 18 /s exponential |
| mouse sensitivity | 0.002–0.003 rad per pixel |
| third-person orbit distance | 3 m default, 1.2–14 m by scroll |
| orbit pitch range | 0.1 to 1.52 rad (never under the ground, never straight down) |
| camera fov | 75° |

## Boot order

1. Create the renderer, scene and camera as usual (`WebGPURenderer`, `await init()`).
2. `createCharacterInput(canvas)` and `input.setLookMode('drag' | 'capture')`.
3. Initialise Jolt and build the physics world with two object layers (static and
   moving). The walking skill ships `createJoltCharacter(...)` that takes the Jolt
   module, the `JoltInterface`, the `PhysicsSystem` and the moving layer index.
4. Build level geometry and add a collider for every solid mesh. A floating mesh with
   no collider is a bug.
5. `createCharacterModel()` and add `model.root` to the scene.
6. Create the cameras: `createCameraManager(camera, { fov })`,
   `createFirstPersonCamera(...)`, `createThirdPersonCamera(...)`.
7. Create the walker: `createWalker({ character, input, ... })`.
8. Start the animation loop.

## Frame order

Every frame, in this order. The order matters: the camera must consume the pointer
delta before the wish direction is computed from its yaw, and physics must step before
anything reads the capsule.

```js
const update = (dt) => {
  crouchHeld = input.isAction('crouch');
  walker.setCrouch(crouchHeld);                 // swaps the capsule shape when it can
  cameraManager.update(dt);                     // consumes look delta, updates yaw/pitch
  const yaw = firstPerson ? fp.rotation.yaw : tp.orbit.yaw;
  const move = input.getMove();                 // -1/0/1 axes, shared object
  const speed = crouchHeld ? 2 : (run ? 7 : 4);
  walker.move(move, yaw, speed, input.wasPressed('jump'), dt);
  physics.step(dt);                             // jolt.Step, clamp dt to 1/30, 2 substeps over 1/55
  const pos = walker.position();                // capsule centre, shared object
  if (firstPerson) camera.position.set(pos.x, pos.y + eye(t) - radius, pos.z);
  else { model.setTransform(feetY, pos.x, pos.z, facing, t); model.update(dt, { speed, grounded, runSpeed: 7 }); }
};
```

Edge presses (`wasPressed`) are cleared at the end of the frame, after all consumers,
not when read. The input skill explains the late-update hook.

## Interfaces between pieces

- Input to walking: `getMove()` gives `{ x, z }` in -1/0/1; `isAction(name)`;
  `wasPressed(name)`.
- Camera to walking: a yaw in radians. The walker rotates the move axes by yaw so the
  caller never does trigonometry.
- Walking to camera and model: `position()` (capsule centre), `grounded`, the current
  capsule height. Objects returned every frame are shared scratch objects; copy them if
  kept.
- Model to nothing: it only receives `setTransform` and `update`.

## Conventions worth keeping

- Factory functions and closures, no classes. Each factory returns a plain object.
- No per-frame allocation in hot paths: reuse `Vector3`, `Euler`, result objects.
- The capsule's feet are at `centre.y - (height/2 - radius)`; eye height is measured
  from the feet. Do not place the camera at the capsule centre plus a constant.
- Crouch is a shape swap, not a scale: Jolt refuses the swap if the standing capsule
  would intersect a ceiling, so the character stays crouched under a table. Ease the
  visible height toward the capsule height so the camera and model do not pop.
- Standing still on an edge must not creep: the ground normal tilts on a lip, so zero
  the horizontal velocity when there is no wish direction and the character is on ground.
- Gravity, speeds and heights live in one constants object; the model and camera read
  heights from the walker, not from their own copies.

## Pitfalls

- `dt` from `requestAnimationFrame` must be clamped (1/30) before physics or a tab
  switch becomes a launch.
- The third-person camera needs a smoothed follow target (16 /s exponential) or
  physics jitter shows as camera jitter.
- Pointer lock can be refused (embedded pages, some browsers); keep drag look as the
  fallback and never block on the lock.
- Jolt objects are WASM: destroy temporary `Vec3`/`RVec3`/settings after use, and call
  `Quat.prototype.sIdentity()` fresh each time rather than caching the result.
