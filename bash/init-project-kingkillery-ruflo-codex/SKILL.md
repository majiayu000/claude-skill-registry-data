---
name: init-project
description: Initialize a new Ruflo project with MCP tools, hooks, and agent configuration
argument-hint: "[--preset standard|minimal|full]"
allowed-tools: Bash(npx *) Read Write Edit
---
Run `npx @claude-flow/cli@latest init --wizard` to set up the project interactively, or `npx @claude-flow/cli@latest init --preset standard` for defaults.

This creates project context files (e.g., AGENTS.md or CODEX.md), IDE settings, and claude-flow config with MCP server registration for the `ruflo` MCP tools. The exact filenames depend on whether the project is primarily using Codex, Claude Code, or both.
