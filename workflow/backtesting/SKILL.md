---
name: backtesting
description: Use when testing a trading strategy on historical data. Covers the biases that make a backtest lie, realistic costs, walk-forward validation, and the statistics that distinguish an edge from a coincidence.
metadata:
  category: finance
  version: 1.0.0
  tags: [backtesting, validation, overfitting, bias, statistics]
---

# Backtesting

## Purpose

Test a strategy honestly. The default outcome of a backtest is a beautiful equity curve that describes the past and predicts nothing — and every bias in the process pushes in that direction.

## When to Use

- Testing a strategy before risking capital.
- Validating that an apparent edge is real.
- Diagnosing why a live strategy underperforms its backtest.
- Reviewing someone else's backtest.

## Capabilities

- Bias elimination: survivorship, look-ahead, selection.
- Realistic cost modeling: commissions, spread, slippage, borrow.
- Walk-forward and out-of-sample validation.
- Statistical significance and multiple-testing correction.
- Robustness testing.

## Inputs

- The strategy rules, stated precisely enough to be executed mechanically.
- Point-in-time historical data, including delisted instruments.
- Realistic assumptions about execution.

## Outputs

- Performance metrics with costs included.
- Out-of-sample results, reported honestly.
- A judgment on whether the edge is real, with the evidence.

## Workflow

1. **Eliminate the biases before you run anything** — Survivorship (delisted names must be in the universe), look-ahead (data must be used only when it was available), and selection (the strategy must be specified before it is tested).
2. **Model the costs honestly** — Commission, the bid-ask spread, slippage that scales with size and inversely with liquidity, and borrow costs on shorts. Most published edges are smaller than realistic costs.
3. **Split the data before you look at it** — In-sample for development, out-of-sample for validation, and a final hold-out you touch exactly once.
4. **Walk forward** — Re-fit on a rolling window and test on the period immediately after. A single in-sample fit tells you nothing about a strategy that will be run forward in time.
5. **Correct for multiple testing** — If you tested forty variants, the best one looks good by chance. A p-value that has not been adjusted for the number of things you tried is not a p-value.
6. **Stress it** — Perturb the parameters. A strategy that only works with a 14-day lookback and fails with 13 or 15 is fitted to noise.

## Best Practices

- The most common backtesting error is look-ahead bias, and it is usually accidental: using a closing price to make a decision that would have been made during the day, or using a fundamental figure on the fiscal date rather than the filing date.
- Transaction costs kill more strategies than any other factor. A strategy trading daily with a 0.05% edge per trade is a losing strategy after a 0.10% round-trip cost, and it will have looked excellent before costs.
- A Sharpe ratio above 2 on a simple strategy in a liquid market is a bug, not a discovery. Look for the bias.
- Parameter sensitivity is the honesty test. If performance collapses when a parameter moves by one unit, the strategy has fitted noise. Plot the surface.
- The out-of-sample period must be genuinely untouched. If you look at it, adjust, and look again, it is now in-sample and you have no validation left.
- Report the strategy's worst period, not just its average. The maximum drawdown and its duration determine whether it is survivable in practice.

## Examples

**A backtest that does not lie to itself:**

```python
def backtest(strategy: Strategy, start: date, end: date) -> BacktestResult:
    equity, trades = [], []

    for day in trading_days(start, end):
        # Point-in-time universe: includes everything that was tradable THAT DAY,
        # including companies that were later delisted or went to zero.
        universe = universe_as_of(day)

        # Point-in-time fundamentals: as reported, on or before this date. Not
        # as later restated, and never before the filing date.
        data = fundamentals_as_of(day, universe)

        # Signals are computed on data available at the CLOSE of the prior day.
        # Trades execute at the NEXT day's open. Using today's close to decide
        # and today's close to fill is the classic look-ahead error.
        signals = strategy.signals(data.shift(1))

        for signal in signals:
            fill = next_open(signal.symbol, day)
            cost = transaction_cost(
                price=fill,
                shares=signal.shares,
                adv=data.loc[signal.symbol, "adv_20d"],
            )
            trades.append(Trade(day, signal.symbol, fill, cost))

        equity.append(mark_to_market(day))

    return BacktestResult(equity=equity, trades=trades)


def transaction_cost(price: float, shares: int, adv: float) -> float:
    """Commission + half the spread + slippage that scales with participation."""
    notional = price * shares
    commission = max(1.0, shares * 0.005)
    spread_cost = notional * 0.0005                       # half-spread, liquid names

    # Market impact grows with the fraction of daily volume you consume.
    participation = (shares * price) / max(adv, 1)
    impact = notional * 0.10 * math.sqrt(participation)   # square-root impact model

    return commission + spread_cost + impact
```

**The result, reported honestly:**

```text
Strategy: momentum + quality, 25 names, monthly rebalance.

                        In-sample    Out-of-sample   Difference
                        2010-2018    2019-2024
CAGR (gross)              18.4%          11.2%
CAGR (net of costs)       14.1%           6.8%        <- costs take 4-5 points
Sharpe (net)               1.12           0.54        <- halved out of sample
Max drawdown             -22.4%         -31.7%
Longest drawdown          8 months      19 months     <- the number that matters

Multiple testing: 34 variants were tested. The reported result is the best of
34. Adjusting for that (Bonferroni), the out-of-sample Sharpe of 0.54 is not
distinguishable from zero at the 5% level.

Parameter sensitivity: performance is stable for lookbacks of 100-150 days
(Sharpe 0.48-0.57) and collapses below 80 days. That stability is mildly
reassuring; the multiple-testing problem is not.

Judgment: the edge, if it exists, is much smaller than the in-sample result
suggests and is not statistically established. A 19-month drawdown is longer
than most people can actually sit through. Not deployable at meaningful size
on this evidence.
```

## Notes

- The gap between in-sample and out-of-sample performance in the example — a Sharpe of 1.12 falling to 0.54 — is entirely typical, and it is the reason out-of-sample testing is not optional.
- The square-root market-impact model is a standard approximation: impact scales with the square root of participation rate. It matters enormously for any strategy trading size, and it is usually omitted from backtests that look excellent.
- This is educational material about backtesting methodology, not financial advice, and no backtest result constitutes a recommendation.
