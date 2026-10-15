---
name: Executing Plans
description: Guidance for executing approved plans sequentially with branch checks, progress tracking, and verification.
---

# Executing Plans

> Never start on main. Execute sequentially. Verify each step. Track progress.

## Triggers

- User says "execute the plan", "implement the plan", "start building"
- After `/plan` produces a plan and user approves it
- When a plan document exists and implementation is requested

## HARD GATE: Branch Check

**Before executing ANY plan**, you MUST verify:

1. You are NOT on `main` or `master` branch
2. If you are on main/master, create a feature branch first
3. Name the branch descriptively: `feature/<plan-topic>` or `fix/<plan-topic>`

```
# Check current branch
git branch --show-current

# If on main/master, create and switch:
git checkout -b feature/<descriptive-name>
```

## 3-Phase Execution

### Phase 1: Load & Review

```
1. Read the plan document or recall the plan from conversation
2. Verify each task has:
   - A clear deliverable (file path + behavior)
   - A failing test that defines "done"
   - An estimated time (2-5 minutes per task)
3. If tasks are missing tests or are too large, refine before starting
4. Confirm the plan with the user before executing
```

### Phase 2: Sequential Execution with Progress

```
For each task in order:
  1. Announce: "Starting task N/M: [description]"
  2. Follow TDD: write failing test -> make it pass -> refactor
  3. Run all tests (not just the new one) to check for regressions
  4. Announce: "Task N/M complete. Tests: X pass, Y fail"
  5. If a task fails or is blocked:
     - Stop execution
     - Report what failed and why
     - Ask user how to proceed (skip, fix, re-plan)
```

### Phase 3: Finalize

```
1. Run the full test suite
2. Run linter/type checker if applicable
3. Show summary: tasks completed, tests passing, files changed
4. Trigger verification-before-completion skill
5. Ask user: ready to commit? ready for review? need changes?
```

## Integration

- Plans come from `/plan` (RIPER Phase 3)
- Each task follows `test-driven-development` skill
- Completion uses `verification-before-completion` skill
- After execution, use `branch-finishing` skill for merge/PR
- Progress tracking uses task management when available

## Task Granularity

If any task in the plan takes more than 5 minutes:
- It's too large. Break it into subtasks.
- Each subtask should have its own test.
- Subtasks should be independently verifiable.
