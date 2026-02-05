---
name: conductor-context
description: Use this skill when the user mentions "plan", "track", "spec", "conductor", asks about project progress, or references conductor files like plan.md, spec.md, tracks.md, product.md, tech-stack.md, or workflow.md. Also use when the user wants to understand the Conductor methodology or Context-Driven Development workflow.
version: 0.1.0
---

# Conductor: Context-Driven Development

Conductor is a workflow methodology that transforms Claude Code into a project manager following a strict protocol: **Context -> Spec & Plan -> Implement**.

## Core Philosophy

**Measure twice, code once.** By treating context as a managed artifact alongside code, you transform your repository into a single source of truth that drives every agent interaction with deep, persistent project awareness.

## Key Concepts

### Tracks
A **track** is a high-level unit of work (feature or bug fix). Each track has:
- `spec.md` - Detailed requirements and acceptance criteria
- `plan.md` - Actionable to-do list with phases, tasks, and sub-tasks
- `metadata.json` - Track metadata (ID, type, status, timestamps)

Tracks are stored in `conductor/tracks/<track_id>/`.

### Project Context Files
Located in the `conductor/` directory:
- **`product.md`** - Product vision, goals, users, features
- **`product-guidelines.md`** - Prose style, brand messaging, visual identity
- **`tech-stack.md`** - Languages, frameworks, databases, tools
- **`workflow.md`** - Development methodology (TDD, commit strategy)
- **`tracks.md`** - Master list of all tracks and their status
- **`code_styleguides/`** - Language-specific coding standards

### Task Status Markers
- `[ ]` - Pending (not started)
- `[~]` - In progress (currently being worked on)
- `[x]` - Completed (finished and committed)

### Workflow Phases
1. **Setup** - Initialize project context (run once)
2. **New Track** - Create spec and plan for feature/bug
3. **Implement** - Execute tasks following TDD workflow
4. **Status** - Check progress across tracks
5. **Revert** - Git-aware rollback of tracks/phases/tasks

## File Locations

When a user mentions "the plan" or "the spec", they likely refer to:
- Current track's plan: `conductor/tracks/<track_id>/plan.md`
- Current track's spec: `conductor/tracks/<track_id>/spec.md`
- Master tracks list: `conductor/tracks.md`

## TDD Workflow

Conductor follows Test-Driven Development by default:
1. **Red Phase** - Write failing tests first
2. **Green Phase** - Implement minimum code to pass tests
3. **Refactor** - Clean up with safety of passing tests

## Phase Completion Protocol

At the end of each phase:
1. Ensure test coverage (>80% target)
2. Manual verification with user
3. Create checkpoint commit
4. Attach git notes with verification report
5. Update plan.md with checkpoint SHA

## Commands Reference

| Command | Purpose |
|---------|---------|
| `/conductor:setup` | Initialize project context |
| `/conductor:new-track` | Create new feature/bug track |
| `/conductor:implement` | Execute tasks from plan |
| `/conductor:status` | Display progress overview |
| `/conductor:revert` | Rollback tracks/phases/tasks |

## Template Location

Templates are bundled with the plugin at `${CLAUDE_PLUGIN_ROOT}/templates/`:
- `workflow.md` - Default workflow configuration
- `code_styleguides/` - Language-specific style guides
