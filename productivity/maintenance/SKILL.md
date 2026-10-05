---
name: maintenance
description: "Periodic housekeeping and session lifecycle management. Use when performing cleanup, pruning, or session commands."
when_to_use: "clear state, purge cache, clean worktrees, housekeeping, maintenance, cleanup, list sessions, inbox check, broadcast message, session lifecycle"
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep"]
argument-hint: "[--clear-state|--purge-cache|--clean-worktrees|--all|session list|session inbox|session broadcast]"
user-invocable: true
model: sonnet
---

# Maintenance

Periodic housekeeping skill for Harness projects. Handles stale state
file removal, plugin cache purging, and orphaned worktree cleanup.

## Quick Reference

| Subcommand | What It Does |
|------------|-------------|
| `--clear-state` | Remove stale files from `.claude/state/` |
| `--purge-cache` | Clear the plugin cache from `~/.claude/plugins/cache/` |
| `--clean-worktrees` | Remove git worktrees with no associated branch |
| `--all` | Run all of the above in sequence |

## When to Use

Run `/maintenance` when any of the following apply:

- `.claude/state/` contains `loop-active.json` but no loop is running
- Old sprint contracts from completed phases are cluttering `.claude/state/contracts/`
- `git worktree list` shows entries for branches that have been deleted
- The plugin cache has grown stale after a Harness version upgrade

## Operations

### --clear-state

Scans `.claude/state/` and removes files that are safe to delete:

- `loop-active.json` — only if no Breezing/harness-work loop is currently running
- Sprint contract files (`*.sprint-contract.json`) for tasks marked `cc:Done` in Plans.md
- Stale `review-result.json` files older than 7 days

**Will not touch**: Active loop state, pending fix proposals, or the `contracts/` directory itself.

### --purge-cache

Removes the plugin cache directory at `~/.claude/plugins/cache/`. The cache is rebuilt
automatically on next plugin load. Use after a major Harness version upgrade if stale
cached files are causing unexpected behavior.

### --clean-worktrees

Lists all git worktrees (`git worktree list`) and removes entries where the associated
branch no longer exists in the repository.

Safe: uses `git worktree remove --force` only on worktrees confirmed to have no live branch.

## Safety Guarantees

- All operations print a dry-run summary before making changes
- Destructive operations (`--purge-cache`) require explicit confirmation
- Operations never touch files outside their defined scope
- The main working tree is never modified

## Execution Details

See [`${CLAUDE_SKILL_DIR}/references/cleanup.md`](${CLAUDE_SKILL_DIR}/references/cleanup.md)
for step-by-step execution procedures for each subcommand.

---

## Session Lifecycle

Consolidates session-related subcommands: listing, inbox checks, and broadcasting.

| User Input | Behavior |
|------------|----------|
| `session list` | Show all active Claude Code sessions in the current project |
| `session inbox` | Check for incoming messages from other sessions |
| `session broadcast "message"` | Send a message to all active sessions |

### `session list`

Shows all active Claude Code sessions in the current project.

```
Active Sessions

| Session ID | Status | Last Activity |
|------------|--------|---------------|
| abc123     | active | 2 min ago     |
| def456     | idle   | 15 min ago    |
```

### `session inbox`

Checks for incoming messages from other sessions.

```
Session Inbox

| From   | Time    | Message            |
|--------|---------|---------------------|
| abc123 | 5m ago  | "Ready for review"  |
```

### `session broadcast "message"`

Sends a message to all active sessions.

For memory optimization, session lifecycle details, and state transitions, see:
- [`references/session-control.md`](${CLAUDE_SKILL_DIR}/references/session-control.md)
- [`references/memory-optimization.md`](${CLAUDE_SKILL_DIR}/references/memory-optimization.md)
- [`references/execution-flow.md`](${CLAUDE_SKILL_DIR}/references/execution-flow.md)

---

## Related Skills

- `harness-plan archive` — Archive completed phases from Plans.md (not the same as maintenance)
- `harness-work` — Implementation; run maintenance before long breezing sessions
