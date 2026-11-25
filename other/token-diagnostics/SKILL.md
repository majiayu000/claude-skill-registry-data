---
name: token-diagnostics
description: Diagnose where an AI coding agent's tokens go over the last 7 days and produce a standard summary with ranked optimisation findings. Finds the Claude Code, pi, or opencode session logs on its own. Supports redacted per-developer export and a fleet merge for team-wide analysis across many developers. Use when asked to "analyse my token usage", "why is my Claude Code bill so high", "run token diagnostics", "where are we spending tokens", "team token report", or invokes /token-diagnostics.
---

# Token Diagnostics

Answer one question: **which habits are burning tokens, and what is the fix worth?**

Output is always the same standard summary — 10 fixed sections — so 50 developers' reports compare directly.

## Quick start

```bash
S=".pi/skills/token-diagnostics/analyze_tokens.py"

python3 $S                      # standard summary, current harness, last 7 days
python3 $S where                # show every harness log dir found
python3 $S export --dev alice -o alice.json   # redacted JSON for a team lead
python3 $S merge ./exports/     # fleet summary across all exported devs
```

No arguments needed. No dependencies. Python 3.11+, stdlib only.

## How it finds the logs

Auto-discovery, in this order:

1. Environment overrides: `CLAUDE_CONFIG_DIR`, `PI_CONFIG_DIR`, `OPENCODE_DATA_DIR` (comma-separated lists supported).
2. Standard locations:

   | Harness | Location | Format |
   |---|---|---|
   | Claude Code | `~/.claude/projects/<slug>/<session>.jsonl` | JSONL |
   | pi | `~/.pi/agent/sessions/<slug>/<ts>_<id>.jsonl` | JSONL |
   | opencode | `~/.local/share/opencode/opencode.db`, or legacy `storage/message/` | SQLite / JSON |

3. If several harnesses are present, it picks the one this shell runs under (`CLAUDECODE`, `PI_AGENT`, `OPENCODE` env markers), else the most recently active.

Override with `--harness claude|pi|opencode`, or pass an explicit path as the last argument.

## Window

**Last 7 days, always.** Recent habits are the ones worth coaching, and a fixed window makes developer comparison fair. `--days N` exists for backfill, but the team report assumes 7.

## Running it

### One developer

```bash
python3 .pi/skills/token-diagnostics/analyze_tokens.py -o token-report.md
```

Read the output back to the user as-is. Do not summarise it further — it is already the summary. Then add at most three sentences naming the single highest-leverage change.

### A team of 50

1. Each developer runs the export and sends one JSON file:

   ```bash
   python3 analyze_tokens.py export --dev "$USER" -o "$USER.json"
   ```

   The export is redacted: no prompts, no source code, no file contents, no commands. Project names become `project-00`, paths become `*.py`, bash commands become the verb only. Only counts, token totals, tool names, and sizes survive.

2. The lead collects them into one directory and merges:

   ```bash
   python3 analyze_tokens.py merge ./exports/ -o fleet-report.md
   ```

The fleet summary gives spend distribution (mean/p50/p90/max, spread, top-10% share), a grade mix, fleet-wide issues ranked by recoverable spend, a per-developer table, and a coaching shortlist.

## What the standard summary contains

| Section | Question it answers |
|---|---|
| Header | Who, which harness, which log dir, which window |
| 1. Scorecard | Every key metric against a healthy target, plus an A–E efficiency grade |
| 2. Volume | Sessions, turns, and each token class |
| 3. Spend by model | Is a premium tier doing routine work? |
| 4. Context filled by tool | Which tool dumps the most into the window |
| 5. Spend by project | Which repo costs the most |
| 6. Most expensive sessions | Which specific sessions ran away |
| 7. Biggest single tool results | The individual dumps to stop making |
| 8. Redundant re-reads | Content paid for twice |
| 9. Findings | Ranked list: title, recoverable dollars, why, fix |
| 10. Bottom line | Grade, monthly extrapolation, one action |

**Efficiency grade** = share of spend *not* flagged as recoverable. A ≥85%, B ≥70%, C ≥55%, D ≥40%, E below. Developers with under $1 of activity are never graded down.

## The diagnostics, and why each matters

Cost is not "tokens used". Cost is **context size × turns**, because every turn re-sends the whole conversation. Every check below targets one driver of that product.

| Check | Signal | Healthy |
|---|---|---|
| Cache hit rate | Cache reads cost 5–60x less than fresh input. Misses come from editing instruction files mid-session, switching model mid-session, or tool output landing above the cache breakpoint. | >85% |
| Startup context | System prompt + instruction files + MCP tool schemas + skill descriptions, resident from turn one and paid every session. | <25k tokens |
| Session peak context | Cost per turn scales with it, and quality degrades once the window fills with stale output. | p90 <120k |
| Tool output share | Tool results enter context verbatim and are re-sent for the rest of the session. One 5k-line dump is paid dozens of times. | no tool >35% |
| Session hygiene | `/clear` and `/compact` are the only things that reset accumulated context. | long sessions get one |
| Model tiering | Realised cost per turn per model, compared within the window. No hardcoded model names. | premium <50% of spend |
| Subagent share | Each subagent pays its own full startup overhead. | <35% of spend |
| Tool failure rate | Every failure costs the call, the error text, and the retry turn. | <10% |
| Redundant re-reads | Same file read 3+ times in one session; it was already in context. | rare |
| Cost per file change | High ratio means spend went to exploration, not to change. | <$2.00 |

## Interpreting results

- **High cost, grade A** — an expensive but efficient developer. Leave them alone.
- **Low cost, grade E** — cheap but wasteful habits. Coach before their volume grows.
- **Spread (max/p50) above 5x** — investigate the top spenders' workflows before touching anyone else; the fleet total is theirs.
- **A fleet-wide issue affecting most developers** — fix it centrally (instruction files, MCP server list, default model, tool guidance), not per person.
- **`?` in the tool table** — tool calls whose result could not be paired; a small share is normal.

## Cost accuracy

pi and opencode record cost per turn; those are used verbatim. Claude Code records only tokens, so cost comes from a built-in price table matched on model-name substring. Override it:

```bash
python3 analyze_tokens.py --prices prices.json
# {"my-model": [input, output, cache_write, cache_read]}   USD per 1M tokens
```

Tool-output tokens are estimated at 4 bytes/token; image and PDF reads are clamped to a flat 1,600 tokens because they bill per tile, not per byte. Cross-check headline totals with `npx ccusage@latest`, which reads the same logs and reports cost only.

## Rules

- Never paste raw session content into a report. Use `export` for anything leaving a developer's machine.
- Report on habits, not people. The fleet table exists to find shared fixes, not to rank individuals.
- Never invent numbers. Every figure in the summary comes from the script.
