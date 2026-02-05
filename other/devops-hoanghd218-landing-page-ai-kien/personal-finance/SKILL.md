---
name: personal-finance
description: Personal finance management with Lunch Money. Use when user mentions finances, budgeting, expense tracking, bank accounts, transactions, monthly finance routine, or financial file organization. Covers file organization, naming conventions, monthly reconciliation, and account setup.
---

# Personal Finance Management

Lunch Money-based finance tracking with organized file storage.

## File Organization

```
iCloud Drive/Finance/
├── 01-Inputs/           # Raw bank downloads (CSV, QFX, PDF statements)
├── 02-LunchMoney/       # Monthly full-exports from LM
└── 03-Documents/        # Receipts >$500 (tax, reimburse, warranty)
```

## Naming Conventions

**Bank downloads:**
`YYYY-MM_<bank>_<account>.csv`
`YYYY-MM_<bank>_<account>_statement.pdf`

**LM exports:**
`YYYY-MM_LM_all.csv`

**Receipts:**
`YYYY-MM_<merchant>_<amount>.pdf`

## Monthly Routine

1. **Export from LM:** All transactions → `02-LunchMoney/YYYY-MM_LM_all.csv`
2. **Download statements:** Chase, CapOne, Apple PDFs → `01-Inputs/`
3. **Reconcile:** Confirm LM balances match statement PDFs
4. **Clean transfers:** Mark credit card payments, internal transfers
5. **Categories:** Keep ≤35 total, merge similar ones

## Connected Accounts

- Chase checking/savings (auto-sync)
- Capital One cards (auto-sync, 3mo limit - supplement with CSV)
- Apple Card/Cash/Savings (iOS helper app)

## Receipt Policy

Keep only if: Tax-relevant, reimbursable, warranty, or >$500

## Troubleshooting

**Duplicate transactions:** Check if period was both imported (CSV) and synced (connector)
**Missing transactions:** Use manual CSV import to backfill
**Balance mismatch:** Cross-reference with PDF statement, look for pending transactions

## Exit Strategy

To plaintext (if needed):
1. Use latest `YYYY-MM_LM_all.csv` as seed data
2. Raw bank files in `01-Inputs/` provide verification
3. Transition to Beancount + Fava web interface
