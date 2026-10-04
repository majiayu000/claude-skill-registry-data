---
name: smb-tax-prep
version: 1.0.0
description: Assemble tax-season materials — quarterly estimates or year-end 1099s — plus an organized accountant packet.
author: matrixx0070
tags: [small-business, tax, quarterly, 1099, accountant, packet]
capabilities: []
---

# Tax Prep

## When to use
Use this ahead of a quarterly estimated-tax deadline or at year-end to organize what the owner needs to file or hand to their accountant — so nothing is missed and the accountant's time isn't spent on cleanup.

**Not for:** tax advice or filing (the owner and a licensed accountant review and file); submitting payments or forms; bookkeeping reconciliation (use smb-month-end-prep).

## Method
1. **Set the job.** Quarterly estimate or year-end (1099s, annual packet), and the period/deadline.
2. **Summarize income and expenses.** Revenue and deductible expenses by category from the books for the period.
3. **For quarterly estimates.** Compute estimated taxable income, apply the owner's effective rate or safe-harbor basis, show the estimated payment and due date. Decision point: label the tax figure an estimate, not filed advice, every time.
4. **For year-end 1099s.** List contractors paid over the reporting threshold, flag missing W-9s/TINs, total per payee. Decision point: an incomplete W-9 is a stop-and-collect before filing, not a guess.
5. **Build the accountant packet.** P&L, category totals, reconciliations, asset purchases, and open questions in one organized handoff.
6. **List gaps.** Missing receipts, uncategorized spend, unanswered items. The owner and accountant review, approve, and file; do not submit payments or forms.

## Example
Q2 estimate. Income $62,000, deductible expenses $28,000 → taxable ~$34,000. Owner's effective rate 22% → estimated payment ~$7,480, due June 15 (estimate only — confirm with accountant). Gaps: 4 expenses uncategorized ($1,900), 2 receipts missing. Packet: P&L, category totals, open questions. Handed to the owner to review before it reaches the accountant.

## Pitfalls
- Presenting an estimate as a filed or final number — always label it and point to the accountant.
- Filing 1099s with incomplete W-9/TIN data instead of flagging and collecting first.
- Missing contractors that crossed the reporting threshold across multiple small payments.
- Handing over a packet with uncategorized spend, forcing the accountant into cleanup you could have flagged.

## Output format
- **Job type / period / deadline.**
- **Income & expense summary** by category.
- **Quarterly:** estimated taxable income | estimate | due date (estimate only).
- **1099s:** payee | amount | W-9 status | threshold flag.
- **Accountant packet contents.**
- **Gaps & open questions** (for owner/accountant); nothing filed or paid without their sign-off.

## Reference

### Quarterly estimated-tax deadlines (US federal)
| Quarter | Income period | Due date |
|---------|---------------|----------|
| Q1 | Jan 1 – Mar 31 | Apr 15 |
| Q2 | Apr 1 – May 31 | Jun 15 |
| Q3 | Jun 1 – Aug 31 | Sep 15 |
| Q4 | Sep 1 – Dec 31 | Jan 15 (next year) |
(If a date falls on a weekend/holiday, it shifts to the next business day. State estimates often mirror these — confirm the owner's state.)

### Safe-harbor rule (avoid the underpayment penalty)
Pay at least the **smaller** of: 90% of *this* year's tax, or **100% of last year's** total tax (**110%** if last year's AGI > $150k). Meeting safe harbor means no underpayment penalty even if you owe more at filing. Rough estimate path when books are clean: `taxable income × effective rate ÷ remaining quarters`. Always label it an estimate, never filed advice.

### Self-employment tax reminder
Sole props, partners, and most LLC members owe **SE tax = 15.3%** (12.4% Social Security up to the annual wage base + 2.9% Medicare, no cap) on net self-employment earnings, **on top of** income tax. Half of SE tax is deductible above the line. S-corp owners pay this only on reasonable W-2 wages, not distributions — a common planning point to flag to the accountant.

### 1099 reference (year-end)
| Form | Who gets it | Threshold | Notes |
|------|-------------|-----------|-------|
| 1099-NEC | Non-employee contractors, freelancers, unincorporated vendors for services | **$600+** in the year | Due to recipient **and** IRS by **Jan 31** |
| 1099-MISC | Rent, prizes, other income | $600+ (rent, etc.) | Due to recipient Jan 31; IRS Feb/Mar |
| 1099-K | Paid via card/third-party platforms | Platform-reported | Don't double-report platform-paid amounts as NEC |
- **No 1099 needed** for payments to C- or S-corporations (except legal fees), or for goods.
- **Aggregate small payments** — $200 + $250 + $300 to one contractor = $750 → over threshold, must file.
- **Collect a W-9 before paying**, not at year-end. Missing TIN = stop-and-collect, not a guess. Missing/late 1099 penalties run $60-$310+ per form.

### Accountant packet — document checklist
- Year/period **P&L** and **balance sheet**.
- **Expense category totals** (mapped to Schedule C / tax buckets).
- **Bank + credit-card reconciliations** (all accounts tied out).
- **Asset purchases** over the de-minimis threshold (for depreciation / Section 179).
- **Payroll reports** (941s, W-2/W-3 if applicable).
- **1099 contractor list** with W-9s and amounts.
- **Mileage log** and home-office square footage (if claimed).
- **Loan statements** (interest is deductible; principal isn't).
- **Prior-year return** and any estimated payments already made (dates + amounts).
- **Open questions** list — anything you couldn't categorize.

### Common deductible categories (Schedule C buckets)
Advertising, car/mileage, contract labor, supplies, rent, utilities, insurance, professional fees, software/subscriptions, travel, meals (generally 50%), home office, depreciation, bank/merchant fees, education.

### Gaps to surface before handoff
Uncategorized transactions, missing receipts over the substantiation threshold, personal-vs-business commingling, missing W-9s, and any estimated payments the owner made that aren't recorded.

### Boundary
This skill organizes and estimates. It does not give tax advice, file returns, or submit payments. The owner and a licensed accountant review, approve, and file everything.
