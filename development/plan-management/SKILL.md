---
name: plan-management
description: >
  Expert in creating, updating, and managing feature implementation plans.
  Use when creating new plans with /plan command, updating plan status,
  marking phases in_progress or completed, checking plan progress, or
  understanding plan structure. Ensures plans are created correctly and
  updated efficiently using the plan-update.py utility.
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
---

# Plan Management Skill

This skill provides expertise in creating and managing structured feature implementation plans. Plans track multi-phase feature development with subagent assignments, dependencies, and progress tracking.

## Plan Location and Structure

- **Active Plans:** `Docs/Plans/plan-*.json`
- **Completed Plans:** `Docs/Plans/Completed/`
- **Template:** `Docs/Plans/plan-template.json`
- **Update Utility:** `Docs/Plans/plan-update.py`
- **Creation Command:** `.claude/commands/plan.md` (invoked via `/plan`)

## Quick Reference: Plan Update Commands

### For Agents Working on Plans

Use these commands to update plans efficiently **without parsing the full JSON**:

```bash
# Check current status - what's in progress, what's next?
python Docs/Plans/plan-update.py <plan-file> --status-check

# See phases assigned to you
python Docs/Plans/plan-update.py <plan-file> --my-assignment <agent-name>

# Start the next available phase (checks dependencies)
python Docs/Plans/plan-update.py <plan-file> --start-next

# Complete the current in_progress phase
python Docs/Plans/plan-update.py <plan-file> --complete-current

# Complete with notes explaining what was done
python Docs/Plans/plan-update.py <plan-file> --complete-current --completion-notes "Implemented webhook handler with retry logic"

# Complete with notes and effort tracking
python Docs/Plans/plan-update.py <plan-file> --complete-current --completion-notes "All tests passing" --actual-effort 4.5

# View full summary
python Docs/Plans/plan-update.py <plan-file> --summary
```

### Detailed Updates

```bash
# Start a specific phase
python Docs/Plans/plan-update.py <plan-file> --phase 2 --status in_progress

# Update completion percentage
python Docs/Plans/plan-update.py <plan-file> --phase 2 --completion 75

# Record actual effort hours
python Docs/Plans/plan-update.py <plan-file> --phase 2 --actual-effort 6.5

# Complete a specific step within a phase
python Docs/Plans/plan-update.py <plan-file> --phase 2 --step 3 --status completed

# Multiple updates in one transaction
python Docs/Plans/plan-update.py <plan-file> --phase 2 --status in_progress --completion 50 --actual-effort 3
```

## Agent Workflow for Executing Plans

### 1. Before Starting Work

```bash
# Check what's assigned to you
python Docs/Plans/plan-update.py Docs/Plans/plan-feature-name-MM-DD-YY.json --my-assignment supabase-backend-specialist

# Or check overall status
python Docs/Plans/plan-update.py Docs/Plans/plan-feature-name-MM-DD-YY.json --status-check
```

### 2. When Starting a Phase

```bash
# Start the next available phase (recommended - checks dependencies automatically)
python Docs/Plans/plan-update.py Docs/Plans/plan-feature-name-MM-DD-YY.json --start-next

# Or start a specific phase
python Docs/Plans/plan-update.py Docs/Plans/plan-feature-name-MM-DD-YY.json --phase 2 --status in_progress
```

### 3. During Work - Update Progress

```bash
# Update completion as you progress
python Docs/Plans/plan-update.py Docs/Plans/plan-feature-name-MM-DD-YY.json --phase 2 --completion 50

# Mark individual steps complete (auto-updates phase completion %)
python Docs/Plans/plan-update.py Docs/Plans/plan-feature-name-MM-DD-YY.json --phase 2 --step 1 --status completed
python Docs/Plans/plan-update.py Docs/Plans/plan-feature-name-MM-DD-YY.json --phase 2 --step 2 --status completed
```

### 4. When Completing a Phase

```bash
# Complete the current phase (recommended - finds in_progress phase automatically)
python Docs/Plans/plan-update.py Docs/Plans/plan-feature-name-MM-DD-YY.json --complete-current

# Complete with notes explaining what was accomplished
python Docs/Plans/plan-update.py Docs/Plans/plan-feature-name-MM-DD-YY.json --complete-current --completion-notes "Implemented RLS policies and tested with service role"

# Complete with notes AND effort tracking (recommended)
python Docs/Plans/plan-update.py Docs/Plans/plan-feature-name-MM-DD-YY.json --complete-current --completion-notes "All migrations applied successfully" --actual-effort 3.5

# Or complete a specific phase with notes
python Docs/Plans/plan-update.py Docs/Plans/plan-feature-name-MM-DD-YY.json --phase 2 --status completed --completion-notes "Webhook handler deployed" --actual-effort 5.5
```

### 5. Auto-Archive on Plan Completion

When ALL phases are marked `completed`:
- The plan is automatically moved to `Docs/Plans/Completed/`
- `metadata.completed_at` is set
- `metadata.status` is set to "completed"
- `metadata.total_actual_effort` is calculated

## Phase Index for Quick Lookups

Every plan includes a `phase_index` field that's auto-updated:

```json
{
  "phase_index": {
    "total": 4,
    "current_in_progress": 2,
    "completed": [1],
    "blocked": [],
    "not_started": [3, 4],
    "next_available": 3
  }
}
```

This allows quick status checks without parsing the full `phases` array.

## Creating New Plans

Use the `/plan` slash command:

```
/plan Implement real-time notifications for transaction updates
```

The `/plan` command will:
1. Research existing code and patterns (Step 0)
2. Analyze the feature request
3. Generate 3-5 implementation phases
4. Assign appropriate subagents
5. Calculate effort estimates with multipliers
6. Create dependency graph
7. Define rollback strategy
8. Save to `Docs/Plans/plan-<feature>-MM-DD-YY.json`

## Plan Structure Overview

```json
{
  "metadata": {
    "created": "ISO-8601",
    "plan_id": "UUID",
    "version": "2.1",
    "status": "active|completed"
  },
  "phase_index": { /* quick lookup */ },
  "planning": { "goal", "reason", "scope", "priority" },
  "exploration_summary": { /* research findings */ },
  "phases": [
    {
      "number": 1,
      "name": "Phase Name",
      "status": "not_started|in_progress|completed|blocked",
      "completion_percentage": 0,
      "assigned_subagent": "agent-name",
      "steps": [ /* individual tasks */ ],
      "dependencies": [ /* phase numbers */ ],
      "deliverables": [ /* outputs */ ]
    }
  ],
  "subagent_assignments": [ /* who does what */ ],
  "rollback_strategy": { /* how to undo */ },
  "dependency_graph": { "ascii": "Phase 1 -> Phase 2" }
}
```

## Status Transitions

Valid status transitions (enforced by plan-update.py):

- `not_started` -> `in_progress` or `blocked`
- `in_progress` -> `completed` or `blocked`
- `blocked` -> `in_progress`
- `completed` -> (none, final state)

Use `--force` to override transitions if needed.

## Dependency Validation

The `--start-next` command automatically:
1. Finds the first `not_started` phase
2. Checks if all dependencies are `completed`
3. Only starts if dependencies are satisfied
4. Reports blocking phases if not

## Best Practices

1. **Always use plan-update.py** - Never manually edit plan JSON
2. **Mark in_progress before starting** - Visibility for other agents
3. **Update completion incrementally** - Track progress as you work
4. **Record actual effort** - Improves future estimates
5. **Complete phases promptly** - Enables dependent phases to start
6. **Use --status-check first** - Understand current state before acting

## Troubleshooting

### "Phase X blocked by dependencies"
The phase depends on other phases that aren't completed yet. Check `--status-check` to see blocking phases.

### "No phase currently in_progress"
No phase has `status: in_progress`. Use `--start-next` to begin the next phase.

### "Phase X is already in_progress"
Complete the current phase before starting a new one, or use `--force` to start anyway.

### Plan not auto-archiving
Ensure ALL phases have `status: completed`. Use `--summary` to verify.

## See Also

- [plan.md](.claude/commands/plan.md) - Plan creation command
- [plan-template.json](Docs/Plans/plan-template.json) - Full template reference
- [plan-update.py](Docs/Plans/plan-update.py) - Update utility source
- [agent-index.md](.claude/agents/agent-index.md) - Available subagents
