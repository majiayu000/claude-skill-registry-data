---
name: isaac-sim
description: Build GPU-accelerated robot simulations and synthetic-data pipelines with NVIDIA Isaac Sim.
---

# Isaac Sim

Isaac Sim is a gated simulation stack. Prove the target hardware and
release-compatible runtime before designing the robot application around it.

## Pass the gate

- Check the current NVIDIA requirements for GPU architecture, VRAM, driver,
  operating system, RAM, and storage. An NVIDIA compute GPU without the required
  ray-tracing support is not interchangeable with a supported RTX GPU.
- Isaac Sim does not run on macOS. Use a qualifying remote host or choose a
  different simulator; do not search for a local workaround.
- Prefer an official, pinned container when local/remote parity matters. Verify
  the matching NGC tag, EULA requirements, host driver, and GPU passthrough at
  the time of use.

## Build outward from a running simulation

- **Runtime:** the chosen Isaac Sim release starts cleanly on the target host.
- **Scene:** the USD stage, physics, units, and robot articulation match the
  intended application.
- **Sensors:** frames, rates, ranges, noise, and rendering modes match the real
  interfaces or the stated synthetic-data purpose.
- **Integration:** ROS 2 bridge version, distro, graph nodes, clock, and topic
  contracts agree with the external system.
- **Operation:** batch jobs run headless; an interactive viewport uses a
  supported streaming path rather than display forwarding assumptions.

## Go deeper only when needed

- Before installing or provisioning, read
  [references/setup-and-requirements.md](references/setup-and-requirements.md)
  and re-check its dated values against current NVIDIA documentation.
- For USD, robot import, sensors, or Replicator, read
  [references/scenes-and-sensors.md](references/scenes-and-sensors.md).
- For the ROS boundary, read
  [references/ros2-integration.md](references/ros2-integration.md).
- For a remote interactive viewport, read
  [references/webrtc-livestream.md](references/webrtc-livestream.md).
- When launch, rendering, streaming, or bridge behavior fails, start with
  [FAILURES.md](FAILURES.md).
- Isaac Lab owns policy training. Data owns source strategy; Isaac Sim owns the
  mechanics of generating synthetic data.

## Done

- The pinned runtime passes a small headless scene, the required sensor or ROS
  output is measured, and any remote viewer works through the same deployment
  path the application will use.
