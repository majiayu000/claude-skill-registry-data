---
name: claude-code
description: Delegate coding to Claude Code CLI (features, PRs).
version: 2.2.0
author: Hermes Agent + Teknium
license: MIT
platforms:
- linux
- macos
- windows
metadata:
  hermes:
    tags:
    - Coding-Agent
    - Claude
    - Anthropic
    - Code-Review
    - Refactoring
    - PTY
    - Automation
    related_skills:
    - codex
    - hermes-agent
    - opencode
    user_owner: the user ([redacted])
    billing_mode: Pro-Subscription via OAuth (claude.ai) — NOT API-Token-Plan
    role_in_swarm: Worker-Heavy (Backup)
    primary_models:
      sonnet-4-5: default for Refactor/Code-Review/Big-Edit
      haiku-4-5: lightweight tasks, mini-edits, lookups
      opus-4: architecture reviews >10k LOC (use sparingly, on the user's request only)
lane: koenigin
reasoning_effort: xhigh
---
# Claude Code — Hermes Orchestration Guide

Delegate coding tasks to [Claude Code](https://code.claude.com/docs/en/cli-reference) (Anthropic's autonomous coding agent CLI) via the Hermes terminal. Claude Code v2.x can read files, write code, run shell commands, spawn subagents, and manage git workflows autonomously.

## the user's Profile (2026-07-04)

- **Auth:** Claude Pro Subscription via OAuth (`claude auth status` → `subscriptionType: "pro"`, `authMethod: "claude.ai"`)
- **Account:** `[redacted]` (Org-ID `4b24e94b-9e73-4abb-b3d0-0a8f2280ec01`)
- **No `ANTHROPIC_API_KEY` set** — do NOT reference it; Pro-OAuth is the only active auth path
- **CLI path:** `~/.local/bin/claude` (v2.1.201)
- **Billing reality:** Pro has stricter limits than API-Token-Plan; treat every delegation as budget-conscious

## the user's Sparsamkeits-Regeln (KRITISCH)

**Delegiere NUR wenn MiniMax M3/StepFun NICHT reicht.** Konkret:

| ✅ Delegieren an Claude | ❌ NICHT delegieren |
|---|---|
| Big Refactor (>1 file, >200 LOC) | Mini-Edit (1-2 lines) |
| Architektur-Review / Design-Feedback | Bug-Search in kleinem Code-Snippet |
| Multi-File Refactor / Test-Writing | Doku-Recherche / Lookups |
| Komplexe Code-Analyse (race conditions, security) | Trivial-Syntax-Korrektur |

**Hard rules:**
- ⏱️ **Immer** `--max-turns` setzen (Default 10, Max 30 für Big-Refactor)
- 💰 **Immer** `--max-budget-usd` setzen (Default 0.50, Max 2.00 für Big-Refactor)
- 🎯 Print-Mode bevorzugen (`claude -p ...`) — keine unnötigen Multi-Turn-Sessions
- 🚫 Opus 4 NUR auf the user's explizite Anweisung
- 📊 Task-Brief immer strukturiert (Yuno-Style: Goal, Constraints, Output-Format)
- 🔄 Wenn 2+ ähnliche Tasks anstehen → batchen statt einzeln delegieren

## Model-Auswahl-Schnellreferenz

```bash
# Default: Refactor, Code-Review, Big-Edit
claude -p "<task>" --model claude-sonnet-4-5 --max-turns 10 --max-budget-usd 0.50

# Lightweight: Mini-Edits, Bug-Fixes, Lookups
claude -p "<task>" --model claude-haiku-4-5 --max-turns 5 --max-budget-usd 0.20

# Heavy: nur auf the user's Anweisung
claude -p "<task>" --model claude-opus-4 --max-turns 30 --max-budget-usd 2.00
```

## When to Use This Skill

- One-shot coding tasks delegated from Hermes (fix bug, add feature, refactor)
- Multi-turn interactive coding sessions (review → fix → test cycles)
- PR reviews and code audits
- Parallel coding tasks (run multiple Claude instances on independent work)
- Any task requiring autonomous git workflow (worktree, commit, push)

**For other autonomous coding agents, see:** `codex`, `opencode`, `hermes-agent` skills.

## Prerequisites

- **Install:** `npm install -g @anthropic-ai/claude-code`
- **Auth:** run `claude` once to log in (browser OAuth for Pro/Max, or set `ANTHROPIC_API_KEY`)
- **Console auth:** `claude auth login --console` for API key billing
- **SSO auth:** `claude auth login --sso` for Enterprise
- **Check status:** `claude auth status` (JSON) or `claude auth status --text` (human-readable)
- **Health check:** `claude doctor` — checks auto-updater and installation health
- **Version check:** `claude --version` (requires v2.x+)
- **Update:** `claude update` or `claude upgrade`

## Quick Start

### Print Mode (Non-Interactive — PREFERRED)

```python
terminal(command="claude -p 'Add error handling to all API calls in src/' --allowedTools 'Read,Edit' --max-turns 10", workdir="/path/to/project", timeout=120)
```

Print mode runs a one-shot task, returns the result, and exits. No PTY, no dialogs, structured output. **Use this for 80% of delegated work.**

### Interactive PTY Mode (Multi-Turn)

```python
# Start a tmux session
terminal(command="tmux new-session -d -s claude-work -x 140 -y 40")

# Launch Claude Code
terminal(command="tmux send-keys -t claude-work 'cd /path/to/project && claude' Enter")

# Wait for startup, then send your task (~3-5s)
terminal(command="sleep 5 && tmux send-keys -t claude-work 'Refactor the auth module to use JWT tokens' Enter")

# Monitor progress
terminal(command="sleep 15 && tmux capture-pane -t claude-work -p -S -50")

# Exit when done
terminal(command="tmux send-keys -t claude-work '/exit' Enter")
```

Interactive mode requires **tmux orchestration** — it gives you `capture-pane` for monitoring and `send-keys` for input. `terminal(pty=true)` works but tmux is preferred.

## Choosing the Right Mode

| Scenario | Mode | Why |
|----------|------|-----|
| Fix a bug, add a feature, refactor | Print (`-p`) | No dialogs, structured JSON output, scriptable |
| CI/CD automation, batch tasks | Print (`-p`) | Non-interactive, no TTY needed |
| Structured data extraction | Print (`-p`) | Use `--json-schema` for typed output |
| Piped input analysis | Print (`-p`) | `cat file \| claude -p "..."` |
| Multi-turn review/fix cycle | Interactive (tmux) | Follow-up prompts, slash commands |
| Human-in-the-loop decisions | Interactive (tmux) | Need conversational flow |
| Using `/compact`, `/review`, `/model` | Interactive (tmux) | Slash commands only work here |
| Parallel multi-task work | Interactive (tmux) | One tmux session per instance |

## Feature Overview

### Print Mode (`-p`)

- **Structured JSON output** with `--output-format json` — includes `session_id`, `num_turns`, `total_cost_usd`, `subtype`
- **Streaming JSON** with `--output-format stream-json --verbose` for real-time token streaming
- **Bidirectional streaming** with `--input-format stream-json --replay-user-messages`
- **JSON Schema** extraction with `--json-schema '{...}'` — Claude validates before returning
- **Session continuation** with `--resume <id>` or `--continue` (same directory)
- **Bare mode** with `--bare` for CI (skips hooks, plugins, MCP, CLAUDE.md, OAuth)
- **Fallback model** with `--fallback-model haiku` for graceful overload handling
- **Cost caps** with `--max-budget-usd` and `--max-turns` (print mode only)

→ **Details, code examples, JSON schemas:** [references/print-mode.md](references/print-mode.md)

### Interactive PTY Mode

- **Tmux orchestration** for reliable multi-turn control
- **Slash commands**: `/compact`, `/review`, `/security-review`, `/plan`, `/model`, `/effort`, `/clear`, `/cost`, `/context`, `/resume`, `/rewind`, `/voice`, and more
- **Custom slash commands** in `.claude/commands/*.md` (project) or `~/.claude/commands/*.md` (user)
- **Skills** (auto-invoked natural language guides) in `.claude/skills/`
- **Keyboard shortcuts**: `Shift+Tab` (permission modes), `Alt+P` (model), `Ctrl+O` (transcript), `Esc Esc` (rewind)
- **"ultrathink" keyword** for maximum reasoning on a single turn
- **Context monitoring** with `/context` (70% threshold for `/compact`)

→ **Dialog handling, slash commands, shortcuts:** [references/interactive-pty.md](references/interactive-pty.md)

### Configuration & Extensibility

- **Settings hierarchy**: CLI flags → `.claude/settings.local.json` → `.claude/settings.json` → `~/.claude/settings.json`
- **CLAUDE.md memory** for project context (global, project, local)
- **Custom subagents** in `.claude/agents/` (project) or `~/.claude/agents/` (user)
- **Hooks** for automation on 8 events (PreToolUse, PostToolUse, Stop, etc.)
- **MCP integration** for external tools (GitHub, Postgres, Puppeteer, etc.)
- **Worktree isolation** with `-w <name> --tmux` for safe parallel work
- **PR review** with `--from-pr <number>` or piped `git diff`

→ **Settings, hooks, MCP, agents:** [references/configuration.md](references/configuration.md)

### CLI Flags (Quick Reference)

| Category | Key Flags |
|----------|-----------|
| **Session** | `-p`, `-c`, `-r`, `--fork-session`, `--session-id`, `--add-dir`, `-w`, `--tmux`, `--from-pr` |
| **Model** | `--model`, `--effort`, `--max-turns`, `--max-budget-usd`, `--fallback-model` |
| **Permissions** | `--dangerously-skip-permissions`, `--permission-mode`, `--allowedTools`, `--disallowedTools` |
| **Output** | `--output-format`, `--json-schema`, `--verbose`, `--include-partial-messages` |
| **Context** | `--append-system-prompt`, `--bare`, `--agents`, `--mcp-config`, `--strict-mcp-config` |
| **Debug** | `-d [filter]`, `--debug-file` |

→ **Complete flag reference:** [references/cli-flags.md](references/cli-flags.md)

## PR Review & Parallel Workflows

### Quick PR Review

```python
terminal(command="cd /path/to/repo && git diff main...feature-branch | claude -p 'Review this diff for bugs, security issues, and style problems.' --max-turns 1", timeout=60)
```

### Deep Review (Worktree + Interactive)

```python
terminal(command="tmux new-session -d -s review -x 140 -y 40")
terminal(command="tmux send-keys -t review 'cd /path/to/repo && claude -w pr-review' Enter")
terminal(command="sleep 5 && tmux send-keys -t review Enter")  # Trust dialog
terminal(command="tmux send-keys -t review 'Review all changes vs main. Check for bugs, security, race conditions, missing tests.' Enter")
```

### Parallel Instances

```python
terminal(command="tmux new-session -d -s task1 && tmux send-keys -t task1 'cd ~/project && claude -p \"Fix auth bug\" --allowedTools \"Read,Edit\" --max-turns 10' Enter")
terminal(command="tmux new-session -d -s task2 && tmux send-keys -t task2 'cd ~/project && claude -p \"Write API tests\" --allowedTools \"Read,Write,Bash\" --max-turns 15' Enter")
terminal(command="sleep 30 && for s in task1 task2; do echo \"=== $s ===\"; tmux capture-pane -t $s -p -S -5; done")
```

→ **Full PR review patterns, worktree, parallel workflows:** [references/pr-workflow.md](references/pr-workflow.md)

## Monitoring Sessions

```python
# Check if Claude is working or waiting
terminal(command="tmux capture-pane -t dev -p -S -10")
```

**TUI status indicators:**
- `❯` at bottom = waiting for input (done or asking a question)
- `●` lines = actively using tools
- `⏵⏵ bypass permissions on` = permissions mode in status bar
- `ctrl+o to expand` = tool output was truncated

**Context health:** Use `/context` in interactive mode. `< 70%` is normal, `70-85%` consider `/compact`, `> 85%` hallucination risk spikes.

## CLI Subcommands

| Subcommand | Purpose |
|------------|---------|
| `claude` | Start interactive REPL |
| `claude "query"` | Start REPL with initial prompt |
| `claude -p "query"` | Print mode (non-interactive, exits when done) |
| `claude -c` | Continue the most recent conversation in this directory |
| `claude -r "id"` | Resume a specific session by ID or name |
| `claude auth login` | Sign in (add `--console` for API billing, `--sso` for Enterprise) |
| `claude auth status` | Check login status (returns JSON; `--text` for human-readable) |
| `claude mcp add <name> -- <cmd>` | Add an MCP server |
| `claude mcp list` | List configured MCP servers |
| `claude mcp remove <name>` | Remove an MCP server |
| `claude agents` | List configured agents |
| `claude doctor` | Run health checks on installation and auto-updater |
| `claude update` / `claude upgrade` | Update Claude Code to latest version |
| `claude remote-control` | Start server to control Claude from claude.ai or mobile app |
| `claude setup-token` | Set up long-lived auth token (requires subscription) |
| `claude plugin` / `claude plugins` | Manage Claude Code plugins |
| `claude auto-mode` | Inspect auto mode classifier configuration |

## Common Pitfalls

1. **Interactive mode REQUIRES tmux** — Claude Code is a full TUI; tmux gives you capture/send-keys.
2. **`--dangerously-skip-permissions` dialog defaults to "No, exit"** — send `Down` then `Enter`. Print mode skips this.
3. **`--max-turns` is print-mode only** — ignored in interactive sessions.
4. **`--max-budget-usd` minimum is ~$0.05** — system prompt cache creation costs this much.
5. **Trust dialog only appears once per directory** — first-time only, then cached.
6. **Session resumption requires same directory** — `--continue` finds the most recent for the current working directory.
7. **`--json-schema` needs enough `--max-turns`** — Claude must read files before producing structured output.
8. **Background tmux sessions persist** — always `tmux kill-session -t <name>` when done.
9. **Slash commands only work in interactive mode** — in `-p` mode, describe the task in natural language.
10. **Context degradation is real** — quality drops above 70% usage; monitor with `/context` and `/compact`.

→ **Full troubleshooting, cost tips, common errors table:** [references/troubleshooting.md](references/troubleshooting.md)

## Quick Rules for Hermes Agents

1. **Prefer print mode (`-p`) for single tasks** — cleaner, no dialog handling, structured output
2. **Use tmux for multi-turn interactive work** — the only reliable TUI orchestration
3. **Always set `workdir`** — keep Claude focused on the right project directory
4. **Set `--max-turns` in print mode** — prevents infinite loops and runaway costs
5. **Monitor tmux sessions** — `tmux capture-pane -t <session> -p -S -50`
6. **Look for the `❯` prompt** — indicates Claude is waiting for input
7. **Clean up tmux sessions** — `tmux kill-session -t <name>` to avoid resource leaks
8. **Report results to user** — summarize what Claude did and what changed
9. **Don't kill slow sessions** — Claude may be doing multi-step work; check progress first
10. **Use `--allowedTools`** — restrict capabilities to what the task actually needs

## References

- **[print-mode.md](references/print-mode.md)** — JSON output, streaming, JSON schema, session continuation, bare mode
- **[interactive-pty.md](references/interactive-pty.md)** — tmux orchestration, dialog handling, slash commands, keyboard shortcuts
- **[configuration.md](references/configuration.md)** — settings, CLAUDE.md, subagents, hooks, MCP, env vars
- **[cli-flags.md](references/cli-flags.md)** — complete flag reference (all categories)
- **[pr-workflow.md](references/pr-workflow.md)** — PR review patterns, worktrees, parallel instances
- **[troubleshooting.md](references/troubleshooting.md)** — pitfalls, cost tips, common errors, full agent rules
