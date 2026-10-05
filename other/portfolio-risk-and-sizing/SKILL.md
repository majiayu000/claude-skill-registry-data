---
name: portfolio-risk-and-sizing
description: Analyze portfolio concentration, position size, issuer/fund look-through overlap, sector/country/currency/rate/factor exposure, liquidity, leverage, correlation fragility, scenario loss, drawdown budget, and add-trim-hedge constraints. Use for portfolio reviews, allocation and rebalancing, “how much should I buy”, concentration or diversification questions, and Turkish intents such as “portföyümü analiz et”, “kaç lot/adet”, “yüzde kaç ayırayım”, “risk dağılımı”, “çok mu yoğunlaştım”, “fonlar çakışıyor mu”. Do not optimize from unstable estimates by default or claim diversification from the number of tickers alone.
---

# Portfolio Risk and Sizing

Own holdings-level risk and the maximum defensible size of a proposed action. Do not decide whether an instrument is attractive; consume thesis and scenario inputs from the relevant analyst.

Read [references/portfolio-risk-protocol.md](references/portfolio-risk-protocol.md). Use `scripts/portfolio_exposure.py` for transparent exposure and scenario aggregation when a structured packet exists. For a single ordinary long cash position, `$investment-copilot` may also use its position-sizer script.

## Workflow

1. **Freeze the snapshot.** Record timestamp, base currency, portfolio NAV, cash, every position, market value, direction, cost basis when relevant, account constraints and data gaps. Do not silently reuse an old portfolio.
2. **Resolve objective and loss budget.** Separate emergency/near-term liquidity, core capital and disposable speculative capital. Establish horizon, maximum portfolio drawdown or loss budget and any legal/account restrictions.
3. **Look through labels.** Aggregate issuer, fund, sector, country, currency, duration, credit, commodity, style/factor and strategy exposures. Use dated fund holdings and state their lag. Count economic exposure, not ticker count.
4. **Measure concentration.** Report largest positions, gross/net exposure, concentration by cluster, employer/household correlation, illiquid exposure and hidden leverage/derivatives. Show both direct and look-through views.
5. **Stress scenarios.** Apply coherent shocks to holdings and correlated clusters. Include gap, volatility, spread, FX/rate, liquidity and catalyst cases. Keep scenario loss separate from a statistically estimated confidence interval.
6. **Assess liquidity.** Estimate days to exit only from verified market value, average daily traded value and a stated participation rate. Flag settlement, fund gates, lockups, market-maker and borrow risks.
7. **Size the action.** Compute budget-limited, risk-limited, concentration-limited and liquidity-limited quantities; choose the smallest valid amount and round down to the product lot. Account for fees, spread, slippage, gap and full-loss cases.
8. **Recommend the portfolio action.** Return add/hold/trim/exit/hedge/watch with size range, binding constraint, scenario loss, review trigger and confidence. Run `$pre-trade-investment-gate` before a consequential order decision.

## Hard rules

- More holdings do not guarantee diversification when exposures overlap.
- Do not assume historical correlations, volatility or liquidity remain stable in stress.
- Do not treat a stop as a guaranteed maximum loss.
- Do not size a leveraged, short, option, warrant or crypto position with ordinary cash-equity loss math.
- Do not produce a precise quantity without verified price, lot, costs, loss boundary and product mechanics.
- Never connect to or rebalance a brokerage account.

## Output

Lead with portfolio status and the binding risk. Then show snapshot/cutoff, NAV and cash, top direct and look-through concentrations, gross/net and liquidity, scenario losses, size limits, proposed add/trim/hedge action, invalidation/review triggers, missing inputs and confidence.
