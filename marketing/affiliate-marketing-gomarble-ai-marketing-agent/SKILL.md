---
name: affiliate-marketing
description: "Use for affiliate and partner marketing on impact.com: partner performance, commission spend, conversions and payouts, which partners drive profitable orders, program-level results, invoices owed, and how affiliate spend compares with paid media. Read-only through GoMarble."
---

# Affiliate marketing (impact.com)

Analyze affiliate and partner programs on impact.com through GoMarble. The connector reads impact.com; it can't change partners, contracts or payouts.

## Setup

1. `impact_list_accounts` first. **Every other impact.com tool needs the `account_id`.**
2. `impact_list_programs` early. impact.com calls programs "campaigns", and most reports need a `program_id`.

## Tools

| Need | Tool |
|---|---|
| Commission spend and conversions for a program or partner, with breakdowns | `impact_get_partner_spend` (needs `program_id` and dates) |
| Individual conversions: order ID, payout, status, clearing dates | `impact_get_conversion_details` (needs `program_id` and dates) |
| Partners and their relationship status | `impact_list_partners` |
| Any impact.com report: clicks, actions, revenue, cost | `impact_list_reports` to find it, `impact_get_report_metadata` to see its filters and columns, then `impact_run_report` |
| What the brand owes partners | `impact_list_invoices`, and `impact_get_invoice` for line items |

Check a report's accepted filters with `impact_get_report_metadata` before running it; impact.com silently ignores filters it doesn't accept. An empty result means no data, not an error.

## How to analyze

- **Spend vs revenue.** `ActionCost` / `action_cost` is what the brand pays (commission), not revenue. Report cost per order and commission as a share of revenue.
- **Partner quality.** Rank partners by profitable orders, not clicks. Watch for partners with high reversal or rejection rates, coupon and cashback partners claiming orders that would have happened anyway, and last-click partners taking credit for paid media's work.
- **Clearing.** Recent conversions may still be pending or reversed. Say how much of the period has cleared.
- **Against paid media.** Compare affiliate cost per order with paid media CPA from the same period, and reconcile orders with Shopify (`shopify-order-discipline`) so the same order isn't counted twice.

## Output

Program and partner performance (orders, revenue, commission, cost per order), the partners worth growing or reviewing, what's still pending, and recommendations written as impact.com steps.

For a cross-channel view, use `build-reports`.
