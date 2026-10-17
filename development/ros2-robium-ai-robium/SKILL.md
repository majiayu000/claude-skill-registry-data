---
name: ros2
description: Build and debug robot software whose runtime interfaces use ROS 2.
---

# ROS 2

Treat ROS 2 as a live distributed graph. Inspect the graph that is actually
running before changing source code.

## Establish the environment

- Identify the repository's ROS distro, RMW implementation, workspace, and
  `ROS_DOMAIN_ID`; do not substitute catalog-wide defaults.
- Source the underlay before the workspace overlay. A fresh shell is a fresh
  environment.
- Run `rosdep` after a fresh clone or dependency change, before interpreting a
  build failure as a source bug.
- Prefer an overlay package or launch-time wiring over editing an installed
  third-party package.

## Inspect the boundary that failed

- **Build:** separate missing dependencies, package metadata, and stale build
  artifacts from compiler or application failures.
- **Launch:** resolve the final arguments, parameters, namespaces, and remaps;
  do not reason only from a launch file's defaults.
- **Graph:** confirm that the expected nodes and endpoints exist and that names
  include the namespace you expect.
- **Messages:** compare publisher and subscriber types and QoS. Discovery
  without data is often an interface mismatch, especially for sensor topics.
- **Time and transforms:** confirm a single time source and a connected,
  current TF path before debugging downstream behavior.
- **Lifecycle:** distinguish an inactive node from a missing or crashed node.

Use topics for streams, services for bounded requests, and actions for
long-running goals with feedback and cancellation. Choose based on semantics,
not convenience.

## Go deeper only when needed

- For workspace layout, package anatomy, overlays, and `rosdep`, read
  [workspace and packages](references/workspace-and-packages.md).
- For launch composition, parameters, includes, remaps, and relays, read
  [launch patterns](references/launch-patterns.md).
- For topics, services, actions, QoS, and TF fundamentals, read
  [interfaces and QoS](references/interfaces-and-qos.md).
- When callbacks block or unexpectedly serialize, read
  [concurrency](CONCURRENCY.md) before adding executor threads.
- For a failing command or silent graph, read [failures](FAILURES.md) and then
  the fuller [debugging guide](references/debugging.md) if necessary.
- For Create 3 and TurtleBot 4 evidence, read [TurtleBot 4](TURTLEBOT4.md).
- Use the bundled `ament_python` example only when a complete minimal package
  is useful; re-check its APIs against the project's distro.

Cross into `navigation`, `gazebo`, or a visualization skill only after ROS 2
evidence shows that their boundary is receiving valid data. Cross into
`integration` when the failure is between processes, containers, or non-ROS
systems; use `environments` when the runtime itself is not reproducible.

## Done

- The intended nodes and endpoints exist under the expected names.
- QoS, time, and TF contracts are compatible at every changed boundary.
- A message, service response, or action result proves the real interface, not
  merely that processes started.
- Version-sensitive syntax was checked against the project's ROS distro and
  current [ROS 2 documentation](https://docs.ros.org/).
