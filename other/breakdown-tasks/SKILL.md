---
name: breakdown-tasks
description: Use when creating, breaking down, tracking, or updating tasks from a spec, project idea, feature request, or implementation goal. Supports local task files with optional epics, or connected external project-management systems. Triggered by phrases like "create tasks from this spec", "break this into tasks", "track tasks", "make tickets", "create issues", or "add epics".
---

# Breakdown Tasks

Announce at start: `Breaking down tasks...`

Create small, trackable tasks from a spec or goal. Keep task tracking vendor-neutral unless the user chooses a connected external system.

## Process

1. Find the source spec or ask for it.
2. Ask where tasks should be created. Read `references/question-format.md` and follow it exactly - including the `Why A wins:` and `If wrong:` lines. The options are:
   - `A. (Recommended) Global local board` - `~/.agents/tasks/<repo>/<project-slug>/`
   - `B. Repo-local board` - `.agents/tasks/<project-slug>/`
   - `C. External system` - requires a connected project-management MCP/plugin/tool
3. If external, verify the tool is available before creating anything.
4. Break the work into tasks small enough for one focused agent session.
5. Use epics only when the spec naturally splits into multiple user-visible outcomes, modules, milestones, or implementation phases.
6. Save or update the task files, then show the root path and the next recommended task.

## Local Layout

For small specs:

```text
<task-root>/<project-slug>/
  TASKS.md
  TASK-001-<slug>.md
  TASK-002-<slug>.md
```

For larger specs:

```text
<task-root>/<project-slug>/
  TASKS.md
  epics/
    EPIC-001-<slug>/
      EPIC.md
      TASK-001-<slug>.md
      TASK-002-<slug>.md
```

Do not create epics for fewer than 4 tasks unless the grouping is clearly useful.

## Task Format

```markdown
# TASK-001: <Title>

Status: todo
Epic: EPIC-001 or None
Source: <spec path or section>

## Goal
<one sentence>

## Acceptance Criteria
- <testable outcome>

## Validation
- <command or manual check>
```

## Epic Format

```markdown
# EPIC-001: <Title>

Status: todo
Source: <spec path or section>

## Goal
<one sentence>

## Tasks
- [ ] TASK-001: <title>
- [ ] TASK-002: <title>
```

## Status Updates

Allowed statuses:
- `todo`
- `in-progress`
- `done`

When updating a task, change only the status/checklist placement unless the user asks for edits.

## External Systems

If the selected system supports epics, create epics using the same grouping rules. If it does not, represent epics as parent tasks, labels, milestones, or the closest native grouping.

## Rules

- Use generic terms: task, ticket, issue, epic, project-management system.
- Do not assume any vendor.
- Do not plan implementation details here. Use `plan` for that.
- Do not include commit, push, or PR steps inside task descriptions.
- Keep task titles short and action-oriented.
