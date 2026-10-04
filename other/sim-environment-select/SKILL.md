---
name: sim-environment-select
description: Use when choosing or setting up a simulator for a robot task — match the engine to the job (MuJoCo for contact-rich manipulation, Isaac Lab for large-scale RL, Gazebo for ROS navigation) and reuse the real URDF.
stacks: [python]
domains: [hardware]
phases: [dev]
tags: [simulation, mujoco, isaac-lab, gazebo, genesis, sim-to-real]
scope: kit
---
**When to use.** Standing up or picking a sim. *Why:* engines differ in contact fidelity, throughput,
and ROS integration; the wrong pick wastes weeks and misleads sim-to-real.

**Procedure.**
1. Classify the task → engine: manipulation/sim-to-real → MuJoCo/MJX; parallel RL locomotion → Isaac Lab; ROS nav/SLAM/multi-robot → Gazebo.
2. Load the *same* URDF/description used on hardware (converge, don't fork).
3. For high stakes, plan dual-sim validation (train Isaac Lab → re-score MuJoCo MJX).
4. **Done when:** the robot loads and a scripted motion runs in-sim matching the real kinematics.

**Knowledge:** KNOWLEDGE-LIBRARY.md §B3. **Example:** the MJCF snippet there.
