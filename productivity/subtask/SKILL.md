---
name: subtask
description: "Parallel task orchestration CLI that dispatches work to AI workers (via Claude Code) in isolated git workspaces. Use when the user wants to draft, create, run, or manage tasks, delegate tasks to workers/subagents, or mentions subtask or Subtask."
---

# Subtask

Subtask is a CLI for orchestrating parallel AI workers. There are three roles: the user who gives direction, you (the lead) who orchestrates and delegates, and workers who execute tasks.

Each worker runs in an isolated git worktree. They can't conflict with each other.

The user tells you what they need. You clarify requirements, break work into tasks, dispatch to workers, review their output, iterate until it's right, and merge when ready.

Prefer to delegate exploration, research and planning to workers as parts of their tasks. Workers have time & space to dig deep, whereas you should preserve context to lead. Only go into details yourself when user explicitly requested, or the situation calls for it.

## Mindset

1. **Understand before delegating** — ask questions, clarify requirements. Don't rush to create tasks until you understand what the user actually wants.
2. **Own the complexity** — stay on top of all tasks. Surface progress and blockers. Don't make the user chase status.
3. **Work autonomously** — review output, request changes, iterate with workers. Only involve the user for decisions they need to make.
4. **Ask before merging** — get user sign-off before merging. Don't merge without user approval.

## Commands

| Command | Description |
|---------|-------------|
| `subtask ask "..."` | Quick question (no task, runs in cwd) |
| `subtask draft <task> --base-branch <branch> --title "..." <<'EOF'` | Create a task |
| `subtask send <task> <prompt>` | Prompt worker on task (blocks until reply) |
| `subtask stage <task> <stage>` | Advance workflow stage |
| `subtask list` | View all tasks |
| `subtask show <task>` | View task details |
| `subtask diff [--stat] <task>` | Show changes (from merge base) |
| `subtask merge <task> -m "msg"` | Squash-merge task into base branch |
| `subtask close <task>` | Close without merging, free workspace |
| `subtask workspace <task>` | Get workspace path (a git worktree) |
| `subtask interrupt <task>` | Gracefully stop a running worker |
| `subtask log <task>` | Show task conversation and history |
| `subtask trace <task>` | Debug what a worker is doing and thinking internally |

**Tip:** Add `--follow-up <task>` on `draft` to carry forward conversation context from a prior task.

## Flow

```bash
# 1. Draft (task name is branch name, task description is shared with worker)
subtask draft fix/bug --base-branch main --title "Fix worker pool panic" <<'EOF'
There's an intermittent panic in the worker pool under high concurrency—likely a race condition in pool.go.
Reproduce, find root cause, fix, and add tests.
EOF

# 2. Start the worker
subtask send fix/bug "Go ahead."

# 3. When worker finishes, review and iterate
subtask stage fix/bug review
# Review with `subtask diff --stat fix/bug`, or read the files at `cd $(subtask workspace fix/bug)`.

# 4. Request changes if needed
subtask send fix/bug <<'EOF'
Also handle the edge case when pool is empty.
EOF

# 5. When ready, merge or close
subtask stage fix/bug ready
subtask merge fix/bug -m "Fix race condition in worker pool"
# Or if not merging: subtask close fix/bug
```

**Critical:** Use the Bash tool with `run_in_background: true` for `subtask send`. Tell the user you're waiting and stop. Don't poll or check. You'll be notified when done.

## Merging

`subtask merge` squashes all task commits into a single commit on the base branch.

```bash
subtask merge fix/bug -m "Fix race condition"
```

**If conflicts occur**, merge will fail with instructions. Follow them.

## Stages

All tasks have stages: `doing → review → ready`

| Stage | When to advance |
|-------|-----------------|
| `doing` | Worker is working (default) |
| `review` | Worker done, you're reviewing code |
| `ready` | Ready for human to decide (human review, merge, more work, etc.) |

Advance with: `subtask stage <task> <stage>`

## Planning Workflows

For complex tasks, add a plan stage: `plan → implement → review → ready`

**You plan (`--workflow you-plan`):** You draft PLAN.md in task folder, worker reviews and pokes holes.
**They plan (`--workflow they-plan`):** Worker drafts PLAN.md in task folder, you review and approve or request changes.

## Notes

- Use `subtask list` to see what’s in flight.
- Use `subtask show <task>` to see progress and details.
- Use `subtask log <task>` to see task conversation and events.
- Use `subtask trace <task>` to debug what a worker is doing and thinking internally.
