---
name: performance
description: Improve latency, throughput, memory or bundle size with a defined metric, a repeatable baseline and evidence that the change helped.
---

# Performance: measure, profile, optimise, re-measure

- Define the metric before optimising: latency percentile, throughput, memory, query count or bundle size. 'Feels slow' is not a target.
- Measure a representative baseline with a repeatable workload. Record environment, dataset size and variance; one fast run is noise.
- Profile before guessing. Find the dominant cost and optimise that, not the line that looks expensive.
- Change one thing at a time. Keep correctness tests green and re-measure with the same workload.
- Prefer algorithmic and I/O improvements over micro-tuning. Cache only with a clear invalidation rule and a measured hit rate.
- Check the tradeoffs: memory for speed, complexity for latency, staleness for freshness. State which one you accepted.
- Verify the improvement is outside normal variance and that no other metric regressed.

---

_NullByte skill pack. Original guidance for this tool; no third-party skill text is bundled._
