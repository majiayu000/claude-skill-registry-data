---
name: momentum-signals
description: Build evidence-only momentum signals from component scores and weights, and emit them as journal notes that never clear a ticket by themselves.
bots:
  - bot-08-signal
gates:
  - G-2
required_tools:
  - market.ohlcv
  - market.trades
  - market.holders_snapshot
required_data:
  - solana_rpc
permissions:
  max_side_effect: read
  network: true
  filesystem: none
fixtures:
  - tests/fixtures/http/holders.json
---

# Momentum Signals

## L1 - Summary

SIGNAL produces evidence, not clearance. Component scores (price action, trade flow, holder change) combine through pinned weights into a signal with its reasons, emitted as a `journal.append` note with payload `note_kind=signal`. A signal never buys, never clears risk, and never overrides a halt.

```
components scored -> weights applied -> signal with reasons -> journal note -> RISK and CHIEF decide
```

## L2 - Method

1. S1 - Score the components: read `market.ohlcv` for price structure, `market.trades` for flow, and `market.holders_snapshot` for concentration change. Each component reports its score plus the window and source it used.
2. S2 - Apply the pinned weights: combine components with the reviewed weight table only. Weight changes go through `replay-and-backtest` first; per-signal weight tuning is forbidden.
3. S3 - Emit with reasons: append the signal via `journal.append kind=journal_note` with payload `note_kind=signal`, carrying the components, weights version, and window. A bare direction without reasons is not a signal.
4. S4 - Stay evidence-only: the signal proposes; RISK verdicts and human approvals dispose. Never phrase a signal as clearance, and never attach urgency to bypass review.
5. S5 - Expire honestly: signals carry their window; past the window they are history, not standing orders. Re-score on fresh data instead of reusing a stale signal.

## Failure modes

| Symptom | Cause | Action |
|---|---|---|
| Signal without reasons | Truncated emission | Re-emit with components and weights version; reasons are the signal |
| Weights tuned per signal | Overfitting to a favorite | Revert to the pinned table; tune only with replay evidence |
| Stale signal reused | Window expired but direction recycled | Re-score on fresh reads; expired signals never trigger |
| Signal treated as clearance | Misread authority | Re-state: SIGNAL advises, RISK plus human decide |

## References

- Tools: `market.ohlcv`, `market.trades`, `market.holders_snapshot` (signal inputs)
- Fixture: `tests/fixtures/http/holders.json` (recorded holder response shape)
- Gate G-2: signals feed approval-gated flow as evidence
- Companion skills: `replay-and-backtest` (weight validation), `desk-strategy-lab` (rule experiments)
