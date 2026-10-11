---
name: apex-design-patterns
description: "Use when structuring Apex into service, selector, domain, factory, and dependency-injection layers for maintainability and testability. Triggers: 'service layer', 'selector pattern', 'domain layer', 'dependency injection', 'fat trigger/controller'. NOT for installing a specific third-party framework or debating package-level architecture outside Apex code structure."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Scalability
  - Reliability
  - Operational Excellence
tags:
  - service-layer
  - selector-pattern
  - domain-layer
  - dependency-injection
  - factory-pattern
triggers:
  - "how should I structure Apex service classes"
  - "selector layer versus querying in service"
  - "domain layer pattern in Salesforce"
  - "dependency injection for Apex tests"
  - "fat trigger or controller needs refactor"
inputs:
  - "current entry points such as trigger, controller, invocable, or REST"
  - "team size and expected codebase growth"
  - "testing pain points and dependency boundaries"
outputs:
  - "Apex layering recommendation"
  - "review findings for coupling and responsibility issues"
  - "refactor pattern for service, selector, domain, or factory layers"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-03-13
---

Use this skill when Apex code needs structure that will survive more than one sprint. The goal is not to import a framework blindly. It is to separate orchestration, querying, business rules, and replaceable dependencies so triggers, controllers, and invocables stay thin and tests can isolate behavior.

## Before Starting

- What are the main entry points today: triggers, Aura/LWC controllers, invocables, REST resources, or schedulers?
- Which dependencies are hardest to test: SOQL, callouts, or global utility classes?
- Is the current pain duplicated business rules, query sprawl, or giant god-classes?

## Core Concepts

### Service Layer Owns Orchestration

Service classes coordinate work. They should decide sequence, call selectors, invoke domain logic, and manage transaction boundaries. They should not absorb every query, validation rule, and integration detail forever. When a service becomes the only place logic can live, it turns into a god-class quickly.

### Selector Layer Centralizes Query Intent

Selectors are for query shape, field lists, and reusable retrieval patterns. They make security review, field list reuse, and query tuning easier because data access is not scattered across controllers, triggers, and utility methods. A selector is not just “any class with SOQL”; it should have a stable retrieval responsibility.

### Domain Layer Holds Object-Specific Rules

Domain logic is where object behavior and cross-field rules belong. If every trigger, flow-invocable method, and controller re-implements the same Account or Opportunity rules differently, domain logic is missing.

### Dependency Injection Creates Testable Boundaries

Apex has limited native DI ergonomics compared with other languages, but interfaces plus factories still help. The purpose is not abstraction for its own sake. It is to replace integrations, notification clients, or expensive collaborators in tests without branching on `Test.isRunningTest()`.

## Common Patterns

### Thin Entry Point To Service

**When to use:** Triggers, controllers, invocables, or REST resources are accumulating business logic.

**How it works:** Keep the entry point as an adapter only, then delegate to a service with explicit inputs.

**Why not the alternative:** Entry-point logic is hard to reuse and harder to review across many contexts.

### Service + Selector Pair

**When to use:** A business workflow reads complex record sets repeatedly.

**How it works:** Put orchestration in the service and field/query definitions in a selector.

### Interface + Factory For External Dependencies

**When to use:** A service depends on a notifier, API client, or expensive collaborator.

**How it works:** Define an interface, provide a production implementation, and use a factory or constructor injection for tests.

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Trigger or controller contains queries, branching, and DML directly | Thin adapter + service layer | Cleaner review and reuse boundary |
| Same query field list appears in several classes | Selector layer | One place to tune and secure data access |
| Object-specific business rules repeat across entry points | Domain layer | Keeps behavior tied to the object’s business rules |
| Tests rely on `Test.isRunningTest()` to skip dependencies | Interface + injected dependency | Better isolation without production branching |


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Core Concepts and Common Patterns sections above
4. Validate — run the skill's checker script and verify against the Review Checklist below
5. Document — record any deviations from standard patterns and update the template if needed

---

## Review Checklist

- [ ] Entry points are adapters, not business-logic containers.
- [ ] Query logic is centralized where reuse or tuning matters.
- [ ] Object-specific rules are not duplicated across multiple services or triggers.
- [ ] Services do not absorb unrelated responsibilities forever.
- [ ] Test seams use interfaces/factories instead of `Test.isRunningTest()` hacks.
- [ ] Pattern usage is proportionate to the codebase size; abstraction is justified.

## Salesforce-Specific Gotchas

1. **A “service layer” can become a dumping ground fast** — if every concern lands there, the pattern has failed.
2. **Selector patterns still need secure query behavior** — centralization does not replace sharing or CRUD/FLS review.
3. **Static helpers are not dependency injection** — they are harder to stub and usually push teams toward test-only branching.
4. **Patterns are not free** — for a tiny one-off class, excessive layering can be ceremony without payoff.

## Output Artifacts

| Artifact | Description |
|---|---|
| Layering review | Findings on where orchestration, queries, and business rules are misplaced |
| Refactor map | Recommendation for service, selector, domain, factory, and interface boundaries |
| Pattern scaffold | Minimal Apex structure showing how to separate responsibilities cleanly |

## Related Skills

- `apex/trigger-framework` — use when the immediate problem starts at the trigger boundary and needs handler structure first.
- `apex/test-class-standards` — use when better layering is mainly valuable because tests are currently brittle.
- `apex/apex-security-patterns` — use when selectors and services need explicit security posture, not just better structure.
