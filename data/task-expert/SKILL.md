---
name: task-expert
description: "'Task as Code' management expert. Responsible for maintaining task files in the todos/ directory, ensuring continuous task IDs, clear statuses, and adherence to specifications."
---

# Task Expert

This skill provides guidance on following the **Task as Code** philosophy. In this system, conversations are fluid, but tasks are persistent. All non-trivial changes must be documented in task files.

## Core Workflow

### 1. Task Identification and Creation

When a specific requirement or bug is identified, a new task should be immediately created in the `todos/zh/active/` directory.

- **ID Allocation**: Find the current maximum `TASK-XXXX` number and increment it by 1.
- **File Naming**: `TASK-{ID}-{slug}.md` (lowercase, hyphen-separated).
- **Front matter**: Must include `id`, `type`, `status`, `title`, `created_at`, `author`.

### 2. Develop and Document

During task execution, the task file is the "Source of Truth":

- **Context**: Record background information in the file.
- **Objectives**: Define clear deliverables.
- **Plan**: Maintain a task list (Checkboxes) in the file.
- **Thought**: Record key design decisions or technical pivots.

### 3. Task Archiving

When a task status changes to `done` or `cancelled`:

- Update the `status` in the Front matter.
- Move the file from `active/` to `archive/`.

## File Format Standards

Task files must use the following structure:

```markdown
---
id: TASK-XXXX
type: task
status: active # active | done | cancelled
title: 'Task Title'
created_at: 202X-XX-XX
author: [Your Name]
---

# TASK-XXXX: [Task Title]

## Background

[Briefly explain why this task is needed]

## Objectives

- [ ] Objective 1
- [ ] Objective 2

## Workflow/Notes

[Record thoughts, command outputs, or key code snippets during execution]
```

## Antipatterns

- **Skipping IDs**: Strictly forbidden to skip ID numbers.
- **Forgetting**: Strictly forbidden to close a conversation without updating statuses.
- **Clutter**: Strictly forbidden to pile up completed tasks in the `active/` directory.
- **Hidden Logic**: Strictly forbidden to discuss complex logic only in the conversation without persisting it in task files.

## Examples

- `todos/zh/active/TASK-0005-setup_skills_reference.md`
- `todos/zh/archive/TASK-0004-fix_pydantic_validation.md`
