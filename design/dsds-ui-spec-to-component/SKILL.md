---
name: dsds-ui-spec-to-component
description: Convert DSDS UI specs, mock HTML screens, and system docs into concrete frontend component implementation tasks. Use when turning design references into React components, hooks, state contracts, and acceptance criteria.
---

# Dsds Ui Spec To Component

## Overview
Translate UI and UX specifications into implementation-ready component plans. Connect visual requirements to state, data contracts, and testable acceptance criteria.

## Workflow

1. Inventory source specs
- Read UI behavior from system docs and mock screens.
- Identify phase-specific interactions (BUILD, SIMULATE, ANALYSE).

2. Decompose into components
- Break each screen into reusable components and containers.
- Define component responsibilities and boundaries.

3. Define data and state contracts
- Map each UI element to state sources, worker messages, and topology fields.
- Define props, events, and store selectors.

4. Define implementation tickets
- Produce tasks with file targets, dependencies, and acceptance criteria.
- Include edge cases and accessibility constraints.

5. Deliver build plan
- Provide sequence for incremental delivery and integration checks.

## Output format
1. `Screen-to-component mapping`
2. `State and data contract mapping`
3. `Implementation ticket list`
4. `Acceptance criteria`
5. `Integration and QA checklist`

## References
- Read `references/ui-implementation-mapping.md` for decomposition checklist.
- Use these repo sources:
- `docs/SYSTEM_OVERVIEW.md`
- `planning/TICKETS.md` (UI phases and hooks)
- `stitch_simulation_output_analysis/*/code.html`
