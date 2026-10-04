---
name: lerobot-imitation-loop
description: Use to bring up a new manipulation skill cheaply — teleoperate demos into a LeRobotDataset, train an imitation policy (ACT/diffusion/SmolVLA), evaluate in sim, then deploy, instead of reward-engineering RL from scratch.
stacks: [python]
domains: [hardware]
phases: [dev]
tags: [robot-learning, lerobot, imitation-learning, act, vla, teleoperation]
scope: kit
---
**When to use.** New manipulation task bringup. *Why:* imitation from ~50 demos is far cheaper and
more reliable than RL reward-shaping for a first working behavior.

**Procedure.**
1. Teleoperate ~50 demonstrations; record to a `LeRobotDataset` (standard Parquet+MP4 format).
2. Train an ACT/diffusion/SmolVLA policy on the dataset.
3. Evaluate in sim, then a supervised hardware trial; iterate on failure cases (add targeted demos).
4. **Done when:** policy succeeds ≥ target rate on held-out starts, in sim and on hardware, with the number reported.

**Knowledge:** KNOWLEDGE-LIBRARY.md §B3. **Example:** the LeRobot record/train commands there.
