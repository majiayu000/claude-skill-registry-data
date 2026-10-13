---
name: consulting-due-diligence
description: "Due diligence consulting frameworks hub -- EY-Parthenon commercial DD, EY integrated DD, EY operational DD, McKinsey deal thesis structuring, Granularity of Growth, dataroom swarm analysis."
---

# Due Diligence Consulting Frameworks Hub

6 DD frameworks for commercial, operational, and integrated due diligence on acquisition targets.

> Before executing, read `../../_shared/plugin-context.md` for Nexus plugin conventions.

## Prerequisites

- **Nexus MCP** (optional): `nexus_get_deal`, `nexus_screen_deal` for deal data and scoring
- **BigData.com MCP** (optional): `bigdata_company_tearsheet`, `bigdata_search` for market/company data
- **Box MCP** (optional): `ai_qa_multi_file`, `get_file_content` for data room document access
- **Manual fallback**: Upload or paste CIM, financials, market data, and operational documents

## Framework Registry

| Framework | Origin | Purpose |
|---|---|---|
| **Commercial DD** | EY-Parthenon | Full commercial assessment: market sizing (TAM/SAM/SOM), competitive landscape, customer concentration, management quality |
| **Integrated DD** | EY | Connect commercial, financial, operational, tech, legal, and ESG DD streams into unified findings |
| **Operational DD** | EY | Assess operational execution across 7 areas: supply chain, operations, IT, procurement, HR, finance, compliance |
| **Deal Thesis Structurer** | McKinsey | Structure investment thesis as MECE issue tree with testable hypotheses |
| **Granularity of Growth** | McKinsey | Decompose historical/projected revenue into organic market growth, M&A contribution, and share gains |
| **Dataroom Analyzer** | Swarm | Multi-document analysis across hundreds of documents with page-level citations and scoring |

## Common DD Workflow

```
Deal Thesis Structurer (hypothesis tree)
  --> Commercial DD (market/customer)
  --> Operational DD (execution)
  --> Granularity of Growth (revenue quality)
  --> Integrated DD (synthesis)
  --> Dataroom Analyzer (evidence)
```

## Commercial DD -- Key Areas

| Area | Key Questions | Data Sources |
|------|--------------|-------------|
| Market Size | TAM/SAM/SOM, growth rate, secular trends | Industry reports, BigData.com |
| Competitive Dynamics | Share, positioning, barriers to entry | Competitor profiles, customer interviews |
| Customer Analysis | Concentration, retention, cohort economics | Company CRM data, financial statements |
| Management Quality | Track record, bench strength, incentive alignment | Interview notes, LinkedIn profiles |

## Deal Thesis Structurer -- MECE Template

```
Investment Thesis: [Company] is attractive because...
  1. Market Attractiveness
     1.1 TAM is large and growing (testable: market >$XB, CAGR >Y%)
     1.2 Secular tailwinds support demand (testable: identify 2+ trends)
  2. Competitive Position
     2.1 Defensible moat exists (testable: switching costs, IP, network effects)
     2.2 Market share is stable or growing (testable: 3-year share trend)
  3. Financial Quality
     3.1 Revenue is recurring/predictable (testable: NRR >100%, churn <X%)
     3.2 Margins are expandable (testable: path from current to target margin)
  4. Value Creation Path
     4.1 Operational improvements identified (testable: specific initiatives)
     4.2 Achievable within hold period (testable: 100-day plan feasibility)
```

## Granularity of Growth Decomposition

```
Total Revenue Growth = Market Growth + M&A Growth + Share Gain/Loss

Quality Ranking:
  1. Organic share gains (highest quality -- sustainable)
  2. Market growth (moderate -- rising tide)
  3. M&A contribution (lowest quality -- requires integration execution)
```

## Related Skills
- `/deal-screener` -- Initial deal screening before DD engagement
- `/deal-memo-writer` -- Write investment memo from DD findings
- `/consulting-assessment` -- Assessment frameworks feeding into DD workstreams

## Confidence Calibration

Apply three-pass calibration per `../../_shared/plugin-context.md` SteerConf protocol. DD findings should explicitly separate confirmed facts from assumptions requiring further verification.
