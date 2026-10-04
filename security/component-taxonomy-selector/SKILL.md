---
name: component-taxonomy-selector
description: Map architecture requirements to valid DSDS component categories and component types. Use when converting system requirements into simulator node selections, resolving ambiguous type choices, and ensuring required attributes are captured before topology authoring.
---

# Component Taxonomy Selector

## Overview
Select DSDS component types from product and architecture requirements with clear reasoning and minimal ambiguity. Produce a mapping that is directly usable in topology authoring.

## Workflow

1. Extract required capabilities
- Parse functional requirements, latency targets, data consistency needs, security constraints, and operational concerns.
- Separate mandatory capabilities from optional capabilities.

2. Map requirements to DSDS categories
- Place each requirement in a category (`compute`, `network`, `storage`, `messaging`, `orchestration`, `security`, `observability`, and others).
- Keep a one-to-many mapping when uncertainty is legitimate.

3. Resolve to component types
- Choose concrete component types from the DSDS taxonomy.
- For each chosen type, include why it is selected and why alternatives are not selected.

4. Attach required attributes
- Add uniform fields needed for simulation (`id`, provider, region, resources, dependencies, health, SLO targets).
- Mark unknown values explicitly as assumptions.

5. Produce selection output
- Return category summary, selected component types, assumptions, and unresolved decisions.

## Output format
1. `Requirements summary`
2. `Category to component mapping`
3. `Required attributes per component`
4. `Assumptions and open decisions`

## References
- Read `references/taxonomy-selection-guide.md` for mapping heuristics and tie-break rules.
- Use these repo sources:
- `canonical-catalogue/DSDS Canonical Catalogue - Component taxonomy.csv`
- `canonical-catalogue/DSDS Canonical Catalogue - Uniform component attributes.csv`
- `schema/complete_simulator_schema.ts` (component unions)
