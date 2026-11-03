---
name: copytrader-suitability-reviewer
description: Review a trader's public copy-trading stats and assess whether they are suitable to copy for a conservative investor profile.
license: MIT
---

# CopyTrader Suitability Reviewer

Reviews a trader's public stats and outputs a suitability verdict for a conservative investor.

## Input

Trader stats: username, risk score (1–10), 12-month gain %, max drawdown %, months active on the platform.

## Output

```
Trader: <username>
Result: SUITABLE | NOT_SUITABLE
Reason: <one line naming the key determining factor>
```

## Rules

- NOT_SUITABLE if any of: risk score > 7, months active < 12, 12-month gain ≤ 0%
- SUITABLE only when all three conditions pass
- Reason must name the specific determining factor — not just "meets criteria" or "does not meet criteria"
- For NOT_SUITABLE with multiple failing factors, name the most disqualifying one
