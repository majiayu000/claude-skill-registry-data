---
name: market-regime-analysis
description: Classify and explain the current market regime across trend, volatility, breadth, liquidity, rates, inflation, FX, credit, earnings revisions, positioning, correlations, and dated policy/event risk, then map it to asset and strategy sensitivities. Use for macro allocation, risk-on/risk-off, timing context, cross-asset comparisons, or Turkish intents such as “piyasa rejimi”, “risk-on risk-off”, “şu an hangi varlık avantajlı”, “faiz-enflasyon-borsa ilişkisi”, “volatilite ve genişlik”, “makro ortamı analiz et”. A regime label is context, not a standalone buy/sell signal or deterministic forecast.
---

# Market Regime Analysis

Own the cross-asset environment, not the final security recommendation. Use current primary data and distinguish measurement from interpretation.

Read [references/regime-protocol.md](references/regime-protocol.md). Use `scripts/regime_features.py` for transparent price/volatility/breadth features when compatible dated data exists.

## Workflow

1. **Define scope.** Establish geography, asset universe, currency, horizon and data cutoff. A daily trading regime and a multi-year macro regime are different questions.
2. **Collect current measures.** Use official central-bank/statistics data for rates, inflation, labor and activity; exchange/primary market data for prices, breadth and liquidity; dated filings/estimates for earnings and credit when relevant.
3. **Measure independent axes.** Report trend, realized/implied volatility, breadth, liquidity/funding, rates/yield curve, inflation/growth direction, FX, credit, earnings revisions and event calendar separately before assigning a label.
4. **Check disagreement.** Highlight mixed regimes such as index strength with weak breadth, falling inflation with tightening liquidity, or calm volatility with concentrated event risk.
5. **Compare history carefully.** Use matched historical episodes as base rates, not templates. State sample, differences, data vintage and whether the current regime is outside the observed range.
6. **Map transmission.** Explain which assets, sectors, durations, currencies, factors and strategies are helped or hurt, and through what mechanism. Separate first-order from second-order effects.
7. **Build transitions.** Give base, improvement and deterioration paths with observable triggers, not a permanent one-word label.
8. **Route action.** Send instrument timing to `$technical-quant-analysis`, outcome ranges to `$probabilistic-market-forecast`, portfolio exposure to `$portfolio-risk-and-sizing`, and final decisions to `$investment-copilot`.

## Hard rules

- Do not reduce the regime to one index, indicator, headline or “risk-on/off” label.
- Do not use revised macro data as if it was known in historical real time.
- Do not infer causality from a recent correlation.
- Do not assume correlations, liquidity or policy transmission stay stable under stress.
- Do not issue a naked BUY/SELL solely from regime classification.

## Output

Lead with scope, cutoff and a one-sentence regime assessment. Then show the axis dashboard, conflicts, historical base-rate limits, asset/strategy transmission, transition triggers, key dated events, implications for the requested horizon and confidence.
