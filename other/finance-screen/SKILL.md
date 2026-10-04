---
name: finance-screen
description: Investment screener with pre-built strategies (Dividend Growth, 3-Fund Index, Bond Allocation, REITs, International Diversification, ESG) and custom criteria support. Returns curated ticker lists, allocation models, expected returns, expense ratios, and a recommended portfolio with rebalancing notes. Output saved as FINANCE-SCREEN.md.
---

# /finance screen — Investment Screener

**DISCLAIMER: For educational/informational purposes only. Not financial advice. This is not a recommendation to buy any specific security.**

## Purpose

Help the user build or refine an investment portfolio using proven, evidence-based screens. Output is a model portfolio with specific ticker examples, allocation weights, and expected behavior — not a buy/sell recommendation.

## When To Trigger

- User types `/finance screen <strategy>` or `/finance screen` (then prompts for strategy)
- User asks "what should I invest in?", "build me a portfolio", "what ETFs for X?", "low cost index fund portfolio"
- User wants to add diversification to existing holdings

## Pre-Built Screens

### 1. Dividend Growth Screen
**Goal:** Companies with rising dividends, sustainable payout ratios, durable moats.

**Criteria:**
- 10+ consecutive years of dividend increases (Dividend Aristocrats / Achievers)
- Payout ratio < 60%
- Free cash flow growth > 5%/yr
- Dividend yield 2-5%
- Debt-to-equity < 1.5

**Representative Holdings:**
- JNJ, PG, KO, PEP, MMM (Dividend Aristocrats)
- VIG (Vanguard Dividend Appreciation ETF, expense ratio 0.06%)
- SCHD (Schwab US Dividend Equity, 0.06%)
- DGRO (iShares Core Dividend Growth, 0.08%)

**Expected:** 8-10% annualized total return, 2-3% yield, lower volatility than S&P 500.

### 2. Three-Fund Index Portfolio (Bogleheads)
**Goal:** Maximum diversification, lowest cost, set-and-forget.

**Allocation (age-based):**
- US Total Stock Market: (110 - age)% * 0.6
- International Total Stock: (110 - age)% * 0.4
- US Total Bond Market: age%

**Example for age 35:** 45% US stocks / 30% International / 25% Bonds

**Representative Holdings:**
- VTI (Vanguard Total Stock, 0.03%) or FSKAX
- VXUS (Vanguard Total International, 0.07%) or FTIHX
- BND (Vanguard Total Bond, 0.03%) or FXNAX

**Expected:** 7-9% annualized real return, broad market exposure, near-zero idiosyncratic risk.

### 3. Bond Allocation Screen
**Goal:** Stability, income, ballast against equity drawdowns.

**Sub-allocation:**
- Total US Bond Market (intermediate): 50%
- Treasury Inflation-Protected (TIPS): 20%
- Short-term Treasuries (cash buffer): 15%
- High-yield corporate (small allocation, optional): 10%
- International bonds (USD-hedged): 5%

**Representative Holdings:**
- BND, AGG (total bond market)
- VTIP, SCHP (TIPS)
- VGSH, SHY (short-term Treasury)
- JNK, HYG (high yield — flag as higher risk)
- BNDX (international bonds, USD-hedged)

**Expected:** 3-5% annualized return, low correlation to equities, downside protection.

### 4. Real Estate (REITs)
**Goal:** Real estate exposure without owning property; inflation hedge; income.

**Allocation:** Cap REIT exposure at 5-15% of portfolio.

**Representative Holdings:**
- VNQ (Vanguard Real Estate, 0.12%)
- SCHH (Schwab US REIT, 0.07%)
- REET (iShares Global REIT, 0.14%)
- O (Realty Income — individual stock, monthly dividend)

**Sub-sectors to consider:**
- Residential, Industrial (data centers, logistics), Healthcare, Self-Storage

**Expected:** 7-9% return, 3-4% yield, sensitive to interest rates.

### 5. International Diversification
**Goal:** Reduce home-country bias; capture global growth.

**Allocation:**
- Developed International (Europe, Japan, Asia-Pac): 60% of international sleeve
- Emerging Markets: 30%
- International Small-Cap: 10%

**Representative Holdings:**
- VEA, IXUS (Developed International)
- VWO, IEMG (Emerging Markets)
- VSS (International Small-Cap)

**Rule of thumb:** 30-40% of equity sleeve in international.

**Expected:** 6-9% return, higher volatility from currency + EM exposure.

### 6. ESG / Sustainable
**Goal:** Environmental, social, governance screen; align portfolio with values.

**Representative Holdings:**
- ESGV (Vanguard ESG US Stock, 0.09%)
- VSGX (Vanguard ESG International, 0.12%)
- ESGD (iShares ESG Developed Markets, 0.20%)
- SUSL (iShares MSCI USA ESG Leaders, 0.15%)

**Caveats to flag:**
- ESG definitions vary; check fund methodology
- Some ESG funds underweight energy, may underperform during energy bull runs
- Expense ratios higher than vanilla index funds

**Expected:** Returns close to broad index minus 0.1-0.3%/yr; tracking error.

## Custom Screen

If user specifies custom criteria, accept inputs like:
- Sector preference (tech, healthcare, energy, etc.)
- Geographic focus (US only, ex-US, emerging)
- Factor tilts (value, growth, momentum, quality, small-cap)
- Yield target (e.g., "3%+ dividend yield")
- Expense ratio cap (e.g., "under 0.20%")
- Risk tolerance (conservative / moderate / aggressive)
- ESG requirements

Combine with relevant pre-built screens and provide a customized allocation.

## Required Inputs

1. **Strategy choice** (one of the 6 above, or "custom")
2. **Investable amount** (lump sum or monthly contribution)
3. **Time horizon** (years until needed)
4. **Risk tolerance** (1-10 scale or conservative/moderate/aggressive)
5. **Age** (for age-based allocations)
6. **Account type** (taxable / IRA / Roth / 401k — affects tax efficiency choices)
7. **Existing holdings** (to avoid overlap and surface concentration)

## Output Format

Save to `FINANCE-SCREEN.md`.

```markdown
# Investment Screen: [Strategy Name]

**Generated:** [Date]
**Investable Capital:** $X (lump) + $Y/mo
**Time Horizon:** [N] years
**Risk Profile:** [Conservative / Moderate / Aggressive]
**Account Type:** [Taxable / IRA / Roth / 401k]

> **DISCLAIMER:** For educational/informational purposes only. Not financial advice. Not a recommendation to buy any specific security. Always consult a licensed financial advisor.

---

## Strategy Summary

[2-3 sentence description of the strategy, philosophy, evidence base]

## Recommended Allocation

| Asset Class | Weight | Vehicle | Expense Ratio | Example Ticker |
|-------------|--------|---------|---------------|----------------|
| US Stocks   | X%     | ETF     | 0.03%         | VTI            |
| International | X%   | ETF     | 0.07%         | VXUS           |
| Bonds       | X%     | ETF     | 0.03%         | BND            |
| ...         |        |         |               |                |

**Total Expense Ratio (weighted):** X.XX%
**Annual Cost on $100K:** $XX

## Dollar Allocation

If investing $X today:
| Holding | Amount | Shares (approx) |
|---------|--------|-----------------|
| VTI     | $X     | Y               |
| ...     |        |                 |

## Expected Behavior

| Metric | Estimate |
|--------|----------|
| Expected annual return | X-Y% |
| Expected volatility (std dev) | X% |
| Max drawdown (historical) | -X% |
| Expected dividend yield | X% |
| Correlation to S&P 500 | X.XX |

## Tax Efficiency Notes

- [Which holdings belong in taxable vs tax-advantaged accounts]
- [Tax-loss harvesting candidates]
- [Foreign tax credit considerations for international]
- [Qualified dividends vs ordinary income]

## Rebalancing Rules

- **Frequency:** Annually, or when any allocation drifts >5% from target
- **Method:** Rebalance with new contributions first (tax-efficient); only sell if drift is severe
- **Threshold for action:** ±5 percentage points from target weight

## Risks To Understand

1. **Market risk** — Broad equity drawdowns of 30-50% have occurred historically
2. **Inflation risk** — [How this strategy fares]
3. **Interest rate risk** — [Bond duration considerations]
4. **Concentration risk** — [Overlap with existing holdings, single-country exposure]
5. **Behavioral risk** — Will you actually stay invested during a 40% drawdown?

## What This Strategy Is NOT

- Not a market-timing strategy
- Not a short-term trading approach
- Not stock picking
- Not guaranteed to outperform

## Action Steps This Week

1. Open or fund account at [broker recommendations: Vanguard, Fidelity, Schwab — all offer commission-free ETF trading]
2. Place initial buy orders for: [list]
3. Set up automatic monthly contributions of $X
4. Calendar a rebalance check 12 months from today

---

**DISCLAIMER:** For educational/informational purposes only. Not financial advice. Not a recommendation to buy any specific security. Tickers are examples of vehicles that fit the screen criteria — equivalent alternatives from other providers exist. Always consult a licensed financial advisor, CPA, or tax professional before making investment decisions. Past performance does not guarantee future results. All investments carry risk of loss.
```

## Important Disclaimers To Include

- Never present screens as "stock picks" or "buy recommendations"
- Always note alternatives exist (VTI ≈ ITOT ≈ SCHB ≈ SPTM)
- Flag any high-cost or high-risk vehicles explicitly
- Note that backtests don't predict the future
- Emphasize behavioral discipline over selection alpha

## Tone

Educational. Quantitative. Cite long-run academic evidence (e.g., "Fama-French three-factor model," "low-cost index funds beat ~80% of active managers over 15 years per SPIVA"). Don't hype any strategy.

**DISCLAIMER: For educational/informational purposes only. Not financial advice.**
