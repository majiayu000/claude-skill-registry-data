---
name: portfolio-review
description: Use when reviewing a portfolio's construction and exposure. Covers concentration, correlation, factor and sector exposure, hidden bets, and whether the portfolio expresses the intended view.
metadata:
  category: finance
  version: 1.0.0
  tags: [portfolio, correlation, exposure, diversification, factors]
---

# Portfolio Review

## Purpose

Determine what a portfolio is actually betting on, which is frequently not what its owner thinks. A portfolio of twenty names can be a single concentrated bet, and the position list will not tell you that.

## When to Use

- Periodic review of holdings and exposure.
- After a drawdown, to understand what actually drove it.
- Before adding a position, to see what it does to the whole.
- Assessing whether diversification is real or nominal.

## Capabilities

- Concentration analysis: position, sector, factor.
- Correlation and effective number of positions.
- Factor exposure: size, value, momentum, quality, volatility.
- Hidden-bet identification.
- Attribution: what actually drove the return.

## Inputs

- Holdings, weights, and cost basis.
- Return history for correlation and factor analysis.
- The stated investment thesis, so the portfolio can be checked against it.

## Outputs

- What the portfolio is actually exposed to.
- Divergences between the intended and the actual bet.
- Concentration risks that are not visible in the position list.

## Workflow

1. **Compute the effective number of positions** — Twenty names with a 0.85 average correlation is not twenty bets. The effective number tells you how many independent bets you actually hold, and it is usually far lower than the count.
2. **Aggregate by sector and by factor** — Sector exposure is visible. Factor exposure — a portfolio that is entirely long-duration growth, whatever the sector labels say — usually is not.
3. **Find the hidden bet** — Ten names in different sectors that all depend on the same input (interest rates, the price of oil, one customer) is one bet. This is what a correlation matrix reveals and a position list conceals.
4. **Attribute the return** — What actually drove performance? If the portfolio is up 12% and 11 points came from one position, the strategy has not been validated; one position has.
5. **Compare with the thesis** — Does the portfolio express the intended view? A portfolio built on a "value" thesis whose factor exposure is momentum has drifted.
6. **Stress it** — What does this portfolio do in a 20% market decline, a 200bp rate move, or a sector rotation?

## Best Practices

- Correlation rises in a crisis. A portfolio that appears diversified in normal conditions can become a single position at the worst possible moment, and that is when it matters.
- The effective number of bets is the honest diversification measure. Position count is not.
- Attribution matters more than the total return. A profitable quarter driven entirely by one position tells you nothing about whether the process works.
- Factor exposure is the most common hidden bet. Every high-growth name is a bet on rates, regardless of what sector it is classified in.
- A position you have not reviewed in a year is a position you have forgotten why you own. Re-derive the thesis or exit.
- Compare against a relevant benchmark. Beating the market by taking three times its risk is not skill.

## Examples

**What a portfolio is actually betting on:**

```python
def review(portfolio: Portfolio, returns: pd.DataFrame) -> PortfolioReview:
    weights = portfolio.weights
    corr = returns[portfolio.symbols].corr()

    # The effective number of independent bets. A position count is a fiction
    # when correlations are high.
    w = weights.values
    portfolio_variance = w @ returns[portfolio.symbols].cov().values @ w
    weighted_avg_variance = (w**2 @ returns[portfolio.symbols].var().values)
    effective_n = float(weighted_avg_variance / portfolio_variance) if portfolio_variance else 0

    # Groups of positions that move together: these are ONE bet, not several.
    clusters = cluster_by_correlation(corr, threshold=0.70)

    # Factor exposure via regression against factor returns.
    factor_betas = regress(portfolio.returns, FACTORS[["mkt", "size", "value", "momentum", "quality"]])

    return PortfolioReview(
        position_count=len(weights),
        effective_positions=effective_n,
        clusters=clusters,
        factor_betas=factor_betas,
        top_5_weight=float(weights.nlargest(5).sum()),
        sector_exposure=portfolio.by_sector(),
    )
```

**A review that finds the bet nobody placed deliberately:**

```text
Portfolio: 22 positions, "diversified across sectors".

Position count            : 22
Effective positions       : 3.4     <- this is the real number

Correlation clusters (rho > 0.70):
  Cluster 1 (58% of book): NVDA, AMD, AVGO, TSM, ASML, MU, ARM, MRVL
      Labelled: Technology, Semiconductors
      Actual bet: AI capital expenditure. One bet, eight ways.

  Cluster 2 (21%): PLTR, SNOW, DDOG, NET, CRWD
      Labelled: Software, Technology
      Actual bet: also AI capital expenditure, plus long-duration growth.
      Correlation with cluster 1: 0.74. It is not a separate bet.

  Cluster 3 (14%): JPM, BAC
  Cluster 4 (7%):  XOM, CVX

Factor exposure:
  Market beta   : 1.42    <- 42% more market risk than the index
  Momentum      : +0.71   <- a large, unintended momentum bet
  Value         : -0.58   <- short value
  Quality       : +0.12

Attribution, trailing 12 months (+31%):
  NVDA alone    : +19 points
  Everything else: +12 points across 21 positions

Findings:
  1. This is a leveraged bet on AI capex, wearing the costume of a diversified
     22-position portfolio. 79% of the book is in two clusters that correlate
     at 0.74 with each other.
  2. Beta of 1.42 means a 20% market decline implies roughly -28% before any
     idiosyncratic damage.
  3. The return is one position. The process has not been validated.
  4. The stated thesis is "quality growth at a reasonable price". The actual
     factor exposure is momentum, short value. The portfolio has drifted from
     its thesis, or the thesis was never what was being executed.
```

## Notes

- The gap between 22 positions and 3.4 effective positions is the single most useful thing a portfolio review produces. It is invisible in a position list and obvious in a correlation matrix.
- A market beta of 1.42 is a leverage decision, whether or not it was made deliberately. Most portfolios have never had it computed.
- This is educational material about portfolio-analysis methodology, not financial advice or a recommendation regarding any holding.
