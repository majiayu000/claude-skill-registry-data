---
name: business-finder
description: Capture uncertain product intent in business language and optionally project structure through Initiative.
disable-model-invocation: true
---

# Business Finder

Explicit human entrypoint for a colleague without technical capability. Use
familiar business language and explain backlog terms before using them.
Unknown values remain explicit.

## Intake profile

Capture the actor or affected party, problem or opportunity, desired outcome
and value, evidence, constraints, non-goals, urgency, and open questions.
Preserve the human's wording when it already lands. This profile asks no
implementation or architecture questions.

Use `$wait-what` when a request or project term does not land: pause, repitch it
in familiar language, and ask again. Use `$show-me` before each structure
decision to present all relevant existing Product Areas and Initiatives with
the proposed impact. Presentation informs the human and grants no mutation
authority.

## Composition

Compose [the shared Finder engine](../finder-phase/SKILL.md) with immutable
intake lens `Business`, this presentation profile, and projection ceiling
`Initiative`. The engine alone owns the Fog lifecycle, generic support work,
resume routing, and durable handoff.

Optional structure may reuse, enrich, or create Product Areas and Initiatives
through `$write-backlog`. The ceiling is Initiative: Business Finder never
projects an Epic, Story, or Task. Skipping projection, or returning an
unresolved projection, never blocks a valid Fog result.

## Bounded return

Return the exact Fog identity, immutable Business intake lens, generic support
work and evidence, optional exact Product Area and Initiative readback,
unresolved decisions, and durable Finder handoff. Return control without
asserting that the Fog is resolved or complete.
