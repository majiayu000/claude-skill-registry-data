---
name: position-sizing
description: Use when deciding how large a position to take. Covers fixed-fractional risk, volatility-based sizing, the Kelly criterion and why to fractionalize it, and portfolio concentration limits.
metadata:
  category: finance
  version: 1.0.0
  tags: [position-sizing, risk, kelly, volatility, portfolio]
---

# Position Sizing

## Purpose

Determine how much to risk on a single position, so that a losing streak is survivable and no single idea can end the account. Position sizing determines survival; entry selection determines returns. Survival comes first.

## When to Use

- Deciding how many shares or contracts to buy.
- Setting a risk-per-trade policy.
- Checking whether a position breaches concentration limits.
- Reviewing why a drawdown was deeper than expected.

## Capabilities

- Fixed-fractional sizing from a stop distance.
- Volatility-adjusted sizing using ATR.
- Kelly criterion, and fractional Kelly in practice.
- Concentration limits: per position, per sector, per correlated group.
- Aggregate portfolio risk.

## Inputs

- Account equity.
- Entry price and stop price (or an ATR and a multiplier).
- Risk per trade, as a percentage of equity.
- Existing exposure, including correlated positions.

## Outputs

- A share or contract count.
- The dollar risk if the stop is hit, stated explicitly.
- Whether the position breaches any limit.

## Workflow

1. **Fix the risk per trade first** — Typically 0.5% to 2% of equity. This is a policy decision made when calm, not a per-trade judgment made when excited.
2. **Determine the stop** — At a level where the thesis is wrong, not at a level that produces a comfortable size. This is the discipline that everything else depends on.
3. **Size from the stop distance** — Shares = (equity × risk%) / (entry − stop). A wider stop means a smaller position, not more risk.
4. **Check the concentration limits** — Position size as a percentage of equity, sector exposure, and correlated exposure. A limit breached is a size reduced.
5. **Check the aggregate** — Ten positions each risking 1% is 10% at risk if they are correlated and all stop out together. In a market-wide selloff, they will be.

## Best Practices

- Never widen a stop to justify a larger position. That inverts the entire logic: the stop defines the risk, and the size follows from it.
- Correlated positions are one position. Five semiconductor names is one bet on semiconductors, and it should be sized as one.
- Full Kelly is theoretically optimal and practically unusable: it produces enormous drawdowns, and it assumes you know your edge precisely. You do not. Half-Kelly or less is the practical range.
- A 50% drawdown requires a 100% gain to recover. Sizing that permits deep drawdowns is not aggressive; it is arithmetically self-defeating.
- Volatility-based sizing normalizes risk across instruments: a fixed dollar risk on a volatile stock and a quiet one produces very different position values, and that is correct.
- Recalculate the size on the current equity, not on the starting equity. Sizing off a high-water mark after a drawdown compounds the damage.

## Examples

**Fixed-fractional sizing — the calculation that matters:**

```python
def position_size(
    equity: float,
    entry: float,
    stop: float,
    risk_pct: float = 0.01,
    max_position_pct: float = 0.20,
) -> PositionSize:
    if stop >= entry:
        raise ValueError("stop must be below entry for a long position")

    risk_dollars = equity * risk_pct
    risk_per_share = entry - stop
    shares = int(risk_dollars / risk_per_share)

    # The concentration limit binds independently of the risk limit. A very tight
    # stop can otherwise produce a position worth more than the account.
    max_shares_by_concentration = int((equity * max_position_pct) / entry)
    limited = shares > max_shares_by_concentration

    final = min(shares, max_shares_by_concentration)

    return PositionSize(
        shares=final,
        position_value=final * entry,
        dollar_risk=final * risk_per_share,
        pct_of_equity=(final * entry) / equity,
        limited_by_concentration=limited,
    )

# equity 100,000 | entry 50.00 | stop 47.50 | risk 1%
#   risk_dollars    = 1,000
#   risk_per_share  = 2.50
#   shares          = 400          -> position value 20,000 (20% of equity)
#   At the concentration cap exactly. A tighter stop of 49.50 would compute
#   2,000 shares ($100,000 — the whole account), and the cap correctly binds.
```

**Kelly, and why it is fractionalized:**

```python
def kelly_fraction(win_rate: float, avg_win: float, avg_loss: float) -> float:
    """f* = p - q/b, where b is the win/loss ratio."""
    b = avg_win / abs(avg_loss)
    f = win_rate - (1 - win_rate) / b
    return max(0.0, f)

# A genuinely good strategy: 55% win rate, 1.5:1 payoff.
#   full Kelly     = 0.55 - 0.45/1.5 = 0.25  -> risk 25% of equity per trade
#
# Full Kelly on this strategy produces expected drawdowns exceeding 50% and
# assumes the 55% and the 1.5 are known exactly. They are estimates from a
# finite sample; if the true win rate is 50%, full Kelly is a losing bet.
#
#   half Kelly     = 12.5%   still aggressive
#   quarter Kelly  =  6.25%  the upper end of what most practitioners use
#
# Most professional risk budgets land between 0.5% and 2% — far below even
# quarter Kelly — because the edge estimate is uncertain and ruin is permanent.
```

## Notes

- Kelly maximizes the expected logarithmic growth rate given a *known* edge. The edge is never known; it is estimated from a sample, and the estimate is biased upward by the fact that you chose this strategy because it looked good. Fractionalize accordingly.
- Correlation rises toward 1 in a crisis. A portfolio that appears diversified in normal conditions can be a single position at the worst moment. Size for the correlated case.
- This is educational material about position-sizing methodology, not financial advice. Any real allocation decision depends on circumstances this skill cannot see.
