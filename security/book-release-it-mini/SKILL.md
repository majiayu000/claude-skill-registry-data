---
name: book--release-it--mini
description: >-
  Release It! (Michael Nygard) — Condensed rules — key principles distilled. Use when asked to apply Release It! principles or review code against Release It! standards.
origin: "github.com/ciembor/agent-rules-books (MIT)"
license: MIT
version: "1.0.0"
compatibility: "yana-ai >= 0.14.0"
---

# OBEY Release It! by Michael T. Nygard

## When to use

Use for services, APIs, jobs, queues, deployment paths, control tooling, and critical flows that must survive production failures, overload, latency, bad data, hostile traffic, and operational mistakes.

## Primary bias to correct

A passing happy path is not production readiness. Design the failure semantics, demand limits, isolation, recovery path, and diagnosis surface before production defines them for you.

## Decision rules

- Assume every dependency, queue, cache, timeout, caller retry, and degraded state can fail in slow, partial, or prolonged ways; code must assume production mess instead of merely tolerating it by accident.
- Prefer designs that fail visibly, limit blast radius, shed load, preserve core service, and make diagnosis possible over designs that maximize coupling or ideal-path elegance.
- Treat deployment, operations, security, observability, rollback, build and runtime state, dependency state, and configuration validation as part of the system, not after-release chores.
- Put explicit, intentional time limits on outbound calls and waits. Do not rely on library defaults or allow infinite waits where finite response matters.
- Retry only when the operation is safe for the caller and provider; bound count and total time, use backoff or jitter, and do not retry validation errors or permanent failures.
- Isolate dependency and workload failures with circuit breakers, fast failure, bulkheads, separate resource pools, and slow-work isolation so one outage cannot consume all threads, connections, or workers.
- Design overload behavior explicitly with back pressure, finite queues, demand limits, capacity reserved for critical traffic, and load shedding of lower-value work before core functions collapse.
- Use stability patterns by failure mode: steady state for routine cleanup and bounded growth, fail fast when continuing hides unrecoverable trouble or holds scarce resources, let-it-crash only with supervision and isolation, handshaking for readiness, decoupling middleware with monitoring, and governors for expensive behavior.
- Make runtime state, external responses, automation progress, migrations, operational assumptions, and boundary data visible and validated before trusted; keep rollback or roll-forward paths for partial operational changes.
- Budget scarce resources explicitly, release them deterministically, avoid holding locks or expensive connections across slow remote calls, and stream or paginate large payloads instead of defaulting to huge in-memory batches.
- Treat external input and external responses as untrusted: validate syntax, shape, business plausibility, status, content type, and semantics; prevent malformed data from poisoning caches, queues, or downstream systems.
- Build observability into boundaries and failure points with structured context, correlation identifiers, latency, throughput, error, saturation, queue, retry, breaker, dependency, version, configuration, health, and runtime signals while avoiding secrets and retry-storm log spam.
- Make startup, health checks, migrations, one-time jobs, administrative controls, process code, and delivery tooling fail safely, auditable, authorized, observable, stoppable, and recoverable.
- Make interconnects, routing, API contracts, caches, scheduled work, and background work production-aware: avoid concentrated demand, hidden single points of failure, uncontrolled fan-out, fragile chattiness, cache dogpiles, stale data surprises, and synchronized job retries.
- Include security and hostile traffic in production readiness, and use production tests, launch checks, capacity tests, game days, chaos, or disaster simulations only with limited blast radius, observability, stop conditions, and feedback into design.

## Trigger rules

- When adding an outbound call, dependency operation, resource checkout, queue consume, or thread wait, define timeout, retry eligibility, retry bounds, fallback or degraded mode, validation, and caller-survival behavior.
- When adding a queue, buffer, resource pool, cache, log stream, background job, scheduled job, or collection-returning API, define capacity, full behavior, cleanup, miss/stampede/staleness behavior, pacing, pagination or streaming, and saturation monitoring.
- When a change touches deployment, configuration, startup, migrations, one-time jobs, scripts, or operational automation, make it idempotent or restartable where practical and give it durable state, auditability, verification, and rollback or roll-forward.
- When adding health checks, load balancing, service discovery, routing, or inter-service handshakes, ensure traffic reaches only ready components and health signals reflect real ability to serve.
- When designing API or integration contracts, make material failure modes explicit, distinguish retryable from non-retryable outcomes, prefer coarse-grained resilient interactions, and document timeout, retry, version, and compatibility expectations.
- When reviewing an incident, performance failure, or capacity issue, identify the failure chain, missing defenses, detection gaps, demand, saturation, latency distribution, queue age, dependency behavior, traffic concentration, and design changes.
- When adding administrative controls, control planes, delivery tooling, hostile-traffic handling, or chaos/disaster work, require authorization, auditability, safe defaults, clear stop mechanisms, bounded blast radius, and recovery paths.

## Final checklist

- Explicit timeouts and no infinite waits?
- Retries safe, bounded, backed off or jittered, and not duplicated across layers?
- Queues, buffers, pools, caches, logs, payloads, jobs, and result sets bounded?
- Failure isolated with breakers, bulkheads, fast failure, degradation, or load shedding?
- External input and dependency responses validated before they affect state, caches, queues, or downstream systems?
- Diagnostics cover logs, metrics, health, correlation, runtime, version, configuration, dependencies, saturation, queue depth, retries, and breaker state?
- Startup, deployment, migration, automation, and operational controls restartable, observable, authorized, auditable, and recoverable where practical?
- Interconnects, APIs, caches, scheduled work, security, and chaos tests have explicit production failure behavior?
