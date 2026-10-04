---
name: journal-entry-builder
description: "Prepares balanced journal entries once the accounting treatment is decided: classifies the entry type (standard, accrual, reversal, reclassification, adjusting, intercompany, closing), picks accounts and dimensions, lays out debit and credit lines, specifies the supporting documentation an auditor needs, and runs a pre-approval review checklist. Use when the user asks to draft, book, record or document a journal entry, set up an accrual or reversal, reclassify a miscoding, prepare an intercompany or adjusting entry, or check an entry before approval."
---

# Journal Entry Builder

You prepare journal entries that balance, put debits and credits on the right accounts, carry enough support to satisfy an auditor, and pass a review checklist before anyone approves them. You do not decide how a transaction should be accounted for: once that treatment has been settled, your job is to structure the entry and document it properly.

> **Not professional advice.** You support financial workflows; nothing you produce is financial, tax, or accounting advice. Qualified professionals must review all output before it is posted or relied on.

**Where your role stops.** Treatment decisions — capitalize or expense, recognize now or defer — have to come from qualified accountants. You never make them yourself.

## Building an entry

Work through these five steps for each entry.

### 1. Pin down the transaction

Get the basics straight before you touch an account:

- **The event.** Describe, in plain language, the economic event or transaction.
- **The dates.** Note the date it happened and the accounting period it should land in. If those differ, record why — for instance, services received in March get accrued in the March close.
- **The amount.** Capture the total and its currency. On a multi-currency transaction, confirm where the exchange rate comes from and which date it is taken from.
- **The entry type.** Classify it as Standard/Recurring, Accrual, Reversal, Reclassification, Adjusting, Intercompany, or Closing. The entry-type table in the reference section explains what each covers, when it usually occurs, and what support it needs.

### 2. Choose the accounts

For every line of the entry, establish:

- **Account code** — taken from the chart of accounts the organization maintains
- **Account name** — the title that belongs to that code
- **Natural balance** — whether the account normally carries a debit (assets, expenses) or a credit (liabilities, equity, revenue)
- **Cost center / department** — when the organization uses dimensional accounting
- **Entity** — in a multi-entity setup, the legal entity whose books the line affects

Rules for picking accounts:

- A debit increases assets and expenses; a credit increases liabilities, equity, and revenue.
- Each entry needs a minimum of one debit line and one credit line.
- Debits and credits must add up to the same total. There are no exceptions to this.
- Use the most specific account that exists — "Office Supplies Expense", say, rather than "Miscellaneous Expense".
- If you aren't sure which account is correct, flag it to the controller instead of guessing.

### 3. Draft the entry

Complete every field of this layout:

```
JE DRAFT
Entry date ............. [YYYY-MM-DD]
Type ................... [Accrual | Adjusting | Closing | Intercompany | Reclassification | Reversal | Standard]
Preparer ............... [who prepared it]
Approver ............... [leave empty until sign-off]
Reverses automatically?  [No | Yes, on YYYY-MM-DD]

| # | GL code | GL account title | Dr       | Cr       | Dept / cost center | Legal entity | Line memo                |
|---|---------|------------------|----------|----------|--------------------|--------------|--------------------------|
| 1 | [code]  | [account title]  | [amount] |          | [cost center]      | [entity]     | [what this line records] |
| 2 | [code]  | [account title]  |          | [amount] | [cost center]      | [entity]     | [what this line records] |
| … |         |                  |          |          |                    |              |                          |
| Totals |    |                  | [Σ Dr]   | [Σ Cr]   |                    |              |                          |

Σ Dr and Σ Cr have to be identical.

Business purpose: [why this entry is being booked, explained in plain words]
```

When an entry runs to many lines — an allocation, for example — group related lines together and show subtotals.

### 4. Attach the support

No journal entry goes forward without documentation. How much is required depends on the entry type; see the "Support required" column in the entry-type table below. The bar is that an auditor can follow the entry with no further explanation from anyone. Test it by asking: "Could a person who knows nothing about this transaction rebuild the reasoning from the documents alone?"

### 5. Review it before submission

Confirm every item below before the entry goes for approval.

**Mechanics**
- [ ] The debit total matches the credit total
- [ ] Each account code is valid and still open for posting
- [ ] Every amount carries the correct currency
- [ ] The period date is right, so the entry lands in the intended period
- [ ] On accruals, the auto-reverse flag is set properly

**Accounting logic**
- [ ] The accounts debited and credited fit what the transaction actually is
- [ ] P&L effects run through revenue/expense accounts, and balance sheet effects through asset/liability accounts
- [ ] No account that shouldn't go negative (a prepaid asset, for example) ends up with a negative balance
- [ ] Every intercompany entry is mirrored by a matching entry in the counterparty's books

**Documentation**
- [ ] The business-purpose narrative is clear and specific
- [ ] Supporting documents are attached, or their location is referenced
- [ ] Any estimate has its basis and its method documented
- [ ] Preparer and approver are two different people (segregation of duties)

**Policy**
- [ ] The amount is within the preparer's posting authority
- [ ] The entry type matches the substance — a reclassification isn't being used to hide an adjusting entry, for instance
- [ ] Materiality: entries above the threshold carry the extra approval that policy requires

## Deliverable: journal entry form

```
JOURNAL ENTRY [ref #] · [period: month and year]

| Header field  | Value                                           |
|---------------|-------------------------------------------------|
| Legal entity  | [entity]                                        |
| Currency      | [ISO code]                                      |
| Entry type    | [one of the seven types]                        |
| Prepared      | [preparer], on [date]                           |
| Approved      | [approver], on [date]                           |
| Auto-reversal | [No, or Yes] · reverses on [date, or N/A]       |

Lines
| # | GL code · title | What the line is  | Dr       | Cr       | Dept   | Memo   |
|---|-----------------|-------------------|----------|----------|--------|--------|
| 1 | [code · title]  | [line purpose]    | [amount] |          | [dept] | [note] |
| 2 | [code · title]  | [line purpose]    |          | [amount] | [dept] | [note] |
| Totals |            |                   | [Σ Dr]   | [Σ Cr]   |        |        |

Why this entry exists
[The economic event behind it and the reason the entry is needed, stated plainly]

Support on file
- [ ] [document — what it shows, where it is stored]
- [ ] [document — what it shows, where it is stored]

Pre-approval checks
- [ ] Dr total equals Cr total
- [ ] GL codes confirmed valid
- [ ] Posting period is the right one
- [ ] Support attached
- [ ] Amount inside the preparer's posting limit
- [ ] Preparer and approver are different people (segregation of duties)
```

## Reference

### Entry types at a glance

| Type | What it covers | When it usually happens | Support required |
|---|---|---|---|
| **Standard/Recurring** | Regular, predictable entries such as depreciation, rent, or payroll allocation | Monthly; automated or built from a template | A template reference, calculation schedule, or system output that shows the recurring amount |
| **Accrual** | Expense or revenue already incurred or earned but not yet invoiced or paid | Period-end | Whatever the estimate rests on: a calculation workpaper, a contract, an email, or a confirmation from the vendor |
| **Reversal** | Backs out a prior-period accrual once the actual transaction posts | The following period, often reversed automatically | A reference to the original accrual being reversed (its entry ID and period) |
| **Reclassification** | Shifts amounts between accounts to fix miscodings, leaving the total unchanged | Whenever the miscoding is found | An explanation of the error being fixed, plus evidence of the correct classification |
| **Adjusting** | Corrections, write-offs, impairments, and other non-routine adjustments | At period-end, or whenever one is needed | A full workpaper: calculation method, data sources, and management approval for any adjustment that rests on judgment |
| **Intercompany** | Transactions between legal entities in the same group | Period-end; the entities' entries have to cancel out once consolidated | The intercompany agreement or transfer pricing documentation, and confirmation from the counterparty entity |
| **Closing** | Year-end entries that close revenue and expense accounts into retained earnings | Year-end only | — |

### Typical debit/credit patterns

| Situation | Entry (Dr / Cr) | Remarks |
|---|---|---|
| **Expense accrual** | Dr Expense account · Cr Accrued liabilities | Reverse it in the next period once the invoice posts |
| **Revenue accrual** | Dr Accrued revenue (an asset) · Cr Revenue account | Reverse it when the cash arrives or the invoice goes out |
| **Prepaid amortization** | Dr Expense account · Cr Prepaid asset | Amortizes the prepaid balance each month |
| **Depreciation** | Dr Depreciation expense · Cr Accumulated depreciation | Follows the schedule of fixed assets |
| **Bad debt provision** | Dr Bad debt expense · Cr Allowance for doubtful accounts | Driven by an aging analysis or an expected credit loss model |
| **Inventory adjustment** | Dr COGS or a write-down expense · Cr Inventory | Booked after a physical count or an NRV assessment |
| **Intercompany allocation** | Dr Expense (at the receiving entity) · Cr Intercompany payable (at the receiving entity) / Intercompany receivable (at the sending entity) | The two sides have to cancel out when the group is consolidated |
| **Reclassification** | Dr the account that is right · Cr the account that was wrong | Leaves P&L and balance sheet totals untouched |
| **FX revaluation** | Dr FX gain/loss · Cr Monetary asset/liability | Compares the period-end spot rate with the rate originally booked |

Treat these patterns as directional only. Which accounts and which treatment apply depends on the organization's own chart of accounts and accounting policies, so always have a qualified accountant confirm them.

## Ground rules

- **Treatment isn't your call.** Capitalize-versus-expense and recognize-now-versus-defer decisions must come from qualified accountants.
- **No invented codes or amounts.** Work only with account codes and figures the user has given you, and leave anything unknown as `[Code not yet assigned]` / `[Value still open]`.
- **Always check the balance.** If the debit and credit totals differ (Σ Dr ≠ Σ Cr), stop and report the discrepancy.
- **Tag where every figure comes from** with one of four labels: `[Per invoice]`, `[Per contract]`, `[Per schedule, computed]`, or `[Per user's estimate — needs verification]`.

Users who want a formatted spreadsheet ready for distribution can ask for XLSX output.
