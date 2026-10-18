---
name: functional-finder
description: Develop uncertain product behavior nontechnically and optionally project structure through Epic.
disable-model-invocation: true
---

# Functional Finder

Explicit human entrypoint for a functional colleague. It includes every
Business Finder capability and adds nontechnical product-behavior guidance.
It does not require Business Finder to have run first.

## Intake profile

Capture the Business profile plus actor, trigger, workflow, observable result,
applicable domain rules, visible alternate and failure paths, acceptance
signals, boundaries, known product dependencies, technical handoff questions,
and target `V*` milestone context. Unknown values remain explicit.

This profile does not require architecture, APIs, data models, component
boundaries, code structure, Tasks, commands, workers, or implementation design.

Use `$wait-what` when terminology or behavior does not land. Use `$show-me` at
each decision about the observable workflow, an alternate or failure path, a
product dependency, milestone context, and final Epic projection. Presentation
informs the human and grants no mutation authority.

## Composition

Compose [the shared Finder engine](../finder-phase/SKILL.md) with immutable
intake lens `Functional`, this presentation profile, and projection ceiling
`Epic`. The engine alone owns the Fog lifecycle, generic support work, resume
routing, and durable handoff.

Optional structure may reuse, enrich, or create Product Areas, Initiatives,
and Epics through `$write-backlog`. The ceiling is Epic: Functional Finder
never projects Stories or Tasks. Skipping projection, or returning an
unresolved projection, never blocks a valid Fog result.

## Bounded return

Return the exact Fog identity, immutable Functional intake lens, generic
support work and evidence, optional exact Product Area, Initiative, and Epic
readback, unresolved decisions, and durable Finder handoff. Return control
without asserting that the Fog is resolved or complete.
