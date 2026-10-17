---
name: live-demo
description: Add temporary, isolated hosted sessions to a tested robotics application.
---

# Live demo

Separate the host-level control plane from the visitor's session data plane.

## Start from a working app

- Add hosted lifecycle only after the application's normal smoke test passes.
- Define one real demo outcome, app-specific readiness, maximum session time,
  fleet capacity, cost boundary, and authoritative teardown.
- Keep the app's runtime and `demo.orchestrator` facts in `robium-app.yaml`.
  The website/orchestrator derives its registry entry from that source; current
  production enablement remains website-owned.
- Never allocate on catalog, overview, or idle live-page load. Starting paid
  capacity requires an explicit visitor action.
- Keep public project copy, cards, articles, and media in `app-publishing`.

## Keep the session boundary explicit

- A host-level lifecycle layer enforces fleet limits and expiry and returns an
  instance ID plus connect host. Local Docker and RunPod allocate explicit
  resources; Cloud Run routes requests to a predeployed service.
- The verified gateway example gives the first active claimant exclusive use
  and rejects concurrent foreign claims. Its browser-provided session ID is a
  coordination key, not authentication.
- When access control matters, issue a signed or high-entropy, host-bound
  capability outside the instance and validate it on every lifecycle and
  viewer route. Affinity and hard-to-guess URLs remain routing conveniences.
- Keep the orchestrator out of the viewer data path. The browser should talk
  directly to the gateway after allocation.
- Read [orchestrator-pattern.md](references/orchestrator-pattern.md) when
  implementing provider drivers or local start/delete behavior. Read
  [gateway-pattern.md](references/gateway-pattern.md) when implementing claims,
  viewer transport, readiness, or shutdown.

## Make lifecycle visible

- Expose idle, allocating, booting, ready, reconnecting, stopping, expired,
  busy, budget-exhausted, and failed states honestly.
- Keep the current instance while reconnecting; a transient poll failure must
  not allocate a replacement.
- Show real boot messages, remaining time, capacity, and expected cold-start
  behavior. Avoid invented percentage progress.
- Read [session-ui.md](references/session-ui.md) for the shared browser state
  machine. Read [viewers.md](references/viewers.md) when choosing or embedding
  Gradio, Lichtblick, Foxglove, or a custom interaction surface.

## Choose a provider only when needed

- Use local Docker for the cheapest full lifecycle probe.
- Route Cloud Run deployment and request-lifecycle mechanics to `cloud-run`,
  and RunPod allocation and paid-resource cleanup to `runpod`; keep the browser
  contract provider-neutral.
- For the proven Gazebo and ROS 2 Cloud Run conditions, read
  [cloud-run-tuning.md](references/cloud-run-tuning.md). Its measured values are
  evidence from that workload, not defaults for another app.
- Adapt [demo_gateway.py](examples/demo_gateway.py) only for the verified
  ROS/WebSocket shape it demonstrates; review its app and origin-specific
  constants first.

## Done

- The hosted smoke covers allocation or routing, first claim, readiness,
  concurrent-claim rejection, one real outcome, and release or deletion. When
  capabilities are enabled, it also rejects an invalid capability.
- Expiry and cleanup do not depend on the browser remaining open.
- The idle public surface performs no paid allocation or provider polling.
