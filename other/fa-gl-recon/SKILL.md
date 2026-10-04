---
name: fa-gl-recon
version: 1.0.0
description: Reconcile a fund general-ledger account to its supporting subledger or source — investments, cash, income, expense, or capital — prove the bridge, and clear differences before the NAV is struck.
author: matrixx0070
tags: [fund-accounting, gl-reconciliation, subledger, trial-balance, nav, close]
capabilities: []
---

# GL Reconciliation

## When to use
Use this to reconcile a fund GL account to its supporting record — investment subledger (lots), cash to custodian/bank, income to the earnings schedule, expense to the accrual schedule, or capital to the investor register — as part of striking or reviewing a NAV. This proves that the trial balance the NAV is built on actually agrees to the underlying detail.

**Not for:** drilling a single stubborn difference to the offending transaction (use fa-break-trace) or tying the finished NAV package together across all accounts (fa-nav-tieout). This proves *one GL account agrees to its source*.

## Method
1. **Define the reconciliation.** Name the GL account and number, the supporting source, the as-of valuation date, and both balances (GL and source).
2. **Confirm the comparison basis.** Trade date vs settlement date, base vs local currency, market value vs cost — both sides must be on the same footing before you subtract.
3. **Compute the raw difference.** GL − source. Decision point: if zero and both are complete, note it and sign off — no items needed.
4. **Identify reconciling items** by category: timing (unsettled trades, in-transit cash), accruals not yet posted, corporate actions, FX, valuation/pricing, and errors or omissions.
5. **Quantify and categorize each item** — amount, side it adjusts, category, root cause. For anything you can't name in one line, hand it to fa-break-trace.
6. **Prove the bridge.** Adjusted GL (± its items) must equal adjusted source (± its items). Decision point: if it doesn't tie, you are missing an item — never sign off on an unnamed residual.
7. **Resolve and sign off.** Propose the correcting entry per item, flag aged items, and state reconciled / not reconciled with any residual. Preparer and reviewer must differ.

## Example
Investments at market, account 1200, 6/30. GL $250.0M; investment subledger (sum of lots at market) $250.4M; raw diff −$0.4M. Items: (a) a buy of $0.5M traded 6/30 but not yet in the subledger feed (+0.5M to source pending, or −0.5M timing on GL depending on which lags) → confirmed the subledger missed a same-day trade; (b) an unapplied stock dividend +$0.1M on the book. Bridge: adjusted GL 250.0 + 0.5 = 250.5; adjusted subledger 250.4 + 0.1 = 250.5 — ties at $250.5M. Correcting: load the trade into the subledger, apply the dividend on the book. Reconciled, $0 residual.

## Pitfalls
- **Signing off on an unexplained residual.** "Reconciled except $40k" is not reconciled — an unnamed gap is a potential error, mispricing, or fraud.
- **Reconciling to an incomplete source.** A custodian feed that dropped the last trades of the day understates the source; confirm the feed is complete and current before you rely on it.
- **Basis mismatch masquerading as a break.** A difference equal to unsettled trades (TD vs SD) or accrued interest (clean vs dirty) is a convention issue — normalize, don't book.
- **Reconciling only the point balance.** For roll-forward accounts (capital, accruals, FA) tie the *movement*, not just the ending balance — an offsetting error in additions and reductions leaves the endpoint right and the account wrong.
- **Letting the same item age every month.** A reconciling item that reappears is a process defect, not timing; fix the source, don't re-explain it.

## Output format
```
Account: <GL# / name> | Source: <subledger/custodian/...> | As-of: <date>
Basis check: TD/SD <ok> | ccy <ok> | MV/cost <ok>
Balances: GL <$> | source <$> | raw diff <$>
Reconciling items:
  | item | amount | side (GL/source ±) | category | root cause | action |
Bridge: adjusted GL <$> = adjusted source <$>  [pass/fail]
Correcting entries proposed: <...>
Aged / unexplained flags: <...>
Conclusion: reconciled / not | residual: <$> | preparer / reviewer: <who/date>
```

## Reference

### The fund trial balance and what backs each account
The NAV is built on a trial balance; every material account must tie to an independent source:
| GL account | Supporting source | Typical reconciling items |
|---|---|---|
| Investments (cost & market) | Investment subledger (lot records) | Unsettled trades, corporate actions, pricing |
| Cash | Custodian / bank statement | Outstanding wires, fees, FX, in-transit |
| Interest / dividend income | Income accrual schedule | Accrual timing, ex-date, withholding tax |
| Accrued expenses | Accrual schedules | Unposted accrual, true-up, invoice timing |
| Unrealized/realized gain | Investment subledger | Pricing, FX, cost-basis method |
| Capital / partners' capital | Investor register / TA | Pending subs/reds, equalization, carry |
| Receivables/payables (unsettled) | Trade blotter | TD/SD timing |

### The two-column bridge
Adjust each side for what the *other* side already reflects, then both must equal the true balance:
`Adjusted GL = GL ± GL-side items` and `Adjusted source = source ± source-side items`; the two must be identical. Only items that represent a genuine book error or omission generate a journal entry — timing items self-clear and are monitored, not booked.

### Diagnostic shortcuts
- Difference divisible by **9** → transposition (e.g., 5,400 vs 4,500 = 900).
- Difference exactly **2×** a known item → sign flip (added what should be subtracted).
- Round, whole-position difference → missing or duplicated transaction.
- Difference that scales with a currency's holdings → FX rate or FX date.
- Difference equal to a security's accrued interest → clean-vs-dirty convention.

### Roll-forward reconciliations
For balance-sheet accounts that move (capital, accruals, prepaids, FA, allowance): `beginning + additions − reductions ± adjustments = ending`, and ending must equal the GL. Auditors test the *movement*; a point-balance tie can hide compensating errors in the flows.

### Rigor by account risk and sign-off standard
Match effort to risk: high-value/high-volume accounts (investments, cash, capital) get line-level recs with independent review each period; stable low-risk accounts can use analytic (reasonableness) review at lower frequency. "Reconciled" means residual = $0 **or** every residual dollar is a named, categorized, aged item with an owner and a clear date. Segregation of duties is mandatory: the preparer and the approver must be different people, and the review must be evidenced (who, when) for audit.
