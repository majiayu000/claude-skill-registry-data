---
name: work-plan
description: This skill should be used when the user asks to "show work plan", "what's the plan for feature N", "show progress", "view execution plan", or wants to see phase breakdown, progress status, and next actions for a feature.
---

# Work Plan

Generate a comprehensive execution plan showing current status, phase breakdown, and next actions.

## User Input

FEATURE_ID = $ARGUMENT (optional, defaults to current branch feature)

Accept feature ID like "001" or "001-mcp-integration". If not provided, extract from current git branch.

## Workflow

### Step 1: Extract Feature ID

1. If ARGUMENT provided:
   - Format "NNN" (e.g., "001"): Search `backlog/plans/` and `backlog/plans/_completed/` for matching folder
   - Format "NNN-slug" (e.g., "001-mcp-integration"): Use directly
2. If no ARGUMENT:
   - Run `git branch --show-current`
   - Extract feature ID from branch name (e.g., `feature/001-mcp-integration` → `001-mcp-integration`)
   - If not on a feature branch, show error and list available features

**Note**: In-progress features are in `backlog/plans/{NNN}-{slug}/`, completed features in `backlog/plans/_completed/{NNN}-{slug}/`

### Step 2: Load Feature Context

Read the following files:
- `{feature-path}/tasks.md` (required)
- `{feature-path}/spec.md` (for feature name/description)
- `specs/tests/{feature-id}.md` (if exists, for spec test info)
- Current git branch status

### Step 3: Parse tasks.md

Extract:

**Phase Information**:
- Phase headers: `## Phase N: Name`
- For each phase: number, name, description, task range, task count, completed count
- Entry spec test task (`[SPEC]` with "→ expect ALL FAIL")
- Exit spec test task (`[SPEC]` with "→ expect ALL PASS")

**Dependency Information**:
- Find dependency diagram (after "## Dependencies" header)
- Parse dependency arrows (──►, ──┬──►, etc.)
- Build dependency graph

**Overall Metrics**:
- Total task count, completed count, percentage

### Step 4: Determine Status

For each phase:
- **Complete**: All tasks checked (`- [x]`)
- **In Progress**: Some tasks checked
- **Not Started**: No tasks checked
- **Blocked**: Depends on incomplete phases

Identify current phase and next action.

### Step 5: Generate Work Plan

Output sections (see `references/output-format.md` for detailed templates):

1. **Current Status** - Feature name, branch, progress, current phase
2. **Phase Overview** - Table with status, progress, blocks
3. **Recommended Execution Plan** - Per-phase commands and goals
4. **Parallel Execution Strategy** - Wave structure for independent phases
5. **Quick Commands Reference** - Command table
6. **Success Criteria** - Completion checklist
7. **Manual Testing Strategy** - What needs manual testing and when
8. **Next Action** - Specific recommended command

### Next Action Logic

| State | Recommendation |
|-------|----------------|
| Wrong branch / no tasks | Prime and start Phase 1 |
| Phase in progress | Continue current phase |
| Phase blocked | Complete blocking phase first |
| Ready for next | Start next phase |
| Multiple independent ready | Run phases in parallel |
| All complete | Final verification, create PR |

## Error Handling

**Feature not found**:
```
❌ Error: Feature '{feature-id}' not found

Available features:
{list folders in backlog/plans/ and backlog/plans/_completed/}

Usage: /work-plan {feature-number}
```

**tasks.md not found**:
```
❌ Error: tasks.md not found at {feature-path}/tasks.md

This feature may not follow the methodology structure.
```

## Output Guidelines

- Keep output concise but actionable
- Use emojis for visual clarity (✓, ⚠️, ✅, 🔄, ⏸️, 🔒)
- Provide specific commands, not just guidance
- Always include "Next Action" - never leave user wondering what to do

## Additional Resources

### Reference Files

For detailed output templates, consult:
- **`references/output-format.md`** - Full templates for all output sections
