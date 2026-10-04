---
name: thrunt-next
description: Automatically advance to the next logical step in the active hunt or THRUNT workflow
allowed-tools: Read, Bash, Grep, Glob, SlashCommand
---

<objective>
Detect the current project or hunt state and automatically invoke the next logical workflow step.
No arguments needed — reads `STATE.md`, `MISSION.md`, `HUNTMAP.md`, and phase directories to determine what comes next.

Designed for rapid multi-project workflows where remembering which phase/step you're on is overhead.
</objective>

<execution_context>
@.github/thrunt-god/workflows/next.md
</execution_context>

<process>
Execute the next workflow from @.github/thrunt-god/workflows/next.md end-to-end.
</process>
