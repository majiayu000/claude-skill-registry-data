---
name: market-data
description: Query market data from Yahoo Finance — prices, fundamentals, earnings, options, dividends, history. Pure data tool for any ticker (US, HK, A-shares, crypto, forex, ETFs). Use before analysis, not instead of it.
---

# Market Data

Data is the raw material of judgment. This tool fetches it. What you do with it — that is analysis, and analysis is your job.

Every subcommand returns one dimension of data for one or more tickers. Combine them as needed. Don't fetch everything when you only need a price.

## Usage

```bash
.agents/skills/market-data/finance <command> <args>
```

## Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `quote` | Price, change, market cap, PE, 52W range | `finance quote AAPL 0700.HK` |
| `history` | OHLCV price history | `finance history TSLA 1y` |
| `fundamentals` | Valuation, margins, debt, analyst targets | `finance fundamentals NVDA` |
| `earnings` | Next date, EPS estimates, past surprises | `finance earnings MSFT` |
| `profile` | Sector, industry, employees, description | `finance profile GOOGL` |
| `dividends` | Yield, ex-date, payout history | `finance dividends KO` |
| `options` | Near-the-money calls and puts | `finance options SPY` |
| `compare` | Side-by-side ticker comparison | `finance compare AAPL,MSFT,GOOGL` |

### history periods

`1d` `5d` `1mo` `3mo` `6mo` `1y` `2y` `5y` `ytd` `max` — default `1mo`.

### Symbol format

Any Yahoo Finance ticker works:
- US: `AAPL`, `MSFT`
- Hong Kong: `0700.HK`, `9988.HK`
- A-shares: `600519.SS` (Shanghai), `000858.SZ` (Shenzhen)
- Crypto: `BTC-USD`, `ETH-USD`
- Forex: `EURUSD=X`
- ETFs: `SPY`, `QQQ`
- Indices: `^VIX`, `^GSPC`, `^HSI`

## When to use

- Before forming or updating a view — get current data, not stale memory
- When the user asks about a stock, price, or financial metric
- When building a briefing or comparison
- When checking if a stored belief still holds

## When not to use

- For news or narrative — use web-search instead
- When the data is already in the conversation and still fresh
