---
name: data-model-planner
description: Plans a conceptual or logical data model covering entities, attributes, relationships, invariants, validation, ownership, lifecycle, retention, and migration concerns without generating implementation code. Use when the user asks to design, review, or evolve a domain model, database schema plan, content model, persistence model, or data migration approach before implementation.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: planner
  audience: product-and-engineering-teams
  tags:
    - data-modeling
    - schema-design
    - domain-modeling
    - validation
    - data-ownership
    - lifecycle
    - migration
  status: draft
  side_effects: none
---

# Data Model Planner

## Purpose

Turn product requirements, domain rules, and existing data constraints into an implementation-neutral data model plan. Define what data exists, how it relates, who owns it, which rules must hold, how it changes over time, and how an existing model can evolve safely.

## When to use this skill

Use this skill when:

- A feature or product needs a conceptual or logical data model before implementation.
- The user asks to plan entities, fields, relationships, constraints, ownership, retention, deletion, or migration.
- An existing model must evolve and the team needs compatibility, backfill, rollout, or rollback considerations.
- Requirements describe workflows but leave persistence boundaries or data invariants unclear.
- Multiple systems, services, tenants, organizations, or users may create, own, share, or modify the same data.

Do not use this skill when:

- The user wants SQL, ORM models, migrations, API schemas, or other implementation code.
- The main task is selecting a database product or benchmarking storage technologies.
- A physical database tuning task needs indexes, partitioning, query plans, or capacity calculations.
- The request is only to document an already-finalized schema without planning or evaluating it.

## Inputs to inspect

Start with the smallest useful set of available inputs:

- Product brief, requirements, acceptance criteria, and explicit non-goals.
- User flows, permissions, roles, tenancy rules, and administrative workflows.
- Existing schemas, entity diagrams, API or event contracts, sample records, and migration notes.
- Integration boundaries, upstream sources, downstream consumers, and synchronization rules.
- Privacy, security, audit, legal, retention, deletion, localization, and accessibility requirements.
- Expected scale, concurrency, offline behavior, import/export needs, and historical reporting needs when they affect the model.

Do not invent missing business rules. Record consequential gaps as assumptions or open decisions and explain their modeling impact.

## Workflow

1. **Frame the model boundary.** State the capability being modeled, primary actors and workflows, systems in scope, systems out of scope, authoritative sources, and known constraints. Distinguish facts from assumptions.
2. **Build a domain vocabulary.** List important terms, define ambiguous words, identify synonyms, and separate real domain concepts from UI labels, transport shapes, and storage artifacts.
3. **Identify candidate entities.** For each entity, state its purpose, identity, essential attributes, mutable attributes, derived values, sensitive data, and whether it is an entity, value object, event, or reference data. Avoid entities that merely mirror screens or request payloads.
4. **Define identity and uniqueness.** Describe stable identity, natural or surrogate identity considerations, tenant scope, uniqueness boundaries, deduplication needs, and behavior when external identifiers change or collide. Keep the decision implementation-neutral.
5. **Map relationships.** For every relationship, define direction, cardinality, optionality, ownership, ordering if meaningful, and behavior when either side changes or disappears. Resolve many-to-many relationships into explicit domain concepts when the relationship has attributes or lifecycle rules of its own.
6. **Specify invariants and validation.** Separate field-level validation, cross-field rules, cross-entity invariants, state-dependent rules, and rules that require external knowledge. State when each rule must hold and whether historical records remain valid after a rule changes.
7. **Assign authority and ownership.** Identify the system of record and the actor or service allowed to create, read, update, transfer, archive, restore, or delete each entity. Clarify tenant boundaries, shared records, delegated control, and conflict resolution.
8. **Model lifecycle and history.** Define creation, activation, transitions, archival, restoration, expiration, soft or hard deletion, retention, anonymization, and audit needs. Use a state table when transitions have guards or side effects. Distinguish current state from immutable history.
9. **Check time and concurrency semantics.** Clarify effective dates, event time versus processing time, time zones, versioning, stale writes, concurrent edits, idempotency, and duplicate delivery only where relevant to the domain.
10. **Plan evolution and migration.** Inventory affected records and consumers; identify additive, breaking, or semantic changes; define mapping, defaulting, backfill, validation, compatibility window, rollout order, observability, failure handling, and rollback or forward-fix strategy. Never assume missing historical values can be reconstructed.
11. **Stress-test the model.** Walk through happy paths plus partial data, duplicate records, ownership transfer, deletion with dependents, restored records, rule changes, failed imports, concurrent updates, and interrupted migrations. Record contradictions and unresolved choices.
12. **Produce the plan.** Present a recommended model, viable alternatives only where a real decision remains, explicit rationale, migration concerns, and questions that must be answered before implementation. Do not emit implementation code or vendor-specific DDL.

## Output format

Return:

```md
## Summary

Scope, recommended model, and the most consequential decisions.

## Assumptions and open decisions

| Item | Status | Modeling impact | Owner or evidence needed |
|---|---|---|---|

## Domain vocabulary

| Term | Meaning | Notes or avoided ambiguity |
|---|---|---|

## Entity plan

| Entity | Purpose and identity | Key attributes | Owner / source of truth | Lifecycle |
|---|---|---|---|---|

## Relationship plan

| From | Relationship | To | Cardinality / optionality | Ownership and delete behavior |
|---|---|---|---|---|

## Validation and invariants

| Rule | Scope | When enforced | Failure or historical-data behavior |
|---|---|---|---|

## Permissions and data ownership

Creation, mutation, transfer, sharing, tenancy, and conflict rules.

## Lifecycle and history

States, allowed transitions, retention, deletion, restoration, and audit requirements.

## Migration and evolution plan

Current-to-target mapping, compatibility, backfill, rollout, validation, monitoring, and recovery concerns.

## Risks and edge cases

- ...

## Readiness checklist

- [ ] Entity boundaries and identities are explicit.
- [ ] Relationships include cardinality, optionality, ownership, and delete behavior.
- [ ] Validation and invariants are testable and assigned to an authority.
- [ ] Lifecycle, retention, deletion, and history behavior are defined.
- [ ] Migration assumptions, compatibility, validation, and recovery are addressed.
- [ ] Open decisions have owners or required evidence.
```

Use concise tables, prose, or Mermaid diagrams according to complexity. A diagram supplements the written rules; it does not replace cardinality, ownership, lifecycle, or migration details.

## Quality bar

The task is complete only when:

- Every proposed entity has a clear domain purpose, identity, authority, and lifecycle.
- Every important relationship states cardinality, optionality, ownership, and delete behavior.
- Business invariants are distinguished from input formatting and storage choices.
- Authorization and data ownership are not inferred from relationship structure alone.
- History, retention, deletion, restoration, and privacy-sensitive fields are addressed where relevant.
- Migration guidance covers existing data, dependent consumers, rollout validation, and recovery.
- Assumptions and unresolved decisions are visible rather than presented as facts.
- The result remains implementation-neutral and contains no SQL, ORM, migration, or API implementation code.

## Edge cases

- **Greenfield model:** Describe evolution assumptions even when no migration is immediately required.
- **Legacy schema without documentation:** Infer cautiously from evidence and label every inference.
- **Event-sourced or append-only systems:** Separate immutable facts from projections and current-state views.
- **Multi-tenant data:** Define identity, uniqueness, access, transfer, export, and deletion within tenant boundaries.
- **Shared or collaborative records:** Separate stewardship, legal ownership, edit authority, and visibility.
- **External system of record:** State synchronization direction, conflict policy, unavailable-source behavior, and local cache authority.
- **Changing validation rules:** Define treatment of previously valid records and whether revalidation is required.
- **Deletion with dependencies:** Choose and justify restrict, detach, anonymize, archive, or cascade semantics at the domain level.
- **Irreversible migration:** Require explicit risk acceptance, rehearsal, backup or recovery evidence, and a forward-fix path.

## Related skills

- `project-brief-builder`
- `requirements-gap-finder`
- `user-flow-planner`
- `constraint-mapper`
- `implementation-order-planner`
- `implementation-checkpoint-planner`
