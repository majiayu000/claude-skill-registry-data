---
name: smb-cash-flow
version: 1.0.0
description: Produce a 30/60/90-day cash-flow forecast from AR and AP with base/low/high confidence bands and shortfall alerts.
author: matrixx0070
tags: [small-business, cash-flow, forecast, ar, ap, runway, 13-week]
capabilities: []
---

# Cash Flow Forecast

## When to use
Use this when the owner needs to know whether cash will cover commitments over the next quarter — before an expense, a hire, or a large purchase, or when a lender or partner asks for a forward view.

**Not for:** the live one-glance snapshot (use smb-business-pulse) or historical reconciliation (use smb-close-month). This is forward-looking decision support, not a closed record.

## Method
1. **Set starting cash and horizon.** State today's bank balance and forecast the next 30, 60, and 90 days, weekly.
2. **Schedule inflows from AR.** List open receivables by expected pay date. Decision point: adjust each date by the customer's historical days-to-pay, not the invoice term — a net-30 invoice from a customer who always pays in 50 lands in week 7.
3. **Schedule outflows from AP.** List payables, payroll, rent, loan payments, taxes, and recurring subscriptions by due date.
4. **Roll the balance forward.** Compute projected ending cash for each week and at the 30/60/90 marks.
5. **Apply confidence bands.** Give a base case, a low case (late payers slip, no new sales), and a high case (on-time collections) as a range.
6. **Flag shortfalls.** Identify any week the balance dips below the owner's minimum buffer, and how large the gap is.

This is decision support; the owner approves any financing, delayed payment, or spending decision it informs.

## Example
Start $32k. Week 5 (base): inflows $18k, outflows $27k → ending $23k. Low case dips to $9k in week 6 — below the $15k buffer, a $6k gap driven by a $12k customer who historically pays 20 days late. Recommend: confirm that payment date or line up a short bridge. Owner decides.

## Pitfalls
- **Using invoice terms, not behavior.** Net-30 on paper, net-55 in practice — history is the truth.
- **Forgetting lumpy outflows.** Quarterly taxes, annual insurance, and loan balloons wreck an otherwise fine month.
- **A single point estimate.** Cash is a range; always show low/base/high, not one line.
- **Counting speculative new sales in the base.** Keep unclosed pipeline in the high case only.

## Output format
```
Starting cash: $__ | forecast date: <date>
Weekly (base):
| Week | Inflows | Outflows | Ending |
30/60/90 summary: base $__ | low $__ | high $__
Shortfall alerts: week __ — gap $__ — driver ___
Assumptions: days-to-pay used, items excluded
Recommended actions (owner approval required):
```

## Reference

### The 13-week direct cash-flow model (row layout)
The 13-week rolling forecast is the SMB and turnaround standard because it's short enough to be accurate and long enough to see trouble coming. Build columns as Week 1…Week 13 (dated Monday-start), plus an "Actual" column you fill each Friday to compare against forecast. Use this exact row order:

```
BEGINNING CASH (= prior week's ending)
  CASH INFLOWS
    + Customer collections (AR by expected pay date)
    + Cash/point-of-sale sales
    + Deposits / retainers received
    + Other (loan draw, tax refund, owner injection)
  = Total inflows
  CASH OUTFLOWS
    − Payroll & contractor pay
    − Payroll taxes & benefits
    − Rent / lease
    − Inventory / COGS / supplier payments (AP)
    − Loan & interest payments
    − Sales tax remittance
    − Estimated income tax
    − Insurance
    − Software / subscriptions
    − Marketing / ad spend
    − Owner draw / distributions
    − Other / one-off
  = Total outflows
NET CASH FLOW (inflows − outflows)
ENDING CASH (beginning + net)
  Minimum buffer line
  Surplus / (shortfall) vs buffer
```
The ending-cash row is the whole point — walk it left to right and mark any week where it crosses below the buffer line.

### Collection-probability haircuts by AR age
Don't book overdue receivables at face value. Discount expected collections by aging bucket, and slide the expected pay date by each customer's real days-to-pay:

| AR age bucket | Collect probability (haircut) | Timing assumption |
|---|---|---|
| Current (not yet due) | 95-100% | On the customer's historical avg days-to-pay |
| 1-30 days past due | 90% | Within 2-3 weeks |
| 31-60 days past due | 75% | Needs a reminder; slip to week 4-6 |
| 61-90 days past due | 50% | Active follow-up required |
| 90+ days past due | 20-30% | Treat as doubtful; base case excludes most of it |

In the **low case**, add ~10-14 days to every payer and drop each bucket one row (current behaves like 1-30, etc.). In the **high case**, everyone pays on term. Reality lands between low and base most quarters.

### Buffer thresholds and the shortfall response ladder
Set the minimum buffer at the larger of one month's fixed operating expense or 6 weeks of total burn. When a week breaches it, escalate cheapest-and-most-reversible first:
1. **Pull inflows forward** — call the top 2-3 overdue customers, offer a small early-pay discount, invoice work-in-progress now.
2. **Push outflows back** — negotiate supplier terms (net-30 → net-45), time discretionary spend (ad spend, owner draw) after the tight week.
3. **Trim** — pause non-essential subscriptions and postpone the non-urgent purchase.
4. **Bridge** — only if 1-3 don't close the gap: draw on a line of credit or arrange short-term financing. This is the owner's call and the last resort, not the first.

### Lumpy-outflow calendar (the killers)
Pre-load these into the right weeks or they'll blindside an otherwise healthy month: quarterly estimated income tax (mid-Apr/Jun/Sep/Jan), sales-tax remittance (monthly or quarterly), annual insurance renewals, equipment/lease balloons, year-end bonuses, and any annual software renewal. A month that looks fine on averages can go negative the week two of these land together.

### Owner-approval gate
This forecast is decision support, not an action. Drawing on credit, delaying a supplier payment, offering an early-pay discount, cutting spend, or making a hire are all owner decisions. Present the shortfall, the driver, and the ranked options — then wait for the owner to choose. Never move money or change a payment date on your own.
