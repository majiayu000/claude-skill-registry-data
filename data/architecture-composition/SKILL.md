---
name: architecture-composition
description: How to combine architecture styles correctly — Clean/Hexagonal/Onion, Vertical Slices, DDD tactical patterns, CQRS, Modular Monolith, transaction scripts — per module, using axes, a compatibility matrix and named recipes. Use this whenever a task involves where code belongs, mixing architectural styles, choosing a recipe for a module, reading or changing the Architecture Profile, or judging whether a structure is over- or under-engineered, even if the user only names one style.
user-invocable: false
---
# Architecture Composition

## 1. The model: styles answer different questions

| Axis | Question it answers | Values | Scale |
|---|---|---|---|
| **A1 Topology** | How many deployables? | monolith · modular-monolith · microservices | system |
| **A2 Boundaries** | Where are the business seams? | modules / bounded contexts | system |
| **A3 Dependency direction** | Which code may depend on which? | clean · hexagonal · onion · layered · none | module |
| **A4 Organization** | How are files grouped? | vertical-slices · technical-layers | module |
| **A5 Request model** | Same model for reads and writes? | none · separate-methods · separate-models · separate-stores | module |
| **A6 Domain logic** | Where do business rules live? | transaction-script · table-module · domain-model | module |
| **A7 Integration** | How do modules interact? | contracts (in-proc) · integration events (+outbox) · messaging | between modules |
| **A8 Persistence** | How is state accessed? | ef-core · dapper · stored-procedures · (event-sourcing) | module / use case |

**Composition law.** Exactly one value per axis per module. Styles on *different* axes compose.
Two styles on the *same* axis in the *same* module conflict. Different modules may choose
differently — that is the purpose of A2.

**Nesting.** A1 contains A2; each A2 module decides A3–A6 and A8; A7 connects modules. A decision at a
larger scale constrains smaller ones (microservices forbid shared-database A8; domain-model A6 forbids
invariants in SQL), never the reverse.

## 2. Recipes (named, valid compositions)

| Recipe | A3 | A4 | A6 | Typical A5 | Use when |
|---|---|---|---|---|---|
| **clean-sliced** | clean | vertical-slices | domain-model | separate-models | core subdomain, rich invariants, long life, several adapters |
| **sliced-domain** | none (rules via tests) | vertical-slices | domain-model | separate-methods | real invariants but small module; a Domain project would be ceremony |
| **pure-slices** | none | vertical-slices | transaction-script / table-module | separate-methods | CRUD-ish, supporting/generic subdomain, reporting |
| **hexagonal-integration** | hexagonal | vertical-slices | transaction-script | separate-methods | module dominated by external systems; needs anti-corruption layer |
| **layered-legacy** | layered | technical-layers | any | none | existing code only; frozen, migrated via `architecture-migration` |

Details, folder layouts and "where does X go" for each recipe: `references/placement-rules.md`.

## 3. Choosing a recipe for a module (fast path)
Score the module; each **yes** = 1 point.
1. Are there rules that span several entities and must hold after every change (invariants)?
2. Does an entity have a lifecycle/state machine with guarded transitions?
3. Are the rules regulated, audited, or expensive when wrong (fiscal, medical, financial)?
4. Will the rules change often and independently of the UI/DB?
5. Are there ≥ 2 real adapters for the same capability (API + jobs + messaging, or 2 providers)?
6. Will the module live > 3 years with more than one developer?

- 0–1 → **pure-slices**
- 2–3 → **sliced-domain** (or **hexagonal-integration** if Q5 is the main driver and rules are thin)
- 4–6 → **clean-sliced**

Then choose A5: `separate-models` if read shapes differ materially from the write model or reads
dominate; `separate-stores` only with measured read-scale or reporting isolation needs; otherwise
`separate-methods`. Full decision framework: skill `architecture-selection`.

## 4. Compatibility matrix (summary)
Full matrix with reasoning: `references/compatibility-matrix.md`.

| Combination (same module) | Verdict | Condition / reason |
|---|---|---|
| Clean + Vertical Slices | ✅ | Clean sets project dependencies; slices organize Application (and optionally Api) |
| Hexagonal + Vertical Slices | ✅ | slice = driving adapter + use case; ports only for driven dependencies |
| Domain Model + Vertical Slices | ✅ | aggregates shared across slices; slices never share handlers |
| Clean + Transaction Script | ⚠️ | legal but usually ceremony: empty Domain layer. Prefer pure-slices |
| Technical layers + Vertical Slices | ❌ | same axis A4. Pick one per module |
| Domain Model + business rules in SPs | ❌ | invariants split across two places; SPs read-side only |
| CQRS separate-stores + Transaction Script | ⚠️ | complexity with no domain to protect; justify with measured read load |
| Mediator everywhere + direct handlers | ❌ | same concern (dispatch), pick one convention per system |
| Microservices + shared database writes | ❌ | A1 forbids it; that is a distributed monolith |
| Modular Monolith + different recipe per module | ✅ | intended; enforce boundaries with tests |
| Event Sourcing + Transaction Script | ❌ | event sourcing needs an aggregate to decide events |

## 5. Rules that make combinations work
1. **Boundary before structure.** Decide A2 before A3/A4. A perfect Clean module with the wrong
   boundary is a well-organized mistake.
2. **Share down, not sideways.** Slices share the domain model and infrastructure, never each other.
   If slice B needs slice A's logic, move that logic into the domain (aggregate/domain service) or a
   module-internal service — never call A's handler.
3. **Rule of three for shared application code.** Duplicate across two slices; extract on the third,
   into the lowest layer that makes sense.
4. **Ports only where there is a real seam:** external system, second implementation, or a test seam
   that cannot use the real thing. `IRepository` over EF Core in a pure-slices module is not a seam.
5. **Contracts are the module's only public surface.** Everything else is `internal`.
6. **Every structural rule is either an architecture test or explicitly `enforce: review`.**

## 6. Anti-patterns (flag as MAJOR unless noted)
- **Ceremony Clean** — 4 projects, repositories, mappers, mediator for a CRUD module.
- **Anemic Domain project** — entities with public setters, logic in handlers, inside `clean-sliced`.
- **Slice-to-slice calls** — handler injecting another slice's handler. (BLOCKER in clean-sliced)
- **Common/Shared/Services dumping ground** at module root.
- **Generic repository over EF Core** — hides the query capabilities you already have.
- **Cross-module DB joins in write paths.** (BLOCKER)
- **Contracts leaking domain types** — integration events carrying aggregates or EF entities. (BLOCKER)
- **Recipe drift** — new slices in a different style than the module's recipe.

## 7. Output when this skill is used for a decision
```
MODULE: <name>  SUBDOMAIN: <core|supporting|generic>  SCORE: <n/6>
RECIPE: <recipe>  AXES: A3=<> A4=<> A5=<> A6=<> A8(write/read)=<>
WHY: <forces → choice, 2–4 lines>
REJECTED: <recipe — reason>
ENFORCEMENT: <architecture tests to add>
```

## References
- `references/placement-rules.md` — per-recipe folder layout and "where does X go" table. Read before placing any file.
- `references/compatibility-matrix.md` — full pairwise matrix with reasons and mitigations.
- `references/profile-schema.md` — every field of `profile.yml` and how agents use it.
- Frontend: `references/frontend-composition.md` — applying the same axes to React/TS (feature-sliced) and Blazor.
