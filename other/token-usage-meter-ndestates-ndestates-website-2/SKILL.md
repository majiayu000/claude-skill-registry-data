---
name: token-usage-meter
description: >
  Always-on xAI/Grok token usage and prompt-cache monitor. Syncs session context
  from Grok updates.jsonl, logs trends to reports/tokens/, warns on context bloat
  and cache misses. Surface a one-line Token meter footer on every substantive
  response when monitoring is enabled. Use on /token-usage-meter, session-start,
  eod-shutdown, or when user asks about token cost.
user-invocable: true
disable-model-invocation: false
---

# Token Usage Meter

## Overview

Monitors **two layers** of token cost:

1. **Session context** (Grok Build) — `totalTokens` in `~/.grok/sessions/.../updates.jsonl` per turn. Tracks context growth and per-turn deltas.
2. **API prompt cache** (xAI API) — `cached_tokens` in API `usage` objects. Tracks cache hit rate and miss warnings.

Always-on mode is **mandatory** when `token_policy.report_tokens_estimate: true` in the project manifest (default for this template).

## Always-On Rules (agents)

Apply on **every substantive response** unless the user says "no token meter" or "skip meter":

1. **Sync** (once per turn, before final reply):
   ```bash
   python3 .github/skills/token-usage-meter/scripts/token_monitor.py --sync --project .
   ```
2. **Footer** — end the response with the script's one-line output, prefixed exactly:
   ```
   Token meter: ctx 170,755 · +6,729 this turn · 17 turns · ~$2.45 session · ~$0.12 turn · CRITICAL
   ```
   (`~` = estimated from `references/pricing.json`). Or run `--footer` if sync already ran this turn.
3. **Warnings** — if sync prints WARNINGS, surface them prominently above the footer (context ≥100k, turn delta ≥15k, or cache miss).
4. **Session start** — run `--sync` during `.github/skills/chain/SKILL.md session-start` after cache load; include meter in standup briefing.
5. **EOD** — run `--sync` then `--report` during `.github/skills/chain/SKILL.md eod-shutdown`; append summary to chain report under `reports/tokens/`.
6. **API usage** — when user pastes `usage` JSON, run `analyze_token_usage.py` and merge cache status into the footer.

Skip the footer only for: trivial acks ("ok", "done"), pure code citations with no prose, or explicit user opt-out.

## When to Activate

- User invokes `/token-usage-meter` or asks about token usage, cost, or cache.
- Session-start, eod-shutdown, or any chain with `token_monitor: true`.
- Context feels heavy, responses slow, or conversation was summarized.
- User pastes API `usage` with `cached_tokens`.

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/token_monitor.py` | Sync Grok session → `reports/tokens/session-log.jsonl` + `latest-summary.json` |
| `scripts/analyze_token_usage.py` | Analyze xAI API `usage` JSON (cache hit rate) |
| `scripts/token_lib.py` | Shared parsing (do not run directly) |

### token_monitor.py

```bash
# Sync latest session for this repo (default)
python3 .github/skills/token-usage-meter/scripts/token_monitor.py --sync --project .

# One-line footer from last sync
python3 .github/skills/token-usage-meter/scripts/token_monitor.py --footer

# Trend report from log (includes est. session cost)
python3 .github/skills/token-usage-meter/scripts/token_monitor.py --report

# Cost breakdown from latest sync
python3 .github/skills/token-usage-meter/scripts/token_monitor.py --cost

# One-off analyze a session file
python3 .github/skills/token-usage-meter/scripts/token_monitor.py --analyze ~/.grok/sessions/.../updates.jsonl
```

**Persistent artifacts** (project-local, gitignored state optional):

| Path | Content |
|------|---------|
| `reports/tokens/session-log.jsonl` | Append-only per-turn records |
| `reports/tokens/latest-summary.json` | Latest session snapshot for agents |
| `reports/tokens/.sync-state.json` | Incremental sync cursor |

### analyze_token_usage.py

```bash
python3 .github/skills/token-usage-meter/scripts/analyze_token_usage.py usage.json
cat response.json | python3 .github/skills/token-usage-meter/scripts/analyze_token_usage.py
```

## Cost analysis

**Pricing source:** `references/pricing.json` (USD per 1M tokens). Official xAI rates for `grok-build-0.1`; estimated rates for `grok-composer-2.5-fast` (Grok Build IDE default).

| Model | Input / 1M | Cached input / 1M | Output / 1M |
|-------|------------|---------------------|-------------|
| grok-build-0.1 | $1.00 | $0.20 | $2.00 |
| grok-composer-2.5-fast | $3.00 (est.) | $0.75 (est.) | $15.00 (est.) |

### Session mode (Grok Build logs)

Estimates per turn:
- **Input** = full context re-sent each turn (with assumed 75% cache hit on prior context after turn 1)
- **Output** ≈ 30% of `turn_delta` (agent reply; minimum 200 tokens)

Sync prints `SESSION COST ANALYSIS` with session total, last-turn cost, avg/turn, and cache savings vs no-cache.

### API mode (precise)

When `usage` JSON is available, `analyze_token_usage.py` bills:
- uncached input × input rate
- cached input × cached rate
- output × output rate

Paste API responses for exact per-call cost; session mode is for always-on monitoring without manual paste.

## Thresholds

### Session context (Grok)

| Condition | Status | Action |
|-----------|--------|--------|
| context ≥ 128,000 | CRITICAL | Summarize thread; offer fresh session |
| context ≥ 100,000 | WARNING | Cache-first only; lean replies |
| turn delta ≥ 15,000 | WARNING | Review large file reads / verbose output |

### API cache (xAI)

| Condition | Status |
|-----------|--------|
| `cached_tokens = 0` and `prompt_tokens > 50` | POOR — cache miss |
| hit rate < 30% on large prompts | FAIR |
| hit rate ≥ 80% | EXCELLENT |

See `references/xai-prompt-caching.md` for cache mechanics.

## Core Analysis Logic (API usage)

1. Parse `usage` (`prompt_tokens_details.cached_tokens` or `input_tokens_details.cached_tokens`).
2. Compute cache hit rate = (cached_tokens / prompt_tokens) × 100.
3. Apply thresholds above; output structured report with recommendations.
4. Never claim cache is working if `cached_tokens = 0` on substantial prompts.

## Worker / Automation

- **Session-start chain** — sync + brief meter in standup.
- **EOD chain** — sync + report + optional daily markdown in `reports/tokens/`.
- **tasks skill** — schedule hourly/daily: "Run token_monitor.py --sync and --report".
- **CI/logging** — pipe API `usage` JSON to `analyze_token_usage.py`; alert on POOR status.

## Reference

`references/xai-prompt-caching.md` — full xAI caching mechanics, headers, billing.