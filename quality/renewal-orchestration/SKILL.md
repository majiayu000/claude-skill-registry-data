---
name: renewal-orchestration
description: 'Renewal orchestration playbook - risk identification, renewal motion design, multi-thread engagement, commercial negotiation, and expansion-at-renewal plays. Use when: renewal playbook, renewal forecast, renewal risk, multi-year renewal, NRR, GRR, churn save, contract negotiation, expansion at renewal, renewal handoff.'
---

# Renewal Orchestration (RENEW Framework)

Design a renewal motion that produces forecastable Gross Revenue Retention, defends price, and uses the renewal moment as an *expansion* event - not a re-validation event. RENEW replaces "let's get the redline back" with a coordinated, signal-driven motion that starts 120+ days before contract end.

## Core Principle

**A renewal is *won or lost 90 days before the contract end date*, not in the redline cycle.** RENEW front-loads risk identification and value evidence so the commercial conversation is short, defensible, and frequently expansion-oriented.

## The RENEW Framework

| Letter | Stage | The Question |
|--------|-------|--------------|
| **R** | Risk Scoring | What is the renewal risk score 180 / 120 / 60 days out, and what signals drive it? |
| **E** | Engagement Re-establishment | Who is the buying group at renewal, and are they re-engaged? |
| **N** | Negotiation Posture | What is the price / terms posture, and what are the walk-away conditions? |
| **E** | Expansion Inclusion | What expansion play, if any, is bundled into the renewal conversation? |
| **W** | Win the Close | What artifact pack, decision criteria, and approval path are pre-aligned? |

## Renewal Risk Scoring

Risk is a composite - not a single number. Score these at T-180:

| Dimension | Signal | Weight |
|-----------|--------|--------|
| **Adoption** | Engagement / workflow coverage vs. cohort | 25% |
| **Outcome attainment** | Customer's stated success metric progress | 25% |
| **Stakeholder** | Champion engaged in last 90 days, exec sponsor identified | 20% |
| **Commercial signal** | Procurement contact, late payment, MSA review | 15% |
| **Competitive exposure** | Inbound research on competitors, RFI signal | 10% |
| **Support / quality** | Critical-severity ticket trend | 5% |

Bucket into Green / Yellow / Red and route to the matching play.

## Renewal Timeline

| Days Out | Activity | Owner |
|----------|----------|-------|
| **T-180** | Risk score baseline, success-plan refresh | CSM |
| **T-150** | Stakeholder map refresh, exec sponsor re-engaged | CSM + AE |
| **T-120** | Value-realization pack draft, expansion thesis identified | CSM + AE |
| **T-90** | Renewal conversation initiated, EBR or value review | CSM + AE |
| **T-60** | Commercial proposal, terms / pricing | AE + Deal Desk |
| **T-30** | Negotiation + approvals | AE + Legal |
| **T-0** | Signed renewal | All |
| **T+30** | Renewal debrief, NRR / GRR booked, post-renewal plan | CSM |

## Negotiation Posture

Pre-decide posture before the customer asks for a discount.

| Lever | Standard Posture | Red-Risk Posture |
|-------|------------------|------------------|
| **Price** | Hold or uplift per index | Concede to price hold, never below |
| **Term** | 1-yr standard, 3-yr incentive | 1-yr only if needed to save |
| **Payment terms** | Annual upfront | Annual; consider semi-annual to save |
| **Auto-renew** | Standard | Convert to manual if relationship is tense |
| **Volume / true-up** | Annual true-up | Defer true-up one cycle |

Walk-away conditions must be written *before* the negotiation starts.

## Expansion at Renewal

A renewal with no expansion thesis is a missed compounding opportunity.

| Expansion Trigger | Play |
|-------------------|------|
| **Adjacent team adoption signal** | Multi-thread + cross-team workshop |
| **New use case in workflow data** | Solution scoping + scoped expansion proposal |
| **Module attach signal** | Bundle into renewal with multi-year discount |
| **Seat utilization > 85%** | Seat expansion conversation pre-renewal |

## Output

Save to `outputs/renewal-orchestration-[segment]-[YYYY-MM-DD].md`

| Artifact | Description |
|----------|-------------|
| **Risk Scoring Spec** | Signals, weights, thresholds, refresh cadence |
| **Renewal Timeline Template** | T-180 → T+30 with owners and SLAs |
| **Posture Matrix** | Pricing / terms posture by risk tier |
| **Walk-Away Rubric** | Pre-decided "won't go below" conditions per segment |
| **Value Realization Pack Template** | Outcome evidence + ROI presentation |
| **Expansion Play Library** | Triggers → plays → AE/CSM ownership |
| **Renewal Dashboard** | Risk distribution, renewal cohort GRR/NRR, save rate, expansion-at-renewal % |

## Process

1. **Build the risk score** with weighted signals; validate against historical churn
2. **Codify the T-180 → T+30 timeline** with owners and SLAs
3. **Pre-decide posture** at the segment level, not deal-by-deal
4. **Write walk-away conditions** with finance and exec alignment
5. **Standardize the value pack** so every CSM produces consistent evidence
6. **Build the expansion play library** with explicit AE handoff rules

## Tips

1. **Late risk identification is the #1 churn driver** - instrument T-180 baseline
2. **The redline is not the negotiation** - the negotiation is at the value pack
3. **Multi-year discounts must be earned**, not given to close
4. **Auto-renew is a privilege**, not a default; revoke when trust erodes
5. **Always debrief renewals** - wins and losses both teach pricing posture

## Pairs With

- **customer-success** - Health score feeds the risk score
- **revenue-analytics** - NRR / GRR diagnostics rolls renewal outcomes
- **enablement-forge** - Builds the value realization pack and EBR templates
- **revenue-forecasting** - Renewal-stage probability informs the forecast
