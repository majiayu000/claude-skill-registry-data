---
name: multi-agent-orchestration
description: >
  Multi-agent orchestration covering strategy, dispatch, context isolation,
  conflict avoidance, progress tracking, and two-stage review gates. Use
  when splitting work across multiple concurrent agent sessions.
version: 1.0.0
permissions:
  - fs.read
  - fs.write
  - shell.exec
triggers:
  - context: "task has multiple independent subtasks"
  - context: "parallel implementation would be faster"
  - context: "dispatching to multiple agents"
platforms:
  - claude-code
  - cursor
  - gemini-cli
  - codex
  - kiro
dependencies:
  - planning-and-task-breakdown@^1.0.0
  - code-review-and-quality@^1.0.0
model_variants:
  claude:
    enforcement_style: "human-partner collaborative"
  gemini:
    enforcement_style: "structured-checklist"
  gpt:
    enforcement_style: "directive-imperative"
author: codehands-core
signed: true
tier: 2
---

## Overview

Multi-agent orchestration splits work across agents for parallel execution. The orchestrating agent identifies parallelizable tasks, dispatches with focused context and clear boundaries, tracks progress, and reviews all output through a two-stage quality gate. Every subagent output is untrusted until reviewed.

## When to Use

- When a plan has 3+ independent tasks that can run in parallel
- When tasks touch separate files/modules with no overlap
- When the platform supports subagent dispatch
- NOT for tightly coupled or sequential tasks

## Process

### 1. Identify Parallelizable Work

From the approved plan, find tasks that:
- Touch different files (no merge conflicts)
- Have no data dependencies on each other
- Can be verified independently

### 2. Write Subagent Prompts

Each subagent receives ONLY what it needs:

```markdown
## Task
[Specific task from the plan]

## Context
[Only the files and patterns relevant to this task]

## Requirements
- [Specific behavior to implement]
- Write tests following DAMP naming
- Follow existing patterns in [file]

## Constraints
- Do NOT modify files outside [scope]
- Do NOT add new dependencies

## Verification
Run: [specific test command]
Expected: [specific outcome]
```

### 3. Pre-Dispatch Checklist

- [ ] All tasks have explicit file boundaries (no overlapping writes)
- [ ] Each task has its own verification command
- [ ] Integration test exists to verify combined output
- [ ] Base branch is clean and all existing tests pass

### 4. Track Progress

```markdown
## Dispatch Log
| Agent | Task | Status | Files | Verification |
|---|---|---|---|---|
| Agent-1 | User model | ✅ Done | src/models/user.ts | `npm test -- user` |
| Agent-2 | Auth service | 🔄 Active | src/services/auth.ts | `npm test -- auth` |
```

### 5. Review & Integrate

**Every subagent output goes through two-stage review** (`codehands:code-review-and-quality`):
1. Spec compliance — does it match the task?
2. Code quality — does it meet standards?

> **NEVER auto-merge subagent output.** Merge one at a time, run full tests after each.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The subtasks are simple, I don't need to review them" | Simple code can still have subtle bugs. Review everything. |
| "I'll give the subagent the whole codebase" | Too much context degrades output. Give only what's needed. |
| "I'll merge all outputs at once" | Sequential merge catches conflicts early. Bulk merge hides the source of breakage. |

## Red Flags

- Two agents modifying the same file
- Subagent given entire codebase as context
- Output merged without review
- No dispatch log or progress tracking

## Verification

- [ ] Tasks are independent (no shared files, no data dependencies)
- [ ] Each subagent prompt includes only relevant context
- [ ] Every subagent output reviewed via two-stage pipeline
- [ ] Outputs merged one at a time with tests after each
- [ ] Full integration test passes after all merges

## See Also

- `codehands:planning-and-task-breakdown` — Create the parallelizable plan
- `codehands:executing-plans` — Sequential plan execution
- `codehands:code-review-and-quality` — Review pipeline for subagent output
