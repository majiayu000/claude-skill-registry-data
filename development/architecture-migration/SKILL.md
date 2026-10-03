---
name: architecture-migration
description: Incremental, reversible migration between architecture styles in brownfield systems — layered/N-tier to vertical slices, anemic model or service layer to domain model, big-ball-of-mud monolith to modular monolith, stored-procedure-centric logic to domain model, and module extraction — using strangler patterns, seams, characterization tests and checkpoints. Use whenever existing code does not match the target recipe, a module is marked layered-legacy, or the user asks to refactor or modernize architecture.
user-invocable: false
---
# Architecture Migration

## Laws
1. **No big bang.** Every step ships, builds, passes tests, and is revertible on its own.
2. **Characterize before changing.** Lock current behavior with tests (integration-level) before moving code.
3. **Migrate by use case, not by layer.** One endpoint/use case at a time moves to the target recipe.
4. **New code goes to the target immediately;** old code moves when touched or by planned batch.
5. **Track progress in the profile:** module `recipe: layered-legacy` + `notes: "migrating to <recipe>; N/M use cases done"` and an ADR.

## M1 — Layered (Controller/Service/Repository) → Vertical slices
1. Pick the most-changed use case (git log frequency). Write characterization tests at HTTP level.
2. Create `Features/{Feature}/{UseCase}/` with endpoint + handler that **calls the existing service** (strangler facade).
3. Route traffic to the new endpoint (same route; remove the controller action).
4. Inline the service method's logic into the handler; delete it from the service when unused.
5. Replace repository calls with direct DbContext/Dapper usage as the recipe allows.
6. Repeat. When a service/repository becomes empty, delete it. Architecture test for the module
   switches from "legacy allowed" to recipe rules when the last use case moves.

## M2 — Anemic model / transaction scripts → Domain model
1. Inventory rules scattered in services/handlers/SPs per entity (grep for status checks, validations, calculations).
2. Choose the aggregate boundary (skill `ddd-tactical` procedure).
3. Encapsulate: make setters private one property at a time; the compiler lists every place that writes → move each write into an intent method.
4. Move the rules into those methods; handlers become load → call → save.
5. Add aggregate unit tests for each moved rule; delete duplicated checks.
6. SP-embedded rules: keep SP as-is behind characterization tests, move the rule to the aggregate,
   reduce SP to persistence or remove it; never have the rule in both places after the step ends.

## M3 — Monolith → Modular monolith
1. **Discover seams:** namespaces, change coupling (files changed together), table clusters by write access, team ownership.
2. Draft modules + ownership table (which module writes each table). Conflicts = boundary decisions for the architect.
3. Create module projects + Contracts; move code without behavior change (namespace moves only).
4. Replace direct cross-module calls with contracts/events, one dependency at a time; add architecture test in "report-only" mode, then enforce per module.
5. Split schemas: move tables to module schemas with synonyms/views for transition; remove cross-schema FKs; remove synonyms at contract phase.

## M4 — Extract a module into a service
Precondition checklist in `modular-monolith` §Extraction path. If any item is false, fix that first.

## Checkpoint template (per step, in the plan)
```
STEP: <n> — <use case / component>
BEFORE: <characterization tests: names, green>
CHANGE: <moves and rewrites>
AFTER: <tests green; architecture tests status>
ROLLBACK: <git revert of this step is sufficient | additional DB step>
PROGRESS: <k/N use cases on target recipe>
```
