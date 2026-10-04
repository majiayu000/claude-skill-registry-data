---
name: hunt-map-environment
description: Map available telemetry, query surfaces, tenants, retention windows, and investigation blind spots
allowed-tools: Read, Bash, Write, AskUserQuestion, Task
---

<objective>
Create or refresh the environment map for this hunt program or case.

**Creates or updates:**
- `.planning/environment/ENVIRONMENT.md`
- `.planning/MISSION.md`
- `.planning/HYPOTHESES.md`
- `.planning/STATE.md`

Unknown tenants, tools, retention windows, access paths, and blind spots must remain `TBD` until the operator confirms them.
Confirmed environment facts should replace existing `TBD` markers immediately; only unresolved fields should stay `TBD`.

**After this command:** Run `/hunt-shape-hypothesis` or `/hunt-plan 1`.
</objective>

<execution_context>
@.github/thrunt-god/workflows/hunt-map-environment.md
@.github/thrunt-god/templates/environment-map.md
</execution_context>

<process>
Execute the environment-mapping workflow from @.github/thrunt-god/workflows/hunt-map-environment.md.
Prefer concrete environment facts over generic best practices. Preserve existing analyst notes.
Default behavior is to preserve confirmed facts and leave unknown values as `TBD` rather than populating simulated environment details.
Replace `TBD` only where live workspace evidence or direct operator input confirms the fact.
</process>
