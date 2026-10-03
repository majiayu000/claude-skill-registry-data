---
name: nse-trading-toolkit
description: |
  Master orchestrator for Indian NSE/BSE equity trading analysis via Groww broker.
  Routes to specialized framework skills: technical analysis, position sizing, stop-loss,
  trailing stops, risk-reward, multi-timeframe, RSI divergence, and Fibonacci trading.

  Use this skill whenever the user asks to: analyze a stock, check a position, decide buy/sell/hold,
  plan entries/exits, or do any comprehensive trading analysis for Indian equities. Triggers on:
  "analyze [stock]", "should I buy/sell [stock]", "check [stock]", "what's the setup on [stock]",
  or any broad market analysis request involving NSE/BSE stocks. This is the go-to skill for
  full stock analysis — it pulls together all the individual framework skills into one workflow.
---

# NSE Trading Toolkit — Orchestrator

This is the master workflow that coordinates 8 specialized trading framework skills for Indian NSE/BSE equities.

## Prerequisites

All skills work standalone with zero dependencies — they're prompt-based frameworks that Claude applies during analysis. Connecting data sources makes them more powerful:

| Data Source | Required? | What It Adds | Setup |
|------------|-----------|-------------|-------|
| **Groww MCP** | Optional | Live quotes, portfolio, technical indicators, candle data, order placement | Add to `.mcp.json` (see README) |
| **yfinance** | Optional | Historical OHLCV (>6 months), backtesting | `pip install yfinance` |
| **TradingView MCP** | Optional | Crypto screening, volume scanners | See [tradingview-mcp](https://github.com/pab-s/tradingview-mcp) |

**Without any data source:** You provide prices manually, Claude applies the frameworks.
**With Groww MCP:** Claude pulls live data automatically. Use `search_stock_and_others_symbol` first to resolve the trading symbol.

### Groww MCP Tool Reference

| Tool | Use For |
|------|---------|
| `search_stock_and_others_symbol` | Find correct trading symbol |
| `get_quotes_and_depth` | Live price, volume, bid/ask depth |
| `get_historical_technical_indicators` | RSI, MACD, SMA, EMA, Bollinger, ADX, ATR |
| `fetch_historical_candle_data` | OHLCV candles (1m to 1w intervals) |
| `get_equity_portfolio_holdings` | Your current holdings and P&L |
| `get_ltp` | Quick last traded price |

### yfinance Quick Reference
```python
import yfinance as yf
data = yf.download("RELIANCE.NS", period="2y", interval="1d")  # NSE: .NS, BSE: .BO
```

## Master Workflow

Follow this sequence for a full analysis. Skip steps not relevant to the user's question.

```
1. CONTEXT    → What does the user hold? What's their goal?
2. DATA       → Pull live quotes + historical candles + indicators
3. STRUCTURE  → Multi-timeframe analysis (→ use multi-timeframe-analysis skill)
4. TECHNICALS → Chart reading, indicators (→ use technical-analysis skill)
                 RSI divergences (→ use rsi-divergence skill)
                 Fibonacci levels (→ use fibonacci-trading skill)
5. DECISION   → Buy / Sell / Hold with specific triggers
6. SIZING     → How many shares, at what risk (→ use position-sizing skill)
7. STOPS      → Initial stop-loss (→ use stop-loss-strategies skill)
                 Trailing plan (→ use trailing-stops skill)
8. TARGETS    → R:R ratio check (→ use risk-reward-ratio skill)
                 Fibonacci extensions (→ use fibonacci-trading skill)
9. PLAN       → Concrete action plan with prices and triggers
```

## When to Use Which Skill

| User's Question | Primary Skill | Supporting Skills |
|----------------|---------------|-------------------|
| "Analyze BBTC" | This orchestrator | All 8 as needed |
| "Position size for RELIANCE" | position-sizing | stop-loss-strategies, risk-reward-ratio |
| "Where to set stop-loss?" | stop-loss-strategies | technical-analysis (for S/R levels) |
| "RSI divergence on TATAMOTORS?" | rsi-divergence | technical-analysis, fibonacci-trading |
| "Fib levels for INFY" | fibonacci-trading | technical-analysis |
| "Should I trail my stop?" | trailing-stops | — |
| "Is this trade worth taking?" | risk-reward-ratio | position-sizing |
| "Weekly vs daily trend?" | multi-timeframe-analysis | technical-analysis |

## Output Format

When presenting a full analysis, use this structure:

```markdown
# [STOCK] Analysis — [Date]

## Quick Take
[1-2 sentence summary: bullish/bearish/neutral + key level to watch]

## Position (if held)
[Current holdings, avg price, P&L]

## Technical Setup
[Trend, key levels, indicator readings]

## Scenarios
[Bullish / Bearish / Sideways with probabilities]

## Action Plan
| Action | Trigger | Price | Size | Stop | Target | R:R |
|--------|---------|-------|------|------|--------|-----|

## Risk Summary
- Max risk: Rs.XXX (X% of capital)
- Stop-loss: Rs.XXX
- Trailing plan: [method]
```

## Indian Market Notes
- NSE trading hours: 9:15 AM - 3:30 PM IST
- Pre-open session: 9:00 - 9:15 AM
- T+1 settlement
- Circuit limits: 5%, 10%, 20% (varies by stock)
- STT, brokerage, GST affect actual P&L — factor ~0.1% for delivery trades
- Use BSE symbol if NSE not available
