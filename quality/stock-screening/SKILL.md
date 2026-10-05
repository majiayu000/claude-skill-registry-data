---
name: stock-screening
description: Use when building a screen to find candidates. Covers screen design, criteria that actually discriminate, avoiding overfitting, survivorship bias, and turning a screen's output into a shortlist rather than a shopping list.
metadata:
  category: finance
  version: 1.0.0
  tags: [screening, filters, factors, selection, bias]
---

# Stock Screening

## Purpose

Build a screen that narrows a universe to a reviewable shortlist. A screen is a filter, not a decision — its output is a list of things to look at, and treating it as a list of things to buy is the fastest way to lose money with a spreadsheet.

## When to Use

- Building a systematic screen for candidates.
- A screen that returns hundreds of results, or none.
- Evaluating whether a screen's criteria actually discriminate.
- Reviewing a screen that historically performed well and now does not.

## Capabilities

- Screen design: fundamental, technical, and combined criteria.
- Criteria selection and threshold setting.
- Overfitting detection.
- Survivorship and look-ahead bias avoidance.
- Ranking and shortlisting.

## Inputs

- The universe, and how it is defined.
- The characteristics being sought, and why they should matter.
- Historical data, if the screen is to be validated.

## Outputs

- A screen that returns a reviewable number of names — typically 10 to 40.
- Each criterion justified by a mechanism, not by backtest fit.
- A ranked shortlist for manual review.

## Workflow

1. **Define the universe first** — Liquidity and market-capitalization floors. A screen that returns illiquid microcaps you cannot actually trade is returning noise.
2. **Choose criteria with a mechanism** — Each filter should have a reason it should work, stated before you test it. "It scored well in the backtest" is not a mechanism; it is a warning sign.
3. **Use few criteria** — Three to six. Each additional filter cuts the result set and increases the chance you have fitted the screen to the past rather than to a real effect.
4. **Set thresholds at round, defensible numbers** — A revenue growth threshold of 23.7% is fitted. 20% is a judgment. The former will not survive out of sample.
5. **Check the biases** — Does the historical universe include companies that no longer exist? If not, the backtest is measuring the performance of survivors, which is not a strategy you could have run.
6. **Rank and review manually** — The screen produces candidates. A human — or a careful, separate analysis — decides. The screen does not know why a company is cheap.

## Best Practices

- A screen that returns 300 names has not screened. A screen that returns zero has been over-fitted. Aim for a number you will actually review.
- Every criterion should have a mechanism you can articulate before testing. Criteria discovered by searching the space of possible criteria are discovered by fitting noise, and there is a great deal of noise.
- Survivorship bias makes almost every naive backtest look good. A universe of "today's S&P 500 constituents, historically" excludes every company that failed, and that is precisely the population the screen needed to avoid.
- Look-ahead bias is subtler: using a fiscal-year figure on the day the year ended, rather than the day it was reported, gives the screen information nobody had. Use point-in-time data.
- Value screens find cheap stocks, and stocks are usually cheap for a reason. The screen finds the candidates; the work of determining whether the reason is fatal is not done by the screen.
- Do not re-optimize a screen after a period of poor performance. That fits it to the most recent regime, which is exactly the regime least likely to persist.

## Examples

**A screen with few criteria, each with a mechanism:**

```python
def momentum_quality_screen(universe: pd.DataFrame) -> pd.DataFrame:
    """Each filter has a stated mechanism. None was found by searching.

    Mechanisms:
      - Liquidity: we must be able to enter and exit without moving the price.
      - Relative strength: momentum is one of the most durable documented
        anomalies. Persistence over 6-12 months is the effect.
      - Trend structure: we do not want falling knives. Above a rising 200-day.
      - Profitability: quality screens out the low-priced momentum that is
        momentum toward zero.
      - Earnings growth: confirms the price move has a fundamental driver.
    """
    return (
        universe
        # Liquidity: tradable, not theoretical.
        .query("market_cap_usd > 2e9 and avg_dollar_volume_50d > 20e6")

        # Relative strength: top quintile over 6 months, versus the benchmark.
        .query("rs_126d > rs_126d.quantile(0.80)")

        # Trend: above a rising 200-day. No falling knives.
        .query("close > ma200 and ma200_slope_20d > 0")

        # Quality: profitable. Filters momentum-toward-zero.
        .query("roe > 0.15 and net_margin > 0.05")

        # Fundamental confirmation of the price move.
        .query("eps_growth_yoy > 0.20 and revenue_growth_yoy > 0.10")

        .sort_values("rs_126d", ascending=False)
        .head(25)                     # a reviewable shortlist, not a portfolio
    )

# Five criteria. Round thresholds. Each defensible without reference to a
# backtest. It will not be the best-performing screen in a backtest, and it is
# far more likely to work out of sample than one that is.
```

**The bias that makes a backtest lie:**

```python
# WRONG: today's index constituents, tested historically. Every company that
# was delisted, acquired, or went to zero is absent. The screen appears to
# have avoided them; in reality it was never offered them.
universe = current_sp500_members()
backtest(screen, universe, start="2010-01-01")   # results are fiction

# RIGHT: point-in-time membership, including everything that later failed.
universe = sp500_members_as_of(date)              # survivorship-free
fundamentals = fundamentals_as_reported(date)     # not as later restated,
                                                  # and not before the filing date
backtest(screen, universe, fundamentals, start="2010-01-01")

# The difference is routinely several percentage points of annual return —
# frequently the entire apparent edge.
```

## Notes

- Survivorship bias alone typically accounts for 1-4 percentage points of annualized return in a naive backtest. An apparent edge of that size is often nothing but the bias.
- The number of criteria is a proxy for overfitting risk. Every additional filter is another chance to have fitted the past. Three good criteria beat eight fitted ones.
- This is educational material about screening methodology, not financial advice, and no screen output is a recommendation to buy anything.
