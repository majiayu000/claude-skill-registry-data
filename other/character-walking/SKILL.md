---
name: character-walking
description: Walking, running, crouching and jumping on a physics capsule in Three.js 0.187.0 with Jolt 1.1.0. Use when a character has to move over level geometry, climb stairs and slopes, ride moving platforms, and not slide off edges. Ships walking-controller.js.
---

# Character walking

Target: Three.js 0.187.0 WebGPU, Jolt 1.1.0 (`jolt-physics` WASM, `jolt-physics.wasm-compat.js`).

`scripts/walking-controller.js` has two parts:

- `createJoltCharacter(Jolt, jolt, physicsSystem, opts)`: builds a `CharacterVirtual`
  capsule with standing and crouching shapes and the filters it needs, and exposes the
  four calls the controller uses.
- `createWalker({ character, gravity })`: turns a wish direction, a camera yaw, a speed
  and a jump flag into capsule velocity, with the rules below.

The controller only needs the adapter interface, so another physics library can be
used by writing an adapter with the same four calls: `setCrouch(bool)`,
`extendedUpdate(velocity, dt)`, `state()` and `teleport(x, y, z)`.

## The rules that make walking feel right

1. **Horizontal velocity is set, not accelerated.** Each frame the horizontal velocity
   becomes `wishDir × speed`. No momentum, no acceleration curve. This is what makes
   WASD feel direct; the physics step still resolves collisions and slopes.
2. **Vertical velocity is kept.** Read the current velocity along `up`, keep it, add
   gravity × dt, add the jump impulse if jumping from ground. On ground and moving
   toward it, vertical is replaced by the ground velocity so stairs and slopes do not
   bounce.
3. **Ride what you stand on.** If the ground body is dynamic and heavy enough to carry
   you (mass ≥ 20 kg), start from the ground velocity instead of zero. Standing on a
   light crate does not drag the crate with you.
4. **Jump only from ground**, on the edge of the key press (not while held), and never
   while crouched. Impulse 8 m/s along `up`.
5. **No creep on edges.** When there is no wish direction and the character is on ground
   or steep ground, zero the horizontal velocity after the update. Contact normals on a
   lip otherwise push the capsule off slowly.
6. **Crouch is a shape swap** between a 1.8 m and a 1.0 m capsule. Jolt refuses the swap
   back to standing when there is no headroom; keep asking every frame and the
   character stands up as soon as it can. Ease the visible height toward the capsule
   height at 10 /s so nothing pops.
7. **Stairs and bumps** are handled by Jolt's `ExtendedUpdate` with step-up 0.55 m and
   stick-to-floor 0.5 m. Do not write your own step logic.
8. **Clamp dt** to 1/30 before stepping. Use two substeps when dt is over 1/55.

## Capsule

- Radius 0.35 m, standing height 1.8 m, crouch height 1.0 m.
- The shape is a capsule translated up so the body origin is at the feet; the
  controller reports the centre (`feet + height/2`) so cameras and models can derive
  feet and eyes from one number.
- Max slope 45°, mass 80 kg, max strength 100 N (how hard the character pushes dynamic
  bodies), padding 0.02 m, penetration recovery 0.5, predictive contact 0.1 m,
  supporting volume plane at `-radius` so the character is supported by the bottom
  hemisphere only.
- Collide with back faces, so a character spawned slightly inside a wall is pushed
  out rather than falling through.

## Wiring with the rest of the kit

```js
import initJolt from 'jolt-physics';
import { createJoltCharacter, createWalker, CHARACTER } from './walking-controller.js';

const Jolt = await initJolt();
// ... JoltSettings with two object layers (0 static, 1 moving), JoltInterface `jolt`,
//     physicsSystem = jolt.GetPhysicsSystem(), gravity set on the system ...
const character = createJoltCharacter(Jolt, jolt, physicsSystem, { movingLayer: 1,
  position: { x: 0, y: 2, z: 0 } });
const walker = createWalker({ character, gravity: 18 });

// per frame, after the camera consumed the look delta:
walker.setCrouch(input.isAction('crouch'));
walker.move(input.getMove(), yaw, speed, input.wasPressed('jump'), dt);
jolt.Step(Math.min(dt, 1 / 30), dt > 1 / 55 ? 2 : 1);
const s = walker.state(); // { x, y, z, grounded, height, crouched, velocityY }
```

`walker.move` rotates the input axes by the camera yaw: forward is the camera's
forward on the ground plane. The caller never does the trigonometry.

## Level geometry

Every solid mesh needs a collider in the static layer. Boxes for walls, floors, stacks
and ramps (a rotated box is a ramp); convex hulls for oddly shaped props; a triangle
mesh only for terrain or large imported geometry. Keep stairs as boxes with 0.17 m
risers and the step-up setting handles them.

## Moving platforms and vehicles

The controller rides any ground body whose entry carries a mass of 20 kg or more. Register
vehicle chassis and platforms as dynamic bodies with their real mass; the character
then moves with them and jumps off with their velocity.

## Swimming and wind

Out of scope here; the source project adds water volumes (buoyancy, surface walk) and
force fields on top of this controller by adjusting the vertical velocity before the
update. The hook for that is the single place where velocity is assembled in
`createWalker`.

## Pitfalls

- Do not scale the capsule for crouch; swap shapes.
- Do not set the camera from the capsule centre plus a constant; derive feet first.
- `GetPosition()` on a `CharacterVirtual` returns the feet (shape origin), not the
  centre. The adapter adds the half height.
- Destroy temporary Jolt `Vec3`/`RVec3`/settings after use; the WASM heap does not
  garbage-collect them. Call `Quat.prototype.sIdentity()` fresh every time.
