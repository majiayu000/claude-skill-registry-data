---
name: pre-trade-investment-gate
description: Run a final read-only readiness check before an investment or trade across exact identity, evidence cutoff, executable entry, thesis, payoff, catalysts, invalidation, quantity, maximum loss, portfolio fit, liquidity, spread/fees/tax, settlement, expiry/margin, operational risk, and independent challenge. Use when the user is about to act, asks “should I place it now”, “final check”, “is this trade ready”, or Turkish intents such as “son kontrol”, “emri vereyim mi”, “işleme gireyim mi”, “alım için hazır mı”, “bir kez daha kontrol et”. Return READY/CONDITIONAL/NOT READY/REJECT, but never place, transmit, or automate an order.
---

# Pre-Trade Investment Gate

Own only the final readiness decision. Do not replace the underlying equity, fund, crypto, warrant, technical, forecast or portfolio analysis.

Read [references/gate-contract.md](references/gate-contract.md). Run `scripts/validate_pretrade.py` when a structured packet is available.

## Workflow

1. Freeze the intended action, instrument, venue, account context, direction, horizon, order type, quantity and data cutoff.
2. Confirm that the narrow analyst has completed recommendation-grade work and that `$finance-evidence-guard` is `PASS` or explicitly bounded `CONDITIONAL`.
3. Reconcile executable bid/ask or NAV context, market status, delay, lot, fees, spread, slippage, tax caveat, settlement and operational restrictions.
4. Verify thesis, catalyst/recognition path, bear/base/bull payoff, invalidation, exit/review rule and the condition under which doing nothing wins.
5. Use `$portfolio-risk-and-sizing` to check cash, loss budget, concentration, look-through overlap, liquidity and post-trade exposure.
6. Require product-specific mechanics: fund cutoff/settlement; warrant/option expiry/payoff; futures margin/liquidation; short borrow; crypto network/contract/custody; leveraged/barrier terms.
7. Require an independent `$investment-red-team` result for concentrated, leveraged, illiquid, high-loss or otherwise consequential actions.
8. Validate the packet. Return the first blocking defect and the shortest path to readiness; do not bury it under a long checklist.

## Status

- `READY`: every critical field is verified and no unresolved condition changes the action.
- `READY WITH CONDITIONS`: executable only if the named price, liquidity, evidence or risk conditions hold.
- `NOT READY`: required evidence or execution input is missing; the idea may still be valid.
- `REJECT`: thesis/payoff, evidence, sizing or operational risk fails the stated objective.

## Hard rules

- Never upgrade stale last price, screenshot/OCR, indicative NAV or modeled value into an executable quote.
- Never mark ready without a quantified size, modeled maximum/stress loss and invalidation.
- Never let user enthusiasm or prior research effort waive a failed gate.
- Never place an order, open a broker page, request credentials or produce auto-trading instructions.

## Output

Lead with status and the decisive reason. Then show action/order snapshot, data time, cleared gates, blocking defects or conditions, quantity/cash/max loss/post-trade weight, exit/invalidation, evidence/red-team results and the exact finalization steps.
