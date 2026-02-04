---
name: Project Tracking
description: System for tracking work across AI sessions. Use when starting or ending work sessions, managing initiatives, capturing ideas or todos, or when needing to understand what work is in progress. Handles knowledge transfer between sessions.
---

# Project Tracking

A system for organizing work, maintaining continuity across AI sessions, and capturing knowledge.

## Core Concepts

### Initiatives
Multi-session efforts with a clear goal. Can be small (1-2 sessions) or large (weeks of work). Tracked through active → completed lifecycle.

### Sessions
One focused work period within an initiative. Captures what happened, decisions made, and what's next.

### Ideas
Quick capture for things that could be explored later. Not committed to.

### Todos
Concrete tasks that should happen but don't warrant a full initiative.

## Workspace Structure

All tracking lives in `docs/workspace/`:

```
docs/workspace/
├── initiatives/
│   ├── active/          # Currently being worked on
│   ├── completed/       # Done, archived for reference
│   └── backlog/         # Planned but not started
├── ideas/               # Quick captures, exploratory
└── todos/               # Tasks, not big enough for initiative
```

## Quick Reference

| I want to... | Do this |
|--------------|---------|
| Start working | Check `workspace/initiatives/active/` for context |
| End a session | Create session summary, update initiative status |
| Track new effort | Create initiative in `active/` or `backlog/` |
| Capture quick idea | Add to `workspace/ideas/` |
| Note a task | Add to `workspace/todos/` |
| Find prior context | Read recent sessions in relevant initiative |

## When to Use Each Reference

| Reference | When to Read |
|-----------|--------------|
| [structure.md](references/structure.md) | Understanding folder layout, document types, what goes where |
| [workflows.md](references/workflows.md) | Starting/ending sessions, managing initiative lifecycle |
| [templates/](references/templates/) | Creating new documents |

## AI Navigation

### Finding Context for Current Work

1. List `docs/workspace/initiatives/active/`
2. Read `INITIATIVE.md` for relevant initiative
3. Read recent sessions in `sessions/` folder
4. Check for blockers or open questions

### Updating After Work

1. Create session summary in initiative's `sessions/` folder
2. Update `INITIATIVE.md` status section
3. Update completion criteria checkboxes
4. Note any blockers or next steps

### Quick Captures

- Ideas: Create `docs/workspace/ideas/[name].md`
- Todos: Create `docs/workspace/todos/[name].md`

Keep these lightweight - a few sentences is fine.
