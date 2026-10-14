---
name: java-immutability-modeling
description: "Trigger: Java immutability, records, value objects, defensive copies, mutable collections, DTO modeling. Model Java data safely and clearly."
license: MIT
metadata:
  author: andresnator
  status: testing
  version: "1.0.4"
---

# Skill: java-immutability-modeling

## Activation Contract

Use this skill when modeling Java data with records, value objects, immutable classes, defensive copies, collection ownership, equality, and state validation.

Do **not** use this skill for persistence mapping only, serialization-only configuration, generic DTO naming, or non-Java data modeling.

## Responsibility

This skill teaches safe Java state modeling. It does not call other skills, impose immutability everywhere, or choose framework annotations unless context requires them.

## Required Context

- Java version.
- Whether the type is domain model, value object, DTO, event, command, or persistence entity.
- Mutability requirements and ownership of collections.
- Equality/hashCode expectations.

## Context Budget

- Keep this `SKILL.md` focused on modeling decisions.
- Use `references/java-immutability.md` for records and defensive-copy details.

## Hard Rules

- Prefer immutable data for values, messages, events, and DTOs unless mutation is required.
- Validate invariants at construction time.
- Make defensive copies of mutable inputs and outputs when ownership is not transferred.
- Do not expose mutable internals accidentally.
- Use records for transparent immutable aggregates when they match the domain and Java version.
- Avoid records for entities that require identity, lazy mutation, or framework lifecycle constraints unless explicitly supported.

## Decision Gates

| Condition | Action |
|---|---|
| Data is a transparent immutable carrier | Prefer record if Java version supports it. |
| Mutable component is stored | Copy on construction and access, or document ownership transfer. |
| Domain invariant exists | Enforce in constructor/canonical constructor. |
| Type has identity/lifecycle mutation | Prefer class over record. |
| Collection is returned | Return immutable copy/view based on ownership contract. |

## Execution Steps

1. Identify the data role and mutability needs.
2. Choose record vs class based on invariants, identity, and framework constraints.
3. Define construction validation.
4. Protect mutable components.
5. Clarify equality and serialization implications when relevant.

## Output Contract

Return:

- Modeling choice: record, immutable class, mutable class, or other.
- Invariants and validation point.
- Mutability/ownership policy.
- Equality/hashCode implications.
- Example shape when useful.

## References

- `references/java-immutability.md` — Records, defensive copies, and modeling choices.

## Assets

- None.
