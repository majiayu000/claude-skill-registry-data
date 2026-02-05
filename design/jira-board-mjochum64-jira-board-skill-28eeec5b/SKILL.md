---
name: jira-board
description: "Organize and manage Jira boards, issues, and sprints. Use when the user wants to: (1) List, create, update, or transition Jira issues, (2) View or manage sprints, (3) Assign issues or change status, (4) Query issues with JQL, (5) Manage Jira boards. Requires environment variables JIRA_URL, JIRA_USERNAME, JIRA_API_TOKEN, and optionally JIRA_PROJECTS_FILTER."
---

# Jira Board Organization

Manage Jira boards, issues, and sprints via the Jira REST API.

## Environment Variables

Required:
- `JIRA_URL`: Jira instance URL (e.g., `https://company.atlassian.net`)
- `JIRA_USERNAME`: Jira username/email
- `JIRA_API_TOKEN`: API token from https://id.atlassian.com/manage-profile/security/api-tokens

Optional:
- `JIRA_PROJECTS_FILTER`: Comma-separated project keys to filter by default (e.g., `PROJ,DEV`)

## Quick Start

Use `scripts/jira_api.py` for all Jira operations:

```bash
# List issues in filtered projects
python scripts/jira_api.py issues

# List my issues in active sprint
python scripts/jira_api.py issues --assignee me --sprint active

# Create an issue
python scripts/jira_api.py create PROJ "Fix login bug" --type Bug --priority High

# Transition issue status
python scripts/jira_api.py transition PROJ-123 "In Progress"

# Assign issue
python scripts/jira_api.py assign PROJ-123 me
```

## Issue Operations

### List Issues
```bash
python scripts/jira_api.py issues [options]
  --project, -p    Project key(s), comma-separated
  --status, -s     Filter by status
  --assignee, -a   Filter by assignee ('me' for yourself)
  --sprint         Filter by sprint ('active' for current)
  --jql            Custom JQL query
  --max            Max results (default: 50)
  --verbose, -v    Show detailed output
```

### Get Issue Details
```bash
python scripts/jira_api.py get PROJ-123
```

### Create Issue
```bash
python scripts/jira_api.py create PROJECT "Summary" [options]
  --type, -t       Issue type (default: Task)
  --description, -d  Description
  --assignee, -a   Assignee
  --priority, -p   Priority
  --labels, -l     Labels (space-separated)
```

### Update Issue
```bash
python scripts/jira_api.py update PROJ-123 [options]
  --summary, -s    New summary
  --description, -d  New description
  --assignee, -a   New assignee
  --priority, -p   New priority
  --labels, -l     New labels
```

### Transition Issue
```bash
python scripts/jira_api.py transition PROJ-123 "Done"
```

### Assign Issue
```bash
python scripts/jira_api.py assign PROJ-123 username
python scripts/jira_api.py assign PROJ-123 me  # Assign to yourself
```

### Add Comment
```bash
python scripts/jira_api.py comment PROJ-123 "Comment text"
```

## Board Operations

### List Boards
```bash
python scripts/jira_api.py boards [--project PROJECT]
```

### List Board Issues
```bash
python scripts/jira_api.py board-issues BOARD_ID [--sprint active] [-v]
```

## Sprint Operations

### List Sprints
```bash
python scripts/jira_api.py sprints BOARD_ID [--state active|future|closed]
```

### Create Sprint
```bash
python scripts/jira_api.py create-sprint BOARD_ID "Sprint Name" [options]
  --start    Start date (ISO format: 2024-01-15)
  --end      End date
  --goal     Sprint goal
```

### Start/Close Sprint
```bash
python scripts/jira_api.py start-sprint SPRINT_ID [--start DATE] [--end DATE]
python scripts/jira_api.py close-sprint SPRINT_ID
```

### Move Issues to Sprint
```bash
python scripts/jira_api.py move-to-sprint SPRINT_ID PROJ-1 PROJ-2 PROJ-3
```

### List Sprint Issues
```bash
python scripts/jira_api.py sprint-issues SPRINT_ID [-v]
```

## Common Workflows

### Daily Standup Review
```bash
# Show my active sprint issues
python scripts/jira_api.py issues --assignee me --sprint active -v
```

### Sprint Planning
```bash
# List backlog issues
python scripts/jira_api.py issues --status "To Do" --project PROJ

# Move issues to sprint
python scripts/jira_api.py move-to-sprint 42 PROJ-100 PROJ-101 PROJ-102
```

### Status Update
```bash
# Start working on issue
python scripts/jira_api.py transition PROJ-123 "In Progress"
python scripts/jira_api.py assign PROJ-123 me

# Complete issue
python scripts/jira_api.py transition PROJ-123 "Done"
```

## JQL Examples

Custom queries with `--jql`:

```bash
# High priority bugs
python scripts/jira_api.py issues --jql 'priority = High AND type = Bug'

# Recently updated
python scripts/jira_api.py issues --jql 'updated >= -7d ORDER BY updated DESC'

# Unassigned in project
python scripts/jira_api.py issues --jql 'project = PROJ AND assignee IS EMPTY'
```
