---
name: launch
disable-model-invocation: true
description: Start (or attach to) the Apeiron editor for the current folder's project
argument-hint: [project folder]
allowed-tools: Bash(ngine mcp list:*), Bash(ngine mcp status:*)
---

Make sure an Apeiron editor is running for the project in `$ARGUMENTS` (default: the current
folder). First run `ngine mcp list`: if an editor already has this project open, report its port and
stop. Otherwise call the `editor.context` op through the `ngine` MCP server — the bridge starts the
editor for this folder's project on the first real call and closes it when this session ends — and
report what `editor.context` returns. Never start a second editor for a project that already has one.
