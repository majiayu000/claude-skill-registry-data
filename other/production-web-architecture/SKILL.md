---
name: production-web-architecture
description: Design, review, or harden a startup web platform for scalability, reliability, security, observability, deployability, data integrity, background work, caching, AI cost control, and staged growth without premature microservices.
---

# Production Web Architecture

Turn product flows into an operable system. Prefer the smallest architecture that removes the largest demonstrated risk.

## Workflow

1. Map users, critical journeys, trust boundaries, data ownership, external services, files, asynchronous work, and failure consequences.
2. State workload assumptions and service objectives: traffic shape, latency, availability, durability, freshness, privacy, and cost.
3. Trace each critical path from browser through API, storage, queue, worker, and response. Mark transaction and idempotency boundaries.
4. Review scalability, reliability, security, data integrity, performance, observability, deployment, and cost.
5. Keep a modular monolith until independent scaling, ownership, deployment, or fault isolation creates a measurable extraction benefit.
6. Move slow or fragile work behind durable queues. Make handlers idempotent, retryable, observable, and visible to users.
7. Add caches only with ownership, key design, TTL, invalidation, stampede protection, and stale behavior defined.
8. Define migrations, rollout, rollback, health checks, alerts, runbooks, and cost guardrails before calling the design production-ready.
9. Validate the highest-risk flow with a failure test, load test, or end-to-end smoke test proportional to the risk.

## Startup Defaults

- Managed relational database, object storage, queue, cache, and observability before custom distributed systems.
- Server-side authorization at every ownership boundary.
- Timeouts, pagination, rate limits, and idempotency keys on relevant APIs.
- Structured logs, trace or request IDs, service metrics, and actionable alerts.
- AI calls use structured output, provider routing, token ceilings, prompt versions, and bounded retries.
- Public reads degrade gracefully; writes fail explicitly rather than silently losing data.

## Delivery Contract

Provide:

1. **System map** - components, data, trust boundaries, and critical paths.
2. **Assumptions and SLOs** - explicit numbers or identified unknowns.
3. **Findings** - severity, evidence, failure mode, and affected journey.
4. **Target architecture** - smallest justified change and deferred complexity.
5. **Execution plan** - schema, API, queue, migration, rollout, and ownership tasks.
6. **Verification and operations** - tests, dashboards, alerts, rollback, and cost controls.

## Reference

Read [references/architecture-checklist.md](references/architecture-checklist.md) for a production review or extraction decision.
