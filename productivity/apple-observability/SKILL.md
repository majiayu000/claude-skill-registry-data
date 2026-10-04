---
name: apple-observability
description: "Instrument and diagnose Apple apps using unified logging, signposts, Instruments traces, crash symbolication, memory graphs, and reproducible evidence without leaking user data."
---

# Privacy-safe logs and performance diagnostics

## Inputs

Define the failure claim, candidate/build identity, workload, process, time window, diagnostic tools, privacy scope, and baseline evidence.

## Rules

- **OBS-001 — Log contracts, not payloads.** Prefer state transitions, operation categories, and bounded opaque correlation. Never log credentials or protected content for convenience.
- **OBS-002 — Measure an interval.** Use paired operation boundaries and consistent time units. Instrument success, failure, cancellation, and timeout without double-ending intervals.
- **OBS-003 — Match diagnostic to failure.** Distinguish CPU work, blocking, UI invalidation, allocation growth, and retained objects before proposing fixes.
- **OBS-004 — Preserve raw provenance.** Keep original traces/crashes privately with tool version and capture conditions. A parser summary is an interpretation, not the complete evidence.
- **OBS-005 — Verify without the harness.** Retest the final candidate without temporary fixtures or debugger effects; compare the same workload and report unmeasured claims.

## Workflow

1. Capture the smallest reproducible scenario and privacy-reviewed telemetry.
2. Inspect symbolication and timeline coverage before trusting a summary.
3. Form one ownership or performance hypothesis and add a focused regression test.
4. Measure again and remove or bound temporary diagnostics.

## Verify

Check cancelled intervals, private interpolations, missing symbols, empty traces, repeated presentations, and retained task/observer ownership. Inspect actual artifact contents before sharing.

## Output

Return the candidate, capture contract, evidence-supported diagnosis, change, comparison, and unresolved hypotheses.

## References

- [Logging, signposts, and trace interpretation](references/logging-and-traces.md).
- [Memory graphs and crash investigation](references/memory-and-crashes.md).
