---
name: parallel-subagent-driven-development
description: Use when executing decomposed plans with parallel batches - dispatches up to 2 fresh subagents per batch with code review between batches, enabling fast parallel iteration with quality gates
---

# Parallel Subagent-Driven Development

Execute decomposed plan by dispatching fresh subagent(s) per batch (up to 2 parallel), with code review after each batch.

**Core principle:** Fresh subagent per task + up to 2 parallel when safe + review between batches = high quality, fast iteration

## Overview

**vs. Subagent-Driven Development:**
- Same process, but runs up to 2 subagents in parallel when tasks are independent
- Uses manifest.json to know which tasks can run together
- Reviews both implementations together
- Everything else identical

**vs. Executing Plans:**
- Same session (no context switch)
- Fresh subagent per task (no context pollution)
- Parallel execution when safe (faster)
- Code review after each batch (catch issues early)
- Faster iteration (no human-in-loop between tasks)

**When to use:**
- After running decomposing-plans (which created manifest.json)
- Staying in this session
- Want parallel execution with quality gates

**When NOT to use:**
- Plan not decomposed yet (run decomposing-plans first)
- Need to review plan first (use executing-plans)
- Tasks are tightly coupled (manual execution better)
- Plan needs revision (brainstorm first)

## Prerequisites

**REQUIRED:** Must have run decomposing-plans skill first to create:
- Individual task files: `docs/plans/tasks/<plan-name>/<feature>-task-NN.md`
- Manifest file: `docs/plans/tasks/<plan-name>/<feature>-manifest.json`

Where `<plan-name>` is the full plan filename (e.g., `2025-01-18-user-auth`)

## The Process

### 1. Load Manifest

Read manifest file from `docs/plans/tasks/<feature>-manifest.json`.

Create TodoWrite with all batches:
```
- [ ] Execute batch 1 (tasks X, Y)
- [ ] Review batch 1
- [ ] Execute batch 2 (task Z)
- [ ] Review batch 2
...
```

### 2. Execute Batch with Subagent(s)

For each batch in `parallel_batches` array:

**If batch has 1 task:**

Dispatch fresh subagent (same as original):
```
Task tool (general-purpose):
  description: "Implement Task N: [task name]"
  prompt: |
    You are implementing Task N from the decomposed plan.

    Read the task file: docs/plans/tasks/<plan-name>/<feature>-task-NN.md

    Your job is to:
    1. Read that task file carefully
    2. Implement exactly what the task specifies
    3. Write tests (following TDD if task says to)
    4. Verify implementation works
    5. Commit your work
    6. Report back

    Work from: [directory]

    Report: What you implemented, what you tested, test results, files changed, any issues
```

**If batch has 2 tasks:**

Dispatch TWO fresh subagents IN SINGLE MESSAGE (parallel execution):

```
<function_calls>
  <invoke name="Task">
    <parameter name="subagent_type">general-purpose</parameter>
    <parameter name="description">Implement Task N: [task name]</parameter>
    <parameter name="prompt">
You are implementing Task N from the decomposed plan.

Read the task file: docs/plans/tasks/<plan-name>/<feature>-task-NN.md

Your job is to:
1. Read that task file carefully
2. Implement exactly what the task specifies
3. Write tests (following TDD if task says to)
4. Verify implementation works
5. Commit your work
6. Report back

Work from: [directory]

Report: What you implemented, what you tested, test results, files changed, any issues
    </parameter>
  </invoke>
  <invoke name="Task">
    <parameter name="subagent_type">general-purpose</parameter>
    <parameter name="description">Implement Task M: [task name]</parameter>
    <parameter name="prompt">
You are implementing Task M from the decomposed plan.

Read the task file: docs/plans/tasks/<plan-name>/<feature>-task-MM.md

Your job is to:
1. Read that task file carefully
2. Implement exactly what the task specifies
3. Write tests (following TDD if task says to)
4. Verify implementation works
5. Commit your work
6. Report back

Work from: [directory]

Report: What you implemented, what you tested, test results, files changed, any issues
    </parameter>
  </invoke>
</function_calls>
```

**CRITICAL:** Both Task tools in SINGLE message = true parallel execution.

**Subagent(s) report back** with summary of work.

### 3. Review Subagent's Work

**Get git SHAs:**
- BASE_SHA: commit before batch started
- HEAD_SHA: current commit after batch

**Dispatch code-reviewer subagent:**

**If batch had 1 task:**
```
Task tool (superpowers:code-reviewer):
  Use template at requesting-code-review/code-reviewer.md

  WHAT_WAS_IMPLEMENTED: [from subagent's report]
  PLAN_OR_REQUIREMENTS: Task N from docs/plans/tasks/<plan-name>/<feature>-task-NN.md
  BASE_SHA: [commit before batch]
  HEAD_SHA: [current commit]
  DESCRIPTION: [task summary]
```

**If batch had 2 tasks:**
```
Task tool (superpowers:code-reviewer):
  Use template at requesting-code-review/code-reviewer.md

  WHAT_WAS_IMPLEMENTED: |
    Task N: [from subagent 1's report]
    Task M: [from subagent 2's report]

  PLAN_OR_REQUIREMENTS: |
    Task N: docs/plans/tasks/<plan-name>/<feature>-task-NN.md
    Task M: docs/plans/tasks/<plan-name>/<feature>-task-MM.md

  BASE_SHA: [commit before batch]
  HEAD_SHA: [current commit]
  DESCRIPTION: Batch with tasks N and M - [summary of both]
```

**Code reviewer returns:** Strengths, Issues (Critical/Important/Minor), Assessment

**Important:** When reviewing 2 tasks, code-reviewer also checks:
- No conflicts between the two implementations
- Proper integration if tasks interact
- Consistent code style across both

### 4. Apply Review Feedback

**If issues found:**
- Fix Critical issues immediately
- Fix Important issues before next batch
- Note Minor issues

**Dispatch follow-up subagent if needed:**

**If issues in 1 task:**
```
Task tool (general-purpose):
  description: "Fix issues from code review in Task N"
  prompt: |
    Fix issues from code review for Task N.

    Issues to fix: [list issues]

    Original task: docs/plans/tasks/<feature>-task-NN.md

    Fix the issues, verify tests pass, commit, report back.
```

**If issues in both tasks:**
```
<function_calls>
  <invoke name="Task">
    <parameter name="subagent_type">general-purpose</parameter>
    <parameter name="description">Fix issues in Task N</parameter>
    <parameter name="prompt">
Fix issues from code review for Task N.

Issues to fix: [list issues for task N]

Original task: docs/plans/tasks/<plan-name>/<feature>-task-NN.md

Fix the issues, verify tests pass, commit, report back.
    </parameter>
  </invoke>
  <invoke name="Task">
    <parameter name="subagent_type">general-purpose</parameter>
    <parameter name="description">Fix issues in Task M</parameter>
    <parameter name="prompt">
Fix issues from code review for Task M.

Issues to fix: [list issues for task M]

Original task: docs/plans/tasks/<plan-name>/<feature>-task-MM.md

Fix the issues, verify tests pass, commit, report back.
    </parameter>
  </invoke>
</function_calls>
```

### 5. Update Manifest and Mark Complete

**Update manifest.json:**
- Set task status to "done"
- Add "completed_at" timestamp

**Mark batch complete in TodoWrite**
- Check off batch execution
- Check off batch review

Move to next batch, repeat steps 2-5.

### 6. Final Review

After all batches complete, dispatch final code-reviewer:
```
Task tool (superpowers:code-reviewer):
  Use template at requesting-code-review/code-reviewer.md

  WHAT_WAS_IMPLEMENTED: [summary of ALL tasks from manifest]
  PLAN_OR_REQUIREMENTS: Original plan file + all task files
  BASE_SHA: [initial commit before all work]
  HEAD_SHA: [current commit after all work]
  DESCRIPTION: Complete implementation of [feature name]
```

**Final reviewer:**
- Reviews entire implementation
- Checks all plan requirements met
- Validates overall architecture
- Checks integration between all tasks

### 7. Complete Development

After final review passes:
- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- **REQUIRED SUB-SKILL:** Use superpowers:finishing-a-development-branch
- Follow that skill to verify tests, present options, execute choice

## Example Workflow

```
You: I'm using Parallel Subagent-Driven Development to execute this decomposed plan.

[Load manifest, create TodoWrite with batches]

Batch 1 (Tasks 1 & 2 - parallel):

[Dispatch 2 implementation subagents IN SINGLE MESSAGE]
Subagent 1: Implemented user model with tests, 5/5 passing
Subagent 2: Implemented logger with tests, 3/3 passing

[Get git SHAs, dispatch code-reviewer]
Reviewer:
  Strengths: Both well-tested, clean separation
  Issues: None
  Ready.

[Update manifest: tasks 1,2 done]
[Mark Batch 1 complete]

Batch 2 (Task 3 - sequential):

[Dispatch 1 implementation subagent]
Subagent: Added user validation, 8/8 tests passing

[Dispatch code-reviewer]
Reviewer:
  Strengths: Good validation logic
  Issues (Important): Missing edge case for empty email

[Dispatch fix subagent]
Fix subagent: Added empty email check, test added, passing

[Verify fix, update manifest: task 3 done]
[Mark Batch 2 complete]

Batch 3 (Tasks 4 & 5 - parallel):

[Dispatch 2 implementation subagents IN SINGLE MESSAGE]
Subagent 1: Implemented API endpoint, 6/6 passing
Subagent 2: Implemented CLI command, 4/4 passing

[Dispatch code-reviewer]
Reviewer:
  Strengths: Both implementations solid
  Issues: None
  Ready.

[Update manifest: tasks 4,5 done]
[Mark Batch 3 complete]

[After all batches]
[Dispatch final code-reviewer]
Final reviewer: All requirements met, no integration issues, ready to merge

Done! Using finishing-a-development-branch...
```

## Advantages

**vs. Original Subagent-Driven Development:**
- 40% faster for parallelizable tasks (2 tasks in time of 1)
- 90% less context per subagent (task file vs monolithic plan)
- Same quality gates (review after each batch)
- Same fresh context per task

**vs. Manual execution:**
- Subagents follow TDD naturally
- Fresh context per task (no confusion)
- Parallel when safe (faster)

**vs. Executing Plans:**
- Same session (no handoff)
- Continuous progress (no waiting)
- Parallel execution (faster)
- Review checkpoints automatic

**Cost:**
- More subagent invocations
- But catches issues early (cheaper than debugging later)
- Parallel execution saves wall-clock time

## Red Flags

**Never:**
- Skip code review between batches
- Proceed with unfixed Critical issues
- Skip decomposing-plans (must have manifest.json)
- Manually execute tasks from monolithic plan
- Dispatch 3+ parallel subagents (max is 2)

**If subagent fails task:**
- Dispatch fix subagent with specific instructions
- Don't try to fix manually (context pollution)

**If both parallel subagents fail:**
- Fix one at a time with follow-up subagents
- Or dispatch 2 fix subagents in parallel if issues are independent

## Integration

**Required prerequisite:**
- **decomposing-plans** - REQUIRED: Creates manifest.json and task files that this skill uses

**Required workflow skills:**
- **writing-plans** - REQUIRED BEFORE decomposing-plans: Creates the monolithic plan
- **requesting-code-review** - REQUIRED: Review after each batch (see Step 3)
- **finishing-a-development-branch** - REQUIRED: Complete development after all batches (see Step 7)

**Subagents must use:**
- **test-driven-development** - Subagents follow TDD for each task

**Alternative workflow:**
- **subagent-driven-development** - Use for monolithic plans (no parallelization)
- **executing-plans** - Use for parallel session instead of same-session execution

See code-reviewer template: requesting-code-review/code-reviewer.md

## Manifest Status Tracking

Update manifest.json after each batch:

```json
{
  "tasks": [
    {
      "id": 1,
      "status": "done",
      "completed_at": "2025-01-18T10:30:00Z"
    },
    {
      "id": 2,
      "status": "done",
      "completed_at": "2025-01-18T10:30:00Z"
    },
    {
      "id": 3,
      "status": "in_progress"
    }
  ]
}
```

This allows resuming if interrupted and tracking overall progress.
