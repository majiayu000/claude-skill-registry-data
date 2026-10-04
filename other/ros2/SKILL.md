---
name: ros2
description: >
  Index and navigation skill for this repo's ROS2 family. Use when the user asks broadly about
  ROS2, wants an overview, asks which ROS2 skill covers a topic, or needs a starting point.
  For concrete ROS2 tasks such as creating nodes, defining messages, debugging QoS, writing
  launch files, lifecycle orchestration, TF2, diagnostics, testing, bags, or architecture,
  prefer the matching focused ros2-* skill.
---

# ROS2 Skill Index

This skill is a navigation aid. The repo's ROS2 coverage is split across nine focused skills,
each triggered by its specific topic. Open the one that matches your task.

## Pick by Task

| Task                                                                  | Skill                          |
|-----------------------------------------------------------------------|--------------------------------|
| Create a node, structure a node, separate logic from ROS, scaffold pkg | `ros2-node-creation`           |
| Choose QoS, define a custom message, debug "topic doesn't connect"    | `ros2-messaging`               |
| Service vs. action, write a server/client, structured error codes     | `ros2-service-action`          |
| Bring up a system, externalize parameters to YAML, composable nodes   | `ros2-launch-config`           |
| Managed startup, configure → activate → deactivate, supervisor patterns | `ros2-lifecycle`             |
| TF2 broadcasters, listeners, frame trees, lookup-at-timestamp         | `ros2-transforms`              |
| Health monitoring, `/diagnostics`, frequency monitors, logging rules  | `ros2-diagnostics`             |
| pytest/gtest for rclpy/rclcpp, integration & launch_testing           | `ros2-testing`                 |
| `rosbag2` recording/playback, MCAP vs SQLite3, programmatic capture   | `ros2-bag`                     |
| Layered architecture for codebases >1 node, domain-port-adapter       | `ros2-clean-architecture`      |

## Pick by Symptom

| Symptom                                                          | Likely skill                    |
|------------------------------------------------------------------|---------------------------------|
| "Publisher and subscriber both exist but no data arrives"        | `ros2-messaging` (QoS mismatch) |
| "Service call hangs forever from inside a callback"              | `ros2-node-creation` (executor) |
| "Action goal accepted but never executes"                        | `ros2-service-action`           |
| "TF lookup fails / extrapolation into the future"                | `ros2-transforms`               |
| "Test passes locally, fails in CI"                               | `ros2-testing` (sleep / QoS)    |
| "Node started but is silently doing nothing"                     | `ros2-lifecycle` (unconfigured) |
| "Tuning a parameter requires a rebuild"                          | `ros2-launch-config` (YAML)     |
| "Camera dropped frames and we noticed minutes later"             | `ros2-diagnostics` (frequency)  |
| "Replay timing is off / TF says ExtrapolationException"          | `ros2-bag` (`use_sim_time`)     |
| "Node is 1000 lines mixing CV, math, and rclpy"                  | `ros2-clean-architecture`       |

## Adjacent Skills (Outside the ROS2 Family)

- `ros1` — Catkin / rospy / roscpp / nodelets, and migration to ROS2.
- `ros2-web-integration` — rosbridge, REST/WebSocket bridges, MJPEG/WebRTC.
- `robot-bringup` — systemd, udev, watchdogs, boot ordering above the launch layer.
- `docker-ros2-development` — multi-stage Dockerfiles, GPU passthrough, devcontainers.
- `robotics-testing` — broader testing strategy (hardware mocks, simulation, CI).
- `robotics-security` — SROS2, DDS encryption, secrets, e-stop isolation.
- `robotics-design-patterns`, `robotics-software-principles`, `robot-perception` — domain-level patterns.
