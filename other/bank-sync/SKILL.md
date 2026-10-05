---
name: bank-sync
description: >
  Connect bank accounts for automatic transaction import via Plaid.
---

# Bank Sync

## Overview
Connect your bank accounts for automatic, recurring transaction imports using the Plaid API. Once connected, Wilson pulls new transactions daily without manual CSV exports. Supports checking, savings, and credit card accounts from thousands of financial institutions.

**Note: Plaid integration requires a Wilson Pro license.**

## Wilson Tools Used
- `transaction_search` — verify imported transactions and check for duplicates
- `categorize` — auto-categorize newly synced transactions

## Workflow
1. Verify the user has a valid Wilson Pro license.
2. Launch the Plaid Link flow to connect a bank account:
   - User selects their financial institution
   - User authenticates with their bank credentials
   - User selects which accounts to sync
3. Store the Plaid access token securely in the local database.
4. Perform an initial sync to pull the last 30 days of transactions.
5. Deduplicate against any previously imported transactions.
6. Run `categorize` on newly synced transactions.
7. Report sync results: new transactions, duplicates skipped, accounts connected.
8. Set up daily automatic sync (runs on next Wilson session start).

## Without Wilson
If you don't have Wilson Pro or prefer manual imports, here are alternatives for each major bank:

### Manual Export Schedule (Recommended Monthly)

**Chase:**
- chase.com > Account > Download account activity > CSV
- Or set up Chase email alerts for transactions over a threshold

**Bank of America:**
- bankofamerica.com > Account > Information & Services > Download transactions > CSV
- BofA also supports auto-export to Quicken/QuickBooks

**Wells Fargo:**
- wellsfargo.com > Account > Download Account Activity > Comma Delimited

**Citi:**
- citibank.com > Account > View Activity > Download (CSV, OFX, QIF)

**Capital One:**
- capitalone.com > Account > Download Transactions > CSV

**American Express:**
- americanexpress.com > Statements & Activity > Download your Transactions > CSV

### Free Plaid Alternatives
- **Monarch Money** ($9.99/mo): Automatic bank sync with budgeting
- **Lunch Money** ($10/mo): Developer-friendly, CSV import + Plaid sync
- **Actual Budget** (free, self-hosted): Manual import with OFX support
- **GnuCash** (free): OFX direct download from some banks

### Automation Without Plaid
- Set calendar reminders to export CSV monthly from each bank
- Use the `import-transactions` skill to import each file
- Some banks support OFX Direct Connect — GnuCash and KMyMoney can pull transactions automatically without Plaid

## Important Notes
- Plaid credentials are stored locally in your Wilson database — they never leave your machine.
- Bank sync uses Plaid's transaction sync API, which handles deduplication server-side.
- Some institutions require re-authentication every 90 days (Plaid will prompt you).
- Plaid supports 12,000+ financial institutions in the US, Canada, and UK.
- If a bank connection breaks, Wilson will notify you and offer to re-authenticate or fall back to manual CSV import.
