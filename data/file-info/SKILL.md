---
name: file-info
description: Provides detailed file statistics including lines, size, and modification time when user asks for file info or stats
---

# File Info Skill

When the user asks for information about a file (stats, details, info, etc.), use this skill to provide comprehensive file statistics.

## What to do

1. Get the file path from the user's request
2. Run the `scripts/get_file_stats.sh` script in this skill's directory, passing the file path as an argument
3. The script will:
   - Create `/tmp/executed.txt` as proof of execution
   - Gather file statistics (lines, size, modification time)
   - Handle both files and directories
4. Present the script output in a clean format

## Example

When user asks: "Give me info on main.go"

You should respond with something like:
```
File: main.go
Lines: 234
Size: 8.2 KB
Modified: 2025-01-15 14:30:22
Type: Go source file
```

## Notes

- Always use absolute paths
- Handle errors gracefully (file not found, permission denied, etc.)
- For directories, mention it's a directory and list file count
