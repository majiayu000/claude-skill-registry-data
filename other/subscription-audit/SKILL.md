---
name: subscription-audit
description: >
  Find recurring subscriptions, calculate total cost, and flag unused ones.
---

# Subscription Audit

## Overview
Scans your transaction history for recurring subscription charges, totals your monthly and annual subscription spend, identifies subscriptions with no recent usage pattern changes, and recommends cancellation candidates.

## Wilson Tools Used
- `anomaly_detect` — detect unused or forgotten subscriptions via type `unused_subscriptions`
- `transaction_search` — find all recurring charges and verify subscription patterns

## Workflow
1. Run `anomaly_detect` with `types: ["unused_subscriptions"]` to surface subscriptions that appear to be unused or redundant.
2. Run `transaction_search` with `query: "subscription OR recurring OR monthly"` and `months: 6` to pull all subscription-like transactions over the past 6 months.
3. Group results by merchant name and calculate the monthly charge amount for each subscription.
4. Sum all recurring charges to produce a total monthly subscription spend and annualized cost.
5. Cross-reference the anomaly detection results with the transaction list. Flag any subscription that appeared in the unused list.
6. Present a table with columns: Merchant, Monthly Cost, Annual Cost, Months Active, Status (Active / Flagged for Review).
7. Recommend cancellation candidates — prioritize subscriptions flagged as unused, then sort remaining by cost descending.
8. Calculate potential annual savings if all flagged subscriptions were cancelled.

## Without Wilson
1. Export transactions from your bank as a CSV file (Chase: Statements & Documents > Download Account Activity > CSV; Bank of America: Statements & Documents > Download Transactions).
2. Open the CSV in a spreadsheet (Google Sheets or Excel).
3. Sort by the Description column and look for repeating merchant names with consistent amounts.
4. Use a filter: in Google Sheets, add a helper column with `=IF(COUNTIF(B:B, B2) > 1, "Recurring", "One-time")` where column B is the merchant/description column.
5. Create a pivot table grouping by merchant name, summing the amounts, and counting occurrences.
6. Any merchant appearing monthly with a consistent amount is likely a subscription.
7. Multiply each monthly charge by 12 to get annual cost.
8. Review each subscription and ask: "Did I use this in the last 30 days?" Cancel anything you answer "no" to.
9. Common subscription merchants to search for: Netflix, Spotify, Hulu, Disney+, Amazon Prime, Adobe, Dropbox, iCloud, Google One, YouTube Premium, gym memberships, news subscriptions.

## Important Notes
- Subscription detection relies on pattern matching in transaction descriptions. Some merchants use varying names across charges.
- Annual subscriptions (charged once per year) may not appear in a 6-month window. Extend the search range to 12-18 months to catch these.
- Free trials that convert to paid subscriptions are easy to miss — look for small initial charges from unfamiliar merchants.
