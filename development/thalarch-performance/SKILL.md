---
name: thalarch-performance
description: >
  Evidence-driven performance engineering for latency, throughput, CPU, memory, startup, build
  time, rendering, I/O, concurrency, and scalability problems. Use for explicit optimization work
  or when profiling/benchmark/build evidence is needed before changing a hot path or feedback loop.
---

# Thalarch Performance

Performance work starts with a metric and comparable evidence, not with code that merely looks
faster.

## 1. Classify the scenario before measuring

For runtime performance establish:

- user/business-visible metric;
- workload/input distribution;
- environment/hardware/runtime;
- baseline and target/regression threshold;
- correctness constraints that optimization must preserve.

For **build/tooling performance**, additionally classify:

- local developer loop vs CI;
- debug/development vs release/distribution artifact;
- cold vs warm vs incremental vs no-op build;
- exact command the user actually waits for;
- dominant phase/task from logs/profile/build scan;
- cache state and whether dependencies/toolchains were already present.

Never compare a cold build to a warm build and call the difference an optimization.

## 2. Find the bottleneck

Use the strongest available evidence for the stack:

- profiler/flame graph;
- tracing;
- benchmark;
- query plan;
- allocation/GC profile;
- browser/device performance trace;
- application metrics;
- build scan/profile/task timing;
- compiler/build reports;
- controlled instrumentation.

Do not optimize a guessed bottleneck merely because it is visually obvious in source.

If execution is unavailable, state that the diagnosis is **static/log-based** and keep runtime
claims `UNVERIFIED`.

## 3. Same-workload rule

A performance result is comparable only when the meaningful conditions match.

Record the exact baseline command/scenario. After each meaningful change, rerun the same workload
and same relevant cache/build state.

For build work, optimize the loop that matters. Do not make local development faster by silently
removing required release artifacts from CI, and do not benchmark a broad `build` task if the user
actually waits on a specific module/link/test task.

## 4. Optimization order

Prefer high-leverage fixes:

1. eliminate unnecessary work/I/O/artifacts;
2. improve algorithm/data structure/query shape;
3. narrow the build/target/workload to what the current loop genuinely needs;
4. restore healthy caching/incrementality before exotic tuning;
5. batch/cache/reuse with a clear invalidation/lifetime model;
6. reduce allocations/copies/serialization/generated work;
7. improve concurrency/backpressure;
8. tune runtime/framework/build settings;
9. experimental switches and micro-optimization only when measurement still points there.

Change one causal surface at a time when practical so improvements can be attributed.

## 5. Cache discipline

A runtime/data cache requires explicit answers for:

- key identity;
- value lifetime;
- invalidation;
- size bound/eviction;
- concurrency;
- stale-data semantics;
- failure behavior.

A build cache requires understanding of inputs/outputs, invalidation, reproducibility and CI/local
policy. Do not enable caching blindly when tasks are not safe/reproducible.

An unbounded map is not a performance solution.

## 6. Concurrency

More parallelism can reduce performance. Measure queueing, saturation, contention, context
switching, downstream rate limits, memory pressure, cancellation behavior and worker/process
oversubscription.

For JVM concurrency route to `thalarch-jvm-concurrency` when the problem touches execution safety
or virtual/platform thread semantics.

## 7. Build-specific diagnosis

For Gradle/Maven/Cargo/Go/npm/native/Xcode/other builds, find the phase that dominates instead of
assuming “the compiler is slow”.

Typical buckets:

- dependency/toolchain download;
- configuration/project discovery;
- code generation/annotation processing;
- compilation;
- linking/native packaging;
- tests;
- resource processing;
- lint/static analysis;
- release signing/packaging;
- broad target matrix;
- remote/cache misses.

When an installed official platform skill exists for the exact build problem — for example Kotlin
Native build performance — prefer it for current platform facts and use this skill for measurement
and release-safety discipline.

## 8. Benchmark quality

Avoid misleading measurements:

- runtime/JIT warmup mismatch;
- debug vs release mismatch;
- cold vs warm cache mismatch;
- tiny synthetic inputs unrelated to production;
- network/environment noise;
- benchmark code that optimizes away the work;
- comparing behavior that no longer performs the same job;
- one lucky timing sample presented without variance/context.

Use the project's native benchmark/profiling ecosystem where possible.

## 9. Secondary-cost review

A faster result can still be worse. Inspect tradeoffs such as:

- latency vs memory;
- throughput vs tail latency;
- startup vs steady state;
- developer-loop speed vs CI/release completeness;
- cache speed vs staleness/storage;
- concurrency vs downstream load;
- code complexity vs a microsecond-level gain.

## 10. Verification

After the change:

- rerun the exact comparable baseline workload;
- report before/after values and relevant variance/state;
- run correctness/regression tests;
- verify required release/production behavior is unchanged;
- inspect secondary costs;
- distinguish measured fact from inference.

Do not report “much faster”, “optimized”, or a percentage based on incomparable runs.

If reliable measurement is unavailable, mark the performance claim `UNVERIFIED`.
