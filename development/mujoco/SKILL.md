---
name: mujoco
description: Build and debug MuJoCo robot simulations. First interactive robot tryouts start with architect's reference-app selection.
---

# MuJoCo

A plausible render proves little by itself. Follow the physical chain from
model through kinematics, actuation, contact, and observation.

## Start from the model

- For a first interactive tryout, new app, or first policy demo, read
  [architect](../architect/SKILL.md) before creating a scene, controller, or
  viewer or downloading a model collection. Reuse its compatible reference-app
  selection if already made. Existing-model edits, physics debugging, and
  explanations stay here.
- Read the MJCF and the pinned asset revision before adding control code. Check
  joint ranges, actuator limits, collision geometry, sites, masses, and the
  intended work surface.
- Prefer a maintained model from
  [MuJoCo Menagerie](https://github.com/google-deepmind/mujoco_menagerie), but
  verify it against the real robot and task envelope.
- Confirm gripper polarity, fingertip gap, and contact geometry empirically.
  Names and documentation can disagree with the model that actually runs.
- Use the current [MuJoCo documentation](https://mujoco.readthedocs.io/) for
  MJCF and Python APIs rather than carrying signatures forward from memory.

## Follow the physical chain

- **Kinematics:** solve only for reachable targets and check the residual;
  damped least-squares can return a poor local solution without raising.
- **Actuation:** compare commanded position or torque with joint state,
  actuator force, range limits, and saturation.
- **Contact:** inspect which geoms belong to the gripper and object. Unnamed
  mesh geoms make name-only contact filters unsafe.
- **Grasp:** calibrate the grasp point, approach path, wrist orientation, and
  lift together. The end-effector site is not automatically the physical pinch
  point.
- **Observation:** make cameras and renderer lifecycle deterministic before
  using frames as training or regression data.
- **Controls:** distinguish model state, actuator limits, and rounded UI
  ranges. Clamp reset values to the actual widget bounds before binding them;
  a physically valid state can still be rejected by a narrower control.

## Go deeper only when needed

- For reachability, collision, grasp, saturation, and rendering symptoms, read
  [FAILURES.md](FAILURES.md).
- For the measured SO-arm and macOS evidence from Robium's manipulation trial,
  read [SO-ARM-MACOS.md](SO-ARM-MACOS.md). Preserve its numbers only with the
  stated model, scene, hardware, and renderer conditions.
- Use LeRobot guidance when the boundary reaches datasets, policies, or
  evaluation; use simulator-selection guidance when MuJoCo itself has not yet
  been chosen.

## Done

- The intended workspace is reachable, commands produce the expected joint and
  contact state, grasps survive a lift across representative poses, and seeded
  resets produce acceptably stable observations.
