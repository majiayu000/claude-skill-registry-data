---
name: perf-measure
version: 0.3.0
license: MIT
metadata:
  formerly: thermometer
description: Use when investigating or improving performance, latency, throughput, memory use, CPU use, startup time, or bundle size. Establishes a repeatable baseline and profiles the measured bottleneck before any optimization. (formerly thermometer)
---

# perf-measure

Performance measurement turns "slow" into a workload, a metric, and a measured boundary. No optimization starts from intuition alone. The same input, environment, and sampling method must exist before and after the change.

## The measurement law

No performance claim without a repeatable baseline and a comparable after measurement. A faster result from a different workload, warm cache, machine, dataset, build mode, or sampling method is not a comparison.

Correctness, security, durability, and accessibility remain requirements. Trading one away for speed requires explicit user approval and must appear in the report.

## Modes

- **Measure and fix** (default): sections 1 through 7 below, one change, one comparison.
- **Climb:** many iterations toward a target on a frozen harness. See [climb](references/climb.md).
- **Diagnose only:** explain a slowdown from a real artifact without changing code. See [diagnosis](references/diagnosis.md).

Whatever the mode, a number is not believed until it passes [distrust the number](references/distrust-the-number.md).

## 1. Pin the question

Turn the complaint into one primary metric:

- latency for a named operation and percentile
- throughput under a stated concurrency level
- peak or retained memory for a defined workload
- CPU time or utilization for a named process
- startup time to a defined ready signal
- artifact or bundle size for a named build target

Name the workload, environment, dataset size, cache state, build mode, and target. If no target exists, use the baseline to quantify the opportunity and report the measured result without inventing a service-level objective.

Before collecting samples, record the decision the measurement will inform and
the smallest difference that would change it. State how you will judge noise.
If repeated runs vary more than that difference, stop and report that the
measurement cannot support the decision.

## 2. Choose the proving command

Prefer the repository's existing benchmark, load test, profiler, tracing setup, or production-like fixture. Otherwise build the smallest repeatable command that exercises the reported path.

The command must produce machine-readable or plainly comparable output. Record tool versions and material environment settings. Avoid a new benchmark framework when a stable existing command can measure the path.

## 3. Establish the baseline

1. Confirm the workload returns correct results.
2. Warm up when the runtime, cache, or just-in-time compiler needs it. Keep cold-start work cold when startup is the metric.
3. Collect at least five samples unless each run is prohibitively expensive.
4. Record the median and range or another spread measure appropriate to the tool.
5. Keep raw samples available for review.

A single timing is a smoke check, not a performance baseline.

## 4. Profile before editing

Use the profiler or tracing tool suited to the metric:

- CPU profiles for compute time
- allocation or heap profiles for memory
- query plans and database timing for data access
- network traces for remote wait time
- build analyzers for bundle or artifact size
- structured spans for request-path latency

Identify the measured bottleneck and its share of the total. If the hot path is external or outside the user's scope, stop and report it rather than polishing a cold path.

## 5. Form one hypothesis

State the mechanism and expected effect before changing code:

```text
The profile attributes <measured share> to <operation> because <mechanism>.
Changing <one boundary> should improve <primary metric> without changing <contract>.
```

Pick the cheapest lever first. Work down this list and stop at the first rung that the profile supports:

1. **Do not do it.** Is the work needed at all? Delete it.
2. **Do not repeat it.** Cache, memoize, hoist out of the loop, batch.
3. **Do less.** Narrower query, smaller payload, early exit, fewer fields.
4. **Do it later.** Defer, lazy-load, move off the critical path.
5. **Do it concurrently.** Overlap independent waits or work.
6. **Do it cheaper.** A better algorithm, structure, or library for the same work.

Earlier rungs are usually cheaper and often win bigger, but the profile decides; if only a cheaper implementation fits, say why the earlier rungs do not apply.

Make one minimal change. Do not bundle cleanup, a new architecture, three caches, and a concurrency rewrite into one result that cannot be explained.

## 6. Compare like with like

Repeat the exact baseline procedure after the change:

- same command and arguments
- same dataset and cache state
- same build mode and environment
- same warm-up and sample count
- same metric extraction

Compare median and spread, not only the best run. If the claimed improvement is smaller than run-to-run noise, the result is inconclusive. Revert the optimization or report it as unproven.

## 7. Verify the contract

Run the focused and full correctness checks that cover the changed path. Inspect error handling, ordering, consistency, resource limits, and concurrency behavior when relevant.

Run the [distrust-the-number checklist](references/distrust-the-number.md) on the after measurement. Use `superpowers:verification-before-completion` before reporting a gain. Quote the baseline samples, after samples, comparison, profiler evidence, and correctness command.

## Performance report

```markdown
# perf-measure: <operation> (<date>)

## Workload
- Command:
- Environment:
- Dataset and cache state:
- Primary metric and target:

## Baseline
- Raw samples:
- Median and spread:

## Profile
- Measured bottleneck:
- Share of total:

## Change
- Hypothesis:
- Minimal implementation:

## Result
- Raw samples:
- Median and spread:
- Relative and absolute change:

## Correctness
- Commands and results:

## Limits
- Noise, environment gaps, and the measured ceiling:
```

## Stop conditions

Stop when (an inconclusive result is a valid outcome; report it as such):

- the workload cannot be reproduced consistently
- profiler overhead or environmental noise exceeds the expected gain
- the measured bottleneck is an unavailable external service
- the proposed change alters correctness, security, or a public contract without approval
- a second optimization requires a different workload or hypothesis

## Common mistakes

- Optimizing the code that looks expensive without profiling it.
- Comparing debug and release builds, cold and warm caches, or different datasets.
- Reporting the fastest sample instead of the distribution.
- Adding a cache without defining invalidation and memory bounds.
- Keeping a complex change whose measured gain fits inside the noise.
- Measuring speed and skipping correctness checks on the changed path.
- Trusting a number without asking what limits it and why it is not twice as good.
- Starting at "do it cheaper" when "do not do it" was available.
- Reporting a gain from a harness that cannot tell an easy case from the target case.
