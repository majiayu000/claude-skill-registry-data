---
name: dex-workflow
description: |
  This skill should be used when implementing features from a PRD spec, tracking
  implementation progress, or resuming work across sessions. Covers Dex task
  management for PRD story execution, daily workflows, and skill auto-loading.
version: 2.0.0
---

# Dex Workflow - Task-Based Feature Implementation

**Current branch:** !`git branch --show-current 2>/dev/null || echo "not in git repo"`
**Task status:** !`dex status 2>/dev/null | head -5 || echo "dex not configured"`

Dex is a CLI for persistent task tracking across sessions. Tasks sync with
GitHub issues and support native cross-session resume.

## When to Use Dex Workflow

- Implementing stories from a PRD spec
- Tracking implementation progress across sessions
- Resuming work after `/clear` or session restart
- When you need GitHub issue sync

## Daily Workflow

### Check Status

```bash
dex status                  # Dashboard with stats, ready tasks, recent completions
dex list                    # All pending tasks (tree view)
dex list --ready            # Unblocked tasks ready to work
dex list --in-progress      # Currently claimed tasks
dex list --blocked          # Tasks waiting on dependencies
```

### Start Working

```bash
dex list --ready            # See what's available
dex show <id> --full        # Read full task details
dex start <id>              # Claim the task (marks in-progress)
```

If task has skills metadata, load them first:
```bash
# Look for "Skills:" line in task description
/Skill <skill-name>
```

### Complete a Task

Use `/complete` command (wraps reviewers + dex complete):
```bash
/complete <task-id>
```

Or manually:
1. Run reviewers (code-simplifier + kieran)
2. Address findings
3. Commit with task reference
4. Mark complete with verified result:
```bash
dex complete <id> --result "What changed: X. Verification: N tests passing."
```

### GitHub Sync

```bash
dex sync                    # Push tasks to GitHub issues
dex sync --github           # Explicit GitHub sync
dex import #123             # Import existing GitHub issue
dex export <id>             # One-time export (no sync)
```

## Task Creation from PRD Spec

### Using `dex plan` (Recommended)

After writing spec with Implementation Stories section:

```bash
dex plan plans/<feature>/spec.md
```

This automatically:
1. Creates parent task from spec title
2. Analyzes Implementation Stories section for subtasks
3. Generates subtasks with proper hierarchy

**Our spec structure is designed for `dex plan`:**
```markdown
## Implementation Stories

### Story 1: Create login form
**Category:** ui
**Skills:** frontend-design
**Blocked by:** none
**Acceptance Criteria:**
- [ ] Form renders with inputs
- [ ] Validation works
```

The CLI parses headings (`### Story N:`) as subtask titles and preserves the description content including Category, Skills, and Acceptance Criteria.

**Dex also provides skills for interactive use:**
- `/dex` - Natural language task management
- `/dex-plan` - AI-powered markdown → tasks conversion

Install with `npx skills add dcramer/dex`. These are useful for ad-hoc work, but CLI commands are more reliable in automated workflows (stop hooks, etc.).

### Manual Creation (if needed)

```bash
# Create epic for the feature
dex create "feature-name" -d "Feature: ..."

# Create stories as child tasks
dex create "Story 1: title" --parent <epic-id> -d "
Category: ui
Skills: frontend-design

Acceptance Criteria:
- [ ] Criterion 1
- [ ] Criterion 2
"

# Set dependencies
dex create "Story 2: ..." --blocked-by <story1-id>
```

## Cross-Session Resume

After `/clear` or new session:

1. `dex status` - See dashboard
2. `dex list --in-progress` - Check if you were mid-task
3. `dex list --ready` - See what's next
4. `dex show <id> --expand` - Get full context with ancestors
5. Load required skills
6. Continue implementation

## Task Metadata Structure

Tasks from PRD specs include:
- **Category**: functional, ui, integration, edge-case, performance
- **Skills**: skill names to load before implementation
- **Acceptance Criteria**: verification checklist
- **Blocked by**: dependency references

## Command Reference

```bash
# Status & Listing
dex status                  # Dashboard view
dex list                    # Pending tasks (tree)
dex list --ready            # Unblocked only
dex list --in-progress      # Currently claimed
dex list --query "auth"     # Search tasks

# Task Details
dex show <id>               # Basic details
dex show <id> --full        # Full untruncated output
dex show <id> --expand      # Include ancestor descriptions

# Working
dex start <id>              # Mark as in-progress
dex start <id> --force      # Reclaim from another agent
dex complete <id> --result "What changed: X. Verification: N tests passing."

# Editing
dex edit <id> -n "new name"
dex edit <id> -d "new description"
dex edit <id> --add-blocker <other-id>

# Creating
dex create "name" -d "description"
dex create "name" --parent <id> --blocked-by <id>
dex plan <file.md>          # Auto-create from markdown

# GitHub Integration
dex sync                    # Sync to GitHub issues
dex import #123             # Import issue
dex export <id>             # One-time export

# Maintenance
dex archive <id>            # Compact completed task tree
dex doctor                  # Validate storage
dex doctor --fix            # Auto-repair issues
```

## Quality Expectations

Production code only:
- Pre-commit reviews required (code-simplifier + kieran)
- Atomic commits per task
- All tests/lint/types must pass

**Result must include verification:**
- ✅ "Added X. 12 tests passing. Build success."
- ❌ "Should work" or "Made changes" (unverified claims)

**Note:** Parent tasks cannot complete until all subtasks are done.

## Related Commands

- `/prd` - Create PRD with Dex handoff (Phase 4)
- `/complete` - Complete task with reviewer workflow
- `/ut` - Unit test coverage with Dex tracking
- `/e2e` - E2E tests with Dex tracking
