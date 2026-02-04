---
name: market-brief
description: Create a 24-hour tactical market brief from the latest macro and financial news, covering equities, commodities, and macro/FX. Use when asked for a market brief, daily/24h outlook, short-term drivers, or a structured multi-asset summary with JST timestamps and strict short-line formatting.
---

# Market Brief

## Overview

Produce a concise, 24-hour tactical market brief using the latest reputable news. Follow the exact structure, line limits, and formatting rules.

## Workflow

### 1) Gather and verify news

- Pull the freshest macro and financial news from reputable sources (Bloomberg, Reuters, Dow Jones/WSJ, Financial Times, MarketWatch, Investing.com, Yahoo/Google Finance).
- Prioritize items published or updated in the last 24-48 hours.
- Verify both article publish time and actual event time; if they conflict, note the event time.

### 2) Cover full scope (all required markets)

- **Equities**: S&P 500, NASDAQ 100, Dow, Russell 2000, Nikkei 225, S&P/ASX 200, China A50, Hang Seng, MSCI Singapore, EURO STOXX 50, DAX, CAC 40, AEX, FTSE 100.
- **Commodities**: WTI, Brent, Gold, Silver, Copper, Platinum, NatGas.
- **Macro/FX**: UST yields, DXY, VIX, USD/JPY, EUR/USD.

### 3) Output structure (exact requirements)

For each category (Equities / Commodities / Macro&FX), do exactly:

1. **Key drivers (2-4)**: the freshest catalysts (data prints, central banks, geopolitics, positioning, microstructure).
2. **Why it matters**: one line per driver linking to price action/mechanism (e.g., "High CPI -> real yields up -> gold pressure").
3. **24h outlook**: Bias = {Bullish | Bearish | Sideways}. Add 2-3 critical levels or events (exact times in JST).
4. **Confidence**: 0-5. Add 1 alternate scenario (what flips the bias).

### 4) Formatting constraints (must follow)

- Use **very short lines**, one idea per line, separated by newlines. No paragraphs.
- Keep each category to **6-8 lines max**.
- Use Asia/Tokyo time for all dates/times and print a timestamp header.
- Numbers concise: yields as %, DXY as index, levels as spot/futures where relevant.
- No fluff, no investment advice. Tactical view only.

### 5) Optional user args

- If a user provides extra instructions (e.g., custom focus or extra assets), incorporate them while keeping all constraints intact.

## Output checklist (silent)

- Recency <=48h confirmed for each driver.
- Each category includes drivers, why, 24h bias, levels, event times (JST), alt scenario, confidence.
- No more than 8 lines per category. No paragraphs.
