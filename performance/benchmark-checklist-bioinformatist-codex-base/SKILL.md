---
name: benchmark-checklist
description: Design, review, or report a measured performance comparison. Use for benchmark methodology, speedup or regression claims, and performance-based choices; not generic performance discussion, ordinary dependency bumps, local renames, or prose edits.
license: MIT
---

# Benchmark Checklist

Vet the claim against measured work. Use the existing benchmark harness and stay
within the task's authority for runs, instrumentation, edits, and publication.

1. State the claim, metric, units, workload, and comparison baseline. Read what
   the harness times, counts, and excludes. A requested quick estimate may use
   one run, labeled as such, but must still check errors and completed work.
   For that estimate, use the quick-estimate report below; steps 2–5 apply to
   comparisons.
   Choosing between options requires a comparison, not a quick estimate.
2. Make the comparison fair: production builds and settings, matched versions,
   data, concurrency, cache state, warmup, and resources. Check machine load and
   load-generator saturation. Name untuned sides; do not select a winner from
   an unfair comparison.
3. Verify correct output and count errors, timeouts, retries, and rejected work.
   Confirm work completed inside the timed region: await promises, consume lazy
   results, and verify requests, rows, or bytes actually reached their target.
4. Identify the limiter with evidence; keep profiling overhead out of reported
   timings. Check physical throughput bounds and how much time the changed
   component could save. Investigate implausible results before reporting them.
5. For a formal comparison, repeat each side at least five times, interleaving
   sides to reduce drift. Report the median and range using the harness's
   statistics where available. Treat differences within noise as no measurable
   difference. Relate microbenchmarks to the end-to-end path users wait on.

For a requested quick estimate, report the observed value, units, environment,
reproduction command, errors and completed work, and label it as a single run
without a comparison verdict. Missing correctness or work evidence makes even
a quick estimate inconclusive.

For a formal comparison, finish with faster, slower, no measurable difference,
or inconclusive; include run count, units, spread, environment, limiter evidence,
and reproduction command.
Mark missing correctness, work, fairness, or limiter evidence as inconclusive.
Separate a measured result from an untested explanation. Stop when the claim is
supported at its stated scope or the remaining evidence gap is explicit.

Adapted from Lauren Tan's [pstack benchmark-checklist](https://github.com/cursor/plugins/blob/6ce45c59b9301a638c1fe1a7b8dc2a82b650898f/pstack/skills/benchmark-checklist/SKILL.md), under the [MIT license](LICENSE).
