---
name: finclaw
description: AI finance assistant — real-time quotes, charts, technical analysis, portfolio tracking, price alerts, watchlists, daily briefings, macro economics, and sentiment analysis for US stocks, BIST, crypto, and forex.
metadata:
  { "openclaw": { "emoji": "📈", "requires": { "bins": ["python3"] }, "install": [{ "id": "setup", "kind": "uv", "package": "yfinance", "bins": ["python3"], "label": "Python 3 required" }] } }
---




### Cleanup Review

`python scripts/_reset_state.py` is an optional cleanup helper for the `FinClaw — AI Finance Assistant` skill. It may recursively remove /tmp/skill_build. Show the exact paths first, explain whether they are skill-private temporary paths or user state, and run the cleanup only after the user confirms.

# FinClaw — AI Finance Assistant

Your personal finance assistant covering **US stocks**, **BIST (Turkish market)**, **crypto**, and **forex**. Includes portfolio tracking, price alerts, charts, technical analysis, daily briefings, and more.

## First-Time Setup

Run once after installation to create the Python venv and database:
```bash
python3 {baseDir}/scripts/setup.py
```

Then add to `openclaw.json` under `skills.entries`:
```json
"finclaw": {
  "env": {
    "FINNHUB_API_KEY": "",
    "FRED_API_KEY": "",
    "ALPHA_VANTAGE_API_KEY": "",
    "EXCHANGE_RATE_API_KEY": ""
  }
}
```
API keys are optional — core features (prices, charts, TA, portfolio, alerts) work without any keys.

## Running Scripts

All scripts use the skill's Python venv:
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/<script>.py [args]
```

---

## Market Data

### quote.py — Real-Time Quotes
Auto-detects asset type from symbol. Results cached for 60 seconds.

```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/quote.py AAPL              # US stock
{baseDir}/venv/bin/python3 {baseDir}/scripts/quote.py THYAO.IS          # BIST stock
{baseDir}/venv/bin/python3 {baseDir}/scripts/quote.py BTC               # Crypto
{baseDir}/venv/bin/python3 {baseDir}/scripts/quote.py USD/TRY           # Forex
{baseDir}/venv/bin/python3 {baseDir}/scripts/quote.py AAPL MSFT BTC     # Multiple
{baseDir}/venv/bin/python3 {baseDir}/scripts/quote.py AAPL --force      # Skip cache
{baseDir}/venv/bin/python3 {baseDir}/scripts/quote.py AAPL --json       # JSON output
```

**Symbol detection:** `.IS` → BIST | `BTC/ETH/SOL...` → Crypto | `USD/TRY` → Forex | else → US stock

### crypto.py — Crypto Market Data
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/crypto.py price BTC        # Binance price
{baseDir}/venv/bin/python3 {baseDir}/scripts/crypto.py top --limit 10   # Top gainers
{baseDir}/venv/bin/python3 {baseDir}/scripts/crypto.py try BTC          # Price in TRY
```

### forex.py — Exchange Rates
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/forex.py rate USD TRY
{baseDir}/venv/bin/python3 {baseDir}/scripts/forex.py convert USD TRY --amount 1000
{baseDir}/venv/bin/python3 {baseDir}/scripts/forex.py multi USD --targets TRY EUR GBP
```

### chart.py — Price Charts
Generates PNG charts. Send the saved file to the user.
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/chart.py AAPL                           # Candlestick
{baseDir}/venv/bin/python3 {baseDir}/scripts/chart.py BTC --type line --period 1y     # Line chart
{baseDir}/venv/bin/python3 {baseDir}/scripts/chart.py AAPL --sma 20 50 200           # With SMAs
```
Periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max

### technical.py — Technical Analysis
SMA, EMA, RSI, MACD, Bollinger Bands with buy/sell signals.
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/technical.py AAPL
{baseDir}/venv/bin/python3 {baseDir}/scripts/technical.py BTC --period 1y --json
```

### news.py — Financial News (requires FINNHUB_API_KEY)
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/news.py company --symbol AAPL
{baseDir}/venv/bin/python3 {baseDir}/scripts/news.py market --category crypto
```

### screener.py — Stock Screener
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/screener.py us                    # US gainers
{baseDir}/venv/bin/python3 {baseDir}/scripts/screener.py bist --direction bottom  # BIST losers
{baseDir}/venv/bin/python3 {baseDir}/scripts/screener.py crypto --limit 15       # Crypto gainers
```

---

## Portfolio & Alerts

### portfolio.py — Position Management
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/portfolio.py add --symbol AAPL --shares 10 --price 150
{baseDir}/venv/bin/python3 {baseDir}/scripts/portfolio.py sell --symbol AAPL --shares 5 --price 175
{baseDir}/venv/bin/python3 {baseDir}/scripts/portfolio.py remove --symbol AAPL
{baseDir}/venv/bin/python3 {baseDir}/scripts/portfolio.py list
{baseDir}/venv/bin/python3 {baseDir}/scripts/portfolio.py summary
```
Optional: `--fees 1.50`, `--date 2024-01-15`, `--name "Apple Inc"`, `--notes "Long hold"`

### alerts.py — Price Alerts
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/alerts.py create --symbol AAPL --condition above --target 200
{baseDir}/venv/bin/python3 {baseDir}/scripts/alerts.py create --symbol BTC --condition below --target 60000 --note "Buy signal"
{baseDir}/venv/bin/python3 {baseDir}/scripts/alerts.py list
{baseDir}/venv/bin/python3 {baseDir}/scripts/alerts.py delete --id 3
{baseDir}/venv/bin/python3 {baseDir}/scripts/alerts.py snooze --id 3 --hours 48
```
Conditions: `above`, `below`, `change_pct`, `volume_above`

### check_alerts.py — Alert Checker (for cron)
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/check_alerts.py
```

### pnl.py — Profit & Loss
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/pnl.py                    # All positions
{baseDir}/venv/bin/python3 {baseDir}/scripts/pnl.py --symbol AAPL      # Single symbol
```

### watchlist.py — Watchlists
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/watchlist.py create --name "Tech"
{baseDir}/venv/bin/python3 {baseDir}/scripts/watchlist.py add --name "Tech" --symbol AAPL
{baseDir}/venv/bin/python3 {baseDir}/scripts/watchlist.py show --name "Tech" --prices
{baseDir}/venv/bin/python3 {baseDir}/scripts/watchlist.py list
```

---

## Intelligence

### briefing.py — Market Briefings
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/briefing.py morning    # Full morning briefing
{baseDir}/venv/bin/python3 {baseDir}/scripts/briefing.py close      # End-of-day summary
{baseDir}/venv/bin/python3 {baseDir}/scripts/briefing.py weekend    # Weekend crypto + forex recap
```

### macro.py — Macro Economics (requires FRED_API_KEY)
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/macro.py dashboard
{baseDir}/venv/bin/python3 {baseDir}/scripts/macro.py indicator --name fed_rate
{baseDir}/venv/bin/python3 {baseDir}/scripts/macro.py list
```

### earnings.py — Earnings Calendar (requires FINNHUB_API_KEY)
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/earnings.py calendar
{baseDir}/venv/bin/python3 {baseDir}/scripts/earnings.py symbol --symbol AAPL
```

### sentiment.py — News Sentiment (requires ALPHA_VANTAGE_API_KEY)
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/sentiment.py --symbol AAPL
{baseDir}/venv/bin/python3 {baseDir}/scripts/sentiment.py --topics technology
```

### research.py — Deep Research
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/research.py AAPL
```

---

## Data Sources
- **US Stocks**: Finnhub (primary), yfinance (fallback) — no key needed
- **BIST**: yfinance with .IS suffix — no key needed
- **Crypto**: Binance API — no key needed
- **Forex**: ExchangeRate-API — works without key
- **Charts/TA**: matplotlib + mplfinance + pandas — local computation
- **News**: Finnhub — needs FINNHUB_API_KEY
- **Macro**: FRED — needs FRED_API_KEY
- **Sentiment**: Alpha Vantage — needs ALPHA_VANTAGE_API_KEY
