---
name: company-teardown
description: Reverse-engineer a target's business model, unit economics, growth drivers, and risk profile from disclosed and inferred data. Use at the start of any sell-side or buy-side mandate, before drafting a CIM section, pitching coverage, or building a financial model. Built around revenue decomposition, cost-structure analysis, capital intensity, and concentration risk.
---

# Company Teardown

## Purpose

Build a fact-based working view of a company — how it makes money, what it actually costs to run, what its capital intensity looks like, who its customers and suppliers are, and where its risks concentrate — before any valuation or model is built.

The teardown is the foundation. A model built on a misread of the business will be precise and wrong.

## Governing Principle

**Read the business before you read the multiple.**

The model is downstream of the teardown. The valuation is downstream of the model. The recommendation is downstream of the valuation. Skip the teardown and every downstream layer is contaminated.

## The Six Lenses Every Teardown Must Cover

A teardown is incomplete unless all six are answered with primary-source evidence.

1. **Revenue lens** — what is sold, to whom, on what economics, growing in what way?
2. **Cost lens** — what is the cost structure, how does it scale, where is operating leverage?
3. **Capital lens** — how capital-intensive is the business, what does the cash flow conversion look like?
4. **Customer / supplier lens** — where is concentration risk, what is the bargaining position?
5. **Competitive lens** — what is the company's structural position, what protects margins?
6. **Governance lens** — who controls the business, what are the incentives, what does ownership want?

## Workflow

### Step 1 — Build the revenue decomposition

Pull the most recent 10-K / 20-F / annual report and the last 4–8 quarters of disclosure. Break revenue along the dimension management reports — typically segment, geography, product, or channel — and then along the dimension that actually predicts behavior, even if management doesn't disclose it.

For each revenue line, build:

- **Revenue model:** subscription, transactional, project, licensing, hardware-and-attach, ad-supported, marketplace take-rate, regulated tariff
- **Volume × price split:** units, transactions, customers — and the price per unit. If management reports growth without the split, estimate from disclosed metrics.
- **Recurring vs. non-recurring:** what % is contractual / subscription / regulated; what % is project / one-time
- **Customer cohort behavior:** retention, expansion, churn — inferred from net revenue retention if disclosed, from gross adds vs. net adds if not
- **Pricing power:** has the company taken price increases? Have they stuck? What does customer churn look like after?

Revenue mix is the single most important slide in any teardown. A "10% growth" business with 80% recurring at 110% NRR is a completely different business from a "10% growth" business with 30% recurring and lumpy project revenue.

### Step 2 — Decompose the cost structure into fixed, variable, and stranded

Walk down the income statement, item by item, and classify each cost:

- **Truly variable costs:** scale linearly with units — COGS components, payment processing, fulfillment, third-party revenue share
- **Step-fixed costs:** flat across volume ranges, jump at break points — facilities, manufacturing lines, regional sales teams
- **Truly fixed costs:** independent of volume in the medium term — corporate overhead, IT platforms, brand spend, R&D
- **Stranded costs:** costs that would not transfer in a carve-out or divestiture — corporate allocations, shared services, public-company costs

For each cost category, estimate:

- % of revenue at current scale
- Sensitivity to revenue change (the implied incremental margin)
- Sensitivity to inflation (labor, commodity, energy exposure)

The cost decomposition reveals where the operating leverage actually sits. A business that converts incremental revenue to EBITDA at 40% is fundamentally different from one that converts at 15% — even if their reported EBITDA margins look similar today.

### Step 3 — Map the unit economics

Build the unit economics from primary disclosure. The framework depends on the business model, but every teardown should answer:

| Business model | Unit economics to build |
|---|---|
| Subscription (B2B SaaS, services) | CAC, gross margin, LTV, payback period, NRR |
| Transactional (payments, marketplace) | Take rate, contribution margin per transaction, frequency, repeat rate |
| Project-based (engineering, consulting) | Utilization, billable rate, gross margin per project, win rate |
| Manufacturing | Gross margin per unit, capacity utilization, contribution margin, ASP trend |
| Retail | Revenue per store, four-wall margin, payback per store, comp sales trend |
| Asset-heavy (infra, real estate, energy) | Yield on invested capital, asset utilization, maintenance capex per asset |

If the disclosure is insufficient to compute the unit economics, name what is missing. The CIM or management presentation should provide it; if it doesn't, that itself is a finding.

### Step 4 — Build the cash flow conversion view

EBITDA is not cash. Build the bridge:

```
EBITDA
  − Stock-based compensation (real cost; back out the add-back)
  − Cash taxes (not book taxes — apply NOL, deferred items)
  − Maintenance capex (separated from growth capex; if not disclosed, estimate as D&A)
  − Change in working capital (AR + Inv − AP, normalized for end-of-period flatter)
  − Cash interest
  − Restructuring / one-time cash outflows that recur every year
  = Unlevered free cash flow (or levered, as needed)
```

Then compute and present:

- **EBITDA-to-FCF conversion %** — the headline metric for cash quality
- **Maintenance capex as % of revenue** — the real ongoing requirement
- **Growth capex as % of revenue** — the discretionary line
- **Working capital intensity (NWC / revenue)** — does it grow with revenue, or is it stable?

A business with 25% EBITDA margin and 80% cash conversion is more valuable than the same headline EBITDA with 40% conversion. Multiples should reflect this; teardowns should surface it.

### Step 5 — Concentration analysis (customer, supplier, geography, channel)

Pull every concentration disclosure: top customer %, top 5/10 customer %, supplier concentration, geographic concentration, channel concentration. Where disclosure is limited (private targets, foreign filers), infer from:

- Customer names referenced in marketing materials, case studies, MD&A
- Supplier disclosures in 10-K risk factors and material contracts
- Geographic revenue by reporting segment
- Channel partner references in earnings calls

For each material concentration:

- **Magnitude:** % of revenue / cost
- **Switching cost:** how locked-in is the relationship?
- **Renewal / contract tenor:** when does the largest customer / supplier contract come up?
- **Direction:** is concentration increasing or decreasing over time?

Concentration is the single most common deal-killer in diligence. The teardown should surface it before the buyer's QofE provider does.

### Step 6 — Competitive position and margin defense

Place the company in its competitive frame. Don't write a Porter essay; answer four specific questions:

- **What is the company's structural position?** (Market leader, fast follower, niche specialist, scale challenger)
- **What protects the margin?** (Brand, switching cost, scale, network effect, regulatory moat, distribution control, IP)
- **Who is the most dangerous competitor and why?** (Often not the largest)
- **How has margin and share trended over the last 3–5 years?** (The actual evidence on whether the moat works)

If margin is declining and share is declining together, the moat is eroding. If margin is holding while share declines, the company may be harvesting. If share is gaining while margin compresses, it may be buying growth. Each of these is a different deal story.

### Step 7 — Ownership, governance, and incentive read

The ownership structure determines what the deal looks like and what counterparty motivations to expect:

- **Capitalization table:** founder, employee, sponsor, public float, strategic minority holders, family
- **Control rights:** dual-class, board composition, blocking minority, drag-along/tag-along
- **Liquidity preferences and preferred stack:** what is owed before common gets paid
- **Management incentives:** option grants, vesting, change-of-control acceleration, single-trigger vs. double-trigger
- **Recent transactions:** secondary sales, sponsor recaps, ESOP transactions, repurchases — what do they tell us about pricing history and shareholder appetite?

For sell-side mandates, this analysis defines the seller's reservation price. For buy-side, it tells you what consideration mix will actually work.

### Step 8 — Synthesize the teardown into a one-page brief

The teardown is not the working file. The deliverable is a one-page brief that answers, in plain language:

- **Business:** what it does, how it makes money, scale
- **Growth drivers:** the 2–3 things that actually drive revenue growth
- **Economics:** EBITDA margin, FCF conversion, ROIC if relevant
- **Concentration:** where is the risk?
- **Position:** market share, competitive frame, moat thesis
- **Ownership:** who controls it, what do they want
- **Investment thesis (one paragraph):** why this business is interesting at the right price, and what would make it not interesting

This page goes into every downstream deliverable — the pitch, the IC memo, the CIM section, the buyer outreach materials.

## Hypotheses to Pressure-Test

1. **"The 'recurring' revenue is less recurring than the headline suggests."** What share of recurring is contractual vs. behavioral? What is the contract tenor distribution?
2. **"The EBITDA margin masks declining unit economics."** Are gross margins holding while SG&A leverage is doing the work? That is mix shift or scale-driven, not earnings power.
3. **"The growth is one customer / one product / one geography away from a reset."** Strip out the largest contributor — what does the underlying growth look like?
4. **"Reported maintenance capex understates the real reinvestment need."** Is D&A higher than disclosed maintenance capex? Is the asset base aging?
5. **"Management's adjustments are doing more work than the operations."** What does EBITDA look like without the adjustments? Is the gap widening over time?

## Quality Checks Before Sharing

- [ ] Revenue decomposed by both the disclosed cut and a behavior-predicting cut
- [ ] Recurring vs. non-recurring split is explicit, with contract tenor where available
- [ ] Cost structure classified into truly variable, step-fixed, truly fixed, and stranded
- [ ] Unit economics built using the right framework for the business model
- [ ] EBITDA-to-FCF bridge built with cash taxes, maintenance capex, and working capital
- [ ] Customer / supplier / geography / channel concentration disclosed with magnitude and trend
- [ ] Margin defense thesis stated, with 3–5 years of margin and share evidence
- [ ] Ownership and management incentive structure documented
- [ ] All material claims sourced to primary disclosure (filing, transcript, contract)
- [ ] One-page brief produced that summarizes the teardown without the working detail

## Common Failure Modes

- **Accepting management's segmentation.** Reporting segments are designed for compensation, not analysis. Re-segment along the dimension that predicts behavior.
- **Headline EBITDA blindness.** Treating reported adjusted EBITDA as cash earnings. Build the bridge.
- **Missing maintenance capex.** Treating all capex as growth and inflating FCF. Capex disclosure separates this; if it doesn't, estimate.
- **Concentration overlooked because it isn't in the risk factors.** Risk factors are minimum disclosure. The real concentration is in the customer list, the geographic mix, and the supplier disclosure scattered across the filings.
- **Margin reading without the trend.** A snapshot says nothing. Five years of margin direction tells the actual story.
- **Ownership ignored.** Sell-side teardowns that don't model the shareholder math produce processes that can't clear approval thresholds.
- **Adjustment acceptance.** Silently adopting every management add-back. Show the company's adjustments, your adjustments, and the delta.

## Deliverable

A working teardown file with the six lenses (revenue, cost, capital, concentration, competitive, governance) fully populated from primary sources, a unit economics build appropriate to the business model, an EBITDA-to-FCF bridge with maintenance capex separated, a one-page synthesis brief with the investment thesis, and a list of disclosure gaps that need to be addressed in management meetings or the data room.
