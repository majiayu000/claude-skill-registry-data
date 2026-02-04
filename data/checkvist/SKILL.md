---
name: checkvist
description: Manage Checkvist tasks, checklists, and notes using checkvist-cli. Use when the user wants to work with Checkvist.com data, including viewing/creating/updating checklists, hierarchical tasks, or task notes.
---

# Checkvist CLI Skill

You are the Checkvist management skill. Your job is to help users work with their Checkvist.com data using the `checkvist-cli` command-line tool.

## What is Checkvist?

Checkvist is a hierarchical task management system that supports:
- **Checklists (Lists)**: Top-level containers for tasks
- **Tasks**: Hierarchical items that can have parent-child relationships
- **Notes**: Additional information attached to specific tasks

## Core Capabilities

### 1. Authentication

Before using any Checkvist commands, ensure the user is authenticated:

```bash
# Check authentication status
checkvist-cli auth status

# If not authenticated, guide user through login
checkvist-cli auth login
```

**When to check auth:**
- First time using Checkvist commands in a session
- When receiving authentication errors (exit code 3)
- When user explicitly asks about authentication

### 2. Working with Lists

**List all checklists:**
```bash
# Basic listing (text format)
checkvist-cli lists

# JSON format for programmatic use
checkvist-cli --format json lists get

# Show archived lists
checkvist-cli lists get --archived

# Sort by update time
checkvist-cli lists get --order updated_at:desc
```

**Create a new list:**
```bash
checkvist-cli lists create "List Name"
```

**Update a list:**
```bash
# Archive a list
checkvist-cli lists update LIST_ID --archive

# Unarchive a list
checkvist-cli lists update LIST_ID --unarchive

# Make public/private
checkvist-cli lists update LIST_ID --public
checkvist-cli lists update LIST_ID --private
```

**Delete an empty list:**
```bash
checkvist-cli lists delete LIST_ID
```

**Show list details:**
```bash
# Show metadata
checkvist-cli lists show LIST_ID

# Show tasks in list
checkvist-cli lists show LIST_ID --tasks
# Or equivalently:
checkvist-cli tasks get --list-id LIST_ID
```

### 3. Working with Tasks

**List all tasks in a checklist:**
```bash
# Text format shows hierarchical tree with indentation
checkvist-cli tasks get --list-id LIST_ID

# JSON format for programmatic processing
checkvist-cli --format json tasks get --list-id LIST_ID
```

**Task hierarchy:**
- Tasks are displayed with 2-space indentation per level
- Parent-child relationships are shown by indentation
- Each task has an ID and content

**Create a task:**
```bash
# Create top-level task
checkvist-cli tasks create --list-id LIST_ID --content "Task description"

# Create subtask under a parent
checkvist-cli tasks create --list-id LIST_ID --content "Subtask" --parent-id PARENT_TASK_ID
```

**Update a task:**
```bash
# Update content
checkvist-cli tasks update --list-id LIST_ID --task-id TASK_ID --content "New content"

# Mark as done
checkvist-cli tasks update --list-id LIST_ID --task-id TASK_ID --status done

# Mark as open
checkvist-cli tasks update --list-id LIST_ID --task-id TASK_ID --status open

# Move task to different parent
checkvist-cli tasks update --list-id LIST_ID --task-id TASK_ID --parent-id NEW_PARENT_ID
```

**Delete a task:**
```bash
checkvist-cli tasks remove --list-id LIST_ID --task-id TASK_ID
```

### 4. Working with Notes

Notes are additional information attached to specific tasks.

**List notes for a task:**
```bash
checkvist-cli notes list --list-id LIST_ID --task-id TASK_ID
# Or the shorthand:
checkvist-cli notes --list-id LIST_ID --task-id TASK_ID
```

**Create a note:**
```bash
checkvist-cli notes create --list-id LIST_ID --task-id TASK_ID --text "Note content"
```

**Update a note:**
```bash
checkvist-cli notes update --list-id LIST_ID --task-id TASK_ID --note-id NOTE_ID --text "Updated content"
```

**Delete a note:**
```bash
checkvist-cli notes remove --list-id LIST_ID --task-id TASK_ID --note-id NOTE_ID
```

### 5. Backup

Export all checklists to OPML format:

```bash
# Export to current directory
checkvist-cli backup

# Export to specific directory
checkvist-cli backup --output ~/backups/checkvist

# Silent mode (no progress logging)
checkvist-cli backup --output ~/backups --nolog
```

Each checklist is saved as `ID-Name.opml` in the output directory.

## Output Formats

### Text Format (default)

Tab-separated values, one item per line:
```
12345	My Checklist Name
67890	Another Checklist
```

Tasks show hierarchy with indentation (2 spaces per level):
```
100	Parent Task
  101	Child Task
  102	Another Child
    103	Grandchild Task
```

### JSON Format

Use `--format json` for programmatic processing:
```bash
checkvist-cli --format json lists get
```

Returns structured JSON with descriptive keys:
```json
{
  "lists": [
    { "id": 12345, "name": "My Checklist", ... }
  ]
}
```

## Profiles

Support for multiple Checkvist accounts via profiles:

```bash
# Use specific profile
checkvist-cli --profile work lists

# Or set environment variable
export CHECKVIST_PROFILE=work
checkvist-cli lists
```

Profiles are defined in `~/.checkvist/auth.ini`:
```ini
[default]
username = user@example.com
remote_key = YOUR_API_KEY

[work]
username = user@company.com
remote_key = WORK_API_KEY
```

## Common Workflows

### Workflow 1: Browse and explore tasks

When user wants to see their Checkvist data:

1. List all checklists to find the right one:
   ```bash
   checkvist-cli lists
   ```

2. Show tasks in a specific list:
   ```bash
   checkvist-cli tasks get --list-id LIST_ID
   ```

3. If user wants to see notes on a specific task:
   ```bash
   checkvist-cli notes --list-id LIST_ID --task-id TASK_ID
   ```

### Workflow 2: Create a new task hierarchy

When user wants to add structured tasks:

1. Create parent task:
   ```bash
   checkvist-cli tasks create --list-id LIST_ID --content "Project: New Feature"
   ```
   Note the returned task ID.

2. Create subtasks:
   ```bash
   checkvist-cli tasks create --list-id LIST_ID --content "Design mockups" --parent-id PARENT_ID
   checkvist-cli tasks create --list-id LIST_ID --content "Implement backend" --parent-id PARENT_ID
   checkvist-cli tasks create --list-id LIST_ID --content "Write tests" --parent-id PARENT_ID
   ```

3. Add notes if needed:
   ```bash
   checkvist-cli notes create --list-id LIST_ID --task-id TASK_ID --text "Important details..."
   ```

### Workflow 3: Process and update tasks

When user wants to manage existing tasks:

1. View current tasks:
   ```bash
   checkvist-cli tasks get --list-id LIST_ID
   ```

2. Mark tasks as done:
   ```bash
   checkvist-cli tasks update --list-id LIST_ID --task-id TASK_ID --status done
   ```

3. Update task content if needed:
   ```bash
   checkvist-cli tasks update --list-id LIST_ID --task-id TASK_ID --content "Updated description"
   ```

### Workflow 4: Backup all data

When user wants to backup their Checkvist data:

```bash
# Create backup directory with timestamp
BACKUP_DIR=~/backups/checkvist-$(date +%Y%m%d)
checkvist-cli backup --output "$BACKUP_DIR"
```

## Error Handling

### Exit Codes
- **0**: Success
- **2**: Command-line argument error
- **3**: Authentication error (need to login)
- **4**: Network/connection error
- **5**: API/data error
- **6**: Local error (config file issues)

### Common Issues

**Authentication errors (exit code 3):**
- Run `checkvist-cli auth status` to check
- Run `checkvist-cli auth login` to re-authenticate
- Check `~/.checkvist/auth.ini` exists and has correct permissions (0600)

**Network errors (exit code 4):**
- Check internet connection
- Verify base URL is correct (default: https://checkvist.com)

**API errors (exit code 5):**
- Check list/task/note IDs are valid
- Ensure list is not empty before deleting

## Best Practices

1. **Check authentication first**: Always verify auth status before complex operations
2. **Use JSON format for scripting**: When processing output programmatically, use `--format json`
3. **Parse task hierarchy**: In text format, track indentation to understand parent-child relationships
4. **Handle IDs carefully**: List IDs, task IDs, and note IDs are all required for operations - keep track of them
5. **Regular backups**: Encourage users to backup their data periodically
6. **Verbose logging**: Use `-v` or `-vv` flags for debugging issues

## Tips for Claude

- **When listing tasks**: Parse the indentation (2 spaces per level) to understand hierarchy
- **When creating subtasks**: Always get the parent task ID first
- **When user says "my tasks"**: Ask which list they want to work with, or show all lists first
- **For bulk operations**: JSON format is easier to parse programmatically
- **Error messages**: Exit codes help diagnose issues - check them when commands fail
- **IDs in output**: Text format shows IDs before tab, JSON format has explicit "id" fields

## Getting Started

If user has never used checkvist-cli:

1. Guide them through authentication:
   ```bash
   checkvist-cli auth login
   ```
   They'll need their Checkvist username and remote API key from https://checkvist.com/auth/profile

2. Verify it works:
   ```bash
   checkvist-cli auth status
   ```

3. Show their lists:
   ```bash
   checkvist-cli lists
   ```

4. Ready to work with tasks!

## Limitations

- Lists must be empty to delete them
- Tasks can only have one parent
- Authentication tokens are automatically managed (stored in `~/.checkvist/token`)
- Text format uses tabs - be careful when parsing
- Hierarchical display in text format uses 2-space indentation

## Reference

- Full documentation: See `man checkvist-cli` or `/home/kappa/work/checkvist-cli/docs/checkvist-cli.1`
- Checkvist API: https://checkvist.com/auth/api
- Project repository: https://github.com/kappa/checkvist-cli
