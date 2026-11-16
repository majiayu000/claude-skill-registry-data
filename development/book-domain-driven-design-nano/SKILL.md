---
name: book--domain-driven-design--nano
description: >-
  Domain-Driven Design (Eric Evans) — Minimal rules — essential one-liners only. Use when asked to apply Domain-Driven Design principles or review code against Domain-Driven Design standards.
origin: "github.com/ciembor/agent-rules-books (MIT)"
license: MIT
version: "1.0.0"
compatibility: "yana-ai >= 0.14.0"
---

# OBEY Domain-Driven Design by Eric Evans

## When to use

Use as always-on DDD guidance when domain language, invariants, lifecycle, or integration boundaries affect implementation choices.

## Primary bias to correct

Generic plumbing and DDD terminology are not a domain model.

## Decision rules

- Keep model, code, tests, documents, and team language aligned inside each Bounded Context.
- Make business behavior explicit in model code, not hidden in controllers, persistence, jobs, scripts, or framework glue.
- Refine Ubiquitous Language when terms are fuzzy, and use only models that solve the problem and can be implemented.
- Use tactical patterns for domain meaning: Entities for identity, Value Objects for value, Services for homeless operations, and Modules for conceptual cohesion.
- Treat Aggregates as consistency and lifecycle boundaries; expose roots only and protect invariants inside the boundary.
- Hide complex creation and persistence behind Factories and Repositories; design for the model first and storage second.
- Define context boundaries and relationships explicitly before sharing terms, data, or behavior across systems.
- Protect the Core Domain from generic subdomains, reusable mechanisms, infrastructure, framework pressure, and foreign models.
- Refactor toward deeper insight: make important constraints, policies, processes, and calculations explicit domain concepts.
- Test invariants, invalid construction, lifecycle transitions, and boundary translations in the Ubiquitous Language.

## Trigger rules

- Fuzzy or inconsistent terms trigger language refinement and code renaming.
- Procedural business rules in orchestration, SQL, jobs, or serializers trigger moving behavior into the model.
- Sprawling transactions or cross-module changes trigger Aggregate and context-boundary review.
- Foreign model, schema, API, or legacy pressure triggers translation or an explicit Conformist choice.
- Supporting mechanisms obscuring distinctive value trigger Core Domain distillation.

## Final checklist

- Domain behavior in the model?
- One language per context?
- Invariants protected by roots and values?
- Integration relationship explicit?
- Domain tests cover invalid states and translations?
- Core Domain still visible?
