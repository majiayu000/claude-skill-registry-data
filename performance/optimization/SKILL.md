---
name: optimization
description: Use when improving performance, latency, throughput, memory usage, or general efficiency. Start by defining target metrics, measuring comprehensively, attributing bottlenecks, validating with static analysis, and prioritizing macro-optimizations before micro-optimizations.
allowed-tools: bash, read, write, grep, agentgrep, batch, todo
---

# Optimization

Use this skill when the task is about making a system faster, lighter, more scalable, or otherwise more efficient.

## Core principle

To optimize properly, you must know:

1. **What metrics you are chasing**
2. **What your real bottlenecks are**

Do not optimize blindly.

## 1. Define the target metrics first

Before changing code, make sure you have the right measurements.

- Identify the exact metrics that matter: latency, throughput, memory, CPU, startup time, compile time, query count, token usage, cost, etc.
- Measure **comprehensively**, not just a convenient subset.
- Make sure the metrics are accurate and representative of the real workload.
- Prefer measurements that are fast to run so you can iterate quickly.
- If possible, create repeatable benchmarks or scripts so improvements are verifiable.

## 2. Get full bottleneck attribution

You should have strong attribution for what each part of the system is doing.

- Instrument the system so you can see where time and resources are going.
- Prefer both:
  - **Ad hoc inspection** for quick debugging
  - **Logged measurements** for later analysis and comparison
- Attribute work across the full path, not just the obviously slow component.
- Make sure the data is detailed enough to explain where the cost comes from.

If you can analyze runs after the fact with logs or traces, that is often much more powerful than relying only on live inspection.

## 3. Use static analysis too

Not every optimization problem needs runtime profiling first. Often, code inspection reveals the issue.

Check for:

- Wrong asymptotic complexity
- The wrong algorithm or data structure
- Unnecessary repeated work
- Work happening in the wrong layer
- Inefficient architecture or control flow
- Directionally incorrect approaches

Make sure your asymptotics are right and the overall algorithm makes sense before tuning small details.

## 4. Macro-optimize before micro-optimizing

Prioritize the largest wins first.

- Remove whole classes of work before making existing work slightly cheaper.
- Fix architecture, batching, caching, query patterns, algorithm choice, parallelism, and data movement before focusing on tiny low-level tweaks.
- If you are very far from the expected metrics, spend more time on macro-optimization.

Micro-optimizations matter most after the major inefficiencies are already addressed.

## Recommended workflow

1. Define success metrics.
2. Reproduce the current baseline.
3. Add measurement and attribution if missing.
4. Identify the top bottleneck.
5. Check for algorithmic or architectural issues.
6. Apply the highest-leverage fix first.
7. Re-measure.
8. Repeat until the target is met or tradeoffs stop being worth it.

## Guardrails

- Do not claim an optimization without before/after evidence.
- Be careful not to optimize the wrong metric.
- Watch for regressions in correctness, reliability, maintainability, and security.
- Prefer changes that are measurable, explainable, and reversible.
