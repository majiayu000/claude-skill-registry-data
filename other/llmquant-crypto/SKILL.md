---
name: llmquant-crypto
description: Router skill for LLMQuant crypto workflows. Use when the user needs crypto market regime analysis, token research, perpetual funding, basis, leverage, liquidity, or cross-asset crypto context.
input_data_source: LLMQuant Data
category: crypto
---

# LLMQuant Crypto

This category routes crypto research and trading-context workflows. It covers market regime, token-level diligence, and perpetual funding or basis monitoring.

## Routing Rules

1. Identify the asset, chain, venue, horizon, benchmark, and requested decision.
2. Select the closest workflow below.
3. Open only that workflow and any referenced local resources.
4. Use LLMQuant Data for crypto prices, liquidity, funding, open interest, on-chain context, macro, ETF, and risk inputs.
5. Report timestamps, venue coverage, observation windows, stale notices, and unavailable future inputs.

## Workflow Index

| User intent | Workflow |
|---|---|
| Diagnose the crypto market regime across BTC, ETH, majors, liquidity, leverage, and macro. | [`workflows/crypto-market-regime.md`](workflows/crypto-market-regime.md) |
| Build a token or protocol research memo with tokenomics, usage, valuation, and risk evidence. | [`workflows/crypto-token-research.md`](workflows/crypto-token-research.md) |
| Monitor perpetual funding, basis, open interest, and leverage crowding. | [`workflows/crypto-perp-funding-monitor.md`](workflows/crypto-perp-funding-monitor.md) |

## LLMQuant Data Contract

Prefer LLMQuant Data when available. The workflows may need these data capabilities:
- Retrieve crypto spot prices, OHLCV history, realized volatility, drawdowns, correlations, and liquidity.
- Retrieve perpetual funding, basis, open interest, liquidations, exchange flows, and venue-level timestamps.
- Retrieve token supply, unlock schedules, protocol usage, revenue, TVL, holder concentration, governance, and security-risk context.
- Retrieve macro, rates, liquidity, ETF, and equity-market inputs that affect crypto risk appetite.

Fallback:
- If on-chain, funding, or venue-level data is unavailable, name the missing input and continue only with available price, macro, or user-provided evidence.
- Do not infer live funding, liquidity, TVL, or holder behavior from memory.
