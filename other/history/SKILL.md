---
name: history
version: 1.1.0
description: |
  Browse Claude Code conversation history. List past sessions with concise
  summaries, view full conversations, and search across all sessions.
allowed-tools:
  - Bash
  - AskUserQuestion
---

## Overview

This skill helps the user browse their Claude Code conversation history using the `cc-history` CLI tool located at `~/.local/bin/cc-history`.

## Default Behavior

When the user types `/history` with no arguments, **ask the user to choose**:

> 请选择查看方式：
> 1. **最近记录** — 显示最近 15 条对话
> 2. **查看全部** — 显示所有对话记录
> 3. **关键词搜索** — 输入关键词查找相关对话
>
> 输入 1/2/3 或直接输入关键词搜索：

Then act based on their choice:
- **1 or 最近** → run `cc-history list --limit 15`
- **2 or 全部** → run `cc-history list --limit 999`
- **3 or any keyword** → run `cc-history search <keyword>`
- If user types `/history <keyword>` with an argument, skip the menu and directly run `cc-history search <keyword>`

**IMPORTANT**: After running the command, copy-paste the result into a fenced code block in your reply — do NOT let it stay hidden inside a collapsed tool call. The user must see the list without clicking anything.

After showing results, remind the user:
- Say a number or session ID to view details
- Say a keyword to search further

## Commands

```bash
cc-history list [--limit N] [--project PATH]   # list sessions with summaries
cc-history view <session-id>                    # view full conversation
cc-history search <keyword>                     # search across sessions
cc-history dump <session-id>                    # raw output for analysis
cc-history json                                 # JSON list for processing
```

## Workflow

### If user wants to browse (default)
Run `cc-history list` and show the output.

### If user wants to view a specific session
```bash
cc-history view <session-id>
```

### If user wants a summary for reference
```bash
cc-history dump <session-id>
```
Read the dump and summarize the key decisions, changes, and outcomes.

### If user wants to search
```bash
cc-history search <keyword>
```
Show results and offer to view matching sessions.

## Session ID Usage

Session IDs only need the first 6-8 characters (e.g., `0575c184`). The tool will match by prefix.

## Notes

- Sessions are stored in `~/.claude/projects/` organized by working directory
- `~` refers to `/Users/adam` (the home directory)
- Each session is a JSONL file with the full conversation
- The tool automatically skips system messages and tool results, showing only user/assistant messages
