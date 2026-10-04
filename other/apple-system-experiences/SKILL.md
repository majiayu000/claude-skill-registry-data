---
name: apple-system-experiences
description: "Integrate WidgetKit, App Intents, ActivityKit, notifications, Spotlight, WatchConnectivity, HealthKit, and StoreKit through truthful shared commands and projections."
---

# System surfaces and framework integration

## Inputs

Identify the system surface, platform/minimum, process/device boundary, canonical data owner, permissions/entitlements, refresh/delivery guarantees, and the in-app equivalent action.

## Rules

- **SYS-001 — Project canonical truth.** Treat widgets, activities, search, and companion views as projections with freshness and unavailable states, not parallel databases of business truth.
- **SYS-002 — Reuse the command boundary.** Intents and external actions validate parameters, authorization, confirmation, and idempotency before invoking the same domain operation as the UI.
- **SYS-003 — Respect delivery limits.** System refresh, background execution, notifications, and companion transport are not guaranteed immediate execution.
- **SYS-004 — Export only truthful semantics.** Do not force app-only data into an unrelated system type or report unsupported permission knowledge.
- **SYS-005 — Verify the whole chain.** Registration, target embedding, permission, storage handoff, execution, rendering, refresh, and recovery are separate gates.

## Workflow

1. Inspect existing integrations and choose the native surface that serves a real user task.
2. Define the projection/command schema, minimum data, stale state, and failure behavior.
3. Wire the correct targets, capabilities, and privacy artifacts with their owning skills.
4. Implement bounded, retry-safe lifecycle and account/device transition handling.
5. Validate the surface in its actual host and on hardware where needed.

## Verify

Test unavailable data, denied/revoked permission, delayed refresh, repeated command, process termination, account/device changes, stale projections, and host-specific rendering.

## Output

Return the boundary diagram, integration-specific guarantees, privacy/project changes, and source/build/runtime/device evidence.

## References

Read the [playbook](references/system-patterns.md) for decisions, failure cases, and source links.

For system surfaces and framework-specific contracts, read the [focused reference](references/system-surface-contracts.md).
