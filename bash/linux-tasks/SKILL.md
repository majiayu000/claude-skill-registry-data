---
name: linux-tasks
description: Manage tasks and todos on Linux using Taskwarrior CLI. Add, list, complete, modify, and delete tasks with projects, tags, priorities, and due dates. Use when a user asks FRIDAY to add a task, list todos, manage projects, or track tasks on Linux.
homepage: https://taskwarrior.org
metadata: {"friday":{"emoji":"✅","os":["linux"],"requires":{"bins":["task"]},"install":[{"id":"apt-taskwarrior","kind":"apt","package":"taskwarrior","bins":["task"],"label":"Install Taskwarrior via apt"}]}}
---

# Linux Tasks CLI (Taskwarrior)

Use `task` (Taskwarrior) to manage tasks and todos from the terminal. This is a Linux alternative to Things 3 on macOS.

## Setup
Install Taskwarrior:
```bash
sudo apt-get install -y taskwarrior
```

Initialize on first run:
```bash
task
# Press 'yes' to create config
```

## View Tasks

### List all pending tasks
```bash
task list
```

### Today's tasks
```bash
task due:today list
```

### Overdue tasks
```bash
task +OVERDUE list
```

### Tasks due this week
```bash
task due.before:eow list
```

### Inbox (tasks without project)
```bash
task project: list
```

### Search tasks
```bash
task /search query/ list
```

### Detailed task info
```bash
task 1 info
```

## Add Tasks

### Basic task
```bash
task add "Buy groceries"
```

### With due date
```bash
task add "Submit report" due:tomorrow
task add "Pay rent" due:2026-02-01
task add "Meeting" due:monday
```

### With project
```bash
task add "Design mockup" project:Work
task add "Book flights" project:Travel
```

### With priority (H=High, M=Medium, L=Low)
```bash
task add "Urgent fix" priority:H
task add "Nice to have" priority:L
```

### With tags
```bash
task add "Call dentist" +health +phone
task add "Review PR" +work +code
```

### Combined example
```bash
task add "Prepare presentation" project:Work due:friday priority:H +meeting
```

### With notes/annotations
```bash
task 1 annotate "Remember to include Q4 numbers"
```

## Complete Tasks

### Mark task as done
```bash
task 1 done
```

### Complete multiple tasks
```bash
task 1-3 done
task 1 2 5 done
```

### Complete by description
```bash
task /groceries/ done
```

## Modify Tasks

### Change due date
```bash
task 1 modify due:tomorrow
```

### Add to project
```bash
task 1 modify project:Personal
```

### Change priority
```bash
task 1 modify priority:H
```

### Add tags
```bash
task 1 modify +urgent +important
```

### Remove tags
```bash
task 1 modify -urgent
```

### Edit in text editor
```bash
task 1 edit
```

## Delete Tasks

### Delete a task
```bash
task 1 delete
```

### Undo last action
```bash
task undo
```

## Projects & Tags

### List all projects
```bash
task projects
```

### Tasks in a project
```bash
task project:Work list
```

### List all tags
```bash
task tags
```

### Tasks with tag
```bash
task +health list
```

## Reports & Views

### Summary
```bash
task summary
```

### Calendar view
```bash
task calendar
```

### Burndown chart
```bash
task burndown.daily
```

### Completed tasks
```bash
task completed
```

### Statistics
```bash
task stats
```

## Recurring Tasks

### Daily task
```bash
task add "Morning standup" due:tomorrow recur:daily
```

### Weekly task
```bash
task add "Weekly review" due:friday recur:weekly
```

### Monthly task
```bash
task add "Pay bills" due:1st recur:monthly
```

## Advanced Filters

### High priority incomplete
```bash
task priority:H status:pending list
```

### Due this week, not completed
```bash
task due.before:eow status:pending list
```

### Work tasks due soon
```bash
task project:Work due.before:eow list
```

## Aliases (add to ~/.taskrc)

```bash
# Add to ~/.taskrc for shortcuts
alias.in=add +inbox
alias.today=list due:today
alias.week=list due.before:eow
```

## Notes
- Linux-only (alternative to Things 3 on macOS).
- Data stored in `~/.task/`.
- Sync available with Taskserver or third-party services.
- Use `task help` for full command reference.
- Highly customizable via `~/.taskrc`.
