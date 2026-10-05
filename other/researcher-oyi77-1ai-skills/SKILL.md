---
name: trading-researcher
description: Use when researching market conditions, on-chain data, and sentiment
  to identify trading opportunities. Use for market analysis.
domain: trading
author: oyi77
license: Apache-2.0
subdomain: trading
tags:
- algorithms
- markets
- researcher
- trading
allowed-tools:
- Bash(trading:*)
- MCP(yahoo:*)
- MCP(exa:*)
- fs
- network
version: 1.0.0
category: trading
---


# Trading Researcher

## Overview

Automated market research and data collection for trading strategies. The Researcher serves as the intelligence arm of the trading team, continuously scanning markets, analyzing conditions, and identifying high-probability trading opportunities. It integrates with Yahoo Finance for price data and Exa for internet-based market research, providing the foundational insights that drive strategy development and execution decisions.

## When to Use

**Trigger phrases:**
- "trading researcher"
- "Use when working with trading researcher"


- Analyzing current market conditions for specific symbols or multiple symbols
- Collecting historical OHLCV data for backtesting and strategy development
- Scanning watchlists for trading opportunities across multiple instruments
- Generating market analysis reports with technical indicators
- Integrating external research from Exa to supplement price data
- Building opportunity scores based on multiple criteria (trend, momentum, volatility)
- Creating market condition alerts for automated triggers

## The Process

The research pipeline collects market data, calculates technical indicators, scans watchlists, and generates analysis reports.


### 1. Analyze Market Conditions

Analyze current market conditions for a specific symbol:

```typescript
const data = await yahoo.getOHLCV({
  symbol: "XAUUSD=X",
  interval: "1h",
  count: 100
});

const sma20 = calculateSMA(data.close, 20);
const rsi = calculateRSI(data.close, 14);

const analysis = {
  trend: sma20 > sma50 ? "bullish" : "bearish",
  rsi: rsi.value,
  recommendation: rsi > 70 ? "overbought" : rsi < 30 ? "oversold" : "neutral"
};

console.log(analysis);
```

### 2. Collect Historical Data

Fetch and store historical data for backtesting:

```typescript
const params = {
  symbol: "XAUUSD",
  start: "2024-01-01",
  end: "2024-12-31",
  timeframe: "H1"
};

const data = await yahoo.getHistorical(params);
await storage.save("xauusd_2024_h1.json", data);

console.log(`Collected ${data.length} bars`);
```

### 3. Scan for Opportunities

Scan watchlist and rank opportunities by signal strength:

```typescript
const symbols = ["XAUUSD", "EURUSD", "GBPUSD", "BTCUSD"];

const opportunities = [];
for (const symbol of symbols) {
  const data = await yahoo.getOHLCV(symbol, "1h", 100);
  const signal = await analyze(data);
  
  if (signal.strength > 0.7) {
    opportunities.push({ symbol, ...signal });
  }
}

opporunities.sort((a, b) => b.strength - a.strength);
console.table(opportunities);
```

### 4. Generate Market Analysis Report

Create comprehensive market analysis for strategy teams:

```typescript
const report = {
  date: new Date().toISOString(),
  symbols: ["XAUUSD", "EURUSD", "GBPUSD"],
  analysis: {},
  recommendations: {},
  riskLevel: "moderate"
};

await notion.createPage("Market Analysis", report);
```

### 5. Scan with External Research

Integrate Exa for additional market context:

```typescript
const research = await exa.search({
  query: "XAUUSD technical analysis and news",
  numResults: 5
});

const signals = await analyzeWithNews(data, research);
```

## When NOT to Use

- Task is about portfolio management, not trading (use portfolio skills)
- Task is about financial analysis (use analysis skills)
- You need to analyze trade results (use analytics skills)
- Task is about risk management (use risk skills)
- You don't have trading capital
- Task requires financial advice (consult advisors)


## Red Flags

- **Data quality issues detected**: Missing bars, sudden price jumps, or inconsistent volumes may indicate data provider issues; verify source and interval settings
- **Opportunity scoring produces no candidates**: Market may be in low-volatility range or strategy parameters too restrictive; review scan criteria and expand if needed
- **Yahoo Finance API rate limited**: Reduce query frequency or implement caching; consider data provider rotation
- **Analysis results inconsistent with visible chart patterns**: Calculation errors or incorrect parameter usage; verify indicator formulas and data alignment
- **Exa search returning irrelevant results**: Query too generic or time-sensitive content not indexed; refine search terms and add date filters
- **No trading signals generated during volatile periods**: Strategy may require adjustment for high-volatility regimes; review parameter sensitivity

## Verification

Verification covers data quality, indicator accuracy, scan consistency, and integration with data sources.


### Data Collection Verification
- [ ] Historical data covers required date range without gaps
- [ ] OHLCV data quality validated (no extreme outliers, consistent volume)
- [ ] Data stored in appropriate format for backtesting engine
- [ ] Data timestamps correctly aligned with trading session hours

### Market Analysis Verification
- [ ] Technical indicators (SMA, RSI, ATR) calculated correctly
- [ ] Trend identification matches visual chart patterns
- [ ] Overbought/oversold signals align with RSI levels (70/30 thresholds)
- [ ] Analysis updates in near real-time with new data

### Opportunity Scanning Verification
- [ ] All symbols in watchlist scanned consistently
- [ ] Opportunity scores computed using defined criteria
- [ ] Ranking correctly orders by signal strength or probability
- [ ] Scan results exported in format usable by Strategist

### Integration Verification
- [ ] Yahoo Finance data feeds correctly configured and responding
- [ ] Exa search queries return relevant market research
- [ ] Notion integration creates research log entries
- [ ] Data collection jobs scheduled and running on configured intervals

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I will cut losses later" | Later never comes. Set stop-losses before entering any trade. |
| "This time is different" | It never is. Follow your strategy, not your emotions. |
| "I do not need to journal" | Journaling reveals patterns in your behavior. Track every trade. |