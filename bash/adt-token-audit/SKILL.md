---
name: token-audit
description: Audit historical Claude Code token usage from JSONL session files — shows total spend, cache hit rates, top costly sessions, weekly trends, and where tokens are going. Run after heavy sessions or weekly to measure optimization impact.
triggers:
  - token audit
  - token usage report
  - how many tokens
  - cache hit rate
  - session cost
  - token spend
  - where are tokens going
  - how expensive was that session
---

# Token Audit

Analyse all Claude Code session files to show where tokens go, how well the cache is working, and which sessions are most expensive.

## Installation

```bash
# The audit script lives at ~/.claude/skills/token-audit/audit.py
# Requires Python 3.10+ (stdlib only)
```

## Usage

```bash
python3 ~/.claude/skills/token-audit/audit.py              # last 30 days
python3 ~/.claude/skills/token-audit/audit.py --days 7     # last 7 days
python3 ~/.claude/skills/token-audit/audit.py --today      # today only
python3 ~/.claude/skills/token-audit/audit.py --session ID # single session detail
python3 ~/.claude/skills/token-audit/audit.py --json       # machine-readable
```

## What It Reports

```
Token Audit — Last 30 days
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Sessions:         247   Turns:            18,420
  Input tokens:     13K   Cache write:      19.6M
  Output tokens:   3.8M   Cache read:     1042.0M

  Cache hit rate: 98.2%  ███████████████████░
  Net cost est:   $483.20  Cache saved:   $9059.18

  ✓ Cache hit rate healthy (≥ 60%).

  Top sessions by cost          turns    cost   hit%
  ─────────────────────────── ─────  ──────  ─────
  730d5a18  2026-05-03         1762  $104.00    98%
  ...
```

## Cache Hit Rate Targets

| Rate | Status | Action |
|------|--------|--------|
| < 40% | Cold starts dominating | Use `context-pack` before new tasks; avoid `/clear` mid-session |
| 40–60% | Improvable | Compact at task boundaries, not mid-task |
| ≥ 60% | Healthy | Continue current strategy |

## Cost Notes

- Prices use Anthropic 2025/2026 API rates per model (Haiku / Sonnet / Opus)
- Mixed-model sessions priced per-turn for accuracy
- Values are estimates — actual billing may differ by plan

## Session End Summary

Wire the companion hook for a per-session summary at shutdown:

```json
"SessionEnd": [{
  "matcher": "*",
  "hooks": [{ "type": "command", "command": "bash ~/.claude/hooks/session-token-stop.sh" }]
}]
```
