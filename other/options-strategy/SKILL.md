---
name: options-strategy
description: Use when analyzing or constructing an options position. Covers the greeks in practical terms, implied volatility and its term structure, common structures and their true risk, and assignment and expiration mechanics.
metadata:
  category: finance
  version: 1.0.0
  tags: [options, greeks, volatility, spreads, risk]
---

# Options Strategy

## Purpose

Construct and analyze options positions with an accurate view of what is actually being risked. Options positions frequently have a risk profile very different from the one the buyer had in mind, and the difference shows up at expiration.

## When to Use

- Constructing an options position to express a view.
- Analyzing the risk of an existing position.
- Deciding whether implied volatility makes an option cheap or expensive.
- Managing a position into expiration or assignment.

## Capabilities

- The greeks: delta, gamma, theta, vega — and what each one actually costs you.
- Implied volatility, IV rank, and term structure.
- Structures: spreads, straddles, strangles, calendars, and their real risk profiles.
- Assignment, exercise, and pin risk.
- Position management and adjustment.

## Inputs

- The view: direction, magnitude, and time frame. All three are required.
- Current implied volatility, and where it sits historically.
- Liquidity of the specific contracts, not just the underlying.

## Outputs

- A structure that matches the view.
- Maximum loss, maximum gain, and breakeven — computed, not assumed.
- The conditions under which the position is exited.

## Workflow

1. **State the view precisely** — Direction, magnitude, *and* time frame. An option requires all three. "I think it goes up" is not sufficient to choose a structure; being right about direction and wrong about timing loses money.
2. **Check where implied volatility sits** — Buying options when IV is at the 90th percentile of its own history means you need a large move just to overcome the volatility crush. Selling when IV is at the 10th percentile means being paid very little for real risk.
3. **Choose the structure that matches** — Long options for a large, fast move with defined risk. Spreads to reduce cost and cap gain. Selling premium only when IV is elevated and the risk is genuinely defined.
4. **Compute the actual maximum loss** — Not the one you imagine. For a naked short option, it is unbounded, and that is not a figure of speech.
5. **Plan the exit before entry** — Including what happens at expiration. Positions held into expiration have assignment and pin risk that did not exist the day before.
6. **Check the liquidity of the contracts** — A liquid underlying can have illiquid options. A wide bid-ask spread is a cost you pay twice.

## Best Practices

- Theta is not free money. Selling premium collects small amounts consistently and loses large amounts occasionally. The strategy's profit and loss distribution is not the same shape as its win rate, and a 90% win rate can still be a losing strategy.
- Gamma is what kills short-option positions. A short option that is comfortably out of the money is safe until the underlying approaches the strike, at which point the delta changes rapidly and the loss accelerates.
- Buying options into an earnings announcement means buying elevated IV that collapses the moment the announcement occurs. You can be right about the direction and still lose money — this is the most common options mistake there is.
- Never sell a naked call. The loss is unbounded and the premium collected is finite. There is no position size at which this is a good trade.
- Long options lose money every day the underlying does not move. Time decay accelerates in the final month.
- An option position with no exit plan will be held to expiration, which is a decision, and usually the wrong one.

## Examples

**The IV crush that catches everyone:**

```text
Situation: earnings in 2 days. You expect a large move.

Stock at $100. The 30-day at-the-money straddle costs $8.00.
Implied volatility: 68% (its 52-week range is 24%-71%).

The market has priced a ±8% move. For the long straddle to profit, the stock
must move MORE than 8%.

After the announcement, IV collapses to ~30% regardless of the direction of
the move — the uncertainty that justified 68% has been resolved.

Outcome if the stock moves 6% (a large move, and you were directionally right):
  Intrinsic value gained : ~$6.00
  Value lost to IV crush : ~$7.20   (vega ~0.18 x 38 vol points)
  Net                    : approximately -$1.20 per share. A loss.

You predicted the direction, the stock moved substantially, and you lost money.
This is the standard outcome of buying options into earnings and it surprises
people every quarter.

The structure that expresses "large move" without paying for elevated IV is a
calendar or a diagonal — long the far-dated option (less vega-sensitive to the
front-month crush), short the front. Or simply take a stock position.
```

**Computing the real risk, not the imagined one:**

```python
def position_risk(legs: list[OptionLeg], underlying: float) -> RiskProfile:
    prices = np.linspace(underlying * 0.5, underlying * 1.5, 400)
    pnl = np.array([sum(leg.payoff_at_expiry(p) for leg in legs) for p in prices])

    has_naked_short_call = any(
        leg.is_short and leg.is_call and not _is_covered(leg, legs) for leg in legs
    )

    return RiskProfile(
        max_gain=float(pnl.max()),

        # This is the number people get wrong.
        max_loss=float("-inf") if has_naked_short_call else float(pnl.min()),

        breakevens=[float(p) for p in _zero_crossings(prices, pnl)],
        net_debit=sum(leg.cost for leg in legs),

        # Aggregate greeks: the position's actual exposure, not each leg's.
        net_delta=sum(leg.delta * leg.quantity * 100 for leg in legs),
        net_theta=sum(leg.theta * leg.quantity * 100 for leg in legs),
        net_vega=sum(leg.vega * leg.quantity * 100 for leg in legs),

        warning=(
            "UNBOUNDED LOSS: this position contains a naked short call. There is "
            "no maximum loss. Do not size this as if there were."
            if has_naked_short_call else None
        ),
    )
```

## Notes

- The earnings IV-crush example is the single most valuable thing in this skill. Being right about the direction and losing money is deeply counterintuitive, and it happens to nearly every options trader once.
- A 90% win rate on short premium is compatible with losing money overall: nine wins of $100 and one loss of $2,000 is a losing strategy with an excellent win rate. Look at expectancy, never at the win rate alone.
- This is educational material about options mechanics, not financial advice. Options can lose their entire value, and short options can lose more than the account holds.
