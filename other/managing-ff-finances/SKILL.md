---
name: managing-ff-finances
metadata:
  version: "2.0.0"
description: >
  Manages FlashFusion's business finances as a sole-proprietor consulting operation — invoice
  lifecycle, revenue tracking, P&L basics, and cash flow visibility. Separate from managing-
  personal-finances (credit, subscriptions, personal cash). Activates on FlashFusion invoice,
  client payment, revenue tracking, P&L, profit and loss, business expenses, quarterly
  finances, cash flow, outstanding invoices, deductibles, how much have I made, what do I owe,
  how much is outstanding. Not for engagement pricing strategy and not for personal finances
  (use managing-personal-finances).
---

## When to Use / When NOT

**Use when** — reviewing FlashFusion invoices, revenue, P&L, cash flow, outstanding payments, or business tax set-aside.

**Do NOT use when** — pricing an engagement (that is strategy, not bookkeeping) or reviewing personal credit and subscriptions (use managing-personal-finances).

# FlashFusion Finance Manager

Covers the financial operation of FlashFusion as a sole proprietor consulting
business. Not accounting software — a discipline system for the habits that
prevent surprises.

---

## Evals

**Should trigger:**
1. "How much has FlashFusion invoiced this quarter and how much has actually collected?"
2. "Help me track this new client payment and make sure taxes are set aside"
3. "What are my outstanding invoices right now?"

**Should NOT trigger:**
1. "How should I price this engagement?" — pricing strategy, not finance management
2. "Check my personal credit score" — use managing-personal-finances

---

## Section 1: Invoice Lifecycle

Every FlashFusion engagement generates one or more invoices. Track every
invoice through to collection. Gaps in this tracking = revenue surprises.

### Invoice states

```
DRAFT      → created, not yet sent
SENT       → sent to client, awaiting payment
OVERDUE    → past due date (Net-15: 15+ days since sent)
COLLECTED  → payment received
DISPUTED   → client has raised an issue
```

### Log format

Maintain in `FlashFusion/Finance/Revenue/{{YYYY}}-invoices.md`:

```
| Date Sent | Client | Invoice # | Amount | Due Date | Status | Collected Date |
|-----------|--------|-----------|--------|----------|--------|----------------|
```

### Follow-up cadence

- **Day 0:** Invoice sent
- **Day 15:** If unpaid → first follow-up (friendly reminder)
- **Day 25:** If unpaid → second follow-up (reference the contract terms)
- **Day 35:** If unpaid → escalate per contract late payment clause

Do not let invoices drift past 15 days without a follow-up. The follow-up
at day 15 closes most gaps.

### When an invoice is collected

1. Update status to COLLECTED with the date
2. Transfer 28–30% to tax account immediately (see managing-personal-finances)
3. Check for any other outstanding invoices

---

## Section 2: Revenue Tracking

### Quarterly revenue summary

At the end of each quarter, calculate:

```
Gross revenue:          sum of all COLLECTED invoices in the quarter
Outstanding:            sum of all SENT but not COLLECTED
Written off:            any amounts abandoned (document why)
Quarter-over-quarter:   compare to prior quarter
```

Store in `FlashFusion/Finance/Revenue/{{YYYY}}-quarterly-summary.md`

### Revenue by engagement type

Track which service type generates the most revenue:
- Workshop
- Audit
- Implementation build
- Retainer
- Training

This informs pricing, positioning, and where to focus pipeline energy.
If audits close fastest and workshops produce the most revenue, focus
pipeline on workshops and use audits as the entry offer.

---

## Section 3: Business Expenses and P&L

### P&L formula (sole proprietor, simplified)

```
Revenue (collected)
- Business expenses (deductible)
= Gross profit (before taxes)
- Self-employment tax (~15.3% on net profit)
- Federal income tax (marginal rate on remaining)
- Illinois state tax (4.95% flat)
= Net income
```

### Expense tracking

Log all business expenses throughout the year — do not reconstruct at tax time.

`FlashFusion/Finance/Expenses/{{YYYY}}-expenses.md`:

```
| Date | Vendor | Amount | Category | Business Purpose |
|------|--------|--------|----------|-----------------|
```

**Likely FlashFusion deductible categories:**
- Software and SaaS (Claude, Vercel, Supabase, Notion, n8n, all tools used for client work)
- Domain and hosting (flashfusion.co, all platform costs)
- Equipment (laptop, monitor, peripherals — if purchased for business)
- Home office (requires dedicated space, consistent use — consult CPA before claiming)
- Professional development (courses, books, conferences)
- Internet (partial — proportional to business use)
- Contractor payments (if you bring in subcontractors)
- Business meals (50% deductible if business purpose documented)

**Not deductible:** personal subscriptions, personal meals without business context

### Quarterly P&L check

Each quarter:
1. Sum collected revenue
2. Sum documented expenses
3. Rough gross profit = revenue - expenses
4. Confirm tax account has ~28-30% of gross profit set aside

---

## Section 4: Cash Flow Visibility

Cash flow = money coming in vs. money going out, and when.

The common consulting cash flow problem: invoices outstanding for weeks
means you have "earned" revenue that isn't in your account. Track the
difference between earned and collected.

### Monthly cash flow check

```
Collected this month:     ${{X}}
Outstanding invoices:     ${{Y}} (expected to collect within 30 days)
Upcoming expenses:        ${{Z}} (subscriptions, tools, estimated tax)
Buffer:                   ${{collected + outstanding - upcoming}}
```

If buffer is negative or thin: follow up aggressively on outstanding
invoices before taking on new expenses.

### Estimated tax deadlines

Carried from managing-personal-finances for business income:
- April 15 (Q1: Jan–Mar income)
- June 15 (Q2: Apr–May income)
- September 15 (Q3: Jun–Aug income)
- January 15 (Q4: Sep–Dec income)

---

## Self-Verification

Monthly:
- [ ] All invoices logged with current status
- [ ] Invoices 15+ days outstanding have a follow-up scheduled or sent
- [ ] Tax account has correct set-aside for collected income

Quarterly:
- [ ] Revenue summary calculated and logged
- [ ] Expense log current (no missing months)
- [ ] Estimated tax payment made or confirmed upcoming

---

## CLAIMS
- Invoices followed up at day 15 consistently collect faster than
  invoices followed up "when I remember" — the cadence matters more
  than the message
- Tracking revenue by engagement type quarterly surfaces the highest-ROI
  service line within two or three quarters of data

## COUNTEREXAMPLE
- The 28–30% tax set-aside rate is an estimate; at higher income levels
  or with significant deductions, actual tax liability differs — this
  skill is a discipline system, not a replacement for a CPA

## CONTRADICTIONS
- "Track all expenses throughout the year" conflicts with the reality
  of busy quarters; if you've fallen behind, reconstruct from bank
  statements and credit card records rather than skipping it — incomplete
  is better than absent

## FAIL Conditions

Named failure modes for this skill. Each is a hard stop, not a warning.

- **Marking an invoice collected before the funds clear the bank** → phantom cash flow — reconcile against the actual bank deposit, not the invoice status.
- **Setting aside tax at a flat rate without checking actual bracket and deductions** → under-withholding surprise — the 28–30% set-aside is a floor estimate, confirm liability with a CPA at year-end.
- **Commingling personal and business expenses in the P&L** → wrong deductions and audit exposure — keep separate accounts, route personal to managing-personal-finances.
- **Spending against earned-but-not-collected revenue** → cash crunch — track collected separately from outstanding, only the collected figure is spendable.
- **Skipping a quarterly estimated-tax deadline** → IRS penalty plus a lump-sum shock — the four dates (Apr 15, Jun 15, Sep 15, Jan 15) are hard.
- **Reconstructing expenses from memory instead of records** → missed deductions or inflated numbers — reconstruct from bank and card statements, incomplete beats invented.
