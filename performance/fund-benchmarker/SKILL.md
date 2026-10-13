---
name: fund-benchmarker
description: "Benchmark fund IRR, MOIC, DPI vs vintage year, strategy, and geography peers. PME analysis, J-curve normalization, quartile ranking."
---

# /fund-benchmarker -- Fund Performance Benchmarking

Benchmark fund performance metrics against vintage year, strategy, and geography peers using institutional methodologies (PME, J-curve normalization, quartile ranking).

> Before executing, read `_shared/plugin-context.md` for Nexus plugin conventions.

## Prerequisites

- **Nexus MCP** (optional): `nexus_list_funds`, `nexus_get_fund` for fund data
- **Chronograph MCP** (optional): PE portfolio monitoring and fund performance benchmarks
- **PitchBook MCP** (optional): Private market peer fund data
- **Manual fallback**: Provide fund metrics (IRR, MOIC, DPI, RVPI, TVPI, vintage, strategy, AUM) manually

## When to Use
- Benchmarking fund returns against peer groups
- Quartile ranking for LP reporting or fundraising materials
- J-curve normalization to compare funds at different maturity stages
- PME (Public Market Equivalent) analysis to justify PE premium
- Preparing performance data for board reports or IC presentations
- Generating talking points for IR team around underperforming metrics

## Workflow

### Step 1: Identify the Fund and Peer Universe
Determine the fund's vintage year, strategy (buyout, growth, venture, credit, real estate), geography (NA, Europe, Asia, Global), and size bucket (micro <$500M, mid $500M-$2B, large $2B-$10B, mega >$10B). Construct a peer set by matching on vintage year +/-1, same strategy, same geography.

### Step 2: Normalize for J-Curve Position
Funds in early years (1-4) show negative returns due to fees and unrealized investments. Calculate the fund's "maturity ratio" (elapsed quarters / expected fund life in quarters). Compare only against peers at equivalent maturity stages.

### Step 3: Calculate Public Market Equivalent (PME)
Run Kaplan-Schoar PME: divide sum of discounted distributions by sum of discounted contributions, using a public index (S&P 500, Russell 2000, or MSCI) as discount factor. PME > 1.0 = fund outperformed public markets.

### Step 4: Compute Quartile Rankings
For each metric (Net IRR, Gross MOIC, DPI, RVPI, TVPI), rank the fund within its peer universe. Assign quartiles: Q1 (top 25%), Q2 (25-50%), Q3 (50-75%), Q4 (bottom 25%). Flag metrics where the fund moved quartiles since last reporting period.

### Step 5: Run Dispersion Analysis
Calculate the spread between top-quartile and bottom-quartile returns within the peer set. Wide dispersion (>15% IRR spread) = manager selection matters more. Narrow dispersion = index-like returns where fees are harder to justify.

### Step 6: Generate Benchmark Report
Produce: (a) summary scorecard table, (b) PME result with index attribution, (c) quartile heatmap across all metrics, (d) J-curve position overlay chart data, (e) peer comparison scatter (IRR vs MOIC).

### Step 7: Flag Performance Alerts
Identify metrics falling below median (Q3/Q4) and generate talking points for IR team. If DPI is below peer median but RVPI is above, note that unrealized value explains the gap. If IRR is decaying QoQ, flag for IC review.

## Sample Output

```
FUND BENCHMARK REPORT -- Nexus Growth Partners III
Vintage: 2020 | Strategy: Growth Equity | Geography: NA
AUM: $450M | Maturity: Year 6 of 10 (value-creation phase)
Peer Universe: 34 funds matching criteria

Metric       Fund     Peer Med  Q1 Thr   Quartile  Trend   Prior Q
Net IRR      18.2%    14.5%     19.0%    Q2        Stable  Q2
Gross MOIC   2.1x     1.8x      2.3x     Q2        Up      Q3
DPI          0.6x     0.7x      0.9x     Q3        Up      Q4
RVPI         1.5x     1.1x      1.4x     Q1        Stable  Q1
TVPI         2.1x     1.8x      2.3x     Q2        Up      Q2

KS-PME: 1.31x (vs S&P 500) -- Outperforming public markets by 31%
J-Curve: Year 6 of 10 -- entering harvesting phase
Dispersion: 16.2% IRR spread (high -- manager selection critical)

ALERTS:
  [WARNING] DPI Q3 -- below peer median. Talking point: RVPI of 1.5x
            (Q1) indicates strong unrealized portfolio; 3 exits
            expected in next 12 months worth $180M in distributions.
  [INFO]    MOIC improved from Q3 to Q2 -- driven by Apex markup (+$42M)
```

## Data Types Reference

```typescript
interface FundBenchmarkRequest {
  fundId: string
  peerCriteria?: {
    vintageRange?: number        // +/- years, default 1
    strategies?: string[]
    geographies?: string[]
    sizeRange?: [number, number] // AUM range in $M
  }
  pmeIndex?: 'sp500' | 'russell2000' | 'msci_world' | 'msci_europe'
  includeDispersion?: boolean
}

interface FundBenchmarkResult {
  fund: {
    name: string
    vintage: number
    strategy: string
    geography: string
    aum: number
    maturityRatio: number
  }
  metrics: {
    metric: string
    fundValue: number
    peerMedian: number
    q1Threshold: number
    q3Threshold: number
    quartile: 1 | 2 | 3 | 4
    trend: 'up' | 'stable' | 'down'
  }[]
  pme: {
    index: string
    ksPme: number              // Kaplan-Schoar PME
    interpretation: string
  }
  jCurve: {
    fundPosition: number       // year in fund life
    expectedLife: number
    phase: 'j-curve' | 'value-creation' | 'harvesting'
  }
  dispersion?: {
    irrSpread: number          // Q1-Q4 IRR spread
    managerSelectionMatters: boolean
  }
  peerCount: number
  alerts: { metric: string; message: string; severity: 'info' | 'warning' | 'critical' }[]
}
```

## Fund Size Buckets

| Bucket | AUM Range | Typical Peer Set Size |
|--------|-----------|----------------------|
| Micro | <$500M | 15-40 funds |
| Mid | $500M-$2B | 30-80 funds |
| Large | $2B-$10B | 20-50 funds |
| Mega | >$10B | 10-25 funds |

## J-Curve Phases

| Phase | Years | Expected Behavior |
|-------|-------|-------------------|
| J-Curve | 1-4 | Negative/low IRR due to fees and unrealized investments |
| Value Creation | 4-7 | IRR inflection, markups on portfolio companies |
| Harvesting | 7-10+ | Exits drive DPI increase, IRR stabilizes |

## Related Skills
- `/portfolio-analyzer` -- Portfolio-level performance analysis
- `/financial-modeling` -- Fund-level IRR, MOIC, DPI computations
- `/deal-memo-writer` -- Embed benchmark data into fund reporting

## Confidence Calibration

Apply three-pass calibration (conservative/neutral/optimistic) per `_shared/plugin-context.md` SteerConf protocol. Flag data gaps where peer benchmark data is estimated or uses stale vintage year datasets.
