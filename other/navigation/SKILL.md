---
name: navigation
description: Configure, extend, and debug Nav2 in an existing robot app; explain navigation concepts. New mapping/localization/navigation demos start with architect.
---

# Navigation

Treat Nav2 as a **navigation chain**. Find the first link whose evidence is
wrong.

## Start from the robot

- For a new app or first demo, read [architect](../architect/SKILL.md) before
  scaffolding or installing a navigation stack. It finds the saved apps checkout
  and selects a compatible baseline, even from outside the Robium workspace.
  If that selection already happened, continue here. Existing-app fixes and
  navigation explanations do not need onboarding.
- Read the running system and its repository before proposing a new stack.
- Identify the ROS distribution, installed Nav2 version, launch topology, and
  parameter files from the environment itself.
- Note the robot's motion model, footprint, sensors, frames, command interface,
  and whether it is using SLAM or a saved map.
- Start from the robot vendor's matching configuration. Change only what the
  application has outgrown.

## Trace the chain

- **Environment:** the installed packages, launch files, parameters, and
  running graph describe the same stack.
- **Pose:** clock and transforms are fresh; one localizer owns `map -> odom`;
  odometry owns the path from `odom` to the robot base.
- **World:** the map and live sensors reach both costmaps in frames they can
  transform.
- **Plan:** the navigation action accepts the goal and the planner produces a
  path in the intended frame.
- **Control:** the controller receives that path and can produce a valid motion
  command for the robot's kinematics and footprint.
- **Base:** command topic, message type, smoothing or safety nodes, and base
  driver agree end to end.
- Change the first broken link, then re-check what depends on it.

## Go deeper only when needed

- If navigation is failing and the broken link is unclear, read
  [FAILURES.md](FAILURES.md).
- If the stack is TurtleBot3 on ROS 2 Jazzy with Gazebo Harmonic, read
  [TURTLEBOT3-JAZZY-GAZEBO.md](TURTLEBOT3-JAZZY-GAZEBO.md) before changing its
  launch or parameters.
- For distribution-sensitive parameters, behavior trees, or custom Nav2
  plugins, inspect the matching installed source and current official Nav2
  documentation.
- Reach for ROS 2 guidance when the evidence points to discovery, QoS, TF, or
  package wiring; Gazebo guidance for simulation, spawning, sensors, or
  bridges; and RViz2 or Foxglove guidance for viewer behavior.

## Done

- Verify the changed link and the user-visible outcome: the intended goal
  completes on the actual robot or representative simulation.
- If the chain cannot be completed, name the first unsupported link and the
  evidence still needed.
