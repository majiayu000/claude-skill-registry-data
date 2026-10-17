---
name: audit-workpaper
description: >
  Write a clear, reviewable audit workpaper documenting procedures, evidence, and
  conclusions. Use when an auditor says "write a workpaper", "document this audit
  procedure", "tick and tie this", "I need to document my testing", "substantive
  testing workpaper", "controls testing documentation", "audit evidence memo",
  "prepare the workpaper for this balance", "document the audit steps I performed",
  or needs to capture any audit work in a format that supports review and sign-off.
  Also trigger when someone has completed audit testing and needs to write it up
  even if they don't use the word "workpaper".
---

## Reference Files

- `references/assertions-by-area.md` - Maps each financial statement area (AR, revenue, AP, cash, inventory, fixed assets, debt, equity, accruals) to standard assertions and typical audit procedures. Read this in Step 1 when selecting assertions and in Step 4 when designing procedures for the account being tested.

## Overview

Based on **"Auditing and Assurance Services"** by Arens, Elder, and Beasley - the standard reference for audit methodology. A workpaper is not a record of what you did; it is evidence that you did sufficient, appropriate work to support your conclusion. The reviewer should be able to pick up the workpaper, understand the objective, trace every tick mark back to a source document, and evaluate the conclusion - without asking the preparer a single question.

PCAOB AS 1215 and AICPA AU-C 230 both require that workpapers be complete enough to allow an experienced auditor with no prior connection to the engagement to understand the work performed.

## Workflow

### Step 1: Write the workpaper header

Every workpaper starts with a standard header that identifies what it covers and where it lives in the audit file.

```
CLIENT: [client name]
ENGAGEMENT: [audit / review / agreed-upon procedures]
PERIOD END: [date]
WORKPAPER REF: [e.g., B-3, or PBC-12]
AREA: [e.g., Accounts Receivable, Revenue, Cash]
ASSERTION(S) TESTED: [existence / completeness / accuracy / valuation / cutoff / rights & obligations / presentation]
PREPARED BY: [initials]   DATE: [date]
REVIEWED BY: [initials]   DATE: [date]
```

Assertions are the anchor. Every procedure in the workpaper must link back to the assertion(s) it tests. If you cannot state which assertion a procedure addresses, remove it.

### Step 2: State the objective

Write one or two sentences that define what the workpaper is meant to conclude. This drives everything that follows.

Example:
```
OBJECTIVE
To obtain sufficient appropriate evidence that accounts receivable at [date]
exists, is accurately stated at net realizable value, and represents amounts
owed by customers for goods or services delivered (existence, valuation, rights).
```

If the objective is vague, the procedures will be unfocused and the conclusion will be unsupportable.

### Step 3: Document the source data and population

Before describing procedures, document what you started with.

```
POPULATION / SOURCE DATA
Source: [e.g., AR aging report exported from [ERP] on [date], provided by [client contact]]
Population total: $[amount]  ([X] items)
Agreed to: [TB line / lead schedule ref]  confirmed
Stratification: [if sampling, document how population was stratified]
Sampling method: [random / haphazard / systematic / full population]
Sample size: [n] - basis: [risk-based / statistical / tolerable misstatement $X]
```

Tracing the population to the trial balance before testing eliminates a common deficiency: testing from a list that does not agree to the financial statements.

### Step 4: Document procedures performed

For each procedure, use this format: procedure - evidence - result.

```
PROCEDURE 1: [Concise description of what was done]
Evidence: [What document, system, or confirmation was used]
Result: [What was found - agree / exception / N/A]
Tick mark: [assign a symbol, e.g., check = agreed to source, ^ = recalculated]
```

Example:
```
PROCEDURE 1: Agreed sample AR balances to signed customer invoices on file.
Evidence: Invoices obtained from client PBC folder [tab: AR Support].
Result: All 25 sample items agreed to invoice amounts. No exceptions.
Tick mark: check = agreed to invoice

PROCEDURE 2: Confirmed 10 balances over $50K directly with customers via
positive confirmation. Sent [date], responses received by [date].
Evidence: Signed confirmation letters filed in [workpaper ref: B-4].
Result: 9 of 10 confirmed without exception. 1 difference noted - see exception below.

EXCEPTION: Customer [X], confirmed balance $142,500 vs. book $148,000. Difference
of $5,500. Client explanation: credit memo issued [date], not yet posted. Credit memo
reviewed and agreed to [doc]. Resolved - no misstatement.
```

### Step 5: Summarize tick mark legend

List every symbol used in the workpaper with its definition.

```
TICK MARK LEGEND
check  = Agreed to source document (invoice, contract, bank statement)
^      = Independently recalculated
diamond = Confirmed directly with third party
F      = Footed (column totals verified)
CF     = Cross-footed (row and column totals reconciled)
TB     = Agreed to trial balance / lead schedule
PY     = Agreed to prior year workpaper [ref]
```

Every tick mark in the workpaper body must appear in this legend. Unexplained tick marks are a common review finding.

### Step 6: Write the conclusion

The conclusion must directly answer the objective. It is not a summary of what was done.

```
CONCLUSION
Based on procedures performed, we obtained sufficient appropriate evidence that
accounts receivable of $[amount] at [date] exists, is accurately stated, and
represents valid customer obligations (existence, valuation, rights assertions).
No exceptions were noted that, individually or in aggregate, represent a material
misstatement. This balance is supported for audit sign-off.
```

If exceptions were found, state whether they were resolved and whether they affect the conclusion. Never write a clean conclusion when there are unresolved exceptions.

## Anti-Patterns

**1. Procedure without result**
Bad: "Reviewed accounts receivable aging for unusual items."
Good: "Reviewed accounts receivable aging report for items over 90 days and any credit balances. Identified 3 balances over 90 days totaling $28K. Obtained client explanation for each - see detail below. No exceptions noted."
Procedures without results are not audit evidence.

**2. Conclusion that does not match the objective**
Bad: Objective tests existence; conclusion says "balances are reasonable."
Good: Conclusion directly addresses the assertion(s) in the objective: existence, accuracy, valuation.
Mismatched objectives and conclusions signal a copy-paste error or that the conclusion was written before the work.

**3. Population not agreed to the trial balance**
Bad: Testing a sample from the AR aging without confirming the aging total agrees to the GL.
Good: Always foot the population and agree it to the trial balance before selecting the sample. A difference between the aging and the GL must be resolved before testing.

**4. Unexplained exceptions left in the file**
Bad: "Difference of $5,500 noted. Not investigated."
Good: Every exception must be investigated, explained, and resolved. Either it is a misstatement (quantify it, add to the summary of misstatements), or it is explained and cleared. Unresolved exceptions cannot be signed off.

**5. Workpaper requires the preparer to explain it**
Bad: A workpaper so brief or cryptic that the reviewer has to ask what it means.
Good: The reviewer should be able to pick up the workpaper and understand the objective, evidence, and conclusion without asking a question. If that test fails, add more detail.

## Quality Checklist

- [ ] Header complete: client, period, ref, assertions, preparer, reviewer
- [ ] Objective states the specific assertion(s) being tested
- [ ] Population agreed to trial balance before testing
- [ ] Source of population documented (system, date, who provided)
- [ ] Each procedure has: description, evidence source, and result
- [ ] All tick marks defined in a legend
- [ ] Exceptions documented with investigation and resolution
- [ ] Conclusion directly answers the objective
- [ ] Conclusion is clean only if all exceptions are resolved
- [ ] Workpaper is self-contained - no reviewer questions required
