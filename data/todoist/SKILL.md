---
name: todoist
description: "Todoist CLI (sachaos/todoist). Use when user mentions: todoist, tasks, todos, adding/listing/completing tasks, creating projects, filtering by date/priority/label, natural language task entry, recurring tasks, or task management workflows."
---

# Todoist CLI

CLI client for Todoist task manager (sachaos/todoist v0.23+).

## Quick Start

```bash
# List all tasks
todoist list
todoist l

# Quick add with natural language
todoist quick 'Buy milk tomorrow #Shopping @errands p1'
todoist q 'Team meeting every Monday 2pm #Work'

# List with filters
todoist list --filter 'today & p1'
todoist list --filter '#Work & @urgent'

# Complete task
todoist close <task-id>

# Sync local cache
todoist sync
```

## Core Commands

| Command | Alias | Usage |
|---------|-------|-------|
| `list` | `l` | Show all tasks |
| `quick` | `q` | Add task with natural language |
| `add` | `a` | Add task (structured) |
| `close` | `c` | Complete task |
| `modify` | `m` | Edit task |
| `delete` | `d` | Delete task |
| `show` | - | Task details |
| `projects` | - | List projects |
| `add-project` | `ap` | Create project |
| `labels` | - | List labels |
| `sync` | `s` | Update local cache |

## Adding Tasks

### Before Adding: Clarify Requirements

When user requests to add a task, check if details are unclear or incomplete. Ask clarifying questions BEFORE creating the task:

- **Vague goals**: "Research X" → What specifically? What's the desired outcome?
- **Missing context**: "Fix bug" → Which bug? Where? What's broken?
- **Unclear scope**: "Update docs" → Which docs? What needs updating?
- **No deadline mentioned for time-sensitive work**: When is this needed?
- **Ambiguous priority**: Is this urgent? Blocking other work?

**Example:**
User: "Add task to research banks"
You: "I can add that. To make it actionable, could you clarify:
- What specific aspects? (fees, online banking, international transfers?)
- What's the goal? (opening account, comparing options?)
- Any constraints? (country-specific, business vs personal?)"

Then create a well-formed task: "Research Danish bank accounts: easy online signup, lowest fees, foreigner-friendly"

### Quick Add (Recommended)

Use `todoist quick` for natural language:

```bash
# Basic task
todoist q 'Write report'

# With project and labels
todoist q 'Email client #Work @email @urgent'

# With date and priority
todoist q 'Call dentist tomorrow at 2pm p1'

# Recurring task
todoist q 'Water plants every Monday #Home'

# All together
todoist q 'Review PRs every weekday 9am #Work @code p2'
```

**Natural language symbols:**
- `#Project` - assign to project
- `@label` - add labels (multiple allowed)
- `p1-p3` - priority (p1=highest, p4=none)
- Date/time - `tomorrow`, `next week`, `Jan 15`, `at 3pm`
- Recurring - `every Monday`, `every 2 weeks`, `daily`

### Structured Add

Use `todoist add` when `quick` fails with special characters:

```bash
todoist add 'Task name' --project-name 'Project' --priority 1 --date 'tomorrow'
```

**Note**: `add` has issues with hyphens in task names. Prefer `quick`.

## Filtering Tasks

Use `--filter` with `todoist list`:

### Date Filters
```bash
--filter 'today'              # Due today
--filter 'tomorrow'
--filter 'overdue'            # or 'od'
--filter 'no date'            # Unscheduled
--filter 'date: Jan 15'       # Specific date
--filter 'date before: May 5' # Before date
--filter 'date after: May 5'  # After date
```

### Priority Filters
```bash
--filter 'p1'                 # Priority 1 (highest)
--filter 'p2'                 # Priority 2
--filter 'p3'                 # Priority 3
--filter 'no priority'        # No priority (p4)
```

### Organization Filters
```bash
--filter '#Project'           # Specific project
--filter '##Project'          # Project + subprojects
--filter '@label'             # With label
--filter '@home*'             # Wildcard labels
--filter 'no labels'          # Without labels
```

### Search
```bash
--filter 'search: keyword'    # Text search
```

### Logical Operators
```bash
--filter '(today | tomorrow) & p1'           # OR + AND
--filter '#Work & @urgent & !@waiting'       # NOT
--filter '(overdue | today) & (p1 | p2)'     # Grouping
```

### Complex Examples
```bash
# High priority tasks due soon
todoist list --filter '(overdue | today | tomorrow) & (p1 | p2)'

# Work tasks excluding meetings
todoist list --filter '#Work & !search: meeting'

# Urgent home tasks
todoist list --filter '#Home & @urgent'
```

## Recurring Tasks

### Absolute Recurrence (`every`)

Next occurrence always on specific day:

```bash
todoist q 'Standup every weekday 9am #Work'
todoist q 'Review metrics every Monday 10am'
todoist q 'Pay rent every 1st #Finance'
todoist q 'Dentist every 6 months'
```

**Patterns:**
- `every day`, `daily`
- `every Monday`, `every Mon, Fri`
- `every 2 weeks`
- `every 15th` (day of month)
- `every 3rd Friday`
- `every last day` (of month)

### Relative Recurrence (`every!`)

Next occurrence from completion date:

```bash
todoist q 'Change air filter every! 3 months #Home'
todoist q 'Review goals every! 2 weeks'
```

Use `every!` when task should recur from when you complete it, not from scheduled date.

### With Boundaries

```bash
todoist q 'Daily standup every day starting next Monday'
todoist q 'Summer task every week ending Aug 31'
todoist q 'Trial period every day for 2 weeks'
```

## Date Formats

### One-Time Dates
```bash
today, tod, tomorrow, tom
next week, next month
Jan 27, 27 jan, 27/1
01/27/2026, 2026-01-27
end of month
```

### With Time
```bash
today at 10          # 10am
tomorrow at 16:00
Fri @ 7pm
in the morning       # 9am
in the afternoon     # 12pm
in the evening       # 7pm
```

### Relative
```bash
in 5 days, +5 days
in 3 weeks
in 2 hours
```

## Projects

```bash
# List projects
todoist projects

# Create project
todoist add-project 'Project Name'
todoist ap 'Work Stuff' --color 42

# List project tasks
todoist list --filter '#ProjectName'
```

## Common Workflows

### Daily Review
```bash
# Check overdue and today's tasks
todoist list --filter '(overdue | today)'

# High priority items
todoist list --filter '(overdue | today) & (p1 | p2)'
```

### Weekly Planning
```bash
# Next 7 days
todoist list --filter 'date before: +7 days'

# By project
todoist list --filter '#Work'
todoist list --filter '#Personal'
```

### Quick Capture
```bash
# Dump to inbox
todoist q 'Task name'

# With context
todoist q 'Task #Project @label p1'
```

### Task Management
```bash
# Complete task
todoist close <id>

# Delete task
todoist delete <id>

# Modify task
todoist modify <id> --content 'New name' --priority 1
```

## Best Practices

1. **Always use `todoist quick`** for adding tasks - handles natural language best
2. **Run `todoist sync`** after external changes (web/mobile)
3. **Use filters extensively** - more powerful than scrolling
4. **Prefer `every!` for maintenance tasks** - recur from completion, not schedule
5. **Use project tags in quick add** - `#Project` faster than `--project-name`
6. **Combine filters** - `(overdue | today) & p1 & #Work`
7. **Wildcards for label families** - `@home*` matches `@home-repair`, `@home-garden`

## Global Flags

Add to any command:

```bash
--color              # Colorize output
--namespace          # Show parent tasks hierarchically
--indent             # Indent subtasks
--project-namespace  # Show parent project structure
--csv                # CSV export
```

## Config

Location: `~/.config/todoist/config.json`

```json
{
  "token": "your_api_token",
  "color": "true"
}
```

Get token from: Todoist Settings → Integrations → Developer → API token
