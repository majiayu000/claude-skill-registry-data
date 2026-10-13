---
name: deal-screener
description: "Screen PE and CRE deal opportunities. Apply scoring criteria, filter by investment thesis, rank targets by fit. Use when evaluating new deals, screening pipeline opportunities, or prioritizing investment targets."
---

# /deal-screener -- Deal Opportunity Screener

Apply scoring criteria to PE/CRE targets and output ranked recommendations.

> Before executing, read `_shared/plugin-context.md` for Nexus domain vocabulary, MCP tool references, and quality standards.

## Prerequisites

**Required**: None -- this skill works with manually provided deal data.

**Optional MCP Connections** (enhance automation):
- **Nexus MCP** (`nexus.syntari-ai.com/api/mcp`) -- `nexus_list_deals`, `nexus_get_deal`, `nexus_screen_deal` for automated deal retrieval and scoring
- **BigData.com MCP** (via `financial-analysis` plugin) -- company tearsheets, financials, sentiment for PE target research
- **PitchBook MCP** -- private market deal data, comparable transactions
- **S&P Global / Kensho MCP** -- Capital IQ financials, company profiles

**Graceful Degradation**: If MCP tools are not connected, provide deal data manually (paste deal summaries, upload spreadsheets, or describe opportunities in conversation). All analytical frameworks work identically with manual input.

## When to Use
- Evaluating a batch of new deal opportunities
- Filtering the deal pipeline by investment criteria
- Ranking targets for investment committee review
- Running weekly pipeline scoring refresh
- Comparing inbound proprietary deals against market benchmarks
- Generating pass/proceed recommendations with evidence

## Scoring Framework

### PE Deal Scoring (100 points)
| Factor | Weight | Criteria |
|--------|--------|----------|
| Revenue quality | 20 | Recurring %, growth rate, concentration |
| Market position | 15 | TAM, market share, competitive moat |
| Management team | 15 | Track record, retention, depth |
| Financial health | 20 | Margins, cash flow, debt levels |
| Growth potential | 15 | Organic + M&A opportunities |
| Valuation | 15 | Multiple vs comps, entry price |

### CRE Deal Scoring (100 points)
| Factor | Weight | Criteria |
|--------|--------|----------|
| Location quality | 20 | Submarket fundamentals, demographics |
| Asset quality | 15 | Condition, vintage, deferred maintenance |
| Income stability | 20 | Occupancy, WALT, tenant credit |
| Return profile | 20 | Cap rate, IRR, cash yield |
| Value-add potential | 15 | Rent upside, repositioning opportunity |
| Risk factors | 10 | Environmental, regulatory, market cycle |

### Signal Output
| Score | Signal | Color |
|-------|--------|-------|
| 80-100 | Strong Buy | Green (#10B981) |
| 60-79 | Buy | Blue (#068EFF) |
| 40-59 | Hold | Amber (#F59E0B) |
| 0-39 | Pass | Red (#EF4444) |

## Data Shapes

### Deal Screen Input

```typescript
interface DealScreenInput {
  dealId?: string              // Optional -- omit if providing data manually
  dealName: string
  dealType: 'pe' | 'cre'
  criteria?: {
    minRevenue?: number        // Minimum revenue threshold ($)
    maxMultiple?: number       // Maximum entry multiple (EV/EBITDA)
    sectors?: string[]         // Target sectors (e.g., ["SaaS", "Health IT"])
    geographies?: string[]     // Target geographies (e.g., ["US", "Western Europe"])
    minScore?: number          // Minimum score threshold for advancement
  }
}
```

### Deal Screen Result

```typescript
interface DealScreenResult {
  dealId?: string
  dealName: string
  dealType: 'pe' | 'cre'
  totalScore: number           // 0-100 weighted score
  signal: 'strong_buy' | 'buy' | 'hold' | 'pass'
  signalColor: string
  factorScores: {
    factor: string             // e.g., "Revenue quality"
    weight: number             // e.g., 20
    score: number              // 0-100 raw score for this factor
    weightedScore: number      // weight * score / 100
    evidence: string           // Supporting evidence for the score
  }[]
  recommendation: string
  keyHighlights: string[]
  keyRisks: string[]
}
```

## Workflow

### Step 1: Gather Deal Data
- **With Nexus MCP**: Use `nexus_list_deals` or `nexus_get_deal` to retrieve deal data automatically.
- **With BigData.com MCP**: Use `bigdata_company_tearsheet` or `bigdata_search` for company research.
- **Without MCP**: Ask the user to provide deal details (company name, sector, financials, property info).

### Step 2: Define Criteria
Confirm investment thesis parameters (sector, size, geography, return threshold).

### Step 3: Score Each Deal
Apply the scoring framework to each opportunity. Document evidence for each factor score.

### Step 4: Rank and Filter
Sort by total score. Apply minimum threshold (typically 60+ for further diligence).

### Step 5: Output
Generate ranked table with scores, signal colors, and key highlights per deal.

## Sample Output

```
=== Deal Screening Report -- Q1 2026 Pipeline ===
Fund: SVP Growth Equity Fund IV
Criteria: Software/SaaS, $50M-$500M EV, >15% revenue growth

Rank  Deal                   Sector      EV       Score  Signal       Key Factor
------------------------------------------------------------------------------
  1   Meridian Data          SaaS       $420M     87.4   STRONG BUY   92% recurring, 118% NRR
  2   Apex Cloud Platform    SaaS       $285M     82.1   STRONG BUY   40% YoY growth, net neg churn
  3   NovaCare Analytics     Health IT  $195M     74.6   BUY          FDA-cleared, 87% gross margin
  4   TerraForm Industrial   SaaS       $340M     68.3   BUY          Strong TAM, mgmt concern
  5   CloudBridge CRM        SaaS       $120M     55.2   HOLD         Revenue concentration risk
  6   DataSync Corp          Data       $250M     41.8   HOLD         Declining margins, stale product
  7   Legacy Systems Inc     IT Svcs    $180M     28.4   PASS         No recurring revenue, 5% growth

Summary: 7 deals screened -> 2 Strong Buy, 2 Buy, 2 Hold, 1 Pass
Recommendation: Advance Meridian Data and Apex Cloud to Phase II diligence
```

## Workflow Chain

This skill is step 2 in the deal analysis chain: `/deal-doc-triage` -> **`/deal-screener`** -> `/deal-memo-writer` -> deep diligence.

## Related Skills
- `/deal-memo-writer` -- Write PE acquisition and CRE investment deal memos from screening results
- `/financial-modeling` -- LBO, DCF, M&A models to support deal valuation
- `/competitive-analysis` -- Analyze competitors of screening targets
- `/om-parser` -- Parse CRE offering memorandums for deal data extraction
- `/cre-underwriter` -- Full CRE underwriting for screened CRE deals

## Confidence Calibration

Every screening output must include a calibrated confidence assessment:

```
## Confidence Assessment
- **Score**: 0.XX (0.0 = no confidence, 1.0 = full confidence)
- **Calibration**: conservative | neutral | optimistic
- **Confidence Drivers**: [what supports the score -- e.g., "complete financials provided", "multiple comp transactions available"]
- **Data Gaps**: [what's missing that would improve confidence -- e.g., "no management references", "market rent data unavailable"]
```

**Three-pass calibration**: Generate scoring from conservative, neutral, and optimistic perspectives. High consistency across passes = high confidence. Divergence = flag for human review.

Typical confidence ranges:
- **0.85+**: Complete financial data, multiple comps, management access
- **0.65-0.84**: Partial data, limited comps, preliminary assessment
- **0.40-0.64**: Teaser/headline data only, significant assumptions required
- **Below 0.40**: Insufficient data -- flag for additional information gathering before scoring
