---
name: system-architecture-translator
description: "Translate data flows, services, queues, workflows, storage, consistency, latency, failures, retries, and distributed-system constraints into visible product and UX decisions for a case study. Use for AI agents, desktop tools, data products, scraping engines, background jobs, cloud systems, or any portfolio story where architecture determines telemetry, state management, loading, recovery, permissions, or user control."
---

# System Architecture Translator

Explain how invisible system behavior shaped the interface. Read `references/system-to-ux-map.md`.

## Workflow

1. Inspect architecture diagrams, code paths, API contracts, schemas, traces, logs, incidents, and product states.
2. Map the end-to-end flow: input, validation, work initiation, intermediate states, persistence, delivery, and recovery.
3. Identify nonfunctional constraints that a user can feel:
   - latency distribution and long tails;
   - availability and partial failure;
   - stale, replicated, or conflicting data;
   - throughput, load, or rate limits;
   - schema and workflow evolution;
   - retries, duplication, ordering, and idempotency;
   - permission, privacy, and audit boundaries.
4. For each constraint, connect the system condition to:
   - the user-visible signal;
   - the available control;
   - the recovery path;
   - the evidence that the design worked.
5. Separate operational telemetry from user-facing explanation.
6. Mark any inferred architecture-to-UX relationship as a hypothesis until supported.

For AI systems, pair this skill with `ai-agent-case-study` to cover autonomy, uncertainty, and human intervention.

## Required sections

Return:

1. a system boundary and data-flow summary;
2. a System→UX translation map;
3. state, latency, and progress behavior;
4. failure, retry, rollback, and recovery behavior;
5. telemetry and audit design;
6. architectural trade-offs and unresolved evidence.

## Example

Input:

```text
Jobs fan out across three APIs. Completion ranges from 8 seconds to 4 minutes.
Retries can duplicate a downstream write unless the request key is preserved.
```

Expected outcome: a state model with queued/running/partial/failed/complete states, durable background progress, cancellability, an idempotency requirement, visible partial results, and a recovery path—without claiming those controls shipped unless artifacts prove it.
