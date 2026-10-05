---
name: budi-analytics
description: >
  budi token/cost analytics for Claude Code — dashboard access, CLI queries,
  cost analysis patterns, session tracking. Trigger on: "budi", "token cost",
  "how much did that cost", "session cost", "spending", "token analytics",
  "cost dashboard", "usage stats", or any question about Claude Code token
  consumption or spending patterns.
---

# budi Analytics

budi (WakaTime for Claude Code) tracks tokens, costs, and file activity per session.

## Quick Reference

```bash
# Dashboard (web UI)
open http://127.0.0.1:<analytics-port>/dashboard

# CLI stats
budi stats                    # summary for current repo
budi stats --all              # all repos
budi stats --json             # machine-readable
budi sessions                 # list sessions
budi cost                     # cost breakdown
budi doctor                   # health check
```

## Architecture

- Daemon: `budi-daemon` on 127.0.0.1:<analytics-port> (started automatically)
- DB: `~/.local/share/budi/repos/<repo-hash>/budi.db` (SQLite, mode 600)
- Hooks: 5 events in `~/.claude/settings.json` (SessionStart, UserPromptSubmit, PostToolUse, SubagentStart, Stop)
- Status line: live cost shown in Claude Code terminal

## What It Tracks

| Data | Source Hook | Stored? |
|---|---|---|
| Session start/end | SessionStart, Stop | Yes |
| Prompt text | UserPromptSubmit | Yes (privacy note: prompts in SQLite) |
| Token counts | UserPromptSubmit | Yes |
| Model used | UserPromptSubmit | Yes |
| Cost estimate | Computed from model + tokens | Yes |
| Files touched | PostToolUse (Read/Write/Edit/Glob) | Yes (paths only, not content) |
| Subagent spawns | SubagentStart | Yes |

## Coexistence with Our Hooks

budi hooks don't conflict with our custom hooks:
- Our `PreToolUse[Agent]` (token-miser) → different event + matcher
- Our `SubagentStop` (cost-tracker) → different event
- budi uses HTTP hooks to daemon, ours use command hooks

## Cost Model

budi uses Anthropic's published pricing. Same rates as token-miser:
- Haiku 4.5: $1/$5 per MTok (in/out)
- Sonnet 4.6: $3/$15 per MTok
- Opus 4.6: $5/$25 per MTok

## Troubleshooting

```bash
budi doctor                   # check hooks, daemon, config
systemctl --user status budi-daemon  # if daemon isn't running
budi-daemon &                 # start manually
```
