---
name: performance-optimization
description: "Investigate slow paths and optimize measured bottlenecks."
license: MIT
metadata:
  author: Addy Osmani and Skillz contributors
  source: addyosmani/agent-skills
  source-commit: 1401c8b8030e023baeebb31781a6653fe8e93026
  adaptation: curated-rewrite
  owner: software-factory
  risk: medium
  capabilities: addyosmani,performance-optimization
---

# Performance optimization

Use measurements to choose a bottleneck, change one cause, and compare the
result under the same workload. A suspected regression justifies investigation;
it does not justify speculative caching, rewrites, or larger infrastructure.

## Establish the baseline

Name the user journey or operation, observed symptom, and agreed performance
budget. Record revision, dataset, runtime, hardware or device class, network,
cache state, concurrency, and measurement method. Repeat enough to identify
noise and state the sample size. Keep cold-start and warm measurements separate.

For web work, distinguish field data from laboratory traces. Field Core Web
Vitals use real user experiences; a Lighthouse run or synthetic interaction
cannot establish production INP. Verify current metric definitions and thresholds
against [web.dev's Web Vitals guide](https://web.dev/articles/vitals) when using
them. Report device segments and the period covered by field measurements.

For services, inspect latency distributions, throughput, errors, saturation,
queue time, and query counts. CPU time alone does not explain I/O waits. Use
representative payloads and concurrency within the authorized test budget.

## Find and change the cause

Trace one slow path through rendering, network, application code, queries, and
external dependencies as relevant. Optimize the measured bottleneck:

- Remove unnecessary requests or N+1 queries after verifying the access pattern.
- Reduce shipped or decoded bytes when transfer or parsing dominates.
- Break up long main-thread work when it blocks measured interactions.
- Change indexing or query shape after examining the actual execution plan.
- Reduce retained objects or concurrency when memory or saturation is the limit.

Keep correctness checks alongside the benchmark. Do not trade away authorization,
data freshness, error handling, or output quality to improve a metric. Request
architecture or product decisions when the tradeoff exceeds the agreed scope.

## Cache only with a consistency contract

Include every response-varying input in the key, including tenant, permissions,
locale, and feature state where relevant. Define invalidation, retention,
acceptable staleness, and behavior after authorization changes. Bound memory,
handle concurrent misses, and distinguish missing data from dependency failure.

For money, permissions, or inventory decisions that require freshness, use the
authoritative state at the decision boundary. A faster stale answer can be a
correctness bug. Test cross-tenant isolation and stale-data behavior explicitly.

## Compare, keep, or revert

Repeat the baseline workload with the same method. Report absolute values,
relative change, noise, and any cost or error regression. If the result does not
support the hypothesis, revert only this task's experiment and record what was
learned. Stop when the agreed budget is met or a dependency blocks measurement.

Add a representative regression check or monitoring signal where it will catch
the demonstrated failure. Avoid brittle timing assertions in ordinary unit
tests. Do not claim a production improvement from a local microbenchmark.
