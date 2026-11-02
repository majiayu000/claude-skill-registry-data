---
name: engine-architecture-adr
description: "Creates evidence-backed architecture decision records for a game engine. Use when selecting boundaries, libraries, thread models, renderer strategies, or language-specific trade-offs."
---

# Engine Architecture Adr

## Use when
A consequential engine decision must be made without allowing preference or novelty to masquerade as evidence.

## Workflow
1. Write the decision context, target workload, current constraints, and the measurable failure that would matter.
2. List at least two viable options, including the simplest option that meets the requirement; note costs, portability, debugging effort, and exit paths.
3. Run the cheapest representative spike or benchmark needed to discriminate between options; label assumptions that cannot yet be tested.
4. Record the decision, rejected alternatives, migration triggers, owner, and a date or milestone for revisiting it.

## Required output
An ADR with context, constraints, options table, evidence links, decision, consequences, and explicit revisit triggers.

## Validation
- Every claim about performance or platform support has a source or is marked unverified.
- The decision can be reversed or migrated without hiding its cost.
- The chosen design solves a stated requirement rather than an imagined future scale.

## Guardrails
Do not adopt an abstraction, dependency, thread, or language merely because it is fashionable; keep prototypes disposable until evidence justifies the commitment.
