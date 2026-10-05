---
name: temporal-orchestration
description: Design, implement, and verify durable Temporal workflows and activities for long-running or failure-prone processes. Use for retries, timers, signals.
license: MIT
---

# Temporal Orchestration

## Boundary

Workflow code must be deterministic and replay-safe. Put network, filesystem, database, randomness, clock access, and AI/provider calls in activities. Never place credentials or large payloads in workflow history.

## Design

1. Define business ID, idempotency key, inputs/outputs, states, timeouts, cancellation, retention, and completion criteria.
2. Split activities around independently retryable external effects, not every function call.
3. Configure schedule-to-close/start-to-close/heartbeat timeouts and retry policy from failure semantics. Mark validation, authorization, and permanent business failures non-retryable.
4. Make activities idempotent because at-least-once execution is possible. Record external operation IDs before retryable effects.
5. Use signals for commands, queries for read-only state, updates when a validated synchronous mutation is required, and child workflows for independently managed lifecycles.
6. Model compensation explicitly; compensation is not a database rollback and must itself be retryable/idempotent.
7. Bound history growth with continue-as-new and pass compact state, not an ever-growing event log.

## AI activities

Keep prompt/model/provider selection and billing/privacy controls inside activity configuration. Use the project's current configured provider/model and verify support at runtime; do not hard-code a default or change it automatically. Persist only the minimum reproducible request/result metadata permitted by privacy policy. Bound tokens, tool rounds, retries, concurrency, and cost. Do not retry non-idempotent tool effects blindly.

## Evolution and deployment

Use Temporal's supported workflow versioning/deployment mechanism for the installed SDK/server version. Existing executions must replay against compatible code. Test replay of real histories before removing old paths. Deploy workers with graceful shutdown, task-queue compatibility, observability, and rollback.

## Testing

Run deterministic unit tests, time-skipping tests, activity mocks, retry/timeout/cancellation tests, signal/update races, duplicate activity execution, compensation failure, continue-as-new, worker restart, and history replay. Add a bounded integration test against an authorized local/test server.

## Completion report

Document workflow/activity boundaries, IDs, timeouts/retries, idempotency, history strategy, versioning, worker topology, tests, observability, security/data boundary, and rollback. Do not deploy or alter a production namespace without explicit authorization.
