---
name: token-usage
description: Analyze Claude Code token consumption and estimated costs across projects and sessions. Use when user asks about token usage, costs, spending, billing, how much they've used, or wants to optimize their Claude Code usage patterns.
---

# Token Usage Analyzer

Analyze token consumption patterns and estimate costs from Claude Code session files (`~/.claude/projects/`).

## What It Does

- Parses all JSONL session files to extract token metrics (input, cache creation, cache read, output)
- Groups usage by project and session
- Estimates costs based on Claude model pricing
- Identifies most expensive sessions and subagent usage
- Supports time range filtering (today, week, month, N days, specific date)
- Generates a detailed markdown report

## Usage

Run the analyzer with a time range argument:

```bash
python3 .claude/skills/token-usage/scripts/analyze.py $ARGUMENTS
```

### Arguments

| Argument | Example | Description |
|----------|---------|-------------|
| *(empty)* | | All time |
| `today` | `today` | Since midnight UTC |
| `week` | `week` | Last 7 days |
| `month` | `month` | Last 30 days |
| N (number) | `3` | Last N days |
| Date | `2026-04-01` | Since that date |
| Datetime | `2026-04-01 11:00` | Since that datetime |

### Additional flags

- `--compare` — show current period vs previous period of same length

Example: `--compare week` shows this week vs last week.

### Output

The script prints a summary to stdout and saves a detailed report to:
```
~/.claude/token-usage-reports/token_report.md
```

## Cost Estimation

Prices are per million tokens, detected automatically per model:

| Model | Input | Cache Create | Cache Read | Output |
|-------|-------|-------------|------------|--------|
| Opus | $15.00 | $18.75 | $1.50 | $75.00 |
| Sonnet | $3.00 | $3.75 | $0.30 | $15.00 |
| Haiku | $0.80 | $1.00 | $0.08 | $4.00 |

The analyzer reads the `model` field from each assistant message and applies correct pricing automatically.

## What the Report Includes

1. **Grand totals** — tokens, estimated cost, session count
2. **Model breakdown** — cost split by opus/sonnet/haiku with percentages
3. **Per-project breakdown** — tokens, cost, subagent count per project
4. **Period comparison** — current vs previous period (with `--compare`)
5. **Most costly sessions** — ranked by estimated cost with first prompt preview

## Tips for Reducing Usage

- **Cache read is cheap** ($1.50/M vs $15/M for input) — long conversations benefit from cache
- **Subagents are expensive** — each spawns a fresh context. Use sparingly.
- **Review your costliest sessions** — often one runaway session costs more than a week of normal work
- **Use specific time ranges** to track daily/weekly spending patterns

## Requirements

- Python 3.8+
- Claude Code (session files in `~/.claude/projects/`)
- No external dependencies (stdlib only)
