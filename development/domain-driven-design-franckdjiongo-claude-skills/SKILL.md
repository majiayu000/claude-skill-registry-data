---
name: domain-driven-design
description: >-
  Expert advisor for Domain-Driven Design, greenfield and brownfield: bounded contexts,
  aggregates, value objects, ubiquitous language, EventStorming, context maps, CQRS,
  event sourcing, anemic model, strangler fig. Use for DDD, "entity or value object?",
  modeling a complex domain.
---

# Domain-Driven Design — Production Reference

This skill is a field-ready expert on Domain-Driven Design covering strategic design, tactical design, supporting architectures, anti-patterns, and migration. It is grounded in a single canonical reference and applies equally to **greenfield projects** (design the domain model right the first time) and **existing projects** (diagnose anemic drift, refactor aggregates, strangle legacy, introduce bounded contexts progressively).

## How to use this skill

DDD is deep. Load only the section you need. Each reference file below is self-contained and stands on its own; jump to the one that matches the user's question.

| If the task involves… | Load |
|---|---|
| Deciding whether DDD applies; carving subdomains; naming bounded contexts; building ubiquitous language; context mapping; EventStorming / Domain Storytelling / Example Mapping / Wardley; Core Domain Charts; Bounded Context Canvas. | `references/01-strategic-design.md` |
| Modeling entities vs value objects; sizing aggregates and finding their invariants; domain events; repositories; domain / application / infrastructure services; factories; modules; specifications; policies / process managers / sagas. | `references/02-tactical-design.md` |
| Hexagonal / Onion / Clean architecture; CQRS (simple and full); event sourcing; inter-context communication; outbox/inbox; microservices; serverless; multi-tenant SaaS; Power Platform/Dataverse; persistence strategies (RDBMS, document, event store, Dataverse, KV). | `references/03-architecture-integration.md` |
| Diagnosing anti-patterns (anemic model, god aggregate, generic/leaky repository, infra leakage, DDD-Lite, primitive obsession, shared DB, event sprawl, double-write, CRUD-as-DDD, smart UI); greenfield minimum viable DDD; brownfield Strangler Fig + ACL + incremental extraction; team onboarding; living artifacts. | `references/04-anti-patterns-adoption.md` |
| Clarifying vocabulary; pointing the user to authoritative sources; citing Evans/Vernon/Khononov/Brandolini/Tune/Kaiser; naming the current state of practice (Team Topologies, data mesh, AI-assisted modeling). | `references/05-glossary-and-bibliography.md` |

If the question spans multiple sections (common), load several. The references are short (~200–400 lines each).

## Core philosophy you should transmit

Six principles carry everything else. Use them to frame answers when the user asks *why* we do something a given way.

1. **Model-driven design.** Code is the model; the model is the code. If one drifts, the team drifts. The single most valuable artifact in complex software is a *useful model of the domain*, built collaboratively with domain experts and expressed faithfully in code.
2. **Ubiquitous Language.** One language per bounded context, used in conversation, tests, code, and documents. Class, method, event, variable names match the glossary literally. Rename PRs are welcome, not rejected.
3. **Collaboration with domain experts.** Designers sit with the people who live the domain; no intermediaries paraphrasing requirements.
4. **Focus on the core domain.** Spend your best people on what differentiates the business. Buy, borrow, or outsource the rest.
5. **Continuous refinement.** The model evolves as understanding deepens; refactoring toward deeper insight is expected, not avoided.
6. **Strategic before tactical.** Patterns are worthless applied to the wrong boundary. *Tactical DDD on wrong boundaries amplifies pain.*

The philosophy: DDD is reasoning **above** frameworks. It is not a framework, not an architecture, not a mandatory set of classes, not a microservices recipe.

## When DDD applies (give this honestly, even against the user's wishes)

DDD pays off when **most** of these are true:

- Business logic is the source of competitive advantage.
- Rules are contested, evolving, and hard to write down.
- System will live more than 2–3 years and accumulate features.
- Multiple teams will work on it concurrently.
- Domain experts are available (or can be made available).
- The domain has non-trivial invariants, workflows, lifecycles.

DDD is **overkill** when: the app is a thin UI over a database (pure CRUD), rules are simple and stable, team is 1–2 devs building an MVP, no domain expert is reachable, expected lifespan is short.

### Scoring rubric for "is this a DDD candidate?"

Score 0–2 per item. Total:

- Business logic is a competitive differentiator.
- Rules are contested and change often.
- Expected lifespan > 2 years.
- More than one team will contribute.
- Domain experts are reachable.
- Domain has non-trivial invariants.
- Integration with multiple other systems.
- Multi-tenant or multi-market.

**≥ 10** → do full DDD. **5–9** → strategic DDD + light tactical. **< 5** → Transaction Script / Active Record; stop pretending.

Khononov's **business-logic-complexity** ladder is the lens: for trivial logic use Transaction Script; for moderate logic Active Record; reach for full Domain Model only when complexity justifies it. **Strategic DDD always pays off at system-of-systems scale; tactical DDD is optional.**

## Two-minute decision trees

Keep these in mind before loading deeper references — they answer ~70% of incoming questions.

### Entity or Value Object?

```
Is identity required independently of attributes?                → Entity
Are two with equal attributes interchangeable?                   → Value Object
Does the concept have a lifecycle (created, changed, archived)?  → Entity
Does the concept represent a measurement, quantity, description? → Value Object
In doubt?                                                        → Value Object; promote later
```

Vernon's heuristic: *"When in doubt, start as a value object; promote to entity only when identity is required."*

### Domain event or Integration event?

```
Consumer inside this bounded context and process?
├── Yes → Domain event (in-process handler is fine)
└── No  → Integration event (versioned schema, outbox, translation at the edge)
```

Never use the domain-event schema as the integration contract — every internal rename breaks consumers.

### Which context-mapping pattern?

```
External organization?
├── Yes → Published Language + OHS (you produce) / ACL (you consume)
└── No  →
    Cooperating teams?
    ├── Yes → Partnership [+ Shared Kernel if small shared core]
    └── No  →
        Power balance?
        ├── You control upstream → Customer/Supplier
        ├── Upstream dominant, model OK → Conformist
        └── Upstream dominant, model bad → Anticorruption Layer
Integration cost > value? → Separate Ways
Legacy tangle? → Recognize as Big Ball of Mud; wall off with ACL; strangle
```

### Aggregate boundary

Vernon's four rules (`references/02-tactical-design.md` has details):

1. **Model true invariants in consistency boundaries.** Only invariants that *must* be consistent together live in the same aggregate.
2. **Design small aggregates.** Small is the default.
3. **Reference other aggregates by identity only.** Store `CustomerId`, not `Customer`.
4. **Use eventual consistency between aggregates.** Multi-aggregate coordination is domain events + process managers, not transactions.

**One aggregate per transaction** is the single most important tactical constraint in DDD. Breaking it produces contention, deadlocks, unclear ownership.

## Adoption, brownfield and review

Greenfield minimum viable sequence, brownfield recipe (Strangler Fig + ACL + incremental extraction, EventStorm the as-is first), team onboarding and the code-review checklist for anemic drift (public setters, primitives where a VO exists, `*Service` enforcing invariants, ORM types in the domain): `references/04-anti-patterns-adoption.md`. Defer event sourcing, full CQRS, sagas and brokers until a concrete need appears.

## Response style

When answering a DDD question:

1. **Anchor in the specific principle or pattern** (name it — *Shared Kernel*, *Bounded Context Canvas*, *Vernon's four rules*, *Strangler Fig*). Give the reader the vocabulary to read more.
2. **Distinguish strategic from tactical.** If the user asks a tactical question but the real problem is strategic, say so.
3. **Explain the *why*, not just the *what*.** DDD is reasoning; rote instructions backfire.
4. **Offer decision trees** for binary choices (entity/VO, domain/integration event, context-mapping pattern).
5. **Cite the canonical source** (Blue Book, Red Book, Learning DDD, Tune, Kaiser) when useful. Full citations: `references/05-glossary-and-bibliography.md`.
6. **Refuse to over-engineer.** If the user is building CRUD with simple rules, recommend Transaction Script or Active Record honestly.
7. **Language matters.** When naming things in examples, name them like the domain — not `FooService` or `EntityBase`.

## Canonical lineage you can cite

Evans (Blue Book, 2003), Vernon (Red Book, 2013; Distilled, 2016), Khononov (Learning DDD, 2021), Brandolini (EventStorming, 2021), Tune and Uludağ (Architecture Modernization, 2024), Kaiser (2022-2024). Full citations: `references/05-glossary-and-bibliography.md`.

---

**Remember:** DDD solves a specific problem — *the team and the code disagreeing about what words mean*. If that is not the user's problem, the best DDD advice is "you don't need DDD."
