---
name: visualization
description: Choose between RViz2, Foxglove, Lichtblick, and Rerun to inspect robot behavior.
---

# Visualization

Choose the view from the evidence you need and where it must be viewed. The
viewer is part of the debugging loop, not a decorative dashboard.

## Choose the path

- **RViz2:** local Linux desktop, live ROS 2 graph, and frame- or
  message-specific debugging.
- **Foxglove or Lichtblick:** remote/headless ROS systems, browser access,
  shareable layouts, and MCAP playback.
- **Rerun:** ML rollouts, perception, arbitrary tensors, and custom non-ROS
  pipelines.
- Mixed systems may use two views: a ROS viewer for robot state and Rerun for
  policy inputs and outputs. Choose per evidence boundary, not per project.

Use the matching `rviz2`, `foxglove`, or `rerun` skill once the path is clear.
Use `environments` only if the unresolved question is where the viewer or
bridge can run.

## Decide live versus recorded

- Use live viewing to interact and form a hypothesis.
- Record before a run when it must be replayed after a crash, compared across
  versions, or shared with someone who is not present.
- Scope recordings to the evidence needed, but include enough context to
  explain timing and transforms.
- Save the layout or blueprint that makes the recording intelligible.

## Always expose useful evidence

- Frames are connected and current.
- Sensor values and rates are plausible, not merely nonzero.
- Commands can be compared with robot response.
- For navigation, show raw sensors alongside costmaps, plan, footprint, and
  pose.
- For a learned policy, align observations, actions, and resulting trajectory
  on one timeline.

## Done

- The selected tool works in the actual local, remote, or headless context.
- The view distinguishes inputs, decisions, and outcomes.
- A recording exists when later comparison or handoff matters.
- Tool-specific setup is delegated to current upstream documentation and the
  matching skill.
