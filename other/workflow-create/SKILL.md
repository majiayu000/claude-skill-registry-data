---
name: workflow-create
description: Create reusable workflow templates with steps, conditions, and parallel execution
argument-hint: "<name> [--steps N]"
allowed-tools: mcp__claude-flow__workflow_create mcp__claude-flow__workflow_template mcp__claude-flow__workflow_list mcp__claude-flow__workflow_status mcp__claude-flow__workflow_delete Bash
---

# Workflow Create

Create reusable workflow templates for automated task execution.

## When to use

When you have a repeatable multi-step process (CI/CD, onboarding, release, review) that should be codified as a workflow.

## Steps

1. **List templates** — call `mcp__claude-flow__workflow_template` to see available workflow templates
2. **Create workflow** — call `mcp__claude-flow__workflow_create` with steps, conditions, and execution order
3. **List workflows** — call `mcp__claude-flow__workflow_list` to see all defined workflows
4. **Check status** — call `mcp__claude-flow__workflow_status` to monitor a workflow
5. **Clean up** — call `mcp__claude-flow__workflow_delete` to remove unused workflows

## Workflow features

- Sequential and parallel step execution
- Conditional branching based on step outcomes
- Template inheritance for common patterns
- Pause/resume for manual approval gates
