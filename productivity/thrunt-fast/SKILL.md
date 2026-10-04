---
name: thrunt-fast
description: Execute a trivial task inline — no subagents, no planning overhead
argument-hint: "[task description]"
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---


<objective>
Execute a trivial task directly in the current context without spawning subagents
or generating PLAN.md files. For tasks too small to justify planning overhead:
typo fixes, config changes, small refactors, forgotten commits, simple additions.

This is NOT a replacement for /thrunt-quick — use /thrunt-quick for anything that
needs research, multi-step planning, or findings validation. /thrunt-fast is for tasks
you could describe in one sentence and execute in under 2 minutes.
</objective>

<execution_context>
@.github/thrunt-god/workflows/fast.md
</execution_context>

<process>
Execute the fast workflow from @.github/thrunt-god/workflows/fast.md end-to-end.
</process>
