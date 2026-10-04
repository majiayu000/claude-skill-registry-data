---
name: alpaca-trading-backtest
description: >
  Execute deterministic, reproducible historical backtests from a start date,
  end date, and strategy concept using the Alpaca CLI plus agent-written
  workspace code. Use when the user wants to backtest a strategy, simulate
  historical trades, or return trades, diagnostics, and reproducibility artifacts.
---

# Trading API Backtesting

Use this skill when you want your AI agent to run a specific historical backtest with the Alpaca CLI and local workspace code. This version is optimized for run-specific execution: your agent writes the minimum readable code needed for the confirmed strategy, stores the exact artifacts, and reports the results back to you.

This skill is written for you, the person invoking it through your AI agent. **You** means the trader, developer, researcher, or operator asking your agent to run the backtest. Your agent should address you directly, restate assumptions clearly, and make every interpretation choice visible.

```text
strategy idea -> formalized rules -> confirmed assumptions -> CLI data fetch -> local script -> artifacts -> report
```

It is not a promise that a strategy will work in live markets. It is a reproducible research workflow.

## Required disclosures

Every report, `notes.md`, `report.md`, notebook, dashboard, or exported result should include:

> **Important disclosure**  
> This backtest is a hypothetical historical simulation and does not represent actual trading performance. Backtested results do not guarantee future results. Results depend on market-data quality, data feed selection, corporate-action handling, fees, slippage, liquidity, taxes, execution assumptions, and implementation details. This material is for research and educational purposes only and is not investment advice, a recommendation, an offer, or a solicitation to buy or sell securities, options, cryptocurrencies, or any other financial product. All investments involve risk and may lose value. Review Alpaca's disclosures and agreements at [alpaca.markets/disclosures](https://alpaca.markets/disclosures).

When paper trading appears in the workflow, add:

> Paper trading is a simulated environment. It does not involve real money or actual securities transactions. Paper results may differ from live trading because of fill assumptions, market impact, liquidity, latency, data differences, order handling, fees, and other market conditions.

When the backtest models Alpaca securities trading-activity fees, `notes.md`, `summary.json`, and `report.md` should link to the Alpaca Brokerage Fee Schedule PDF:

```text
https://files.alpaca.markets/disclosures/library/BrokFeeSched.pdf
```

Record the PDF revision date, extraction timestamp, modeled fee categories, and any fee items intentionally excluded.

## CLI prerequisites

### Alpaca CLI

Your agent should use the Alpaca CLI for market-data access.

Check whether it is installed:

```bash
alpaca version
```

Install with Go when needed:

```bash
go install github.com/alpacahq/cli/cmd/alpaca@latest
```

On macOS or Linux with Homebrew:

```bash
brew install alpacahq/tap/cli
```

Make sure the binary directory is on `PATH`, commonly `~/go/bin` for Go installs.

### Local execution permissions

Alpaca CLI commands should run in your local workspace where your Alpaca profile, environment variables, network access, and saved artifacts are available. Some agent runtimes express this as:

```text
required_permissions: ["all"]
```

Use the equivalent permission model in your agent environment so the CLI can access local auth/config and write run artifacts.

### Connectivity and authentication check

Before any backtest run, verify the CLI and credentials:

```bash
alpaca doctor
```

If authentication fails, your agent should stop the run and show you the available login/help command:

```bash
alpaca profile login --help
```

For interactive paper setup:

```bash
alpaca profile login
```

For API-key setup:

```bash
alpaca profile login --api-key
```

For automation, environment variables are preferred because secrets do not need to be written into generated code:

```bash
export ALPACA_API_KEY=PK...
export ALPACA_SECRET_KEY=...
export ALPACA_QUIET=1
```

Your agent should never print your secret key, commit it to files, include it in reports, or pass it in a way that exposes it to shell history.

### Machine-readable output

Use `--quiet` for commands whose output will be parsed by code:

```bash
alpaca account get --quiet
alpaca data bars --symbol SPY --start 2024-01-01 --end 2024-12-31 --timeframe 1Day --quiet
```

Use installed CLI help and schemas as the source of truth for flags and response fields:

```bash
alpaca --help-all
alpaca data bars --help
alpaca data bars --schema
alpaca data quotes --schema
```

Because the CLI is generated from API specifications and may evolve, your agent should prefer current `--help`, `--schema`, and `alpaca doctor` output over stale examples.

## Required workflow

Your agent should follow this workflow:

1. Gather required inputs: start date, end date, strategy concept or strategy file.
2. Gather or infer the rest: asset class, symbols or universe, timeframe, initial cash, position sizing, feed, adjustment mode, execution assumptions, benchmark.
3. Work through [run considerations](#run-considerations-checklist): order simulation, indicators, dividends, splits, fees, slippage, spread, market hours, calendar handling, and validation.
4. Translate your freeform idea into precise mathematical rules.
5. Present the formalized interpretation to you before writing code unless your request was already mathematically precise.
6. Check the workspace for reusable data, prior runs, and existing utilities.
7. Create a self-contained run folder.
8. Write `notes.md`, `strategy_spec.json`, `config.json`, and a readable run-specific script.
9. Fetch historical data through the Alpaca CLI, save raw CLI outputs, filter to the chosen market hours, and compute data fingerprints.
10. Run the local simulation.
11. Write artifacts.
12. Return the Teaching Five, first/last trade, assumptions, caveats, data fingerprint, and artifact paths.

## Workspace awareness

Before generating new code or fetching data, your agent should inspect the workspace.

### Data reuse

Look for prior raw data files or cached normalized data that match:

```text
symbol
asset class
feed
adjustment mode
timeframe
start/end range
calendar filter
regular-hours or extended-hours setting
```

Reuse data only when the data fingerprint matches. If fingerprints differ, your agent should treat the runs as using different input data.

### Run lineage

If this run is a variant of a prior run, `notes.md` should say what changed:

```text
changed RSI threshold from 30/70 to 25/75
changed fill model from next_open bar proxy to quote-aware fill
changed slippage from 5 bps to 10 bps
extended date range from 2020-2024 to 2018-2025
```

### Existing code

If the workspace already has a backtest engine or shared utility that matches the strategy requirements, your agent may reuse it. Otherwise, the default is a single readable `run.py` in the run folder.

## Run folder and artifact contract

Artifact paths in this skill use `raw/` and `normalized/` as canonical names.

Every run should create a folder like:

```text
runs/YYYY-MM-DD_symbol_strategy_timeframe/
  notes.md
  strategy_spec.json
  config.json
  run.py
  requirements.txt or pyproject.toml when needed
  raw/
    bars_SYMBOL.json
    quotes_SYMBOL.json
    trades_SYMBOL.json
    calendar.json
    corporate_actions.json
  normalized/
    bars_SYMBOL.csv
    quotes_SYMBOL.csv
  summary.json
  report.md
  trades.csv
  round_trips.csv
  equity.csv
  benchmark_equity.csv
  data_fingerprint.json
  warnings.json
  fee_source.json
```

### `notes.md`

`notes.md` should include your original request, confirmed strategy interpretation, every inferred/defaulted assumption, indicator definitions, fill model, fee model, data feed and adjustment mode, dividend and split treatment, benchmark definitions, calendar and market-hours handling, warnings and caveats, and Alpaca disclosure and fee schedule links.

### Other artifacts

See [reference.md](reference.md) for `summary.json`, `strategy_spec.json`, `data_fingerprint.json`, and `fee_source.json` schemas.

## Code generation rules

For run-specific CLI backtests, your agent should generate a script, not a reusable framework. A single-file `run.py` is the default.

Use readable code:

```python
fill_price = bar_open * (1 + friction_pct)
```

instead of compressed expressions that make the artifact hard to audit.

The generated code should:

- read raw or normalized files from the run folder;
- implement the confirmed strategy exactly;
- implement the chosen indicator definitions exactly (see [Indicator formulas](reference.md#indicator-formulas));
- keep signal timing separate from fill timing;
- compute fees, slippage, spread, and settlement according to the confirmed assumptions;
- produce all required artifacts;
- include deterministic sorting and timezone handling;
- avoid hidden network calls after data fetch unless explicitly documented.

Use Python 3 by default. Prefer the standard library plus pandas/numpy when available. Add dependencies only when they materially improve correctness or readability.

## Strategy translation

Your agent should formalize your idea before code generation.

Every rule should specify: data field, trigger, inclusive/exclusive bounds, indicator variant and parameters, warmup behavior, position sizing and rounding, cash handling, order type, fill model, and benchmark.

Example confirmation:

```text
I interpreted your strategy as:
- Symbol: SPY
- Timeframe: 1Day
- Data: Alpaca CLI bars, feed=sip, adjustment=split
- Indicator: SMA(50) and SMA(200), simple arithmetic mean of completed daily closes
- Entry: fast SMA crosses above slow SMA
- Exit: fast SMA crosses below slow SMA
- Signal timing: completed bar close
- Fill timing: next trading day's open
- Fill model: next_open bar proxy with 5 bps slippage unless quotes are available
- Sizing: invest 100% of available cash, fractional shares allowed when supported
- Benchmark: SPY buy-and-hold with same assumptions
```

After confirmation, code should match the confirmed interpretation.

## Fill models

Use these model names in confirmations and `notes.md`. Implementation detail is in [Fill model rules](reference.md#fill-model-rules).

- **`next_open`** (default): signal on bar T close; fill on bar T+1 open or quote at T+1 open timestamp.
- **`time_based`**: fill at a confirmed time of day; quote bid/ask when available.
- **`same_bar`**: only when explicitly requested; document look-ahead risk in `notes.md` and the report.
- **Limit and stop orders**: OHLC-bar eligibility rules apply; use conservative intrabar conflict policy when stop and target both touch the same bar.

## Report format

`report.md` should lead with **Performance vs Benchmarks**:

```markdown
| | Total Return | Ann. Return | Max Drawdown | Sharpe | Final Equity |
|---|---:|---:|---:|---:|---:|
| **Strategy** | ...% | ...% | ...% | ... | $... |
| Benchmark | ...% | ...% | ...% | ... | $... |
```

After the table, include strategy configuration, symbols/timeframe/feed/adjustment, fill model and friction, first and last trade, detailed metrics, benchmark explanation, assumptions, data fingerprint, caveats, and the disclosure block.

Metric definitions are in [reference.md](reference.md#metric-formulas).

## In-chat response standard

Lead with the **Teaching Five**:

1. total return versus benchmark;
2. max drawdown;
3. number of trades;
4. win rate;
5. Sharpe ratio versus benchmark.

Then include: annualized return, profit factor, fees paid, first trade, last trade, assumptions made, data fingerprint summary, artifact paths, and most important caveats.

If no trades occurred, say that directly and explain whether this was due to warmup, no signal, insufficient cash, missing data, or calendar filtering.

## Run considerations checklist

Your agent should resolve each item before running:

- order simulation and fill timing;
- quote-aware versus bar-proxy fills;
- dividend handling;
- split and reverse-split handling;
- execution friction;
- PDF-derived trading-activity fees;
- market hours and extended-hours inclusion;
- calendar-based decisions;
- benchmark choice;
- look-ahead bias;
- survivorship bias;
- out-of-sample or walk-forward validation for parameter tuning;
- overfitting risk for repeated variants.

For order simulation, dividends, splits, fees, calendar, and benchmarks, document choices in `notes.md` when not specified by you.

## Safety and quality guardrails

Your agent must avoid:

- using future data in signal generation;
- using same-bar decision and fill without a documented `same_bar` model and warning;
- hiding execution assumptions;
- mixing adjusted bars with separate split adjustments;
- pretending vague rules were fully specified;
- discarding generated code after the run;
- including extended-hours bars unless you requested them;
- silently substituting indicator variants;
- treating open, close, high, low, VWAP, and quote-derived prices as interchangeable fill proxies;
- computing Sharpe from per-bar returns when the report says daily Sharpe;
- using population standard deviation for Sharpe when sample standard deviation (N-1) is required;
- submitting live orders as part of a historical backtest;
- claiming support for unsupported products — options require explicit contract selection and fill logic;
- bypassing the Alpaca CLI by switching to direct HTTP calls;
- running Alpaca CLI commands in a sandbox without local auth and filesystem access;
- implementing fill logic that deviates from [Fill model rules](reference.md#fill-model-rules) without documenting the deviation in `notes.md`;
- using `close` vs `high` vs `low` interchangeably for signal triggers;
- silently choosing between crossover and threshold signal logic;
- generating a multi-module engine when a single-file script will do.

## Optional paper forward-validation handoff

After a historical backtest, your agent may prepare a paper forward-validation package if you request it:

```text
paper_config.json
strategy_runtime.py
risk_limits.json
alpaca_order_adapter.py
reconciliation_plan.md
```

This is separate from the historical backtest. It should use explicit risk limits, client order IDs for automation, and reconciliation of expected versus actual paper fills.

## Troubleshooting

```text
command not found: alpaca
  Check PATH and Go install location, commonly ~/go/bin.

alpaca doctor reports auth failure
  Re-run alpaca profile login or set ALPACA_API_KEY and ALPACA_SECRET_KEY.

CLI output includes non-data text
  Use --quiet or set ALPACA_QUIET=1.

Parsed fields changed
  Run <command> --schema and update the parser for the current CLI response.

Rate limited
  Respect Retry-After, reduce request frequency, and use cached data where fingerprints match.

Pagination missing data
  Check next_page_token and fetch all pages.
```

## Related references

Useful commands:

```bash
alpaca version
alpaca update --check --quiet
alpaca doctor
alpaca --help-all
alpaca data bars --help
alpaca data bars --schema
alpaca data quotes --schema
alpaca calendar --help
```

Disclosure links:

```text
https://alpaca.markets/disclosures
https://files.alpaca.markets/disclosures/library/BrokFeeSched.pdf
```

CLI data acquisition, indicator formulas, fee model, metrics, benchmarks, and JSON schemas: [reference.md](reference.md).

## Related files

- [reference.md](reference.md)
