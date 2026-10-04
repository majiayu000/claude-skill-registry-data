---
name: thrunt-progress
description: Check project or hunt progress, show context, and route to the next action
allowed-tools: Read, Bash, Grep, Glob, SlashCommand
---

<objective>
Check project or hunt progress, summarize recent work and what's ahead, then intelligently route to the next action within the active hunt or THRUNT workflow.

Provides situational awareness before continuing work.
</objective>

<execution_context>
@.github/thrunt-god/workflows/progress.md
</execution_context>

<process>
Execute the progress workflow from @.github/thrunt-god/workflows/progress.md end-to-end.
Preserve the hunt-native routing plus the THRUNT utility branches and edge case handling.
</process>
