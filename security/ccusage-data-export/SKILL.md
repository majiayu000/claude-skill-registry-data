---
name: ccusage-data-export
description: "Use when exporting ccusage usage data to JSON."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [ccusage, usage, export, cost, tokens, agents]
---

# ccusage data export

Produce a folder of JSON usage reports from the `ccusage` CLI (a unified tracker for
Claude, Codex, OpenCode, Hermes, Amp, Copilot, Antigravity, pi, and others) for a
report or audit.

## When to use

- Someone asks for a full ccusage data export, usage report, or cost/token totals.
- Need per-agent (Claude vs Codex vs Hermes vs OpenCode …) totals from ccusage.
- Need machine-readable (JSON) daily/monthly/session breakdowns.

## Prerequisites

- `npx` available; ccusage runs via `npx -y ccusage@latest` (no install needed).
- Output folder (default `~/ccusage-export`).

## Procedure

1. Create the output folder: `mkdir -p ~/ccusage-export`.
2. Learn flags: `npx -y ccusage@latest --help` plus `daily --help`, `monthly --help`,
   `session --help`. Key flags: `-j/--json`, `-s/--since`, `-u/--until`, `-z/--timezone`,
   `--all`, `--by-agent`, `--sections`, `-O/--offline`, `--no-cost`, `--last`.
   There is NO `--breakdown` flag; per-model breakdowns are included by default as
   `modelBreakdowns` in each JSON row.
3. Generate reports in ONE quick batch (ccusage reads live data; totals drift between
   runs, so keep them consistent):
   - `npx -y ccusage@latest daily --json --by-agent > /tmp/daily_byagent.json`
   - `npx -y ccusage@latest monthly --json > ~/ccusage-export/monthly.json`
   - `npx -y ccusage@latest session --json > ~/ccusage-export/session.json`
4. Derive `daily.json` from the `--by-agent` snapshot by dropping the per-row `agents`
   sub-array (keeps the standard daily report on the same snapshot):
   ```python
   import json, copy
   d = copy.deepcopy(json.load(open('/tmp/daily_byagent.json')))
   for row in d['daily']: row.pop('agents', None)
   json.dump(d, open('~/ccusage-export/daily.json','w'), indent=2)
   ```
5. Per-agent split (`agents.json`): aggregate the `--by-agent` daily rows — each row's
   `agents` array has one entry per agent present that day with `totalCost`, `totalTokens`,
   `inputTokens`, `outputTokens`, `cacheCreationTokens`, `cacheReadTokens`, `modelsUsed`.
   Sum across dates per agent; collect date range from row `period` values. Add session
   counts from `session.json` (each session row has an `agent` field). Write `agents.json`
   with `grandTotals` taken from the daily snapshot so it matches `daily.json` exactly.
6. Verify all four files share identical grand totals (cost + tokens); fix if not.
7. Report back ONLY: exact file paths, each file's size in bytes, grand totals from the
   daily report (total cost, total tokens, date range), and how the per-agent split was
   obtained. Do NOT paste JSON contents.

## How the per-agent split is obtained

- ccusage supports grouping by agent via the `--by-agent` flag on unified reports, and
  also exposes per-agent subcommands (`ccusage <agent> daily|monthly|session|...` for
  claude, codex, opencode, hermes, amp, copilot, antigravity, pi, and others).
- Preferred: `--by-agent` aggregation (one run, consistent snapshot) plus session counts
  from `session.json`.
- Cross-check: run a couple of per-agent subcommands (`ccusage claude daily --json`,
  `ccusage codex daily --json`) and confirm totals match the aggregated values.
- If neither `--by-agent` nor per-agent subcommands existed, say so plainly — do not
  fabricate a split.

## Pitfalls

- **No `--breakdown` flag exists** (despite the name being plausible). Per-model data is
  already in `modelBreakdowns` by default; do not hunt for a flag.
- **Per-agent schemas differ.** The unified report uses `totalCost`/`period`; the codex
  subcommand uses `costUSD`/`date` (and adds `reasoningOutputTokens`). Normalize on the
  unified schema when aggregating; do not assume field names transfer.
- **Live-data drift.** ccusage reads live logs; totals change between runs. Generate all
  files in one quick batch and derive `daily.json` + `agents.json` from the same
  `--by-agent` snapshot so grand totals agree across files.
- **`--by-agent` row shape.** Unified rows have `agent: "all"` plus an `agents` array;
  each agent entry mirrors the row's token/cost fields. A single day can contain multiple
  agents — handle each entry separately, do not assume one agent per day.
- **Session count.** Comes from `session.json` (count rows where `agent == X`), not from
  the daily report. The unified session report is grouped by session id, one row per session.
- **Unpriced models.** `totals.unpricedModels` lists models with no rate; their cost is
  excluded from `totalCost`. Report cost as reported; do not estimate.
- **npx noise.** Install/progress messages go to stderr; redirect stdout to the file and
  stderr to a temp file so JSON stays clean.
- **Detected agents vary by machine.** Only agents with local data appear; do not hardcode
  the list — read it from `metadata.agents` / row `agents` entries.
- **Report-back discipline.** Return only paths, byte sizes, grand totals, and method.
  Do not paste JSON contents into the reply.
