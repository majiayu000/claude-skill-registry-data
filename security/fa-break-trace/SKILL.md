---
name: fa-break-trace
version: 1.0.0
description: Trace a break between two records of the same position or cash — accounting vs custodian, fund vs prime broker, trade vs settlement — from the aggregate difference down to the offending transaction, and classify it for clearing.
author: matrixx0070
tags: [fund-accounting, breaks, reconciliation, custodian, position, cash, settlement]
capabilities: []
---

# Break Trace

## When to use
Use this when two sources that should agree do not — the accounting book vs the custodian/prime-broker feed, position vs holdings report, cash ledger vs bank, or trade-date vs settlement-date view — and you need to find *which transaction* causes the gap and *why*. This is the drill-down that turns a headline difference into a named, ownable item.

**Not for:** proving a full GL account to a subledger (use fa-gl-recon), or tying the whole NAV package together (fa-nav-tieout). This isolates and classifies *one break*, then hands the fix downstream.

## Method
1. **State the two sides.** Name source A and source B, the exact field (quantity, market value, cost, or cash), the as-of date, and the basis of each (trade date vs settlement date, local vs base currency, clean vs dirty price).
2. **Compute the break.** A − B, signed. Decision point: confirm you are comparing like for like first — a "break" that is really TD-vs-SD or clean-vs-dirty is a definition mismatch, not a real difference. Normalize before you hunt.
3. **Localize by decomposition.** Split the difference by security, then by transaction type (buy/sell/corporate action/income/fee/FX), narrowing until one line carries the gap. For value breaks, decompose into quantity × price × FX to see which factor moved.
4. **Pull the two transaction records.** Compare quantity, price, trade/settle date, fees, accrued interest, and FX rate field by field.
5. **Classify the break.** Timing (one side posted, the other pending), quantity, price/valuation, FX, corporate-action, fee/accrual, booking error, or missing/duplicate transaction.
6. **Attribute root cause and side.** State which source is wrong (or both) and why. Decision point: if you cannot say which side is right, escalate to the counterparty for their record before booking anything.
7. **Assign clearing.** Recommend the correction (rebook, accrue, chase custodian, await settlement), owner, and expected clear date; flag the item aged if it recurs.

## Example
Position break in XYZ: accounting shows 10,000 sh; custodian shows 10,050. Difference +50 (accounting long). Decompose: no price factor (quantity break). Pull transactions — a 100-for-99 stock split (a 1.0101 ratio) settled on the custodian but the corporate action wasn't applied on the book; expected new quantity 10,000 × 100/99 ≈ 10,101 vs custodian 10,050 doesn't match either, so re-examine: custodian applied a partial. Root: unapplied corporate action on the book *and* a pending 50-share sell on the custodian not yet on the book. Split into two named items — apply the CA (book), await the sell settlement — each of which clears cleanly. Neither side was "wrong"; two timing/event items overlapped.

## Pitfalls
- **Netting two breaks into one.** A single aggregate difference can be two offsetting errors; if the decomposition leaves a clean residual, keep splitting — don't sign off on a net that hides a large plus and a large minus.
- **Comparing trade date to settlement date.** The most common false break. Normalize both sides to the same date basis before computing anything.
- **Assuming the custodian is right.** Custodian feeds carry stale prices, missed corporate actions, and their own booking lags; treat both sides as suspect until you find the cause.
- **Clean vs dirty price on bonds.** A value break equal to accrued interest is a convention mismatch, not a real difference.
- **FX rate source drift.** A value break that scales with a currency's positions is an FX-rate or FX-timing difference — check the rate and the rate date, not the quantity.

## Output format
```
Break: <security/cash> | Field: <qty/MV/cost/cash> | As-of: <date>
Source A: <name/basis> <value> | Source B: <name/basis> <value> | Difference: <signed>
Normalization checked: TD/SD <ok> | ccy <ok> | clean/dirty <ok>
Decomposition: <by security → txn type → factor>
Offending transaction(s): <id, qty, price, date, fee, fx>
Classification: <timing/qty/price/fx/CA/fee/error/missing/dup>
Root cause & side: <A wrong / B wrong / both / counterparty> — <why>
Clearing: <action> | owner: <who> | expected clear: <date> | aged: Y/N
```

## Reference

### Break taxonomy
- **Timing:** one side posted (TD) and the other pending (SD), unsettled trade, in-transit cash/wire, pending corporate action. Self-clears — track the expected date.
- **Quantity:** unapplied split/dividend-in-kind, missed corporate action, wrong lot, partial fill booked whole.
- **Price / valuation:** stale price, wrong price source, clean-vs-dirty, wrong valuation point, manual override not carried.
- **FX:** different rate, different rate date/time, or triangulation vs direct quote.
- **Fee / accrual:** commission, custody, or accrued-interest difference; one side gross, the other net.
- **Booking error:** wrong account, sign flip, transposition, wrong CCY, duplicate, or wholly missing transaction.

### Decomposition math
A market-value break decomposes as `MV = quantity × price × fx`. Compare each factor across sources: if quantity and fx tie but value doesn't, it's a price break; if quantity ties and value scales with the currency, it's fx. A **transposition** in any figure produces a difference divisible by 9 (e.g., 540 vs 450 = 90). A break exactly **2×** a known transaction signals a sign flip — one side added what the other subtracted. A round, whole-position difference points to a missing or duplicated transaction.

### Trade date vs settlement date
- **Trade-date accounting** recognizes the position/cash on execution; most fund NAVs are struck TD.
- **Settlement-date** recognizes on cash movement; custodian cash often reports SD.
- A break between a TD book and an SD custodian view for unsettled trades is *expected* and self-clears at settlement — do not book a correction, reconcile the timing.

### Corporate actions as break sources
Splits, reverse splits, stock/scrip dividends, spin-offs, mergers, rights, and returns of capital change quantity and/or cost basis. A break that appears on the ex-date or pay-date of a known action is almost always an unapplied or differently-timed corporate action. Confirm the ratio, ex/record/pay dates, and elective vs mandatory treatment before rebooking.

### Aging and escalation
Classify by age: **T+0/T+1** current (expected to clear at settlement); **>5 days** investigate; **>30 days** presumed error — escalate to the counterparty and consider a reserve. Every open break needs an owner, a category, and an expected clear date. An aged position or cash break is a control finding: it can mask a real loss, a fraud, or a valuation error, so it never ages silently.

### Cash vs position breaks
A **cash break** (ledger vs bank) is usually fees, interest, FX, or unbooked wires. A **position break** (book vs custodian) is usually corporate actions, settlement timing, or lot mismatches. When both a cash break and a position break appear for the same security on the same date and are economically linked (e.g., a sale booked one side but not the other), clear them together — fixing one alone re-opens the other.
