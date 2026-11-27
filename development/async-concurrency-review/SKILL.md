---
name: async-concurrency-review
description: "Review or improve async/await, cancellation, bounded concurrency, worker lifetimes and UI continuation correctness in .NET code."
---

# Async and concurrency review

1. Inspect target framework, app model (ASP.NET Core, Blazor, MAUI, library, worker), code and callers. Read `knowledge/ASYNC_AWAIT_CONCURRENCY.md` and path-scoped async rules.
2. Classify every changed operation: dependent vs independent; I/O vs CPU; request vs background; UI-context vs context-independent; idempotent vs irreversible.
3. Search for sync-over-async, forgotten `await`, `async void`, `Task.Run` misuse, unbounded `Task.WhenAll`, non-propagated cancellation, shared `DbContext` fan-out, blocking locks, swallowed task faults and unowned fire-and-forget work.
4. Cite concrete file:line, failure mode and smallest viable repair. Explain any concurrency/timeout tradeoff. Do not treat all loop awaits as bugs or `ConfigureAwait(false)` as mandatory.
5. When implementation is requested, make a small diff, add tests (fault/cancel/concurrency/lifetime), and run applicable build/tests. For worker jobs require shutdown/idempotency evidence; for UI require dispatcher/render context checks.
6. Report actual checks and remaining risks. Do not enable new analyzers/packages or tune concurrency constants without repo context and measurement.

**Review-only use:** do not modify files unless implementation is explicitly requested.
