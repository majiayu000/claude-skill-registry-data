---
name: benchmark-checklist
description: Vet a performance measurement or design a fair comparison before using a speedup, regression, throughput, or latency number to make a decision. Use explicitly for benchmark review or measurement validation, not ordinary correctness checks or every incidental timing observation.
disable-model-invocation: true
license: MIT
---

# Benchmark Checklist

Check what the number actually measures before trusting it. Adapted from pstack; see [source notes](UPSTREAM.md).

## Define the decision

State the claim, workload, metric, baseline, and result that would change the decision. Inspect the measurement code: what starts and stops the clock, which work is counted, and which failures are omitted? A quick requested ballpark may use one run, labeled as such; a comparison needs stronger evidence.

## Validate the work

- **Did it happen?** Confirm requests reached the target, results were consumed, asynchronous work was awaited, and writes completed within the claimed measurement boundary. Lazy or cached work can produce spectacular but meaningless numbers.
- **Was it correct?** Count errors, rejections, timeouts, retries, and incorrect outputs separately. Fast failures are not successful throughput.
- **Was it fair?** Match versions, data, build mode, configuration, batching, concurrency, and intended warm/cold conditions. Compare realistic, appropriately tuned setups; label configuration comparisons as configuration comparisons.
- **What limits it?** Use a separate profiling run or system counters to identify the bottleneck. Check the load generator too. Do not treat an unmeasured bottleneck guess as a finding.
- **Is the number plausible?** Compare with CPU, I/O, network, and affected-work limits. Eliminating a component that takes 10% of runtime cannot remove more than 10% of total elapsed time by itself.

## Compare under noise

Keep runtime and concurrency bounded and preserve other agents’ processes. Observe background load; use available platform tools rather than assuming Linux utilities exist. Alternate or randomize A/B order, repeat enough to expose variability, and retain per-run observations. Start with a small pilot before an expensive campaign.

Report appropriate summaries and spread; do not average percentiles as if they were pooled observations. A small gap relative to noise is inconclusive, not a win. The statistical method must match the experiment; absence of a significant difference does not prove equivalence.

Measure the relevant end-to-end path alongside a microbenchmark when the claim is about user impact. Keep profiling overhead out of the reported timing or disclose it.

## Conclude

Say faster, slower, no measurable difference, or inconclusive for the specific workload. Include units, repetitions, variability, correctness/error counts, configuration, and bottleneck evidence. Label missing evidence and estimates. Do not declare a general winner from an untuned side, a single noisy run, or a proxy that omitted the promised work.
