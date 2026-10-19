---
name: design-durable-execution
description: Design or review durable agent execution on any durable execution engine. Use when adding workflows, durable steps, retries, timeouts, idempotency, external events, human approval, continuing as a new run, payload versioning, replay tests, or recovery for long-running agent work.
---

# Design Durable Agent Execution

Use a durable execution engine to make orchestration recoverable while keeping model calls and other nondeterministic work inside durable steps.

## Workflow

1. Confirm that the agent needs durable execution. Use `ephemeral` execution only for bounded work without externally visible side effects; use `durable` or `human_governed` execution for engine-backed paths.
2. Draw the workflow boundary. Put only deterministic coordination, durable state transitions, timers, external events, read-only state inspection, and durable-step scheduling in workflow code.
3. Put model inference, agent runs, database access, network I/O, file I/O, random values, and wall-clock decisions in durable steps.
4. Define versioned, schema-validated payloads for workflow inputs, step inputs, results, external events, and externally stored state.
5. Assign stable business identifiers to workflows and idempotency keys to side-effecting steps.
6. Configure timeouts and retries by failure class. Never blindly retry authentication failures, invalid input, policy denial, or non-idempotent writes.
7. Model human approval as an explicit workflow state with an external event, timeout, authorized actor, and audit record.
8. Bound histories and payload sizes. Use external artifact storage and continue as a new run when histories can grow indefinitely.
9. Add unit, integration, controlled-clock, failure-injection, idempotency, and replay tests.
10. Document deployment compatibility for in-flight workflows.

## Required Separation

```text
durable workflow -> schedules durable step -> builds/runs agent -> calls allowed tools
```

Read [the durability standard](references/standard.md) before implementing workflow code. Use [the examples](references/examples.md) for retry, approval, and workflow patterns.

## Guardrails

- Do not call a model or external service from workflow code.
- Do not use unconstrained retries for side effects.
- Do not persist large transcripts in workflow history.
- Do not change workflow behavior for in-flight executions without replay testing or versioning.
- Do not treat durability as authorization.

## Completion Check

Demonstrate recovery after worker loss, safe step retries, deterministic replay, approval timeout behavior, and trace correlation across workflow, durable step, agent run, model call, and tool call.
