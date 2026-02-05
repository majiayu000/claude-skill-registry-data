---
name: codex-cli-subagent
description: Helps you to run a subagent using codex exec
---

This skill lets you spawn a nested Codex process (a “subagent”) using `codex exec` so it can work with the same project and AGENTS.md instructions.

```shell
filename="$(openssl rand -hex 4)"
codex exec "count the total number of lines of code in this project" 2>>/tmp/${filename}.log
```

In non-interactive mode, `codex exec` runs without a TUI and follows the configured approval/sandbox policy (flags and/or `~/.codex/config.toml`). By default it runs in `read-only` mode, so it cannot edit files or run commands that require network access.

When you use this skill, follow these logging rules:

- Before running `codex exec`, generate a unique log file name with `openssl rand -hex 4`.
- By default, append `2>>/tmp/${filename}.log` to your `codex exec` command so only the subagent’s final message is visible to the caller, while stderr is captured for debugging.
- If a run fails, behaves unexpectedly, or the user explicitly asks to see what the inner agent is doing, read the log file (for example: `cat /tmp/${filename}.log`).

Since the `codex exec` may run couple hours, set a generous timeout so long-running subagent work can complete:

- Use a timeout of at least 60 minutes for the `Run` (or `Bash`) tool unless the user explicitly requests other limit.

Use this skill when you want a focused helper agent (for refactors, audits, scripted operations, or scans) while keeping your main session and context intact.

Use `codex exec --full-auto` to allow file edits. Use `codex exec --sandbox danger-full-access` to allow edits and networked commands, but only when the user clearly permits this level of access.

### Practical gotchas

- Prefer stdin for long prompts to avoid shell quoting/globbing issues: `codex exec - < /tmp/prompt.md`.
- If you need built-in web search, pass `--search` (otherwise assume “no web tool” and use `curl`/repo sources).
- Don’t run nested subagents (avoid calling `codex exec` from inside a `codex exec` session).
- Consider `--output-last-message /tmp/${filename}.out` to capture the final answer without scraping logs.

### Key Flags

- `--full-auto`: Unattended operation with workspace-write sandbox
- `--dangerously-bypass-approvals-and-sandbox` or `--yolo`: Complete hands-off mode (use carefully)
- `--cd <path>`: Set working directory
- `--model <model>` or `-m`: Specify model (e.g., `-m gpt-5.1-codex-max`)
- `--sandbox`: Sandbox types:
  - `read-only`: No file edits, no networked commands
  - `workspace-write`: Can edit files in the workspace
  - `danger-full-access`: No sandboxing; full access (use with care)
- `--search`: Enable built-in web search tool
- `--config`: Pass config variables:
  - `model_reasoning_effort`: Model reasoning effort: `low`, `medium`, `high`;

### Examples

```bash
# As a subagent, perform automated refactoring
filename="$(openssl rand -hex 4)"
codex exec --full-auto "Update all README links to HTTPS" 2>>/tmp/${filename}.log

# Run in a specific project directory
filename="$(openssl rand -hex 4)"
codex exec --cd /path/to/project "Fix failing tests" 2>>/tmp/${filename}.log

# Use AGENTS.md context for a focused refactor
filename="$(openssl rand -hex 4)"
codex exec --cd /path/to/project "Using this repo's AGENTS.md instructions, refactor the test helpers for clarity and consistency" 2>>/tmp/${filename}.log

filename="$(openssl rand -hex 4)"
codex exec --model gpt-5.1-codex-max --sandbox workspace-write --config model_reasoning_effort=medium - < /tmp/some-big-prompt.md 2>>/tmp/${filename}.log

# For audits / deep analysis
filename="$(openssl rand -hex 4)"
codex exec --model gpt-5.2 --sandbox read-only --config model_reasoning_effort=high "Audit this repo for security issues" 2>>/tmp/${filename}.log
```

### Input Methods

```bash
# Pipe prompt from file
filename="$(openssl rand -hex 4)"
codex exec - < prompt.txt 2>>/tmp/${filename}.log

# Standard input
filename="$(openssl rand -hex 4)"
echo "Review this code" | codex exec - 2>>/tmp/${filename}.log
```

When this skill is invoked, you should decide:

- Whether a subagent is appropriate (e.g., long-running refactor, scan, or analysis).
- Which flags, sandbox level, and model to use based on user intent and risk.
- For code changes: default to `--model gpt-5.1-codex-max --config model_reasoning_effort=medium` unless the user explicitly requests otherwise.
- For audits: default to `--model gpt-5.2 --config model_reasoning_effort=high` unless the user explicitly requests otherwise.
- Whether to keep logs suppressed (default: `2>>/tmp/${filename}.log` or read/tail `/tmp/${filename}.log`)
