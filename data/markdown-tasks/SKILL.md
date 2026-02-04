---
name: markdown-tasks
description: Work with markdown-based task lists in .llm/todo.md files. Use when managing tasks, working with todo lists, extracting incomplete tasks, marking tasks complete, or implementing tasks from a task list.
---

# Markdown Task Management

This skill enables working with the markdown task list stored in `.llm/todo.md`.

## Scripts

### task_get.py - Extract Next Task

Extract the first incomplete task with its context:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/task_get.py .llm/todo.md
```

Returns the first `[ ]` checkbox line with all indented context lines below it.

**Exit codes**: 0 (success), 1 (file not found or error)

### task_add.py - Add New Task

Add a new task:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/task_add.py .llm/todo.md "Task description
  Context line 1
  Context line 2"
```

Creates the `.llm/` directory and `todo.md` file if they do not exist, and appends the new task with a `[ ]` checkbox. The script preserves all indentation in multi-line strings.

**Exit codes**: 0 (success), 1 (error)

### task_complete.py - Mark Task Done

Mark the first incomplete task as done:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/task_complete.py .llm/todo.md
```

Changes the first `[ ]` to `[x]`.

**Exit codes**: 0 (success), 1 (no incomplete tasks or error)

### task_archive.py - Archive Task List

Archive a completed task list:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/task_archive.py .llm/todo.md
```

Moves the file to `.llm/YYYY-MM-DD-todo.md` where YYYY-MM-DD is today's date.

**Exit codes**: 0 (success), 1 (file not found or error)

## Task Format

The task list is in `.llm/todo.md`.

NEVER use the `Read` tool on `.llm/todo.md`. Always interact with the task list exclusively through the Python scripts.

### Task States

- `[ ]` - Not started (ready to work on)
- `[x]` - Completed
- `[!]` - Blocked after failed attempt

### Task Structure

Each task includes indented context lines with full implementation details:

- Absolute file paths
- Exact function/class names
- Code analogies to existing patterns
- Dependencies and prerequisites
- Expected outcomes

### Standalone Context

Each task is extracted and executed in isolation. Every task must contain ALL context needed to implement it. Repeat shared context in every related task. Never reference other tasks.

If tasks were created from a plan file (e.g., from planning mode), include the plan file path in each task so the implementing agent can read the full context.
