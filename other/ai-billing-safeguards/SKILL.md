---
name: ai-billing-safeguards
description: Design and verify provider-neutral spend, token, request, and concurrency controls for AI workloads. Use when an application or agent can incur usage.
license: MIT
---

# AI Billing Safeguards

Cost controls are enforcement, not a dashboard. Use both provider/account limits and application-side guards.

## Requirements

1. Define scope: organization, project, user, workflow, agent, request, and billing period.
2. Load current rates and units from a versioned configuration or provider billing export. Never embed a reusable "current price" or assume a model tier is permanently cheap/expensive.
3. Estimate the maximum authorized cost before each call using requested limits, tool rounds, retries, cache behavior, image/audio units, and fallback routes.
4. Atomically reserve budget before work and reconcile it with provider-reported usage afterward. Release unused reservation.
5. Reject work that would exceed a hard limit. Warn at configurable thresholds and preserve partial results.
6. Bound requests, tokens, output, tool rounds, retries, concurrency, elapsed time, and external operations—not dollars alone.
7. Attribute every usage event to a stable task/user/workflow ID without logging prompts, secrets, or personal data.
8. Treat fallback/provider routing as a separate authorization and data-boundary decision; a budget guard must not silently send data elsewhere.

## Usage ledger

Record timestamp, provider/account, configured model ID, rate-table version, input/output/cache/media units, estimated cost, reconciled cost, currency, reservation ID, task attribution, retry/fallback reason, and limit decisions. Use idempotency keys so retried accounting cannot double-charge the ledger.

## Failure policy

- fail closed when rate data or currency conversion required for enforcement is missing;
- distinguish quota, billing, authentication, transient, and application errors;
- never retry a billing/quota denial indefinitely;
- surface a bounded error with spent/reserved/remaining amounts and recovery options;
- prevent concurrent workers from racing past a shared limit.

## Validation

Test exact-boundary acceptance, one-unit-over rejection, concurrent reservations, provider under/over-reporting, retry reconciliation, cache units, fallback denial, stale rate tables, partial streaming, cancellation, clock/period rollover, and ledger restart recovery. Compare a sample against the actual provider bill/export.

## Completion report

State limits, current rate source/version, enforcement points, alerts, ledger location, tests, observed gaps, and who can raise a limit. Never change quotas, billing accounts, or spending limits without the user's explicit authorization for that external change.
