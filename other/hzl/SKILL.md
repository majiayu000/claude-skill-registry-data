---
name: hzl
description: OpenClaw's persistent task database. Coordinate sub-agents, checkpoint progress, survive session boundaries.
homepage: https://github.com/tmchow/hzl
metadata:
  { "openclaw": { "emoji": "🧾", "homepage": "https://github.com/tmchow/hzl", "requires": { "bins": ["hzl"] }, "install": [ { "id": "brew", "kind": "brew", "package": "hzl", "bins": ["hzl"], "label": "Install HZL (Homebrew)" }, { "id": "node", "kind": "node", "package": "hzl-cli", "bins": ["hzl"], "label": "Install HZL (npm)" } ] } }
---

# HZL: Persistent task tracking for agents

HZL (https://github.com/tmchow/hzl) is a local-first task ledger (database-backed, optionally cloud-synced for backup) that an agent can use to:

- plan multi-step work into projects + tasks
- checkpoint progress (so work survives session boundaries)
- coordinate sub-agents or multiple coding tools with leases
- generate reliable status reports ("what's done vs what's left")

This skill teaches an agent how to use the `hzl` CLI.

## When to use HZL

Use HZL when the agent needs a durable source of truth for work state:

- Multi-step projects with real sequencing (dependencies) and handoffs
- Work that spans multiple sessions, days, or tools/agents
- Orchestration: delegating work to sub-agents and needing recovery if they crash
- Anything where "resume exactly where we left off" matters

Not ideal for:

- Time-based reminders/alerts (use a scheduler, for example OpenClaw Cron)
- Longform notes or knowledge capture (use a notes or memory system)
- Tiny one-step tasks you will complete immediately

Personal tasks: HZL is not a polished human to-do app, but it is usable for personal task tracking, and it can also serve as a backend for a lightweight UI.

## Core concepts

- **Project**: stable container for a body of work. Typically one per repo or long-running initiative. Do not create per-feature projects.
- **Task**: top-level work item (often a feature). Use `--depends-on` to sequence separate tasks.
- **Subtask**: breakdown of a task into parts (`--parent <id>`). Max 1 level of nesting. Parent tasks are organizational containers—never returned by `hzl task next`.
- **Checkpoint**: short progress snapshot to support recovery
- **Lease**: time-limited claim (prevents orphaned work in multi-agent flows)

## ⚠️ DESTRUCTIVE COMMANDS - READ CAREFULLY

The following commands **PERMANENTLY DELETE ALL HZL DATA** and cannot be undone:

| Command | Effect |
|---------|--------|
| `hzl init --force` | **DELETES ALL DATA.** Prompts for confirmation. |
| `hzl init --force --yes` | **DELETES ALL DATA WITHOUT CONFIRMATION.** Extremely dangerous. |

**NEVER use `--force` or `--force --yes` unless the user explicitly instructs you to destroy all task data.**

These commands delete the entire event history, all projects, all tasks, all checkpoints—everything. There is no recovery without a backup.

## Quick reference

```bash
# Setup
hzl init                                      # Initialize (safe, won't overwrite)
hzl init --reset-config                       # Reset config to default location (non-destructive)
hzl project create <project>
hzl project list

# Create tasks
hzl task add "<title>" -P <project>
hzl task add "<title>" -P <project> --priority 2 --tags backend,auth
hzl task add "<title>" -P <project> --depends-on <other-id>

# Subtasks (organize related work)
hzl task add "<title>" --parent <parent-id>   # Create subtask
hzl task list --parent <parent-id>            # List subtasks
hzl task list --root                          # Top-level tasks only
hzl task next --parent <parent-id>            # Next subtask of parent

# Find work
hzl task list --project <project> --available
hzl task next --project <project>

# Work + persist progress
hzl task claim <id> --author <agent-id>
hzl task checkpoint <id> "<what changed / what's next>"
hzl task show <id> --json
hzl task complete <id>

# Dependencies + validation
hzl task add-dep <task-id> <depends-on-id>
hzl validate

# Diagnostics
hzl status   # database mode, paths, sync state
hzl doctor   # health check for debugging

# Web Dashboard (human visibility into task state)
hzl serve                    # Start on port 3456 (network accessible)
hzl serve --host 127.0.0.1   # Restrict to localhost only
hzl serve --background       # Fork to background
hzl serve --stop             # Stop background server

# Multi-agent recovery
hzl task claim <id> --author <agent-id> --lease 30
hzl task stuck
hzl task steal <id> --if-expired --author <agent-id>
```

Tip: When a tool needs to parse output, prefer `--json`.

## Recommended patterns

### Start a multi-step project

1) Create (or reuse) a stable project name.  
2) Decompose into tasks.  
3) Use dependencies to encode sequencing, not just priority.  
4) Validate.

```bash
hzl project create myapp-auth

hzl task add "Clarify requirements + acceptance criteria" -P myapp-auth --priority 5
hzl task add "Design API + data model" -P myapp-auth --priority 4 --depends-on <reqs-id>
hzl task add "Implement endpoints" -P myapp-auth --priority 3 --depends-on <design-id>
hzl task add "Write tests" -P myapp-auth --priority 2 --depends-on <impl-id>
hzl task add "Docs + rollout plan" -P myapp-auth --priority 1 --depends-on <tests-id>

hzl validate
```

### Work a task with checkpoints

Checkpoint early and often. A checkpoint should be short and operational:
- what you verified
- what you changed
- what's next
- what's blocking you (if anything)

```bash
hzl task claim <id> --author orchestrator
# ...do work...
hzl task checkpoint <id> "Implemented login flow. Next: add token refresh. Blocker: need API key for staging."
hzl task complete <id>
```

### Coordinate sub-agents with leases

Use leases when delegating, so you can detect abandoned work and recover.

```bash
hzl task add "Implement REST endpoints" -P myapp-auth --priority 3 --json
hzl task claim <id> --author subagent-claude-code --lease 30
```

Delegate with explicit instructions:
- claim the task (with their author id)
- checkpoint progress as they go
- complete when done

Monitor:
```bash
hzl task show <id> --json
hzl task stuck
hzl task steal <id> --if-expired --author orchestrator
```

### Break down work with subtasks

Use parent/subtask hierarchy to organize complex work:

```bash
# Create parent task
hzl task add "Implement vacation booking" -P portland-trip --priority 2
# → abc123

# Create subtasks (project inherited automatically)
hzl task add "Research flights" --parent abc123
hzl task add "Book hotel" --parent abc123 --depends-on <flights-id>
hzl task add "Plan activities" --parent abc123

# View breakdown
hzl task show abc123

# Work through subtasks
hzl task next --parent abc123
```

**Important:** `hzl task next` only returns leaf tasks (tasks without children). Parent tasks are organizational containers—they are never returned as "next available work."

When all subtasks are done, manually complete the parent:
```bash
hzl task complete abc123
```

## Web Dashboard

HZL includes a built-in Kanban dashboard for monitoring task state:

```bash
hzl serve                    # Start on port 3456
hzl serve --background       # Fork to background
```

The dashboard shows tasks in columns (Backlog → Blocked → Ready → In Progress → Done), with filtering by date and project. Useful for human visibility into what agents are working on.

For always-on access (e.g., via Tailscale), run as a systemd service:

```bash
hzl serve --print-systemd > ~/.config/systemd/user/hzl-web.service
systemctl --user enable --now hzl-web
```

## OpenClaw-specific notes

- Run `hzl ...` via the Exec tool.
- OpenClaw skill gating checks `requires.bins` on the host at skill load time. If sandboxing is enabled, the binary must also exist inside the sandbox container too. Install it via `agents.defaults.sandbox.docker.setupCommand` (or use a custom image).
- If multiple agents share the same HZL database, use distinct `--author` ids (for example: `orchestrator`, `subagent-claude`, `subagent-gemini`) and rely on leases to avoid collisions.
