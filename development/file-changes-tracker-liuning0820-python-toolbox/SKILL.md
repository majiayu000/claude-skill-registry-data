---
name: file-changes-tracker
description: Track and list files modified in the current workspace within the last week, ordered by most recent modification date. Use when you need to see recent file changes, track development progress, or identify files that have been worked on recently in a git repository.
---

# File Changes Tracker

This skill helps you track and analyze recent file modifications in your workspace. It provides a comprehensive view of files changed in the last 7 days, sorted by modification date to help you understand recent development activity.

## Quick Start

To list all files changed in the current workspace in the last week:

```bash
python scripts/list_recent_changes.py
```

For a different workspace path:

```bash
python scripts/list_recent_changes.py --path /path/to/workspace
```

For JSON output (useful for further processing):

```bash
python scripts/list_recent_changes.py --json
```

## How It Works

The skill uses git log to analyze commit history and identify files that have been modified. It:

1. **Scans git history** for the last 7 days using `git log --since="1 week ago"`
2. **Tracks file modifications** and keeps the most recent change for each file
3. **Sorts by date** with the most recently modified files first
4. **Provides detailed information** including modification date, author, and commit hash

## Output Format

The default output shows:
- File path (truncated if very long)
- Last modification date and time
- Author of the change
- Commit hash (shortened)

Example output:
```
Files changed in the last week (ordered by most recent modification):
================================================================================
src/main.py                 2024-12-26 14:30  John Doe     abc1234
README.md                   2024-12-25 09:15  Jane Smith   def5678
config/settings.json        2024-12-24 16:45  John Doe     ghi9012

Total: 3 files changed
```

## Use Cases

- **Development tracking**: See what files you've been working on recently
- **Code review preparation**: Identify files that need review
- **Progress reporting**: Show recent development activity
- **File cleanup**: Find files that may need attention
- **Collaboration**: Share recent changes with team members

## Requirements

- Must be run in a git repository
- Git must be installed and accessible
- Python 3.6+ required

## Script Options

- `--path PATH`: Specify a different workspace directory (default: current directory)
- `--json`: Output results in JSON format for programmatic use

## Troubleshooting

**"Error: [path] is not a git repository"**
- Ensure you're running the script in a directory that's a git repository
- Use `--path` to specify the correct repository location

**No files shown**
- Check if there have been any commits in the last week
- Verify the repository has recent activity

**Permission errors**
- Ensure you have read access to the git repository
- Check that git commands work in your terminal