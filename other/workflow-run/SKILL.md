---
name: workflow-run
description: Execute, pause, resume, and cancel running workflows
argument-hint: "<workflow-id>"
allowed-tools: mcp__claude-flow__workflow_execute mcp__claude-flow__workflow_run mcp__claude-flow__workflow_pause mcp__claude-flow__workflow_resume mcp__claude-flow__workflow_cancel mcp__claude-flow__workflow_status Bash
---

# Workflow Run

Execute and manage running workflows.

## When to use

When you need to run a defined workflow, monitor its progress, or control its execution (pause, resume, cancel).

## Steps

1. **Execute** — call `mcp__claude-flow__workflow_execute` or `mcp__claude-flow__workflow_run` with the workflow ID
2. **Monitor** — call `mcp__claude-flow__workflow_status` to check progress and step outcomes
3. **Pause** — call `mcp__claude-flow__workflow_pause` to halt execution at the current step
4. **Resume** — call `mcp__claude-flow__workflow_resume` to continue from where paused
5. **Cancel** — call `mcp__claude-flow__workflow_cancel` to abort the workflow

## Execution modes

- **Sequential** — steps run one after another
- **Parallel** — independent steps run concurrently
- **Conditional** — steps execute based on previous step outcomes
- **Manual gate** — pause for human approval before continuing
