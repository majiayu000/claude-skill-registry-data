---
name: expense-optimizer
description: >
  Find recurring expenses and subscriptions to cut or reduce.
---

# Expense Optimizer

## Overview
Analyze your transaction history to identify recurring expenses, unused subscriptions, duplicate services, and optimization opportunities. Surfaces actionable savings by detecting charges you may have forgotten about or services you could downgrade.

## Wilson Tools Used
- `transaction_search` — detect recurring charges by pattern and frequency
- `anomaly_detect` — flag subscriptions with price increases or irregular charges
- `spending_summary` — identify highest-spend recurring categories

## Workflow
1. Use `transaction_search` to find all transactions from the last 6 months.
2. Identify recurring charges by grouping transactions with similar descriptions and regular intervals (weekly, monthly, annual).
3. Build a recurring expense inventory:
   | Service | Monthly Cost | Frequency | Last Charged | Category |
   |---------|-------------|-----------|--------------|----------|
4. Use `anomaly_detect` to flag:
   - Subscriptions with recent price increases
   - Charges that stopped (possible cancellation or card expiry)
   - Services charged but not seen in a while (potential unused subscriptions)
5. Classify each recurring expense into optimization categories (see table below).
6. Present findings with estimated annual savings for each recommendation.
7. Summarize total potential savings.

## Optimization Categories

| Category | Description | Examples |
|----------|-------------|---------|
| Cancel | Services you likely don't use | Gym memberships with no related spending nearby, streaming services you haven't watched |
| Downgrade | Premium tiers you could reduce | Phone plan with unused data, cloud storage over 50% empty |
| Negotiate | Services with competitive alternatives | Internet, insurance, cell phone |
| Consolidate | Overlapping services | Multiple streaming, multiple cloud storage, multiple music services |
| Switch | Cheaper alternatives exist | Bank fees (switch to no-fee), high-interest debt (refinance) |
| Keep | Good value, actively used | No action needed |

## Without Wilson
To find recurring expenses manually:

### Step-by-Step in a Spreadsheet
1. **Export 6 months of transactions** from your bank as CSV.
2. **Sort by Description** alphabetically to group similar charges.
3. **Identify recurring charges**:
   - Filter for common subscription amounts: $4.99, $9.99, $12.99, $14.99, $15.99, $19.99
   - Search for keywords: `SUBSCRIPTION`, `RECURRING`, `MONTHLY`, `ANNUAL`, `RENEWAL`
   - Look for identical amounts from the same vendor appearing monthly
4. **Build your subscription inventory** in a new sheet:
   ```
   =SUMIFS(Amount, Description, "*NETFLIX*", Date, ">="&TODAY()-180) / 6
   ```
   This gives the average monthly cost for Netflix over the last 6 months.
5. **Detect price increases**: Compare the most recent charge to the oldest charge for each vendor:
   ```
   Current:  =INDEX(Amount, MATCH(1, (Description="*NETFLIX*")*(Date=MAX(IF(Description="*NETFLIX*",Date))), 0))
   Original: =INDEX(Amount, MATCH(1, (Description="*NETFLIX*")*(Date=MIN(IF(Description="*NETFLIX*",Date))), 0))
   ```
6. **Calculate annual cost**: `=MonthlyCost * 12`
7. **Sum potential savings**: Add up the annual cost of services you'd cancel, downgrade, or switch.

### Free Tools
- **Rocket Money** (formerly Truebill): Automatically detects and helps cancel subscriptions
- **Trim**: Negotiates bills on your behalf (takes a percentage of savings)
- **Bobby** (iOS app): Manual subscription tracker with renewal reminders

## Important Notes
- Recurring detection works best with 3+ months of transaction history. With less data, some annual charges may be missed.
- Annual charges (e.g., Amazon Prime, domain renewals) only appear once — Wilson looks back 12 months for these if data is available.
- Some services use different billing descriptors than their brand name (e.g., "GOOGLE *YouTube" for YouTube Premium). Wilson groups these by learning common aliases.
- This skill identifies candidates for optimization but does not cancel or modify any services on your behalf.
