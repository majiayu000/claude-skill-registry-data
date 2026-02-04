---
name: backlog-manager
description: Expert guidance for managing tasks using the Backlog.md CLI tool. Use this skill when working with backlog tasks, creating or editing task files, managing acceptance criteria, tracking task progress, or understanding backlog workflows and best practices. Activates when users mention backlog, tasks, acceptance criteria, task management, or backlog commands.
---

# Backlog Manager Skill

This skill provides comprehensive guidance for using the Backlog.md CLI tool to manage project tasks effectively.

## Core Principles

**⚠️ CRITICAL RULE: NEVER EDIT TASK FILES DIRECTLY**

All task operations MUST use the Backlog.md CLI commands:
- ✅ Use `backlog task edit` and other CLI commands
- ✅ Use `backlog task create` to create new tasks
- ✅ Use `backlog task edit <id> --check-ac <index>` to mark acceptance criteria
- ❌ DON'T edit markdown files directly
- ❌ DON'T manually change checkboxes in files
- ❌ DON'T add or modify text in task files without using CLI

**Why?** Direct file editing breaks metadata synchronization, Git tracking, and task relationships.

## Task Lifecycle

### 1. Creating Tasks

Use CLI to create tasks with proper metadata:

```bash
# Basic task
backlog task create "Task title" -d "Description"

# With acceptance criteria
backlog task create "Task title" \
  -d "Description" \
  --ac "First criterion" \
  --ac "Second criterion"

# With full metadata
backlog task create "Task title" \
  -d "Description" \
  -a @assignee \
  -s "To Do" \
  -l backend,api \
  --priority high
```

**Task Components:**
- **Title**: Clear, brief summary (one liner)
- **Description (The "why")**: Purpose and goal without implementation details
- **Acceptance Criteria (The "what")**: Outcome-oriented, testable criteria

**Good AC Examples:**
- ✅ "User can successfully log in with valid credentials"
- ✅ "System processes 1000 requests per second without errors"
- ❌ "Add a new function handleLogin() in auth.ts" (implementation detail)

### 2. Starting Work

**FIRST STEPS when taking over a task:**

```bash
# Set status and assign yourself
backlog task edit 42 -s "In Progress" -a @myself

# View task details
backlog task 42 --plain

# Create implementation plan (The "how")
backlog task edit 42 --plan $'1. Research codebase\n2. Implement solution\n3. Add tests\n4. Update docs'
```

### 3. During Implementation

Mark acceptance criteria as complete when done:

```bash
# Check single AC
backlog task edit 42 --check-ac 1

# Check multiple ACs at once
backlog task edit 42 --check-ac 1 --check-ac 2 --check-ac 3

# Mixed operations
backlog task edit 42 --check-ac 1 --uncheck-ac 2 --remove-ac 3
```

**Important:** Only implement what's in the Acceptance Criteria. If you need to do more:
1. Update the AC first: `backlog task edit 42 --ac "New requirement"`
2. Or create a follow-up task: `backlog task create "Additional feature"`

### 4. Completing Tasks

Add implementation notes (PR description):

```bash
# Replace notes
backlog task edit 42 --notes $'Implemented using pattern X\n- Modified files Y and Z\n- Added comprehensive tests'

# Append notes progressively
backlog task edit 42 --append-notes $'- Added tests\n- Updated docs'
```

Mark task as done:

```bash
backlog task edit 42 -s Done
```

## Common Operations

### Finding and Viewing Tasks

```bash
# List all tasks (AI-friendly output)
backlog task list --plain

# List by status
backlog task list -s "To Do" --plain
backlog task list -s "In Progress" --plain

# List by assignee
backlog task list -a @sara --plain

# View specific task
backlog task 42 --plain

# Search tasks (fuzzy matching)
backlog search "auth" --plain
backlog search "api" --type task --status "In Progress" --plain
```

### Editing Task Metadata

```bash
# Change title
backlog task edit 42 -t "New Title"

# Change status
backlog task edit 42 -s "In Progress"

# Assign task
backlog task edit 42 -a @sara

# Add/change labels
backlog task edit 42 -l backend,api,urgent

# Set priority
backlog task edit 42 --priority high

# Multiple changes at once
backlog task edit 42 -s "In Progress" -a @myself -l backend
```

### Managing Acceptance Criteria

```bash
# Add new criteria
backlog task edit 42 --ac "New criterion" --ac "Another criterion"

# Check criteria (mark as complete)
backlog task edit 42 --check-ac 1
backlog task edit 42 --check-ac 1 --check-ac 2  # Multiple at once

# Uncheck criteria
backlog task edit 42 --uncheck-ac 3

# Remove criteria
backlog task edit 42 --remove-ac 2

# Mixed operations
backlog task edit 42 --ac "New" --check-ac 1 --remove-ac 4
```

## Multi-line Content

For descriptions, plans, and notes with newlines, use shell-specific syntax:

**Bash/Zsh (ANSI-C quoting):**
```bash
backlog task edit 42 --desc $'Line 1\nLine 2\n\nLine 3'
backlog task edit 42 --plan $'1. Step one\n2. Step two'
backlog task edit 42 --notes $'Implemented A\nTested B'
```

**PowerShell:**
```powershell
backlog task edit 42 --notes "Line 1`nLine 2"
```

**POSIX portable:**
```bash
backlog task edit 42 --notes "$(printf 'Line 1\nLine 2')"
```

## Definition of Done

A task is **Done** only when ALL of the following are complete:

**Via CLI:**
1. All acceptance criteria checked (`--check-ac`)
2. Implementation notes added (`--notes`)
3. Status set to Done (`-s Done`)

**Via Code/Testing:**
4. Tests pass
5. Documentation updated
6. Code reviewed
7. No regressions

## Quick Reference: DO vs DON'T

### Viewing Tasks

| ✅ DO | ❌ DON'T |
|------|---------|
| `backlog task 42 --plain` | Open .md file directly |
| `backlog task list --plain` | Browse backlog/tasks folder |
| `backlog search "topic" --plain` | Manually grep files |

### Modifying Tasks

| ✅ DO | ❌ DON'T |
|------|---------|
| `backlog task edit 42 --check-ac 1` | Change `- [ ]` to `- [x]` in file |
| `backlog task edit 42 --notes "..."` | Type notes into .md file |
| `backlog task edit 42 -s Done` | Edit status in frontmatter |
| `backlog task edit 42 --ac "New"` | Add `- [ ] New` to file |

## Best Practices

1. **Phase Discipline:**
   - **Creation**: Title, Description, Acceptance Criteria, optional metadata
   - **Implementation**: Implementation Plan (after moving to "In Progress")
   - **Wrap-up**: Implementation Notes, AC checks, mark as Done

2. **Task Quality:**
   - Atomic tasks (one unit of work = one PR)
   - Independent (don't depend on future tasks)
   - Testable with clear verification criteria
   - Valuable (delivers standalone value)

3. **Implementation Notes Formatting:**
   - Keep PR-ready and human-friendly
   - Use short paragraphs or bullet lists
   - Lead with the outcome, then supporting details
   - Use Markdown bullets for easy GitHub paste

4. **Always use `--plain` flag** when viewing/listing for AI-friendly output

## Typical Workflow

```bash
# 1. Find work
backlog task list -s "To Do" --plain

# 2. Read task
backlog task 42 --plain

# 3. Start work
backlog task edit 42 -s "In Progress" -a @myself

# 4. Add plan
backlog task edit 42 --plan $'1. Research\n2. Implement\n3. Test'

# 5. Work on the task (write code, test)

# 6. Mark criteria complete
backlog task edit 42 --check-ac 1 --check-ac 2 --check-ac 3

# 7. Add notes
backlog task edit 42 --notes $'Implemented feature X\n- Modified files A, B\n- Added tests'

# 8. Mark done
backlog task edit 42 -s Done
```

## File Structure (Read-Only Reference)

Tasks live in `backlog/tasks/` as `task-<id> - <title>.md` files. Never edit these directly!

**Task Structure (for viewing only):**
```markdown
---
id: task-42
title: Add GraphQL resolver
status: To Do
assignee: [@sara]
labels: [backend, api]
---

## Description
Brief explanation of the task purpose.

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 First criterion
- [x] #2 Second criterion (completed)
- [ ] #3 Third criterion
<!-- AC:END -->

## Implementation Plan
1. Research approach
2. Implement solution

## Implementation Notes
Summary of what was done.
```

## Remember

**🎯 The Golden Rule:** If you want to change ANYTHING in a task, use `backlog task edit`.

**📖 CLI is the interface** - it handles Git, metadata, relationships, and file naming.

For complete help: `backlog --help`
