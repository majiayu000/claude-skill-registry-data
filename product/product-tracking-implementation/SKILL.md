---
name: product-tracking-implementation
description: "Implement approved product telemetry safely in a scoped codebase, preserving existing behavior and validating emitted event contracts. Use when a reviewed tracking plan and implementation guide already exist and the user asks to add or repair instrumentation. Turkish triggers: onaylı ürün takibini kodla, event/property uygula ve test et."
---

# Product Tracking: Implement

Implement only the reviewed telemetry contract. Treat telemetry as non-blocking evidence collection, not business logic.

## Preconditions

- An approved plan and repository-specific guide exist, or the user explicitly accepts a narrowly stated draft.
- The target runtime, test method, consent boundary, and destination configuration are known.

## Workflow

1. Snapshot the relevant source and tests. Restate the exact events and files in scope.
2. Reuse the project’s existing telemetry boundary where it exists; do not install or switch vendors without approval.
3. Add the smallest changes that emit required events after the underlying action succeeds.
4. Pass only schema-approved, minimized properties. Keep identifiers and consent logic consistent with the plan.
5. Add or update tests for event name, properties, duplication, error isolation, and opt-out behavior.
6. Verify that failed telemetry cannot block the user action. Report files changed and evidence.

## Guardrails

- Never expose secrets or live customer data in tests or logs.
- Do not add tracking for unapproved events, hidden clicks, or sensitive content.
- Do not declare delivery verified without an authorized test destination or an observable local boundary.
- Hand off new feature work to `product-tracking-feature-update`.
