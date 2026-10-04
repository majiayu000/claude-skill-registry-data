---
name: claude-code
description: "Delegate coding to Claude Code CLI (features, PRs)."
version: 2.3.0
author: Hermes Agent + Teknium
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Coding-Agent, Claude, Anthropic, Code-Review, Refactoring, PTY, Automation]
    related_skills: [codex, hermes-agent, opencode]
---

# Claude Code — Hermes Orchestration Guide

Delegate coding tasks to [Claude Code](https://code.claude.com/docs/en/cli-reference) (Anthropic's autonomous coding agent CLI) via the Hermes terminal.

## Prerequisites

- **Install:** `npm install -g @anthropic-ai/claude-code`
- **Auth:** run `claude` once to log in, or set `ANTHROPIC_API_KEY`
- **Check status:** `claude auth status --text`
- **Quick test before committing:** `claude -p "echo ok" --max-turns 1 --allowedTools Bash`

## When to Use (and When Not To)

| Use Claude Code | Don't Use (fall back to direct) |
|----------------|-------------------------------|
| Multi-step refactoring across files | Single file edit |
| Complex feature implementation | Quick fix / one-off change |
| Tasks requiring complex tool orchestration | Claude Code fails auth/network check |
| OpenSpec-driven feature development | API 403 / org restriction blocks CLI |

## Two Orchestration Modes

### Mode 1: Print Mode (`-p`) — Non-Interactive (PREFERRED)

```bash
claude -p 'Add error handling to all API calls in src/' --allowedTools 'Read,Edit' --max-turns 10
```

**Skips all interactive dialogs.** Ideal for automation.

### Mode 2: Interactive PTY via tmux — Multi-Turn

```bash
tmux new-session -d -s claude-work -x 140 -y 40
tmux send-keys -t claude-work 'cd /project && claude' Enter
# Handle trust dialog
sleep 5 && tmux send-keys -t claude-work Enter
# Send task
tmux send-keys -t claude-work 'Implement auth module' Enter
# Monitor
tmux capture-pane -t claude-work -p -S -50
```

## Auth Failure: API 403 on Pro/Org Accounts

**Symptom:** `claude auth status --text` shows logged in, but `claude -p "echo ok"` returns `"Failed to authenticate. API Error: 403 Request not allowed"`.

**Cause:** Organization-level restrictions on the Claude Pro plan may block CLI API calls even though OAuth is valid. This is NOT a local configuration issue.

**Detection:**
```bash
claude auth status --text     # Looks fine
claude doctor                 # Reports healthy
claude -p "echo ok" --max-turns 1 --allowedTools Bash
# Returns 403 → Claude Code is unavailable
```

**Fix:**
1. Try API key auth instead: `claude auth login --console` or set `ANTHROPIC_API_KEY`
2. If that also fails, **fall back to direct implementation** (see below)

## Fallback: Direct Implementation When Claude Code Is Unavailable

When Claude Code is unavailable but the task requires OpenSpec-driven development with quality gates:

### Workflow

1. **Read specs FIRST** — load OpenSpec or read spec files directly
2. **Create modules directly** — use `write_file()` per file
3. **Update umbrella files** — lib.rs, Cargo.toml
4. **Quality gates after each module** — `cargo fmt && cargo clippy -- -D warnings && cargo test`
5. **Atomic commits** — `git add -A && git commit -m "feat: ..."` with conventional messages
6. **Update CHANGELOG** — note test count per phase

### Key Differences

| Aspect | Claude Code | Fallback (Direct) |
|--------|------------|-------------------|
| File creation | Delegated | `write_file()` |
| Test writing | Included in task | Write alongside implementation |
| Iteration | Self-corrects | Manual patch per clippy error |
| Speed | Parallel | Sequential per-module |
| Quality gates | Runs at end | After each module |

## Quality Gates (Must Pass Before Commit)

```bash
cargo fmt && cargo clippy -- -D warnings && cargo test
```

## Conventions

- **Conventional commits:** `feat:`, `fix:`, `test:`, `docs:`, `refactor:`
- **Update CHANGELOG.md** with each commit
- **Test count in commit message** — e.g. "24 tests passing"
- **One feature per commit**

## Autonomous ML Research Loop

For autonomous ML experiment iteration (run → analyze → fix → re-run → scale → paper update), see `references/autonomous-ml-research-loop.md`.

Key steps:
1. Write experiment script + CLAUDE.md in experiment directory
2. Start Claude Code in tmux: `tmux new-session -d -s <name> && tmux send-keys ... claude --dangerously-skip-permissions`
3. Send initial prompt via load-buffer + paste-buffer (not heredoc — special chars break send-keys)
4. Monitor with `tmux capture-pane -t <session> -p -S -20`
5. After bugs found, send structured fix instructions (root cause → fix → expected outcome)
6. After results, update paper and git push

## Pitfalls & Gotchas

1. **Interactive mode REQUIRES tmux**
2. **`--dangerously-skip-permissions` defaults to "No, exit"** — must send Down then Enter
3. **`--max-turns` is print-mode only**
4. **`--json-schema` needs enough `--max-turns`** — Claude must read files first
5. **Trust dialog appears once per directory**
6. **Background tmux sessions persist** — always clean up
7. **Context degradation above 70%** — use `/compact`
8. **API 403 on Pro accounts** — `claude auth status` lies. Always quick-test before starting long sessions.
