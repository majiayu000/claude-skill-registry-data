---
name: financial-analysis
description: "\"Research company financials, market prices, SEC filings, earnings calls, investor presentations, options, forex, crypto, and macroeconomic data using structured financial APIs. Use for stock prices, OHLCV charts, financial statements, ratios and screening, fundamentals, earnings transcripts, management commentary, SEC filings (10-K/8-K/risk factors), technical indicators, dividends, IPOs, splits, options chains, exchange rates and currency conversion, crypto prices, treasury yields, inflation, labor data, non-US listings, and table or CSV financial-data requests.\""
compatibility: opencode
---

# Financial Analysis

Professional-grade financial market data across multiple asset classes and data domains. This skill pairs a broad multi-asset API surface with strict execution discipline: confirmed operation names, clear source-selection rules, and corrections for known failure modes.

## When to Use This Skill

**ALWAYS invoke these structured APIs (never web scraping or guessing) when users mention:**
Market data (prices, charts, OHLCV, snapshots, quotes, trades); fundamentals (balance sheet, income statement, cash flow, P/E, revenue, EPS, market cap, screening); technical analysis (SMA, EMA, MACD, RSI, overbought/oversold); SEC filings (10-K, 10-Q, 8-K, risk factors, annual report); earnings (earnings call, transcript, "what did the CEO say", management commentary, guidance); corporate actions (dividend, IPO, stock split, short interest, float); options (contracts, calls, puts, strike, expiration); forex (exchange rate, currency conversion, EUR/USD); crypto (BTC, ETH, crypto market); macro (inflation, CPI, treasury yield, unemployment, interest rate, labor market); and IR content (investor presentation, slide deck, investor day, AGM).

## Source Selection (Route to the Right Provider)

Three providers are available through the sandbox `data_api.ApiClient`. Pick the **smallest source set** that satisfies the request; do not call all three by reflex.

| Need | Provider | Notes |
| :--- | :--- | :--- |
| Latest/current price, intraday quick check, **non-US listings** (e.g., `7203.T`, `005930.KS`), company profile, insider/institutional holders, analyst insights | **Yahoo Finance** | Best for real-time/current prices and international tickers. 5 endpoints only. |
| US structured fundamentals, OHLCV history, ratios & screening, SEC filing text, options, forex, crypto, macro, technical indicators, **bulk/table data** | **Massive** | US-centric quantitative engine. ~60 verified endpoints. |
| Earnings call transcripts (full text + chapters), corporate events, investor presentation slide decks, filing PDFs | **Quartr** | Qualitative IR documents. Use the events-first workflow. |

Use **Massive for numbers and structured/bulk data**, **Quartr for documents/transcripts/events**, and **Yahoo Finance for current prices and non-US tickers**.

All three providers are accessed the same way; never look for an MCP server:
```python
import sys
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient
client = ApiClient()
```

## Critical Execution Rules (Known Failure-Mode Corrections)

These rules override default behavior. They exist because each addresses a previously observed failure.

1. **Latest stock price → Yahoo Finance, not stale Massive bars.** For "current"/"latest"/"today's" price, call `YahooFinance/get_stock_chart` (read `meta.regularMarketPrice`). Do NOT report a historical Massive bar close as the current price, and never pull a price from web search.

2. **Financial statements → Massive structured endpoints, not scraping.** For income statement, balance sheet, or cash flow, call `Massive/get_income_statements` / `Massive/get_balance_sheets` / `Massive/get_cash_flow_statements`. Do NOT scrape websites or hand-type numbers. Cite `fiscal_year`/`fiscal_quarter`/`period_end`.

3. **Earnings calls → Quartr events-first workflow.** Resolve company → `Quartr/list_events` (`sortBy='date'`, `direction='desc'`) → pick the right fiscal event → `list_transcripts`/`list_reports`/`list_slides` with `eventIds` → retrieve by **Document ID**. Never call the document-list endpoints without first finding the event (they sort by internal ID, not date).

4. **Do NOT invent API operation names.** Only use names confirmed in the reference files. Verified-invalid examples that must NOT be used: `Massive/get_edgar_index` (use `get_sec_edgar_index`), `Massive/get_quotes` (use `get_stock_quotes`), `Massive/get_trades` (use `get_stock_trades`), `Massive/get_top_market_movers` (use `get_top_movers`), `Massive/get_single_ticker_snapshot` (use `get_stock_snapshot`), `Massive/get_13f_filings`/`get_form3`/`get_form4` (not available), `Quartr/list_slide_decks` (use `list_slides`), `Quartr/get_transcript_chapters` (use `list_transcript_chapters`), `YahooFinance/get_stock_quote`/`get_stock_financials` (do not exist).

5. **Non-US tickers → Yahoo Finance.** Massive does not cover ordinary international listings. For Toyota (`7203.T`), Samsung (`005930.KS`), Nestlé (`NESN.SW`), etc., use Yahoo Finance with the correct suffix and `region`.

6. **Bulk/table/CSV requests → structured APIs + pagination, not one-by-one scraping.** For "all the splits", multi-year statements, full OHLCV history, or screening, use the appropriate Massive list endpoint with `limit`/pagination, then assemble the table programmatically.

## API Operation Discipline

- All query parameter values must be **strings** (e.g., `'limit': '5'`).
- Respect `path_params` vs `query` placement exactly as documented per endpoint.
- For Yahoo Finance, add a **0.5–1.0s sleep** between consecutive calls to avoid `429` rate limiting.
- If an operation returns "api not found", do not retry variants blindly — check the reference for the confirmed name.

## Core Capabilities

**Stock market data:** real-time snapshots, historical OHLCV bars (minute to yearly), daily summaries, previous-day bars, open/close with pre/after-hours, top gainers/losers, last trade, last NBBO quote, tick-level trades and quotes.

**Company fundamentals:** income statements, balance sheets, cash flow statements; 22 financial ratios (P/E, P/B, ROE, ROA, EV/EBITDA) with range filtering for **screening**; company profile (market cap, employees, SIC, IPO date); free float, short interest, daily short volume.

**Technical indicators:** SMA, EMA (configurable window/timespan), MACD (line/signal/histogram), RSI (0–100).

**SEC filings & regulatory:** 10-K section text, 8-K material-event text, SEC EDGAR index, standardized risk factors and risk categories; filing PDFs via Quartr.

**Earnings & investor relations (Quartr):** full-text transcripts with chapter navigation, corporate events (earnings calls, AGMs, investor days, conferences), investor presentation slide decks, company IR profiles.

**Corporate actions:** dividends, IPOs (2008+), stock splits, ticker lifecycle events.

**Options:** contract search (filter by ticker/type/expiration/strike), contract details, historical OHLCV bars, previous-day and open/close data.

**Forex:** historical OHLCV bars, real-time quotes and snapshots, top movers, currency conversion (`C:EURUSD`).

**Crypto:** historical OHLCV bars, snapshots, daily summaries, open/close, top movers, tick-level and last trade (`X:BTCUSD`).

**Macroeconomic:** CPI / core CPI inflation, inflation expectations, treasury yields (7 maturities, back to 1962), labor market (unemployment, participation, hourly earnings).

**Reference data:** cross-asset ticker search, unified snapshots, exchange directory, condition codes, ticker types, market holidays and status.

## Common Workflows

### 1. Stock Deep Dive
```
"Full analysis of NVDA"
→ YahooFinance/get_stock_chart (latest price, meta.regularMarketPrice)
→ Massive/get_ticker_overview (company profile)
→ Massive/get_income_statements + get_financial_ratios (financials & valuation)
→ Massive/get_stock_bars (price history)
→ Massive/get_rsi + get_macd (technical signals)
→ Massive/get_news (recent news)
```

### 2. Earnings Call Analysis (events-first)
```
"What did Apple's CEO say on the last earnings call?"
→ lookup_company.py --name "Apple"  (or Quartr/list_companies by ticker)
→ Quartr/list_events (sortBy=date, direction=desc) → select latest earnings event
→ Quartr/list_transcripts (eventIds=..., expand=event)
→ Quartr/get_transcript (by Document ID) + list_transcript_chapters
   (or simply: fetch_quartr_document.py --ticker AAPL --document transcript --latest --full)
```

### 3. SEC Filing Research
```
"What are Tesla's risk factors?"
→ Massive/get_10k_sections (section 1A)
→ Massive/get_risk_factors (standardized text)
→ Massive/get_sec_edgar_index (browse all filings)
```

### 4. Stock Screening
```
"Find stocks with ROE > 15% and P/E < 25"
→ Massive/get_financial_ratios (return_on_equity.gte=0.15, price_to_earnings.lte=25)
```

### 5. Macro / Economic Research
```
"Show inflation trends and the treasury yield curve"
→ Massive/get_inflation + get_inflation_expectations
→ Massive/get_treasury_yields
→ Massive/get_labor_market
```

### 6. Options Analysis
```
"Find Apple call options expiring in June"
→ Massive/get_option_contracts_list (underlying_ticker, contract_type=call, expiration_date)
→ Massive/get_option_contract (details) → get_option_bars (price history)
```

### 7. Forex & Currency
```
"Convert 10,000 USD to EUR and show the trend"
→ Massive/convert_currency (from=USD, to=EUR, amount=10000)
→ Massive/get_forex_bars (C:EURUSD history)
```

### 8. Non-US Stock
```
"How is Toyota stock doing?"
→ YahooFinance/get_stock_chart (symbol=7203.T, region=JP)
→ YahooFinance/get_stock_profile (company background)
```

### 9. Investor Presentations
```
"Show Meta's latest investor presentation"
→ Quartr/list_events → Quartr/list_slides (eventIds) → Quartr/get_slide (Document ID)
   (or: fetch_quartr_document.py --ticker META --document slide --latest)
```

## Ticker Formats

| Asset Class | Format | Examples |
|-------------|--------|----------|
| US Stocks | Plain symbol | `AAPL`, `TSLA`, `NVDA` |
| Non-US Stocks (Yahoo) | Symbol + exchange suffix | `7203.T`, `005930.KS`, `NESN.SW` |
| Options | OCC format (`O:`) | `O:AAPL250620C00150000` |
| Forex | `C:{FROM}{TO}` | `C:EURUSD`, `C:GBPJPY` |
| Crypto | `X:{BASE}{QUOTE}` | `X:BTCUSD`, `X:ETHUSD` |
| Indices | Caret prefix | `^GSPC` (S&P 500) |

## Helper Scripts (Quartr)

Run from the installed skill directory. They automate the events-first workflow.
```bash
python3 /home/ubuntu/skills/financial-analysis/scripts/lookup_company.py --name "Microsoft"
python3 /home/ubuntu/skills/financial-analysis/scripts/fetch_quartr_document.py --ticker MSFT --document transcript --latest --full --output transcript.json
```

## API Reference

Search any API by name with `type: api` to get full parameters, response schemas, and code examples. Reference files list only confirmed-working operation names.
- [Massive APIs](references/massive-api-reference.md) — stocks, fundamentals, ratios, filings, options, forex, crypto, macro, technicals
- [Quartr APIs](references/quartr-api-reference.md) — transcripts, events, reports, slide decks (events-first)
- [Yahoo Finance APIs](references/yahoo-finance-api-reference.md) — latest prices, profiles, holders, insights, SEC filings list (incl. non-US)

## Final Answer Checklist

Before delivering, confirm: (1) latest-price requests used Yahoo Finance, not stale Massive bars; (2) every API operation name used appears in a reference file; (3) financial figures came from structured endpoints with period metadata cited; (4) earnings/IR documents were retrieved via the events-first workflow by Document ID; (5) non-US tickers were routed to Yahoo Finance; (6) bulk/table requests used pagination, not one-by-one lookups.
