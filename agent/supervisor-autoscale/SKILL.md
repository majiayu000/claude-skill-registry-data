---
name: supervisor-autoscale
description: Implement supervised MCP/sub-agent worker pools and autoscaling behavior.
disable-model-invocation: true
---

# Supervisor and Autoscale Skill

Procedure:

1. Introduce `ManagedEndpointPool`, `EndpointTemplate`, `EndpointInstance`, and `EndpointLease`.
2. Implement Windows Job Object based process supervision.
3. Add readiness probes and health states.
4. Add lease assignment for stable logical endpoints.
5. Add scale-out thresholds: active leases, queue wait, inflight requests, saturation.
6. Add drain behavior. Existing stateful sessions remain sticky; new sessions route to healthier/newer instances.
7. Do not hot-migrate active MCP sessions unless a backend-specific migration contract exists.
8. Add failure/restart behavior.
9. Add tests for lease assignment, drain, restart, and scale-out decisions.

Output must include state diagrams or tables for instance lifecycle and lease lifecycle.
