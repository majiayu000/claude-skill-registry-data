---
name: patpat-perf
description: Diagnose a resource regression or drive sustained numeric optimization against a measurable target. Use for latency, CPU, memory, throughput, startup, or other performance implementation when comparable before-and-after measurement is practical.
---

# Patpat Performance

When invoked directly, read the [operating protocol](../patpat-loop/references/operating-protocol.md) and [execution graph](../patpat-loop/references/execution-graph.md) in full. Do not load the router.

Read [proof over proxy](../patpat-loop/principles/proof-over-proxy.md), [explain the number](../patpat-loop/principles/explain-the-number.md), [fix root causes](../patpat-loop/principles/fix-root-causes.md), and [smallest safe change](../patpat-loop/principles/smallest-safe-change.md). Apply the [performance playbook](../patpat-loop/playbooks/performance.md) and [benchmark checklist](../patpat-loop/references/benchmark-checklist.md).

Measure the reported surface before reading toward a preferred cause. Keep workload, environment, warm-up, sample policy, and units comparable. Locate the dominant cost, change one causal variable, and preserve correctness and safety invariants.

When the objective requires sustained improvement toward a numeric target rather than one regression fix, apply the [metric hillclimb playbook](../patpat-loop/playbooks/metric-hillclimb.md) through `patpat-run`.

Report the baseline, post-change result, measurement noise, artifact locations, and remaining tradeoffs. Do not claim improvement from a single incomparable or proxy measurement.

## Proof closure

Close repository mutations through:

- [`patpat-verify`](../patpat-verify/SKILL.md)
- [`patpat-review`](../patpat-review/SKILL.md)
