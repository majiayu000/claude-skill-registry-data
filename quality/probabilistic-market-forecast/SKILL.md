---
name: probabilistic-market-forecast
description: "Estimate realistic price/return distributions, target and downside probabilities, and probability-weighted scenarios for stocks, funds/ETFs, futures, warrants, crypto, commodities, FX, and portfolios; freeze and score forecasts after maturity. Use for how much/when an instrument may rise or fall, highest realistic upside, target odds, or Turkish intents such as ‘ne kadar yükselir/düşer’, ‘kaç günde/ayda’, ‘en çok ne artar’, ‘hedefe ulaşma ihtimali’, ‘ayı-baz-boğa’, ‘olasılıklı fiyat tahmini’, and ‘tahminlerin ne kadar tuttu’. Compare against naive/market benchmarks and calibration; never claim single-point certainty or guaranteed accuracy."
---

# Probabilistic Market Forecast

Forecast a distribution, not a story. Give the user the most realistic actionable estimate the evidence supports, including high-risk opportunities when requested.

Read [references/forecast-method.md](references/forecast-method.md) and [references/calibration.md](references/calibration.md).

## Workflow

1. Resolve instrument, venue, currency, current executable price, data timestamp, horizon and target event.
2. For an open-ended “which stock has the best upside?” request, use `$equity-opportunity-funnel` first and forecast only the properly shortlisted finalists. Do not rank a few convenient tickers and imply a market-wide search.
3. Obtain adjusted point-in-time history and enough observations for the horizon. Measure volatility, drawdowns, skew, gaps, liquidity and regime dependence.
4. Run `scripts/forecast_ranges.py` for a transparent parametric range and, when a history CSV is available, empirical rolling-horizon base rates.
5. Add current information that a pure price model misses:
   - Fundamentals, valuation and what is priced in
   - Earnings, legal, policy, unlock or other dated catalysts
   - Macro and sector regime
   - Technical structure and volatility regime
   - Bid/ask, depth, funding, time decay and product mechanics
6. Build bear, base and bull cases with conditional probabilities. Use an event mixture when a catalyst makes the return distribution discontinuous.
7. Shrink uncertain drift toward zero or the relevant benchmark, especially at short horizons. Let volatility dominate when evidence for directional edge is weak.
8. Compare candidates using probability-weighted return, probability of loss, tail loss, liquidity, catalyst and invalidation—not maximum theoretical upside alone.
9. Freeze the forecast before the outcome with record ID, issue time, source cutoff, maturity rule, horizon, quantiles/probabilities, model/version, assumptions and declared naive/market benchmark. Never overwrite it after the cutoff.
10. Score matured records with `scripts/score_forecasts.py --strict`. Review Brier score, ranked probability score where categorical, quantile coverage/pinball loss, calibration bins and skill versus the declared benchmark. Tighten or widen future confidence only after a sufficiently large comparable sample.

## Required forecast

Return:

- Current price, source, timestamp and delay
- Horizon and model/data cutoff
- P10, P25, P50, P75 and P90 price or return ranges
- Probability of reaching the user's target
- Probability of losing more than the stated threshold
- Bear/base/bull scenarios and conditions
- Expected return range and tail-risk caveat
- Entry gate, invalidation, size input and monitoring trigger
- Confidence level and which evidence most changes the estimate
- Declared benchmark and a record key that permits later no-hindsight scoring

Use rounded ranges that match evidence quality. Do not print fake precision from a fragile model.

## High-risk requests

- Do not replace the forecast with “do not invest.” If the user accepts the full stated loss, show the strongest positive-asymmetry setup and alternatives.
- Explicitly distinguish `highest possible upside` from `highest probability-weighted upside` and recommend from the latter unless the user asks for a lottery-like payoff.
- For lottery-like requests, show probability of near-total loss and break-even probability, then provide the best structured candidate if a defensible one exists.
- If no positive edge is detectable, say `no edge`; if the user still wants a trade, provide the least-bad conditional setup and label it accurately.

## Model limits

Historical and lognormal ranges understate some event, liquidity and leverage tails. Warrants require time, implied volatility, delta, ratio and issuer quotes; futures require margin and mark-to-market; funds use dated NAV rather than intraday execution. Never map an underlying forecast mechanically to a derivative return without product-specific modeling.
