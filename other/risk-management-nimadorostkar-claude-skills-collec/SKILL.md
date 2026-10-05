---
name: risk-management
description: Use when defining or enforcing trading risk limits. Covers drawdown circuit breakers, exposure budgets, correlation risk, stop discipline, and pre-trade gates that prevent the worst decisions.
metadata:
  category: finance
  version: 1.0.0
  tags: [risk, drawdown, exposure, discipline, limits]
---

# Risk Management

## Purpose

Define the limits that keep a losing period from becoming a terminal one, and enforce them mechanically — because the moment they matter most is the moment you will most want to override them.

## When to Use

- Setting risk limits for a strategy or an account.
- In a drawdown, deciding whether to reduce size.
- Before entering a trade, checking it against the rules.
- After a loss, reviewing whether the rules were followed.

## Capabilities

- Drawdown circuit breakers and de-risking schedules.
- Exposure budgets: gross, net, per sector, per correlated group.
- Correlation-aware risk aggregation.
- Stop-loss discipline and the failure modes around it.
- Pre-trade checklists as a hard gate.

## Inputs

- Account equity and the current drawdown from the high-water mark.
- Open positions and their correlations.
- The proposed trade.

## Outputs

- A pass/fail against each limit.
- Required size reduction, if any.
- A stated reason for a rejection.

## Workflow

1. **Set the limits when calm** — Maximum risk per trade, maximum total exposure, maximum drawdown before de-risking. Write them down. They must be decided before they are tested.
2. **Define the circuit breaker** — A drawdown level at which size is cut, and a deeper level at which trading stops entirely. This is the rule that prevents a bad month from becoming a career-ending one.
3. **Aggregate correlated risk** — Positions in the same sector, the same factor, or the same theme are one risk. Sum them.
4. **Gate every trade** — Check it against the limits before entry, mechanically. A checklist that is consulted after the position is on is not a gate.
5. **Honor the stop** — The stop is the risk. Moving it further away after entry converts a defined loss into an undefined one, and it is the single most common way accounts are destroyed.
6. **Review the rule, not the outcome** — A trade that followed the rules and lost was a good trade. A trade that broke the rules and won was a bad one, and it will be repeated.

## Best Practices

- Widening a stop is the cardinal sin. The stop was set where the thesis is wrong; moving it means the thesis is wrong and you are staying anyway.
- A drawdown circuit breaker must be mechanical. In a drawdown, judgment is impaired precisely when it is most needed — that is what the rule is for.
- Reduce size in a drawdown, not after recovering from one. Risking the same percentage of a smaller account is already a reduction; cutting the percentage as well is what stops the compounding.
- Correlation is not a static number. It rises sharply in a selloff, which is exactly when the diversification you were relying on stops existing.
- The purpose of a risk limit is to be binding. A limit you override when it is inconvenient is not a limit; it is a preference.
- Track rule adherence separately from profit and loss. They are different things, and only one of them is under your control.

## Examples

**A drawdown circuit breaker with a defined de-risking schedule:**

```python
@dataclass(frozen=True)
class RiskPolicy:
    base_risk_pct: float = 0.01           # 1% per trade at full size
    max_gross_exposure: float = 1.5       # 150% of equity, long + short
    max_sector_exposure: float = 0.30
    max_correlated_risk_pct: float = 0.04 # aggregate risk across correlated positions


def size_multiplier(drawdown_pct: float) -> float:
    """De-risk as the drawdown deepens. Mechanical, not discretionary."""
    if drawdown_pct >= 0.20:
        return 0.0        # STOP. No new positions. Review the strategy, not the market.
    if drawdown_pct >= 0.15:
        return 0.25
    if drawdown_pct >= 0.10:
        return 0.50
    if drawdown_pct >= 0.05:
        return 0.75
    return 1.0


# Equity 100,000, high-water 120,000 -> drawdown 16.7% -> multiplier 0.25.
# Risk per trade is now 0.25% of 100,000 = $250, not the $1,000 it was at the peak.
# This is a 4x reduction in position size at the point where the strategy is
# demonstrably not working. It is not pessimism; it is arithmetic.
```

**A pre-trade gate that is actually a gate:**

```python
def pre_trade_check(trade: ProposedTrade, book: Portfolio, policy: RiskPolicy) -> GateResult:
    failures = []

    if trade.stop is None:
        failures.append("BLOCK: no stop defined. Risk is undefined and unbounded.")

    if trade.dollar_risk > book.equity * policy.base_risk_pct * size_multiplier(book.drawdown):
        failures.append(
            f"BLOCK: risk ${trade.dollar_risk:,.0f} exceeds the current limit "
            f"(drawdown {book.drawdown:.1%} -> size multiplier "
            f"{size_multiplier(book.drawdown):.2f})"
        )

    sector_after = book.sector_exposure(trade.sector) + trade.position_value / book.equity
    if sector_after > policy.max_sector_exposure:
        failures.append(
            f"BLOCK: {trade.sector} exposure would reach {sector_after:.0%} "
            f"(limit {policy.max_sector_exposure:.0%})"
        )

    # Correlated positions are one position.
    correlated = book.positions_correlated_with(trade.symbol, threshold=0.7)
    total_correlated_risk = sum(p.dollar_risk for p in correlated) + trade.dollar_risk
    if total_correlated_risk > book.equity * policy.max_correlated_risk_pct:
        failures.append(
            f"BLOCK: aggregate risk across {len(correlated) + 1} correlated positions "
            f"({', '.join(p.symbol for p in correlated)}) would reach "
            f"${total_correlated_risk:,.0f}"
        )

    if trade.is_earnings_within(days=2) and not trade.earnings_intentional:
        failures.append("BLOCK: earnings within 2 days. Overnight gap risk is not sized for.")

    return GateResult(passed=not failures, failures=failures)
```

## Notes

- The gate above blocks on a missing stop. That single check prevents the majority of catastrophic single-position losses, because an unbounded loss requires an undefined risk.
- A 20% drawdown triggering a full stop is not a panic response; it is a recognition that either the strategy has stopped working or the market regime has changed, and both warrant investigation rather than more trades.
- This is educational material on risk-management methodology, not financial advice. Limits appropriate for one account and strategy may be entirely wrong for another.
