---
name: data-freshness-audit
description: Use this skill to check whether market prices, filings, financial statements, material news, and source dates are current enough for investment analysis. Trigger for current valuation, margin of safety, buy/hold/sell views, latest data, today/now requests, stale-data concerns, or auditing an existing stock note.
---

# Data Freshness Audit Skill

## Purpose

Ensure investment analysis reflects the current situation of the company.

## Trigger Examples

- "Audit my AAPL valuation note for stale data."
- "Is this analysis using the latest filing and price?"
- "Can I rely on these numbers for a current buy/sell view?"
- "Check data freshness before calculating margin of safety."

## Trigger Conditions

Activate whenever:

- A current valuation is requested
- A margin of safety is calculated
- A buy / hold / avoid rating is generated
- Financial statements are used
- User asks about “current situation”, “now”, “latest”, or “today”

## Required Inputs

- Analysis as-of date
- Source date for current price / market cap
- Latest filing period and filing date
- Periods for revenue, EBIT / operating income, FCF, cash, debt, and shares
- Date of material news or management guidance when used

If dates are missing, classify the affected fields as `Missing` rather than assuming freshness.

## Workflow

1. Identify analysis as-of date.
2. Identify source date for each critical data point.
3. Classify freshness:
   - Current
   - Recent but needs review
   - Stale
   - Historical only
   - Missing
4. Block current valuation if key data is stale.
5. Allow old data only for historical trend or normalized cycle analysis.
6. Output Data Freshness Table.
7. Add warning if current data is insufficient.

## Blocking Data for Current Valuation

Current valuation must not be finalized if any of these are stale or missing:

- Current price
- Shares outstanding
- Revenue
- EBIT / operating income
- Free cash flow
- Cash
- Debt
- Latest filing period

## Same-Day Price Rule

For current valuation or buy/add/hold/trim/sell guidance, the current price must have a market timestamp on the same calendar date as the analysis timestamp. The exact timestamp should be used when available.

- If `regular_market_time` is same-day: use the price and disclose the timestamp.
- If only delayed same-day data is available: use it, but label the exact timestamp and source.
- If `regular_market_time` is missing or not same-day: mark current price as missing/stale and block current margin of safety, reverse DCF, and price-zone conclusions until a same-day quote is available.
- During non-trading hours, use the latest regular-market timestamp only if it is still on the analysis date; otherwise label it as prior-session data and block current-price-dependent conclusions.
- Do not use generic WebSearch snippets, search-result cards, or webpage snapshots as current-price sources unless they include an explicit same-day market timestamp. If the page shows a price but no market timestamp, classify current price as `Missing` / `Blocked`.
- If `yfinance` is unavailable in the runtime, try installing it into a local sandbox package target before falling back to Yahoo public endpoints. Do not use WebSearch price snippets as the fallback.

## Script Mapping

- Freshness implementation: `scripts/data/check_data_freshness.py`
- Public data packet source dates: `scripts/connectors/public_data_packet_builder.py`
- Data freshness policy: `references/data_source_policy/data_freshness_policy.md`

## Minimal Output Contract

Return a freshness status for each critical data category and explicitly say whether current valuation / action guidance is usable, downgraded, or blocked.

## Required Output

```text
Analysis as-of date:
Market data as-of:
Financial statement period:
Latest filing used:
Data freshness status:
```

## Rule

If data is stale, say explicitly:

```text
This is a historical analysis, not a current investment analysis.
```
