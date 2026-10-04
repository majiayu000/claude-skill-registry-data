---
name: Deal Screening
description: Rapid triage of inbound or proactively sourced deal opportunities using a structured scoring rubric, TAM logic, and sponsor-fit criteria to prioritise pipeline.
---

# Deal Screening

## When to use

Use this skill when you receive an inbound teaser or have identified a proactive target and need to decide quickly whether to pursue further diligence. It applies equally to sponsored processes (where a bank or advisor is running a formal auction) and to proprietary sourcing (direct outreach, intermediary referrals, sector screens). The goal is a rapid, defensible go/no-go recommendation -- not a full diligence opinion.

## What it does

Produces a structured screening note that covers: deal summary, thesis fit, market sizing logic, business quality indicators, preliminary financial assessment, key risk flags, and a recommended next action with rationale. The note is written to the standard of a first-stage investment memo -- brief enough to complete in one sitting, rigorous enough to present to a senior deal partner.

## Method

### Step 1 -- Ingest and summarise the opportunity

Read the teaser, CIM executive summary, or the available source material. Extract:
- Company name, sector, geography
- Revenue, EBITDA, and revenue growth rate (LTM and forward, if available)
- Business model (product vs services, recurring vs transactional, B2B vs B2C)
- Process type (auction, bilateral, proprietary) and timeline
- Seller and ownership structure
- Stated reason for sale

Flag immediately if any hard stops appear: regulated industry outside fund mandate, geography outside mandate, revenue too small or too large for target cheque size, obvious ESG exclusions.

### Step 2 -- Thesis fit assessment

Test the opportunity against three filters:

**Sector fit:** Does this business sit within the fund's stated sector focus? If the fund targets tech-enabled services, assess whether the business's revenue model and competitive dynamics match that profile, not just the sector label.

**Stage and scale fit:** Compare LTM revenue and EBITDA against the fund's typical deal size. Account for co-investment appetite if the deal is large. Flag if the business is at an inflection (pre-profitability, recent carve-out, post-restructuring) and whether the fund has the operating capability to manage that complexity.

**Return profile fit:** Estimate entry multiple range from the process terms or comparable transactions. Ask: at a 10-12x EV/EBITDA entry (adjust to sector norms), can this business deliver the fund's target return on a 5-year hold with conservative assumptions? If the required EBITDA growth to justify entry is implausible, flag it here.

### Step 3 -- Market sizing (TAM/SAM/SOM)

Apply the top-down / bottom-up cross-check:

**Top-down:** Start with the total addressable market (TAM) using a named public data point or logical sizing (do not invent figures). Apply penetration rates to arrive at serviceable addressable market (SAM). Cross-check: if the company has X% market share at its stated revenue, does that imply a plausible TAM?

**Bottom-up:** Count the customer universe (how many buyers of this type of product or service exist), multiply by average spend, and cross-check against the top-down figure. If the two are more than 3x apart, note it as a market sizing risk.

State the conclusion in one sentence: is this a large, growing market where a strong player can compound, or a niche market where growth requires share gains?

### Step 4 -- Business quality indicators

Score the following on a traffic-light basis (green / amber / red) with one line of evidence for each:

- Revenue quality: recurring vs transactional, contract length, renewal rate
- Customer concentration: top-5 and top-10 customer revenue share
- Gross margin profile: stated gross margin vs sector benchmarks
- Management team: tenure, track record, sponsor-backed experience
- Competitive moat: proprietary technology, switching costs, brand, regulatory barriers
- Organic growth: organic CAGR vs stated total CAGR (strip out M&A contribution)
- Working capital: does the business generate cash before or after working capital? Is there a working capital trap?

Summarise in 2-3 sentences: what is the core moat, and what is the primary quality risk?

### Step 5 -- Preliminary financial assessment

Using the available financial data (management accounts, teaser financials, or public filings), compute or estimate:

- LTM EBITDA and EBITDA margin
- Revenue growth rate (2-year CAGR minimum)
- EBITDA growth trajectory (expanding, stable, or declining margins)
- Capital expenditure intensity: capex as % of revenue
- Free cash flow conversion: EBITDA less capex, as a rough proxy

If the business has significant add-backs in EBITDA, note the quantum and whether they are one-time or recurring. Apply a conservative "quality of earnings haircut" as a placeholder: flag if adjusted EBITDA could be materially lower than headline EBITDA.

### Step 6 -- Key risk flags (MECE)

Apply a MECE (mutually exclusive, collectively exhaustive) framework across four risk dimensions:

**Business risk:** Demand cyclicality, technology disruption, customer concentration, key-person dependency, regulatory exposure.

**Financial risk:** Leverage headroom at entry, covenant risk, cash flow visibility, working capital seasonality.

**Execution risk:** Integration complexity (if a platform + add-on strategy is planned), management depth, ERP / data infrastructure.

**Macro / market risk:** Interest rate sensitivity on debt service, FX exposure, supply chain concentration.

For each identified risk, state: (a) severity (high/medium/low), (b) probability, and (c) mitigant available to the fund.

### Step 7 -- Recommended next action

Choose one of four outcomes:
1. **Pass to full diligence:** clear thesis fit, no hard stops, financial profile supports target returns.
2. **Conditional pass:** one significant risk flag that requires a single management call or data request to resolve before committing to full process.
3. **Monitor:** interesting asset but either too early in its maturity, priced too aggressively for current vintage, or outside near-term deployment window.
4. **Pass:** hard stop -- sector fit, scale, or return profile cannot be reconciled.

State the recommended next action in one sentence, followed by the top two reasons.

## Inputs

- Teaser, CIM executive summary, or descriptive paragraph about the opportunity
- Fund mandate summary (sector focus, geography, target EBITDA range, target cheque size) -- or confirm it is already known from context
- Any available financials (even one year of revenue and EBITDA is enough to start)
- Process timeline if known

## Output format

A structured screening note with the following sections:
1. Deal summary (5-6 bullet points)
2. Thesis fit (3 short paragraphs: sector, scale, return)
3. Market sizing (top-down / bottom-up cross-check, one conclusion sentence)
4. Business quality scorecard (traffic-light table as prose, not HTML table)
5. Preliminary financial assessment (4-5 bullet points)
6. Key risk flags (MECE four-quadrant, bullet points per dimension)
7. Recommended next action (one sentence + two supporting reasons)

Total length: 600-900 words. Written in concise, institutional prose -- no filler.

## Example

**Input:** "SoftServe Analytics -- B2B SaaS, workforce analytics for mid-market manufacturers. LTM revenue $28M, EBITDA $7M, growing 22% YoY. Founder-led, no institutional capital. Running a bilateral process at 12-14x EV/EBITDA."

**Output excerpt (Business quality scorecard):**
- Revenue quality: GREEN -- 85% ARR, average contract length 24 months, NRR ~110% per management.
- Customer concentration: AMBER -- top customer 18% of revenue; top 5 = 54%. Mitigant: each contract independently renewed, no single renewal risk in next 12 months.
- Gross margin: GREEN -- 73% gross margin, consistent with best-in-class vertical SaaS.
- Management: AMBER -- founder-CEO, no prior sponsor-backed experience. COO hired 18 months ago from [large software company], strong operational profile.
- Competitive moat: GREEN -- proprietary ML layer trained on 8 years of customer data; switching cost is high due to ERP integration depth.
