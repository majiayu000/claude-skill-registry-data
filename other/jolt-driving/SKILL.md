---
name: jolt-driving
description: Use when a Three.js scene needs a drivable wheeled vehicle (car, truck, SUV, optionally towing a trailer) on Jolt physics (jolt-physics wasm-compat) over streamed heightfield terrain. Ships a Jolt world (layers, fixed step, body helpers, heightfield chunks, budgeted retirement, guarded ray casts), a tuned VehicleConstraint vehicle with per-surface tyre grip, and a trailer hitch.
---

# Jolt driving

Target: Three.js 0.187.0 (`three` for the maths; the kit draws nothing) and jolt-physics 1.0.0, the `wasm-compat` build. Three companion files sit in this folder. Copy them into the project. They import only `three`, and the caller passes in the Jolt namespace it initialised:

- `scripts/jolt-world.js`: `createJoltWorld(Jolt, options)` and `createHeightfieldRing(world, samplesFor, options)`
- `scripts/jolt-vehicle.js`: `class WheeledVehicle`, `VEHICLE_DEFAULTS`, `SURFACES`
- `scripts/jolt-towing.js`: `class TowHitch`, `TRAILER_DEFAULTS`

## What it is

A four-wheel vehicle driven by Jolt's own `VehicleConstraint` and `WheeledVehicleController`. Jolt solves suspension, tyre slip, weight transfer and the drivetrain. On top sits a thin handling layer, and every constant in it was settled by driving tests. It covers steering smoothing and taper, a brake pedal that reverses once the vehicle has stopped, a holding brake with hysteresis, a park pin that puts the body to sleep, friction curves per surface, a handbrake slide, extra gravity in the air, water buoyancy and drag, and a fell-through net. Around the vehicle the kit has a world with two layers, heightfield colliders only in the 3x3 chunks around the vehicle, a mesh-shape queue, body retirement on a budget, and ray casts that cannot hang. A trailer couples to it with a swing-twist joint.

## When to use

- Driving games and simulations where the car should feel physical (suspension, body roll, grip loss), not arcade-on-rails.
- Large streamed terrain: colliders follow the vehicle, and the rest of the world has none.
- Use something else for a kinematic or arcade car with no real physics, for a pure flight model, or for tracked vehicles (Jolt has a `TrackedVehicleController`, but this kit does not cover it).

## API

### `createJoltWorld(Jolt, options)` (defaults in `WORLD_DEFAULTS`)

Returns `{ Jolt, jolt, physicsSystem, bodyInterface, layers: { NON_MOVING, MOVING }, fixedDt, step, ... }`.

- `step(frameDt, beforeEachStep)`: runs the fixed-step accumulator. `beforeEachStep(dt)` runs before every `jolt.Step`. Vehicle and trailer updates go there, never once per frame. Returns `alpha` for pose blending.
- `createDynamicShape(shape, { position, rotation, mass, friction, restitution, angularDamping, allowSleeping, activate })`: mass is overridden and inertia is calculated from the shape.
- `createDynamicBox({ x, y, z, hx, hy, hz, mass, rotation?, friction = 0.8 })` and `createDynamicCylinder({ x, y, z, halfHeight, radius, mass, rotation?, friction = 0.6 })`: props. They are created asleep and contacts wake them.
- `createStaticBox({ x, y, z, hx, hy, hz, rotation? })`: uses an LRU box-shape cache.
- `createStaticCompound(boxes, ox, oz)`: one body for a chunk's prop boxes, in a frame at (ox, 0, oz). Returns `null` on failure; then call `createStaticBox` per box.
- `createStaticMeshQueued({ key, positions, indices, x, y, z, rotation?, isCancelled? })` returns a Promise of a Body. `pumpMeshQueue(perFrame = 1)` builds that many new shapes per call. Cached keys resolve at once. A cancelled request resolves `null`.
- `createHeightfieldChunk({ x, z, size, cells, heights })`: `heights` is a Float32Array of `(cells+1)^2` world heights, row-major (i along +x, j along +z). It covers [x, x+size] x [z, z+size]. It throws on a wrong length or on a non-finite or out-of-range sample.
- `removeBody(body)` removes and destroys a body now. `retireBody(body)` queues it, and `pumpRetired(n = 64)` destroys n per call.
- `castRay(from, dir, maxDist, { ignoreBody })` returns `{ fraction, distance, point, bodyId }` or `null`. Non-finite rays and rays longer than `maxRayLength` are refused.
- `boxShape(hx, hy, hz)` and `compoundShape(boxes, spheres, com)` build shapes. They are used by the vehicle and the trailer.

### `createHeightfieldRing(world, samplesFor, options)` (`RING_DEFAULTS`)

`samplesFor(cx, cz)` returns `{ heights, cells }`, or `null` while that chunk is not ready. Chunk (cx, cz) covers `[cx*size, (cx+1)*size]`. The ring has these methods:

- `update(x, z)` (per frame): builds the chunk under the point at once, then the nearest missing chunks within `radius` (`buildsPerFrame` per call). It retires chunks beyond `keepRadius`.
- `ensure(x, z)` builds the chunk under a point now and returns `true` if a collider is there. `has(x, z)` only checks.
- `remove(cx, cz)` and `dispose()`.

### `new WheeledVehicle(world, options)` (`VEHICLE_DEFAULTS`)

- `update(dt, input, env)`: call once per fixed step, inside `beforeEachStep`.
  - `input` is `{ throttle 0..1, brake 0..1, steer -1..1 (+1 = right), handbrake bool, reverse bool }`.
  - `env` is `{ surfaceAt(x, z) -> surface name, waterLevelAt(x, z) -> y | null, groundContact bool, heightAt?, wetness 0..1 }`.
  - `groundContact` says whether the collider under the vehicle exists (`ring.ensure(x, z)`). When it is `false`, the chassis is held on `heightAt` instead of falling.
- Getters: `speed` (horizontal m/s), `speedKmh`, `fwdSpeed` (signed along the heading, updated each step), `pose` ({ position, quaternion, yaw }), `airborne`, `inWater`, `braking`, `reversing`, `wheelContacts[i]` ({ x, y, z, grounded, surface }), `renderFwd` (the blended heading: use it as a chase camera's yaw source).
- `applyPoseTo(object3D, wheels, alpha)`: call once per render frame. It sets the object's blended pose. Each wheel Object3D must be hub-centred with its axle along x. It is placed at the mount minus the suspension length, steered and spun.
- `modelTransform(rawHalfWheelbase, rawAxleMidZ)` returns `{ scale, position }` for a body model hung under the posed object. The scale comes from the wheelbase and the offset puts the model at rest height.
- `reset(position, yaw)`: upright and still. A missing `position.y` means `heightAt + ride`. `flip()` sets it upright in place with its heading kept. `place(position, quaternion)` and `hold(y)` are also available.
- `fitChassisBox(hx, zMin, zMax)` refits the collider to another body shell. `towing` is set by the hitch. `dispose()`.

### `new TowHitch(world, tractor, trailerOptions)` (`TRAILER_DEFAULTS`)

- `place(x, z, yaw, heightAt)`. `canAttach()` and `attach()`, `canDetach()` and `detach()`.
- `update(dt, { groundSolidAt(x, z) })`: once per fixed step, after the tractor's update.
- `applyPoseTo(object3D, wheels, alpha)`: `wheels` is either one axle pivot or one object per wheel, as children of `object3D`.
- `save()` returns `{ x, y, z, qx, qy, qz, qw, attached }`. `restore(state, heightAt)` re-attaches by itself once it can. `dispose()`.

## Usage

```js
import initJolt from 'jolt-physics/wasm-compat';
import * as THREE from 'three/webgpu';
import { createJoltWorld, createHeightfieldRing } from './jolt-world.js';
import { WheeledVehicle } from './jolt-vehicle.js';
import { TowHitch } from './jolt-towing.js';

const Jolt = await initJolt();
const world = createJoltWorld(Jolt);
const SIZE = 256, CELLS = 256;                      // collider grid = an exact subdivision of the visual grid
const ring = createHeightfieldRing(world, (cx, cz) => terrain.samples(cx, cz, CELLS), { chunkSize: SIZE });
const heightAt = (x, z) => terrain.height(x, z);    // the same surface the heightfield samples

ring.ensure(0, 0);                                  // solid ground before the vehicle exists
const car = new WheeledVehicle(world, { spawn: { x: 0, z: 0 }, heightAt });
const tow = new TowHitch(world, car, { mass: 300 });
tow.place(0, -6, 0, heightAt);

const chassis = new THREE.Group(); scene.add(chassis);
const { scale, position } = car.modelTransform(0.84, 0.24);
bodyModel.scale.setScalar(scale); bodyModel.position.copy(position); chassis.add(bodyModel);
const env = { heightAt, surfaceAt: (x, z) => terrain.surface(x, z), waterLevelAt: (x, z) => lakes.level(x, z), groundContact: true, wetness: 0 };

function frame(dt) {
  const p = car.pose.position;
  ring.update(p.x, p.z);
  env.groundContact = ring.ensure(p.x, p.z);
  world.pumpRetired(); world.pumpMeshQueue(1);
  const input = { throttle: keys.w ? 1 : 0, brake: keys.s ? 1 : 0, steer: (keys.d ? 1 : 0) - (keys.a ? 1 : 0), handbrake: keys.space };
  const alpha = world.step(dt, (h) => { car.update(h, input, env); tow.update(h, { groundSolidAt: (x, z) => ring.has(x, z) }); });
  car.applyPoseTo(chassis, wheelMeshes, alpha);
  tow.applyPoseTo(trailerGroup, [trailerAxle], alpha);
}
// E key: tow.attached ? (tow.canDetach() && tow.detach()) : tow.attach();
```

Wheel meshes must be scene-level objects, not children of `chassis`. `applyPoseTo` writes world poses. Trailer wheels are the opposite: they are children of the trailer group, posed in its local frame.

## How it works

- **Chassis.** The collider is a box whose bottom is lifted by `bodyLift`; the top does not move. It is wrapped in `OffsetCenterOfMassShapeSettings` that drops the COM by `comDrop`. A box's own COM sits at axle height, far too high. The drop is the main anti-roll-over lever and does not change grip. In the measured test, full lock at full throttle peaked at 60 deg of tilt without it and 14 deg with it. The body never sleeps by itself (`mAllowSleeping` false); the park pin puts it to sleep explicitly.
- **Constraint.** Each wheel is a `WheelSettingsWV`: suspension straight down, the spring in frequency mode, its steer angle only if steerable, and handbrake torque only on the rear wheels. The transmission is `ETransmissionMode_Auto` with ONE forward ratio and one reverse ratio, so it never shifts and the torque curve stays flat. Two differentials at 0.5 each make it 4WD, and there are front and rear anti-roll bars. The collision tester is `VehicleCollisionTesterCastSphere` (radius = half the wheel radius). Then come `AddConstraint`, `AddStepListener(new VehicleConstraintStepListener(c))`, and `castObject(GetController(), WheeledVehicleController)` for `SetDriverInput(forward, right, brake, handBrake)`.
- **Top speed** is set by the drivetrain: wheel speed at max RPM = maxRPM x 2 pi / 60 / (gear x differential ratio, 3.42 by Jolt default) x radius, about 28 m/s here. Headless test: 0 to 89 km/h in 6 s and 102 km/h flat out. `topSpeed` (38 m/s) is the reference for the steering taper. Past it, the arcade drag bleeds the excess. It only engages downhill or with a stronger engine.
- **Friction per surface.** `mLongitudinalFriction` and `mLateralFriction` are LinearCurves (slip to friction), not scalars. The kit rebuilds them from Jolt's default points with Y scaled by the surface factors:
  - longitudinal: (0, 0), (0.06, 1.2), (0.2, 1.0) over slip ratio
  - lateral: (0, 0), (3, 1.2), (20, 1.0) over slip angle in degrees

  The friction is rewritten only when a wheel's key changes. The key is surface + wetness quarter + handbrake slide.
- **Pedals.** Throttle drives forward. Brake brakes while `fwdSpeed > 0.3`. Once stopped, a FRESH brake press reverses: releasing the pedal re-arms reverse, so holding the brake keeps the car stopped. `reverse: true` turns the throttle into a reverse throttle. With no pedal pressed, the holding brake engages below 0.5 m/s and releases above 1.0 m/s.
- **Per step, in order:**
  1. Hold the chassis if no collider is under it.
  2. Fell-through net: more than 2 m under `heightAt` means it is re-seated.
  3. Steering taper.
  4. Water impulses.
  5. Wheel contacts and friction keys.
  6. Driver input.
  7. Gravity factor, changed only when the airborne state changes.
  8. Handbrake assist.
  9. Top-speed drag.
  10. Park pin: zero the horizontal speed, keep only a downward settle (all of vy while towing), sleep below 0.05 m/s.
  11. Activation, only while something asks it to move.
  12. Visual wheel spin, integrated.
- **Render blend.** Each step stores the previous pose, spin, suspension and steer. `applyPoseTo` blends previous to current by `alpha`. Each stepped channel is blended; showing any one raw causes a hitch on frames that get 0 or 2 steps.
- **Heightfields.** `HeightFieldShapeSettings` takes mOffset (chunk corner), mScale (cell, 1, cell) and mSampleCount N. The samples are written straight into the WASM heap with `new Float32Array(Jolt.HEAPF32.buffer, Jolt.getPointer(hf.mHeightSamples.data()), N*N).set(heights)`. The body is static on the non-moving layer with friction 1.0. Every temporary is destroyed.

## Tuning: vehicle (`VEHICLE_DEFAULTS`)

| Constant | Value | Unit | What moving it does |
| --- | --- | --- | --- |
| halfExtents | 1.3, 0.65, 2.9 | m | collider box; fit it to the shell with `fitChassisBox` |
| bodyLift | 0.2 | m | the collider bottom sits above the visual underside; unlifted, the overhangs beach on concave breaks of 13 deg or more (lifted: about 21 deg) |
| comDrop | 0.45 | m | raise it if the car leans too far, lower it if it feels glued; the anti-flip lever |
| mass | 2000 | kg | heavier is slower to launch at the same torque |
| angularDamping | 0.5 | 1/s | lower is livelier after bumps |
| maxPitchRoll | 60 | deg | past this tilt the constraint stops driving |
| wheelRadius / wheelWidth | 0.49 / 0.28 | m | radius also sets top speed and visual spin |
| halfTrack / halfWheelbase / mountY | 1.02 / 1.65 / 0.15 | m | wheel mounts from the chassis centre |
| restHeight | 0.94 | m | chassis centre above the ground at rest; the model offset |
| suspRest | 0.7 | m | natural length; the car settles about 0.68 |
| suspMinFrac / suspMaxFrac | 0.40 / 1.25 | x rest | adding droop (more max) hangs the wheels and feeds roll rocking through the undamped bars |
| suspFrequency | 1.0 | Hz | heavy-vehicle ride; 1.4 Hz with 0.6 damping bounced like a ball off-road |
| suspDamping | 0.95 | ratio | near-critical: rebound absorbed, not stored |
| antiRoll | 600 | N/m | UNDAMPED springs; 2500+ pumped a growing roll oscillation; re-run a roll-kick test (2.2 rad/s; peaks must decay) before raising |
| castRadiusFrac | 0.5 | x radius | sphere cast: rolls over triangle edges, still climbs kerbs |
| maxSteer | 34 | deg | lock at walking pace |
| steerSmoothing | 0.12 | per step | higher is twitchier |
| highSpeedSteer | 0.7 | share | lock left at top speed (taper from 12 % to 78 % of 0.85 x topSpeed) |
| maxBrakeTorque | 6000 | Nm/wheel | Jolt's default of 1500 barely slows 2 t |
| maxHandBrakeTorque | 24000 | Nm | rear only |
| engineTorque / minRPM / maxRPM | 900 / 800 / 6000 | Nm / rpm | flat curve; wheel torque = engine x gear x diff ratio |
| gearRatio / reverseRatio | 3.2 / -3.2 | | the only gears; do not add a gearbox |
| clutchStrength | 10 | | |
| differentials | [0,1,0.5], [2,3,0.5] | | 4WD; [[2, 3, 1]] = RWD |
| topSpeed | 38 | m/s | steering taper reference and drag start |
| topSpeedDrag | 2.0 | 1/s | bleed rate of the excess; 0 = off |
| reverseRearmSpeed | 0.3 | m/s | below this the brake pedal may reverse |
| holdBrakeOn / holdBrakeOff | 0.5 / 1.0 | m/s | holding-brake hysteresis; one threshold lurches |
| parkPinSpeed / sleepSpeed | 0.35 / 0.05 | m/s | pin and sleep thresholds (tyres creep at mm/s on grades) |
| handbrakeLat | 0.35 | share | rear lateral grip with the handbrake held: lets handbrake turns rotate |
| handbrakeDecel | 12 | m/s^2 | extra decel while held (locked rears alone stop too slowly) |
| airGravity | 1.9 | x g | all wheels off the ground: jumps land sooner |
| wetLong / wetLat | 0.30 / 0.38 | share | grip lost at wetness 1 (quantised to quarters) |
| waterFloatOffset | 0.45 | m | float line above the chassis centre |
| waterBuoyancy / waterDamping | 14 / 4 | 1/s^2 per m, 1/s | lift per metre submerged, minus vertical speed damping |
| waterMaxLift | 22 | m/s^2 | lift cap |
| waterDrag / waterDragK | 3 / 0.9 | m/s^2, 1/s | horizontal drag; kept low so the engine can push out |
| fallThrough | 2 | m | under `heightAt` by this = re-seat at restHeight + 0.4 |
| spawnClearance | 0.15 | m | drop height above suspRest + radius on reset/flip |

Surfaces (`SURFACES`, long / lat / share of wetness): snow 1.00 / 1.00 / 0.5 (the tuned baseline), asphalt 1.05 / 1.18 / 1, wetAsphalt 0.735 / 0.73 / 0, ice 0.25 / 0.35 / 0. These four were tuned by driving. Gravel 0.95 / 0.85, dirt 0.92 / 0.90 and grass 0.80 / 0.80 (wetness 0.5) are interpolated and still need a driving test. Add entries through `options.surfaces`.

## Tuning: world, ring, trailer

| Constant | Value | Unit | What moving it does |
| --- | --- | --- | --- |
| fixedDt / maxSteps | 1/60 / 5 | s / steps | every vehicle constant is tuned at 60 Hz; after 5 steps the accumulator is dropped (no death spiral) |
| groundFriction / staticFriction | 1.0 / 0.75 | | heightfield grip baseline times the tyre curves |
| boxCacheMax | 512 | shapes | LRU of box shapes (random prop scales make the keys unbounded) |
| heightRange | +-1e5 | m | heightfield sanity window |
| retirePerFrame | 64 | bodies | destroying ~450 at once was a 5-25 ms stall; 64 a frame is 0.1 ms |
| maxRayLength | 1000 | m | longer rays are refused |
| ring radius / keepRadius | 1 / 2 | chunks | 3x3 colliders; nothing at distance 2 is ever touched by the wheels, trailers or dynamic props |
| buildsPerFrame | 1 | bodies | one heightfield is ~3.8 ms from pre-baked 257^2 samples |
| trailer mass / loadShare | 300 / 0.91 | kg / share | 7-9 % on the drawbar stops sway (COM low and ahead of the axle) |
| com | 0, -0.15, 0.10 | m | low and forward; behind the axle the trailer sways |
| sag / dampingRatio | 0.09 / 0.9 | m / ratio | k = wheel load / sag, c = 2 zeta sqrt(k m); explicit (frequency mode sat on the bump stops) |
| suspMin / suspMax | 0.06 / 0.22 | m | travel |
| antiRoll (trailer) | 300 | N/m | 1500 for a tall 1100 kg caravan |
| brakeTorque | 1200 | Nm | parking brake unhitched; 4000 for 1100 kg |
| overrun / start / range | off / 0.8 / 4 | m/s^2 | brake with the tractor's deceleration; unbraked, an 1100 kg caravan folded to 54 deg on a downhill brake in a turn, with it 0 deg |
| constraint yaw / tilt | 70 / 25 | deg | swing-twist limits: jackknife stop, pitch/roll cone; body boxes colliding stop it a little earlier |
| reach / attachMaxSpeed / detachMaxSpeed | 0.9 / 1.5 / 3 | m, m/s | coupling gates; attach also needs yaw under 0.9 x the limit |
| teleportGap | 1.0 | m | ball to coupler apart by more = the tractor was moved: let go before the solver flings it |
| sleepAfterSteps | 45 | steps | sleeping sooner froze it 4 cm low mid-settle |
| ballBehind / parkClearance | 0.10 / 0.25 | m | ball behind the tractor's box; drop height when placed |

## Pitfalls (each one cost a session)

- **Destroy every WASM temporary** (settings, Vec3, Quat, RVec3, BodyCreationSettings) after the body exists. Leaked per-chunk heightfield settings ran the Jolt heap out of memory (Aborted OOM) after minutes of streaming.
- **NaN rays hang the tab.** A ray built from a NaN or absurd camera position in the first boot frames sent Jolt's tree walk into an endless loop. `castRay` checks that the ray is finite and shorter than the length cap. Do the same for mesh vertices and indices before `MeshShapeSettings`, and for heightfield samples.
- **`MeshShapeSettings` needs three arguments** `(VertexList, IndexedTriangleList, PhysicsMaterialList)`. Two arguments resolve to another overload and crash with "table index out of bounds". Check `result.HasError()`.
- **Cached shapes need their own `AddRef()`.** The ShapeResult slot is overwritten by the next `Create()`. Without the ref, the shape dies with its first body and leaves a dangling pointer.
- **Friction is a curve.** `ws.mLateralFriction = 0.5` silently does nothing. `jw.GetSettings()` returns the base class, so `castObject` it to `WheelSettingsWV`; that object mutates the live wheel.
- **Do not detect contact with your own ground ray.** Its threshold disagrees with Jolt's suspension travel and flips the air-gravity state every step, which becomes a limit cycle. Use `GetWheel(i).HasContact()`.
- **Cast a sphere for the wheels.** A cylinder catches heightfield triangle edges (bounce, rocking). A ray has no width, so it drops into gaps and cannot climb kerbs.
- **Heightfield sampling must match the visual surface.** Make the collider grid an EXACT subdivision of the render mesh's grid, so triangle edges land on its bilinear kink lines; otherwise the collider bulges above the visible ground. The samples must include anything the wheels ride on (a road platform on an embankment). Bare terrain under an analytic road buried the wheels by up to 0.13 m on one shoulder.
- **Concave terrain features must stay wider than 3-4 cells** (12-16 m at a 4 m grid). Narrower gullies become vehicle traps for the mesh and the collider alike.
- **A clamp on velocity is a ratchet.** Keeping only the downward part of vy in the park pin lets the suspension sink but never rebound. Alone it never shows, because the body sleeps a moment later. With a trailer hitched, the joint wakes the tractor every step, and the drawbar load pushed the rear suspension down at a CONSTANT speed: 0.669 to 0.406 m in 13 s with 1100 kg, 2 mm/s with 300 kg. Fix: `towing` leaves vy alone, and the trailer sleeps WITH the tractor. LESSON: a slow constant-speed creep means something is clamping a velocity, not applying a force.
- **Activate only on demand.** Calling `ActivateBody` every step means a parked car never quiesces. The pin calls `DeactivateBody` itself.
- **Teleports.** After `SetPositionAndRotation`, reset the blend history (`place` does), or one frame renders the car halfway along the jump. Detach or move a trailer first. The teleport guard detaches it, but only on the next update.
- **Spawn order.** Build the collider under the spawn (`ring.ensure`) before the first step. Hold the vehicle on `heightAt` (`groundContact: false`) whenever the collider under it is missing, and keep a detached trailer asleep where `groundSolidAt` is false.
- **`slerpQuaternions(a, b)` is `copy(a).slerp(b)`.** If the destination is `b`, nothing happens. Use a separate scratch quaternion.
- **Steer sign.** `SetDriverInput`'s second argument is "right". With +Z forward and +Y up, right is -X, so a steered visual wheel turns by `rotateY(-angle)`.
- **SetShape frees the old shape.** Build a fresh shape for each swap (trailer jockey on/off). Never hand back one you have already let go of.
- **Trailer springs:** use `ESpringMode_StiffnessAndDamping`. Frequency mode sizes the spring from the effective mass at the wheel, which on a light trailer is mostly roll inertia (about 66 kg for a 300 kg trailer), and the trailer sat on its bump stops.

## Towing in short

The joint is a `SwingTwistConstraintSettings` in `EConstraintSpace_WorldSpace` at the ball. It is created after sliding the trailer the last centimetres onto the ball. Each body's twist axis is its OWN up and its plane axis its own forward, so zero means straight behind, whatever angle they coupled at. Twist covers +-70 deg of yaw; the normal and plane cones cover +-25 deg of pitch and roll. While hitched, the jockey sphere leaves the compound and the parking brake is released. `constraint: { type: 'point' }` swaps in a `PointConstraintSettings` (no limits; the bodies' own collision is the only jackknife stop). A drop hitch is a visual matter: hang the ball mesh on the TRACTOR at the joint. If it hangs on the trailer, its tube swings out from under the tractor in every turn. Saving: `save()` goes into the game save. `restore()` holds the trailer asleep until its ground is solid, then keeps trying `attach()` for 25 s of steps. Time that window from the first update, not from module load, or it expires during boot.

## Performance

- Per vehicle and step: 4 wheel reads, at most 4 friction rewrites (only on a key change), a few impulses. The cost is Jolt's.
- Heightfield creation is the expensive call: about 3.8 ms per 257^2 chunk when the samples are baked elsewhere. Bake samples in a worker (a transferable Float32Array) and only copy them on the main thread. Sampling on the main thread with a road overlay cost 20-54 ms per chunk. Build at most one heightfield per frame and let the chunk under the vehicle jump the queue (`ensure`). A 5x5 ring instead of the 3x3 costs 25 bodies instead of 9, and the outer ring is never driven on.
- One compound per chunk for its static props instead of hundreds of boxes. Dynamic props are cheap only while asleep; the source capped them at 28 new bodies per frame, in the 3x3 only.
- Mesh shapes: a building site's 13 first-time mesh shapes built in one frame cost 67 ms. With `pumpMeshQueue(1)`, they build on consecutive frames.
- Never destroy a ring's worth of bodies in one frame: `retireBody` plus `pumpRetired(64)`. Stale colliders 2 chunks out are harmless.
