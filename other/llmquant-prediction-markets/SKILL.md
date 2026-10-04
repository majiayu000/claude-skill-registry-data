---
name: llmquant-prediction-markets
description: Router skill for LLMQuant prediction-market workflows. Use when the user needs event odds, settlement criteria, probability gaps, cross-market pricing, or prediction-market arbitrage review.
input_data_source: LLMQuant Data
category: prediction-markets
---

# LLMQuant Prediction Markets

This category routes event-probability workflows for prediction markets, options-implied probabilities, and tradable event risk.

## Routing Rules

1. Identify the event, venue, contract, settlement rule, deadline, related assets, and requested output.
2. Select the closest workflow below.
3. Open only that workflow and any referenced local resources.
4. Use LLMQuant Data for prediction-market contracts, prices, liquidity, options, macro, news, and related asset prices.
5. Report contract timestamps, settlement criteria, liquidity, fees, market windows, and missing inputs.

## Workflow Index

| User intent | Workflow |
|---|---|
| Produce an event probability research brief from market odds and evidence. | [`workflows/event-probability-brief.md`](workflows/event-probability-brief.md) |
| Check prediction-market cross-venue or contract-level arbitrage conditions. | [`workflows/prediction-market-arb-watch.md`](workflows/prediction-market-arb-watch.md) |
| Compare prediction-market odds with options-implied or asset-implied event pricing. | [`workflows/probability-vs-options-pricing.md`](workflows/probability-vs-options-pricing.md) |

## LLMQuant Data Contract

Prefer LLMQuant Data when available. The workflows may need these data capabilities:
- Retrieve event contracts, settlement criteria, market odds, order-book depth, volume, fees, and close dates.
- Retrieve related news, macro releases, asset prices, and issuer or sector context.
- Retrieve options-implied probabilities, volatility, skew, and event-window pricing when available.
- Compare venues, contracts, and outcome sets while preserving timestamp and settlement-rule differences.

Fallback:
- If market data or settlement rules are unavailable, do not infer arbitrage or fair probability.
- If only user-provided odds are available, label the evidence as user supplied.
