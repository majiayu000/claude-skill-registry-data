---
name: bd-issue-tracking
description: Track and manage work with bd issue tracker for persistent context across sessions and compaction events. Use for work needing dependencies, recovery after compaction, or multi-session tracking.
---

# bd Issue Tracking

bd is a graph-based issue tracker providing persistent memory across sessions. Use for multi-session work; use TodoWrite for simple single-session tasks.

## When to Use bd vs TodoWrite

| Use bd | Use TodoWrite |
|--------|---------------|
| Multi-session work (days/weeks) | Single-session tasks (this hour) |
| Complex dependencies/blockers | Linear step-by-step execution |
| Need context after compaction | All context in conversation |
| Fuzzy/exploratory work | Simple checklist |

**Decision rule**: "If I need this context in 2 weeks after compaction, use bd"

## Session Start

```bash
bd ready --json                              # Find available work
bd list --status in_progress --json          # Check active work
bd show <issue-id>                           # Read notes from previous session
```

Report to user: "X items ready. Issue Y in_progress: [summary from notes]"

## Core Operations

```bash
# Create issue
bd create "Title" -d "Description" -p 2 -t task --json

# Start work
bd update bd-xxx --status in_progress --json

# Checkpoint progress (at 70% tokens, milestones, blockers)
bd update bd-xxx --notes "COMPLETED: ...\nIN_PROGRESS: ...\nNEXT: ..." --json

# Complete work
bd close bd-xxx --reason "What was done and how verified" --json

# Manage dependencies
bd dep add bd-setup bd-impl --type blocks    # A blocks B
bd dep tree bd-xxx                           # View dependency tree
```

## Notes Format

Write for post-compaction recovery (no conversation context):

```
COMPLETED: Specific deliverables done
KEY DECISION: Important choices with rationale
IN PROGRESS: Current state + immediate next step
BLOCKERS: What's preventing progress
NEXT: What to do when unblocked
```

## Priority Levels

0=critical, 1=high, 2=normal (default), 3=low, 4=backlog

## Description Template

```bash
bd create --title "$TITLE" --description "$(cat <<'EOF'
# Description
1-4 sentences: what and why.

# Relevant files and snippets
Files identified during discovery with code snippets.

# Additional sources
Repos explored, web searches performed.
EOF
)" --json
```

## Reference Documentation

For detailed guidance, read these files:

| Topic | Reference |
|-------|-----------|
| bd vs TodoWrite decisions | [references/BOUNDARIES.md](references/BOUNDARIES.md) |
| Complete CLI reference | [references/CLI_REFERENCE.md](references/CLI_REFERENCE.md) |
| Session workflows & checklists | [references/WORKFLOWS.md](references/WORKFLOWS.md) |
| Dependency types & patterns | [references/DEPENDENCIES.md](references/DEPENDENCIES.md) |
| Issue creation guidance | [references/ISSUE_CREATION.md](references/ISSUE_CREATION.md) |
| Context recovery patterns | [references/RESUMABILITY.md](references/RESUMABILITY.md) |
| Static data usage | [references/STATIC_DATA.md](references/STATIC_DATA.md) |
