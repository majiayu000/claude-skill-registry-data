---
name: debugging
description: Use when a bug's cause is unknown. Applies a hypothesis-driven method — reproduce, isolate, instrument, prove — instead of speculative edits, and covers profiler, debugger, and log-based investigation.
metadata:
  category: development
  version: 1.0.0
  tags: [debugging, root-cause, diagnostics, profiling]
---

# Debugging

## Purpose

Find the actual cause of a defect, not a change that makes the symptom disappear. Debugging is a search problem, and the method is binary search over hypotheses.

## When to Use

- A test fails and the reason is not obvious from the assertion.
- Production behavior differs from local behavior.
- An intermittent or timing-dependent failure.
- A performance regression with no obvious cause.
- A bug that "came back" after being fixed.

## Capabilities

- Deterministic reproduction, including of flaky failures.
- Bisection over code history, input space, and configuration.
- Instrumentation: strategic logging, breakpoints, tracing, core dumps.
- Concurrency debugging: race detectors, deadlock analysis, lock ordering.
- Performance debugging: CPU and allocation profiles, flame graphs.

## Inputs

- The failure: error message, stack trace, failing test, or observed behavior.
- The last known-good state, if any.
- Environment differences between where it fails and where it does not.

## Outputs

- A reproduction that fails reliably.
- A stated root cause, with the evidence that proves it.
- A fix, plus a regression test that fails without the fix.

## Workflow

1. **Reproduce** — Reduce to the smallest input and shortest path that still fails. If you cannot reproduce it, you cannot verify a fix. For flaky failures, run in a loop until you have a failure rate.
2. **Read the evidence** — Read the entire stack trace, including the parts you have seen before. Read the actual error, not the one you assume it is.
3. **Form one hypothesis** — State it as a falsifiable claim: "the cache returns a stale value because the invalidation runs before the write commits."
4. **Test the hypothesis** — Add instrumentation that would distinguish true from false. Do not change behavior yet.
5. **Bisect** — If no hypothesis survives, bisect. `git bisect` over commits; comment out halves of the input; disable half the config.
6. **Prove the cause** — You have the cause when you can turn the bug on and off at will.
7. **Fix and regress** — Write the failing test first, then fix, then confirm the test passes and the rest still do.

## Best Practices

- Never change two things at once. You will not know which one mattered.
- "It works now" without an explanation means the bug is still there.
- Trust the machine over your memory of what the code does — read the code that is running, on the branch that is deployed.
- If the bug is in a dependency, prove it with a minimal script before reporting or working around it.
- Timing-dependent bugs are nearly always missing synchronization or an assumed ordering. Look for shared mutable state first.
- Delete instrumentation you added, or promote it to permanent, structured logging. Do not leave debug prints behind.

## Examples

**Hypothesis log for an intermittent failure:**

```text
Symptom : /checkout returns 500 approximately 1 in 40 requests under load.
Evidence: Stack trace shows NullPointerException in CartCache.get(); no error at low load.

H1: Cache eviction races with read.
    Test: log cache size + key on every get/put; run 500 concurrent requests.
    Result: FALSE — evictions never coincide with the failures.

H2: Cart is written by request thread but read by an async pricing task
    before the write commits.
    Test: log thread id and transaction id at write and at read.
    Result: TRUE — pricing task reads on a different connection, 3-8ms before commit.

Cause: Async task enqueued inside the transaction, executed outside it.
Fix  : Enqueue on transaction commit (after-commit hook).
Test : Regression test asserting the task is not enqueued until commit.
```

## Notes

- `git bisect run <script>` automates bisection completely when you have a scripted reproduction. It is the single highest-leverage debugging tool most engineers underuse.
- Heisenbugs that vanish under a debugger are usually timing or optimization-related. Reach for logging and race detectors instead of breakpoints.
- A bug that reappears was never fixed — the original fix addressed a symptom. Reopen the investigation rather than patching again.
