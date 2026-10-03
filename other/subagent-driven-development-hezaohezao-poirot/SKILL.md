---
name: subagent-driven-development
description: "Execute plans task-by-task with two-stage review."
allowed-tools:
  - bash
  - read_file
  - write_file
  - str_replace
  - list_dir
enabled: true
related-skills: [plan, requesting-code-review, test-driven-development]
license: MIT
author: Adapted from hermes-agent (Nous Research, MIT); obra/superpowers
---

# Subagent-Driven Development

## Overview

Execute implementation plans task-by-task with systematic two-stage review
between tasks.

**Core principle:** Fresh focus per task + two-stage review (spec then quality)
= high quality, fast iteration.

> **Poirot note:** The original skill dispatches a fresh subagent per task via
> `delegate_task`. Poirot has no subagents, so this version executes tasks
> **sequentially in the same context** with a deliberate context-reset between
> tasks. The two-stage review methodology is preserved.

## When to Use

- You have an implementation plan (from the `plan` skill or user requirements)
- Tasks are mostly independent
- Quality and spec compliance are important
- You want automated review between tasks

## The Process

### 1. Read and Parse Plan

Read the plan file. Extract ALL tasks with full text and context upfront:

```
read_file(".poirot/plans/feature-plan.md")
```

Create a todo list with all tasks. Read the plan ONCE — don't re-read per task.

### 2. Per-Task Workflow

For EACH task in the plan:

#### Step 1: Context Reset

Before starting each task, deliberately reset your focus:
- Re-read only the current task's description
- Forget previous tasks' implementation details (they're committed)
- Treat each task as if a fresh agent is picking it up

#### Step 2: Implement

Follow the task's steps exactly:
1. Write the failing test (TDD — see `test-driven-development` skill)
2. Run test to verify failure
3. Write minimal implementation
4. Run test to verify pass
5. Run full test suite to check for regressions
6. Commit

```
bash("pytest tests/test_feature.py::test_name -v")
# ... implement ...
bash("pytest tests/ -q")
bash("git add -A && git commit -m 'feat: task N description'")
```

#### Step 3: Stage 1 Review — Spec Compliance

After implementation, review against the plan:
- [ ] Does the implementation match the task's stated objective?
- [ ] Are all files listed in the task created/modified?
- [ ] Are all tests listed in the task written?
- [ ] Does the implementation do what the task says, not more, not less?

**If spec compliance fails:** Fix before proceeding to Stage 2.

#### Step 4: Stage 2 Review — Code Quality

Review the committed diff for quality:
- [ ] No hardcoded secrets, credentials
- [ ] Input validation on user-provided data
- [ ] Error handling for I/O/network/DB
- [ ] No debug print/console.log left behind
- [ ] No commented-out code
- [ ] Tests cover happy path + edge cases
- [ ] Code follows project conventions

Use the `requesting-code-review` skill's checklist for thoroughness.

**If quality review fails:** Fix, re-commit, re-review.

#### Step 5: Proceed to Next Task

Only after both reviews pass:
1. Mark current task complete in the todo list
2. Move to next task
3. Repeat from Step 1 (Context Reset)

### 3. Handling Failures

**Implementation fails (tests don't pass):**
1. Use `systematic-debugging` skill to find root cause
2. Fix the root cause
3. Re-run tests
4. If 3+ fixes fail → question the approach, discuss with user

**Review fails (spec or quality):**
1. Fix the specific issues found
2. Re-commit
3. Re-review only the fixed parts

**Task is blocked (depends on unfinished work):**
1. Note the blocker
2. Skip to next independent task
3. Return to blocked task when dependency is resolved

## Two-Stage Review Detail

### Stage 1: Spec Compliance

Re-read the task from the plan. Compare against what you actually built:

```
Task says: "Create User model with email and password_hash fields"
Check:
- [ ] User model exists
- [ ] Has email field
- [ ] Has password_hash field
- [ ] No extra fields not in the task
- [ ] Test exists for the model
```

**Common spec violations:**
- Implementing more than the task asks ("while I'm here" scope creep)
- Missing a file the task lists
- Different API shape than the task specifies
- No test for the feature

### Stage 2: Code Quality

Review the `git diff` for the current task:

```
bash("git diff HEAD~1 HEAD")
```

Check for security, correctness, and conventions. Use the `requesting-code-review`
skill's security scan + self-review checklist.

## Pitfalls

- **Context accumulation**: without subagents, context grows across tasks. If
  you feel confused about which task you're on, re-read the plan + current task.
- **Scope creep**: "while I'm here" edits to previous tasks' code. Don't.
  Each task is atomic.
- **Skipping review**: the two-stage review IS the value of this skill. Without
  it, you're just implementing sequentially.
- **Re-reviewing everything**: after a fix, only re-review the fixed parts,
  not the entire task.
- **Forgetting to commit**: commit after each task. Don't accumulate uncommitted
  changes across tasks — if a later task breaks, you can't cleanly revert.
