---
name: domain-modeling
description: "Model entities, value objects, aggregates, ownership, invariants. Separate domain, persistence, DTO, response models; never auto-expose ORM entities."
---

# domain-modeling

Make illegal states unrepresentable; keep persistence and API shapes out of the domain.

## Activate when

- Modeling business concepts, drawing aggregate boundaries, or reviewing anemic/leaky domain code.

## Do NOT activate for

- Table/index design (see databases/fundamentals); API contract shaping (see architecture/api-design).

## Inspection

List the concepts, their lifecycles, who owns them, and the invariants that must always hold. Find where ORM entities leak into APIs and where validation lives.

## Decision rules

- Entity (identity matters) vs value object (attributes matter, immutable) vs aggregate (consistency boundary with one root).
- Invariants enforced by the aggregate root at mutation time — never by callers remembering.
- Four models, four jobs: domain (rules) / persistence (ORM rows) / DTO (wire shapes) / response (client views). Map explicitly between them; auto-exposing ORM entities is a defect.
- Repositories per aggregate, not per table; domain events for cross-aggregate effects (with outbox, not dual-write).

## Procedure

1. Name aggregates, roots, and invariants; draw ownership and cross-aggregate flows.
2. Move validation into roots/value objects; split the four model layers with explicit mappers.
3. Cover each invariant with a test that violates it directly.
4. Verify: no ORM import in web layer, no invariant enforceable only by convention, aggregate tests green.

## Failure modes

- Anemic models (getters + service scripts); god aggregates; lazy-loading outside transactions; dual-write to DB + queue without outbox.

## Escalation

Persistence mechanics → databases/*; event transport → distributed/systems.

## References

- Related: `../data-modeling/`, `../../backend/database-design/`, `../../backend/validation/`.
