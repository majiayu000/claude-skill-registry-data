---
name: warrant-structured-product-analyst
description: Analyze listed warrants, certificates, turbos, and related structured products from the official product terms, executable quote, underlying distribution, strike/barrier, expiry, conversion convention, settlement, market maker, spread, liquidity, time decay, implied volatility, Greeks, effective gearing, break-even, and total-loss scenarios. Use for “which warrant”, warrant quantity/return/risk, call-put comparisons, or Turkish intents such as “varant alınır mı”, “hangi varant”, “varant kaç adet”, “dayanak yüzde 10 artarsa varant ne olur”, “kullanım fiyatı/vade/dönüşüm oranı”. Never infer a fixed return from the underlying move or treat indicative model value as an issuer quote.
---

# Warrant and Structured Product Analyst

Own product mechanics and translation from an underlying scenario to the exact listed product. Use `$probabilistic-market-forecast` for the underlying distribution and `$finance-evidence-guard` for current terms and quotes.

Read [references/product-protocol.md](references/product-protocol.md). Use `scripts/warrant_model.py` only for a plain European option-like payoff after confirming its inputs and limitations.

## Workflow

1. **Resolve exact product.** Verify code/ISIN, issuer, venue, currency, product family, underlying, call/put or long/short direction, strike, barrier/knock-out when any, expiry, exercise/settlement, conversion convention, corporate-action terms and official product document.
2. **Verify execution.** Record bid, ask, quote time/delay, market-maker presence, spread, depth/size when available, trading hours, minimum lot, fees, settlement and any issuer credit exposure.
3. **Separate payoff types.** Determine whether the product is a plain warrant, capped/callable certificate, turbo/knock-out, quanto, basket or another structure. Do not apply Black-Scholes or vanilla intrinsic formulas to a non-vanilla payoff.
4. **Model the underlying first.** Build dated bear/base/bull underlying distributions with catalysts and tail events. Do not start from the user's desired warrant return.
5. **Translate product mechanics.** For a verified plain European payoff, show intrinsic value, time value, break-even at expiry, delta, theta, vega, effective gearing and a grid across underlying price, time and volatility. Label theoretical values as indicative, not executable.
6. **Stress failure paths.** Include flat-underlying decay, adverse volatility change, widening spread, market-maker interruption, gap/barrier event, issuer/counterparty risk, corporate-action adjustment and near-total/total loss.
7. **Compare structures.** Compare at least one alternative expiry/strike or the cash underlying using the same horizon, budget and loss cap. Prefer probability-weighted payoff and execution quality over maximum advertised gearing.
8. **Size.** Require executable ask, lot size, budget, maximum acceptable loss, fees and product terms. Cap speculative capital explicitly and round down. Use `$portfolio-risk-and-sizing` and finalize through `$pre-trade-investment-gate`.

## Hard rules

- A 10% underlying move never implies a fixed warrant percentage return.
- Do not use a leverage/effective-gearing snapshot as a constant across price, time or volatility.
- Expiry intrinsic value and pre-expiry market price are different outputs.
- Issuer quotation policy and the product document override a generic model.
- A long warrant may expire worthless; other structures can contain barrier, settlement or issuer risks not captured by premium loss alone.
- Never invent a quantity from stale last price or unresolved conversion terminology.

## Output

Lead with `BUY / SPECULATIVE BUY / WATCH / NO ACTION` or localized action, horizon, quote time and confidence. Then show verified identity/terms, bid-ask and cost, underlying bear/base/bull cases, product scenario grid, break-even, time/volatility sensitivity, maximum loss, alternative product, quantity/allocation gate, invalidation and missing evidence.
