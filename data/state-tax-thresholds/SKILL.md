---
name: state-tax-thresholds
description: Current state-by-state tax nexus thresholds for all 50 states including economic nexus, P.L. 86-272 rules, and franchise tax. Use when validating tax calculations, reviewing nexus detection logic, or checking threshold amounts.
---

# State Tax Thresholds Reference

**Last Updated:** January 2026

This Skill provides current economic nexus thresholds for sales tax, income tax, and franchise tax across all 50 US states. Use this as the authoritative source when implementing or validating nexus detection logic.

## Quick Reference

### Sales Tax Economic Nexus (Top States)

| State | Revenue Threshold | Transaction Threshold | Both Required? |
|-------|------------------|----------------------|----------------|
| CA    | $500,000         | -                    | No (revenue only) |
| TX    | $500,000         | -                    | No (revenue only) |
| NY    | $500,000         | 100 transactions     | **Yes (AND)** |
| FL    | -                | -                    | No economic nexus |
| IL    | $100,000         | 200 transactions     | **Yes (AND)** |
| PA    | $100,000         | -                    | No (revenue only) |
| OH    | $100,000         | 200 transactions     | No (OR) |
| GA    | $100,000         | 200 transactions     | No (OR) |
| NC    | $100,000         | 200 transactions     | No (OR) |
| MI    | $100,000         | 200 transactions     | No (OR) |

### Common Thresholds Summary

**$500,000 Revenue Threshold:**
- California, Texas, Washington, Massachusetts, Maryland, New York (+ 100 txns)

**$100,000 Revenue Threshold (Most Common):**
- 40+ states use this threshold
- Many also require 200+ transactions (varies by state)

**No Economic Nexus:**
- Florida (physical presence only)
- Montana (no sales tax)
- Oregon (no sales tax)
- New Hampshire (no sales tax)
- Delaware (no sales tax)

## Sales Tax Economic Nexus - All 50 States

### Alabama
- **Revenue:** $250,000
- **Transactions:** None required
- **Effective Date:** October 1, 2018
- **Notes:** One of the lower thresholds

### Alaska
- **No statewide sales tax**
- **Notes:** Some local jurisdictions have sales tax

### Arizona
- **Revenue:** $100,000
- **Transactions:** None required (revenue only)
- **Effective Date:** October 1, 2019

### Arkansas
- **Revenue:** $100,000
- **Transactions:** 200 transactions
- **Combined:** OR (either threshold triggers)
- **Effective Date:** July 1, 2019

### California
- **Revenue:** $500,000
- **Transactions:** None required
- **Effective Date:** April 1, 2019
- **Notes:** Higher threshold than most states

### Colorado
- **Revenue:** $100,000
- **Transactions:** None required
- **Effective Date:** December 1, 2018

### Connecticut
- **Revenue:** $100,000
- **Transactions:** 200 transactions
- **Combined:** AND (both required)
- **Effective Date:** December 1, 2018

### Delaware
- **No sales tax**

### Florida
- **No economic nexus**
- **Physical presence required**
- **Notes:** One of few states without economic nexus

### Georgia
- **Revenue:** $100,000
- **Transactions:** 200 transactions
- **Combined:** OR (either threshold)
- **Effective Date:** January 1, 2019

### Hawaii
- **Revenue:** $100,000
- **Transactions:** 200 transactions
- **Combined:** OR (either threshold)
- **Effective Date:** July 1, 2018

### Idaho
- **Revenue:** $100,000
- **Transactions:** None required
- **Effective Date:** June 1, 2019

### Illinois
- **Revenue:** $100,000
- **Transactions:** 200 transactions
- **Combined:** AND (both required)
- **Effective Date:** October 1, 2018

### Indiana
- **Revenue:** $100,000
- **Transactions:** 200 transactions
- **Combined:** OR (either threshold)
- **Effective Date:** October 1, 2018

### Iowa
- **Revenue:** $100,000
- **Transactions:** None required
- **Effective Date:** January 1, 2019

### Kansas
- **Revenue:** $100,000
- **Transactions:** None required
- **Effective Date:** October 1, 2019

### Kentucky
- **Revenue:** $100,000
- **Transactions:** 200 transactions
- **Combined:** OR (either threshold)
- **Effective Date:** October 1, 2018

### Louisiana
- **Revenue:** $100,000
- **Transactions:** 200 transactions
- **Combined:** OR (either threshold)
- **Effective Date:** July 1, 2020

### Maine
- **Revenue:** $100,000
- **Transactions:** None required
- **Effective Date:** July 1, 2018

### Maryland
- **Revenue:** $100,000
- **Transactions:** 200 transactions
- **Combined:** OR (either threshold)
- **Effective Date:** October 1, 2018
- **2019 Update:** Changed to $100,000 from prior threshold

### Massachusetts
- **Revenue:** $100,000
- **Transactions:** None required
- **Effective Date:** October 1, 2019
- **Notes:** Previously had cookie nexus rules

### Michigan
- **Revenue:** $100,000
- **Transactions:** 200 transactions
- **Combined:** OR (either threshold)
- **Effective Date:** October 1, 2018

### Minnesota
- **Revenue:** $100,000
- **Transactions:** 200 transactions (retail sales)
- **Combined:** OR (either threshold)
- **Effective Date:** October 1, 2018

### Mississippi
- **Revenue:** $250,000
- **Transactions:** None required
- **Effective Date:** September 1, 2018

### Missouri
- **Revenue:** $100,000
- **Transactions:** None required
- **Effective Date:** January 1, 2023

### Montana
- **No sales tax**

### Nebraska
- **Revenue:** $100,000
- **Transactions:** 200 transactions
- **Combined:** OR (either threshold)
- **Effective Date:** January 1, 2019

### Nevada
- **Revenue:** $100,000
- **Transactions:** 200 transactions
- **Combined:** OR (either threshold)
- **Effective Date:** October 1, 2018

### New Hampshire
- **No sales tax**

### New Jersey
- **Revenue:** $100,000
- **Transactions:** 200 transactions
- **Combined:** OR (either threshold)
- **Effective Date:** November 1, 2018

### New Mexico
- **Revenue:** $100,000
- **Transactions:** None required
- **Effective Date:** July 1, 2019

### New York
- **Revenue:** $500,000
- **Transactions:** 100 transactions
- **Combined:** AND (both required)
- **Effective Date:** June 21, 2018
- **Notes:** Higher revenue threshold but lower transaction count

### North Carolina
- **Revenue:** $100,000
- **Transactions:** 200 transactions
- **Combined:** OR (either threshold)
- **Effective Date:** November 1, 2018

### North Dakota
- **Revenue:** $100,000
- **Transactions:** None required
- **Effective Date:** October 1, 2018

### Ohio
- **Revenue:** $100,000
- **Transactions:** 200 transactions
- **Combined:** OR (either threshold)
- **Effective Date:** August 1, 2019

### Oklahoma
- **Revenue:** $100,000
- **Transactions:** None required
- **Effective Date:** November 1, 2019

### Oregon
- **No sales tax**

### Pennsylvania
- **Revenue:** $100,000
- **Transactions:** None required
- **Effective Date:** July 1, 2019

### Rhode Island
- **Revenue:** $100,000
- **Transactions:** 200 transactions
- **Combined:** OR (either threshold)
- **Effective Date:** July 1, 2019

### South Carolina
- **Revenue:** $100,000
- **Transactions:** None required
- **Effective Date:** November 1, 2018

### South Dakota
- **Revenue:** $100,000
- **Transactions:** 200 transactions
- **Combined:** OR (either threshold)
- **Effective Date:** November 1, 2018
- **Notes:** The Wayfair case originated from this state

### Tennessee
- **Revenue:** $100,000
- **Transactions:** None required
- **Effective Date:** October 1, 2019

### Texas
- **Revenue:** $500,000
- **Transactions:** None required
- **Effective Date:** October 1, 2019
- **Notes:** Higher threshold than most states

### Utah
- **Revenue:** $100,000
- **Transactions:** 200 transactions
- **Combined:** OR (either threshold)
- **Effective Date:** January 1, 2019

### Vermont
- **Revenue:** $100,000
- **Transactions:** 200 transactions
- **Combined:** OR (either threshold)
- **Effective Date:** July 1, 2018

### Virginia
- **Revenue:** $100,000
- **Transactions:** 200 transactions
- **Combined:** OR (either threshold)
- **Effective Date:** July 1, 2019

### Washington
- **Revenue:** $100,000
- **Transactions:** None required
- **Effective Date:** October 1, 2018

### West Virginia
- **Revenue:** $100,000
- **Transactions:** 200 transactions
- **Combined:** OR (either threshold)
- **Effective Date:** January 1, 2019

### Wisconsin
- **Revenue:** $100,000
- **Transactions:** None required
- **Effective Date:** October 1, 2018

### Wyoming
- **Revenue:** $100,000
- **Transactions:** 200 transactions
- **Combined:** OR (either threshold)
- **Effective Date:** February 1, 2019

## Income Tax Nexus & P.L. 86-272

### Public Law 86-272 Overview

**Protection Applies When:**
- Only activity is solicitation of orders for tangible personal property
- Orders are approved and filled outside the state
- No other business activities in the state

**Protection Does NOT Apply To:**
- Services (e.g., software as a service)
- Intangible goods
- Selling products AND providing services
- Having employees perform non-solicitation activities
- Maintaining inventory in the state

### States with Factor Presence Nexus

**California:**
- $500,000+ sales (property + payroll + sales)
- $50,000+ property
- $50,000+ payroll
- 25% of total sales

**New York:**
- No factor presence statute (physical presence required)

**Texas:**
- See Franchise Tax section

**Other States:**
- Most states rely on physical presence for income tax
- P.L. 86-272 provides protection for many out-of-state sellers

## Franchise Tax Thresholds

### Texas Franchise Tax (Margin Tax)

**Revenue Threshold:** $1,230,000 (2024)
- Below this = no franchise tax due
- Above this = subject to margin tax

**Tax Rates:**
- Retail/Wholesale: 0.375%
- Other businesses: 0.75%

**Calculation Base:**
- Total revenue minus either:
  - Cost of goods sold (COGS)
  - Compensation
  - 30% of total revenue (standard deduction)
  - $1 million deduction

### Delaware Franchise Tax

**Based on authorized shares:**
- Minimum: $175
- Maximum: $200,000

### Other States

Most states don't have separate franchise taxes. Check state-specific rules for:
- Annual report fees
- Minimum taxes
- Entity-level taxes

## Alert Severity Guidelines

Use these guidelines when generating alerts:

### RED (Critical) - Immediate Action Required
- Revenue exceeds threshold by 20%+ OR
- Both revenue AND transaction thresholds met (for AND states) OR
- Already operating in state without registration

### ORANGE (Warning) - Review Recommended
- Revenue at 80-120% of threshold OR
- One threshold met but not both (for AND states) OR
- P.L. 86-272 judgment required (services + goods)

### YELLOW (Info) - Monitor Situation
- Revenue at 60-80% of threshold OR
- Trending toward threshold (analyze historical data) OR
- Recent state law change affecting nexus

## Validation Examples

### California Sales Tax
```javascript
// Correct implementation
if (stateRevenue['CA'] >= 500000) {
  createAlert({
    state: 'CA',
    type: 'SALES_NEXUS',
    subtype: 'ECONOMIC_NEXUS',
    severity: 'RED',
    threshold: 500000,
    currentAmount: stateRevenue['CA'],
    message: 'California sales tax economic nexus triggered'
  });
}
```

### New York Sales Tax (AND logic)
```javascript
// Correct - BOTH thresholds required
if (stateRevenue['NY'] >= 500000 && transactionCount['NY'] >= 100) {
  createAlert({
    state: 'NY',
    type: 'SALES_NEXUS',
    subtype: 'ECONOMIC_NEXUS',
    severity: 'RED',
    threshold: 500000,
    currentAmount: stateRevenue['NY'],
    message: 'New York sales tax nexus - both revenue and transaction thresholds met'
  });
}
```

### Texas Franchise Tax
```javascript
// Correct threshold for 2024
if (totalRevenue >= 1230000) {
  createAlert({
    state: 'TX',
    type: 'FRANCHISE_TAX',
    severity: 'RED',
    threshold: 1230000,
    currentAmount: totalRevenue,
    message: 'Texas franchise tax threshold exceeded'
  });
}
```

## Maintenance Notes

**Update Frequency:** Review quarterly (January, April, July, October)

**Sources to Check:**
- State department of revenue websites
- Tax Foundation updates
- Bloomberg Tax
- State tax policy changes

**Recent Changes:**
- January 2024: TX franchise tax threshold increased to $1,230,000
- July 2023: MO economic nexus enacted ($100,000)

**States to Watch:**
- Florida (may enact economic nexus)
- States changing transaction count requirements

## Common Mistakes to Avoid

1. **Using OR logic for AND states**
   - NY requires BOTH $500k revenue AND 100 transactions
   - IL requires BOTH $100k revenue AND 200 transactions
   - CT requires BOTH $100k revenue AND 200 transactions

2. **Forgetting no-sales-tax states**
   - AK, DE, MT, NH, OR have no statewide sales tax
   - Don't generate alerts for these states

3. **Outdated thresholds**
   - Always check this Skill for current amounts
   - Don't hardcode thresholds from old references

4. **Applying P.L. 86-272 to services**
   - Protection only for tangible goods
   - SaaS, consulting, etc. are NOT protected

5. **Ignoring measurement period**
   - Most states measure on rolling 12-month or calendar year basis
   - Check state-specific lookback periods

## References

- **South Dakota v. Wayfair (2018):** Supreme Court case enabling economic nexus
- **P.L. 86-272 (1959):** Federal law limiting state taxation of interstate commerce
- **Streamlined Sales Tax:** Multi-state initiative for sales tax simplification

---

**When using this Skill:**
1. Always verify the current date matches "Last Updated" above
2. If more than 3 months old, check for state law changes
3. Cite specific thresholds when reviewing code
4. Generate alerts using severity guidelines above
