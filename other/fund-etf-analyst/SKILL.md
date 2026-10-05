---
name: fund-etf-analyst
description: Analyze and compare mutual funds, ETFs, index funds, money-market funds, pension funds, and TEFAS products using exact identity, mandate, benchmark, holdings, look-through overlap, fees/tax, NAV versus market price, liquidity, drawdown, factor exposures, and category-consistent alternatives. Use for fund/ETF buy-hold-sell decisions, portfolio fund selection, “best fund” or “which fund” requests, and Turkish intents such as “fon alınır mı”, “hangi fon daha iyi”, “TEFAS fon karşılaştır”, “ETF mi fon mu”, “fon dağılımı” and “fonu satayım mı”. Do not rank by trailing return alone or treat a fund code as verified identity.
---

# Fund and ETF Analyst

Own product-level fund analysis. Use the user's language, explain unfamiliar terms once, and keep the recommendation conditional on current documents and prices.

Read [references/fund-analysis-protocol.md](references/fund-analysis-protocol.md). Use `scripts/fund_metrics.py` when dated NAV or adjusted-price data is available.

## Workflow

1. **Resolve identity.** Confirm full name, code/ISIN, share class, domicile, currency, founder/sponsor, manager, venue, distribution/accumulation policy, investor eligibility and whether the product is an open-end fund, ETF, closed-end fund or pension product.
2. **Resolve the decision.** Establish new buy/add/hold/reduce/sell/compare, horizon, liquidity need, tax residence when relevant, current allocation and the role the product should fill.
3. **Verify current facts.** Use the official fund page, prospectus/investor document, latest holdings report and benchmark definition. For TEFAS/KAP/SPK facts, also use `$turkey-markets-analysis`. Apply `$finance-evidence-guard` to current NAV, market price, fee, tax, cutoff or settlement claims.
4. **Normalize history.** Detect mandate, benchmark, manager, category, merger and share-class changes before comparing returns. Do not back-project today's label over an incompatible history.
5. **Measure net outcomes.** Calculate total/annualized return, volatility, maximum drawdown, recovery, Sharpe/Sortino and, when a compatible benchmark exists, tracking error, information ratio and upside/downside capture. State data frequency, risk-free input and missing costs.
6. **Look through exposures.** Analyze holdings concentration, issuer and fund-family overlap, sector, country, currency, duration, credit, commodity, derivative and cash exposure. Distinguish manager skill from factor beta and a one-off favorable regime.
7. **Check implementation.** For ETFs include bid/ask, volume/depth, premium/discount, creation/redemption and market hours. For open-end funds include NAV timing, dealing cutoff, settlement, valuation lag, gates and minimums.
8. **Compare fairly.** Use the declared benchmark, a category peer and a simple low-cost alternative on the same currency, horizon and net-of-fee basis. Compare portfolio role, not just headline return.
9. **Decide.** Return `BUY / ADD / HOLD / REDUCE / SELL / WATCH` or localized equivalents with an allocation range, entry/review conditions, invalidation and confidence. Use `$portfolio-risk-and-sizing` for portfolio fit and `$investment-red-team` for consequential choices.

## Hard rules

- Past performance, star ratings, popularity and one-year league tables are not forecasts.
- Never mix NAV return with ETF market-price return without labeling the difference.
- Never compare different currency, leverage, duration, benchmark or tax exposures as if they were peers.
- Never infer holdings from a fund name; use the latest dated disclosure and record the reporting lag.
- Do not present a management fee as total investor cost when other expenses, spread, tax or transaction charges matter.
- If identity or current documents are unresolved, provide a conditional comparison checklist rather than a fabricated recommendation.

## Output

Lead with action, intended portfolio role, horizon, data cutoff and confidence. Then show identity, mandate/benchmark, cost, net performance and drawdown, look-through exposure/overlap, liquidity/settlement, main alternatives, bear/base/bull conditions, allocation range, invalidation and missing evidence.
