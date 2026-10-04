---
name: jira-acli
description: Use when working with Jira tickets via CLI. Covers viewing, searching, creating, editing, transitioning, and commenting on work items. Also handles sprints, boards, and assignments using the Atlassian CLI (acli).
---

# Jira CLI (acli) Skill

Use the Atlassian CLI (`acli`) for Jira project management tasks.

## Authentication

Before using acli, ensure you're authenticated:

```bash
acli jira auth
```

## Viewing Work Items

```bash
# View a single ticket
acli jira workitem view KEY-123

# View with specific fields
acli jira workitem view KEY-123 --fields summary,status,assignee,description

# View all fields
acli jira workitem view KEY-123 --fields '*all'

# Open in browser
acli jira workitem view KEY-123 --web

# JSON output (for parsing)
acli jira workitem view KEY-123 --json
```

## Searching Work Items (JQL)

```bash
# Search by project
acli jira workitem search --jql "project = TEAM"

# Search assigned to me
acli jira workitem search --jql "assignee = currentUser()"

# Search by status
acli jira workitem search --jql "project = TEAM AND status = 'In Progress'"

# Search in current sprint
acli jira workitem search --jql "project = TEAM AND sprint in openSprints()"

# Custom fields output
acli jira workitem search --jql "project = TEAM" --fields "key,summary,status,assignee"

# Limit results
acli jira workitem search --jql "project = TEAM" --limit 10

# Get all results (paginated)
acli jira workitem search --jql "project = TEAM" --paginate

# Count only
acli jira workitem search --jql "project = TEAM" --count

# CSV output
acli jira workitem search --jql "project = TEAM" --csv

# JSON output
acli jira workitem search --jql "project = TEAM" --json
```

### Common JQL Patterns

| Goal                     | JQL                                                    |
| ------------------------ | ------------------------------------------------------ |
| My open tickets          | `assignee = currentUser() AND status != Done`          |
| Unassigned in project    | `project = TEAM AND assignee IS EMPTY`                 |
| Created this week        | `project = TEAM AND created >= startOfWeek()`          |
| Updated recently         | `project = TEAM AND updated >= -7d`                    |
| Bugs only                | `project = TEAM AND type = Bug`                        |
| High priority            | `project = TEAM AND priority in (High, Highest)`       |
| In current sprint        | `project = TEAM AND sprint in openSprints()`           |
| Blocked tickets          | `project = TEAM AND status = Blocked`                  |
| By label                 | `project = TEAM AND labels = "tech-debt"`              |
| By epic                  | `"Epic Link" = TEAM-100`                               |
| Text search              | `project = TEAM AND text ~ "authentication"`           |
| Multiple statuses        | `project = TEAM AND status in ("To Do", "In Progress")`|

## Creating Work Items

**IMPORTANT:** The `--description` flag produces plain text with no line breaks.
For formatted descriptions with paragraphs, use `--from-json` with Atlassian
Document Format (ADF).

### Simple creation (no formatting needed)

```bash
# Basic creation
acli jira workitem create \
  --project "TEAM" \
  --type "Task" \
  --summary "Implement feature X"

# With plain text description (renders as single block, no line breaks)
acli jira workitem create \
  --project "TEAM" \
  --type "Task" \
  --summary "Fix login error" \
  --description "This is a plain text description with no formatting"

# With assignee
acli jira workitem create \
  --project "TEAM" \
  --type "Bug" \
  --summary "Fix login error" \
  --assignee "@me"

# With labels
acli jira workitem create \
  --project "TEAM" \
  --type "Task" \
  --summary "Refactor auth module" \
  --label "tech-debt,refactor"
```

### With epic/parent linking

There is NO `--epic` flag. Use `--parent` to link to an epic or parent issue:

```bash
# Link to epic via --parent
acli jira workitem create \
  --project "TEAM" \
  --type "Task" \
  --summary "Implement feature X" \
  --parent "TEAM-100"
```

Or use `parentIssueId` in JSON (see below).

### With formatted description (recommended for multi-paragraph)

Use `--from-json` with ADF for descriptions that need paragraphs, bullet lists,
headings, or any formatting. The `description` field MUST be in ADF format when
using JSON — plain text strings will be rejected.

```bash
cat > /tmp/ticket.json << 'EOF'
{
  "projectKey": "TEAM",
  "type": "Task",
  "summary": "Implement feature X",
  "parentIssueId": "TEAM-100",
  "description": {
    "type": "doc",
    "version": 1,
    "content": [
      {
        "type": "paragraph",
        "content": [{ "type": "text", "text": "First paragraph." }]
      },
      {
        "type": "paragraph",
        "content": [{ "type": "text", "text": "Second paragraph renders with proper spacing." }]
      },
      {
        "type": "bulletList",
        "content": [
          { "type": "listItem", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Bullet point one" }] }] },
          { "type": "listItem", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Bullet point two" }] }] }
        ]
      }
    ]
  }
}
EOF
acli jira workitem create --from-json /tmp/ticket.json
```

### Other creation options

```bash
# Open editor for description
acli jira workitem create \
  --project "TEAM" \
  --type "Story" \
  --summary "Complex feature" \
  --editor

# Generate JSON template (useful to see all available fields)
acli jira workitem create --generate-json
```

### Work Item Types

Common types (varies by project configuration):

- `Epic` - Large feature or initiative
- `Story` - User-facing feature
- `Task` - Technical work item
- `Bug` - Defect to fix
- `Sub-task` - Child of another issue

## Editing Work Items

```bash
# Edit summary
acli jira workitem edit --key "TEAM-123" --summary "Updated title"

# Edit description (plain text only, no line breaks)
acli jira workitem edit --key "TEAM-123" --description "New description"

# Change type
acli jira workitem edit --key "TEAM-123" --type "Bug"

# Add labels
acli jira workitem edit --key "TEAM-123" --labels "urgent,production"

# Remove labels
acli jira workitem edit --key "TEAM-123" --remove-labels "draft"

# Remove assignee
acli jira workitem edit --key "TEAM-123" --remove-assignee

# Bulk edit with JQL (--yes required to skip prompt)
acli jira workitem edit --jql "project = TEAM AND labels = old-label" \
  --labels "new-label" --yes
```

### Editing with formatted description (ADF via JSON)

**IMPORTANT:** `--key` and `--from-json` CANNOT be combined. When using
`--from-json` for edits, specify the target ticket(s) in the `issues` array
inside the JSON file. Also requires `--yes` to confirm.

```bash
cat > /tmp/edit.json << 'EOF'
{
  "issues": ["TEAM-123"],
  "description": {
    "type": "doc",
    "version": 1,
    "content": [
      {
        "type": "paragraph",
        "content": [{ "type": "text", "text": "First paragraph." }]
      },
      {
        "type": "paragraph",
        "content": [{ "type": "text", "text": "Second paragraph with proper line breaks." }]
      }
    ]
  }
}
EOF
acli jira workitem edit --from-json /tmp/edit.json --yes
```

## Transitioning Work Items (Status Changes)

```bash
# Move to In Progress
acli jira workitem transition --key "TEAM-123" --status "In Progress"

# Move to Done
acli jira workitem transition --key "TEAM-123" --status "Done"

# Bulk transition
acli jira workitem transition --jql "project = TEAM AND assignee = currentUser()" \
  --status "In Review" --yes
```

**Note:** Available statuses depend on your project's workflow configuration.

## Assigning Work Items

```bash
# Self-assign
acli jira workitem assign --key "TEAM-123" --assignee "@me"

# Assign to someone
acli jira workitem assign --key "TEAM-123" --assignee "user@company.com"

# Assign to default assignee
acli jira workitem assign --key "TEAM-123" --assignee "default"

# Remove assignee
acli jira workitem assign --key "TEAM-123" --remove-assignee

# Bulk assign
acli jira workitem assign --jql "project = TEAM AND assignee IS EMPTY" \
  --assignee "@me" --yes
```

## Comments

```bash
# Add comment
acli jira workitem comment create --key "TEAM-123" --body "This is my comment"

# Add comment from file
acli jira workitem comment create --key "TEAM-123" --body-file "comment.txt"

# Open editor for comment
acli jira workitem comment create --key "TEAM-123" --editor

# Edit last comment
acli jira workitem comment create --key "TEAM-123" --body "Updated" --edit-last

# List comments
acli jira workitem comment list --key "TEAM-123"
```

## Sprints

```bash
# List sprints for a board
acli jira board list-sprints --id 123

# Active sprints only
acli jira board list-sprints --id 123 --state active

# Future sprints
acli jira board list-sprints --id 123 --state future

# Multiple states
acli jira board list-sprints --id 123 --state active,future

# JSON output
acli jira board list-sprints --id 123 --json

# List work items in a sprint
acli jira sprint list-workitems --id 456
```

## Finding Boards

```bash
# Search all boards
acli jira board search

# Search by name
acli jira board search --name "Team"

# Filter by project
acli jira board search --project "TEAM"

# Filter by type
acli jira board search --type scrum

# JSON output (useful for getting board IDs)
acli jira board search --project "TEAM" --json
```

## Projects

```bash
# List all projects
acli jira project list

# View project details
acli jira project view TEAM
```

## Workflow Tips

### Start Working on a Ticket

```bash
# View the ticket
acli jira workitem view TEAM-123

# Assign to yourself and move to In Progress
acli jira workitem assign --key "TEAM-123" --assignee "@me"
acli jira workitem transition --key "TEAM-123" --status "In Progress"
```

### Daily Standup View

```bash
# My in-progress tickets
acli jira workitem search \
  --jql "assignee = currentUser() AND status = 'In Progress'" \
  --fields "key,summary,status"
```

### Quick Ticket Creation from Current Work

When you need to create a follow-up ticket while working:

```bash
acli jira workitem create \
  --project "TEAM" \
  --type "Task" \
  --summary "Follow-up: description here" \
  --assignee "@me"
```

### Link to PR in Comment

```bash
acli jira workitem comment create \
  --key "TEAM-123" \
  --body "PR: https://github.com/org/repo/pull/456"
```

## Output Formats

All search and view commands support multiple output formats:

| Flag       | Use Case                           |
| ---------- | ---------------------------------- |
| (default)  | Human-readable table               |
| `--json`   | Parsing in scripts, full data      |
| `--csv`    | Spreadsheets, data analysis        |
| `--web`    | Open in browser for full UI access |

## Troubleshooting

### "Not authenticated"

Run `acli jira auth` and follow the prompts.

### "Invalid JQL"

- Check field names match your Jira instance
- Wrap values with spaces in quotes: `status = "In Progress"`
- Use `AND`/`OR` operators correctly

### "Transition not allowed"

The status you're trying to transition to may not be valid from the current
status. Check your project's workflow.

### "Field not found"

Custom field names vary by project. Use `acli jira field list --project TEAM`
to see available fields.
