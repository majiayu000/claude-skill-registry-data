---
name: vault-task-aggregator
description: Query, prioritize, and manage tasks across the whole vault — find overdue items, suggest what to do next, mark tasks complete. Use when the user says "what's overdue", "show my tasks", "what should I do today", or "complete that task". NOT for EmptyOS dev-session task tracking (TaskCreate / the projects app) or weekly planning (use eos-week-review).
---

# Task Management

This skill manages tasks across the vault, providing intelligent prioritization and task operations.

## Files

- **Script**: `80_Code/scripts/task-manager.py`
- **Index**: `99_Attachments/task-index.json`

## Task Format

Tasks in this vault use:
- `- [ ] Task description` — Open task
- `- [x] Task description` — Completed task
- `📅 YYYY-MM-DD` — Due date (anywhere in task text)
- `🔁 every week` — Recurring task (day/week/month)
- `✅ YYYY-MM-DD` — Completion date (added when done)

See: [[journal-planner]] skill for task architecture (where tasks live, how they flow).

## Commands

### Generate/Refresh Index
```bash
python "80_Code/scripts/task-manager.py"
```
Auto-skips if fresh (<4h old). Use `--force` to regenerate.

### Get Suggestions (Primary Use)
```bash
python "80_Code/scripts/task-manager.py" --suggest
```
Returns AI-prioritized tasks:
1. URGENT: Overdue tasks
2. TODAY: Due today
3. THIS WEEK: Project tasks due soon
4. QUICK WINS: Small tasks without dates

### Query Commands

| Command | Description |
|---------|-------------|
| `--overdue` | List all overdue tasks |
| `--today` | Tasks due today |
| `--week` | Tasks due within 7 days |
| `--project "name"` | Tasks for specific project/area |
| `--stats` | Full statistics breakdown |
| `--check` | Check if index needs refresh |

### Example Queries

```bash
# What should I work on?
python3 .../task-manager.py --suggest

# Show 189 Visa tasks
python3 .../task-manager.py --project "189-Visa-Tracker"

# Show job search tasks
python3 .../task-manager.py --project "Job-Search-Tracker"

# What's overdue?
python3 .../task-manager.py --overdue
```

## Key Project Trackers

| Tracker | File | Focus |
|---------|------|-------|
| [[189-Visa-Tracker]] | `10_Projects/` | 移民材料、CO 应对、获批 checklist |
| [[Job-Search-Tracker]] | `10_Projects/` | 求职申请、面试准备、目标公司 |
| [[YouTube Music Channel Plan]] | `10_Projects/` | 视频制作、发布计划 |

## Task Operations (Claude Code Actions)

### Complete a Task
When user says "mark X as done" or "complete X":

1. Find the task in the index or search vault
2. Read the source file
3. Replace `- [ ]` with `- [x]` for that task
4. Confirm completion to user

```python
# Example: Mark task done
old = "- [ ] Submit PTE score report 📅 2026-01-15"
new = "- [x] Submit PTE score report 📅 2026-01-15"
# Use Edit tool to replace in source file
```

### Reschedule a Task
When user says "move X to next week" or "reschedule X":

1. Find the task
2. Calculate new date
3. Replace old date with new date
4. Confirm change

```python
# Example: Reschedule
old = "- [ ] Review CPD log 📅 2026-01-05"
new = "- [ ] Review CPD log 📅 2026-01-12"
```

### Create a Task
When user says "add task X to Y":

1. Determine target file (project/area note)
2. Find appropriate section (usually under a "Tasks" or "TODO" heading)
3. Append task with optional due date
4. Confirm creation

### Bulk Operations
When user wants to review/clean tasks:

1. Run `--stats` to show overview
2. Offer to show overdue items
3. For each overdue: ask reschedule or complete
4. Update index after changes

## Suggestion Logic

The `--suggest` command prioritizes tasks by:

| Priority | Criteria |
|----------|----------|
| 1. URGENT | Overdue (past due date) |
| 2. TODAY | Due date = today |
| 3. THIS WEEK (Projects) | Project tasks due within 7 days |
| 4. QUICK WINS | Short tasks (<50 chars) without dates |

## Index Structure

```json
{
  "generated": "ISO timestamp",
  "stats": {
    "total_open": 625,
    "total_completed": 234,
    "overdue": 12,
    "due_today": 3,
    "due_this_week": 28,
    "no_date": 450,
    "by_category": {"project": 45, "area": 120, ...},
    "by_context": {"Career-Development-Plan": 25, ...}
  },
  "tasks": [
    {
      "text": "Submit PTE score report",
      "file": "10_Projects/189 Visa.md",
      "context": "189 Visa",
      "category": "project",
      "completed": false,
      "due": "2026-01-15",
      "urgency": "this_week"
    }
  ]
}
```

## When to Use

| User Says | Action |
|-----------|--------|
| "What should I do today?" | Run `--suggest` |
| "What's overdue?" | Run `--overdue` |
| "Show me visa tasks" | Run `--project "visa"` |
| "Mark X as done" | Find task, edit file, complete it |
| "Add task to project Y" | Create task in target file |
| "Reschedule X to Friday" | Update due date in file |

## Proactive Behaviors

Claude Code should:
- Offer `--suggest` when user asks "what should I work on?"
- Warn about overdue tasks when reviewing projects
- Suggest due dates for tasks without them
- Offer to complete tasks after user reports finishing something

## Obsidian CLI (Fast Task Queries) — with Fallbacks

Try CLI first for instant results. Fall back to Python script or Grep if Obsidian is unavailable.

```bash
OBS="bash 80_Code/scripts/obs.sh"

# All open tasks across vault
$OBS tasks todo                                 # full list
$OBS tasks todo total                           # count only
# FALLBACK: Grep for '- \[ \]' across *.md files

# Tasks grouped by file with line numbers
$OBS tasks todo verbose
# FALLBACK: Grep with file grouping

# Tasks in a specific file
$OBS tasks todo "file=Job-Search-Tracker"
# FALLBACK: Grep for '- \[ \]' in that specific file

# Completed tasks
$OBS tasks done total
# FALLBACK: Grep for '- \[x\]' across *.md files

# Tasks from daily note
$OBS tasks todo daily
# FALLBACK: Read today's daily note file, extract tasks
```

**When to use CLI vs Python script:**
| Need | Tool | Fallback |
|------|------|----------|
| Quick count of open tasks | CLI `tasks todo total` | Grep `- \[ \]` + count |
| Tasks for one specific file | CLI `tasks todo file=X` | Grep in that file |
| All tasks with line numbers | CLI `tasks todo verbose` | Grep with `-n` flag |
| AI-prioritized suggestions | Python `--suggest` | (always use Python) |
| Overdue/today/this-week filtering | Python `--overdue` / `--today` | (always use Python) |
| Statistics breakdown | Python `--stats` | (always use Python) |

## Related Skills

- **journal-planner**: Task architecture (where tasks live, task flow from yearly → daily)
- **project-builder**: Creating new project trackers
