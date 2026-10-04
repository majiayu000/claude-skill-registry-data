---
name: company-analysis
description: >
  Use this skill to perform a deep analysis for a given company. It correlates market news, sentiment, earnings, and stock price performance (1d, 1w, 3m, YTD).
  It highlights bearish and bullish sections, provides analyst recommendations, and performs a simulation of buying 5, 10, or 25 shares to maximize profits
  after removing fees and taxes for both short-term and long-term holdings. This is not financial advice, it's a report and simulation.
---

# Company Analysis & Simulation Skill

Two bundled scripts produce the report. The Go tool fetches the data and runs the
simulations. The Python script assembles the Markdown. Run both and show the
output.

## Usage

```
/company-analysis <TICKER>
```

## Process

Run this one command. Replace `<TICKER>` with the symbol, such as `AAPL`.

```bash
"${CLAUDE_PLUGIN_ROOT}/tools/company-analysis/run.sh" <TICKER>
```

`run.sh` finds its own directory, so the command works from any working
directory. If `${CLAUDE_PLUGIN_ROOT}` is empty, you are in a checkout of the
repository instead of a plugin install. Use this path:

```bash
./tools/company-analysis/run.sh <TICKER>
```

The command prints the finished Markdown report. Show that output to the user.

`run.sh` runs the Go tool, which prints JSON, and pipes that JSON into
`generate_report.py`, which writes the report. It uses the Go toolchain when it
is present and the bundled binary when it is not. Neither step needs help from
you.

## Rules

**Do not write any part of the report yourself.**

- Do not read the JSON and compose your own Markdown.
- Do not add your own sentiment analysis. `generate_report.py` does this.
- Do not add your own analyst recommendations. `generate_report.py` does this.
- Do not calculate prices, changes, fees, taxes, or profits. The Go tool does this.
- Do not add sections, remove sections, or reword the output.
- Do not summarize the report in place of showing it.

The report is deterministic. Two runs with the same data give the same text.
Your own wording would break that.

## Prerequisites

- **Python 3.6 or later.** Required. `generate_report.py` imports only the
  standard library (`json`, `sys`, `argparse`). There is nothing to
  `pip install`. Do not create a virtual environment for it.
- **Go 1.25 or later.** Optional. `run.sh` uses it when it is present, and the
  first run downloads the module dependencies. Without Go, `run.sh` falls back
  to the bundled `company-analysis` binary, which is Linux x86-64 only.

`run.sh` reports a missing prerequisite and exits with status 3.

## If a step fails

When the Go tool cannot fetch the price data, it prints a JSON object with an
`error` field and exits with status 1. `generate_report.py` sees that field,
prints one line, and stops before it writes a report:

```
$ ./tools/company-analysis/run.sh ZZZZ
error: fetch price data for ZZZZ: yahoo finance returned status 404
```

Report that line to the user. Common causes:

| Error text | Cause |
|---|---|
| `status 404` | The ticker symbol does not exist. |
| `status 429` after retries | Yahoo Finance is rate limiting. Wait, then retry. |
| `fetch crumb` | Yahoo Finance blocked the session token request. |

Do not substitute a placeholder price and do not write the report by hand
instead. A report built on invented data is worse than no report.

Earnings and news are optional. If those fetches fail, the Go tool logs a
warning to stderr and still prints usable JSON. Let the pipeline continue.

News arrives from two Yahoo endpoints. The search endpoint gives the headline,
the publisher and the link. The RSS headline feed gives the article summary,
which the sentiment analysis needs. When the RSS fetch fails, the headlines stay
and the summaries are empty, so more articles classify as neutral.

Each headline in the report is a Markdown link to the article, so the user can
open the source. An item that arrives without a link stays as plain text.

## Bundled files

All of these ship with the plugin under `tools/company-analysis/`:

| File | Role |
|---|---|
| `run.sh` | The entry point. Run this. |
| `main.go`, `internal/` | The data fetcher and the simulator. |
| `generate_report.py` | Turns the JSON into the Markdown report. |
| `company-analysis` | Prebuilt Linux x86-64 binary, used when Go is absent. |
| `go.mod`, `go.sum` | Go module definition. |

## Simulation Parameters

- **Fee Scenarios**:
  - Robinhood/Vanguard: $0 commission per trade
  - Traditional Broker: $4.95 per trade (applied to both buy and sell transactions)
- **Tax Scenarios**:
  - Short-term gains (held < 1 year): Flat default rate of ~24%
  - Long-term gains (held ≥ 1 year): Flat default rate of ~15%
- **Cost to buy**: quantity × current price, before fees. Shown as its own column.
- **Sell price**: current price × 1.10, a hypothetical +10% gain
