---
name: book--release-it--nano
description: >-
  Release It! (Michael Nygard) — Minimal rules — essential one-liners only. Use when asked to apply Release It! principles or review code against Release It! standards.
origin: "github.com/ciembor/agent-rules-books (MIT)"
license: MIT
version: "1.0.0"
compatibility: "yana-ai >= 0.14.0"
---

# OBEY Release It! by Michael T. Nygard

## When to use

Use when operational survivability matters and context is tight.

## Primary bias to correct

Production failure semantics, overload behavior, isolation, recovery, and diagnosis must be designed, not discovered after release.

## Decision rules

- Assume dependencies, queues, caches, callers, timeouts, bad data, and degraded states fail slowly, partially, and for longer than expected.
- Prefer visible failure, blast-radius limits, load shedding, preserved core service, and diagnosis over happy-path elegance.
- Bound outbound calls, waits, retries, queues, pools, caches, logs, result sets, payloads, and scarce resources where finite response matters.
- Retry only when safe, bounded, and backed off or jittered; never retry permanent failures or stack retries into storms.
- Isolate failure with circuit breakers, bulkheads, fast failure, separate pools, degraded modes, and deterministic cleanup.
- Treat deployment, startup, automation, health, observability, configuration, rollback, security, and runtime state as production design.
- Validate external input and responses before trusting them; prevent bad data from poisoning caches, queues, state, or downstream systems.
- Make APIs, interconnects, caches, jobs, and operational controls explicit about failure, capacity, recovery, authorization, and stop behavior.

## Trigger rules

- When adding a remote call, wait, queue, pool, cache, job, retry, or large result path, define bounds, failure behavior, validation, and saturation signals.
- When changing startup, deployment, migration, configuration, script, or control tooling, make recovery, auditability, observability, and restartability explicit.
- When traffic can concentrate through routing, scheduling, retries, fan-out, or hostile use, add back pressure, shedding, pacing, or isolation before expensive work.
- When using production tests, game days, chaos, or disaster drills, require hypothesis, blast-radius limit, observability, stop condition, and recovery path.

## Final checklist

- Bounded?
- Retry disciplined?
- Failure isolated?
- Load controlled?
- Data validated?
- Observable?
- Recoverable?
- Stoppable?
