---
name: rerun
description: Visualize robot and machine-learning data with Rerun.
---

# Rerun

Choose the **data sink first**. Where and when the viewer must run determines
how the application should log.

## Choose the viewing shape

- Use a spawned viewer for short local exploration with a real desktop.
- Stream to a separate viewer or serve one when the producer is remote or
  headless.
- Save an `.rrd` when the run must be inspectable later, reproducible in CI, or
  shared without keeping the producer alive.
- Embed a viewer only when it is part of the actual application experience;
  otherwise keep visualization out of the service boundary.

## Make the recording understandable

- Organize entity paths around the robot, sensors, policy, and world so related
  data shares a useful hierarchy.
- Use an explicit sequence or time timeline for episodes and rollouts. Log
  static geometry once and changing state at the corresponding step.
- Align transforms, images, actions, predictions, and outcomes on the same time
  basis before interpreting what the viewer shows.
- Check the current [Rerun documentation](https://rerun.io/docs) and
  [examples](https://rerun.io/examples) before choosing archetypes or calling
  APIs. Names and signatures change between releases.

## Go deeper only when needed

- For local, remote, file, and browser modes plus their common failures, read
  [OPERATING-MODES.md](OPERATING-MODES.md).
- For the Robium-tested Gradio streaming pattern and dependency conflict, read
  [GRADIO.md](GRADIO.md).
- Let LeRobot's dataset visualizer produce the recording when inspecting a
  LeRobot episode; use LeRobot guidance for its current command.
- When the boundary is live ROS topics, use RViz2 or Foxglove. Use the
  visualization skill only when the tool itself has not been chosen.

## Done

- The chosen sink works in the target environment, related data is aligned and
  navigable, and a saved or replayable artifact exists when the observation
  matters beyond the live session.
