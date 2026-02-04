---
name: speculator-orchestration
description: Multi-agent task orchestration using the spec CLI. Guides agents on claiming tasks, parallel execution, blocking, and coordination. Use when working with multiple agents, claiming tasks, or managing parallel work.
---

# Speculator Orchestration

## Core Principle

**Claim before you code.**

Never start work on a task without atomically claiming it first. This prevents duplicate effort and merge conflicts in multi-agent scenarios.

## Quick Reference

| Command | Purpose |
|---------|---------|
| `spec tasks ready` | Find tasks available for work (todo, unblocked, dependencies complete) |
| `spec task claim <id>` | Atomically claim a task (marks as in_progress) |
| `spec task complete <id>` | Mark a task as done |
| `spec task block <id> --reason <reason>` | Record a blocker with reason |
| `spec task unblock <id>` | Remove a block |
| `spec task release <id>` | Return a claimed task to todo |
| `spec task add --feature <id> --title <title>` | Create a new task or subtask |
| `spec task depend <id> --on <other-id>` | Add a dependency between tasks |

## Workflows

- [Claiming Tasks](workflows/claiming.md) - How to find and claim work
- [Completing Tasks](workflows/completing.md) - When and how to mark work done
- [Blocking Tasks](workflows/blocking.md) - When and how to record blockers

## Patterns

- [Parallelization](patterns/parallelization.md) - Which tasks can run concurrently
- [Decomposition](patterns/decomposition.md) - Breaking large tasks into subtasks

## Examples

- [Multi-Agent Session](examples/multi-agent-session.md) - Two agents working concurrently

## The Orchestration Loop

```
1. spec tasks ready → find available work
2. Evaluate conflicts → check for file overlap with other in-progress tasks
3. spec task claim <id> → atomically claim
4. Implement → do the work
5. spec task complete <id> | spec task block <id> --reason <reason> → finish or record blocker
6. Repeat
```

## Important Notes

- Always check `spec tasks ready` before starting work
- If claim fails, another agent got it first - move on
- Block tasks with clear, actionable reasons
- Release tasks if you can't complete them
- Create subtasks for large pieces of work
