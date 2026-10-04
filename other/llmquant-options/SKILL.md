---
name: llmquant-options
description: Router skill for LLMQuant options workflows. Use when the user needs IV rank, option scoring, strategy construction, Greeks, P&L simulation, volatility surface, unusual activity, earnings IV crush, backtests, or hedges.
input_data_source: LLMQuant Data
category: options
---

# LLMQuant Options

This category routes option, volatility, hedge, and options-backtest workflows.

## Routing Rules

1. Identify ticker, expiration, strikes, direction, horizon, risk budget, and strategy constraints.
2. Select the closest workflow below.
3. Open only the selected workflow and relevant scripts/assets.
4. Use LLMQuant Data for prices, option chains, IV history, Greeks, option flow, earnings, and event inputs.
5. Report timestamps, contract metadata, data windows, assumptions, stale notices, and missing inputs.

## Workflow Index

| User intent | Workflow |
|---|---|
| Evaluate whether implied volatility is cheap or expensive versus history. | [`workflows/iv-rank.md`](workflows/iv-rank.md) |
| Score and rank option contracts. | [`workflows/options-score.md`](workflows/options-score.md) |
| Build a multi-leg option strategy from a market view. | [`workflows/options-strategy.md`](workflows/options-strategy.md) |
| Calculate and interpret option Greeks. | [`workflows/greeks-dashboard.md`](workflows/greeks-dashboard.md) |
| Simulate option P&L, breakevens, and stress scenarios. | [`workflows/pnl-simulator.md`](workflows/pnl-simulator.md) |
| Analyze IV across strikes and expirations. | [`workflows/volatility-surface.md`](workflows/volatility-surface.md) |
| Analyze single-expiry skew and smile shape. | [`workflows/volatility-smile.md`](workflows/volatility-smile.md) |
| Detect and interpret unusual options activity. | [`workflows/unusual-activity.md`](workflows/unusual-activity.md) |
| Analyze earnings implied moves and IV crush. | [`workflows/earnings-iv-crush.md`](workflows/earnings-iv-crush.md) |
| Backtest bull put spread signal rules versus controls. | [`workflows/bull-put-spread-backtest.md`](workflows/bull-put-spread-backtest.md) |

## LLMQuant Data Contract

Prefer LLMQuant Data when available. The workflows may need these data capabilities:
- Retrieve option chains with expirations, strikes, bid/ask, volume, open interest, and implied volatility.
- Retrieve IV history, IV rank, IV percentile, term structure, skew, and volatility surface data.
- Retrieve Greeks, option flow, unusual activity, strategy backtest inputs, and earnings/event calendars.
- Retrieve underlying equity prices, realized volatility, drawdowns, and liquidity context.

Fallback:
- If option data is missing, state the exact chain, IV, Greek, flow, or backtest input needed.
- If LLMQuant Data or a compatible data MCP is unavailable, ask for option chain exports or user-provided pricing tables.
- Do not fabricate option quotes, IV, open interest, or Greeks.
