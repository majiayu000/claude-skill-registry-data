---
name: llmquant-commodities
description: Router skill for LLMQuant commodities workflows. Use when the user needs commodity spot, futures curve, inventory, roll yield, or macro linkage analysis.
input_data_source: LLMQuant Data
category: commodities
---

# LLMQuant Commodities

This category routes commodity research and futures-curve workflows. It defines the LLMQuant Data inputs required even when some commodity endpoints are future product surface.

## Routing Rules

1. Identify the commodity, contract codes, region, horizon, and output target.
2. Select the closest workflow below.
3. Open only that workflow and relevant local resources.
4. Use LLMQuant Data for spot, futures, inventory, macro, FX, and rate inputs.
5. Report contract dates, observation dates, source coverage, and missing inputs.

## Workflow Index

| User intent | Workflow |
|---|---|
| Build a commodity market brief across price, curve, inventory, macro, and equities. | [`workflows/commodity-market-lens.md`](workflows/commodity-market-lens.md) |
| Analyze futures term structure, roll yield, contango/backwardation, and curve shifts. | [`workflows/futures-curve-monitor.md`](workflows/futures-curve-monitor.md) |

## LLMQuant Data Contract

Prefer LLMQuant Data when available. The workflows may need these data capabilities:
- Retrieve commodity spot or front-month prices, recent changes, volume, and observation timestamp.
- Retrieve futures curves by contract month, including curve shape, roll yield, volume, and open interest.
- Retrieve inventory, production, demand, import/export, weather, and commodity event context.
- Retrieve macro indicators, rates, FX, inflation, growth, and related equity or ETF price proxies.

Fallback:
- If commodity data is not available, list the exact inputs needed and continue only with available macro, market, or user-provided evidence.
- Do not infer spot prices, inventories, or curve shape from memory.
