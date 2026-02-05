---
name: jira-discipline
description: Use this skill when discussing code changes, implementation work, feature status, or when starting/completing development tasks. Reminds about Jira issue tracking discipline - always having an issue in progress before writing code, transitioning to done, and creating Subtasks for unexpected scope. Triggers when users mention implementing features, writing code, or checking on work status.
---

# Jira Discipline Skill

This skill ensures proper Jira issue tracking discipline is maintained throughout development conversations.

## When to Use

Apply this skill when:
- Users mention they're about to start coding something
- Discussing implementation without mentioning a Jira issue
- Users complete work and might forget to update Jira
- Unexpected scope or bugs are discovered during work
- Checking on feature or work status

## Core Discipline Rules

### Rule 1: No Code Without an Issue
**Never write code without a Jira issue in "In Progress" status.**

Before any implementation work:
1. Ensure a Jira issue exists for the work
2. Transition the issue to "In Progress"
3. Only then begin writing code

### Rule 2: Transition Work Complete Immediately
**When work is done, immediately transition in Jira.**

1. Commit the code changes
2. Transition the Jira issue to "Done"
3. Don't batch status updates

### Rule 3: Subtasks Are Mandatory
**A Story is NOT done until all Subtasks are done.**

- Track progress at the Subtask level
- Transition each Subtask to "Done" as completed
- Parent Story stays open until all Subtasks complete

### Rule 4: Create Missing Scope
**If you discover work that needs doing but has no issue, create a Subtask first.**

- Found a bug? Create a bug Subtask first
- Need to refactor? Create a REFACTOR Subtask first
- Missing functionality? Create a new Subtask first

Always: Create Subtask → Transition "In Progress" → Do work → Transition "Done"

## Jira Status Transitions

Unlike Linear where you set status directly, Jira uses **transitions**:

```
To Do → In Progress → Done
          ↓
     (If blocked)
          ↓
       Blocked → In Progress → Done
```

Use `mcp__mcp-atlassian__jira_get_transitions` to see available transitions, then `mcp__mcp-atlassian__jira_transition_issue` to execute them.

## Gentle Reminders

### When User Says They're Starting Work
> "Before we begin, let's make sure there's a Jira issue for this work. Is there an existing issue we should transition to 'In Progress', or should we create a Subtask?"

### When User Completes Something
> "Great work! Don't forget to transition the Jira issue to 'Done' to keep tracking accurate."

### When Unexpected Work Appears
> "This looks like new scope. Let's create a Subtask for it before we implement it."

## Integration with Workflow

This discipline integrates with:
- `/planFeature` - Creates properly structured Stories with Subtasks
- `/work-on-feature` - Enforces status tracking during execution
- `execute-issue-jira` agent - Automatically manages transitions

Remember: **Jira is the source of truth. Keep it accurate.**
