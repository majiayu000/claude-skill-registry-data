---
name: e2e-validation
description: Validate a critical user or system journey end to end across real application boundaries, state changes, integrations, side effects, recovery behavior, and observable final outcomes.
---
# End-to-End Validation

Use when confidence depends on the assembled system rather than one component, such as release-critical user journeys, cross-service workflows, authentication, payments, onboarding, deployment flows, or data-changing operations.

## Procedure
1. Define the journey from a real starting state to a user-meaningful final outcome. State the actors, permissions, environment, seed data, external dependencies, and acceptance criteria before execution.
2. Confirm the environment represents the behavior being claimed. Record application/build versions, backend/service versions, feature flags, browser/device or client, and whether dependencies are real, sandboxed, simulated, or unavailable.
3. Start from a controlled precondition. Create or reset data so the test does not accidentally depend on leftovers from a prior run, and define cleanup for durable side effects.
4. Execute the flow through normal interfaces rather than bypassing the layers whose integration is under test. Observe UI/client behavior, network/service responses, async work, persisted state, emitted events, external integrations, and final user-visible state as relevant.
5. Verify intermediate checkpoints where they clarify failure location, but do not mistake internal activity for the final outcome. A request returning success is insufficient if the user's durable result is wrong.
6. Exercise the most important failure or recovery variant when the journey depends on retries, redirects, asynchronous jobs, reconnect, cancellation, partial success, or an external dependency.
7. Capture diagnostics with timestamps and stable identifiers so a failure can be traced across components. Preserve enough evidence to reproduce without dumping unnecessary sensitive data.
8. Check idempotency and cleanup for workflows that may be repeated. A second run should not silently duplicate destructive, financial, messaging, provisioning, or other durable side effects unless duplication is the expected behavior.
9. If automation exists, assess whether it faithfully covers the real journey and environment; supplement it when browser/platform/integration behavior is mocked away. If the flow is manual, record steps and evidence precisely enough to repeat.
10. Report pass/fail against the user-meaningful acceptance criteria, plus environment limitations, degraded dependencies, and any behavior not actually validated.

## Decision rules
- End-to-end tests are valuable when integration is the risk; they are not a substitute for focused component/service tests that localize failures faster.
- A green UI path is not enough if the durable backend or external side effect is wrong.
- Do not call a mocked dependency "end to end" without clearly stating the boundary that was simulated.
- Cleanup is part of test design when the journey creates durable or costly state.

## Quality gate
E2E validation is complete when the critical journey was exercised through the relevant real boundaries from controlled preconditions, the durable final outcome and key side effects were verified, diagnostics make failures traceable, repetition/cleanup behavior is understood, and environment limitations are explicit.