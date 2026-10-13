---
name: deal-memo-writer
description: "Write deal memos for PE acquisitions and CRE investments. Structure company/property overview, investment thesis, financial analysis, risks, and recommendation. Use when preparing deal memos, writing investment summaries, or documenting deal rationale."
---

# /deal-memo-writer -- Deal Memo Writer

Write structured deal memos for PE acquisitions and CRE investments.

> Before executing, read `_shared/plugin-context.md` for Nexus domain vocabulary, MCP tool references, and quality standards.

## Prerequisites

**Required**: Deal data -- either from MCP tools or provided manually (financials, company/property info, market context).

**Optional MCP Connections** (enhance automation):
- **Nexus MCP** (`nexus.syntari-ai.com/api/mcp`) -- `nexus_get_deal`, `nexus_run_model` for deal data and financial model outputs
- **BigData.com MCP** (via `financial-analysis` plugin) -- company tearsheets, financials, SEC filings for research
- **PitchBook MCP** -- comparable transactions, market sizing
- **S&P Global / Kensho MCP** -- Capital IQ financial data

**Graceful Degradation**: If MCP tools are not connected, provide deal details manually. Paste financials, upload documents, or describe the deal in conversation. The memo structure and analytical frameworks work identically with manual input.

## When to Use
- Documenting a deal for IC review
- Creating a preliminary deal summary after initial screening
- Writing up deal rationale after first-round diligence
- Generating CRE investment memos with property-specific analysis
- Preparing a condensed one-pager for deal committee
- Converting raw deal data into formatted investment narrative

## Memo Structure

### Executive Summary (1 page)
- Deal overview: target, sector, size, structure
- Key thesis points (3-4 bullets)
- Headline financial metrics
- Recommendation (proceed/pass/more diligence)

### Company/Property Overview (1-2 pages)
- Business description / property description
- History and key milestones
- Market position and competitive landscape
- Management team / tenant roster

### Investment Thesis (1-2 pages)
- Market opportunity and TAM
- Competitive advantage / moat
- Value creation plan
- Return expectations
- Key risks and mitigants

### Financial Analysis (2-3 pages)
- Historical financial performance
- Pro forma projections
- Return analysis (IRR, MOIC for PE; cap rate, cash yield for CRE)
- Sensitivity tables
- Comparable transactions

### Risk Assessment (1 page)
- Key risks with severity rating (Critical / High / Medium / Low)
- Mitigation strategies
- Downside scenario analysis

### Recommendation & Next Steps
- Clear recommendation with supporting rationale
- Conditions or open items
- Timeline for next steps

## Data Shapes

### Deal Memo

```typescript
interface DealMemo {
  dealName: string
  dealType: 'pe_acquisition' | 'cre_investment'
  status: 'draft' | 'review' | 'approved' | 'rejected'
  sections: {
    executiveSummary: string
    companyOverview: string
    investmentThesis: string
    financialAnalysis: string
    riskAssessment: string
    recommendation: string
  }
  financials: {
    enterpriseValue?: number    // PE: total enterprise value
    equity?: number             // PE: equity check size
    irr?: number                // Projected IRR (%)
    moic?: number               // Projected MOIC (x)
    capRate?: number            // CRE: going-in cap rate (%)
    noi?: number                // CRE: net operating income ($)
  }
  createdBy: string
  createdAt: string
}
```

## Workflow

### Step 1: Gather All Inputs
- **With Nexus MCP**: Use `nexus_get_deal` to pull deal data. Use `nexus_run_model` for financial model outputs.
- **With BigData.com MCP**: Use `bigdata_company_tearsheet` for target company profiles and financials.
- **Without MCP**: Collect deal data, financial analysis, market research, and diligence findings from the user.

### Step 2: Draft Each Section
Write with professional analytical tone, data-driven assertions, balanced risk perspective.

### Step 3: Financial Tables
Format all financial data with monospaced font, consistent decimals, proper currency formatting. Use `Intl.NumberFormat` conventions ($X.XM, X.Xx for multiples, X.X% for percentages).

### Step 4: Review
Cross-check all figures, ensure internal consistency, verify market data citations.

## Sample Output

```
=======================================================
CONFIDENTIAL -- INVESTMENT MEMORANDUM
=======================================================
Target:     Meridian Data Solutions, Inc.
Sector:     Enterprise Software (Data Infrastructure)
Structure:  Control Buyout (85% equity)
EV:         $420M (8.2x LTM EBITDA)
Sponsor:    SVP Growth Equity Fund IV

EXECUTIVE SUMMARY
-----------------
Meridian Data Solutions is a mission-critical data infrastructure
platform serving 340+ enterprise clients across financial services
and healthcare. We recommend proceeding to final diligence based on:

  1. 92% recurring revenue with 118% NRR -- best-in-class retention
  2. $2.1B TAM growing 14% CAGR -- significant whitespace
  3. EBITDA margin expansion opportunity: 38% -> 48% via sales efficiency
  4. Platform stickiness: <2% annual logo churn, 18-month implementation

RETURN ANALYSIS
-----------------
                  Base        Upside      Downside
  Entry EV/EBITDA  8.2x        8.2x        8.2x
  Exit EV/EBITDA   10.0x       11.5x       8.0x
  Revenue CAGR     12%         16%         8%
  EBITDA Margin     48%         52%         42%
  Gross IRR        28.4%       35.1%       14.2%
  Net IRR          23.1%       29.6%       10.8%
  MOIC             2.8x        3.5x        1.8x

RECOMMENDATION: PROCEED to Phase II diligence
  > Outstanding items: management reference calls, IT security audit
  > Timeline: 4 weeks to final IC presentation
=======================================================
```

## Workflow Chain

This skill is step 3 in the PE deal chain: `/deal-screener` -> **`/deal-memo-writer`** -> `/financial-modeling`. Also participates in document analysis and autonomous diligence chains.

## Related Skills
- `/deal-screener` -- Screen and score deals before memo writing
- `/financial-modeling` -- LBO, DCF, M&A models to support deal memo financial analysis
- `/om-parser` -- Parse CRE offering memorandums for property deal data
- `/cre-underwriter` -- Full CRE underwriting model for CRE investment memos
- `/competitive-analysis` -- Competitor analysis for the market position section

## Confidence Calibration

Every deal memo must include a calibrated confidence assessment:

```
## Confidence Assessment
- **Score**: 0.XX (0.0 = no confidence, 1.0 = full confidence)
- **Calibration**: conservative | neutral | optimistic
- **Confidence Drivers**: [what supports the score -- e.g., "audited financials available", "management meetings completed", "multiple data sources cross-referenced"]
- **Data Gaps**: [what's missing that would improve confidence -- e.g., "no customer reference calls", "industry comps limited to 3 transactions"]
```

**Three-pass calibration**: Generate analysis from conservative, neutral, and optimistic perspectives. High consistency across passes = high confidence. Divergence = flag for human review.

Typical confidence ranges:
- **0.85+**: Full diligence materials, audited financials, management access, market data confirmed
- **0.65-0.84**: Preliminary diligence, unaudited financials, limited management interaction
- **0.40-0.64**: Screening-stage data only, significant assumptions required
- **Below 0.40**: Insufficient data for a credible memo -- request additional information before drafting
