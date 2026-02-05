---
name: linear-discipline
description: Use this skill when discussing code changes, implementation work, feature status, or when starting/completing development tasks. Reminds about Linear issue tracking discipline - always having an issue in progress before writing code, marking work as done, and creating issues for unexpected scope. Triggers when users mention implementing features, writing code, or checking on work status.
---

# Linear Discipline Skill

This skill ensures proper Linear issue tracking discipline is maintained throughout development conversations.

## When to Use

Apply this skill when:
- Users mention they're about to start coding something
- Discussing implementation without mentioning a Linear issue
- Users complete work and might forget to update Linear
- Unexpected scope or bugs are discovered during work
- Checking on feature or work status

## Core Discipline Rules

### Rule 1: No Code Without an Issue
**Never write code without a Linear issue in "In Progress" status.**

Before any implementation work:
1. Ensure a Linear issue exists for the work
2. Mark the issue as "In Progress"
3. Only then begin writing code

### Rule 2: Mark Work Complete Immediately
**When work is done, immediately update Linear.**

1. Commit the code changes
2. Mark the Linear issue as "Done"
3. Don't batch status updates

### Rule 3: Sub-Issues Are Mandatory
**A parent issue is NOT done until all sub-issues are done.**

- Track progress at the sub-issue level
- Mark each sub-issue "Done" as completed
- Parent issue stays open until all children complete

### Rule 4: Create Missing Scope
**If you discover work that needs doing but has no issue, create one first.**

- Found a bug? Create a bug issue first
- Need to refactor? Create a refactor issue first
- Missing functionality? Create a sub-issue first

Always: Create issue → Mark "In Progress" → Do work → Mark "Done"

## Gentle Reminders

### When User Says They're Starting Work
> "Before we begin, let's make sure there's a Linear issue for this work. Is there an existing issue we should mark 'In Progress', or should we create one?"

### When User Completes Something
> "Great work! Don't forget to mark the Linear issue as 'Done' to keep tracking accurate."

### When Unexpected Work Appears
> "This looks like new scope. Let's create a sub-issue for it before we implement it, so it's properly tracked."

## Status Flow

```
Todo → In Progress → Done
         ↓
    (If blocked)
         ↓
      Blocked → In Progress → Done
```

## Integration with Workflow

This discipline integrates with:
- `/planFeature` - Creates properly structured issues
- `/work-on-feature` - Enforces status tracking during execution
- `execute-issue` agent - Automatically manages status transitions

Remember: **Linear is the source of truth. Keep it accurate.**
