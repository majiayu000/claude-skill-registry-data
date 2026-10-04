---
name: terminal
description: Execute shell commands on the server
activation_keywords: [terminal, shell, command, execute, bash, sh, zsh, cli, cmd, run]
---

# Terminal Skill

Executes arbitrary shell commands on the server (not on user's machine). Useful for:
- Running scripts or one-liners
- Checking system state (OS, processes, files)
- Building or compiling code
- Running tests or benchmarks
- Installing or updating packages
- Any CLI tool available on the server

Use `builtin_terminal` tool with fields:
- `command` (required): shell command to execute (e.g., `ls -la /tmp`)
- `timeout` (optional): execution timeout in seconds (default 30, max 300)
- `workdir` (optional): working directory for the command

When the command generates image files (e.g., `output.png`, `screenshot.jpg`), **always return everything in a single message**. Embed the image inline via `![alt](data:image/png;base64,...)` — do not split into multiple messages.

⚠️ WARNING: This tool runs commands directly on the server with the full permissions of the process. Every invocation requires explicit user approval.
