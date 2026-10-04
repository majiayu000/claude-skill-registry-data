---
name: physics-baseline
description: Use this skill whenever initialising the physics engine, configuring gravity, timestep, collision detection, constraints, or any rigid body in the Myelin simulator. This defines the physics world configuration that must remain fixed across all sessions for reproducible assessment outcomes. Do not change physics constants or timestep values. Load this skill before writing any physics initialisation or rigid body code.
---

This skill defines the physics configuration for the Myelin simulator. Reproducible assessment outcomes depend on a deterministic physics world. Changing any constant here — even slightly — can shift the torque curve, pressure model, or hasp snap behaviour in ways that invalidate scoring comparisons across sessions.

---

## Physics Engine Selection

Use Cannon-ES (`cannon-es`) as the physics engine. It is lightweight, WebAssembly-free (important for cold load times), and sufficient for the constraint and force requirements of the LOTO simulation.

```javascript
import * as CANNON from 'cannon-es';
```

Do not substitute Rapier, Ammo.js, or any other engine without updating this skill and the `loto-interaction-mechanics` skill. The torque curve and pressure model values are calibrated for Cannon-ES's constraint solver behaviour.

---

## World Initialisation

```javascript
function createPhysicsWorld() {
  const world = new CANNON.World();

  // Gravity — fixed, non-negotiable
  world.gravity.set(0, -9.81, 0);

  // Broadphase — SAPBroadphase is faster than NaiveBroadphase for sparse industrial scenes
  world.broadphase = new CANNON.SAPBroadphase(world);
  world.broadphase.axisIndex = 1; // Y-axis sweep (objects mostly spread on XZ plane)

  // Allow sleeping — reduces CPU load for stationary objects between interactions
  world.allowSleep = true;

  // Solver iterations — 20 is stable for constraint chains in LOTO sequence
  world.solver.iterations = 20;
  world.solver.tolerance  = 0.001;

  return world;
}
```

`gravity.set(0, -9.81, 0)` is fixed. Do not parameterise this value. Do not apply scene-level gravity overrides.

---

## Fixed Timestep

The physics world must advance with a fixed timestep for simulation reproducibility. Variable timestep produces different constraint resolution depending on frame rate — this breaks scoring consistency.

```javascript
const FIXED_TIMESTEP    = 1 / 60;  // 60 Hz physics — matches render target
const MAX_SUBSTEPS      = 3;       // maximum substeps per frame to avoid spiral of death
const HIGH_FREQ_TIMESTEP = 1 / 120; // use for fast/small objects (e.g. padlock shackle)

let lastTime = null;

function stepPhysics(currentTime) {
  if (lastTime === null) {
    lastTime = currentTime;
    return;
  }
  const delta = (currentTime - lastTime) / 1000; // convert ms to seconds
  lastTime = currentTime;

  world.step(FIXED_TIMESTEP, delta, MAX_SUBSTEPS);
}
```

Call `stepPhysics` in the render loop before `composer.render()`. Never call `world.step` with a variable timestep argument only — the fixed timestep must always be the first argument.

For the padlock shackle body (small, fast-moving during engagement): override to `HIGH_FREQ_TIMESTEP` for that body's island during the shackle engagement animation to prevent tunnelling.

---

## Material Properties

Define shared physics materials and contact behaviours once. All LOTO scene objects reference these materials rather than defining their own.

```javascript
function createPhysicsMaterials(world) {
  const metalMaterial   = new CANNON.Material('metal');
  const rubberMaterial  = new CANNON.Material('rubber');
  const groundMaterial  = new CANNON.Material('ground');
  const handMaterial    = new CANNON.Material('hand');

  // Metal on metal — valve, hasp, padlock contacts
  const metalMetal = new CANNON.ContactMaterial(metalMaterial, metalMaterial, {
    friction:    0.3,
    restitution: 0.1   // low bounce — industrial components do not spring
  });

  // Rubber on metal — grip handle contacts
  const rubberMetal = new CANNON.ContactMaterial(rubberMaterial, metalMaterial, {
    friction:    0.75,
    restitution: 0.05
  });

  // Hand (grab proxy) on metal — grab interaction contact
  const handMetal = new CANNON.ContactMaterial(handMaterial, metalMaterial, {
    friction:    0.8,
    restitution: 0.0
  });

  // Ground/fixture — static base contacts
  const groundMetal = new CANNON.ContactMaterial(groundMaterial, metalMaterial, {
    friction:    0.5,
    restitution: 0.05
  });

  world.addContactMaterial(metalMetal);
  world.addContactMaterial(rubberMetal);
  world.addContactMaterial(handMetal);
  world.addContactMaterial(groundMetal);

  return { metalMaterial, rubberMaterial, groundMaterial, handMaterial };
}
```

---

## Standard Rigid Body Configuration

Mass, centre of mass, and inertia values for primary LOTO objects. These are derived from the geometry dataset and must not be estimated.

```javascript
const LOTO_BODY_CONFIG = {
  valve: {
    mass: 2.4,         // kg — cast iron handwheel valve
    linearDamping:  0.4,
    angularDamping: 0.6,
    material: 'metal',
    allowSleep: true
  },
  hasp: {
    mass: 0.18,        // kg — steel safety hasp
    linearDamping:  0.3,
    angularDamping: 0.5,
    material: 'metal',
    allowSleep: false   // hasp must remain responsive during alignment
  },
  padlock: {
    mass: 0.22,        // kg — standard safety padlock
    linearDamping:  0.4,
    angularDamping: 0.6,
    material: 'metal',
    allowSleep: false
  },
  bleedValve: {
    mass: 0.08,
    linearDamping:  0.5,
    angularDamping: 0.7,
    material: 'metal',
    allowSleep: true
  }
};

function createRigidBody(config, shape, position, quaternion) {
  const body = new CANNON.Body({
    mass:            config.mass,
    linearDamping:   config.linearDamping,
    angularDamping:  config.angularDamping,
    allowSleep:      config.allowSleep
  });
  body.addShape(shape);
  body.position.copy(position);
  if (quaternion) body.quaternion.copy(quaternion);
  return body;
}
```

---

## Constraints

### Valve rotational constraint (Step 2)

The valve rotates on a single axis (Y in world space). Use a `HingeConstraint` locked to the pipe axis.

```javascript
function createValveConstraint(valveBody, pipeBody) {
  const constraint = new CANNON.HingeConstraint(valveBody, pipeBody, {
    pivotA: new CANNON.Vec3(0, 0, 0),     // pivot at valve centre
    axisA:  new CANNON.Vec3(0, 1, 0),     // Y-axis rotation
    pivotB: new CANNON.Vec3(0, 0, 0),     // pivot at pipe flange
    axisB:  new CANNON.Vec3(0, 1, 0),
    maxForce: 25                           // matches grab maxForce from loto-interaction-mechanics
  });

  // Apply torque resistance phases from loto-interaction-mechanics
  // These are applied as motor torque at each phase boundary
  constraint.enableMotor();
  constraint.setMotorSpeed(0);

  return constraint;
}
```

Torque resistance is applied via `setMotorMaxForce` as the rotation angle crosses phase thresholds. See `loto-interaction-mechanics` skill for the phase values `[8.2, 3.1, 11.8]` Nm.

### Hasp proximity constraint (Step 3)

Do not use a physics spring for hasp snap. Use a distance check in the game loop and dispatch `STEP_PASS` when distance < 0.02 m. Physics constraints for hasp should only prevent interpenetration — the snap is a state machine event, not a physics-driven behaviour.

### Padlock lock constraint (Step 4)

Once shackle engagement is confirmed, lock the padlock body to the hasp body with a `LockConstraint`:

```javascript
function lockPadlockToHasp(padlockBody, haspBody) {
  const lock = new CANNON.LockConstraint(padlockBody, haspBody, {
    maxForce: 1e6 // effectively rigid
  });
  world.addConstraint(lock);
  padlockBody.allowSleep = true; // lock is set — body can sleep
  return lock;
}
```

Once locked, no grab interaction may remove the padlock. Disable the grab handler on the padlock body after constraint is applied.

---

## Continuous Collision Detection (CCD)

Enable CCD for small fast-moving objects to prevent tunnelling through thin geometry.

```javascript
function enableCCD(body, radius) {
  body.ccdSpeedThreshold  = 0.1; // m/s — enable CCD above this speed
  body.ccdIterations      = 10;
  body.boundingSphereRadius = radius;
}

// Apply to padlock shackle during engagement animation
enableCCD(padlockShackleBody, 0.015);
```

CCD is expensive. Apply only to bodies where tunnelling is a genuine risk (small, fast, thin-geometry contact). Do not apply globally.

---

## Physics-to-Render Synchronisation

After each `world.step`, copy physics body positions and quaternions to their Three.js mesh counterparts.

```javascript
function syncMeshesToBodies(meshBodyPairs) {
  for (const { mesh, body } of meshBodyPairs) {
    mesh.position.copy(body.position);
    mesh.quaternion.copy(body.quaternion);
  }
}
```

Call `syncMeshesToBodies` every frame after `stepPhysics` and before `composer.render()`. Do not apply any additional transform to a physics-driven mesh outside of this sync — it will be overwritten on the next frame.

---

## Grab Interaction Physics

The grab proxy is a zero-mass kinematic body that the learner's cursor or hand position drives. It connects to the target object via a spring-like constraint.

```javascript
function createGrabProxy(world) {
  const grabBody = new CANNON.Body({ mass: 0 }); // kinematic — mass 0 = static
  grabBody.addShape(new CANNON.Sphere(0.03));     // grab radius 0.03 m from loto-interaction-mechanics
  world.addBody(grabBody);
  return grabBody;
}

function createGrabConstraint(grabBody, targetBody, localPointOnTarget) {
  return new CANNON.PointToPointConstraint(
    grabBody,
    new CANNON.Vec3(0, 0, 0),
    targetBody,
    localPointOnTarget,
    25  // maxForce matches loto-interaction-mechanics grab maxForce
  );
}
```

The grab proxy moves to the pointer/hand position on every frame before `world.step`. The spring constraint transmits the force to the target object.

Grip ramp: interpolate constraint `maxForce` from 0 to 25 N over 0.2 seconds (12 frames at 60 fps) on grab initiation. On release, set `maxForce` to 0 and remove the constraint on the next frame.

---

## Performance Budget

Physics budget from the simulation spec:
- Maximum physics bodies in scene: 200 (high-end tier), 100 (mid-range), kinematic-only on low-end
- Physics memory ceiling: 32 MB
- Fixed timestep cost: <= 2 ms per step at 60 Hz target

Monitor physics step time in the performance tracking loop. If average physics step exceeds 3 ms sustained over 60 frames, reduce non-essential body count (e.g. put distant static fixtures to sleep).

---

## What Not To Do

- Do not change `gravity.set(0, -9.81, 0)` — it is fixed for scoring reproducibility
- Do not use a variable timestep as the first argument to `world.step`
- Do not apply physics spring/constraint for hasp snap — use state machine distance check instead
- Do not keep CCD enabled globally — apply only to small fast bodies
- Do not apply additional Three.js transforms to physics-driven meshes outside the sync loop
- Do not set grab `maxForce` instantly to 25 N — ramp over 0.2 seconds
- Do not allow padlock removal after `LockConstraint` is applied
- Do not substitute a different physics engine without updating `loto-interaction-mechanics` calibration values
