---
name: scalpel
description: >
  Surgical AI for your codebase. Plugs into any project, performs a 12-dimension
  diagnostic scan (git forensics, architecture, tech debt, security, infrastructure),
  delivers a Codebase Vitals health score, then assembles and manages an adaptive
  AI surgical team calibrated to YOUR project. Pendrive architecture — plug in, work,
  unplug, zero trace. Also ships a standalone bash scanner (zero AI, zero tokens)
  for instant codebase health checks.
version: 2.0.0
license: MIT
author: anupmaster
homepage: https://github.com/anupmaster/scalpel
triggers:
  - scalpel
  - scalpel scan
  - Hi Scalpel
  - codebase health
  - code audit
  - project diagnostic
tools:
  - Read
  - Write
  - Edit
  - MultiEdit
  - Glob
  - Grep
  - Bash
  - WebSearch
  - WebFetch
  - Task
  - Teammate
  - EnterWorktree
  - ExitWorktree
platforms:
  - claude-code
  - codex
  - gemini-cli
  - cursor
  - windsurf
  - aider
  - opencode
---

# Scalpel — Surgical AI for Your Codebase

12-dimension diagnostic. Adaptive surgical teams. Zero side effects.

## Installation

```bash
# Claude Code
git clone https://github.com/anupmaster/scalpel.git ~/.claude/skills/scalpel

# Codex CLI
git clone https://github.com/anupmaster/scalpel.git ~/.agents/skills/scalpel

# Any project (pendrive style)
cd your-project && git clone https://github.com/anupmaster/scalpel.git .scalpel && .scalpel/install.sh
```

## Usage

```
> Hi Scalpel, start work
> scalpel scan              # Diagnostic only, no changes
> scalpel skip recon        # Jump to task execution
```

## Standalone Scanner (Zero AI)

```bash
./src/scanner.sh                # Pretty terminal output
./src/scanner.sh --json         # Machine-readable
./src/scanner.sh --score-only   # Just the number: "83"
```

## What It Does

1. **Diagnose** — Scans 12 dimensions: stack, architecture, git forensics, database, auth, infrastructure, tests, security, integrations, agent ecosystem, code quality, performance
2. **Consult** — Delivers Codebase Vitals health score, asks targeted questions
3. **Assemble** — Designs a custom surgical team calibrated to YOUR project
4. **Operate** — Spawns parallel agents in isolated worktrees with file jurisdiction
5. **Close** — Delivery report, session memory saved, optional regression monitoring

## Features

- **Standalone scanner** — Pure bash, zero AI, zero tokens. Runs anywhere.
- **12-dimension diagnostic** — Deeper than any linter. Reads git history, deleted files, abandoned branches.
- **Adaptive teams** — Not templates. Teams shaped by YOUR project's needs.
- **File jurisdiction** — Each agent owns specific files. Zero merge conflicts.
- **Agent scoring** — Quality enforcement. Score < 50 = agent terminated.
- **Session memory** — Remembers previous sessions. Gets smarter over time.
- **Pendrive architecture** — Plug in, work, unplug. Zero trace.
- **7 agent adapters** — Claude Code, Codex, Gemini, Cursor, Windsurf, Aider, OpenCode.
- **GitHub Action** — Automated PR health checks.
- **Extensible config** — Custom scan dimensions, team roles, scoring rules.

## Permissions

Read-only during diagnostic. Write access only during surgical team operation.
Never modifies your existing CLAUDE.md, agents, commands, or settings.
Never commits itself to your git history. Uninstall leaves zero trace.
