---
name: using-task-list
description: Use when deciding whether to TaskCreate. Tasks track multi-step work — don't open one for trivial single-step jobs.
---

# Using Task List — Track Multi-Step Work

`TaskCreate` / `TaskList` / `TaskGet` / `TaskUpdate` are for tracking work the user can see and inspect. They are not a notebook, not a reminder system, not a substitute for actually doing the work.

## Iron Law

**A task is a unit the user could verify independently.** "Read the file" is not a task. "Refactor the auth module so tests pass" is. If you can't imagine the user asking "is task #3 done?", it shouldn't be a task.

## When to TaskCreate

Yes:
- 3+ truly distinct steps that span time or files
- Cross-file refactor, feature implementation, debug-and-fix loops
- Work where mid-flight reporting helps the user steer
- Plan-mode output (one task per plan step)

No:
- 1-2 step jobs ("read X, summarize" — just do it)
- Pure exploration / Q&A
- User wants an immediate answer ("what does this function do?")
- You're about to do it in the next 10 seconds anyway

When uncertain: **don't**. Over-tasking is more annoying than under-tasking.

## Status Workflow — MUST

```
pending  →  in_progress  →  completed
```

- Set `in_progress` **immediately before starting** the task. Not "I'll set it when I'm done with the previous one" — right when you begin.
- Set `completed` **immediately on finishing**. Don't batch 5 completions at the end of the session.
- Only one `in_progress` at a time (usually). If you genuinely paused one to do another, that's fine, but rare.
- Never mark `completed` if:
  - Tests are failing
  - Implementation is partial
  - You hit an error you couldn't resolve
  - You skipped a sub-step

If blocked, leave `in_progress` and TaskCreate a new task describing the blocker.

## Before Creating — Check Existing

When the user gives new requirements, **call `TaskList` first**. Don't blindly TaskCreate 5 tasks if 3 already exist. Merge, don't duplicate.

```
1. TaskList  → see what's open
2. Decide: extend existing tasks, or genuinely new?
3. TaskCreate only the new ones
```

## Fields

- **subject**: imperative, brief — "Fix login redirect bug", "Add CSV export to /reports"
- **description**: what done looks like, with enough context that you (or another agent) could pick this up later
- **activeForm**: present continuous, shown in the spinner — "Fixing login redirect", "Adding CSV export"
- **blockedBy**: task IDs that must complete first (creates dependency)
- **blocks**: tasks waiting on this one

## Dependencies

Use `addBlockedBy` / `addBlocks` when order matters:

```
Task 1: "Add user table migration"
Task 2: "Add user API endpoint"  blockedBy: [1]
Task 3: "Add user UI"            blockedBy: [2]
```

`TaskList` shows blocked tasks so you can pick available work.

## Red Flags

- You created 3 tasks but never updated their status — task list is now a lie
- You marked completed before tests passed — you'll forget and ship the bug
- You batched 5 status updates at once at session end — the user couldn't see progress in flight
- You wrote a task but didn't reference it when you started working ("ok let me do the auth thing" instead of "starting task #2")
- You opened a task for "read README" — single step, just read it
- You used the task list as a notepad ("remember to ask user about Y") — that's not a task, that's a memory note

## Examples

### Good

User: "重构 auth 模块，现在登录/登出/会话刷新分散在 5 个文件"

```
TaskCreate("Audit current auth code — list all entry points and shared state")
TaskCreate("Design unified Auth service interface", blockedBy: [1])
TaskCreate("Migrate login to Auth service",   blockedBy: [2])
TaskCreate("Migrate logout to Auth service",  blockedBy: [2])
TaskCreate("Migrate session refresh",          blockedBy: [2])
TaskCreate("Run full test suite, fix breakage", blockedBy: [3,4,5])
```

Each is independently verifiable. Order is clear via blockedBy.

### Bad

User: "看一下 README 然后告诉我这个项目是干啥的"

```
TaskCreate("Read README")
TaskCreate("Understand project purpose")
TaskCreate("Summarize for user")
```

No. Just read it and answer. This is 30 seconds of work, not a 3-task project.

### Mid-Flight Update — Good

```
[user gives a 4-step request]
1. TaskList — none exist, ok
2. TaskCreate × 4
3. TaskUpdate task 1 → in_progress
4. ... do work ...
5. TaskUpdate task 1 → completed
6. TaskUpdate task 2 → in_progress
7. ...
```

User sees real-time progress in the spinner via `activeForm`.

### Mid-Flight Update — Bad

```
1. TaskCreate × 4
2. ... do all 4 silently ...
3. TaskUpdate 1 → completed
   TaskUpdate 2 → completed
   TaskUpdate 3 → completed
   TaskUpdate 4 → completed
```

User had no visibility. The task list provided zero value.

## Cleanup

- Finished tasks stay marked completed (they show in TaskList).
- If a task was wrong / superseded: `status: "deleted"` (permanent removal).
- Don't manually delete completed tasks just to "clean up" — the history is useful.

## See Also

- `[[using-cron]]` — for time-based reminders. Tasks don't fire on time, crons do.
- `[[writing-plans]]` — plan first, then convert plan steps to tasks.
- `[[executing-plans]]` — running tasks in batches with checkpoints.
