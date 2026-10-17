---
name: rails-performance
description: Use when diagnosing, designing, reviewing, or changing Rails performance across Active Record queries, N+1 behavior, caching, request rendering, Puma capacity, connection pools, background jobs, allocations, memory, and production throughput.
license: MIT
---

# Rails Performance Engineering

## Purpose

Treat Rails performance as an evidence-driven systems problem.

The performance chain is:

workload
-> baseline
-> bottleneck evidence
-> hypothesis
-> smallest targeted change
-> functional verification
-> performance re-measurement
-> production observation

The skill complements `ruby-performance`. Use this skill for Rails-specific boundaries and use `ruby-performance` for Ruby runtime, allocation, GC, profiling, and general benchmark methodology.

## Activate when

- a Rails endpoint, job, query, render, boot, or test suite is slow
- Active Record query count, N+1 behavior, object loading, or query plans are involved
- changing eager loading, preloading, batching, pagination, or selected columns for performance
- changing a database index because of a measured query
- introducing or changing Rails fragment/low-level/SQL caching
- investigating cache hit rate, invalidation, stampede, or key construction
- changing Puma workers/threads or `WEB_CONCURRENCY` / `RAILS_MAX_THREADS`
- changing database connection pools or encountering pool exhaustion
- increasing background-job concurrency or batch size
- analyzing request throughput, queueing, memory, or downstream saturation
- adding a Rails performance regression check
- reviewing a Rails performance-sensitive change

Do not activate merely because a loop, association, or query exists. Require a workload, symptom, or explicit measurable target.

## Repository inspection

Before changing Rails performance, inspect:

1. Ruby and Rails versions;
2. Active Record adapter and database version;
3. representative data volume/cardinality;
4. existing query logs and instrumentation;
5. current request/job latency and throughput evidence;
6. existing eager-loading/query conventions;
7. schema indexes and constraints;
8. Puma workers/threads and process limits;
9. Active Job/queue adapter and worker concurrency;
10. database connection-pool configuration;
11. cache store, namespace/versioning, and expiration conventions;
12. existing benchmarks and performance tests;
13. CI performance checks;
14. deployment/container CPU and memory limits when runtime capacity changes.

Do not infer production capacity from development defaults.

## Measurement model

Separate these dimensions:

- request latency;
- queueing time;
- throughput;
- Ruby CPU time;
- wall-clock time;
- database time;
- query count;
- rows/materialized records;
- allocations/retained memory;
- GC cost;
- lock/contention time;
- cache hit/miss behavior;
- external dependency time;
- boot/load time.

Do not claim that one dimension improved when the change only moved cost to another boundary.

For a performance claim, record:

workload
+ environment
+ runtime version
+ data volume
+ metric
+ baseline
+ changed result

No baseline exists: report the absence instead of inventing one.

## Decision rules

1. Measure first: establish the baseline and the dominant cost before choosing a technique.
2. Classify the bottleneck: query path (Active Record queries, N+1, read-path design, pagination, indexes and plans), caching and stampedes, request and Puma/connection-pool capacity, or background jobs, batching, and memory.
3. Load the matching reference below, apply the smallest change, and re-measure with the same workload; add regression protection only where the repository already supports it.

## References

Load only the reference for the boundary being changed, before changing behavior there. Each reference is self-contained and one level deep; none links to another. Consult a listed pattern from the pattern catalog only when the change needs its implementation shape.

| Load when | Reference | Covers | Patterns |
|---|---|---|---|
| the bottleneck is query count, N+1 access, read-path design, data volume, or indexes and query plans | [references/query-performance.md](references/query-performance.md) | Active Record query performance; N+1 detection; Query-object and read-path design; Pagination and data volume; Indexes and query plans | `n-plus-one-review`, `query-plan-evidence`, `query-object` |
| a change adds, alters, or invalidates a cache or must control stampedes | [references/caching.md](references/caching.md) | Caching; Cache stampede | `cache-stampede-control` |
| the bottleneck is request latency, Puma threads/workers, or database connection pool capacity | [references/request-and-capacity.md](references/request-and-capacity.md) | Rails request performance; Puma and web concurrency; Connection-pool capacity | `puma-capacity`, `connection-pool-capacity` |
| the bottleneck is job throughput, batch size, memory or allocations, or a change needs performance regression tests | [references/jobs-batching-memory.md](references/jobs-batching-memory.md) | Background-job performance; Batching; Memory and allocations; Performance regression testing | `performance-investigation` |

## Performance-safe change procedure

~~~text
reproduce
-> inspect evidence
-> establish baseline
-> pin the regression (query-count fixes: a failing query-count test first)
-> identify owning boundary
-> choose smallest suitable pattern
-> implement one targeted change
-> run functional tests
-> run performance measurement
-> inspect secondary effects
-> simplify
-> report evidence
~~~

## Cross-skill coordination

Use these combinations deliberately:

- `ruby-performance`: Ruby CPU, allocations, GC, profiling, benchmark methodology;
- `rails-active-record`: query/persistence implementation;
- `rails-database-engineering`: schema, index, locking, pool/database capacity;
- `rails-active-job`: queue/retry/concurrency semantics;
- `rails-observability`: measurements and request/job telemetry;
- `ruby-concurrency`: threads, contention, race/concurrency reasoning;
- `rails-security`: tenant/auth/cache correctness;
- `rails-test-engineering`: performance regression and deterministic test design.

## Anti-patterns

- optimizing without a workload or baseline;
- adding `includes` without understanding the query shape;
- eager-loading every association;
- adding an index without query-plan evidence;
- increasing Puma threads without DB-pool analysis;
- increasing workers without memory analysis;
- increasing job concurrency without downstream capacity analysis;
- increasing DB pool size until timeout errors disappear;
- caching without freshness/invalidation semantics;
- cache keys that omit tenant/resource identity;
- solving cache stampede with distributed locks without measured contention;
- using OFFSET pagination for very large datasets without inspecting query cost;
- making timing-based CI thresholds unrealistically strict;
- benchmarking only development-sized data;
- treating one faster benchmark as proof of production scalability;
- hiding a bottleneck by moving it to another subsystem.

## Reference example

N+1 eliminated by planning loads up front, with query count asserted in the test rather than hoped for in production.

```ruby
class StatementsController < ApplicationController
  def index
    @statements = current_account.statements
      .includes(:invoice, :customer)   # one planned query, not 1 + N lazy loads
      .order(issued_on: :desc)
      .limit(50)
  end
end

# test/performance/statements_query_test.rb
#   it "renders 50 statements without N+1" do
#     create_list(:statement, 50, account: account)
#     assert_queries(2) { get statements_path } # count the SQL, not the feeling
#   end
#
# Evidence first: Bullet/sql.event trace identifies the association before includes
# is added, and the assertion keeps it from regressing.
```

## Agent review checklist

- [ ] Ruby/Rails/runtime versions inspected
- [ ] workload and symptom identified
- [ ] representative data volume considered
- [ ] bottleneck boundary identified
- [ ] baseline or structural evidence recorded
- [ ] query count/shape reviewed when Active Record is involved
- [ ] query plan reviewed when indexing/query execution is the issue
- [ ] N+1 behavior checked where associations are iterated
- [ ] cache freshness/invalidation/key semantics checked
- [ ] tenant/security identity included in cache keys when applicable
- [ ] Puma concurrency checked against DB/downstream capacity
- [ ] DB pool checked against aggregate concurrency
- [ ] job concurrency checked against DB/external capacity
- [ ] memory/allocation effects considered
- [ ] functional tests pass
- [ ] performance claim re-measured or structurally justified
- [ ] no speculative optimization remains

## Verification

Report evidence in this form:

~~~
workload: ...
environment: ...
baseline: ...
change: ...
after: ...
metric: ...
secondary_effects: ...
trade_off: ...
~~~

If timing evidence is unavailable, explicitly state the structural reason for the conclusion instead.

Never claim "scales better", "faster", "lower memory", or "higher throughput" without measurement or a demonstrated structural property.

## Source foundation

Primary Rails guidance:
- https://guides.rubyonrails.org/caching_with_rails.html
- https://guides.rubyonrails.org/active_record_querying.html
- https://guides.rubyonrails.org/performance_testing.html

Repository-specific foundations:
- `ruby-performance` skill
- `rails-active-record` skill
- `rails-database-engineering` skill
- `rails-active-job` skill
- `cache-boundary` pattern
- `production-index` pattern
- `puma-capacity` pattern
- `connection-pool-capacity` pattern
- `n-plus-one-review` pattern
- `query-plan-evidence` pattern

## Performance-sensitive changes

For performance work:
- establish a workload and baseline before optimizing when practical;
- distinguish latency, throughput, CPU, allocations, GC, database, network, and contention costs;
- use profiling/benchmarking only to answer a concrete question;
- never claim a performance improvement without measurement or a demonstrated structural property;
- do not introduce caching without explicit freshness and invalidation semantics;
- do not increase concurrency without downstream capacity analysis;
- keep performance thresholds stable enough for CI.
