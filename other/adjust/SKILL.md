---
description: Record accruals, deferrals, depreciation, and other period-end adjustments
---

# Adjust

Record adjusting entries for "$ARGUMENTS". Ensure revenue and expenses are recognized in the correct period by recording accruals, deferrals, depreciation, and estimates.

## Prerequisites

Read `.metapowers/accounting/$ARGUMENTS/04-trial-balance.md` for the unadjusted trial balance.

## Process

1. **Identify required adjustments:**
   - **Accrued revenues** — revenue earned but not yet billed or received
   - **Accrued expenses** — expenses incurred but not yet paid (wages, interest, taxes)
   - **Prepaid expenses** — payments made in advance that need to be expensed over time
   - **Unearned revenue** — cash received in advance that needs to be recognized as earned
   - **Depreciation** — allocate the cost of long-lived assets over their useful lives
   - **Allowances & estimates** — bad debt allowance, warranty reserves, inventory write-downs

2. **Create adjusting journal entries:**
   - For each adjustment, record:
     - **Type** — accrual, deferral, depreciation, or estimate
     - **Accounts** — debit and credit accounts
     - **Amount** — calculated adjustment amount with supporting calculation
     - **Rationale** — why this adjustment is necessary
   - Number entries sequentially (AJE-001, AJE-002, etc.)

3. **Validate adjustments:**
   - Each adjusting entry must have equal debits and credits
   - Verify that no operating transactions are included (those belong in Phase 2)
   - Confirm depreciation methods and useful lives are consistent with policy

4. **Write the artifact** to `.metapowers/accounting/$ARGUMENTS/05-adjust.md` with sections:
   - **Adjusting Journal Entries** — all entries with type, accounts, amounts, and rationale
   - **Adjustment Summary** — total adjustments by type
   - **Impact Analysis** — how adjustments affect net income and key account balances

## Output

The adjustments written to `.metapowers/accounting/$ARGUMENTS/05-adjust.md`. Present a summary highlighting:
- Number of adjusting entries by type
- Net impact on net income
- Largest adjustments by dollar amount
