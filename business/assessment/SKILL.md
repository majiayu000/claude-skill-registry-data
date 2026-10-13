---
name: consulting-assessment
description: "Business assessment frameworks hub -- Bain NPS, Elements of Value, Repeatable Models, Founders Mentality, BCG TSR decomposition, Experience Curve, Full Potential, Oliver Wyman CVM, Deloitte Human Capital, Operations Optimizer."
---

# Business Assessment Frameworks Hub

10 assessment frameworks from Bain, BCG, Oliver Wyman, and Deloitte for scoring business health, competitive position, and operational maturity.

> Before executing, read `../../_shared/plugin-context.md` for Nexus plugin conventions.

## Prerequisites

- **Nexus MCP** (optional): `nexus_list_portfolio`, `nexus_get_deal` for company data
- **BigData.com MCP** (optional): `bigdata_company_tearsheet` for financials and benchmarks
- **Manual fallback**: Provide company financials, survey data, or operational metrics directly

## Framework Registry

| Framework | Origin | Purpose |
|---|---|---|
| **NPS Tracker** | Bain | Track customer loyalty, benchmark NPS, correlate with revenue |
| **Elements of Value** | Bain | Score products on 30 value elements, identify gaps vs competitors |
| **Repeatable Models** | Bain | Assess business model scalability and adjacency growth potential |
| **Founders Mentality** | Bain | Score insurgent mission, frontline obsession, owner's mindset |
| **TSR Decomposition** | BCG | Decompose total shareholder return into growth, margin, multiple, leverage |
| **Experience Curve** | BCG | Plot cost decline vs cumulative volume for competitive advantage |
| **Full Potential** | Bain | Size total value creation opportunity with gap waterfall |
| **Customer Value Mgmt** | Oliver Wyman | Segment customers by profitability, identify value leakage |
| **Human Capital** | Deloitte | Evaluate management quality, org design, talent gaps, bench strength |
| **Operations** | Deloitte | Diagnose procurement, manufacturing, and supply chain inefficiencies |

## When to Use Each

- **Customer loyalty**: NPS Tracker -- score and benchmark customer sentiment
- **Product differentiation**: Elements of Value -- identify unmet value dimensions
- **Scalability check**: Repeatable Models -- can the business model scale without breaking?
- **Cultural health**: Founders Mentality -- has the company lost its insurgent edge?
- **Shareholder value**: TSR Decomposition -- where is value being created or destroyed?
- **Cost advantage**: Experience Curve -- is the company riding the cost curve?
- **Total opportunity**: Full Potential -- what is the maximum achievable value?
- **Customer economics**: Customer Value Mgmt -- which segments are profitable?
- **Talent quality**: Human Capital -- is the management team capable of executing?
- **Operational efficiency**: Operations -- where are the process bottlenecks?

## TSR Decomposition Formula

```
TSR = Revenue Growth + Margin Expansion + Multiple Expansion + Leverage Effect + Dividends

Components:
  Revenue Growth:      YoY revenue change contribution to equity value
  Margin Expansion:    EBITDA margin change x revenue
  Multiple Expansion:  EV/EBITDA multiple change x EBITDA
  Leverage Effect:     Debt paydown contribution to equity value
  Dividends:           Cash distributions to shareholders
```

## Full Potential Waterfall

```
Current EBITDA
  + Revenue enhancement (pricing, mix, new markets)
  + Cost reduction (procurement, labor, overhead)
  + Working capital release (DSO, DPO, DIO)
  + Capital efficiency (capex optimization)
  = Full Potential EBITDA
  - Implementation costs
  = Net Value Creation Opportunity
```

## Related Skills
- `/consulting-strategy` -- Strategic frameworks (7-S, Three Horizons, Porter)
- `/consulting-value-creation` -- Post-acquisition value creation execution
- `/consulting-due-diligence` -- Due diligence assessment frameworks

## Confidence Calibration

Apply three-pass calibration per `../../_shared/plugin-context.md` SteerConf protocol. Assessment frameworks often blend quantitative and qualitative inputs -- flag where scores derive from judgment vs. hard data.
