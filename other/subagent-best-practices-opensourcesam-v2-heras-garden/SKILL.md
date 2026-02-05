---
name: subagent-best-practices
description: Auto-injects subagent delegation best practices when agents, subagents, Task tool, or parallel execution is mentioned.
---

# Subagent Best Practices

Auto-inject when: User mentions "subagent", "Task tool", "spawn agent", "parallel"

## Core Principle: Main Agent = Orchestrator ONLY

Main agents should NOT:
- Run Grep/Glob/Bash (delegate to subagents)
- Read files directly (ask subagents to extract info)

Main agents SHOULD:
- Decompose task into independent subtasks
- Spawn subagents with specific prompts
- Aggregate and synthesize results

## Task Decomposition Pattern

Step 1: Break task into independent chunks
Step 2: Ensure parallel independence
Step 3: Define clear deliverables

## Subagent Prompt Template

```
You are Subagent {N} tasked with:
{Specific subtask description}
Search scope: {directories/files}
Output format: {table/list/JSON}
Return ONLY specified output format.
```

## Quick Reference

Before spawning: Can I decompose? Clear deliverables? Parallel independence?
When spawning: Specific prompts, defined scope, single message (parallel)
After spawning: Aggregate WITHOUT re-running, make decisions from reports

[Codex - 2026-01-24]
