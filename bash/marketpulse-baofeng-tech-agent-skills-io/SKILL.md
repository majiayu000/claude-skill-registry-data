---
name: marketpulse
description: 'Query real-time and historical equity market data—prices, news, financial statements, metrics, analyst estimates, insider and institutional activity, SEC filings, earnings press releases, segmented revenues, stock screening, and macro interest rates. Use when you need broad public-market research from a single AIsa-backed skill. Use when: the user needs market data, stock analysis, dividend research, or read-only financial data workflows.'
license: MIT
allowed-tools: Read Bash Grep
when_to_use: 'you need broad public-market research from a single AIsa-backed skill. Use when: the user needs market data, stock analysis, dividend research, or read-only financial data workflows'
---

> Release note: This package is published for Claude Code. References to OpenClaw below describe the original source workflow, a companion runtime, or compatibility guidance unless the skill is explicitly about OpenClaw itself.

# MarketPulse 📊

Broad equity market data for autonomous agents, powered by AIsa.

Use this skill when you need one place to query stock prices, company news, financial statements, filings, estimates, ownership activity, screening results, and macro interest-rate context.

## Use when

- You want historical or intraday price data for a public equity ticker.
- You need company news, SEC filings, insider trades, or institutional ownership data.
- You want annual, quarterly, or TTM financial statements and related metrics.
- You need analyst estimates, earnings press releases, or segmented revenue breakdowns.
- You want to screen stocks or compare specific financial line items across multiple tickers.
- You need macro interest-rate data to add policy context to equity research.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible harness, including:

- **Claude Code** and **Claude**
- **OpenAI Codex**
- **Cursor**
- **Gemini CLI**
- **OpenCode**, **Goose**, **OpenClaw**, **Hermes**
- and other harnesses that implement the [Agent Skills specification](https://agentskills.io/specification)

Requires Python 3, a POSIX shell, and `AISA_API_KEY` (available from [aisa.one](https://aisa.one)).

## Quick start

```bash
export AISA_API_KEY="your-key"
```

## Example requests

### Investment research

```text
"Full analysis: NVDA price trends, insider trades, analyst estimates, SEC filings"
```

### Earnings analysis

```text
"Get Tesla earnings press releases, analyst estimates, and price reaction"
```

### Market screening

```text
"Find stocks with P/E < 15 and revenue growth > 20%"
```

### Insider activity review

```text
"Track insider trades at Apple and correlate with price movements"
```

### Segment deep-dive

```text
"Break down Apple's revenue by product segment and geography"
```

---

## Traditional finance endpoints

### Stock prices

```bash
# Historical price data (daily)
curl "https://api.aisa.one/apis/v1/financial/prices?ticker=AAPL&interval=day&interval_multiplier=1&start_date=2025-01-01&end_date=2025-12-31" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Weekly price data
curl "https://api.aisa.one/apis/v1/financial/prices?ticker=AAPL&interval=week&interval_multiplier=1&start_date=2025-01-01&end_date=2025-12-31" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Minute-level data (intraday)
curl "https://api.aisa.one/apis/v1/financial/prices?ticker=AAPL&interval=minute&interval_multiplier=5&start_date=2025-01-15&end_date=2025-01-15" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

**Parameters:**
- `ticker`: Stock symbol (required)
- `interval`: `second`, `minute`, `day`, `week`, `month`, `year` (required)
- `interval_multiplier`: Multiplier for interval, for example 5 for 5-minute bars (required)
- `start_date`: Start date in `YYYY-MM-DD` format (required)
- `end_date`: End date in `YYYY-MM-DD` format (required)

### Company news

```bash
# Get news by ticker
curl "https://api.aisa.one/apis/v1/financial/news?ticker=AAPL&limit=10" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### Financial statements

```bash
# All financial statements (requires period)
curl "https://api.aisa.one/apis/v1/financial/financials?ticker=AAPL&period=annual" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Income statements
curl "https://api.aisa.one/apis/v1/financial/financials/income-statements?ticker=AAPL&period=annual" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Balance sheets
curl "https://api.aisa.one/apis/v1/financial/financials/balance-sheets?ticker=AAPL&period=annual" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Cash flow statements
curl "https://api.aisa.one/apis/v1/financial/financials/cash-flow-statements?ticker=AAPL&period=annual" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

**Parameters:**
- `ticker`: Stock symbol (required)
- `period`: `annual`, `quarterly`, or `ttm` (required)

### Segmented revenues

```bash
# Break down revenue by business segment and geography
curl "https://api.aisa.one/apis/v1/financial/financials/segmented-revenues?ticker=AAPL&period=annual" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

**Parameters:**
- `ticker`: Stock symbol (required)
- `period`: `annual` or `quarterly` (required)

### Financial metrics

```bash
# Real-time financial metrics snapshot
curl "https://api.aisa.one/apis/v1/financial/financial-metrics/snapshot?ticker=AAPL" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Historical financial metrics (period required)
curl "https://api.aisa.one/apis/v1/financial/financial-metrics?ticker=AAPL&period=annual" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### Analyst estimates

```bash
# Earnings per share estimates
curl "https://api.aisa.one/apis/v1/financial/analyst-estimates?ticker=AAPL&period=annual" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### Earnings press releases

```bash
# Get earnings press releases
curl "https://api.aisa.one/apis/v1/financial/earnings/press-releases?ticker=NVDA" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

**Note:** This endpoint has narrower ticker coverage than other financial endpoints. Passing an unsupported ticker returns `{"error":"Invalid ticker"}`. See [earnings-press-releases-tickers.md](./earnings-press-releases-tickers.md) for the full list of supported tickers (~2,776 as of 2026-04-14).

### Insider trading

```bash
# Get insider trades
curl "https://api.aisa.one/apis/v1/financial/insider-trades?ticker=AAPL" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### Institutional ownership

```bash
# Get institutional ownership (by ticker OR investor)
curl "https://api.aisa.one/apis/v1/financial/institutional-ownership?ticker=AAPL" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### SEC filings

```bash
# Get SEC filings
curl "https://api.aisa.one/apis/v1/financial/filings?ticker=AAPL" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Get SEC filing items (requires filing type and year)
curl "https://api.aisa.one/apis/v1/financial/filings/items?ticker=AAPL&filing_type=10-K&year=2024" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### Company facts

```bash
# Get company facts (by ticker or CIK)
curl "https://api.aisa.one/apis/v1/financial/company/facts?ticker=AAPL" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### Stock screener

```bash
# Screen for stocks matching criteria
curl -X POST "https://api.aisa.one/apis/v1/financial/financials/search/screener" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"filters":{"pe_ratio":{"max":15},"revenue_growth":{"min":0.2}}}'
```

### Search line items

```bash
# Search specific financial line items across tickers
curl -X POST "https://api.aisa.one/apis/v1/financial/financials/search/line-items" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"tickers":["AAPL","MSFT"],"line_items":["revenue","net_income"],"period":"annual"}'
```

### Interest rates (macro)

```bash
# Current interest rates
curl "https://api.aisa.one/apis/v1/financial/macro/interest-rates/snapshot" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Historical interest rates
curl "https://api.aisa.one/apis/v1/financial/macro/interest-rates?bank=fed" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

---

## Python client

```bash
# ==================== Stock Data ====================
# Note: start_date and end_date are REQUIRED for prices
python3 scripts/market_client.py stock prices --ticker AAPL --start 2025-01-01 --end 2025-01-31
python3 scripts/market_client.py stock prices --ticker AAPL --start 2025-01-01 --end 2025-01-31 --interval week
python3 scripts/market_client.py stock news --ticker AAPL --count 10

# ==================== Financial Statements ====================
python3 scripts/market_client.py stock statements --ticker AAPL --type all --period annual
python3 scripts/market_client.py stock statements --ticker AAPL --type income --period quarterly
python3 scripts/market_client.py stock statements --ticker AAPL --type balance --period annual
python3 scripts/market_client.py stock statements --ticker AAPL --type cash --period ttm

# ==================== Segmented Revenues ====================
python3 scripts/market_client.py stock segments --ticker AAPL --period annual

# ==================== Metrics & Analysis ====================
python3 scripts/market_client.py stock metrics --ticker AAPL
python3 scripts/market_client.py stock metrics --ticker AAPL --historical --period annual
python3 scripts/market_client.py stock analyst --ticker AAPL
python3 scripts/market_client.py stock earnings --ticker AAPL

# ==================== Insider & Institutional ====================
python3 scripts/market_client.py stock insider --ticker AAPL
python3 scripts/market_client.py stock ownership --ticker AAPL

# ==================== SEC Filings ====================
python3 scripts/market_client.py stock filings --ticker AAPL
python3 scripts/market_client.py stock filings --ticker AAPL --items --filing-type 10-K --year 2024

# ==================== Stock Screener / Line Items ====================
python3 scripts/market_client.py stock screen --pe-max 15 --growth-min 0.2
python3 scripts/market_client.py stock line-items --tickers AAPL,MSFT --items revenue,net_income --period annual

# ==================== Interest Rates ====================
python3 scripts/market_client.py stock rates
python3 scripts/market_client.py stock rates --historical --bank fed
```

---

## API endpoints reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/financial/prices` | GET | Historical stock prices (requires interval params) |
| `/financial/news` | GET | Company news by ticker |
| `/financial/financials` | GET | All financial statements (requires `period`) |
| `/financial/financials/income-statements` | GET | Income statements (requires `period`) |
| `/financial/financials/balance-sheets` | GET | Balance sheets (requires `period`) |
| `/financial/financials/cash-flow-statements` | GET | Cash flow statements (requires `period`) |
| `/financial/financials/segmented-revenues` | GET | Revenue by segment/geography (requires `period`) |
| `/financial/financial-metrics/snapshot` | GET | Real-time financial metrics |
| `/financial/financial-metrics` | GET | Historical metrics (requires `period`) |
| `/financial/analyst-estimates` | GET | EPS estimates |
| `/financial/earnings/press-releases` | GET | Earnings press releases (see [supported tickers](./earnings-press-releases-tickers.md)) |
| `/financial/insider-trades` | GET | Insider trades |
| `/financial/institutional-ownership` | GET | Institutional ownership |
| `/financial/filings` | GET | SEC filings |
| `/financial/filings/items` | GET | SEC filing items (requires `filing_type`, `year`) |
| `/financial/company/facts` | GET | Company facts |
| `/financial/financials/search/screener` | POST | Stock screener |
| `/financial/financials/search/line-items` | POST | Search specific line items across tickers |
| `/financial/macro/interest-rates/snapshot` | GET | Current interest rates |
| `/financial/macro/interest-rates` | GET | Historical rates |

---

## Pricing

| API | Cost |
|-----|------|
| Stock prices | ~$0.001 |
| Company news | ~$0.001 |
| Financial statements | ~$0.002 |
| Segmented revenues | ~$0.002 |
| Analyst estimates | ~$0.002 |
| Earnings press releases | ~$0.001 |
| SEC filings | ~$0.001 |
| Line items / screener | ~$0.002 |
| Interest rates | ~$0.0005 |

---

## Get started

1. Sign up at [aisa.one](https://aisa.one)
2. Get your API key
3. Add credits (pay-as-you-go)
4. Set the environment variable: `export AISA_API_KEY="your-key"`

## Full API reference

See [API Reference](https://aisa.one/docs/api-reference/) for complete endpoint documentation.
