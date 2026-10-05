---
name: session-miser
description: >
  Intelligent model routing for Claude Code sessions. Recommends optimal model
  (Opus/Sonnet/Haiku) and effort level based on task complexity. Delegates
  mechanical work to cheaper subagents. Maximizes quality-per-dollar across
  the entire session. Trigger on: any new session, "save tokens", "cheaper model",
  "delegate this", "use sonnet", "effort level", "cost", or automatically when
  task complexity is clearly below the current model's tier.
---

# Session-Miser — Intelligent Session Cost Optimization

## Core Principle
Use the cheapest model that can do the job well. Opus for thinking, Sonnet for doing, Haiku for fetching.

## Model Selection Matrix

| Task Type | Model | Effort | Why |
|---|---|---|---|
| Architecture, design, complex reasoning | Opus | high | Needs deep reasoning |
| Security audits, code review with judgment | Opus | medium | Quality-sensitive |
| Code generation (new features, complex logic) | Opus or Sonnet | medium | Sonnet handles most code well |
| Code generation (boilerplate, simple functions) | Sonnet | low | Templated, predictable |
| Text editing, formatting, refactoring | Sonnet | low | Mechanical transformation |
| Git operations (commit, push, branch, merge) | Sonnet | low | Deterministic commands |
| File search, grep, glob, reading files | Haiku (subagent) | — | Read-only, no reasoning |
| Config file edits (.yaml, .json, .toml) | Sonnet | low | Structural, not creative |
| Documentation writing | Sonnet | medium | Needs coherence, not deep reasoning |
| Debugging (root cause analysis) | Opus | high | Multi-step reasoning |
| Debugging (applying a known fix) | Sonnet | low | Just follow the plan |
| Research (web search, GitHub crawl) | Sonnet | medium | Synthesis, not deep reasoning |
| Planning (PRD, architecture) | Opus | high | Open-ended judgment |
| Running tests, checking status | Haiku (subagent) | — | Mechanical execution |

## Session Start Recommendation

At the start of every session, assess the likely work and recommend:

```
You're on Opus. Based on the project and recent activity:
- If primarily editing/committing/deploying → suggest /model sonnet
- If primarily debugging/designing/architecting → stay on Opus
- If mixing both → stay on Opus but DELEGATE mechanical tasks to subagents
```

## Delegation Rules

ALWAYS delegate these to subagents (automatic, don't ask):
- File exploration (Explore agent → haiku)
- Running bash commands for status checks → haiku
- Git status, diff, log → haiku
- Searching codebase → haiku

SUGGEST delegating these (mention to user):
- Bulk file edits across multiple repos → sonnet subagent
- Running test suites → haiku subagent
- Documentation generation → sonnet subagent
- Config file updates → sonnet subagent

NEVER delegate (must stay in main thread):
- Anything the user is actively discussing
- Decisions that need user confirmation
- Security-sensitive operations
- Complex multi-step reasoning chains

## Effort Level Guide

Claude Code supports effort levels: opus:low, opus:medium, opus:high (and sonnet:low/medium/high)

| Effort | Use For | Cost |
|---|---|---|
| high | First attempt at complex problems, architecture, security | 1x |
| medium | Most coding, debugging, research | ~0.7x |
| low | Simple edits, formatting, git ops, status checks | ~0.4x |

Recommend `/model opus:low` for simple tasks instead of switching to Sonnet entirely.
This preserves Opus quality for unexpected complexity while saving cost.

## Integration with Multi-Instance Coordination

When coordinating work across multiple nodes:
- Route GPU-intensive tasks to GPU hosts (create coordination task with requires: [gpu, ollama])
- Route mechanical fleet tasks to primary/CPU hosts (lower cost hosts)
- When creating coordination tasks, specify the model tier in the task description:
  "This is a sonnet-tier task: bulk edit config files across 5 repos"
- This helps the claiming instance pick the right model

## Cost Tracking

After significant work blocks, check session-snitch:
```bash
session-snitch stats       # session cost so far
session-snitch cost        # cost breakdown by model
```

If session cost is climbing fast, suggest:
1. Delegate more to subagents
2. Switch to /model sonnet for the current phase
3. Use /model opus:low instead of opus:high

## Anti-Patterns

DON'T:
- Use Opus to read a file and report its contents (that's a haiku job)
- Use Opus to run `git status` and parse the output (haiku)
- Use Opus to format JSON or YAML (sonnet:low)
- Stay on Opus when doing 30 minutes of file edits (switch to sonnet)

DO:
- Start on Opus for planning, switch to Sonnet for execution
- Delegate parallel searches to haiku subagents
- Come back to Opus for review/verification of Sonnet's work
- Use effort levels to fine-tune cost within a model tier
