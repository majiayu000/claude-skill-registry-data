---
name: ros2-perception-pipeline
description: Use when adding or debugging a perception node (camera, LiDAR, depth) in ROS 2 — verify the TF frame tree and time sync first, then wire sensor topics through PCL/Open3D processing to a documented output frame.
stacks: [python]
domains: [hardware]
phases: [dev]
tags: [ros2, perception, tf2, pointcloud, pcl, open3d, sensors]
scope: kit
---
**When to use.** Any perception change. *Why:* a wrong sensor→`base_link` transform or bad time sync
makes everything downstream silently wrong — this is the #1 perception bug, so check it before logic.

**Procedure.**
1. Inspect the TF tree (`ros2 run tf2_tools view_frames`); confirm every sensor frame is connected and correct.
2. Confirm timestamps/`use_sim_time` alignment across fused topics.
3. Process (PCL/Open3D) and publish results in a named, documented frame.
4. **Done when:** TF tree verified (paste it), output visualized in RViz in the right frame, latency measured.

**Knowledge:** KNOWLEDGE-LIBRARY.md §B1.
