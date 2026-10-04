---
name: architecture-principles
description: "Guides module boundaries, dependency direction, and domain structure. Do not use for local edits that leave architecture unchanged."
---

# Skill: architecture-principles

## Purpose

Design and modify software while preserving boundaries, dependency direction, domain clarity, and long-term maintainability.

This skill covers Clean Architecture, Hexagonal Architecture, DDD, modularity, layering, dependency inversion, and boundary discipline.

## First Rule

Respect the existing architecture.

Do not force Clean Architecture, DDD, CQRS, Event Sourcing, Hexagonal Architecture, microservices, or any other style unless:

- the repository already follows it;
- the change clearly requires it;
- or the user explicitly requests it.

Architecture is a tool. It is not a costume party for simple CRUD.

## Dependency Direction

Prefer dependencies pointing toward stable business rules.

General direction:

```text
Transport / UI / CLI
  -> Application / Use Cases
      -> Domain
Infrastructure / Persistence / External APIs
  -> Application or Domain abstractions
```

Rules:

- Domain rules must not depend on transport details.
- Domain rules must not depend on database models unless the repository intentionally uses active record style.
- Application/use-case code coordinates behavior but should not become a dumping ground.
- Infrastructure implements details and adapters.
- Transport layers should be thin.

## Boundary Rules

Do not mix:

- routing and business policy;
- validation and persistence;
- domain rules and HTTP/CLI details;
- database schema models and public API schemas unless deliberate;
- configuration parsing and runtime behavior;
- hardware control and UI state;
- integration retries and domain decisions.

When boundaries are already messy, make the change without making them worse.

## Domain-Driven Design

Use DDD where domain complexity justifies it.

Prefer DDD concepts when the codebase has:

- rich business rules;
- multiple domain concepts with invariants;
- workflows that need clear language;
- bounded contexts;
- domain events or policies;
- complex state transitions.

Do not use DDD ceremony for simple data plumbing.

### DDD Practical Rules

- Use domain language in names.
- Keep invariants close to the domain model.
- Make invalid states hard or impossible to represent.
- Keep application orchestration separate from domain decisions.
- Keep infrastructure adapters outside the domain model.
- Keep bounded contexts explicit.
- Do not leak persistence concerns into domain behavior.

## Clean Architecture Practical Rules

- Business rules should not know about frameworks.
- Use cases should express application behavior.
- Adapters translate between external systems and internal models.
- Interface boundaries should exist where they reduce coupling, not because diagrams enjoy arrows.
- Dependency inversion is useful when there are multiple implementations, test seams, or infrastructure volatility.

## Package / Module Design

A package should have a reason to exist.

Good package reasons:

- one bounded context;
- one application capability;
- one integration boundary;
- one infrastructure adapter;
- one presentation area;
- one hardware responsibility.

Bad package reasons:

- "misc";
- "common" full of unrelated code;
- "services" as a junk drawer;
- "models" containing every shape in the universe.

## Interface Rules

Introduce an interface/abstraction when it helps with:

- dependency inversion;
- testability;
- multiple implementations;
- external system isolation;
- stable domain/application contracts.

Do not introduce interfaces for one implementation unless the boundary is meaningful.

## Data Flow

Make data flow explicit.

Avoid:

- hidden service locators;
- global mutable registries;
- implicit configuration reads everywhere;
- side-effectful imports;
- action-at-a-distance state changes.

## Architecture Review Checklist

Before finishing an architectural change, verify:

- responsibilities are cohesive;
- dependency direction is preserved;
- public contracts are stable or intentionally changed;
- new abstractions have real callers or clear boundary value;
- errors cross boundaries in a controlled way;
- tests cover important behavior;
- no layer gained unrelated responsibilities.
## Extended References


For deeper architecture work, read the relevant documents:

- `../../engineering/05_design_principles.md`
- `../../engineering/06_responsibility_model.md`
- `../../engineering/09_architectural_smells.md`
- `../../engineering/22_evolution_rules.md`
