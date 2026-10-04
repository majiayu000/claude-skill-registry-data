---
name: money-check
description: Quick P&L snapshot. Outstanding balances, overdue payments, upcoming deposits due, revenue forecast, profit margins. Use when user says "money check", "who owes me", "financials", "P&L", "how's money looking", or morning briefing needs financial status.
user-invocable: true
---

# Money Check - Financial Snapshot

Everything about money in one view. Who owes what, what's coming in, what's going out.

## Trigger Conditions

Auto-fire when:

- User says "money check", "financials", "P&L", "who owes me"
- User says "how's money looking", "cash flow", "outstanding balances"
- `/morning` needs a financial section
- `/status` needs money context

## Step 1: Gather Financial Data

Fetch in parallel:

### Outstanding Balances

Use `lib/finance/payment-reminder-actions.ts` -> `getEventsWithOutstandingBalances()`:

- Returns all non-terminal events with outstanding balance
- Includes event date, client name, amount, days until event

### Event Financial Summaries

Use `lib/ledger/compute.ts` -> `getEventFinancialSummary()` for active events:

- Quoted price, total paid, total refunded, expenses, tips
- Net revenue, outstanding balance, profit, profit margin
- Payment status

### Deposit Status

Use `lib/finance/deposit-actions.ts` -> `calculateDeposit()` for upcoming events:

- Deposit amount, deposit status (pending/partial/paid/overdue)
- Balance due date, balance status

### Revenue Forecast

Use `lib/finance/revenue-forecast-actions.ts`:

- Pipeline value (confirmed + probable)
- Monthly/quarterly projections
- Year-over-year comparison

### Recent Revenue

Query `lib/finance/index.ts` for this month and last month actuals.

## Step 2: Display Dashboard

```
MONEY CHECK [timestamp]
━━━━━━━━━━━━━━━━━━━━━━

OUTSTANDING BALANCES ($X,XXX total)
  Sarah M. - Wedding Jun 15    $1,500 due (8d to event)
  Mike R.  - Anniversary Apr 20  $800 due (OVERDUE, event passed)
  Corp Inc - Team Build Jun 22  $2,200 due (deposit pending)

DEPOSITS DUE
  Corp Inc - $1,100 deposit due Jun 8 (1d away!)
  Lisa K.  - $750 deposit due Jun 20 (ok)

THIS MONTH
  Revenue:    $4,200 (3 events)
  Expenses:   $1,890
  Profit:     $2,310 (55% margin)

LAST MONTH
  Revenue:    $6,800 (5 events)
  Expenses:   $2,720
  Profit:     $4,080 (60% margin)

PIPELINE (next 90 days)
  Confirmed:  $8,500 (4 events)
  Probable:   $3,200 (2 inquiries)
  Total:      $11,700

━━━━━━━━━━━━━━━━━━━━━━
ACTIONS:
  1. Collect from Mike R. ($800, event already passed)
  2. Send deposit invoice to Corp Inc (due tomorrow!)
  3. Follow up on 2 probable inquiries ($3,200 pipeline)
```

## Step 3: Recommend Actions

Prioritize by urgency:

1. **Overdue payments** (event passed, money owed) - highest
2. **Deposits due within 3 days** - critical
3. **Large outstanding balances** with events approaching
4. **Pipeline follow-ups** that could convert

For each, suggest a concrete next step (send invoice, call client, send reminder).

## One-Liner Mode

For `/morning` or `/status`:

```
MONEY: $4,500 outstanding (1 overdue). Pipeline: $11,700 next 90d. Margin: 55% MTD.
```

## Deep Dive Mode

If user says "deep dive" or "break it down":

- Show per-event P&L for last 3 months
- Food cost percentage trends
- Average profit per guest
- Best/worst margin events

Use `lib/finance/food-cost-actions.ts`, `lib/finance/margin-calculator.ts`, `lib/analytics/cost-trends.ts`.

## Key Files

- Outstanding balances: `lib/finance/payment-reminder-actions.ts`
- Event financial summary: `lib/events/financial-summary-actions.ts`
- Ledger compute: `lib/ledger/compute.ts`
- Deposit tracking: `lib/finance/deposit-actions.ts`
- Revenue forecast: `lib/finance/revenue-forecast-actions.ts`
- Food cost: `lib/finance/food-cost-actions.ts`
- Margin calculator: `lib/finance/margin-calculator.ts`
- Cost trends: `lib/analytics/cost-trends.ts`
- Client spending: `lib/clients/spending-actions.ts`
- Break-even: `lib/finance/break-even-actions.ts`
- Sales tax: `lib/finance/sales-tax-actions.ts`
- Tip tracking: `lib/finance/tip-actions.ts`
- Plate cost: `lib/finance/plate-cost-actions.ts`
- Revenue goals: `lib/revenue-goals/actions.ts`

## Rules

- NEVER fabricate financial numbers. All data from ledger/database.
- If ledger query fails, say so. Don't show $0 as if nothing is owed.
- Financial data is REAL MONEY. Show exact cents, not rounded.
- Always show outstanding balances first (that's actionable cash).
- Overdue = event date passed AND balance > 0. Flag prominently.
- Profit margin = (revenue - expenses) / revenue. Use ledger-computed values.
