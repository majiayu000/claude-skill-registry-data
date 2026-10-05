---
name: technical-quant-analysis
description: "Perform evidence-based technical and quantitative analysis from verified OHLCV data, including trend, momentum, volatility, volume, support/resistance, multi-timeframe structure, scenario levels, position risk, strategy testing, and backtest quality control. Use when the user asks for chart analysis, RSI/MACD/ATR, entry or exit timing, short-term price scenarios, stop/invalidation levels, technical screening, or whether a signal historically worked. Do not use technical indicators alone to claim certainty or replace fundamental, event, liquidity, and product-risk analysis. Turkish triggers: teknik ve nicel piyasa analizi, grafik/destek-direnç, OHLCV ve backtest."
---

# Technical Quant Analysis

Use indicators as measurements, not prophecies. Read [references/data-contract.md](references/data-contract.md), [references/interpretation.md](references/interpretation.md), and for strategy testing [references/backtest-standard.md](references/backtest-standard.md).

## Workflow

1. Verify instrument, exchange, currency, timezone, interval, data source, fetch time, delay, and corporate-action adjustment.
2. Exclude incomplete candles. Reject duplicated, unordered, non-positive, or internally inconsistent OHLCV rows.
3. Run `scripts/technical_indicators.py` on sufficient data. Do not report unavailable long-window indicators as if calculated.
4. Classify regime: trend, range, breakout, breakdown, volatility expansion/contraction, and liquidity quality.
5. Inspect price structure, moving averages, RSI, MACD, ATR, volume, gaps, and multi-timeframe agreement. Avoid indicator-count voting.
6. Express entry zone, invalidation, targets, and risk/reward as scenarios tied to confirmed levels and execution costs.
7. Combine with fundamentals, valuation, macro, catalysts, and product mechanics when the decision is an investment rather than a chart exercise.
8. For historical performance claims, require a point-in-time backtest packet and run `scripts/backtest_audit.py` before interpreting results.
9. Route cross-asset rates/inflation/FX/credit/breadth regime work to `$market-regime-analysis`; keep this skill focused on instrument data, signals and test quality.

## Hard rules

- Never calculate from a screenshot when raw dated prices can be obtained.
- Never mix adjusted and unadjusted prices across splits, dividends, rights issues, or contract rolls.
- Never use an unfinished candle to confirm a close-based signal.
- Never call overbought an automatic sell or oversold an automatic buy.
- Never optimize on the full sample and report the same sample as validation.
- Include fees, spread, slippage, taxes, latency, delistings, survivorship bias, look-ahead, and data revisions where relevant.
- Distinguish exploratory signals from independently validated strategies.

## Output

Report data timestamp and quality first, then regime, decisive levels, indicator readings, bull/base/bear paths, invalidation, modeled risk, and confidence. Say what evidence would confirm or reject the setup. Do not output a naked BUY/SELL score.
