---
name: mini-kanban
description: "File-based task management with shai-tix CLI. Use when user mentions kanban, ticket, planning, task tracking, or references tickets by [id] or #id format. MUST run via: uvx --from shai-tix==0.1.3 shai-tix <cmd>. Data stored in .tix/ directory (NOT .shai-tix/)."
---

# mini-kanban

A local JIRA-like task management system. Uses CLI to manage stories and tasks stored in `.tix/` directory under git repo root. All data is human-readable markdown files tracked by git.

**First step for any operation**: `uvx --from shai-tix==0.1.3 shai-tix rebuild_index_db`

## Command Format

All commands run via `uvx` (no installation needed):

```bash
uvx --from shai-tix==0.1.3 shai-tix <command>
```

Example:
```bash
uvx --from shai-tix==0.1.3 shai-tix create_story "My Feature" --description "Description here"
```

## Core Concepts

### Story and Task Hierarchy

```
Story (Feature/Epic)
└── Task (Atomic work unit)
```

- **Story**: High-level feature or requirement
- **Task**: Specific work item under a Story

**Best practice**: If a story involves multiple independently testable steps, break it down into tasks. Tasks may have dependencies - describe the order/prerequisites in each task's description.

### File System Structure

While you can access files directly, **prefer using CLI commands** as the primary API for list/search/get/create/update/delete operations on stories and tasks.

```
.tix/
├── index.sqlite                              # SQLite index (cache, auto-generated)
└── stories/
    └── story-{date}-{id}-{title}/
        ├── metadata.json                     # {"status": "IN_PROGRESS", ...}
        ├── description.md                    # Story description (editable)
        ├── report.md                         # Completion report
        ├── tmp/                              # Temporary scripts and data
        └── tasks/
            └── task-{date}-{id}-{title}/
                ├── metadata.json
                ├── description.md
                ├── report.md
                └── tmp/                      # Task-specific temp files
```

**Key files:**
- `metadata.json`: Contains status and other metadata
- `description.md`: Detailed description of the story/task
- `report.md`: Completion report (written when done)
- `tmp/`: Directory for temporary scripts, data files, or intermediate outputs

### Status Values

| Status | Description |
|--------|-------------|
| `TODO` | Not started |
| `IN_PROGRESS` | Currently being worked on |
| `COMPLETED` | Finished |
| `BLOCKED` | Blocked by external dependencies |
| `CANCELED` | Canceled |

## CLI Commands

Most operations should be done via CLI.

### Workflow (MUST FOLLOW)

**Step 1**: Run `rebuild_index_db` first to sync the index:
```bash
uvx --from shai-tix==0.1.3 shai-tix rebuild_index_db
```

**Step 2**: Run `-h` to see all available subcommands:
```bash
uvx --from shai-tix==0.1.3 shai-tix -h
```

**Step 3**: Based on SKILL doc scenarios, identify which subcommands you need, then run `-h` for each to learn the exact arguments:
```bash
# Run multiple -h commands in parallel to get usage info
uvx --from shai-tix==0.1.3 shai-tix create_story -h
uvx --from shai-tix==0.1.3 shai-tix create_task -h
uvx --from shai-tix==0.1.3 shai-tix list_stories -h
```

**Step 4**: Now execute the actual commands with correct arguments.

### Available Subcommands

- **Story**: `create_story`, `get_story`, `list_stories`, `search_stories`, `update_story`, `delete_story`
- **Task**: `create_task`, `get_task`, `list_tasks`, `list_tasks_by_story`, `search_tasks`, `update_task`, `delete_task`
- **Index**: `rebuild_index_db` (run this first before any workflow)

## Common Scenarios

These examples show typical workflows. **Remember**:
1. Run `rebuild_index_db` first
2. Run `<subcommand> -h` to confirm exact argument format before executing

### Creating a New Feature (Story with Tasks)

When user defines a requirement that needs multiple work items:

```bash
# 1. Create the story
uvx --from shai-tix==0.1.3 shai-tix create_story "User Authentication" --description "Implement login and logout"

# 2. Break down into tasks
uvx --from shai-tix==0.1.3 shai-tix create_task 1 "Create login form" --description "HTML form with validation"
uvx --from shai-tix==0.1.3 shai-tix create_task 1 "Add session management"
uvx --from shai-tix==0.1.3 shai-tix create_task 1 "Implement logout endpoint"
```

### Viewing Pending Work

When user asks "what's not done?" or "show me pending tickets":

```bash
# List recent stories
uvx --from shai-tix==0.1.3 shai-tix list_stories

# Find incomplete work (TODO or IN_PROGRESS)
uvx --from shai-tix==0.1.3 shai-tix search_stories --status "TODO,IN_PROGRESS"
uvx --from shai-tix==0.1.3 shai-tix search_tasks --status "TODO,IN_PROGRESS"

# List tasks under a specific story
uvx --from shai-tix==0.1.3 shai-tix list_tasks_by_story 1
```

### Working on a Specific Ticket

When user references a ticket by `[id]` or `#id` (e.g., "work on [3]" or "do #3"):

```bash
# 1. Get ticket details to understand the work
uvx --from shai-tix==0.1.3 shai-tix get_story 3    # if story
uvx --from shai-tix==0.1.3 shai-tix get_task 3     # if task
```

The output includes the `Path` to the directory. You can:
- Read `description.md` for detailed requirements
- Read `report.md` if already completed (to understand what was done)
- Create scripts in `tmp/` directory for task execution
- Store intermediate data in `tmp/` directory

```bash
# 2. Mark as in progress
uvx --from shai-tix==0.1.3 shai-tix update_task 3 --status IN_PROGRESS

# 3. After completing, update with report
uvx --from shai-tix==0.1.3 shai-tix update_task 3 --status COMPLETED --report "Implemented with unit tests"
```

**Direct file access**: After getting the path from `get_story` or `get_task`, you can directly:
- `Read` the `metadata.json`, `description.md`, `report.md` files
- Create temp scripts in `${path}/tmp/` to execute work
- Store data or intermediate results in `${path}/tmp/`

### Searching for Specific Tickets

When user needs to find tickets by criteria:

```bash
# Search by title keyword (token matching)
uvx --from shai-tix==0.1.3 shai-tix search_stories --title "login auth"
uvx --from shai-tix==0.1.3 shai-tix search_tasks --title "form"

# Search by status
uvx --from shai-tix==0.1.3 shai-tix search_tasks --status "BLOCKED"

# Search by date range
uvx --from shai-tix==0.1.3 shai-tix search_stories --date_lower 2025-01-01 --date_upper 2025-01-31

# Search by ID range with limit
uvx --from shai-tix==0.1.3 shai-tix search_stories --id_lower 1 --id_upper 10 --limit 5

# Combined filters
uvx --from shai-tix==0.1.3 shai-tix search_tasks --title "api" --status "TODO,IN_PROGRESS"
```

### Updating Ticket Status

```bash
# Mark as in progress
uvx --from shai-tix==0.1.3 shai-tix update_task 5 --status IN_PROGRESS

# Mark as blocked
uvx --from shai-tix==0.1.3 shai-tix update_story 2 --status BLOCKED

# Complete with report
uvx --from shai-tix==0.1.3 shai-tix update_task 5 --status COMPLETED --report "Feature implemented and tested"
```

### Batch Operations

For running multiple queries efficiently:

```bash
# Rebuild index once, then run multiple queries
uvx --from shai-tix==0.1.3 shai-tix rebuild_index_db
uvx --from shai-tix==0.1.3 shai-tix list_stories
uvx --from shai-tix==0.1.3 shai-tix search_tasks --status TODO
```

## Title Restrictions

Titles must contain only: letters (a-z, A-Z), digits (0-9), and spaces.

**Invalid**: `Feature: Login`, `Bug Fix #123`, `Task [urgent]`
**Valid**: `Feature Login`, `Bug Fix 123`, `Task urgent`

## Project Root

The `--root` parameter specifies the git repository root directory. The CLI expects a `.tix/` directory under this root:

```
/path/to/git-repo/          <-- --root points here
├── .git/
├── .tix/                   <-- shai-tix data directory
│   ├── index.sqlite
│   └── stories/
├── src/
└── ...
```

By default, CLI uses current working directory as root. Use `--root` to specify a different project:

```bash
uvx --from shai-tix==0.1.3 shai-tix list_stories --root /path/to/git-repo
uvx --from shai-tix==0.1.3 shai-tix create_story "New Feature" --root /path/to/git-repo
```
