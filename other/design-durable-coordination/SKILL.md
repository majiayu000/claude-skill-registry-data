---
name: design-durable-coordination
description: Design or refactor durable multi-agent coordination on any durable execution engine. Use when a system needs recoverable delegation, parallel branches, external events, timers, approvals, cancellation, compensation, deterministic aggregation, or replay-safe graph and budget state.
---

# Design Durable Multi-Agent Coordination

Keep durable coordination deterministic and isolate all nondeterminism in durable steps.

## Workflow

1. Read the System Spec, interaction, termination, approval, and data-flow policies.
2. Model the workflow state machine: pinned manifest, graph version, delegation records, budgets, approvals, artifacts, branch status, and terminal outcome.
3. Put model calls, member runs, tools, registry lookups, storage, and network I/O in durable steps.
4. Keep routing validation, budget reservation, state transitions, aggregation, termination, and compensation decisions in workflow code.
5. Give each delegation a stable ID and each effect an idempotency key. Let the workflow own retries.
6. Use child workflows only for independently durable sub-processes; bound their number and recursion depth.
7. Bind approvals to action hashes, actor, tenant, manifest, expiry, and current workflow state.
8. Implement cancellation, late result, duplicate result, timeout, partial-effect, and compensation paths.
9. Add replay, worker-restart, external-event-ordering, duplicate-delivery, and new-run (history rollover) tests.

## Required Output

Produce typed workflow and durable-step boundaries, durable state, retry and timeout policy, idempotency strategy, approval protocol, terminal states, and recovery tests.

Read [the durability standard](references/standard.md) before implementation and use [the examples](references/examples.md) for failure paths.

## Guardrails

- Do not call models, tools, registries, clocks, or random APIs from workflow code.
- Do not let individual agents own system retries or termination.
- Do not retry non-idempotent effects without an effect ledger.
- Do not treat a human approval message as an unbound boolean.

## Completion Check

A replay after any worker crash must reconstruct the same graph, budgets, approvals, aggregation decisions, and terminal outcome without duplicating effects.
