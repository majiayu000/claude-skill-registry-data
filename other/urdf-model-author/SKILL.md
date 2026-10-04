---
name: urdf-model-author
description: Use when creating or editing the robot's URDF/description — keep link frames, joint axes, and inertials honest and add a ros2_control block, so one description drives TF, MoveIt, simulation, and hardware alike.
stacks: [python]
domains: [hardware]
phases: [dev]
tags: [ros2, urdf, ros2-control, robot-description, kinematics, tf2]
scope: kit
---
**When to use.** Any change to the robot model. *Why:* the URDF is the single source every layer reads;
frame/axis errors here are the top root cause of sim-to-real divergence.

**Procedure.**
1. Define links/joints with correct frames, axes, limits, and realistic inertials.
2. Add the `ros2_control` block binding joints to command/state interfaces.
3. Validate: `check_urdf`, visualize in RViz, confirm the TF tree and joint motion match reality.
4. **Done when:** URDF parses, RViz shows correct geometry/axes, and the same file loads in sim and on hardware.

**Knowledge:** KNOWLEDGE-LIBRARY.md §B2. **Example:** the `ros2_control` URDF snippet there.
