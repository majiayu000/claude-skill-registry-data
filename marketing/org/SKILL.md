---
name: Org
description: Org-mode file manipulation using Emacs batch mode. USE WHEN you need to programmatically read, parse, or modify org-mode files (.org) for TODOs, notes, or other structured content.
---

# Org-Mode File Manipulation

## Purpose
Provide reliable, programmatic access to org-mode files using Emacs batch mode and the org-element API. This skill is used by other skills (TODOs, Notes) for org-mode operations.

### Context Detection

**This skill activates when:**
- Other skills need to manipulate org-mode files
- Parsing TODO items, denote notes, or org content
- Updating TODO states, scheduling, or properties
- Querying org-mode structure or metadata
- Working with files ending in `.org`

## Tool: org-manager

### Location
`tools/org-manager` - Bash CLI wrapper around Emacs batch mode

### Usage

#### TODO Operations
```bash
# List TODOs
./tools/org-manager list ~/desktop/org/todos.org --state=NEXT

# Add TODO
./tools/org-manager add ~/desktop/org/todos.org "Task name" \
  --section=Work --priority=2 --scheduled=2025-12-10

# Update state
./tools/org-manager update-state ~/desktop/org/todos.org "Task name" DONE

# Count by state
./tools/org-manager count ~/desktop/org/todos.org

# Get scheduled items
./tools/org-manager scheduled ~/desktop/org/todos.org

# Search
./tools/org-manager search ~/desktop/org/todos.org "term"

# Get full TODO content (metadata + body)
./tools/org-manager get ~/desktop/org/todos.org "Task name"

# Get overdue tasks (deadline before today)
./tools/org-manager overdue ~/desktop/org/todos.org

# Get upcoming tasks (scheduled/deadline in next N days)
./tools/org-manager upcoming ~/desktop/org/todos.org --days=7
```

#### Tag Management
```bash
# List all unique tags in file
./tools/org-manager list-tags ~/desktop/org/todos.org

# Add tags to existing TODO
./tools/org-manager add-tags ~/desktop/org/todos.org "Task name" "urgent,review"

# Remove specific tags
./tools/org-manager remove-tags ~/desktop/org/todos.org "Task name" "urgent"

# Replace all tags with new set
./tools/org-manager replace-tags ~/desktop/org/todos.org "Task name" "done,archived"
```

#### Property Operations
```bash
# List all properties of a heading
./tools/org-manager list-properties ~/desktop/org/todos.org "Task name"

# Get specific property value
./tools/org-manager get-property ~/desktop/org/todos.org "Task name" "PR_URL"

# Set property value
./tools/org-manager set-property ~/desktop/org/todos.org "Task name" "STATUS" "In Progress"
```

#### Bulk Operations
```bash
# Update all tasks matching a state to a new state
./tools/org-manager bulk-update-state ~/desktop/org/todos.org "TODO" "DONE"

# Update with tag filter (only tasks with specific tags)
./tools/org-manager bulk-update-state ~/desktop/org/todos.org "TODO" "DONE" "work,urgent"

# Add tags to all tasks with a specific state
./tools/org-manager bulk-add-tags ~/desktop/org/todos.org "NEXT" "urgent,review"

# Set priority for all tasks with a specific state
./tools/org-manager bulk-set-priority ~/desktop/org/todos.org "TODO" 1
```

#### Time Tracking
```bash
# Start time tracking on a task
./tools/org-manager clock-in ~/desktop/org/todos.org "Implement feature X"

# Stop time tracking (clocks out of currently active task)
./tools/org-manager clock-out ~/desktop/org/todos.org

# Check what task is currently being tracked
./tools/org-manager get-active-clock ~/desktop/org/todos.org

# Get total time spent on a task (returns minutes)
./tools/org-manager get-clocked-time ~/desktop/org/todos.org "Implement feature X"
```

#### Statistics & Analytics
```bash
# Get comprehensive statistics (counts by state, priority, tags, overdue, etc.)
./tools/org-manager get-statistics ~/desktop/org/todos.org

# Get priority distribution across all tasks
./tools/org-manager get-priority-distribution ~/desktop/org/todos.org

# Get tag usage statistics (sorted by frequency)
./tools/org-manager get-tag-statistics ~/desktop/org/todos.org
```

#### Export & Reporting
```bash
# Export to CSV for spreadsheet analysis
./tools/org-manager export-csv ~/desktop/org/todos.org /tmp/todos.csv

# Export to JSON for programmatic processing
./tools/org-manager export-json ~/desktop/org/todos.org /tmp/todos.json
```

#### Recurring Tasks
```bash
# Set repeater for a task (+1w = weekly, .+2d = 2 days after completion)
./tools/org-manager set-repeater ~/desktop/org/todos.org "Weekly Review" "+1w"

# Get all recurring tasks
./tools/org-manager get-recurring-tasks ~/desktop/org/todos.org
```

#### Dependencies & Relationships
```bash
# Set a blocker for a task
./tools/org-manager set-blocker ~/desktop/org/todos.org "Deploy to production" "Complete testing"

# Get blocker for a specific task
./tools/org-manager get-blocker ~/desktop/org/todos.org "Deploy to production"

# List all blocked tasks
./tools/org-manager get-blocked-tasks ~/desktop/org/todos.org

# Create task relationship (child/parent/related/depends-on)
./tools/org-manager set-related ~/desktop/org/todos.org "Implement feature" "Design review" "depends-on"

# Get all relationships for a task
./tools/org-manager get-related ~/desktop/org/todos.org "Implement feature"
```

#### Denote Operations
```bash
# Create denote-formatted note
./tools/org-manager denote-create "My Note Title" "tag1,tag2,tag3" \
  --category=homelab --directory=~/desktop/org/notes

# Create with signature (for automated notes)
./tools/org-manager denote-create "Session Log" "history,session" \
  --signature=pkai --category=history

# Read note metadata
./tools/org-manager denote-metadata ~/desktop/org/notes/20251205T*.org

# Update note frontmatter
./tools/org-manager denote-update ~/desktop/org/notes/20251205T*.org \
  --title="New Title" --tags="new,tags" --category="updated"

# Append content to note
echo "* New Section" > /tmp/content.org
./tools/org-manager denote-append ~/desktop/org/notes/20251205T*.org /tmp/content.org
```

### Output Format

All commands return JSON:

```json
{
  "success": true,
  "data": [
    {
      "heading": "Task name",
      "todo": "NEXT",
      "priority": 2,
      "tags": ["tag1"],
      "level": 2,
      "scheduled": "2025-12-05",
      "deadline": null
    }
  ]
}
```

## Implementation

### Core Functions (batch-functions.el)

**TODO Operations:**
- `org-batch-list-todos` - Parse and filter TODOs
- `org-batch-scheduled-today` - Get scheduled items
- `org-batch-by-section` - Filter by section
- `org-batch-count-by-state` - Count statistics
- `org-batch-search` - Full-text search
- `org-batch-get-children` - Get direct children of a heading
- `org-batch-get-sections` - List all top-level sections
- `org-batch-get-todo-content` - Get full TODO content (metadata + body + properties)
- `org-batch-get-overdue` - Get tasks with deadline before today
- `org-batch-get-upcoming` - Get tasks scheduled/due in next N days
- `org-batch-add-todo` - Add new TODO
- `org-batch-update-state` - Change states
- `org-batch-schedule-task` - Set SCHEDULED
- `org-batch-set-deadline` - Set DEADLINE
- `org-batch-set-priority` - Set priority
- `org-batch-archive-done` - Archive items

**Tag Operations:**
- `org-batch-add-tags` - Add tags while preserving existing
- `org-batch-remove-tags` - Remove specific tags
- `org-batch-replace-tags` - Replace all tags with new set
- `org-batch-list-all-tags` - Get all unique tags in file

**Property Operations:**
- `org-batch-get-property` - Get specific property value
- `org-batch-set-property` - Set property value
- `org-batch-list-properties` - List all properties of a heading

**Bulk Operations:**
- `org-batch-bulk-update-state` - Update all tasks matching a state
- `org-batch-bulk-add-tags` - Add tags to all tasks with specific state
- `org-batch-bulk-set-priority` - Set priority for all tasks with specific state

**Time Tracking:**
- `org-batch-clock-in` - Start time tracking on a task
- `org-batch-clock-out` - Stop time tracking
- `org-batch-get-active-clock` - Get currently clocked task
- `org-batch-get-clocked-time` - Get total time spent on a task

**Statistics & Analytics:**
- `org-batch-get-statistics` - Comprehensive statistics (counts, priorities, tags, overdue)
- `org-batch-get-priority-distribution` - Priority distribution across tasks
- `org-batch-get-tag-statistics` - Tag usage statistics

**Export & Reporting:**
- `org-batch-export-csv` - Export TODOs to CSV format
- `org-batch-export-json` - Export TODOs to JSON format

**Recurring Tasks:**
- `org-batch-set-repeater` - Set repeater specification for a task
- `org-batch-get-recurring-tasks` - List all tasks with repeaters

**Dependencies & Relationships:**
- `org-batch-set-blocker` - Set task blocker
- `org-batch-get-blocker` - Get blocker for a task
- `org-batch-get-blocked-tasks` - List all blocked tasks
- `org-batch-set-related` - Create task relationships (child/parent/related/depends-on)
- `org-batch-get-related` - Get all relationships for a task

### Denote Functions (denote-batch-functions.el)

**Note Creation and Management:**
- `denote-batch-create-note` - Create denote note with proper naming and frontmatter
- `denote-batch-create-note-from-file` - Create note with content from file
- `denote-batch-append-content` - Append content to existing note
- `denote-batch-update-frontmatter` - Update note metadata (title, tags, category)
- `denote-batch-read-metadata` - Read note metadata as JSON

**Features:**
- Automatic timestamp generation (YYYYMMDDTHHMMSS)
- Signature support for automated notes (e.g., `==pkai`)
- Proper denote filename format: `TIMESTAMP==SIG--title__tags.org`
- Org-mode frontmatter generation (#+title, #+date, #+filetags, etc.)
- JSON output for programmatic integration

### Configuration

TODO keywords and priorities are configured for your setup:

```elisp
(setq org-todo-keywords
      '((sequence "STRT(s)" "NEXT(n)" "TODO(t)" "WAIT(w)" "|" "DONE(d!)" "CANX(c@/!)")))

(setq org-priority-highest 1
      org-priority-lowest 5
      org-priority-default 4)
```

## Performance

Tested on 354-item todos.org:
- Parse: <100ms
- Filter: <50ms
- Updates: <100ms per item

## References

- [[file:~/desktop/org/notes/20251205T092927--emacs-batch-mode-for-org-automation__emacs_orgmode_automation_elisp_reference.org][Research Note]]
- See `README.md` for full documentation

## Examples

**Example 1: Reading and parsing org file**
```
User: "What TODOs are in my project.org file?"
→ Uses Emacs batch mode to parse org file
→ Extracts TODO items with org-element-map
→ Returns formatted list with priorities and tags
→ Shows deadlines and scheduled dates
→ Result: Complete overview of project TODOs
```

**Example 2: Updating org file programmatically**
```
User: "Mark all DONE items as archived"
→ Reads org file with Emacs batch mode
→ Finds all DONE entries
→ Moves them to archive section
→ Preserves timestamps and properties
→ Saves updated file
→ Result: Clean org file with archived history
```

**Example 3: Extracting information from org**
```
User: "Get all meeting notes from last month"
→ Parses org files for date range
→ Filters entries with :meeting: tag
→ Extracts content and metadata
→ Formats as summary report
→ Result: Month's meeting notes compiled
```
