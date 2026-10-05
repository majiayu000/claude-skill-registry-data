---
name: turkey-markets-analysis
description: Analyze Turkish financial markets using BIST, KAP, TEFAS, TCMB EVDS, TÜİK, SPK, issuer/fund/product documents, and current Türkiye-specific rules. Use for BIST equities, Turkish ETFs/certificates, TEFAS funds, TRY/FX macro effects, inflation accounting, corporate actions, VİOP, warrants, broker/bank products, or Turkish intents such as “BIST hissesi”, “TEFAS fon”, “varant/VİOP”, “TCMB faiz”, “KAP bilanço”, “TMS 29”. Apply universal fund, warrant, forecast, technical and portfolio specialists where appropriate; own Türkiye sourcing and market mechanics. Do not use for non-Turkish markets except comparison.
---

# Turkey Markets Analysis

Use official Turkish sources first and label every live figure with date, time, currency, and delay status.

Read only the relevant reference:

- BIST equity: [references/bist-equity.md](references/bist-equity.md)
- TEFAS fund: [references/tefas-funds.md](references/tefas-funds.md)
- Türkiye macro: [references/macro-regime.md](references/macro-regime.md)
- VİOP or warrants: [references/leveraged-products.md](references/leveraged-products.md)
- Source routing: [references/turkey-sources.md](references/turkey-sources.md)

## Workflow

1. Verify code, instrument class, issuer/founder, currency, and market. Stop on OCR or code ambiguity.
2. Identify whether the decision is new buy, add, hold, reduce, sell, hedge, or compare and establish the horizon.
3. For an open-ended BIST stock recommendation or alternatives request, use `$equity-opportunity-funnel` to scan the broad eligible universe and progressively deepen finalists. Do not generate a final action from a handful of familiar BIST names.
4. Gather the minimum current official evidence, then add market data and independent corroboration.
5. Normalize accounting period, consolidation basis, TMS 29 inflation treatment, corporate actions, fund category, NAV date, and benchmark.
6. Use `$public-equity-research` for deep listed-company filings, normalized financials, valuation, earnings, thesis and catalysts. It may use the installed `$public-equity-investing` plugin for narrower workflows when available but must not depend on it.
7. Use `$fund-etf-analyst` for product-level TEFAS/fund comparison, holdings overlap, fees, benchmark and portfolio role; this skill retains TEFAS/KAP/SPK sourcing and Türkiye-specific tax/settlement verification.
8. Use `$warrant-structured-product-analyst` for product-document-first listed warrant/certificate analysis; this skill retains BIST/VİOP market rules and official Turkish sources.
9. Use `$technical-quant-analysis` when price timing or chart evidence matters and `$market-regime-analysis` when cross-asset regime context matters.
10. Use `$probabilistic-market-forecast` for realistic price ranges, target probabilities, and high-upside candidate ranking.
11. Keep `scripts/fund_metrics.py` and `scripts/leveraged_scenarios.py` as compatible transparent calculation fallbacks; prefer the dedicated specialist's richer protocol when available.
12. Use `$portfolio-risk-and-sizing` for allocation/quantity and `$pre-trade-investment-gate` when the user is about to act.
13. Use `$finance-evidence-guard` before quoting a live price, NAV, fee, tax/legal rule, or current filing number.
14. Give a clear action, bear/base/bull cases, invalidation, liquidity/cost constraints, and confidence.

## Hard rules

- Do not describe Borsa İstanbul's delayed public web data as real-time.
- Do not infer a public KAP or TEFAS API merely because an unofficial scraper exists.
- Do not analyze a fund code until the exact fund is confirmed.
- Do not compare TEFAS funds from return alone; include holdings, mandate, fee, benchmark, risk, drawdown, liquidity/valuation timing, and category consistency.
- Do not compare nominal revenue or profit across high-inflation periods without checking reporting basis and real effects.
- Do not invent an exact VİOP or warrant quantity before contract terms, executable price, fees, budget, and loss boundary are verified. Until then, give a conditional shortlist, price gate and quantity formula rather than ending the analysis.
- Do not imply that a stop order guarantees the modeled loss.
- Do not reject an informed legal high-risk trade merely for being high risk. Rank the strongest setup and alternatives, quantify the full-loss or margin risk once, and provide an executable plan when inputs are available.
- Do not label a broad-screen result `AL`. A BIST equity must clear the full opportunity-funnel gate before a final buy action.

## Output

Start with action, horizon, data timestamp, and confidence. Then show the decisive evidence, valuation or fund quality, technical timing if used, macro transmission, catalysts, bear/base/bull cases, invalidation, quantity/cost, and missing evidence.
