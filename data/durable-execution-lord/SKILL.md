---
name: durable-execution-lord
description: Lord skill for crash-resilient agent workflows using durable execution frameworks — Temporal, Inngest, DBOS, Prefect, Restate — with idempotency, checkpoint/replay, and saga patterns.
triggers:
  - durable execution lord
  - durable execution
  - temporal
  - inngest
  - dbos
  - prefect
  - restate
  - workflow
  - crash resilient
  - تنفيذ دائم
personas:
  - ARCH
  - DEV
  - DEVOPS
  - SRE
tech_stack: []
lord: true

---

# Durable Execution Lord

[OBJ] Design agent workflows that survive crashes, restarts, and partial failures using durable execution frameworks with replay, idempotency, and compensation.

## Problem

Agent workflows span multiple steps, external API calls, human approvals, and long waits. A crash mid-workflow leaves the system in an inconsistent state — half-sent emails, partial database writes, orphaned resources. Traditional try/catch cannot recover a process that died. Durable execution frameworks persist workflow state so any process can resume from the last completed step after a restart.

## Rules

1. [REQ] **When to use durable execution.** Use a durable framework when the workflow is: long-running (>30s), multi-step with external side effects, human-in-the-loop (waits hours/days), or requires guaranteed completion. Short stateless requests do not need it.
2. [REQ] **Temporal patterns.** Use Temporal for complex enterprise workflows. Workflow-as-code (not DSL), durable timers (`workflow.sleep`), automatic retries with backoff, signals (external input mid-workflow), queries (read workflow state without affecting it). Workflows are deterministic — no random, no `Date.now()` inside workflow code.
3. [REQ] **Inngest patterns.** Use Inngest for serverless event-driven workflows. `step.run` for durable steps, `step.sleep` for timed delays, `step.waitForEvent` for external triggers. Fan-out via batch events. No long-lived servers needed — runs on serverless functions.
4. [REQ] **DBOS patterns.** Use DBOS for Python-native workflows with transactional guarantees. Steps are database-backed; checkpoints are DB rows. `@DBOS.step` decorators, `DBOS.sleep`, `DBOS.recv`. Ideal for data-intensive Python pipelines.
5. [REQ] **Prefect patterns.** Use Prefect for data pipelines and ETL. `@flow` and `@task` decorators, `flow.run` for orchestration, native Dask/Spark integration. Good for batch data processing with retry and caching.
6. [REQ] **Restate patterns.** Use Restate for durable services and virtual objects. Virtual objects = keyed actors with durable state. `async` handlers, durable timers, exactly-once invocation. Ideal for stateful agent services.
7. [REQ] **Idempotency.** Every step MUST be idempotent — safe to execute multiple times with the same result. Use idempotency keys (request ID, event ID) at external API boundaries. The framework retries; idempotency prevents duplicate side effects.
8. [REQ] **Checkpoint and replay.** The framework MUST checkpoint after each step. On crash, replay from last checkpoint — re-execute only incomplete steps. Never replay completed steps with side effects (idempotency covers this, but checkpoints prevent unnecessary calls).
9. [REQ] **Error handling.** Distinguish retryable errors (network, 5xx, timeout) from non-retryable (validation, 4xx, auth). Retryable = framework retries with backoff. Non-retryable = fail the step, trigger compensation or human escalation.
10. [REQ] **Timeout and saga patterns.** Every step has a timeout. Long workflows use the saga pattern: each step has a compensating action (undo). On failure, execute compensations in reverse order. No step without a defined compensation for side-effecting operations.
11. [REQ] **Compensation.** Compensations MUST be idempotent and best-effort. If compensation fails, log + escalate to human. Do not infinite-loop on compensation failure. Document what "compensated" means per step (email sent → send retraction, DB write → delete row).
12. [REQ] **Observability.** Every workflow run MUST be traceable: workflow ID, run ID, step history, current status, duration per step. Use the framework's built-in UI (Temporal Web, Inngest Dashboard, Prefect UI) + export metrics to Prometheus/Datadog.
13. [REQ] **Testing durable workflows.** Test workflows by: (a) unit testing individual steps, (b) simulating crashes by killing the worker mid-run and verifying resume, (c) testing compensation by injecting failures at each step. No workflow ships without a crash-resume test.
14. [REQ] **Cost considerations.** Durable frameworks have costs: Temporal (hosting or self-host infra), Inngest (per-invocation), DBOS (DB storage), Prefect (cloud or self-host), Restate (self-host). Estimate cost per workflow run × expected volume before choosing.
15. [REQ] **Framework selection matrix.** Temporal: enterprise, complex, multi-language. Inngest: serverless, event-driven, JS/TS. DBOS: Python, transactional, data-heavy. Prefect: data pipelines, Python, batch. Restate: stateful services, virtual objects, low-latency. Match framework to workload, not hype.
16. [PROHIBIT] Using raw `async/await` with manual state persistence for workflows that have external side effects and must guarantee completion — this is not durable, it is wishful thinking.

## References

- Temporal: https://temporal.io
- Inngest: https://www.inngest.com
- DBOS: https://dbos.dev
- Prefect: https://www.prefect.io
- Restate: https://restate.dev
- Saga pattern: https://microservices.io/patterns/data/saga.html
