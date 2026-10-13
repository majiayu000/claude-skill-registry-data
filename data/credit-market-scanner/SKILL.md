---
name: credit-market-scanner
description: "Scan high-yield bond market and distressed debt universe. Analyze credit spreads, track new issuance, identify stressed/distressed opportunities using OAS, YTW, and Altman Z-Score screening."
---

# /credit-market-scanner -- Credit Market Scanner

Scan HY bond markets and distressed debt for investment opportunities using credit spread analytics, BigData.com MCP, and spread monitoring.

> Before executing, read `_shared/plugin-context.md` for Nexus plugin conventions.

## Prerequisites

- **Nexus MCP** (optional): `nexus_search_market` for credit spread data
- **BigData.com MCP** (optional): `bigdata_search` for issuer news, `bigdata_events_calendar` for catalysts
- **Manual fallback**: Paste credit instrument data, spread sheets, or bond screener exports

## When to Use
- Running daily/weekly HY credit spread monitoring sweeps
- Identifying distressed debt names for credit special situations fund
- Tracking spread widening signals for existing portfolio companies
- Screening new issuance calendar for relative value opportunities
- Monitoring covenant violations and credit event triggers
- Building a watchlist of stressed credits approaching distress thresholds

## Credit Market Metrics Reference

| Metric | Description | Distressed Threshold |
|--------|-------------|---------------------|
| OAS | Option-adjusted spread to benchmark (bps) | >1,000 bps |
| YTW | Yield to worst (worst-case redemption scenario) | >15% |
| Z-Score (Altman) | Composite default probability score | <1.81 (distressed zone) |
| DSCR | Debt service coverage ratio | <1.2x (stressed) |
| Leverage | Net debt / EBITDA | >7.0x (elevated) |
| Interest Coverage | EBITDA / interest expense | <2.0x (at risk) |
| Price | Bond price (cents on dollar) | <70 cents |
| Recovery Rate | Expected recovery in default | <40% |

## Spread Classification Bands

| Band | OAS Range | Classification |
|------|-----------|---------------|
| Investment Grade | 0-150 bps | IG |
| BB (Split IG) | 150-300 bps | HY / Upper |
| B (Core HY) | 300-600 bps | HY / Core |
| Stressed | 600-1,000 bps | Stressed HY |
| Distressed | >1,000 bps | Distressed |
| Defaulted | Trading flat (accrued) | Default |

## Workflow

### Step 1: Define Scan Criteria
Specify: sector, rating range (BB to CCC), OAS threshold (e.g., >500 bps), maturity range, issuer size (min $200M face value). Narrow or broaden based on mandate.

### Step 2: Pull Universe Data
Use Nexus MCP `nexus_search_market` to pull credit spread data, or BigData.com `bigdata_search` for issuer research and `bigdata_events_calendar` for upcoming catalyst events (earnings, maturities, covenant tests). If MCP unavailable, provide data manually.

### Step 3: Screen for Opportunities
Filter the universe by scan criteria. Sort by OAS (widest first). Flag any name crossing from "stressed" to "distressed" since the last scan.

### Step 4: Compute Default Risk Signals
For each screened name, calculate Altman Z-Score components: working capital/assets, retained earnings/assets, EBIT/assets, market cap/liabilities, revenue/assets. Score < 1.81 triggers distress flag.

### Step 5: New Issuance Monitoring
Scan the new issuance calendar for upcoming HY deals. Compare new-issue pricing vs. existing comps to identify day-1 concessions or pricing dislocations.

### Step 6: Track Spread Movements
Compare current OAS to 30/90/365-day trailing averages. Flag names with >100 bps widening in the past 30 days as "spread expansion alerts."

### Step 7: Rank and Output
Produce a ranked opportunity list sorted by risk-adjusted attractiveness: wide spread + improving fundamentals + near-term catalyst = highest priority. Include brief thesis for each name.

## Sample Output

```
CREDIT MARKET SCAN -- HY Universe
Date: 2026-03-02 | Criteria: OAS >500 bps, BB/B/CCC, All Sectors

DISTRESSED (OAS >1,000 bps) -- 3 names
1. Riverside Retail 8.25% 2028   OAS: 1,842 bps  YTW: 24.1%  Price: $52  Z-Score: 1.12
   - NEW DISTRESSED: spread widened +680 bps in 30 days
   - Covenant test breach expected Q2 2026 (leverage 8.5x vs. 8.0x limit)
   Thesis: Potential distressed-for-control; EBITDA recovering post-restructuring

2. Summit Energy 9.0% 2027        OAS: 1,241 bps  YTW: 18.7%  Price: $71  Z-Score: 1.54
   - Spread widened +210 bps since last scan
   - Upcoming $180M maturity Aug 2026 -- refi risk elevated

STRESSED (OAS 600-1,000 bps) -- 7 names
3. Acme Logistics 7.5% 2029       OAS: 847 bps   YTW: 13.2%  Price: $79  Z-Score: 2.05
   - Leverage 6.8x (elevated); mgmt guidance implies improvement to 5.5x by YE

NEW ISSUANCE MONITORING
- Summit Healthcare $500M B+ 7-year: Pricing +275 bps SOFR (3 pts concession vs. comps)

SPREAD MOVEMENT ALERTS (>100 bps widening, 30 days)
- Riverside Retail: +680 bps (NEW DISTRESSED)
- Metro Networks: +145 bps (watch list)
```

## Data Types Reference

```typescript
interface CreditInstrument {
  issuer: string
  cusip: string
  coupon: number
  maturityDate: string
  rating: 'BB+' | 'BB' | 'BB-' | 'B+' | 'B' | 'B-' | 'CCC+' | 'CCC' | 'CCC-' | 'D'
  oasBps: number          // Option-adjusted spread in basis points
  ytw: number             // Yield to worst (%)
  pricePerDollar: number  // e.g. 82.5 = 82.5 cents on the dollar
  altmanZScore: number
  netDebtEbitda: number
  interestCoverage: number
}

interface ScanCriteria {
  minOasBps: number
  maxRating: string
  sectors?: string[]
  minFaceValueM?: number
}

interface ScanResult {
  instrument: CreditInstrument
  classification: 'stressed' | 'distressed' | 'defaulted'
  spreadChange30d: number   // bps change over 30 days
  isNewDistressed: boolean  // crossed threshold since last scan
  thesisBullets: string[]
}
```

## Altman Z-Score Components

| Component | Formula | Weight |
|-----------|---------|--------|
| X1 | Working Capital / Total Assets | 1.2 |
| X2 | Retained Earnings / Total Assets | 1.4 |
| X3 | EBIT / Total Assets | 3.3 |
| X4 | Market Cap / Total Liabilities | 0.6 |
| X5 | Revenue / Total Assets | 1.0 |

**Zones**: >2.99 = Safe, 1.81-2.99 = Grey, <1.81 = Distressed

## Chain: credit-analysis
**Position**: Step 1 of 3
**Next**: `/credit-stats-analyst` -- passes screened universe for 5-year/8-quarter financial analysis
**Then**: `/covenant-extractor` -- extracts loan covenants for highest-conviction names

## Related Skills
- `/credit-stats-analyst` -- Credit statistics analysis: 5-year/8-quarter financials, EBITDA analysis
- `/credit-restructuring-advisor` -- Distressed debt workout scenarios and recovery estimates
- `/covenant-extractor` -- Extract loan covenants from credit agreements

## Confidence Calibration

Apply three-pass calibration (conservative/neutral/optimistic) per `_shared/plugin-context.md` SteerConf protocol. Flag data gaps where live market pricing is unavailable.
