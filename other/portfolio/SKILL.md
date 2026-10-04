---
name: portfolio
description: "Manage investment portfolios. Use when adding positions, analyzing allocation, calculating returns, or generating rebalance advice."
version: "3.4.0"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
tags:
  - portfolio
  - investment
  - finance
  - stocks
  - allocation
  - rebalance
---

# Portfolio

Investment portfolio manager. Add and remove holdings, list positions, analyze allocation weights, generate rebalance suggestions against target weights, and calculate performance returns over configurable time periods. All data is stored locally in JSON files — no external API calls required.

## Commands

| Command | Description | Flags |
|---------|-------------|-------|
| `add <ticker> <qty> <price>` | Buy shares — adds to holdings and records a buy transaction | `--date YYYY-MM-DD` (defaults to today) |
| `remove <ticker>` | Sell shares — removes from holdings and records a sell transaction | `--quantity N` (partial sell; omit to sell all) |
| `list` | Display all current holdings in a formatted table | `--format table\|json\|csv` |
| `analyze` | Analyze portfolio allocation with value and weight percentages | `--by ticker\|sector` `--format table\|json` |
| `rebalance` | Generate buy/sell suggestions to reach target allocation weights | `--target TICKER:PCT,...` `--threshold PCT` (default 5) |
| `performance` | Calculate portfolio returns (invested, sold, current value, gain/loss) | `--period 1d\|1w\|1m\|3m\|1y\|all` `--format table\|json` |
| `help` | Show the built-in help message with all command examples | — |

## Data Storage

All data is stored locally in `~/.portfolio/`:

- **`holdings.json`** — Array of current positions, each with `ticker`, `quantity`, `avg_price`, and `date_added`
- **`transactions.json`** — Array of all buy/sell transactions with `type`, `ticker`, `quantity`, `price`, and `date`

Both files are auto-created as empty JSON arrays (`[]`) on first use. The `add` command automatically merges duplicate tickers by recalculating the weighted average price.

## Requirements

- **bash** (4.0+)
- **python3** (standard library only — `json`, `os`, `sys`, `datetime`)
- No external APIs, no pip packages, no network access needed

## When to Use

1. **Tracking purchases** — When you buy stocks, ETFs, or crypto and want to record ticker, quantity, and price with automatic cost-basis averaging
2. **Reviewing holdings** — When you need a quick snapshot of your current portfolio in table, JSON, or CSV format
3. **Allocation analysis** — When you want to see how your portfolio is weighted across assets, with percentage breakdowns and visual bars
4. **Rebalancing** — When you need buy/sell recommendations to reach target allocation weights (e.g., `AAPL:40,GOOG:30,BTC:30`), with configurable drift thresholds
5. **Performance tracking** — When you want to calculate total invested, total sold, current value, and gain/loss percentage over a specific time period (1 day to all-time)

## Examples

```bash
# Add 100 shares of AAPL at $150.50, purchased on Jan 15, 2024
bash scripts/script.sh add AAPL 100 150.50 --date 2024-01-15

# Add 0.5 BTC at $42,000 (today's date auto-applied)
bash scripts/script.sh add BTC 0.5 42000

# Sell 50 shares of AAPL (partial sell)
bash scripts/script.sh remove AAPL --quantity 50

# Remove entire GOOG position
bash scripts/script.sh remove GOOG

# List holdings as a formatted table
bash scripts/script.sh list

# List holdings as JSON for programmatic use
bash scripts/script.sh list --format json

# List holdings as CSV for spreadsheet import
bash scripts/script.sh list --format csv

# Analyze allocation by ticker with visual weight bars
bash scripts/script.sh analyze --format table

# Get allocation as JSON
bash scripts/script.sh analyze --format json

# Generate rebalance suggestions with custom targets and 3% threshold
bash scripts/script.sh rebalance --target AAPL:40,GOOG:30,BTC:30 --threshold 3

# Equal-weight rebalance (no --target defaults to equal weight across all holdings)
bash scripts/script.sh rebalance

# Check performance over the last month
bash scripts/script.sh performance --period 1m

# All-time performance as JSON
bash scripts/script.sh performance --period all --format json
```

## How It Works

The script uses embedded Python (standard library only) for JSON manipulation and calculations. Bash handles argument parsing and dispatches to the appropriate Python block. When you `add` a position that already exists, the script recalculates the weighted average price automatically. The `rebalance` command compares current allocation percentages against your targets and flags any drift exceeding the threshold, recommending dollar amounts to buy or sell. The `performance` command filters transactions by date range and computes total invested, total sold, current portfolio value, and the resulting gain/loss.

## Output

All commands print to stdout. Use `--format json` for machine-readable output where supported. Redirect with standard shell operators:

```bash
bash scripts/script.sh list --format csv > portfolio.csv
bash scripts/script.sh performance --format json | jq .
```

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
