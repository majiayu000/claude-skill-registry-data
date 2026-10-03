---
name: ba
description: Task tracking. "$ba status" for current tasks, "$ba claim <id>" to start work, "$ba finish <id>" when done.
---

# ba - Task Tracking for AI Sessions

Simple, file-based task tracking. No server, no database - just files in `.ba/`.

All commands invoke the `ba` CLI. If ba is not installed, show:
```
ba not installed. Install with:
  brew tap open-horizon-labs/homebrew-tap && brew install ba
  # or: cargo install ba
```

## $ba status

Show current task status - what's ready, what's claimed, what's blocked.

```bash
ba ready && echo "" && ba mine && echo "" && ba list --status open
```

## $ba init

Initialize task tracking for this project.

```bash
ba init
```

## $ba claim <id>

Claim a task to start working on it.

```bash
ba claim <id>
```

## $ba finish <id>

Mark a task as complete (releases claim and closes).

```bash
ba finish <id>
```

## $ba create <title>

Create a new task.

```bash
ba create "<title>"
```

## $ba ready

Show tasks that are ready to work on (open and not blocked).

```bash
ba ready
```

## $ba list

List all tasks with optional filters.

```bash
ba list                    # All tasks
ba list --status open      # Open tasks only
ba list --status closed    # Closed tasks only
ba list --label <label>    # Tasks with specific label
```

## $ba show <id>

Show details of a specific task including comments and blocking relationships.

```bash
ba show <id>
```

## $ba block <id> <blocker>

Mark that task <id> is blocked by task <blocker>.

```bash
ba block <id> <blocker>
```

## $ba unblock <id> <blocker>

Remove a blocking relationship.

```bash
ba unblock <id> <blocker>
```

## $ba comment <id> <comment>

Add a comment to a task.

```bash
ba comment <id> "<comment>"
```

## $ba tree

Show the dependency tree of all tasks.

```bash
ba tree
```

## $ba quickstart

Show the quick start guide for using ba.

```bash
ba quickstart
```

---

## Workflow

Typical task workflow:

1. **Check what's ready:** `$ba status` or `$ba ready`
2. **Claim a task:** `$ba claim <id>`
3. **Do the work**
4. **Add comments if needed:** `ba comment <id> "progress note"`
5. **Finish when done:** `$ba finish <id>`

**Protocol:** Always track non-trivial work. If a task has multiple steps or will take >5 minutes, create a task.
