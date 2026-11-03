---
name: trade-exit-reviewer
description: Review SELL actions against the active position's strategy exit rules. Use when a trader logs a SELL and needs confirmation that a mechanical exit condition was triggered.
license: MIT
---

# Trade Exit Reviewer

Checks whether a SELL action is mechanically justified by the active strategy's exit rules.

## Exit conditions by strategy

**MR (Mean Reversion):**
- Price reached +8% target from entry
- 30-day holding horizon expired
- Stop loss triggered (typically −5% to −8%)

**MOM (Momentum):**
- RSI_14 > 75
- Price fell below SMA_20
- 15-day holding horizon expired
- Stop loss triggered

## Output format

```
Exit review: <ticker>
Strategy: [MR] | [MOM]
Result: VALID EXIT | PREMATURE EXIT
Condition triggered: <name of condition> | NONE
```

## Rules

- VALID EXIT requires at least one named exit condition to be met
- PREMATURE EXIT when none of the exit conditions are satisfied
- Name the specific condition triggered — do not just say "conditions met"
- For stop loss: also note the percentage drop from entry
