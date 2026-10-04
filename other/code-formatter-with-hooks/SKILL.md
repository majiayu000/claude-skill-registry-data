---
name: code-formatter
description: Automatically format code files using project-specific formatters. Use when editing code files or when the user asks to format code.
allowed-tools: Read, Edit, Write, Bash
hooks:
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: '"$CLAUDE_PROJECT_DIR"/.claude/hooks/format-code.sh $TOOL_INPUT'
          timeout: 30
---

# Code Formatter

This skill automatically formats code files after editing or writing, using project-specific formatters.

## How It Works

When you edit or write code files, a post-edit hook runs to format the file using:

- Python: `black` or `autopep8`
- JavaScript/TypeScript: `prettier`
- Go: `gofmt`
- Rust: `rustfmt`

## Instructions

1. **Edit or write code** as normal
2. **Automatic formatting** happens via the PostToolUse hook
3. **Formatted code** is applied back to the file

## Hook Script

The hook script (`.claude/hooks/format-code.sh`) should:

- Detect file type from extension
- Run appropriate formatter
- Handle errors gracefully
- Return formatted content

## Example Hook Script

```bash
#!/bin/bash
# .claude/hooks/format-code.sh

FILE_PATH=$(echo "$1" | jq -r '.file_path')
EXT="${FILE_PATH##*.}"

case "$EXT" in
  py)
    black "$FILE_PATH" 2>/dev/null || autopep8 -i "$FILE_PATH"
    ;;
  js|jsx|ts|tsx)
    prettier --write "$FILE_PATH" 2>/dev/null
    ;;
  go)
    gofmt -w "$FILE_PATH"
    ;;
  rs)
    rustfmt "$FILE_PATH"
    ;;
esac

exit 0
```

## Setup

1. Create the hook script at `.claude/hooks/format-code.sh`
2. Make it executable: `chmod +x .claude/hooks/format-code.sh`
3. Install formatters for your languages
