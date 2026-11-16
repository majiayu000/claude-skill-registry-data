---
name: book--domain-driven-design--mini
description: >-
  Domain-Driven Design (Eric Evans) — Condensed rules — key principles distilled. Use when asked to apply Domain-Driven Design principles or review code against Domain-Driven Design standards.
origin: "github.com/ciembor/agent-rules-books (MIT)"
license: MIT
version: "1.0.0"
compatibility: "yana-ai >= 0.14.0"
---

# OBEY Domain-Driven Design by Eric Evans

## When to use

Use when business complexity, model language, lifecycle rules, or cross-team/system boundaries shape the design more than generic technical organization.

## Primary bias to correct

Keep domain behavior, code, tests, documents, and team language aligned inside explicit Bounded Contexts. Do not let persistence, UI, frameworks, integration formats, or DDD vocabulary replace an implementation-driving model.

## Decision rules

- Use a model only when it organizes domain knowledge, clarifies communication, and can be expressed in implementation; iterate through code, expert conversation, scenarios, and refactoring toward deeper insight.
- Maintain one Ubiquitous Language per Bounded Context across names, tests, documents, diagrams, planning, and feature discussion; keep explanatory models separate from the implementation model.
- Put business logic in the domain layer. Keep UI, application coordination, infrastructure, persistence, messaging, and framework constraints outside the model or behind adapters.
- Use tactical patterns for model meaning: Entities for stable identity, Value Objects for immutable descriptive value, Services for important operations with no natural object home, and Modules for conceptual cohesion.
- Manage lifecycle through Aggregates, Factories, and Repositories: expose only Aggregate roots, enforce invariants inside the boundary, hide complex creation and persistence, and prevent partially formed objects from escaping.
- Design domain objects for the model first and persistence second; preserve identity, Aggregate boundaries, Value Object semantics, and domain query criteria instead of exposing database structure.
- Refactor toward deeper domain insight, not only mechanical cleanliness. Make constraints, policies, processes, calculations, allocations, and generation rules explicit when they carry domain meaning.
- Design for model users: name operations by domain purpose, separate side-effect-free functions from state-changing commands, make assertions explicit, and shape boundaries around conceptual contours.
- Define every Bounded Context explicitly. Do not assume a term has the same meaning elsewhere; use context maps, tests, and active communication to protect model integrity.
- Choose context relationships deliberately: Shared Kernel, Customer/Supplier, Conformist, Anticorruption Layer, Separate Ways, Open Host Service, Published Language, or incremental legacy replacement.
- Distill and protect the Core Domain by strategic value. Keep generic subdomains, infrastructure, reusable mechanisms, and supporting details from consuming core-domain attention.
- Add large-scale structure only when individual objects no longer make a large model understandable; keep structures domain-specific, evolvable, and valid only inside compatible contexts.
- Use analysis patterns, design patterns, specifications, industry formalisms, and prior art only when they clarify the current model and preserve domain language.
- Test the model in the Ubiquitous Language: prioritize domain tests for invariants, allowed and forbidden transitions, valid construction, specifications, application orchestration, and boundary translation before generic infrastructure checks.
- Make major strategic moves with people who understand both the implementation and the domain; architecture and framework guidance must serve application teams and domain goals.

## Trigger rules

- When terminology is awkward, ambiguous, inconsistent, or repeatedly translated, refine the Ubiquitous Language and rename code before adding more behavior.
- When controllers, services, scripts, SQL, jobs, or serializers carry business decisions, move rules into domain objects, domain services, specifications, or explicit domain concepts.
- When UI, persistence, messaging, APIs, or frameworks start shaping domain concepts, isolate them with layers, adapters, translation, or an Anticorruption Layer.
- When a change crosses unrelated modules, many objects, or multiple roots, reassess Module cohesion, Aggregate ownership, consistency timing, and context boundaries.
- When clients know creation, lifecycle, persistence, identity generation, or internal mutation details, repair Factories, Repositories, roots, and encapsulation.
- When new behavior is hard to explain, test, or extend, search for a deeper model, missing implicit concept, or breakthrough refactoring instead of adding procedural branches.
- When integrating with another model, choose the relationship, translation strategy, published language or protocol, and boundary tests before writing boundary code.
- When changing invariants, lifecycle transitions, specifications, orchestration, or context translation, add domain-language tests that prove valid behavior and block invalid states.
- When generic mechanisms, reusable frameworks, or supporting subdomains obscure distinctive value, distill the Core Domain or separate the mechanism.

## Final checklist

- Is domain behavior explicit in the model rather than hidden in delivery, persistence, or integration code?
- Do code, tests, documents, and conversations use one language inside each Bounded Context?
- Do tactical patterns protect identity, value semantics, lifecycle, invariants, and responsibility instead of adding ceremony?
- Does every cross-context integration have an explicit relationship, translation strategy, and boundary test?
- Do tests read like executable examples of the model and cover invalid transitions or construction?
- Is the Core Domain visible and protected from supporting complexity, generic mechanisms, infrastructure, and frameworks?
