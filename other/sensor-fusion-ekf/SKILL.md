---
name: sensor-fusion-ekf
description: Use when estimating robot pose/odometry from multiple sensors (wheel odom, IMU, GPS, visual odom) — configure a robot_localization EKF/UKF with per-sensor state masks rather than trusting a single source.
stacks: [python]
domains: [hardware]
phases: [dev]
tags: [ros2, sensor-fusion, ekf, robot-localization, odometry, imu, gps]
scope: kit
---
**When to use.** Pose/odometry estimation or drift problems. *Why:* every sensor lies differently
(wheel slip, IMU bias, GPS jumps); an EKF with correct per-sensor masks beats any one sensor.

**Procedure.**
1. List sensors and which state dims each is trustworthy for (odom→x/y/yaw & velocities, IMU→orientation/angular-rate, GPS→global x/y).
2. Write the `*_config` boolean masks accordingly; set frames (`odom`/`base_link`/`world`).
3. Tune process/measurement covariance from real logs (system ID), not guesses.
4. **Done when:** fused odom is continuous and drift-bounded over a test trajectory (plot pasted).

**Knowledge:** KNOWLEDGE-LIBRARY.md §B1. **Example:** the `ekf.yaml` there.
