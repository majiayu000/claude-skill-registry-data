---
name: ui-architecture
description: "UI architecture: primitive-component-composite-feature-page, composition over inheritance, state ownership, derived state. Avoid generic AI UI."
---

# ui-architecture

Compose upward: primitives → components → composites → features → pages. State lives with its owner; everything else derives.
## Inspection

Map the layer stack (primitives → pages), state owners, and route-file weight; find logic living in pages that belongs in modules.

## Decision rules

Pages hold routing only; domain code in feature modules; Server-first with client at interactive leaves; one data owner per datum.


## Activate when

- Structuring UI code, placing state, or reviewing component boundaries.

## Do NOT activate for

- Visual system decisions (see design-systems); global data flows (see state-management).

## Procedure

1. Layer strictly: primitives (unstyled/system-based) → components → composites → features → pages/routes. Pages hold routing only.
2. State: single owner per datum; derived data computed, never duplicated; server state via query layer, client state local until shared.
3. Composition over inheritance/props-sprawl;stable component APIs with explicit contracts.
4. Verify: no duplicated state, no prop-drilling chains, route files thin, ownership diagram reviewable.

## Failure modes

Fat pages with domain logic; client wrappers around whole subtrees; duplicated state across layers; unowned shared state.

## Escalation

State placement → frontend/state-management; module splits → architecture/modularity.
