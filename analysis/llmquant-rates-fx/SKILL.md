---
name: llmquant-rates-fx
description: Router skill for LLMQuant rates and FX workflows. Use when the user needs yield curve, duration, central-bank divergence, FX carry, real-rate, dollar, or cross-currency analysis.
input_data_source: LLMQuant Data
category: rates-fx
---

# LLMQuant Rates FX

This category routes rates and foreign-exchange workflows for curve analysis, central-bank divergence, and FX carry.

## Routing Rules

1. Identify currencies, countries, curve points, instrument proxy, horizon, and decision type.
2. Select the closest workflow below.
3. Open only that workflow and any referenced local resources.
4. Use LLMQuant Data for yield curves, policy rates, inflation, growth, FX prices, carry, volatility, credit, commodities, and macro context.
5. Report observation dates, price timestamps, policy dates, curve tenors, stale notices, and missing inputs.

## Workflow Index

| User intent | Workflow |
|---|---|
| Analyze yield curve shape, duration exposure, and curve trades. | [`workflows/yield-curve-trade-lens.md`](workflows/yield-curve-trade-lens.md) |
| Compare central-bank paths and macro divergence across countries. | [`workflows/central-bank-divergence.md`](workflows/central-bank-divergence.md) |
| Build an FX carry, momentum, valuation, and risk dashboard. | [`workflows/fx-carry-dashboard.md`](workflows/fx-carry-dashboard.md) |

## LLMQuant Data Contract

Prefer LLMQuant Data when available. The workflows may need these data capabilities:
- Retrieve nominal and real yield curves, policy rates, inflation expectations, rate histories, and term-premium context.
- Retrieve FX spot history, carry, forward points, rate differentials, volatility, positioning, and trade-weighted dollar context.
- Retrieve central-bank meeting calendars, policy communication, macro indicators, commodities, credit, and risk sentiment.
- Retrieve portfolio duration, currency exposures, ETF look-through, and hedging instruments when available.

Fallback:
- If forward points, real rates, or positioning are unavailable, state the missing inputs and use spot/rate-differential evidence only.
- Do not infer live FX carry or curve trades without timestamped rate and FX data.
