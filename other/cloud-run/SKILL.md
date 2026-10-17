---
name: cloud-run
description: Deploy and debug headless robotics containers on Google Cloud Run.
---

# Cloud Run

Treat Cloud Run as a request-driven web runtime, not a conventional robot
host.

## Shape the workload for Cloud Run

- Expose one HTTP port and keep durable state outside the instance.
- Decide whether startup is covered by a held request. Under request-based
  billing, background robot or simulator boot can lose CPU when no request is
  open; instance-based CPU changes the cost model.
- Expect WebSocket sessions to inherit the request timeout and instance
  lifecycle. Size the timeout to the intended session, not to an assumed
  default.
- Scale to zero unless a paid warm floor is explicitly justified. State the
  session cost, fleet ceiling, and cold-start expectation.
- General container composition belongs to `integration`; the session gateway
  and visitor lifecycle belong to `live-demo`.

## Verify before deploying

- Check current commands, flags, quotas, WebSocket behavior, and pricing in
  [official Cloud Run documentation](https://cloud.google.com/run/docs) and the
  [`gcloud run deploy` reference](https://cloud.google.com/sdk/gcloud/reference/run/deploy).
- Read [DEPLOYMENT.md](DEPLOYMENT.md) when building, choosing billing and
  concurrency, configuring affinity, authenticating CI, or validating the
  deployed route.
- Treat Robium's measured values as compatibility evidence tied to their
  workload and date. Re-measure CPU, memory, timeouts, and fleet size for the
  application being deployed.
- Public shells require a separate threat model for credentials and egress;
  unauthenticated reachability is not a security design.

## Account for robotics networking

- Cloud Run does not provide the multicast discovery expected by Gazebo
  transport or DDS. A single-container deployment needs an explicit local
  discovery strategy and evidence that the actual graph communicates.
- For the proven Gazebo Harmonic, ROS 2, and Nav2 deployment conditions, read
  [GAZEBO-ROS2.md](GAZEBO-ROS2.md). Do not copy those values into a different
  stack as defaults.
- Route bridge protocol, layouts, and client behavior to `foxglove`; Cloud Run
  only owns how the HTTP/WebSocket route reaches the container.

## Debug from the boundary inward

- Distinguish image pull, CPU starvation, transport discovery, application
  readiness, proxy behavior, affinity, and VPC capacity before changing the
  application.
- Read [FAILURES.md](FAILURES.md) for the evidence that separates common
  failures.
- A probe under request-based billing must remain open long enough to cover the
  work it is testing; connect-and-drop can create the failure it appears to
  diagnose.

## Done

- The immutable image starts with the selected billing mode and resource
  limits.
- Readiness and the real HTTP or WebSocket path work through Cloud Run.
- Idle capacity, session timeout, fleet ceiling, authentication, and cleanup
  behavior match the stated cost and security boundaries.
