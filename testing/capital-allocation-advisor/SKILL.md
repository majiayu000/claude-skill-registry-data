---
name: capital-allocation-advisor
description: Ranks competing uses of capital (reinvest in the core, M&A, debt paydown, buyback, dividend, cash buffer) by value creation, scoring each on its return spread over cost of capital subject to leverage, liquidity, and covenant constraints. Triggers on "capital allocation", "use of cash", "deploy capital", "buyback vs debt", "where to invest excess cash", "reinvest or return", "allocation framework", "capital plan".
---
# Capital Allocation Advisor

## When to use
Use when the CFO must decide how to deploy available capital across competing uses and wants the choices ranked by value creation with the logic exposed. Typical triggers:
- An annual capital plan or capital-return policy review.
- A windfall, refinancing, or asset-sale event that frees up cash.
- A board discussion on buyback versus dividend versus debt paydown.
- A "what should we do with the cash" or "reinvest or return" question.
This is portfolio-of-uses allocation across the whole capital base. It is not the standalone valuation of one acquisition target.

## What it produces
A ranked capital-allocation table that lists each use of capital, its estimated marginal return, the cost-of-capital hurdle it clears or fails, the spread between the two, the constraints it touches, and a strategic-fit note. It ends with a recommended allocation of the available pool and the conditions that would change the ranking.

## Method
1. Size the allocable pool. Only surplus capital is allocable.
   - Available capital = beginning cash + projected free cash flow over the horizon - minimum operating cash - committed outflows (debt maturities, earn-outs, contracted capex).
   - State the horizon (typically the next 12 to 24 months) and keep the minimum cash floor explicit.
2. Set the common hurdle. Estimate WACC:
   - WACC = (E / V) x cost of equity + (D / V) x after-tax cost of debt.
   - After-tax cost of debt = pre-tax rate x (1 - tax rate).
   - E and D are market values of equity and debt; V = E + D. Use WACC as the shared hurdle unless a use has its own natural benchmark.
3. Estimate the marginal return on each use of capital:
   - Reinvest in the core: project ROIC = after-tax operating profit from the investment / invested capital. Spread = ROIC - WACC.
   - M&A (bolt-on): post-synergy ROIC = (acquired operating profit + run-rate synergies) x (1 - tax rate) / (purchase price + integration cost). Spread = post-synergy ROIC - WACC. Haircut synergies for execution risk.
   - Debt paydown: return = after-tax interest rate retired = pre-tax coupon x (1 - tax rate). Compare to WACC, and value it primarily as risk reduction and added covenant headroom.
   - Buyback: return bought back = earnings yield = EPS / share price, or FCF yield = FCF per share / share price. Spread = earnings yield - cost of equity. State clearly that buying back above intrinsic value destroys value regardless of the optical EPS accretion.
   - Dividend or dividend increase: treat as return of capital at the cost of equity; value is in payout policy and signaling, not in a positive spread.
   - Cash buffer: opportunity cost = WACC - after-tax yield on cash; justified by liquidity insurance and optionality, not by a positive spread.
4. Apply constraints as hard gates, not preferences. Test each use against:
   - The leverage target (for example a net debt / EBITDA ceiling).
   - The minimum liquidity floor.
   - Covenant headroom (leverage covenant, fixed-charge or interest-coverage covenant).
   - Any credit-rating threshold the company commits to hold.
   Any use that would breach a gate is capped or removed before ranking, not ranked and then waved through.
5. Rank by spread over cost of capital. Order surviving uses by spread, highest first.
6. Break ties on strategic fit. Where spreads are close, prefer the use with the more durable advantage, more optionality, and more reversibility, and consider timing of the cash need.
7. Recommend an allocation of the pool across the top uses, respecting every gate, and stop allocating once the marginal spread turns negative. Show the resulting ending leverage and liquidity.
8. State what would change the ranking. Name the two or three inputs (WACC, valuation, covenant reset, leverage target, a new core project) and the trigger values at which the order flips.

Common pitfalls to avoid:
- Ranking a use that breaches a gate, then "noting" the breach. Gate first, rank second.
- Comparing a buyback's optical EPS accretion to a project ROIC. Compare returns on a like-for-like basis: spread over the relevant cost of capital.
- Counting the full cash balance as allocable. Subtract the minimum operating cash and committed outflows first.
- Treating debt paydown as automatically low-value. Even when its after-tax return is below WACC, the covenant headroom and risk reduction can be the binding reason to do it.
- Double-counting synergies in M&A returns without an execution haircut and without integration cost in the denominator.

## Inputs
Gather: cash balance and FCF forecast, minimum operating cash, the debt schedule (balances, coupons, maturities, covenants), current and target leverage, tax rate, capital-structure weights and cost of equity (or beta plus risk-free and market inputs to derive it), candidate projects with expected returns and invested capital, any M&A pipeline with price and synergy estimates, share price and share count, and current dividend policy. Ask for any missing item; never invent a coupon, valuation, or synergy figure.

## Output format
1. Pool summary: available capital, minimum cash floor, committed outflows, horizon.
2. Hurdle: WACC with its components (cost of equity, after-tax cost of debt, weights).
3. Ranked table: columns = Use of Capital, Marginal Return, Hurdle, Spread, Constraint Touched, Strategic Fit, Rank.
4. Recommended allocation: amount and percent of pool to each selected use, with resulting ending leverage and liquidity.
5. Sensitivity note: the inputs that would re-rank the list and the trigger values.

## Quality bar
- The recommended allocation sums to the available pool and to 100 percent; nothing is allocated past a constraint gate.
- After-tax cost of debt and project ROIC use consistent after-tax, pre-financing definitions; no mixing of pre-tax and after-tax returns.
- Buyback return is explicitly tied to current valuation, with the value-destruction-above-intrinsic-value caveat stated.
- Resulting leverage and liquidity after the recommendation are shown and respect the stated targets.
- Assumptions (WACC, tax rate, target leverage) and the trigger points that would change the ranking are stated; no fabricated benchmarks.

## Example
Input (hypothetical): allocable pool 100, WACC 9%, tax rate 25%, net debt / EBITDA target ceiling 2.5x (currently 1.8x). Core reinvestment ROIC 16%; debt eligible for paydown carries a 7% coupon; buyback earnings yield 6% against cost of equity 11%.
Output snippet:
- Ranked (1) Reinvest core: return 16%, hurdle 9%, spread +7.0%, no gate breached, fit high.
- Ranked (2) Debt paydown: after-tax return 5.25%, spread -3.75% vs WACC but adds covenant headroom, fit medium.
- Ranked (3) Buyback: earnings yield 6% vs cost of equity 11%, spread -5.0%, value-dilutive at current price, fit low.
- Recommendation: 70 to core reinvestment, 30 to debt paydown (leverage falls toward 1.5x); defer buyback until earnings yield clears cost of equity. Trigger: if a second core project at ROIC above 9% appears, shift the 30 from debt to that project. All figures hypothetical.
