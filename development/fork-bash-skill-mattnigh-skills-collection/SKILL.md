---
name: Fork Bash Skill
description: Execute agentic coding tools directly via bash commands with output capture. Use this when the user requests to run AI agents (Gemini, Claude Code, etc.) and get their results directly.
---

# Purpose

Execute agentic coding tools directly via bash commands and capture their output in real-time. This is a simpler and more reliable alternative to fork-terminal for one-off tasks.

Follow the `Instructions`, execute the `Workflow`, based on the `Cookbook`.

## Variables

ENABLE_GEMINI_CLI: true
ENABLE_CLAUDE_CODE: true
ENABLE_CODEX_CLI: true
AGENTIC_CODING_TOOLS: gemini, claude-code, codex

## Instructions

- Based on the user's request, follow the `Cookbook` to determine which tool to use.
- Execute the command directly using bash and capture stdout/stderr
- Return the output to the user immediately

## Workflow

1. Understand the user's request
2. Follow the `Cookbook` to determine which tool to use
3. Construct the appropriate bash command
4. Execute using the Bash tool with appropriate timeout
5. Return results to the user

## Cookbook

### Gemini CLI

- IF: The user requests Gemini to execute a task AND `ENABLE_GEMINI_CLI` is true
- THEN: Read and execute: `.claude/skills/fork-bash/cookbook/gemini-cli.md`
- EXAMPLES:
  - "Use Gemini to scrape the latest news from CNN"
  - "Ask Gemini to analyze this webpage"
  - "Run Gemini with yolo mode to get information about X"

### Claude Code

- IF: The user requests Claude Code agent AND `ENABLE_CLAUDE_CODE` is true
- THEN: Read and execute: `.claude/skills/fork-bash/cookbook/claude-code.md`
- EXAMPLES:
  - "Use Claude Code to refactor this file"
  - "Ask Claude Code to analyze the codebase"

### Codex CLI

- IF: The user requests Codex AND `ENABLE_CODEX_CLI` is true
- THEN: Read and execute: `.claude/skills/fork-bash/cookbook/codex-cli.md`
- EXAMPLES:
  - "Use Codex to generate code for X"
  - "Ask Codex to explain this function"

## Notes

- This skill executes commands synchronously and captures output
- Use appropriate timeouts based on task complexity
- Always use YOLO mode (-y flag) for automated execution
- Output is captured directly from stdout/stderr
