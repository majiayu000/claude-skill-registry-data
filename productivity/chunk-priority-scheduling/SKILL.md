---
name: chunk-priority-scheduling
description: Design and audit chunk-work prioritization using distance, visibility, player intent, deadlines, and starvation prevention.
---

# Chunk Priority Scheduling

## Goal

Keep the world responsive by scheduling generation, meshing, collision and upload work according to observable player value and resource limits.

## Inputs to inspect

Chunk job queues, priority formula, camera/player trajectory, job stages, worker capacity and completion traces.

## Workflow

1. Separate work classes such as generation, meshing, collision, upload and persistence; record which stages are prerequisites for visible or interactive readiness.
2. Define a priority score from distance, view relevance, player movement, urgency and job age, documenting units and tie-breaking.
3. Test camera turns, rapid travel, multiple players if applicable, repeated requests and a sustained background backlog for starvation and queue churn.
4. Measure queue age and completion time per work class while enforcing CPU, memory and GPU-upload budgets.
5. Add aging/priority inheritance or cancellation/coalescing only where tests show starvation or wasted work; preserve deterministic debug traces.

## Validation checklist

- [ ] Urgent nearby work becomes ready without starving required distant or maintenance tasks indefinitely.
- [ ] Repeated priority changes do not repeatedly restart expensive work without a policy reason.
- [ ] Cancelled/stale jobs release capacity and cannot publish results after their chunk revision changes.
- [ ] Metrics distinguish waiting, execution and upload latency.

## Required output

A priority policy, queue-age distribution, starvation/churn findings and stress-test scenario for chunk scheduling.

## Boundaries and failure handling

Do not rank every job only by distance; persistence, collision readiness and cleanup may have different urgency and safety requirements.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
