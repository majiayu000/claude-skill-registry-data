---
name: thalarch-architecture
description: >
  Evidence-driven software architecture design and review. Use for module/service boundaries,
  dependency direction, monolith vs distributed decomposition, system design, scalability,
  platform/data decisions, ADRs, architecture refactors, or cross-cutting changes where tradeoffs
  and quality attributes matter more than local code style.
---

# Thalarch Architecture

Architecture is a set of costly-to-change decisions and explicit tradeoffs, not a catalog of
patterns to apply by fashion.

## 1. Start from current reality

Before proposing architecture, establish from repository/runtime evidence:

- existing modules/services and ownership boundaries;
- entry points and dependency directions;
- data stores and consistency boundaries;
- deployment units and runtime topology when known;
- public/internal APIs and event/message contracts;
- build/test/release constraints;
- operational observability and failure domains;
- important historical constraints from docs/ADRs/Git when available.

For an existing project, prefer evolutionary changes over greenfield redesign unless the user
explicitly requests replacement architecture.

## 2. Quality-attribute contract

Make the forces explicit before choosing a pattern:

- correctness/consistency;
- latency/throughput;
- availability/resilience;
- security/privacy;
- scalability;
- deployability;
- operability/observability;
- testability;
- maintainability/change frequency;
- data ownership/migration cost;
- team/organizational constraints when actually known;
- cost and platform constraints.

Do not rank an architecture without saying which attributes it optimizes and what it sacrifices.

## 3. Alternatives, not foregone conclusions

For material decisions compare at least the plausible alternatives, including the simplest option.

For each alternative record:

- benefits under the stated workload/constraints;
- failure modes;
- coupling introduced/removed;
- data/transaction consequences;
- operational burden;
- migration/rollback cost;
- evidence/unknowns that could change the decision.

Do not recommend microservices, event sourcing, CQRS, hexagonal architecture, a new database, or a
new messaging layer merely because the system is “large”.

## 4. Dependency architecture

Build a task-focused dependency map when changing boundaries.

Look for:

- cycles;
- stable core depending on volatile infrastructure;
- feature modules reaching through multiple layers;
- shared “utils/common” packages accumulating unrelated policy;
- duplicated domain rules across services/modules;
- cross-boundary access to another component's persistence internals;
- APIs that expose implementation details;
- hidden runtime coupling through environment/config/shared databases.

A dependency analyzer is a lead generator. Confirm important cycles/coupling in the actual build
and source graph before restructuring.

## 5. Data and distributed boundaries

A service boundary is also a data/failure boundary.

Before splitting components review:

- transaction requirements;
- ownership of records and writes;
- synchronous vs asynchronous consistency;
- duplicate/out-of-order delivery;
- idempotency;
- retry/timeout budgets;
- schema/event evolution;
- backfills and migrations;
- operational recovery when one side is unavailable.

Do not claim “exactly once” or strong consistency across components without an actual mechanism
that proves it.

## 6. Architecture Decision Record

For a consequential decision, produce a compact ADR when useful:

- Context / problem;
- Decision drivers;
- Options considered;
- Decision;
- Consequences/tradeoffs;
- Migration/rollback plan;
- Evidence and remaining unknowns;
- Revisit trigger.

Do not create permanent ADR files unless the user asked or the repository already uses ADRs and
the task includes documentation.

## 7. Evolution plan

Prefer reversible increments:

1. establish/strengthen the boundary;
2. add contract/regression tests;
3. move one dependency/data flow;
4. observe behavior;
5. remove the old path only after consumers migrate.

Use strangler/adapter/compatibility stages when a big-bang rewrite would create unnecessary risk.

## 8. Architecture review

Review at the level of consequences:

- Does the change preserve intended ownership?
- Does it create a new dependency cycle?
- Has one failure domain become several without recovery behavior?
- Has local simplicity been traded for distributed complexity?
- Is configuration now architecture-by-flag?
- Is a public interface stable enough for its consumers?
- Are tests located at the new boundary?
- Can the system be rolled back or operated during partial migration?

Avoid style-level findings disguised as architecture.

## 9. Verification

Architecture cannot be fully proven by a diagram. Use the strongest available evidence:

- build/module dependency graph;
- compile boundaries;
- architecture/static tests already used by the repo;
- integration/contract tests;
- deployment/config validation;
- runtime traces/metrics for performance or failure-domain claims;
- migration rehearsal when data/contracts change.

Mark speculative capacity/operational assumptions `UNVERIFIED` when no production-like evidence
exists.
