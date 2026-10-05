---
name: multi-entity
description: >
  Manage finances across multiple businesses or legal entities.
---

# Multi-Entity Financial Management

## Overview
Track and report on finances across multiple businesses, LLCs, or legal entities from a single view. Prevents commingling, generates per-entity reports, and provides a consolidated overview.

## Wilson Tools Used
- `transaction_search` — query transactions filtered by entity (using account, tag, or category prefix) to isolate each business
- `spending_summary` — generate per-entity spending summaries for comparison
- `export_transactions` — export entity-specific transaction sets for accountants or tax filing

## Workflow
1. Ask the user to define their entities and how they are separated (separate bank accounts, category prefixes, tags, or description patterns).
2. For each entity, use `transaction_search` with the appropriate filter:
   - By account: search transactions from the specific bank account
   - By tag/prefix: search for transactions tagged or prefixed with the entity name (e.g., "LLC1:" or "rental:")
3. Use `spending_summary` for each entity over the same period.
4. Generate per-entity P&L summaries plus a consolidated view:

```
MULTI-ENTITY SUMMARY — [Period]
═══════════════════════════════════════════════════════
                    Entity A    Entity B    Consolidated
                    (Consulting) (SaaS)
───────────────────────────────────────────────────────
Revenue              $45,000     $22,000       $67,000
Expenses            ($28,000)   ($18,000)     ($46,000)
Net Income           $17,000      $4,000       $21,000
Net Margin             37.8%       18.2%         31.3%

Cash Balance         $32,000     $14,000       $46,000
───────────────────────────────────────────────────────
Inter-Entity Transfers: $2,500 (A → B)
═══════════════════════════════════════════════════════
```

5. Flag any inter-entity transfers (payments between your own accounts/entities) and exclude them from revenue and expense totals to avoid double-counting.
6. Use `export_transactions` to create separate CSV files per entity for tax preparation.
7. Alert on commingling: flag personal expenses in business accounts or business expenses in personal accounts.

## Without Wilson
1. If each entity has a separate bank account (recommended), export each account's transactions as a separate CSV file.
2. If entities share a bank account (not recommended but common), export all transactions and add an "Entity" column. Tag each transaction manually.
3. Create separate spreadsheet tabs per entity. For each: pivot by category, sum income and expenses.
4. For the consolidated view, create a summary tab that references each entity tab: `=EntityA!TotalRevenue + EntityB!TotalRevenue`.
5. Track inter-entity transfers: search for transfers between your accounts. Mark these as "Transfer" category and exclude from income/expense totals.
6. For tax filing, each entity files separately. LLCs file Schedule C (single-member) or Form 1065 (multi-member). S-corps file Form 1120-S. Keep transaction exports separated by EIN.
7. Use separate QuickBooks files or Xero organizations per entity. QBO allows up to 25 companies per subscription.

## Important Notes
- Separate bank accounts per entity is strongly recommended. Commingling funds can pierce the corporate veil and remove liability protection.
- Inter-entity transactions (loans, payments, shared expenses) must be tracked carefully. They are not income or expenses — they are transfers.
- If one entity pays a shared expense (e.g., office rent), split it proportionally and record an inter-entity receivable/payable.
- Each entity should have its own EIN. Do not use one EIN for multiple entities.
- Consult a CPA for multi-entity tax strategy. Entity structure (LLC, S-corp, C-corp) significantly affects tax liability.
