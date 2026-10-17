---
name: foxglove
description: Visualize live or recorded ROS robot data remotely with Foxglove or Lichtblick.
---

# Foxglove and Lichtblick

Treat remote visualization as a chain: ROS graph, bridge, network, client, and
layout. Find the first link without evidence.

## Choose the client deliberately

- **Lichtblick:** prefer an inspectable open-core viewer, local/offline use, or
  a browser client you can host and extend yourself.
- **Foxglove:** prefer its managed data, fleet, organization, and support
  services, or when the team already uses its layouts and platform.
- Both clients can consume a Foxglove WebSocket and recordings for the common
  ROS workflow. Re-check current licensing and self-hosting terms before making
  them an architecture dependency.

Read [client choices](CLIENTS.md) when licensing, hosting, extensions, or
managed services affect the decision. If the visualization tool itself has not
been chosen, use `visualization` first.

## Trace the live-data chain

- Prove the ROS topics and QoS locally before blaming the bridge.
- Run the bridge near the ROS graph; DDS discovery should not need to cross a
  browser, NAT boundary, or public internet.
- Keep its unauthenticated WebSocket on a private network, VPN, or SSH tunnel.
- Confirm the listening port and WebSocket reachability before debugging a
  client layout.
- Limit high-rate topics at the bridge when bandwidth is constrained. Hiding a
  panel does not reduce transport load.
- Save a focused layout per task and record before any run that must be shared,
  replayed, or compared.

For bridge, MCAP, navigation goals, teleop, actions, layouts, and custom clients,
read [ROS 2 workflows](ROS2-WORKFLOWS.md). For a connection that is blank,
unreachable, mixed-content blocked, or missing controls, read
[failures](FAILURES.md).

Cross into `ros2` when the local graph or QoS is wrong. Cross into
`environments` when the bridge host, VPN, or container cannot provide the
network contract. Cross into `navigation` only after pose, map, sensors, and
goal messages are proven across the viewer boundary.

## Done

- The intended client reaches the bridge without exposing it publicly.
- The necessary topics render at useful rates and with correct frames.
- Controls publish to the interfaces the robot actually consumes.
- The layout and recording path can be reused by another person.
- Current behavior and hosting terms were checked against official
  [Foxglove](https://docs.foxglove.dev/docs) and
  [Lichtblick](https://lichtblick-suite.github.io/docs/) documentation.
