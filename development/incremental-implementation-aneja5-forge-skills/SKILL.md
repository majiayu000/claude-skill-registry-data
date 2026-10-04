---
name: incremental-implementation
description: Use when .forge/tasks.yaml exists and implementation is starting, when executing a planned task list one task at a time, when a feature must ship in independently-verifiable slices, or when contracts in .forge/contracts/ need to be implemented against acceptance criteria.
---

# Incremental Implementation

## Overview

Pick the next ready task from `.forge/tasks.yaml`, load its contracts from `.forge/contracts/`, implement using `tdd` discipline (red-green-refactor), verify against acceptance criteria, commit, and mark done. Repeat until all tasks are complete.

## When to Use

- `.forge/tasks.yaml` exists with at least one unstarted task
- Dependencies for the next task are complete
- Ready to write code (not planning, not designing)

## When NOT to Use

- No task plan exists — run `planning-and-task-breakdown` first
- Architecture is unclear — run `architecture-and-contracts` first
- Task is XL and not decomposed — spike first, then plan

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "I'll implement a few tasks together to go faster" | Mixing tasks blurs acceptance criteria and commit history |
| "I don't need to read the contract — I know the interface" | Contracts encode invariants and error types you'll miss |
| "I'll write tests after the implementation is working" | Then you're testing implementation, not behavior |
| "This small extra thing is obviously correct to add" | Scope creep is always "obviously correct" in the moment |
| "I'll commit everything at the end" | Atomic commits per task make revert and review tractable |

## Red Flags

- Implementing a task that has unsatisfied dependencies in `tasks.yaml`
- Writing code that touches modules not listed in the task's `files_likely_affected`
- Skipping the contract read — implementing to an assumed interface
- Committing with a message that doesn't reference the task ID
- Acceptance criteria not verifiable after implementation
- Task marked done before verification step passes
- `.forge/tasks.yaml` not updated mid-flight when a task is split or blocked (the plan diverges silently)
- Editing `.forge/contracts/<X>.md` inline when build reveals the contract is wrong (file `/feedback` instead)
- Skipping `skills:` tag reads — implementing UI without loading `design-system`, writing migrations without loading `database-design`

## Core Process

### Step 1: Select the next task

Read `.forge/tasks.yaml`. Find all tasks where `status: pending` (or unset) AND every task in `depends_on` has `status: done`. Pick the highest-priority unblocked task (or ask the user if multiple are ready).

Immediately mark the selected task in place:
- `status: in_progress`
- `started_at: <ISO 8601 UTC with Z>`

Write the file back. The mutation is per-task — do not rewrite the whole `tasks.yaml`. Re-emit only the `forge:meta` `generated_at`/`content_hash` if the file as a whole was touched (status flips count); the `depends_on` set does not change.

### Step 2: Load context

Read the task's acceptance criteria and verification steps. Read each contract listed in the task's `contracts` field from `.forge/contracts/`. Load only the `files_likely_affected` — don't read the whole codebase.

**Skill-tagged context load (#41):** if the task has a `skills:` field (e.g., `[design-system, accessibility, api-design]`), read `skills/<each>/SKILL.md` BEFORE writing the first test. These tags exist precisely because the task touches a domain whose rules are encoded in another skill. Skipping them means the implementation will recreate problems those skills exist to prevent.

If `.forge/testing-strategy.md` exists, also read it — per-module coverage decisions there override TDD defaults.

### Step 3: Implement with TDD

Follow the `tdd` skill. For this task's acceptance criteria:

```
RED:   Write a failing test for the first acceptance criterion
GREEN: Write minimum code to make it pass
REPEAT for each acceptance criterion
REFACTOR: Clean up while keeping all tests green
```

Stay within the task's scope. Do not add features not in the acceptance criteria. Do not touch files outside `files_likely_affected` without explicit reason.

### Step 4: Verify

Run the verification steps listed in the task. All must pass:
- Unit tests green
- Integration tests green (if listed)
- Manual verification step confirmed (if listed)

### Step 5: Commit

```
git add <files>
git commit -m "[T001] <task title>

- Implements: <acceptance criterion 1>
- Implements: <acceptance criterion 2>
- Tests: <what the tests verify>"
```

### Step 6: Mark done

Update `.forge/tasks.yaml` in place:
- `status: done`
- `completed_at: <ISO 8601 UTC with Z>`
- `commit: <short sha of the commit from Step 5>`

Check if any tasks whose `depends_on` is now fully satisfied. Report progress to user.

### Step 7: Mid-task discoveries — split, block, or feedback

If during Steps 2-4 you discovered the task can't complete as-scoped, do NOT silently continue. Update `.forge/tasks.yaml` and (if upstream is wrong) file a feedback entry:

- **Scope creep discovered** → split the task. Mark the original `status: split`. Append new task IDs into the `notes` array describing the split. Add new task entries for the carved-out work. Do not implement the carved-out work in this run.
- **Unmet dependency surfaced** → set `status: blocked`. Append the blocker to `notes`. Stop work on this task. Pick the next ready task.
- **The CONTRACT is wrong** (refund endpoint missing, wrong type, missing error case) → run `/feedback` to file `.forge/feedback/<timestamp>-build.md` targeting the broken contract. Do NOT edit the contract inline. Mark the task `status: blocked` with `notes` referencing the feedback entry path. The contract update happens via `/architect` re-run.
- **The TEST STRATEGY contradicts what you need to write** → file `/feedback` targeting `.forge/testing-strategy.md`. Continue per the strategy's current text for now.

After ≥3 such events in a sprint, `forge-sync` will flag `TASKS_DIVERGED` — at that point, run `/plan` to re-baseline before picking the next task.

## Verification

Before marking any task done:

- [ ] Task started: `status: in_progress` + `started_at` set when work began
- [ ] All `skills:` tags read (if any listed) BEFORE first test was written
- [ ] `.forge/testing-strategy.md` consulted if it exists
- [ ] All acceptance criteria in tasks.yaml satisfied
- [ ] All verification steps in tasks.yaml passed
- [ ] No files touched outside the task's scope (or explicitly justified)
- [ ] Contract invariants not violated (check against `.forge/contracts/`)
- [ ] Tests verify behavior through public interface, not implementation details
- [ ] Commit message references task ID
- [ ] `.forge/tasks.yaml` updated: `status: done`, `completed_at`, `commit` (short sha)
- [ ] If mid-flight discoveries occurred: split tasks were added, OR a feedback entry was filed, OR the task was marked blocked with a reason — never silently absorbed
