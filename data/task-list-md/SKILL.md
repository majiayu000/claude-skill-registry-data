---
name: task-list-md
description: Parse and manage tasks list in a markdown file using checklist format (tasks.md, checklist.md)
---

# task-list-md

Task List MD CLI (`scripts/task_list_md.py`) parses hierarchical checklists, maintains task metadata, and tracks progress for markdown task files.

## Status Mapping

- `[ ]` → `pending` (yellow)
- `[-]` → `in-progress` (blue)
- `[x]` → `done` (green)
- `[+]` → `review` (cyan)
- `[*]` → `deferred` (red)

## Progress Tracking

- Persists statistics in `.tasks.local.json` (auto-created next to the CLI).
- Records totals, completion percentage, per-task history, and optional tracking conditions.
- Status changes automatically append timestamped history entries.

## File Resolution

- Every command accepts an optional `file` argument. If omitted, the CLI auto-selects the most recently modified entry from `.tasks.local.json` and echoes the selection.
- The parser detects misplaced file paths in other arguments (for example, if a path is passed instead of `task_id`) and reassigns them to `file`.

## Task Identifiers

- IDs must be digits with optional dot-separated hierarchy: `1`, `2.1`, `3.2.4`, etc.
- Parent/child relationships are inferred from dot notation; indentation in the markdown follows the same hierarchy.

## Command Reference

### list-tasks

`python3 scripts/task_list_md.py list-tasks [file]`

- Prints all tasks in hierarchical order with colored statuses when supported by the terminal.
- Shows descriptions, requirements, dependencies, and nested structure.

### show-task

`python3 scripts/task_list_md.py show-task [file] <task_id>`

- Displays the specified task plus its sub-tasks, requirements, dependencies, and status history.
- Requires a valid task ID.

### set-status

`python3 scripts/task_list_md.py set-status [file] <task_id1> [task_id2 ...] <status>`

- Updates one or many tasks to `pending`, `in-progress`, `done`, `review`, or `deferred`.
- Enforces hierarchy rules: sub-tasks cannot move from `pending` while their parent is `pending` or `done`.
- Automatically updates parent tasks when all sub-tasks share the same status.
- Records status transitions in `.tasks.local.json`.

### add-task

`python3 scripts/task_list_md.py add-task [file] <task_id> "<description>" [--dependencies dep1 dep2 ...] [--requirements req1 req2 ...]`

- Creates a new pending task inserted in ID order.
- Validates uniqueness of `task_id` and existence of referenced dependency IDs.
- Optional `_Requirements:_` and `_Dependencies:_` lines are written under the task.

### update-task

`python3 scripts/task_list_md.py update-task [file] <task_id> [--add-dependencies dep ...] [--add-requirements req ...] [--remove-dependencies dep ...] [--remove-requirements req ...] [--clear-dependencies] [--clear-requirements]`

- Modifies dependency and requirement lists in place.
- `--clear-*` cannot be combined with the corresponding `--add-*` or `--remove-*` flags.
- Rewrites the markdown block for the task and refreshes cached statistics.

### delete-task

`python3 scripts/task_list_md.py delete-task [file] <task_id1> [task_id2 ...]`

- Removes the specified tasks and any nested sub-tasks.
- Refuses to delete when other tasks (not in the deletion list) depend on the target.

### get-next-task

`python3 scripts/task_list_md.py get-next-task [file] [--wait DURATION]`

- Suggests the next actionable task from PENDING tasks only (excludes IN_PROGRESS tasks)
- Honors dependencies and parent constraints
- Prefers sub-tasks when the parent is `in-progress`
- Surfaces context (dependencies, parent, sub-tasks)
- Distinguishes between two scenarios:
  - "All tasks have been completed!" - when all tasks are done/review
  - "No tasks available to work on..." - when tasks exist but are blocked or in-progress/deferred
- Optional `--wait DURATION` parameter:
  - Waits for specified duration when no task is available
  - Duration format: `30` (30 minutes), `30m` (30 minutes), `2h` (2 hours), `90s` (90 seconds)
  - Units: `s` for seconds, `m` for minutes, `h` for hours (defaults to minutes if no unit specified)
  - Periodically checks for available tasks (every 10 seconds)
  - Automatically reloads task file to detect status changes
  - Examples: `--wait 30m`, `--wait 2h`, `--wait 120s`

### check-dependencies

`python3 scripts/task_list_md.py check-dependencies [file]`

- Validates that every dependency exists, is not self-referential, and does not create circular relationships.
- Lists violations or confirms success.

### show-progress

`python3 scripts/task_list_md.py show-progress [file]`

- Refreshes statistics, then prints totals, completion percentages, status counts, last-modified timestamp, and per-task status history.

### filter-tasks

`python3 scripts/task_list_md.py filter-tasks [file] [--status STATUS] [--requirements req ...] [--dependencies dep ...]`

- Returns tasks matching all provided filters.
- `--requirements` and `--dependencies` require tasks to include every supplied value.

### search-tasks

`python3 scripts/task_list_md.py search-tasks [file] <keyword1> [keyword2 ...]`

- Case-insensitive search across task IDs, descriptions, requirements, dependencies, and captured content.
- Maintains hierarchy in the output for readability.

### ready-tasks

`python3 scripts/task_list_md.py ready-tasks [file]`

- Lists pending tasks whose dependencies are all complete (`done` or `review`).
- Excludes sub-tasks whose parent is still `pending` or already `done`.

### export

`python3 scripts/task_list_md.py export [file] [--output output.json]`

- Emits a JSON document containing statistics, task metadata, hierarchy, and status history.
- Writes to `stdout` when `--output` is omitted, enabling piping to other tooling.

### track-progress

Manage time-bound completion conditions stored in `.tasks.local.json`.

#### track-progress add

`python3 scripts/task_list_md.py track-progress add [file] <task_id1> [task_id2 ...] [--valid-for DURATION] [--complete-more N]`

- Creates a tracking condition with an expiration.
- `--valid-for` accepts integers (seconds) or values ending with `h`, `m`, or `s` (default `2h`).
- `--complete-more` expects an integer that adds to the current completed count; the CLI validates it against the total tasks.

#### track-progress check

`python3 scripts/task_list_md.py track-progress check [file]`

- Evaluates all active conditions and reports unmet tasks or completion targets to stderr.
- Exit codes: `0` when all conditions are satisfied, `2` when conditions remain unmet, and `1` for errors.

#### track-progress clear

`python3 scripts/task_list_md.py track-progress clear [file] [--yes]`

- Clears every stored condition after confirmation.
- Use `--yes` to skip the interactive prompt (helpful in scripted environments).

## Examples

<file> is the path to the markdown file contain the task list

Basic Usage:

- python3 scripts/task_list_md.py list-tasks <file>
- python3 scripts/task_list_md.py show-task <file> <task_id>
- python3 scripts/task_list_md.py set-status <file> <task_id1> [task_id2...] <status>
- python3 scripts/task_list_md.py get-next-task <file>
- python3 scripts/task_list_md.py check-dependencies <file>
- python3 scripts/task_list_md.py show-progress <file>

Task Management:

- python3 scripts/task_list_md.py add-task <file> <task_id> "<description>" [--dependencies dep1 dep2] [--requirements req1 req2]
- python3 scripts/task_list_md.py update-task <file> <task_id> [--add-dependencies dep1 dep2] [--add-requirements req1 req2] [--remove-dependencies dep1] [--remove-requirements req1] [--clear-dependencies] [--clear-requirements]
- python3 scripts/task_list_md.py delete-task <file> <task_id1> [task_id2...]

Advanced Filtering & Search:

- python3 scripts/task_list_md.py filter-tasks <file> [--status pending] [--requirements req1] [--dependencies dep1]
- python3 scripts/task_list_md.py search-tasks <file> keyword1 [keyword2...]
- python3 scripts/task_list_md.py ready-tasks <file>

Export:

- python3 scripts/task_list_md.py export <file> [--output filename.json]

## Importance

Replace the script path `scripts/task_list_md.py` with `${CLAUDE_PLUGIN_ROOT}/skills/task-list-md/scripts/task_list_md.py` when execute script in this skill.
