---
name: context-tools
description: Context management tools for Claude Code - provides intelligent codebase mapping with Python, Rust, and C++ parsing, duplicate detection, and MCP-powered symbol queries. Use this skill when working with large codebases that need automated indexing and context management.
---

# Context Tools for Claude Code

This skill provides intelligent context management for large codebases through:

- **Repository Mapping**: Parses Python, Rust, and C++ code to extract classes, functions, and methods
- **Duplicate Detection**: Identifies similar code patterns using fuzzy matching
- **MCP Symbol Server**: Enables fast symbol search via `search_symbols` and `get_file_symbols` tools
- **Automatic Indexing**: Background incremental updates as files change

## Included Components

### Hooks
- **SessionStart**: Generates project manifest and starts background indexing
- **PreToolUse**: Monitors for file changes and triggers reindexing
- **PreCompact**: Refreshes context before compaction
- **SessionEnd**: Cleans up background processes

### MCP Server (repo-map)
- `search_symbols(pattern, kind?, limit?)` - Search symbols by name pattern
- `get_file_symbols(file_path)` - Get all symbols in a specific file

### Slash Commands
- `/context-tools:repo-map` - Regenerate repository map
- `/context-tools:manifest` - Refresh project manifest
- `/context-tools:learnings` - Manage project learnings
- `/context-tools:status` - Show plugin status

## Language Support

| Language | Parser | File Extensions |
|----------|--------|-----------------|
| Python | AST | `.py` |
| Rust | tree-sitter-rust | `.rs` |
| C++ | tree-sitter-cpp | `.cpp`, `.cc`, `.cxx`, `.hpp`, `.h`, `.hxx` |
