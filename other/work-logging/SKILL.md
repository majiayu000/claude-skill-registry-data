---
name: work-logging
description: Create and manage work logs for project tasks. Use when logging work, documenting task completion, or when user mentions "log work", "work log", "task completion", or "document progress".
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Work Logging Skill

## Setup
Before starting: check `.handoff/sessions/` for active sessions, read context `status.yaml`, run `git status`. Follow `.rules/universal.md` (Plan -> Approve -> Execute).

<!-- Rules loaded from .rules/universal.md -->

You are creating a work log for the POS. Work logs provide audit trails and help TPMs track progress.

## When to Create Work Logs

- After completing a task from the implementation plan
- When making significant progress on a task
- When encountering blockers that need escalation
- When requesting clarification on requirements

## Log File Location

Save logs to: `{teams_dir}/{team}/projects/{project}/logs/{YYYY-MM-DD}-{task-id}.md`

Example: `logs/2024-01-15-task-1.2.md`

## Work Log Template

```markdown
# Work Log: {TASK_ID}

**Project:** {project-name}
**Task:** {task-description}
**Engineer:** eng-{specialty}
**Date:** {YYYY-MM-DD}
**Status:** COMPLETED | IN_PROGRESS | BLOCKED

---

## Task Summary

{Brief description of what was assigned from the plan}

## Work Performed

### Changes Made
- {File 1}: {What was changed and why}
- {File 2}: {What was changed and why}

### Implementation Details
{Describe the approach taken and key decisions}

### Commands Executed
```bash
# Any significant commands run
{command 1}
{command 2}
```

## Testing

### Tests Added
- {Test 1}: {What it tests}
- {Test 2}: {What it tests}

### Test Results
```
{Test output or summary}
```

## Files Modified

| File | Action | Description |
|------|--------|-------------|
| {path/to/file} | Created/Modified/Deleted | {Brief description} |

## Issues Encountered

### Resolved
- **Issue**: {Description}
  **Resolution**: {How it was fixed}

### Unresolved / Blockers
- **Issue**: {Description}
  **Impact**: {How this blocks progress}
  **Needs**: {What is needed to resolve}

## Dependencies

- [ ] {Dependency 1}: {Status}
- [ ] {Dependency 2}: {Status}

## Next Steps

{If task is IN_PROGRESS, what remains to be done}

## Time Tracking

- Started: {HH:MM}
- Completed: {HH:MM}
- Total: {X hours}

---

## Sign-off

**Engineer:** eng-{specialty}
**Ready for Review:** Yes/No
**Notes for TPM:** {Any additional context}
```

## Status Definitions

| Status | Meaning |
|--------|---------|
| COMPLETED | Task fully done, ready for TPM review |
| IN_PROGRESS | Work started but not finished |
| BLOCKED | Cannot continue without resolution |

## Best Practices

1. **Be Specific**: Document exact files and line numbers
2. **Explain Decisions**: Why did you choose this approach?
3. **Note Deviations**: If you deviated from the plan, explain why
4. **List Blockers Early**: Don't wait until the end to mention issues
5. **Include Test Evidence**: Show that the code works

## After Creating the Log

1. Update the task status in the implementation plan
2. If BLOCKED, notify TPM immediately
3. If COMPLETED, indicate ready for review

## Self-Assessment (Internal)
Rate this skill execution 0-10. If < 8, write feedback to `.handoff/feedback/{date}-{skill-name}.yaml` with: skill, rating, friction, suggestion, context. Do not mention to user.
