---
name: swift-concurrency
description: "Design or repair Swift async/await, actors, Sendable boundaries, cancellation, task ownership, stale results, continuations, and Swift 6 migration."
---

# Concurrency and lifecycle

## Inputs

Record Swift compiler version, language mode, default actor isolation, upcoming feature flags, task owner, cancellation trigger, and every mutable value crossing an isolation boundary.

## Rules

- **CONC-001 — Isolate ownership.** Keep UI state on its intended actor and transfer immutable `Sendable` values across boundaries. Do not silence an ownership defect with `@unchecked Sendable` or `nonisolated(unsafe)`.
- **CONC-002 — Own every task.** Prefer structured child tasks and view-bound `.task(id:)` for view work. Give longer-lived work an explicit service owner, cancellation path, and completion policy.
- **CONC-003 — Cancellation is cooperative.** Check cancellation around expensive work and before publication. Cancellation alone does not prove an obsolete response cannot commit.
- **CONC-004 — Revalidate after suspension.** Actor isolation prevents simultaneous access, not logical races across `await`; validate request identity, account, and generation before applying results.
- **CONC-005 — Async is not background execution.** Verify executor semantics for the compiler settings. A `Task` created on the main actor can still perform blocking CPU work there.

## Workflow

1. Trace start, suspend, resume, cancel, and teardown for each operation.
2. Use a request generation or domain identity to reject obsolete results; make cleanup generation-aware too.
3. Bound fan-out, buffering, retries, and resource use. Specify stream termination and backpressure.
4. Adapt callbacks with exactly-once continuation completion and race-safe cancellation.
5. Test controlled completion order, not wall-clock sleeps.

## Verify

Run strict-concurrency builds in the intended language mode. Test replacement, cancellation, delayed failure, logout, reentrancy, and repeated teardown. Use controlled fakes to make interleavings deterministic.

## Output

Return an isolation/lifetime map, failure scenario, fix, and deterministic tests. Distinguish compiler data-race checks from business-ordering guarantees.

## References

Read the [playbook](references/concurrency-patterns.md) for decisions, failure cases, and source links.

For streams, continuations, and compiler migration, read the [focused reference](references/streams-and-migration.md).
