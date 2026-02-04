---
name: markdown-writer
description: Write markdown content to file paths using the MCP markdown-writer server. Use when you need to save generated markdown content to a file, especially in contexts where (1) The Write tool is unavailable or restricted, (2) You need guaranteed atomic writes with verification, (3) Writing markdown files for documentation, reports, or research outputs, (4) An agent needs to persist markdown without user permission prompts.
allowed-tools: mcp__markdown-writer__write, mcp__markdown-writer__verify
---

# Markdown Writer

Write markdown content to disk reliably using the MCP markdown-writer server with atomic writes and verification.

## Usage

### Write a file

Use the `mcp__markdown-writer__write` tool directly:

**Example:**
```
Use mcp__markdown-writer__write to write the following content to /path/to/file.md:

# Your Markdown Content

Multi-line content works fine.

## Sections supported
- Lists
- Code blocks
- All markdown features
```

**Parameters:**
- `path`: Absolute path (e.g., `/tmp/test.md`) or relative path from repository root (e.g., `docs/test.md`)
- `content`: Markdown content to write

### Verify a file (optional)

Use the `mcp__markdown-writer__verify` tool:

**Example:**
```
Use mcp__markdown-writer__verify to check /path/to/file.md
```

**Parameters:**
- `path`: Absolute path (e.g., `/tmp/test.md`) or relative path from repository root (e.g., `docs/test.md`)

## Key Behaviors

- **Creates parent directories** automatically
- **Overwrites existing files** without prompting
- **Atomic writes** via temporary files and rename
- **Supports** absolute paths (e.g., `/tmp/file.md`) and relative paths from repository root (e.g., `docs/file.md`)
- **Path validation** prevents traversal attacks (../)
- **Returns** file size and statistics

## When to Use This Skill

Use this skill when:
- You need to write markdown files from within an agent/subagent
- The Write tool is restricted or unavailable
- You need guaranteed atomic writes
- You're generating documentation, reports, or research outputs
- You want to avoid user permission prompts for file writes

## Notes

- The MCP server handles all file operations
- No external Python dependencies required
- All operations are logged for debugging
