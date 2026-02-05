---
name: aico-frontend-task-breakdown
description: |
  Break down PM story into frontend tasks following UI DEVELOPMENT order: Setup → Static UI → Dynamic Logic → Interactions → Testing.

  UNIQUE VALUE: Ensures proper dependency order. Tasks are ordered by UI development layers, not random order.

  Use this skill when:
  - Running /frontend.tasks command
  - User asks to "break down story", "create frontend tasks", "split into tasks"
  - Have story at docs/reference/pm/stories/ and need organized task list
  - Need tasks ordered by UI development layers (not random order)
  - Starting frontend work and want organized task list

  Task order is CRITICAL: Setup → Static UI → Dynamic → Interactions → Tests
  Output: ALWAYS write to docs/reference/frontend/tasks/{story-name}.md
---

# Task Breakdown

## Language Configuration

Before generating any content, check `aico.json` in project root for `language` field to determine the output language. If not set, default to English.

## Process

1. **Read story/PRD**: Load from `docs/reference/pm/stories/` or `docs/reference/pm/versions/`
2. **Read design** (if exists): Load from `docs/reference/frontend/designs/`
3. **Identify components**: What UI elements are needed
4. **Identify interactions**: What logic and events are needed
5. **Break into tasks**: Independently testable, single responsibility
6. **Order by dependencies**: Setup → Static UI → Dynamic → Tests
7. **Save output**: ALWAYS write to `docs/reference/frontend/tasks/{story-name}.md`

## Task File Template

```markdown
# [Story Name] - Frontend Tasks

> Project: [project-name]
> Created: YYYY-MM-DD
> Last Updated: YYYY-MM-DD
> Source: docs/reference/pm/stories/[story].md
> Design: docs/reference/frontend/designs/[name].md
> Status: in_progress

## Progress

| Task                         | Status         | Notes |
| ---------------------------- | -------------- | ----- |
| 1. Setup component structure | ✅ completed   |       |
| 2. Implement header section  | 🔄 in_progress |       |
| 3. Implement content section | ⏳ pending     |       |

## Tasks

### Task 1: [Task Name]

**Status**: ⏳ pending
**Goal**: What this task achieves
**Scope**: Files to create/modify
**Acceptance Criteria**:

- [ ] Criterion 1
- [ ] Criterion 2
      **Dependencies**: Task X (if any)
```

## Task Types

| Type        | Examples                                |
| ----------- | --------------------------------------- |
| Setup       | Create component structure, setup state |
| UI          | Implement section/component layout      |
| Logic       | Add form validation, API integration    |
| Interaction | Implement hover, click, animations      |
| Testing     | Unit tests, integration tests           |

## Granularity Rules

- Each task = independently testable
- Each task = single responsibility
- Each task = clear scope (not too big, not too small)

## Ordering Rules

1. Setup tasks first
2. Static UI before dynamic
3. Core functionality before edge cases
4. Tests after implementation

## Key Rules

- ALWAYS include test tasks at the end
- MUST note dependencies between tasks
- ALWAYS save to `docs/reference/frontend/tasks/` directory
- Keep tasks focused - not too big, not too small

## Common Mistakes

- ❌ Tasks too large (full page) → ✅ Break into sections
- ❌ Tasks too small (add one button) → ✅ Group related work
- ❌ Skip dependencies → ✅ Note which tasks depend on others
- ❌ Forget testing → ✅ Always include test tasks
