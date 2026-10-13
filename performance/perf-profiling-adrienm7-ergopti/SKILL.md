---
name: perf-profiling
description: Measure a driver before proposing or implementing performance work. Use for AHK, Hammerspoon, latency, hot-path, startup, CPU, or memory audits; also matches "audit perf AHK" and "audit perf Hammerspoon".
---

# Performance profiling

Do not optimize from intuition. Establish a reproducible baseline, label every
number's provenance, change one mechanism, and repeat the same measurement.
Complexity or operation counts are useful hypotheses; they are not measured
latency.

Read only the scope reference that matches the request:

- Windows/AutoHotkey: [references/ahk.md](references/ahk.md)
- macOS/Hammerspoon: [references/hammerspoon.md](references/hammerspoon.md)

Before proposing a cache or architectural shortcut, read
`docs/memory/README.md` and the relevant topic plus
`docs/memory/rejected_proposals.md`. A cache is an optimization only when its
invalidation contract is proved.

## Shared method

1. Resolve the real runtime log directory before asserting that evidence exists
   or is absent. A log filename records process start; date events from their
   line timestamps.
2. Record the time window, input/workload, machine state, sample count, and
   command or script used. Report tail behavior and maximum, not mean alone.
3. Trace the highest-frequency path and count allocations, lookups, I/O, native
   calls, and work repeated with an unchanged result.
4. Prefer removing unnecessary work to adding a cache. Do not trade an ordering,
   ownership, suspension, privacy, or output guarantee for speed.
5. Measure after with the same method and run every gate selected by
   `verify-change`.

An audit reports proposed changes; it does not edit production code unless the
user explicitly asks for implementation. Never weaken a test to obtain a green
performance change, and never push without current authorization.
