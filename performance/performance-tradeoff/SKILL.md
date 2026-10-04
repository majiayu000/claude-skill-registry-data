---
name: performance-tradeoff
description: Measure and judge hardware-bound optimization tradeoffs involving latency, throughput, CPU/GPU/device or unified memory, headroom, capacity, OOM, fallback, offload, admission limits, or workload size. Use for benchmark design or execution, performance-claim review, hardware qualification, and optimization acceptance decisions. Do not use for routine cleanup or performance-neutral refactors with no material resource claim.
---

# Performance Tradeoff Evaluation

## Establish the claim

Treat the pre-change implementation as the **baseline** and the proposed implementation as the **candidate**. Identify:

- the claimed benefit;
- the affected phase and operation frequency;
- the target hardware and plausible user workload;
- quality and correctness criteria that must remain unchanged;
- applicable lifecycle behavior, including cancellation, fallback, cleanup, and subsequent jobs.

Label every material claim **measured**, **estimated**, or **missing**. When required evidence is missing, define the minimum benchmark, classify the decision as **unproven**, and stop short of acceptance or rejection based on invented values or estimates presented as measured relief.

## Make the comparison equivalent

Use identical hardware, software, model, driver, workload inputs, quality settings, cache and warmup state, and relevant power or thermal conditions. Record every deviation.

Run identical cases in both arms. Use fresh processes when allocator history or retained state can matter. Include warmups; alternate or randomize arm order; record samples per arm, failures, the statistic used, and observed spread. Do not substitute a different machine for a hardware-bound claim.

Recompute every absolute and percentage delta from the raw baseline and candidate values, state the percentage denominator, and flag inconsistent supplied arithmetic instead of repeating it.

## Measure time

Report the baseline, candidate, absolute delta, and percentage delta for:

- the affected operation;
- the affected phase;
- the complete user-visible workload.

Report operation frequency and cumulative repeated cost. Interpret absolute end-to-end impact before percentages.

## Measure memory and capacity

For memory claims, report where available:

- allocated, reserved, process or device-reported, and externally sampled memory;
- peak phase and relative timestamp;
- physical capacity, effective usable device or unified-memory budget, and headroom calculation;
- sampling interval and missed-transient risk;
- OOM, fallback, offload, admission rejection, allocator pressure, and workload-reduction behavior;
- the largest **tested plausible** workload each arm completes reliably.

Classify the result as exactly one of:

1. **Capacity-enabling** — the baseline fails, falls back, or cannot admit a plausible supported case; the candidate completes the identical case reliably.
2. **Boundary-protecting** — the baseline is inside a predeclared unsafe headroom margin; the candidate repeatedly restores the declared safe margin.
3. **Resource-reducing only** — memory falls without a demonstrated capability, reliability, concurrency, operating-cost, or supported-workload change.

Declare any unsafe margin before inspecting candidate results. When memory relief supports acceptance, sweep a plausible workload dimension to the baseline's real boundary, then run identical cases with the candidate. Do not manufacture an implausible oversized workload.

## Judge the result

Decide in this order:

1. correctness and output quality;
2. real workload capability or stability;
3. absolute end-to-end user cost;
4. fresh-process repeatability;
5. lifecycle behavior;
6. implementation and maintenance cost;
7. percentages as supporting context.

Capacity-enabling or genuine boundary-protecting results may justify a modest measured latency cost when quality and lifecycle behavior remain sound. Resource-reducing-only results normally do not justify added complexity or regression without another measured operational benefit.

## Report one decision per hardware and workload case

Use this schema without forcing unavailable numbers:

> On `<hardware>`, for `<workload>`, the candidate changes memory at `<phase and relative timestamp>` from `<baseline>` to `<candidate>` (`<absolute delta>`, `<percentage>`), moving measured headroom from `<before>` to `<after>`. It `<does/does not>` avoid `<OOM/fallback/offload/admission failure/severe allocator pressure/workload reduction>`. The affected operation occurs `<frequency>` and changes time from `<baseline>` to `<candidate>` (`<absolute delta>`, `<percentage>`), producing an end-to-end change from `<baseline>` to `<candidate>` (`<absolute delta>`, `<percentage>`). Evidence: `<warmups; samples per arm; ordering; statistic and spread>`. Quality and applicable lifecycle checks: `<result>`. Classification and decision: `<class; accept/reject/unproven; rationale>`.

Use `not measured`, `not applicable`, or `unproven` where appropriate. Report the largest tested case, not an unbounded maximum.
