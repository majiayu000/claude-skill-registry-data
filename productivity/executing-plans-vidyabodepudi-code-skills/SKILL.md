---
name: executing-plans
description: >
  Coordinate the execution of approved implementation plans across
  sessions. Track progress, handle deviations, and maintain momentum.
  Use when working through a multi-task plan.
version: 1.0.0
permissions:
  - fs.read
  - fs.write
  - shell.exec
triggers:
  - context: "executing an implementation plan"
  - context: "working through a task list"
  - command: "/build"
platforms:
  - claude-code
  - cursor
  - gemini-cli
  - copilot
  - codex
  - opencode
  - windsurf
  - kiro
dependencies:
  - planning-and-task-breakdown@^1.0.0
  - incremental-implementation@^1.0.0
model_variants:
  claude:
    enforcement_style: "human-partner collaborative"
  gemini:
    enforcement_style: "structured-checklist"
  gpt:
    enforcement_style: "directive-imperative"
author: codehands-core
signed: true
tier: 1
---

## Overview

Plans are only as good as their execution. This skill coordinates working through multi-task plans, tracking progress, handling deviations, and ensuring each completed task meets quality standards before moving to the next.

## When to Use

- When executing an approved implementation plan
- When resuming work on a multi-session project
- When a plan spans multiple tasks or sessions
- NOT for single-task work (just use the individual skill directly)

## Process

### 1. Load the Plan

At the start of each session:
1. Read the plan file: `docs/plans/<plan>.md`
2. Identify which tasks are complete, in progress, and pending
3. Verify completed tasks still pass their tests

### 2. Execute Each Task

For each task in dependency order:

```
Mark task as IN PROGRESS
→ Read task description + relevant files
→ Follow codehands:test-driven-development
→ Follow codehands:incremental-implementation
→ Run task verification command
→ Commit with descriptive message
→ Mark task as COMPLETE
→ Update plan file with status
```

### 3. Handle Deviations

When reality doesn't match the plan:
- **Task is larger than estimated** → Split it into subtasks. Update the plan.
- **New dependency discovered** → Add the dependency task. Update the plan.
- **Requirement is unclear** → Ask the human. Don't guess.
- **Better approach discovered** → Note it. Finish the current task. Then propose a plan update.

> **Never silently deviate from the plan.** If the plan needs to change, update the plan document and inform the human.

### 4. Session Continuity

At the end of each session, update the plan with:
- Tasks completed this session
- Current progress on in-progress tasks
- Any deviations or discoveries
- What to do next

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll skip this task, it's not needed anymore" | Don't silently remove tasks. If a task is no longer needed, mark it as SKIPPED with a reason. |
| "I'll do these two tasks in a different order" | Dependency ordering exists for a reason. If you want to reorder, verify no dependencies are broken. |
| "I don't need to update the plan file" | Written state survives context resets. If you don't update the plan, the next session starts from scratch. |

## Red Flags

- Working from memory instead of the plan file
- Skipping tasks without updating the plan
- Not verifying completed tasks after context switch
- Plan file not updated at session end

## Verification

- [ ] Plan file loaded and current status understood
- [ ] Tasks executed in dependency order
- [ ] Each completed task passes its verification command
- [ ] Plan file updated with progress after each task
- [ ] Deviations documented and communicated

## See Also

- `codehands:planning-and-task-breakdown` — Creating the plan
- `codehands:incremental-implementation` — Implementing each task
- `codehands:multi-agent-orchestration` — Parallel execution
