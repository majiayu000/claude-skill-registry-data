---
name: unknowns-mapper
description: separate knowns, unknowns, assumptions, and risks for a given problem frame or repository. use when a project is starting and research paths need to be defined.
---
# unknowns-mapper

Produces an **Unknowns Map** to separate what we know from what we are guessing. This skill prevents premature implementation by making the "information gaps" visible.

## Workflow
1. **Intake**: Review the Problem Frame or Repository goal.
2. **Classification**:
    - **Known**: Facts backed by code or documentation.
    - **Unknown**: Explicitly missing information.
    - **Assumed**: Beliefs treated as facts but not yet verified.
    - **Risk**: Potential failures or blockers.
3. **Pathfinding**: Define "Research Paths" to convert unknowns/assumptions into knowns.
4. **Stopping Rules**: Define when research should stop (to prevent rabbit holes).

## Output Format
Every response must follow the [Unknowns Map](references/unknowns-map-template.md) structure.

## Boundary Rule
Do not perform the research yourself. Your job is to map the gaps and define the paths, not to travel them.

## References
- [Unknowns Map Template](references/unknowns-map-template.md)
