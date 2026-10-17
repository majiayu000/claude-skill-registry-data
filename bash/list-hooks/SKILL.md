---
name: list:hooks
description: List all configured hooks
disable-model-invocation: true
allowed-tools: Bash
---

## Context

Show all configured hooks from both project-level and global Claude Code settings.

## Your task

Read the settings files and display hooks in a compact format showing:

- Event type
- Matcher pattern
- Brief description or script name (basename only for file paths)

Do NOT print full command text. For command hooks, show only the script filename without the full path or inline commands.
