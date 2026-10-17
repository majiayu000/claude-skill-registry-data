---
name: rviz2
description: Inspect and debug live ROS 2 robot state with RViz2.
---

# RViz2

Treat RViz2 as a consumer of ROS evidence. A blank display usually means its
frame, message, QoS, or time contract is wrong.

## Build a focused view

- Start with a fixed frame that exists now, then add only the displays needed
  for the question being asked.
- Prefer adding by topic when discovering a graph; it helps match message type
  to display type.
- Keep a saved `.rviz` configuration per robot and task. Do not rebuild the
  display list on every run or make one unreadable everything-dashboard.
- For navigation, view raw sensors and TF alongside map, costmaps, footprint,
  plan, and robot model so upstream data can be distinguished from Nav2 output.

## Read what the display is telling you

- A red or empty display is evidence about the input boundary, not proof that
  RViz itself is broken.
- Check fixed frame and TF first, then publisher/display QoS, then simulation
  time and `/clock`.
- Compare the configured topic and namespace with the live graph; stale configs
  often point at an old robot name.
- A missing display plugin can fail one saved display while the rest of the
  config continues to load.

Read [failures](FAILURES.md) when something does not render. Cross into `ros2`
only when the evidence points to TF, QoS, graph, or time at the publisher. Cross
into `navigation` when those inputs are healthy but a costmap, plan, or
controller result is wrong.

Use `foxglove` instead for a headless, remote, browser, or shareable workflow;
use `rerun` for data-centric ML and non-ROS logging. If the viewer has not been
chosen, use `visualization` first.

## Done

- The fixed frame is present and every displayed message transforms into it.
- Display QoS and topic namespaces match their publishers.
- Simulation time is consistent when applicable.
- The saved config opens into a focused, useful debugging view.
- Any CLI or UI details were checked against the installed RViz2 build and
  current [RViz documentation](https://github.com/ros2/rviz).
