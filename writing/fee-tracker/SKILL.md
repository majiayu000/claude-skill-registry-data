---
name: fee-tracker
description: "Tracks a project's design fee in docs/practice/fees.md: the contract fee by phase, percent complete as you state it, earned fee computed from the two, invoices as issued and as paid, and the aging of what is outstanding, with the arithmetic shown. Trigger on \"fee tracker\", \"how much have we billed\", \"earned vs billed\", \"unbilled\", \"outstanding invoices\", \"receivables\", \"invoice log\", \"fee-tracker\", or an invoice to record. Percent complete is your judgment and the skill never estimates it; fees, invoice amounts, and dates come from you, in your currency, and nothing is recalled or benchmarked. Estimating a fee before there is a contract is fee-estimator's job; this starts when the contract is signed. It is a project record, not accounting: no tax, no ledger, no payroll costs."
license: MIT
metadata:
  title: "Fee Tracker"
  summary: "Track earned fee against billed, invoice by invoice"
  discipline: "practice-contracts"
  tags: "Project Management"
---

# Fee Tracker

The fee side of a project is three numbers that drift apart: what the
contract says, what the work has earned, and what has actually been billed
and paid. Small firms lose real money in the gaps between them, usually by
forgetting the middle one. This keeps the three side by side, per project,
with the arithmetic visible.

## Scope and limits — read first

**What this does.** Maintains `docs/practice/fees.md`: the contract fee
broken by phase with its source, percent complete per phase as you state
it, earned fee computed from the two with the arithmetic shown, an invoice
log with issued, paid, and outstanding status, and an aging view of what
is unpaid as of a date you give. Answers "where are we against the fee"
from the file alone.

**What this does not do.**

- **It does not estimate anything.** Not the fee (`fee-estimator` does
  that, before the contract), not percent complete, not what a phase
  should cost. Percent complete is your professional judgment, stated by
  you, dated.
- It is not accounting. No tax, no ledger, no revenue recognition rules,
  no payroll or overhead costs. What it computes is arithmetic on the
  numbers you logged, for your own steering.
- It does not draft or send invoices, and it does not chase clients. It
  can tell you which invoice to chase.
- It does not track the office's costs or hours. Earned here means fee
  times progress, not effort spent.
- Additional services are logged as their own fee lines when you state
  them; whether something is an additional service is a contract question
  it does not decide.
- One project per file. Office-wide roll-ups are a different view this
  file feeds, not one it contains.

**What you need before starting.** The contracted fee and its phase
breakdown, from the agreement, cited. After that: progress statements,
invoices, and payments as they happen.

## Workflow

### Step 1. Bootstrap if needed

Check whether `docs/practice/fees.md` exists. If not, copy
`assets/fee-tracker-template.md` there and record the project, the
currency as the contract states it, and the fee table with the agreement
article each line comes from. If the project has no `docs/` folder at all,
confirm before creating one.

### Step 2. Record progress

When you state a phase's percent complete, record it with the date and
your one-line basis. The previous figure moves to the history, never
overwritten. Then recompute earned:

```
Phase <name>
  fee               <as contracted>  [cited]
  percent complete  <as stated, dated>
  earned            <arithmetic>
Earned to date      <sum across phases>
```

### Step 3. Record invoices and payments

One row per invoice: number, date, period or phase it bills, amount,
status `issued`, `paid`, `partial`, `disputed`, with dates. A payment
updates the row, dated; a partial payment records both figures.

### Step 4. Report

On "where are we", compute and show, as of the date you give:

```
Earned to date      <n>
Billed to date      <n>
Unbilled earned     <arithmetic>     <- the money being forgotten
Outstanding         <sum of unpaid invoices>
  aging             <each unpaid invoice, days since issue>
```

Unbilled earned is stated first. It is the number this file exists for.

### Step 5. Amendments

A fee change (amendment, additional service) is a new fee line with its
own source, never an edit to the original. The contract history stays
readable.

## Rules

- **Every fee line cites the agreement** or the amendment it comes from.
- **Percent complete is stated, dated, and attributed to you.** Never
  inferred from time elapsed, invoices sent, or drawings issued.
- **Show the arithmetic** on earned, unbilled, and aging, every time.
- **History over overwrite.** Progress and status changes append.
- **Currency as the contract states it.** No conversion, ever.
- Nothing is deleted; a cancelled invoice is marked `void`, dated.

## Anti-patterns

- Estimating percent complete from the calendar because a statement is
  overdue.
- Treating billed as earned, which hides exactly the gap that matters.
- Logging an amendment by editing the original fee table.
- Netting a disputed invoice out of the totals so the report reads clean.
- Turning the file into a time sheet. Effort is a different axis.

## Resources

- `assets/fee-tracker-template.md` — the file this creates, empty.

No reference files. The numbers come from your contract and your invoices,
not from here.
