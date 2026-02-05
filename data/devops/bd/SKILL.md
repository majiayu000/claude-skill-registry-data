---
name: bd
description: Track issues and dependencies with beads (bd). Use when work spans multiple sessions, has blockers/dependencies, or needs to survive conversation compaction. Triggers - "create task", "what's ready", "show task", "track this", "what's blocking", "update status".
---

# Beads (bd) - Persistent Task Memory

Graph-based issue tracker that survives conversation compaction. Provides persistent memory for multi-session work with complex dependencies.

## When to Use bd vs TodoWrite

| Use bd when...                   | Use TodoWrite when...               |
| -------------------------------- | ----------------------------------- |
| Work spans multiple sessions     | Single-session tasks                |
| Tasks have dependencies/blockers | Simple linear checklist             |
| Need context after compaction    | All context in current conversation |
| Exploratory/research work        | Will complete this session          |

**Decision rule**: If resuming in 2 weeks would be hard without bd, use bd.

## Session Start Protocol

1. `bd ready` - Find unblocked tasks (sorted by priority)
2. Pick highest priority (P0 > P1 > P2 > P3 > P4)
3. `bd show <id>` - Get full context, dependencies, audit trail
4. `bd update <id> --status in_progress` - Claim the task
5. Add notes as you work (critical for compaction survival)

## Essential Commands

### Find Work

```bash
bd ready                # Tasks with no blockers
bd list --status=open   # All open issues
bd blocked              # Show blocked issues
bd show <id>            # Full issue details
bd search <query>       # Text search
bd stats                # Project metrics
```

### Create Issues

```bash
bd create "Title" -p <priority> --type <type>
```

- **Priority**: 0=critical, 1=high, 2=medium (default), 3=low, 4=backlog
- **Types**: task (default), bug, feature, epic, chore

Examples:

```bash
bd create "Fix auth bug" -p 0 --type bug
bd create "Add OAuth support" -p 1 --type feature
```

### Update Issues

```bash
bd update <id> --status <status>   # Change status
bd update <id> --notes "Progress"  # Add notes (appends, doesn't replace)
bd update <id> -p 0                # Change priority
```

**Status values**: open, in_progress, blocked, closed

**Note format** (best practice for compaction survival):

```
COMPLETED: What was done
IN PROGRESS: Current state + next step
BLOCKERS: What's preventing progress
```

### Complete Issues

```bash
bd close <id>
bd close <id> -r "Completion summary"   # -r optional but recommended
bd close <id1> <id2>                    # Close multiple
```

### Dependencies

```bash
bd dep add <child> <parent>   # parent blocks child
bd dep list <id>              # View dependencies
```

Example:

```bash
# deploy-task is blocked by test-task
bd dep add deploy-task test-task
```

### Labels

```bash
bd label add <id> backend
bd label add <id> security
```

### Git Sync

```bash
bd sync   # Export, commit, pull, push - all-in-one
```

## Session End Checklist

```bash
git status              # Check changes
git add <files>         # Stage code
bd sync                 # Sync beads
git commit -m "..."     # Commit code
bd sync                 # Sync any new beads changes
git push                # Push to remote
```

## Quick Reference

| Command                               | Purpose         |
| ------------------------------------- | --------------- |
| `bd ready`                            | Find ready work |
| `bd create "Title" -p 1`              | Create task     |
| `bd show <id>`                        | View details    |
| `bd update <id> --status in_progress` | Start work      |
| `bd update <id> --notes "..."`        | Add progress    |
| `bd close <id>`                       | Complete task   |
| `bd dep add <a> <b>`                  | b blocks a      |
| `bd list`                             | List all tasks  |
| `bd search <q>`                       | Find by text    |
| `bd sync`                             | Git sync        |
| `bd stats`                            | Project metrics |

## Additional Commands

Run `bd --help` for complete list. Key categories:

- **Views & Reports**: `activity`, `count`, `stale`, `status`
- **Dependencies & Structure**: `epic`, `graph`, `duplicate`, `supersede`
- **Labels & Comments**: `label`, `comments`
- **Maintenance**: `repair`, `doctor`, `migrate`
- **Integrations**: `jira`, `linear`

## Error Handling

**`bd: command not found`**
Install from https://github.com/steveyegge/beads

**`No .beads database found`**
Run `bd init` (humans do this once, not agents)

**`Task not found`**
Use `bd list` or `bd search` to find correct ID

**`Circular dependency detected`**
Restructure dependencies - bd prevents cycles automatically

**Git conflicts in `.beads/issues.jsonl`**
Run `bd sync --merge` for auto-resolution
