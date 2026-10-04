---
name: lbo-returns-analysis
description: Build a structured LBO returns analysis with bear/base/bull scenarios, MOIC and IRR sensitivity to entry multiple and leverage, and covenant headroom assessment.
---

# Financial Scenario Modelling

## When to use

Use this skill when you need to build or stress-test the returns analysis for an LBO acquisition. It is most useful in three situations: (1) ahead of an indicative bid, when you need to establish the range of supportable entry prices; (2) ahead of a final bid, when you need to refine the model with updated diligence data; or (3) ahead of the IC memo, when you need to present returns under clearly defined scenarios with transparent assumptions. This skill structures the logic and the sensitivity analysis -- it does not replace a live Excel model, but it defines what that model must contain and what assumptions to test.

## What it does

Produces: (1) a structured LBO model logic description (sources and uses, capital structure, operating assumptions, exit assumptions); (2) bear/base/bull scenario assumptions clearly differentiated; (3) a returns sensitivity table described in prose (MOIC and IRR vs entry multiple and exit multiple, and vs leverage and interest rate); and (4) a covenant headroom analysis and downside protection assessment.

## Method

### Step 1 -- Sources and uses of funds

Define the transaction structure:

**Enterprise value (entry):** EV = entry multiple x LTM EBITDA (or NTM EBITDA if forward-looking). State both the multiple and the EBITDA base. Note whether EBITDA is management-adjusted or QoE-adjusted -- always use QoE-adjusted as the base after financial diligence.

**Sources of funds:**
- Senior secured debt (first lien, revolving credit facility)
- Subordinated or mezzanine debt (if applicable)
- Equity contribution (sponsor equity + management rollover)
- Any seller financing or earnout

Compute: total debt / EBITDA (leverage ratio), equity contribution as % of EV, and net debt at close.

**Uses of funds:**
- Equity to seller
- Debt repayment at close (if refinancing existing debt)
- Transaction fees and expenses (M&A advisory, legal, financing fees)
- Working capital adjustments
- Any capex or integration investment committed at close

Verify that sources = uses. The equity check is: EV minus net debt at close minus fees equals equity deployed.

### Step 2 -- Operating model assumptions (three scenarios)

Define bear, base, and bull cases across four operating dimensions. Each scenario must be internally consistent -- bear case assumptions should all be conservative, not selectively pessimistic on one line and optimistic on another.

**Revenue growth:**
- Base: management plan revenue growth rate, validated against historical CAGR and commercial diligence findings.
- Bull: acceleration scenario (new product launch, geographic expansion, or M&A contribution). Must be bounded by what is plausible, not what is hoped for.
- Bear: recession or market softness scenario. For subscription businesses, model revenue as a function of beginning ARR, new ARR booked, and gross churn. For project-based businesses, model a drop in average deal value or win rate.

**EBITDA margin:**
- Base: stable margin with modest operating leverage on fixed costs.
- Bull: margin expansion driven by revenue mix shift toward higher-margin products or scale efficiencies in G&A.
- Bear: margin compression -- volume shortfall without proportional cost reduction. For labour-intensive businesses, model the minimum margin floor (fixed cost base divided by bear-case revenue).

**Capital expenditure:**
- Base: maintenance capex at historical run rate as % of revenue; growth capex per approved plan.
- Bull: no incremental growth capex required; organic expansion funded within operating budget.
- Bear: higher maintenance capex required (deferred investment, technology refresh cycle, or facility repair).

**Working capital:**
- Base: neutral working capital movement, consistent with historical days sales outstanding (DSO), days payable outstanding (DPO), and days inventory outstanding (DIO).
- Bull: working capital improvement through DSO reduction or DPO extension.
- Bear: working capital deterioration -- growth requires cash investment, or customer payment terms lengthen.

### Step 3 -- Debt schedule and interest

For each debt tranche:
- Opening balance at close
- Amortisation schedule (% of original principal per year; typical senior secured: 1% amortisation with bullet at maturity)
- Interest rate (fixed or floating; for floating, state the benchmark rate assumption and the spread)
- Maturity date
- Prepayment flexibility (is there a prepayment premium or call protection?)

Compute total interest expense per year and total debt service. Compute free cash flow after debt service (FCF post-debt service) under each scenario. This is the primary driver of equity value accrual.

For the bear case: compute the minimum EBITDA required to service debt covenants. Standard covenants include: net leverage ratio (total debt / EBITDA) and interest coverage ratio (EBITDA / interest expense). State the headroom in the bear case.

### Step 4 -- Exit assumptions

**Hold period:** Standard 5-year base case. Present sensitivity to 3-year and 7-year holds to show the IRR impact of early or late exit.

**Exit multiple:**
- Base: exit at entry multiple (no multiple expansion or compression). This is the most conservative and defensible assumption in most markets.
- Bull: exit at entry multiple + 1-2 turns (sector re-rating, multiple expansion from software label, or premium for scale).
- Bear: exit at entry multiple minus 1-2 turns (market softness, sector de-rating, or forced sale in poor conditions).

**Exit EBITDA:** Apply the scenario EBITDA in year 5. Exit equity value = (exit multiple x exit EBITDA) minus net debt at exit.

**Net debt at exit:** Starting net debt, minus annual FCF post-debt service, compounded over the hold period. In the bear case, verify that net debt does not increase -- if FCF is insufficient to cover interest, debt can accrete.

### Step 5 -- Returns computation

For each scenario, compute:
- Gross MOIC = exit equity value / entry equity investment
- Gross IRR = the discount rate that makes the NPV of (negative entry equity, positive exit equity) equal to zero

Present a sensitivity table described in prose:
- **Entry multiple sensitivity:** Hold exit multiple, exit EBITDA, and leverage constant. Show MOIC and IRR at entry multiples ranging from the floor (minimum supportable) to the ceiling (maximum bid).
- **Exit multiple sensitivity:** Hold entry assumptions constant. Show MOIC and IRR at exit multiples from bear to bull.
- **Leverage sensitivity:** Show returns at 4x, 5x, and 6x entry leverage. Higher leverage amplifies returns in the bull case and amplifies losses in the bear case.

Flag the specific entry multiple at which the base-case IRR falls below the fund's target return threshold. This is the bid ceiling.

### Step 6 -- Covenant headroom and downside analysis

The bear case must be stress-tested against financial covenants:

- Identify the binding covenant (usually net leverage or interest coverage)
- Compute the covenant level in the bear case in each year of the hold
- Compute headroom as: (actual ratio minus covenant level) / covenant level, expressed as a percentage
- Flag if headroom falls below 15-20% in any year -- this indicates material covenant breach risk in a downside scenario

**Equity cushion analysis:** In the bear case, compute the implied equity value at the point of maximum stress (typically year 2-3). If implied equity value turns negative in the bear case, the transaction carries default risk, not just return risk.

**Structural protections to consider:** PIK toggle provisions, equity cure rights, covenant resets, and the ability to inject additional equity to cure a breach. Note whether the proposed credit agreement includes these.

## Inputs

- Entry multiple range (from process terms or comparable transactions)
- QoE-adjusted LTM EBITDA
- 3-5 year management financial projections
- Proposed capital structure (debt quantum and terms, if from a financing bank)
- Fund target IRR and hold period
- Exit multiple range assumption

## Output format

Six sections:
1. Sources and uses summary (prose with key figures)
2. Operating model assumptions (bear/base/bull table described in prose, one row per assumption)
3. Debt schedule summary (per tranche, with annual interest and FCF post-service)
4. Exit assumptions (prose, with hold period and multiple range)
5. Returns summary (MOIC and IRR per scenario; sensitivity described in words)
6. Covenant headroom and downside analysis (bear-case covenant check, equity cushion)

Total length: 900-1,300 words. Written to brief a CFO or chief investment officer.

## Example

**Bear-case covenant check (excerpt):**
At 5x entry leverage on $10M QoE EBITDA, opening debt is $50M. In the bear case, EBITDA declines to $8.5M in year 1 (15% miss vs management plan) before recovering to $9.2M in year 2. The net leverage covenant is set at 5.5x, stepping down to 5.0x in year 2. In year 1, net leverage in the bear case is 5.6x (debt $49.3M after minimal amortisation, EBITDA $8.5M) -- which breaches the year 1 covenant of 5.5x by 0.1 turns. Covenant headroom is negative, implying the deal requires either a higher initial covenant cushion negotiated at close, a more conservative entry leverage of 4.5x, or an equity cure provision in the credit agreement.
