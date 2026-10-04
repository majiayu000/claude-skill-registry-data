---
name: telemetry-dashboard
description: Implement real-time telemetry and Tron dashboard surfaces.
disable-model-invocation: true
---

# Telemetry Dashboard Skill

Procedure:

1. Separate host telemetry, client telemetry, gateway telemetry, and worker telemetry.
2. Host telemetry: CPU, GPU, network, disk.
3. Worker telemetry: process/job CPU, memory, I/O, health, active leases, queue pressure.
4. Client telemetry: connection/request metrics server-side; true CPU/GPU/disk only via client heartbeat/sidecar.
5. Activity log: connection, onboarding, gateway, governance, worker lifecycle, warnings, errors.
6. Dashboard: real-time indicators with graceful degradation when a metric is unavailable.
7. Never fake utilization metrics.

Output must include telemetry schema changes and dashboard acceptance criteria.
