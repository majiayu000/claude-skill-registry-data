---
name: rails-reliability-engineering
description: Use when Rails/Ruby systems need explicit reliability objectives, failure containment, graceful degradation, dependency isolation, load shedding, recovery planning, or resilience testing.
license: MIT
---

# Reliability Engineering & Resilience

## Purpose

Treat reliability as an engineered system property with explicit objectives, failure budgets, containment boundaries, recovery procedures, and evidence.

A reliable system does not merely retry failures. It limits blast radius, preserves critical behavior under dependency failure, sheds unsafe load, recovers predictably, and exposes whether reliability objectives are being met.

Core flow:

define critical user journeys
-> define SLIs
-> set SLOs and error budgets
-> map dependencies/failure modes
-> choose containment/degradation
-> bound retries/concurrency
-> define recovery objectives
-> observe budget/saturation/failure
-> test failure and recovery
-> review operational evidence
-> evolve the design

Compose this skill with:

- rails-observability for telemetry, health, correlation, and error reporting;
- rails-performance for workload/capacity evidence;
- rails-api-integration for dependency timeout/retry/compatibility;
- rails-distributed-systems for cross-service failure and consistency;
- rails-event-driven-messaging for broker/consumer failure and lag;
- rails-production-runtime for process lifecycle, restart, and deployment;
- rails-active-job for retry/queue semantics;
- ruby-concurrency for bounded workers and isolation;
- rails-database-engineering for transaction, lock, replica, and backup/recovery concerns;
- rails-security for failure-mode abuse and trust boundaries.

## Activate when

- defining or reviewing SLI/SLO/error-budget contracts;
- diagnosing recurring availability/latency/reliability failures;
- adding circuit breakers or dependency failure isolation;
- designing graceful degradation or stale/fallback behavior;
- introducing bulkheads or isolated worker/resource pools;
- adding load shedding/admission control;
- planning retries across multiple layers;
- reviewing cascading failure or retry storms;
- defining RTO/RPO and recovery procedures;
- reviewing backups, restore, failover, or reconciliation;
- introducing resilience tests, fault injection, or game days;
- reviewing dependency criticality or blast radius;
- operating systems where overload is as dangerous as component failure.

Do not activate merely because a system has a production bug. Use the narrowest reliability capability justified by the failure mode.

## Repository inspection

Inspect:

1. critical user journeys and business priority;
2. existing SLIs, SLOs, dashboards, alerts, and incident history;
3. request/job/message latency and saturation metrics;
4. dependency inventory and failure behavior;
5. HTTP timeout/retry/circuit conventions;
6. queue/broker retry, dead-letter, and lag behavior;
7. database pool, replica, lock, transaction, and failover behavior;
8. Puma/worker/process topology and resource limits;
9. cache/fallback/stale-data behavior;
10. feature flags and kill-switch conventions;
11. backup/restore/failover/reconciliation procedures;
12. deployment and rollback mechanics;
13. existing resilience/fault-injection tests;
14. operational runbooks and ownership.

Do not invent an SLO, breaker threshold, timeout, or recovery target without workload/business evidence or an explicit contract.

## Decision rules

1. Start from the critical user journey and its reliability objective, not from a technical metric.
2. Classify the change: objectives, error budgets, and dependency criticality; failure isolation (circuit breakers, bulkheads, load shedding, degradation, retry/timeout coordination); recovery objectives and disaster recovery; or resilience testing, observability, and rollout safety.
3. Load the matching reference below before changing behavior; any new retry, timeout, or breaker needs the failure-isolation reference.

## Critical invariants

- Do not treat every technical metric as an SLO.
- Retries can amplify an incident.
- Backups are only useful when restore is tested.

## References

Load only the reference for the boundary being changed, before changing behavior there. Each reference is self-contained and one level deep; none links to another. Consult a listed pattern from the pattern catalog only when the change needs its implementation shape.

| Load when | Reference | Covers | Patterns |
|---|---|---|---|
| a change defines or alters SLIs/SLOs, error budget policy, or dependency criticality | [references/objectives-and-budgets.md](references/objectives-and-budgets.md) | Reliability objectives; Error budgets and operational decisions; Dependency criticality | `slo-error-budget` |
| a change adds or alters circuit breakers, bulkheads, admission control, degraded modes, retries, or timeouts | [references/failure-isolation.md](references/failure-isolation.md) | Circuit breakers; Bulkheads; Load shedding and admission control; Graceful degradation; Retry and timeout coordination; Cascading failure analysis | `circuit-breaker`, `bulkhead-isolation`, `load-shedding`, `graceful-degradation` |
| a change alters RTO/RPO, backups and restore, failover, or post-incident reconciliation | [references/recovery.md](references/recovery.md) | Recovery objectives; Disaster recovery and reconciliation | none |
| adding resilience tests or fault injection, reliability telemetry, or rollout guards | [references/testing-observability-rollout.md](references/testing-observability-rollout.md) | Resilience testing; Observability; Change and rollout safety | none |

## Reference example

A circuit breaker guarding a flaky dependency: failures trip it, the cooldown half-opens it, one success closes it again.

```ruby
class CircuitBreaker
  class OpenError < StandardError; end

  def initialize(failsafe:, threshold: 2, cooldown: 5, clock: Time)
    @failsafe = failsafe
    @threshold = threshold
    @cooldown = cooldown
    @clock = clock
    @failures = 0
    @opened_at = nil
  end

  def call
    raise OpenError, "circuit open" if open? && !half_open_window?

    begin
      result = @failsafe.call
      @failures = 0
      @opened_at = nil
      result
    rescue StandardError
      @failures += 1
      @opened_at = @clock.now if @failures >= @threshold
      raise
    end
  end

  private

  def open? = !@opened_at.nil?
  def half_open_window? = @clock.now >= @opened_at + @cooldown
end

attempts = 0
breaker = CircuitBreaker.new(
  failsafe: -> { attempts += 1; raise "provider 500" },
  clock: (now = Time.utc(2026, 1, 1); Struct.new(:now).new(now))
)

2.times { begin; breaker.call; rescue StandardError; end }
begin
  breaker.call
  raise "should still be open"
rescue CircuitBreaker::OpenError => e
  puts "tripped after 2 failures: #{e.message}"
end
puts "failures counted: #{attempts} (third call never reached the provider)"
```

## Agent review checklist

- [ ] critical user journey identified
- [ ] SLI measures user-visible impact
- [ ] SLO window/target explicit
- [ ] error budget semantics explicit
- [ ] dependency criticality classified
- [ ] timeout/retry budget coordinated
- [ ] circuit-breaker conditions justified
- [ ] bulkhead boundary tied to a shared resource
- [ ] load-shed policy protects critical work
- [ ] degradation fallback preserves correctness/security
- [ ] RTO/RPO explicit where recovery matters
- [ ] restore/failover/reconciliation tested
- [ ] resilience test has fault, expected containment, recovery, and verification
- [ ] capacity/saturation evidence exists
- [ ] alerts map to actionable user/system impact
- [ ] rollback/disable path exists for resilience controls
- [ ] old/new deployment compatibility considered

## Anti-patterns

- arbitrary 99.99% SLO without user/business evidence;
- treating every metric as an SLI;
- retrying every exception;
- stacking retries independently at every layer;
- circuit breaker on validation failures;
- one global breaker for unrelated failure domains;
- bulkheads that fragment capacity without justification;
- unbounded queues used as a substitute for capacity;
- load shedding without priority semantics;
- silent dropping of durable business work;
- fallback data that violates correctness/security requirements;
- backups without restore tests;
- declaring DR complete because a process boots;
- destructive chaos experiments without a bounded contract;
- alerts that page on noise while missing saturation or user impact.

## Verification

For reliability design verify:

`objective -> failure model -> control -> user behavior -> recovery -> evidence`

For a dependency:

`timeout -> retry -> breaker -> fallback/degradation -> recovery`

For overload:

`arrival -> capacity -> admission -> protected work -> recovery`

For disaster recovery:

`failure -> restore/failover -> reconcile -> validate -> user journey`

Report the reliability objective, failure mode, containment control, degradation semantics, recovery target, test evidence, and remaining assumptions.

## Source foundation

- Rails Error Reporting: https://guides.rubyonrails.org/error_reporting.html
- Rails Active Support Instrumentation: https://guides.rubyonrails.org/active_support_instrumentation.html
- Rails Active Job: https://guides.rubyonrails.org/active_job_basics.html
- Rails Testing: https://guides.rubyonrails.org/testing.html
- Repository skills: rails-observability, rails-performance, rails-api-integration, rails-distributed-systems, rails-event-driven-messaging, rails-production-runtime, rails-active-job, ruby-concurrency

## Reliability engineering changes

For reliability, resilience, overload, or recovery work:
- identify the critical user journey before choosing infrastructure metrics;
- define user-visible SLIs, an evidence-based SLO/window, and the resulting error budget;
- classify dependencies as critical, degradable, optional, or asynchronous;
- bound timeout/retry/concurrency budgets across every layer instead of stacking independent retries;
- use circuit breakers only for justified dependency failure domains and exclude deterministic caller errors from health signals;
- use bulkheads to isolate genuinely shared resources and verify capacity fragmentation does not create a new bottleneck;
- define load-shed priorities and never silently discard durable business work;
- make graceful degradation explicit, including freshness, correctness, authorization, and recovery semantics;
- define RTO/RPO and verify restore, failover, reconciliation, and post-recovery invariants where recovery matters;
- resilience-test failure containment and recovery with deterministic, bounded fault injection;
- make reliability controls observable, reversible, and compatible with rolling deployment;
- report measured evidence and remaining assumptions instead of claiming resilience from structural patterns alone.
