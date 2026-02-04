---
name: alphavantage-earnings
description: Consensus estimates and earnings data from Alpha Vantage.
---

# Alpha Vantage Earnings

## EARNINGS_ESTIMATES

Returns forward and historical consensus:
- `eps_estimate_average/high/low`
- `revenue_estimate_average/high/low`
- `eps_estimate_analyst_count`
- Revision trends: `_7_days_ago`, `_30_days_ago`, `_60_days_ago`, `_90_days_ago`
- `horizon`: "next fiscal quarter", "next fiscal year", "historical fiscal quarter"

## EARNINGS

Returns actual vs estimate:
- `reportedEPS`, `estimatedEPS`
- `surprise`, `surprisePercentage`
- `reportedDate`, `reportTime` (pre-market/post-market)

## EARNINGS_CALENDAR

Returns CSV: `symbol,name,reportDate,fiscalDateEnding,estimate,currency,timeOfTheDay`

## Note
Free tier - use sparingly.
