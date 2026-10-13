---
name: portfolio-analyzer
description: "Analyze PE and CRE portfolio performance. Aggregate metrics across portfolio companies, compute KPIs vs benchmarks, identify trends and outliers."
---

# /portfolio-analyzer -- Portfolio Performance Analyzer

Aggregate and analyze portfolio metrics across PE and CRE holdings, comparing KPIs against benchmarks.

> Before executing, read `_shared/plugin-context.md` for Nexus plugin conventions.

## Prerequisites

- **Nexus MCP** (optional): `nexus_list_portfolio`, `nexus_list_funds` for portfolio data
- **BigData.com MCP** (optional): Company financials for public comps
- **Manual fallback**: Paste portfolio company data, fund metrics, or export spreadsheets

## When to Use
- Quarterly portfolio review preparation
- Identifying underperforming or outperforming holdings
- Benchmarking portfolio against indices or peer groups
- Generating portfolio-level KPI dashboards
- Preparing board-level portfolio summaries
- Triaging companies by AI health score for asset management prioritization

## Key Metrics

### PE Portfolio

| Metric | Computation | Display |
|--------|-------------|---------|
| Total NAV | Sum of company valuations | Currency |
| Weighted IRR | Time-weighted across investments | Percentage |
| MOIC | Total value / total invested | Multiple (1.0x) |
| DPI | Distributions / paid-in | Multiple |
| RVPI | Residual value / paid-in | Multiple |
| Health Score | AI-computed health (0-100) | Score with color coding |

### CRE Portfolio

| Metric | Computation | Display |
|--------|-------------|---------|
| Total AUM | Sum of property values | Currency |
| Weighted Cap Rate | NOI-weighted across assets | Percentage |
| Avg Occupancy | SF-weighted occupancy | Percentage |
| NOI Growth | YoY aggregate NOI change | Percentage with trend |
| DSCR Coverage | Portfolio-level DSCR | Ratio |

## Workflow

### Step 1: Gather Data
Use Nexus MCP `nexus_list_portfolio` and `nexus_list_funds` for automated retrieval. Without MCP, provide portfolio company data manually (name, sector, invested capital, current value, IRR, MOIC, health score).

### Step 2: Compute Aggregates
Calculate portfolio-level metrics by aggregating across all holdings. Apply appropriate weighting (NAV-weighted for PE, SF-weighted for CRE occupancy, NOI-weighted for cap rates).

### Step 3: Benchmark Comparison
Compare against:
- Prior period (QoQ, YoY)
- Fund target returns
- Market indices (if available)
- Peer fund benchmarks

### Step 4: Identify Outliers
Flag holdings that are:
- Top/bottom quartile performers
- Trending significantly up or down
- Below investment thesis assumptions
- Requiring attention (low health score)

### Step 5: Output Summary
Generate a portfolio summary with metrics table, trend analysis, and action items.

## Sample Output

```
SVP Growth Equity Fund IV -- Portfolio Summary
As of: Q4 2025  |  12 Active Companies  |  3 Realized Exits

PORTFOLIO METRICS
                    Current     Prior QTR    YoY Change
  Total NAV        $1.42B      $1.35B       +18.3%
  Weighted IRR      24.3%       22.8%       +150bps
  MOIC              1.85x       1.78x       +0.20x
  DPI               0.42x       0.38x       +0.10x
  Avg Health Score   74.2        71.8        +2.4pts

TOP PERFORMERS (by IRR)
  Company              Sector          IRR     MOIC    Health
  Meridian Data        SaaS           42.1%    3.2x      92
  Apex Logistics       Supply Chain   31.5%    2.4x      87
  NovaCare Health      Healthcare     28.3%    2.1x      81

WATCH LIST (Health Score < 50)
  Company              Sector          IRR     MOIC    Health   Issue
  TerraForm Mfg        Industrial     -4.2%    0.8x      34    Revenue decline
  CloudBridge          SaaS            6.1%    1.1x      42    Customer churn

ACTION ITEMS
  1. TerraForm Mfg: Schedule asset management deep-dive (health 34)
  2. CloudBridge: Review customer retention strategy (churn +3.2pp)
  3. Apex Logistics: Evaluate follow-on investment opportunity
```

## Data Types Reference

```typescript
interface PortfolioSummary {
  totalNav: number
  totalInvested: number
  weightedIrr: number
  moic: number
  dpi: number
  rvpi: number
  tvpi: number
  companiesCount: number
  avgHealthScore: number
  topPerformers: PortfolioCompany[]
  watchList: PortfolioCompany[]
}

interface PortfolioCompany {
  id: string
  name: string
  sector: string
  investedCapital: number
  currentValue: number
  irr: number
  moic: number
  aiHealthScore: number
  revenueGrowth: number
  ebitdaMargin: number
  status: 'on_track' | 'watch' | 'underperforming' | 'outperforming'
}
```

## Health Score Thresholds

| Range | Classification | Color | Action |
|-------|---------------|-------|--------|
| 80-100 | Strong | Green | Monitor, evaluate follow-on |
| 60-79 | Healthy | Blue | Standard quarterly review |
| 40-59 | Watch | Yellow | Increased monitoring frequency |
| 0-39 | At Risk | Red | Asset management deep-dive required |

## Related Skills
- `/fund-benchmarker` -- Benchmark fund IRR, MOIC, DPI vs vintage year peers
- `/competitive-analysis` -- Competitive landscape for portfolio companies
- `/financial-modeling` -- LBO, DCF, M&A models for individual holdings

## Confidence Calibration

Apply three-pass calibration (conservative/neutral/optimistic) per `_shared/plugin-context.md` SteerConf protocol. Flag data gaps where portfolio company financials are stale or estimated.
