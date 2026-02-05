---
name: code-pointer
description: Use the VSCode CLI to open files at specific line and column positions when explaining code, debugging, pointing to TODOs, or guiding users to specific locations in files. Automatically invoked when Claude needs to show users exactly where in a file to look.
allowed-tools: Bash
---

# Code Pointer

## Overview

Open files in VSCode at precise line (and optionally column) positions using the `code` CLI. Use this skill whenever pointing users to specific locations in code, configuration files, documentation, or any text file.

## When to Use

Invoke this skill automatically when:
- **Explaining code**: Showing specific lines when discussing implementation
- **Debugging**: Pointing to error locations or problematic code sections
- **Code reviews**: Highlighting lines that need attention
- **TODO navigation**: Opening files at TODO(human) or other task markers
- **Documentation references**: Showing specific sections in config files or docs
- **Teaching**: Guiding users to exact locations for hands-on work

## How to Use

### Basic Syntax

Open file at specific line:
```bash
code -g path/to/file.js:42
```

Open file at line and column:
```bash
code -g path/to/file.js:42:10
```

### Best Practices

**1. Always validate file exists first:**
```bash
if [[ -f "path/to/file.js" ]]; then
    code -g path/to/file.js:42
else
    echo "File not found: path/to/file.js"
fi
```

**2. Use absolute paths for reliability:**
```bash
# Convert to absolute path
ABS_PATH="$(cd "$(dirname "path/to/file.js")" && pwd)/$(basename "path/to/file.js")"
code -g "$ABS_PATH:42"
```

**3. Quote paths with spaces:**
```bash
code -g "my project/src/app.js:100"
```

**4. Provide context to user:**
```bash
echo "Opening publisher.py at line 36 (MQTT connection TODO)"
code -g PiPico/publisher.py:36
```

## Common Patterns

### Opening Multiple Locations
```bash
# Open several related files at their relevant sections
code -g src/publisher.py:36 -g src/subscriber.py:45
```

### Window Control
```bash
# Open in new window (avoid disturbing current work)
code -n -g file.js:10

# Reuse existing window (add as new tab)
code -r -g file.js:10
```

### Finding and Opening TODOs
```bash
# Search for TODOs, then open at found location
grep -n "TODO(human)" *.py
# Publisher has TODO at line 36
code -g publisher.py:36
```

## Important Notes

**Line and Column Numbering:**
- Lines are 1-indexed (line 1 is the first line)
- Columns are 0-indexed (column 0 is the first character)

**Path Resolution:**
- Relative paths resolve from current working directory
- Absolute paths are more reliable for skills
- Paths with spaces must be quoted

**Non-existent Files:**
- VSCode will create empty file if path doesn't exist
- Position will be applied when user starts editing

## Technical Reference

For detailed documentation, see:

- **`references/cli_basics.md`** - Core syntax, line/column numbering, path handling
- **`references/advanced_usage.md`** - Window control, multiple files, diff/merge
- **`references/troubleshooting.md`** - Common errors and solutions
- **`references/integration_patterns.md`** - Best practices for scripts and automation
