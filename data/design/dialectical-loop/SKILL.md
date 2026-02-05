---
name: dialectical-loop
description: Run a bounded adversarial cooperation coding loop (Architect -> Player <-> Coach). Use when implementing features from REQUIREMENTS.md, generating SPECIFICATION.md plans, and iterating with strict review until approved.
version: 1.0.3
tags: [coding, multi-agent, code-review, automation, dialectical, python, llm, workflow, github-copilot]
author: chipfox
repository: https://github.com/chipfox/dialetic-agents
license: MIT
---

# Dialectical Loop

Run a **bounded, adversarial coding workflow** rather than single-turn “vibe coding”.

## Core idea

- **Architect** turns high-level intent (`REQUIREMENTS.md`) into an actionable contract (`SPECIFICATION.md`).
- **Player** implements the specification and runs verification commands.
- **Coach** adversarially evaluates compliance and blocks until it’s correct.

This keeps attention bounded, forces explicit plans, and adds a strict review gate.

## Inputs / outputs

- Input: `REQUIREMENTS.md` (recommended)
- Generated/optional input: `SPECIFICATION.md`
- Output: code edits + command outputs per turn

## Agent prompts (no manual install)

This skill ships its role prompts inside the skill folder:

- `agents/architect.md`
- `agents/player.md`
- `agents/coach.md`

The orchestrator loads these files automatically at runtime. You do not need to “install agents” separately or configure them in OpenSkills.

## Key Features

- **Bounded iteration**: `--max-turns` prevents runaway token usage
- **Fast-fail optimization**: Skip Coach if verification fails (save tokens)
- **Auto-context switching**: Full snapshot turn 1 → git-changed thereafter
- **Token-optimized**: `--lean-mode` activates all savings (fast-fail, coach-focus-recent, auto-fix)
- **Production observability**: JSON logs with token estimates, loop health metrics, inter-agent communication tracking

## Prerequisites

- Python 3.10+
- GitHub CLI authenticated (`gh auth login` or `GITHUB_TOKEN` set)
- GitHub Copilot CLI available as `copilot` command

## Essential Options

- `--max-turns N` — Bound the loop (required)
- `--lean-mode` — Activate all token optimizations (recommended)

- `--verbose` — Detailed debug output
- `--quiet` — Minimal output (final summary only)
- `--skip-architect` — Use existing SPECIFICATION.md
- `--architect-model`, `--player-model`, `--coach-model` — Override defaults

## Recommended Models (GitHub Copilot CLI)

**Tier 1 (Balanced):** `claude-sonnet-4.5` for all roles (~38 units/5 turns)
**Tier 2 (Budget):** `gemini-3-pro-preview` Architect, `claude-haiku-4.5` Player, `claude-sonnet-4.5` Coach (~26 units)
**Tier 3 (Premium):** `claude-opus-4.5` Architect/Coach, `claude-sonnet-4.5` Player (~79 units)

## Observability

Automatic JSON logs (`dialectical-loop-TIMESTAMP.json`) include:

- Per-turn events (agent, model, tokens, duration)
- Loop health metrics (zero-edit streaks, fast-fail spirals)
- Inter-agent communication tracking (feedback coverage, error persistence)
- Real-time warnings for stuck patterns

## Usage Examples

```bash

# Basic usage
python ~/.claude/skills/dialectical-loop/scripts/dialectical_loop.py --max-turns 10

# Token-optimized
python ~/.claude/skills/dialectical-loop/scripts/dialectical_loop.py --max-turns 10 --lean-mode

# With existing spec
python ~/.claude/skills/dialectical-loop/scripts/dialectical_loop.py --skip-architect --max-turns 5
```

## Complete Documentation

See [README.md](README.md) for:

- Installation instructions
- Complete options reference
- Model selection guide (3 tiers with cost analysis)
- Token-saving strategies
- Dynamic spec pruning
- Verification configuration
- Troubleshooting
- Cross-platform shell configuration
