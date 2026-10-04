---
name: backend-architecture
description: >-
  This skill should be used for consequential backend architecture decisions:
  module or service boundaries; modular monoliths versus independent services;
  service extraction and data migration; data ownership and consistency;
  synchronous, event-driven, actor/stateful, or pipeline designs; failure
  isolation, backpressure, deployment topology; or deciding where orchestration
  and invariants belong. Trigger on requests to review or design a backend,
  split a service, choose a queue or communication shape, or restructure a
  backend that is difficult to change. Not for routine implementation, syntax
  questions, isolated bug fixes, or generic code review.
---

# Backend Architecture

Start from the system that exists, not from an architecture diagram you already
want to impose.

## Investigate before choosing

Inspect entry points, module boundaries, data stores, call paths, deployment
units, tests, and recent changes. Where available, inspect runtime signals,
incident and deployment history, data growth, and ownership or regulatory
constraints. Identify the constraint driving the decision:
independent deployment, failure isolation, data ownership, latency, throughput,
team ownership, regulatory separation, or simply code that is hard to change.

Separate evidence from assumptions and perform a blind-spot pass before
converging. Research what the repository, telemetry, and primary documentation
can answer; prioritize remaining user questions by how likely their answers are
to change the architecture. Do not use remembered version trivia as evidence.

## Production opinions

- **Default to a modular monolith.** A process boundary must earn its network,
  operational, consistency, and observability costs. Split a service when the
  system needs independent deployment, failure isolation, scaling, ownership,
  or a genuinely separate data lifecycle--not to make the folder tree look
  cleaner.
- **Draw boundaries around change and ownership.** Code that changes together
  should usually live together. A service owns its writes and invariants; shared
  tables and cross-service transactions are evidence the boundary is wrong.
- **Keep delivery mechanisms thin.** HTTP handlers, message consumers, jobs,
  CLIs, and real-time hubs translate and delegate. They should not become the
  only place where business rules are enforced.
- **Put invariants near the state they protect.** Use application services for
  orchestration and transaction boundaries. Use domain types when they prevent
  illegal states. Do not add layers, repositories, interfaces, or value objects
  that protect no real seam or invariant.
- **Prefer synchronous flows until asynchronous behavior is required, unless
  the workload is inherently ingest-, stream-, or fan-in-shaped.** Events and
  queues are justified by decoupled lifecycles, buffering, fan-out, or
  resilience requirements.
- **Name one authority for each invariant and published contract.** Validate at
  every trust boundary; derive mechanical validators and types from versioned
  contracts where useful. Avoid shared runtime packages that compromise
  independent service release autonomy.
- **Architecture includes operations.** Account for cancellation, backpressure,
  graceful shutdown, readiness, migrations, telemetry, failure recovery, and
  bounded resource use. A clean dependency graph that fails badly in production
  is not a good architecture.

## Use judgment

Do not reward ceremony. A small CRUD service may need a framework-native data
layer and little else. A complex workflow may justify explicit application and
domain boundaries. Preserve a coherent existing architecture unless changing
it solves a demonstrated problem.

Load `references/production-shapes.md` when changing process or deployment
boundaries, extracting a service, migrating data, introducing events or a
broker, designing long-lived concurrent state, building a staged pipeline, or
comparing candidate shapes. Use it to compare failure models and operational
costs, not to label every codebase with a pattern.

Present the recommendation with the evidence that supports it, the important
tradeoffs, and the unknowns that could reverse it. Prefer a reversible next
step--a module boundary, contract test, measurement, or small extraction--over
a speculative rewrite. State how the team can verify that the decision improved
the system with a contract test at the seam and a before/after measurement of
the constraint that motivated the change.
