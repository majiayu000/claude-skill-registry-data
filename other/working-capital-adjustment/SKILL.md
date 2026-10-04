---
name: working-capital-adjustment
description: Sets a normalised working-capital peg and the completion-accounts mechanism that settles it, for use when you need to know how much real money the closing adjustment moves.
---

# Working Capital Adjustment Agent

## When to use
Use this when a deal is priced cash-free debt-free and someone has to say what normal working capital is. The trigger is any signed LOI promising a purchase-price adjustment without defining the peg. Reach for it before drafting starts: the peg is negotiated once and then settled in cash.

## What it does
It produces a working-capital position: a defined net working capital metric, a peg normalised from a trailing monthly average, the completion-accounts mechanism that settles it, and a bridge from enterprise value to the seller's actual proceeds.

## Method
1. Fix the perimeter. Cash-free debt-free, and say what that means.
   - The seller keeps all cash and repays all debt at close, so the equity check is enterprise value plus cash, less debt, less any shortfall against the peg.
   - Every balance sits in exactly one bucket: cash, debt, debt-like, or working capital. An item in two buckets is paid for twice.

2. Define the metric line by line. Never write "current assets less current liabilities".
   - Schedule the included accounts — receivables, inventory, prepayments, payables, accruals — and exclude cash, borrowings, and tax.
   - Attach a worked sample at a recent month-end so both sides see the definition applied.

3. Classify the debt-like items explicitly. This is where value moves.
   - Stretched payables, deferred revenue, accrued bonuses, capex creditors, restructuring provisions, declared but unpaid dividends.
   - Each item argued into net debt cuts the price twice if it also sits inside the peg.

4. Scrub the history, then build the peg. Twelve monthly balances, not four quarter-ends.
   - Strip factoring, a year-end collections push, and one-off stock builds, restate onto one policy, then average twelve month-end balances so a seasonal business is not pegged at a trough.
   - For a fast grower a flat currency peg is stale by close; peg to a percentage of trailing revenue instead.

5. Write the completion-accounts mechanism. Settle the process before the numbers.
   - Who prepares the closing statement and by when, the review window, valid grounds for objection, and referral to an independent accountant on disputed items only.
   - Set the accounting hierarchy: the specified policies first, then the target's historical practice consistently applied, then the applicable standard.

6. Decide the settlement shape and bridge it. True-up, collar, or locked box.
   - A dollar-for-dollar true-up both ways, or a deadband so small variances trigger nothing, with a payment deadline and interest.
   - A locked box fixes the equity price at a past balance-sheet date with a leakage covenant and an interest ticker; it ends the argument but hands the buyer the trading result from then on.
   - Then bridge enterprise value, plus cash, less debt and debt-like items, plus or less the adjustment, to proceeds.

## Inputs
- Headline enterprise value and the earnings base behind it
- Monthly balance sheets for at least the last twenty-four months
- The seasonality profile, the growth trajectory, and the target's accounting policies
- Expected closing cash and debt, and the draft agreement's definitions of each

## Output format
- The cash-free debt-free framing, with every balance assigned to a bucket
- The working capital definition as an included and excluded line-item list
- The trailing monthly series and the peg derived from it, with the normalisations named
- The mechanism: preparer, deadlines, objection rights, dispute route, accounting hierarchy, settlement shape
- A bridge from enterprise value to seller proceeds
- Present all schedules in prose, never as markdown tables

## Example
For Ardwick Components (fictional, illustrative), enterprise value is 300 at 10.0x EBITDA of 30. Trailing twelve-month average net working capital is 42, and that becomes the peg. Completion accounts show 36 at close, a shortfall of 6, so the price falls by 6. The bridge runs 300 of enterprise value plus 12 of cash less 45 of debt, or 267, less the 6 shortfall: 261 to the seller. Had the peg been set on the month-end at signing, a seasonal trough of 34, the same 36 would have paid the seller 2 — an 8 swing on identical facts, worth 2.7 percent of headline value and 0.3 turns of EBITDA. A second trap sits in 3 of capex creditors booked inside payables: deducted again as debt-like, the seller funds them twice.
