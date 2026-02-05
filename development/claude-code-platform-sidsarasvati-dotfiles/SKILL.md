---
name: Claude Code Platform
description: Expert knowledge of Claude Code CLI tools (Read, Write, Edit, Bash, Grep, Glob, Task, MCP), features (Skills, Checkpoints, Hooks), and best practices for agentic coding assistance
---

# Claude Code Platform Skill

This skill provides comprehensive expertise on using Claude Code effectively.

**Skill Directory**: `~/.claude/skills/claude-code-platform/`

## Core Tool Knowledge

### File Operations
**Read Tool**: Read files with `file_path` (required), optional `offset` and `limit` for large files. Returns up to 2000 lines, supports images/PDFs/Jupyter notebooks.

**Write Tool**: Create files with `file_path` and `content`. MUST Read existing files first. Always prefer Edit over Write for existing files.

**Edit Tool**: Replace text with `file_path`, `old_string`, `new_string`, optional `replace_all`. String must be unique or use replace_all. MUST Read file first.

**Glob Tool**: Find files with `pattern` (e.g., `**/*.ts`) and optional `path`. Returns sorted by modification time.

**Grep Tool**: Search with `pattern`, optional `path`, `output_mode` (content/files_with_matches/count), `-i` for case-insensitive, `-n` for line numbers, `multiline` for cross-line patterns.

### Execution
**Bash Tool**: Execute commands with `command` (required), `description` (recommended), `timeout` (default 120000ms, max 600000ms), `run_in_background` (for async execution). Always quote paths with spaces. Use && for dependent commands, parallel tool calls for independent commands.

**Task Tool**: Launch subagents with `subagent_type` and `prompt`. Available types: general-purpose, Explore (quick/medium/very thorough), pragmatic-lead, qa, plus custom agents.

### Core Patterns
**Parallel Execution**: Call multiple independent tools in one message for dramatic speedup.

**Tool Selection**: Specialized tools (Read/Edit/Grep/Glob) > Bash commands for file operations.

**Progressive Loading**: Glob → Grep → Read (narrow before deep dive).

## When You Need More Details

### Complete Tool Parameters and Usage
For detailed parameter specifications, return formats, error handling, and advanced usage patterns, read:
```bash
cat ~/.claude/skills/claude-code-platform/tools-reference.md
```

### MCP Integration Patterns
For Model Context Protocol server configuration, tool naming conventions (mcp__server__function), and integration with Linear/Calendar/Stripe etc, read:
```bash
cat ~/.claude/skills/claude-code-platform/mcp-integration.md
```

### Advanced Features
For Skills system details, Checkpoints (save/restore state), custom Subagent creation, Hooks (PreToolUse/PostToolUse), and Haiku 4.5 model usage, read:
```bash
cat ~/.claude/skills/claude-code-platform/advanced-features.md
```

### Performance Optimization
For parallel execution patterns, context efficiency, workflow patterns (investigation/debugging/research), git protocols, and error recovery, read:
```bash
cat ~/.claude/skills/claude-code-platform/best-practices.md
```

### Troubleshooting
For debugging tool failures, permission issues, MCP connection problems, git errors, and common error patterns with solutions, read:
```bash
cat ~/.claude/skills/claude-code-platform/troubleshooting.md
```

## Quick Reference Examples

**Reading multiple files in parallel**:
```
✓ Read file1.ts + Read file2.ts + Read file3.ts (one message)
✗ Read file1.ts → wait → Read file2.ts (sequential)
```

**Finding and searching**:
```
Step 1: Glob **/*.ts
Step 2: Grep "pattern" --type ts --output-mode files_with_matches
Step 3: Read specific matches
```

**Bash best practices**:
```
✓ git add . && git commit -m "msg" && git push (sequential with &&)
✓ cd "/path with spaces/" (quoted paths)
✗ cat file.txt (use Read tool instead)
```

**MCP tool naming**: `mcp__server-name__function-name`

**Task tool for deep work**: Use Explore agent (thoroughness: quick/medium/very thorough) for codebase exploration.

**Haiku vs Sonnet**: Haiku 4.5 = routine tasks (2x speed, 1/3 cost), Sonnet 4.5 = complex reasoning.

## Key Principles

1. **Specialized tools > Bash** for file operations
2. **Parallel when independent** for speed
3. **Progressive disclosure** - Glob → Grep → Read
4. **Read before Write/Edit** always
5. **Verify after critical operations**
6. **Clear tool descriptions** for user transparency

## This Skill Uses Progressive Disclosure

- **Level 1** (This file): Core tool knowledge and quick reference
- **Level 2** (Reference files): Detailed docs loaded via bash when needed
- **Level 3** (On-demand): Specific sections of reference files as required

When you need deeper information, read the appropriate reference file from the skill directory using bash commands shown above.

---

*Version: 2.0 - Updated Oct 16, 2025 for proper progressive disclosure*
