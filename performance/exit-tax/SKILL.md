---
name: consulting-exit-tax
description: "Exit planning and tax structuring frameworks -- Bain exit readiness, BCG/Bain PE benchmarks, PwC tax structuring, PwC ESG in PE."
---

# Exit Planning & Tax Structuring Hub

4 frameworks for PE exit preparation, benchmarking, tax optimization, and ESG compliance.

> Before executing, read `../../_shared/plugin-context.md` for Nexus plugin conventions.

## Prerequisites

- **Nexus MCP** (optional): `nexus_list_funds`, `nexus_get_fund`, `nexus_list_portfolio` for fund and portfolio data
- **PitchBook MCP** (optional): PE benchmark data for vintage year comparisons
- **Manual fallback**: Provide fund performance data, entity structures, and tax assumptions directly

## Framework Registry

| Framework | Origin | Purpose |
|---|---|---|
| **Exit Readiness** | Bain | Structured 12-18 month exit preparation with equity story and buyer targeting |
| **PE Benchmarks** | BCG + Bain | Benchmark fund performance against annual PE reports for quartile positioning |
| **Tax Structuring** | PwC | Model entity structures, debt push-down, credits, and exit tax scenarios |
| **ESG in PE** | PwC | Score ESG risks, map to financial impact, generate LP-ready reports |

## Common Exit Workflow

```
PE Benchmarks (where do we stand?)
  --> Exit Readiness (12-18 month plan)
  --> Tax Structuring (optimize exit)
  --> ESG in PE (LP-ready compliance)
```

## Exit Readiness -- 12-18 Month Timeline

| Phase | Months Out | Key Actions |
|-------|-----------|-------------|
| **Foundation** | 18-12 | Financial audit, management incentive alignment, operational improvements |
| **Preparation** | 12-6 | Equity story development, buyer universe mapping, data room build |
| **Execution** | 6-0 | Process launch, management presentations, final negotiation |

## Exit Readiness Checklist

- [ ] Audited financials (3 years + current interim)
- [ ] Quality of earnings report
- [ ] Management presentation deck
- [ ] Equity story with clear value creation narrative
- [ ] Buyer universe (strategic + financial, tiered)
- [ ] Data room organized and populated
- [ ] Management team retention / incentive plan
- [ ] Known issues pre-remediated (legal, environmental, compliance)
- [ ] Tax structure optimized for exit scenario

## Tax Structuring -- Key Levers

| Lever | Description | Impact |
|-------|-------------|--------|
| Entity Structure | C-corp vs pass-through, holdco jurisdiction | Tax rate on exit proceeds |
| Debt Push-Down | Interest deduction at target level | Reduces taxable income during hold |
| Section 338(h)(10) | Asset vs stock deal election | Buyer step-up vs seller tax treatment |
| Qualified Small Business | QSBS exclusion (Section 1202) | Up to $10M or 10x basis exclusion |
| Installment Sale | Defer gain recognition | Spread tax liability over time |
| Opportunity Zone | OZ investment deferral/exclusion | Capital gains deferral + exclusion |

## ESG Scoring Dimensions

| Dimension | Key Metrics | SFDR Alignment |
|-----------|-------------|---------------|
| Environmental | Carbon emissions, energy usage, waste | SFDR Article 8/9 indicators |
| Social | Workforce diversity, health & safety, community | Principal Adverse Impacts |
| Governance | Board composition, anti-corruption, data privacy | EU Taxonomy alignment |

## Related Skills
- `/fund-benchmarker` -- Detailed fund performance benchmarking
- `/consulting-value-creation` -- Value creation that drives exit multiples
- `/financial-modeling` -- Exit scenario modeling (LBO returns at various exit multiples)

## Confidence Calibration

Apply three-pass calibration per `../../_shared/plugin-context.md` SteerConf protocol. Tax structuring outputs should flag jurisdiction-specific assumptions and note that tax advice requires professional review.
