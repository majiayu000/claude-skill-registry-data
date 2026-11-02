---
name: skill-broker-load-shedding
description: "Protects a skill broker from overload while preserving clear errors and bounded retries. Use when many agents can query the same registry or generation pipeline."
---

# Skill Broker Load Shedding

## Purpose

Maintain predictable response and cost behavior when request volume, large results, indexing jobs, or agent retries exceed capacity.

## Required inputs

Request traffic profile, service objectives, search/fetch cost estimates, queue limits, retry behavior, and available degraded modes.

## Workflow

1. Profile request classes separately: metadata search, semantic search, content fetch, index rebuild, gap submission, and candidate generation.
2. Set concurrency, queue, payload size, and deadline budgets per class; reserve capacity for small reads and health checks.
3. Define overload responses with retry guidance and distinguish capacity rejection from no-match or service failure.
4. Ensure clients use bounded exponential backoff with jitter and do not retry request classes intentionally shed by the server.
5. Load-test bursts, slow storage, oversized requests, and recovery after traffic drops; inspect queue drain time and error distribution.

## Validation checklist

- [ ] Search/fetch remain within defined resource limits during overload.
- [ ] Expensive generation jobs cannot starve basic retrieval indefinitely.
- [ ] Retry responses include safe guidance or an explicit no-retry status.
- [ ] Queue depth and load-shedding events are observable without sensitive payloads.
- [ ] The service recovers without duplicate proposal creation or unbounded retry storms.

## Required output

A load-shedding policy, client retry guidance, stress-test matrix, and observed saturation report.

## Boundaries and failure handling

Do not scale costs without a defined budget or skip access checks as a performance shortcut. Under pressure, fail predictably rather than serving unauthenticated content.

If required evidence is missing, record the gap and stop before irreversible actions. Do not claim a test, network request, compatibility result, or approval occurred unless its evidence was observed.

## Trigger examples

- **Positive:** Multiple agents issue bursts of lookups after a shared task planner starts.
- **Negative:** The catalog is local to one process and has no meaningful concurrent load.
