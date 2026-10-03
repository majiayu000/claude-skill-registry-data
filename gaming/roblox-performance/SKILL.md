---
name: roblox-performance
description: "Diagnose and improve Roblox mobile, server, physics, rendering, replication, and memory performance from measured evidence."
---

# Roblox performance work

Start with a reproducible workload and one metric. Trace the measured cost to its owner before changing code.

Inspect per-frame callbacks, scheduler frequency, instance scans, spatial queries, pathfinding, physics assemblies, network ownership, remotes, replication volume, particles, UI updates, allocations, connections, caches, and unbounded player or round state.

Prefer fixes that remove work, reduce frequency, bound scope, move cosmetic work to clients, or replace polling with events. Pool only when creation cost is measured and lifecycle complexity is justified. Preserve gameplay authority and visible behavior.

Report the baseline, workload, measurement, root cause, change, after measurement, and regression floor. If runtime measurement requires Studio, prepare the exact user-run MicroProfiler or Stats scenario. Never invoke Roblox Studio MCP playtest controls.
