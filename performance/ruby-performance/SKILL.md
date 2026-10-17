---
name: ruby-performance
description: Use when diagnosing or changing Ruby/Rails performance, latency, throughput, allocations, memory usage, database/query cost, caching, profiling, benchmarking, or runtime optimization.
license: MIT
---

# Ruby Performance Engineering

## Purpose

Treat performance as an evidence-driven engineering problem, not a code-style preference.

Core loop:

~~~text
define workload
-> establish baseline
-> measure
-> identify bottleneck
-> form hypothesis
-> make smallest targeted change
-> measure again
-> verify behavior
-> document trade-off
~~~

Rails documentation covers performance testing and caching; current Rails caching guidance includes fragment, low-level, SQL, cache-key, conditional-GET, and Solid Cache concepts.
Sources:
- https://guides.rubyonrails.org/caching_with_rails.html
- https://guides.rubyonrails.org/performance_testing.html

## Activate when

- a user reports a slow endpoint, job, command, query, or test suite
- latency, throughput, CPU, memory, allocations, or GC are relevant
- optimizing Ruby code
- introducing or changing caching
- changing Active Record query shape for performance
- investigating N+1 queries
- investigating boot/load cost
- evaluating YJIT/runtime settings
- adding benchmarks or performance regression tests
- interpreting profiler output
- reviewing a performance-sensitive change

Do not activate merely because code contains loops or because someone has a generic "optimize this" preference.

## Repository inspection

Inspect Ruby/Rails versions, runtime/JIT configuration, production process model, worker counts, database adapter and pool, query logs/observability, cache configuration, job runtime, existing benchmarks, profiler configuration, representative data volume, CI performance checks, and repository performance conventions.

A benchmark with unrealistic workload or data is not production performance evidence.

## Performance dimensions

Separate latency, throughput, CPU time, wall-clock time, allocations, retained memory, GC time/count, database time, network time, lock/contention time, and boot/load time.

Do not optimize one dimension while silently regressing another.

## Measurement discipline

Establish a baseline for performance-motivated changes.

Record workload, input/data size, environment, Ruby/Rails version, warmup/iterations, runtime flags, database/cache state, metric, baseline result, and changed result.

Avoid interpreting one noisy timing as a meaningful improvement.

## Benchmarking

Use the smallest appropriate tool.

Ruby includes the Benchmark standard library. Minitest also supports optional benchmark assertions.

For repeated microbenchmarks, use benchmark-ips when already present or explicitly introduced.

A benchmark must answer a concrete question. Do not add benchmarks that merely produce numbers without a decision criterion.

## Profiling

Choose the profiler based on the question:

- sampling: identify hot call paths with lower instrumentation overhead
- instrumentation: detailed call relationships
- allocation/memory profiling: object creation or retained memory
- event/request profiling: expensive application events
- database instrumentation: query count/time rather than Ruby CPU

StackProf is a sampling profiler. Use the installed version and CLI as the compatibility authority:
https://github.com/tmm1/stackprof

ruby-prof provides detailed Ruby call profiling and multiple printers:
https://github.com/ruby-prof/ruby-prof

Do not profile production blindly. Prefer controlled reproduction or an explicitly bounded production profiling procedure.

## Reading profiles

Distinguish self time from inclusive/total time.

A high-level framework method is not automatically the root cause. Follow the call path until the application-owned expensive operation is identified.

## Database performance

When Active Record is involved, inspect query count, duration, N+1 behavior, eager loading/preloading, selected columns, object materialization, pagination, indexes, predicates, sorting/grouping, transaction scope, lock contention, and connection-pool saturation.

Do not solve every database performance problem with eager loading. Measure query shape and returned data first.

## Allocation and GC

Use allocation/GC evidence before changing allocation patterns.

Ruby exposes GC statistics through GC.stat and profiling through GC::Profiler. These are CRuby implementation-sensitive facilities.

Ask:

- Are allocations unexpectedly high?
- Are temporary objects dominating a hot path?
- Is GC time significant?
- Did the optimization actually reduce useful work?

Avoid obscure mutable code without measured benefit.

## Caching

Caching is a performance strategy with correctness consequences.

Before adding a cache define:

- cache key
- ownership
- freshness requirement
- invalidation strategy
- namespace/versioning
- stampede behavior
- memory/storage cost
- serialization cost
- failure behavior
- multi-process/distributed behavior

Never add caching without answering: "When can this value be stale?"

Prefer stable, versioned cache keys with all required tenant/user/resource identity.

## Rails request performance

For a slow request decompose:

~~~text
network
-> Rack/middleware
-> controller
-> authorization
-> database
-> domain/service work
-> rendering/serialization
-> response
~~~

Measure before moving work between layers.

## Background jobs

Inspect batch size, query pattern, serialization, external API latency, retries, concurrency, DB connection use, memory growth, and idempotency.

Increasing worker concurrency is not automatically a performance fix; verify downstream capacity first.

## Concurrency interaction

Coordinate with ruby-concurrency.

Before increasing threads/workers consider database pool size, external limits, CPU, memory, queue depth, lock contention, and rate limits.

## YJIT/runtime optimization

Check the application's Ruby version and deployment support before recommending YJIT.

Ruby documentation includes YJIT configuration, performance tips, memory considerations, and profiling guidance:
https://ruby-doc.org/3.3.7/table_of_contents.html

Treat JIT configuration as a workload/runtime decision, not a universal switch.

## Performance regression tests

A useful regression test has a stable workload, explicit metric, meaningful threshold/comparison, controlled environment, enough warmup/iterations, and a documented reason for the threshold.

Do not make CI flaky with tight wall-clock thresholds.

Prefer structural performance contracts when timing is unstable: query count, external-call count, stable allocation bounds, algorithmic complexity, or cache behavior.

## Safe optimization procedure

~~~text
reproduce
-> benchmark/profile
-> identify dominant cost
-> formulate hypothesis
-> make smallest change
-> run functional tests
-> rerun measurement
-> compare dimensions
-> simplify
-> keep only evidence-backed optimization
~~~

## Anti-patterns

- optimizing without a baseline
- unrealistic microbenchmarks
- one timing sample as proof
- speculative micro-optimization
- caching without invalidation semantics
- adding indexes without query evidence
- eager-loading every association
- increasing workers without capacity analysis
- confusing CPU time with wall-clock latency
- ignoring allocations/GC
- profiling unrepresentative traffic
- unstable timing thresholds in CI
- optimizing a non-dominant operation

## Reference example

Measure before optimizing: allocation counts and wall time make the difference between two candidate implementations observable.

```ruby
require "benchmark"

def concat_naive(n)
  s = ""
  n.times { s = s + "x" }   # allocates a new String per iteration
  s
end

def concat_mutating(n)
  s = +""
  n.times { s << "x" }      # single buffer, mutated in place
  s
end

n = 2_000
Benchmark.bm(16) do |x|
  x.report("naive (+)")     { concat_naive(n) }
  x.report("in-place (<<)") { concat_mutating(n) }
end

allocs = GC.stat(:total_allocated_objects)
concat_mutating(n)
delta = GC.stat(:total_allocated_objects) - allocs
puts "mutating version allocated #{delta} objects for #{n} appends"
```

## Agent review checklist

- [ ] workload defined
- [ ] baseline measured
- [ ] relevant metric identified
- [ ] runtime/version inspected
- [ ] representative data considered
- [ ] bottleneck evidence identified
- [ ] hypothesis stated
- [ ] smallest targeted change made
- [ ] functional tests pass
- [ ] performance re-measured
- [ ] other dimensions considered
- [ ] cache correctness considered when applicable
- [ ] DB/pool capacity considered when applicable
- [ ] concurrency capacity considered when applicable
- [ ] final diff simplified

## Verification

Report evidence:

~~~text
baseline: ...
after: ...
workload: ...
metric: ...
environment: ...
trade-off: ...
~~~

Never claim "faster", "more efficient", "lower memory", or "scales better" without measurement or a demonstrated structural property.

## Source foundation

- Ruby: https://ruby-doc.org/
- Rails caching: https://guides.rubyonrails.org/caching_with_rails.html
- Rails performance testing: https://guides.rubyonrails.org/performance_testing.html
- StackProf: https://github.com/tmm1/stackprof
- ruby-prof: https://github.com/ruby-prof/ruby-prof

## Performance-sensitive changes

For performance work:
- establish a workload and baseline before optimizing when practical;
- distinguish latency, throughput, CPU, allocations, GC, database, network, and contention costs;
- use profiling/benchmarking only to answer a concrete question;
- never claim a performance improvement without measurement or a demonstrated structural property;
- do not introduce caching without explicit freshness and invalidation semantics;
- do not increase concurrency without downstream capacity analysis;
- keep performance thresholds stable enough for CI.
