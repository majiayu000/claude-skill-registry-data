---
name: verk
description: "Manage tasks, projects, and workflows in Verk — AI-powered task management. Create, update, assign, and track tasks. Add comments, change status, list automation flows."
metadata:
  openclaw:
    emoji: "⚡"
    requires:
      env:
        - VERK_API_KEY
        - VERK_ORG_ID
      bins:
        - node
    primaryEnv: VERK_API_KEY
  minis:
    originalSource: "https://clawskills.sh/skills/abhibavishi-verk"
    convertedAt: "2026-10-31T22:14:52.728Z"
    license: "Unknown"
---

# Verk Task Management

You can manage tasks, projects, and automation flows in Verk using the `verk-cli.mjs` CLI tool.

## Available Commands

### Tasks

- **List tasks**: `node scripts/verk-cli.mjs tasks list [--status STATUS] [--priority PRIORITY] [--search QUERY]`
- **Get task**: `node scripts/verk-cli.mjs tasks get <taskId>`
- **Create task**: `node scripts/verk-cli.mjs tasks create --title "Title" [--description "Desc"] [--status STATUS] [--priority PRIORITY] [--assigned userId1,userId2]`
- **Update task**: `node scripts/verk-cli.mjs tasks update <taskId> [--title "New Title"] [--status STATUS] [--priority PRIORITY] [--assigned userId1,userId2]`
- **Delete task**: `node scripts/verk-cli.mjs tasks delete <taskId>`
- **Comment on task**: `node scripts/verk-cli.mjs tasks comment <taskId> --text "Comment text"`

### Projects

- **List projects**: `node scripts/verk-cli.mjs projects list`

### Flows (Automation Workflows)

- **List flows**: `node scripts/verk-cli.mjs flows list`

## Valid Values

- **Status**: `Backlog`, `Todo`, `In-Progress`, `Review`, `Done`
- **Priority**: `Urgent`, `High`, `Medium`, `Low`, `None`

## When to Use Each Command

- When asked to see what tasks exist, use `tasks list`. Add `--status` or `--priority` to filter, or `--search` to find specific tasks.
- When asked about a specific task, use `tasks get <taskId>`.
- When asked to create a task, use `tasks create` with at least a `--title`.
- When asked to update, change, or modify a task, use `tasks update <taskId>` with the fields to change.
- When asked to mark a task as done/complete, use `tasks update <taskId> --status Done`.
- When asked to assign a task, use `tasks update <taskId> --assigned userId`.
- When asked to delete or remove a task, use `tasks delete <taskId>`.
- When asked to comment on or add a note to a task, use `tasks comment <taskId> --text "..."`.
- When asked about projects, use `projects list`.
- When asked about automation workflows, use `flows list`.
- To see comments on a task, use `tasks get <taskId>` — comments are included in the task response.

## Output Format

All commands return JSON. Parse the output to extract relevant information for the user. When listing tasks, summarize key fields (title, status, priority, assignee) rather than dumping raw JSON.

## Examples

```bash
# List all high-priority tasks
node scripts/verk-cli.mjs tasks list --priority High

# Create a task and assign it
node scripts/verk-cli.mjs tasks create --title "Review Q2 roadmap" --priority High --status Todo

# Mark a task as done
node scripts/verk-cli.mjs tasks update task-abc123 --status Done

# Add a comment
node scripts/verk-cli.mjs tasks comment task-abc123 --text "Completed the review, looks good"
```
