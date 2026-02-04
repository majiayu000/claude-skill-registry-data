---
name: sprint-orchestrator
description: "Manage multi-project sprints with daily planning, progress tracking, and context switching. Use when coordinating work across multiple repositories."
---

# Sprint Orchestrator

Coordinate development across multiple projects with systematic tracking.

## Critical Rule

**Never execute git commands.** Always output git commands for manual execution.

## Daily Workflow

### Morning: Generate Tasks
```markdown
## Today's Focus: Day [X] of [Total]

### Primary Project: [Name]
**Tasks:**
1. [P0] [Task]
2. [P1] [Task]

### Secondary Project: [Name]
**Tasks:**
1. [P1] [Task]
```

### During Work: Log Progress
```markdown
## Progress: [Project] - [Date]

### Completed
- [x] Task description

### Next Steps
- [ ] Remaining task

### Git Commands to Run
```bash
git add .
git commit -m "feat: description"
```
```

### Project Switch: Context Handoff
```markdown
# Handoff: [From] → [To]

## Exiting [From]
- **Summary:** What was done
- **State:** Current status
- **Resume:** Instructions for continuing

## Git Commands Before Switch
```bash
git add .
git commit -m "wip: in progress"
```

## Entering [To]
- **Last session:** Previous state
- **Today's focus:** Priority tasks
```

### End of Day: Summary
```markdown
# Daily Summary: Day [X]

| Project | Tasks Done | Time |
|---------|-----------|------|
| project | task list | Xh |

## Tomorrow
1. Primary: [Project] - [Focus]
2. Secondary: [Project] - [Focus]
```

## Best Practices

1. Never switch mid-task—complete or checkpoint first
2. Log progress immediately after completing work
3. Generate handoff document before every switch
4. All git commands output only, never executed

See `references/templates.md` for full templates.
