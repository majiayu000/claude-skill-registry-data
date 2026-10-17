---
name: integration
description: Wire robotics modules with ROS 2 interfaces, Docker Compose, or non-ROS transports.
---

# Integration

Every module boundary needs an explicit contract: why the boundary exists, what
crosses it, how peers discover each other, and how failure is observed.

## Draw boundaries for a reason

- Split components with different rates when sharing an executor or process can
  starve the faster loop.
- Split failure domains when one component must restart, scale, or exhaust
  memory without taking down another.
- Keep tightly coupled code together when neither rate nor failure isolation
  justifies serialization and deployment overhead.
- Make each container a supervisable unit. Multiple processes may belong
  together, but their shared lifecycle should be intentional.

## Choose the boundary contract

- Inside one ROS 2 system, default to ROS topics, services, and actions.
- Crossing hosts or containers does not by itself require a new application
  protocol; configure ROS discovery explicitly first.
- Use gRPC or REST at a genuine non-ROS system or organizational boundary.
- Use shared memory or zero-copy paths only after measurement shows copying is
  the bottleneck.
- Treat names, schemas, QoS, time, backpressure, health, restart behavior, and
  ownership as part of the interface.

Read [communication selection](references/comms-selection.md) when choosing
between ROS 2, DDS discovery options, Zenoh, gRPC, REST, or shared memory.

## Package the running system

- Use separate build and runtime stages for shipped modules; leave compilers
  and build-only dependencies behind.
- Give each service a health signal that proves readiness, not merely a live
  process.
- Make network mode, `ROS_DOMAIN_ID`, discovery, volumes, devices, and
  shutdown behavior visible in the composition.
- A successful `docker compose up` proves process creation, not communication.
  Verify real cross-boundary messages.

Read [the Dockerfile guide](references/dockerfile-guide.md) for build/runtime
structure and signal handling. Read [compose patterns](references/compose-patterns.md)
for DDS discovery, health, domains, and networking. Use the examples only as
starting shapes and verify them in the target environment.

Use `environments` for one module's reproducibility and GPU/runtime contract.
Use `ros2` when the failed interface is within a healthy ROS graph. Use
`foxglove` only when the boundary is specifically remote visualization.

## Done

- Each split has a rate, failure, deployment, or ownership reason.
- Every boundary has an explicit protocol and interface contract.
- Peers discover each other in the real host/container topology.
- Health and shutdown behavior are observable and scoped to the failed unit.
- A real message or request proves each changed boundary end to end.
