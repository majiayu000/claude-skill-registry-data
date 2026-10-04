---
name: hunt-plan
description: Create phase plans for a threat hunt with exact telemetry tasks, receipts, and query outputs
argument-hint: "<phase>"
allowed-tools: Read, Bash, Write, Task
---

<objective>
Plan a hunt phase from the current HUNTMAP.

`HUNTMAP.md` remains the source of truth for phase layout and sequencing.

**Creates or updates:**
- `.planning/phases/[phase-slug]/`
- `CONTEXT.md`
- `PLAN.md` files
- `.planning/STATE.md`
- `.planning/HUNTMAP.md` when phase metadata changes

**After this command:** Run `/hunt-run <phase>`.
</objective>

<execution_context>
@.github/thrunt-god/workflows/hunt-plan.md
@.github/thrunt-god/templates/context.md
@.github/thrunt-god/templates/phase-prompt.md
</execution_context>

<process>
Execute the hunt planning workflow from @.github/thrunt-god/workflows/hunt-plan.md.
Plans must name the telemetry source, intended evidence, and required receipts.
</process>
