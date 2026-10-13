---
name: competitive-analysis
description: "Analyze competitors of portfolio companies or acquisition targets using Porter's 5 Forces, competitive matrix, SWOT, and financial benchmarking."
---

# /competitive-analysis -- Competitive Analysis

Analyze the competitive landscape for portfolio companies or acquisition targets using structured frameworks, multi-source data, and financial benchmarking.

> Before executing, read `_shared/plugin-context.md` for Nexus plugin conventions.

## Prerequisites

- **Nexus MCP** (optional): `nexus_get_deal`, `nexus_search_market` for deal and market data
- **BigData.com MCP** (optional): `find_companies`, `bigdata_company_tearsheet` for competitor profiles
- **Manual fallback**: Provide competitor names, financials, and market data manually

## When to Use
- Evaluating competitive position of a PE target before investment committee
- Benchmarking a portfolio company against public and private peers
- Supporting the investment thesis section of a deal memo with competitive evidence
- Identifying competitive threats or moat erosion in portfolio company monitoring
- Preparing competitive intelligence for LP reporting on portfolio company progress
- Running a Porter's 5 Forces assessment as part of commercial due diligence

## Framework: Porter's 5 Forces

| Force | Assessment Dimensions | Risk Level |
|-------|----------------------|-----------|
| **Rivalry Among Competitors** | Market concentration, growth rate, switching costs, differentiation | High if HHI < 1800 |
| **Threat of New Entrants** | Capital requirements, regulatory barriers, network effects | High if barriers low |
| **Threat of Substitutes** | Alternative products, price-performance ratio, buyer switching | Moderate if substitutes exist |
| **Buyer Power** | Customer concentration, price sensitivity, backward integration | High if top 3 > 30% revenue |
| **Supplier Power** | Supplier concentration, input differentiation, switching costs | High if sole-source |

## Workflow

### Step 1: Define the Competitive Universe
Identify the company's primary market segment and all direct, indirect, and adjacent competitors. Use BigData.com MCP (`find_companies`) with SIC/NAICS codes to build the initial competitor list. Without MCP, provide competitor names and basic profiles manually.

### Step 2: Pull Financial Benchmarks
For each competitor, extract key financial metrics using BigData.com MCP (`bigdata_company_tearsheet`). Build a comparison matrix: revenue, revenue growth, gross margin, EBITDA margin, headcount, funding/leverage.

### Step 3: Run Porter's 5 Forces Assessment
Score each force on a 1-5 scale (1 = favorable, 5 = unfavorable for the target). Document supporting evidence for each score. Aggregate into a competitive intensity score.

### Step 4: Build Competitive Feature Matrix
Create a capability comparison table. Score each cell: 3 = Leading, 2 = Parity, 1 = Lagging, 0 = Absent. Highlight defensible differentiation vs. vulnerabilities.

### Step 5: Financial Benchmarking
Compare the target's financials against the competitor set. Calculate percentile rankings on key metrics. Flag significant under/outperformance.

### Step 6: SWOT Synthesis
Synthesize findings into a structured SWOT. Every item must reference a named competitor or quantified metric -- no generic observations.

### Step 7: Produce Report
Generate the structured deliverable for consumption by `/deal-memo-writer` or `/investment-thesis-writer`.

## Sample Output

```
COMPETITIVE ANALYSIS -- AcmeTech Industrial SaaS
COMPETITIVE INTENSITY: MODERATE (Porter composite: 2.8/5.0)

PORTER'S 5 FORCES:
  Rivalry:          3.5/5  [HIGH]   -- 4 well-funded competitors
  New Entrants:     2.0/5  [MOD]    -- ERP lock-in raises switching costs
  Substitutes:      1.5/5  [LOW]    -- No credible substitute for MES
  Buyer Power:      3.0/5  [MOD]    -- Top 3 = 28% ARR; multi-year contracts
  Supplier Power:   2.0/5  [LOW]    -- Cloud infra easily substitutable

FINANCIAL BENCHMARKING (FY2025):
  Company         Rev($M)  Growth  GrossMargin  EBITDA%  NRR
  AcmeTech          26.3   22.1%    78.2%        12.4%   115%
  Robovate          41.0   38.0%    72.0%        -18%    118%
  Factori           18.5   15.0%    81.0%         8.0%   108%
  AcmeTech rank    2nd/4   3rd/4    2nd/4         1st/4  2nd/4

SWOT SUMMARY:
  S: 78% gross margin (best-in-class), 95% retention, deep ERP integrations
  W: 22% growth below Robovate (38%), smallest headcount in set
  O: Regulatory mandate pipeline driving demand; white space in mid-market
  T: Robovate's $85M war chest could accelerate enterprise capture
```

## Data Types Reference

```typescript
interface CompetitorProfile {
  name: string
  ticker?: string
  revenue: number
  revenueGrowth: number
  grossMargin: number
  ebitdaMargin: number
  headcount: number
  fundingStage: string
  lastValuation?: number
}

interface CompetitiveMatrix {
  target: CompetitorProfile
  competitors: CompetitorProfile[]
  porterScores: {
    rivalry: number          // 1-5 scale
    entrantThreat: number
    substituteThreat: number
    buyerPower: number
    supplierPower: number
    overallIntensity: number // weighted average
  }
  featureMatrix: Record<string, Record<string, number>>  // feature -> company -> score
}
```

## Porter's 5 Forces Scoring Guide

| Score | Label | Meaning |
|-------|-------|---------|
| 1.0 | Very Favorable | Minimal competitive pressure |
| 2.0 | Favorable | Low competitive pressure |
| 3.0 | Moderate | Balanced competitive dynamics |
| 4.0 | Unfavorable | Significant competitive pressure |
| 5.0 | Very Unfavorable | Intense competitive pressure |

## Feature Matrix Scoring

| Score | Label | Description |
|-------|-------|-------------|
| 3 | Leading | Best-in-class capability, clear differentiation |
| 2 | Parity | Competitive capability, no advantage |
| 1 | Lagging | Below competitors, vulnerability |
| 0 | Absent | Capability does not exist |

## Related Skills
- `/deal-memo-writer` -- Consumes competitive analysis for investment memorandum
- `/deal-screener` -- Screen deals with competitive positioning as a factor
- `/portfolio-analyzer` -- Portfolio monitoring with competitive context

## Confidence Calibration

Apply three-pass calibration (conservative/neutral/optimistic) per `_shared/plugin-context.md` SteerConf protocol. Flag data gaps where competitor financials are estimated or unavailable.
