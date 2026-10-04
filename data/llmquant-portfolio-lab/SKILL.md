---
name: llmquant-portfolio-lab
description: Router skill for LLMQuant portfolio-lab workflows. Use when the user needs portfolio exposure maps, what-if simulations, scenario states, or virtual portfolio comparisons.
input_data_source: LLMQuant Data
category: portfolio-lab
---

# LLMQuant Portfolio Lab

This category routes portfolio virtualization workflows: exposure maps, scenario states, and what-if simulations for real or hypothetical portfolios.

## Routing Rules

1. Identify portfolio ID, holdings list, benchmark, scenario, and requested visualization/output.
2. Select the closest workflow below.
3. Open only that workflow and relevant local assets/scripts.
4. Use LLMQuant Data for positions, prices, ETF look-through, factors, scenarios, and risk model outputs.
5. Report as-of dates, model dates, benchmark, missing holdings, and unsupported asset types.

## Workflow Index

| User intent | Workflow |
|---|---|
| Map portfolio exposure by holdings, sectors, factors, geography, ETF look-through, and concentration. | [`workflows/portfolio-exposure-map.md`](workflows/portfolio-exposure-map.md) |
| Simulate adds, trims, hedges, shocks, and virtual portfolio states. | [`workflows/portfolio-what-if-simulator.md`](workflows/portfolio-what-if-simulator.md) |

## LLMQuant Data Contract

Prefer LLMQuant Data when available. The workflows may need these data capabilities:
- Retrieve portfolio holdings, weights, cost basis, asset types, benchmarks, and as-of dates.
- Retrieve factor exposures, sector/geography exposures, ETF look-through holdings, risk model outputs, and scenario simulation results.
- Retrieve prices, correlations, drawdowns, volatility, option Greeks, and hedge context when relevant.
- Compare current, pro forma, and hypothetical portfolio states.

Fallback:
- If portfolio APIs are unavailable, ask for a holdings table or build a structured portfolio input template.
- Do not invent weights, holdings, factor exposures, or scenario returns.
