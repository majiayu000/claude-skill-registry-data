---
name: swift-concurrency-runtime
description: Design production Swift concurrency. Use when ownership, cancellation, actor reentrancy, streams, admission, deadlines, or shutdown affect correctness.
license: MIT
metadata:
  author: "coryparrry"
  version: "0.1.0"
  last-updated: "2026-08-30"
  last-reviewed: "2026-08-30"
  apple-docs-reviewed: "2026-08-30"
---

# Swift Concurrency Runtime

Make ownership, capacity, and shutdown explicit, then prove behavior under adversarial timing.

## Runtime contract

For each unit of work, identify:

- owner, lifetime, cancellation source, and completion observer;
- mutable-state owner and invariants crossing `await`;
- numeric capacity and queue/coalesce/replace/drop/reject policy;
- success, failure, cancellation, timeout, supersession, and shutdown semantics.

Keep these invariants:

- Cancellation is cooperative. A canceled task-group scope still drains children; an uncooperative loser can defeat a naive timeout.
- Actors serialize access, not transactions across suspension. Revalidate identity, generation, or state before committing after `await`.
- Unstructured tasks are valid when deliberately supervised: retain the handle, bound creation, define cancellation/drain, and reject stale or duplicate completion.
- Streams need an intentional buffer and upstream termination path. An actor does not make an unbounded queue safe.
- `@MainActor`, `Task.detached`, and `@unchecked Sendable` require semantic justification rather than serving as general fixes.

Read [references/runtime-design.md](references/runtime-design.md) for deadline races, actor patterns, bounded admission, `AsyncStream`, and shutdown ordering.

## Workflow

1. Bind the toolchain and Swift language mode, strict-concurrency level, default actor isolation, Approachable Concurrency setting, enabled upcoming/experimental features, exact executable/configuration, and observable failure. These settings change isolation and diagnostics; the project label alone is insufficient.
2. Map task ownership, state invariants, capacity, and terminal states before editing.
3. Force the smallest failing interleaving with controllable dependencies, clocks, or gates instead of sleeps.
4. Change the narrow ownership, cancellation, or invariant rule supported by evidence.
5. Verify cancellation before/during/after work, reentrancy, saturation, late results, and shutdown as relevant.

Read [references/diagnosis-and-tests.md](references/diagnosis-and-tests.md) for failure classification, deterministic probes, and adversarial scenarios.

## Completion

Report the ownership/capacity model, cancellation propagation, terminal behavior, targeted tests, and runtime evidence for live hangs, leaks, storms, or duplicate work. State any harness boundary that prevented observation.

Consult [references/apple-documentation.md](references/apple-documentation.md) for reviewed Apple API anchors and refresh conditions.

## Review

- Last updated: 2026-08-30
- Last reviewed: 2026-08-30
- Apple documentation reviewed: 2026-08-30

Swift concurrency ownership, cancellation, actor isolation, streams, and shutdown guidance was reviewed against Apple evidence surfaced through Xcode MCP `DocumentationSearch`.

[Apple documentation evidence](references/apple-documentation.md)
