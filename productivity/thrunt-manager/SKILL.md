---
name: thrunt-manager
description: Interactive command center for managing multiple project or hunt phases from one terminal
allowed-tools: Read, Write, Bash, Glob, Grep, AskUserQuestion, Task
---

<objective>
Single-terminal command center for managing a milestone or hunt campaign. Shows a dashboard of all phases with visual status indicators, recommends optimal next actions, and dispatches work. In hunt mode that means shape/plan/run; in THRUNT utility mode it means management, audit, and workspace flows.

Designed for power users who want to parallelize work across phases from one terminal: shape or discuss a phase while another plans or runs in the background.

**Creates/Updates:**
- No files created directly — dispatches to existing hunt or THRUNT commands and background Task agents.
- Reads `.planning/STATE.md`, `MISSION.md`, `HUNTMAP.md`, and phase directories for status.

**After:** User exits when done managing, or all phases complete and the appropriate publish/verify lifecycle is suggested.
</objective>

<execution_context>
@.github/thrunt-god/workflows/manager.md
@.github/thrunt-god/references/ui-brand.md
</execution_context>

<context>
No arguments required. Requires `MISSION.md`, `HUNTMAP.md`, and `STATE.md`.

Project context, phase list, dependencies, recommendations, and workflow mode are resolved inside the workflow using `thrunt-tools.cjs init manager`. No upfront context loading needed.
</context>

<process>
Execute the manager workflow from @.github/thrunt-god/workflows/manager.md end-to-end.
Maintain the dashboard refresh loop until the user exits or all phases complete.
</process>
