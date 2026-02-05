---
name: rulebook-task-management
description: Spec-driven task management for features and breaking changes using OpenSpec format. Use when creating new features, planning breaking changes, organizing development work, or managing project tasks with proposals and specifications.
version: "1.0.0"
category: core
author: "HiveLLM"
tags: ["task-management", "openspec", "spec-driven", "workflow"]
dependencies: []
conflicts: []
---

# Rulebook Task Management

## When to Create Tasks

**Create tasks for:**
- New features/capabilities
- Breaking changes
- Architecture changes
- Performance/security work

**Skip for:**
- Bug fixes
- Typos, formatting, comments
- Dependency updates (non-breaking)

## Task Commands

```bash
rulebook task create <task-id>    # Create new task
rulebook task list                # List all tasks
rulebook task show <task-id>      # Show task details
rulebook task validate <task-id>  # Validate structure
rulebook task archive <task-id>   # Archive completed task
```

## Mandatory Workflow

**NEVER start implementation without creating a task first:**

1. **STOP** - Do not start coding
2. **Create task** - `rulebook task create <task-id>`
3. **Plan** - Write proposal.md and tasks.md
4. **Spec** - Write spec deltas
5. **Validate** - `rulebook task validate <task-id>`
6. **THEN** - Start implementation

## Task Directory Structure

```
rulebook/tasks/<task-id>/
├── proposal.md         # Why and what changes
├── tasks.md            # Implementation checklist
├── design.md           # Technical design (optional)
└── specs/
    └── <module>/
        └── spec.md     # Technical specifications
```

## Best Practices

1. **Always create task first** - Document before implementing
2. **Keep tasks.md simple** - Only checklist items
3. **Put details in specs** - Technical requirements in spec files
4. **Validate before implementing** - Run `rulebook task validate`
5. **Archive when done** - Move completed tasks to archive
