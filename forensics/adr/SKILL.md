---
name: adr
description: Writing and maintaining Architecture Decision Records (MADR-style) that are linked to the Architecture Profile — when an ADR is required, structure, statuses, supersession, and how ADRs back profile exceptions. Use whenever an architectural decision is made or changed, a profile exception is added, a new library/abstraction/pattern is introduced, or the user asks to document a decision.
user-invocable: false
---
# Architecture Decision Records

## An ADR is required when
- `profile.yml` changes (new module, recipe/axis change, conventions change)
- a profile exception is added or extended
- a new library that shapes code structure is introduced (mediator, ORM, messaging, validation)
- a ⚠️ combination from the compatibility matrix is used
- a decision is expensive to reverse (data model ownership, public contracts, event schemas)

## File & numbering
`docs/adr/NNNN-kebab-title.md`, four-digit sequence, never renumbered. Template: `assets/adr-template.md`.

## Writing rules
1. **Context = forces with evidence**, not a narrative. Numbers, constraints, incidents.
2. **Options ≥ 2**, including the status quo. Each with consequences, not just pros/cons adjectives.
3. **Decision** in one paragraph, active voice: "We will…".
4. **Consequences** include what becomes harder and the enforcement (test names or review rules).
5. **Profile diff** section contains the exact YAML change.
6. Status: `proposed` → `accepted` | `rejected`; later `superseded by NNNN` or `deprecated`.
   Never edit the decision of an accepted ADR — supersede it.
7. ≤ 2 pages. Detail goes in links.
