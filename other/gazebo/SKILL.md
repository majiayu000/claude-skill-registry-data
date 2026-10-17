---
name: gazebo
description: Build and debug modern Gazebo simulations and their ROS 2 boundary.
---

# Gazebo

Treat a Gazebo simulation as a contract between world, robot, sensors,
transport, and time. Find the first contract that is not producing believable
evidence.

## Start from the actual stack

- For a new robotics app or first demo, read
  [architect](../architect/SKILL.md) before creating worlds, launchers, or
  containers. Reuse its compatible reference-app selection if already made.
  Existing-world edits, simulator debugging, and explanations stay here.
- Confirm the installed `gz` release, ROS distro, `ros_gz` pairing, render
  backend, and whether the run is graphical or headless.
- When consuming an upstream simulator repository, select and pin an explicit
  branch or ref compatible with that ROS distro; default HEAD is not
  compatibility evidence.
- Use modern Gazebo (`gz`). Gazebo Classic and `libgazebo_ros_*` tutorials are
  a different, end-of-life stack.
- Keep upstream compatibility tables and SDF specifications as the authority
  for release-sensitive package names, tags, and plugin APIs.

## Trace the simulation boundary

- **World:** the selected world loads and the expected systems are present.
- **Robot:** links, joints, frames, and drive plugins agree with the physical
  model and downstream interfaces.
- **Sensors:** rates, fields of view, ranges, noise, frames, and timestamps
  model the intended hardware rather than tutorial defaults.
- **Transport:** prove the Gazebo topic exists before debugging its ROS bridge.
- **Bridge:** prefer reviewable YAML for a static bridge set. Use Python or XML
  launch-based `parameter_bridge` nodes when substitutions, grouping, or
  vendor conventions require them; reserve ad-hoc commands for diagnosis.
- **ROS:** confirm `/clock`, commands, odometry, transforms, and sensor messages
  arrive with the expected direction and QoS.

Do not infer simulation correctness from a running process or visible GUI. A
render-backed sensor may be silent even while physics continues.

## Go deeper only when needed

- For SDF worlds, models, drive plugins, spawning, and headless server mode,
  read [worlds and models](references/worlds-and-models.md).
- For lidar, camera, IMU, contact, noise, and rendering, read
  [sensors](references/sensors.md).
- For `ros_gz_bridge`, topic direction, types, QoS, `/clock`, and frame
  overrides, read [the ROS 2 bridge guide](references/ros2-bridge.md).
- For a silent world, sensor, bridge, or remote launch, read
  [failures](FAILURES.md).
- Use the bundled SDF and bridge YAML together only as a starting pair; keep
  their topic and frame names synchronized and verify syntax upstream.

Move to `navigation` only after the robot pose, sensor, map, and velocity
interfaces are valid. Move to `ros2` when Gazebo is publishing correctly and
the fault is in the ROS graph. Use `environments` for container GPU/display
setup and `simulation` only when the simulator itself has not been chosen.

## Done

- Physics time advances and the expected world and model are present.
- Every required Gazebo topic has a matching, correctly directed ROS interface.
- Sensor rate, frame, timestamp, and render output are believable.
- The run works in its intended graphical or headless environment.
- Release-specific claims match current [Gazebo](https://gazebosim.org/docs/)
  and [ros_gz](https://github.com/gazebosim/ros_gz) documentation.
