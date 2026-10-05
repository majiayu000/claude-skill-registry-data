---
name: revenue-analytics
description: 'Revenue analytics architecture - ARR / NRR / GRR decomposition, cohort retention, expansion drivers, segment economics, and CAC payback diagnostics. Use when: revenue analytics, ARR waterfall, NRR analysis, GRR, expansion analysis, cohort revenue retention, CAC payback, magic number, segment economics, revenue diagnostics.'
---

# Revenue Analytics (LADDER Framework)

Design a revenue analytics layer that answers *where revenue is being created, where it's leaking, and which lever to pull next* - not a dashboard of vanity totals. LADDER decomposes ARR, attributes it, diagnoses drivers, and turns analysis into named actions.

## Core Principle

**Revenue analytics fails when it stops at the totals.** Reporting ARR up-and-to-the-right tells you nothing actionable. LADDER decomposes revenue into the components a leadership team can act on within a quarter.

## The LADDER Framework

| Letter | Stage | The Question |
|--------|-------|--------------|
| **L** | Leading Indicators | Which forward-looking metrics predict ARR movement 1-2 quarters out? |
| **A** | Attribution | Where does new ARR come from - channel, motion, segment, cohort? |
| **D** | Drivers | Which 3-5 levers explain most of the variance in NRR and growth? |
| **D** | Diagnosis | What's broken or accelerating, and what's the named hypothesis? |
| **E** | Expansion Economics | What's the economics of expansion vs new logo by segment? |
| **R** | Retention Decomposition | What's GRR, contraction, churn - by cohort and reason code? |

## ARR Waterfall

The minimum decomposition every leader should be able to recite:

| Component | Definition |
|-----------|------------|
| **Starting ARR** | Beginning-of-period book |
| **New Logo ARR** | Net-new customer ARR added |
| **Expansion ARR** | Seat / module / price-up from existing customers |
| **Contraction ARR** | Seat / module / price-down from existing customers (not churn) |
| **Churn ARR** | Customers lost (logo or full) |
| **Ending ARR** | Computed from the above |
| **NRR** | (Ending − New Logo) / Starting |
| **GRR** | (Starting − Contraction − Churn) / Starting |

## Leading Indicators

Lagging metrics (ARR, NRR) confirm what already happened. Leading metrics let you act:

| Metric | Leads What | Lead Time |
|--------|------------|-----------|
| **Qualified pipeline coverage (3x)** | Bookings | 1-2 quarters |
| **Engagement score trajectory** | Renewal / NRR | 2 quarters |
| **Health score distribution** | GRR | 1-2 quarters |
| **MQL→SQL conversion** | New logo bookings | 1 quarter |
| **Expansion pipeline coverage** | Expansion ARR | 1 quarter |
| **Win-rate by segment** | Booking productivity | 1 quarter |

## Driver Decomposition

| Driver | Definition | Watch For |
|--------|------------|-----------|
| **Acquisition** | New logo ARR / period | Channel mix shift, win-rate change |
| **Expansion** | Expansion / Starting ARR | Mix of seat vs module vs price |
| **Retention (GRR)** | 1 − (Churn + Contraction) / Starting | Cohort drift, segment concentration |
| **Pricing** | Realized ARPA trend | Discount creep, packaging drift |
| **Mix** | Segment / motion share | Concentration risk, dilution risk |

## Economics

| Metric | Formula | Why |
|--------|---------|-----|
| **CAC Payback (months)** | Fully loaded S&M / (New ARR × gross margin / 12) | Sustainability of acquisition |
| **LTV / CAC** | Gross-margin LTV / CAC | Long-run profitability |
| **Magic Number** | (Net New ARR × 4) / Prior-Q S&M spend | Efficiency of growth motion |
| **Net Magic Number** | Same but using net new ARR (incl. churn) | Truer efficiency view |
| **Expansion ROI** | Expansion ARR / (CS + Expansion S&M cost) | Cheaper growth lane usually |

## Cohort Retention

Cohort retention surfaces what the totals hide:

| Lens | Insight |
|------|---------|
| **Logo retention by acquisition cohort** | When did the product stop retaining? |
| **NRR by ICP segment** | Which segments compound, which decay? |
| **Channel-of-acquisition retention** | Which channels deliver durable revenue? |
| **Use-case retention** | Which use cases retain best? |

## Output

Save to `outputs/revenue-analytics-[scope]-[YYYY-MM-DD].md`

| Artifact | Description |
|----------|-------------|
| **ARR Waterfall** | Period-over-period with segmentation |
| **Leading-Indicator Pack** | 6-8 metrics with thresholds and trend |
| **Driver Decomposition** | Top 3-5 drivers with quantified contribution to variance |
| **Cohort Retention Heatmap** | Cohort × period with segment cuts |
| **Economics Pack** | CAC payback, LTV/CAC, magic number, segment breakdown |
| **Diagnosis Memo** | Anomalies + hypotheses + named owners |
| **Forecast Roll-Up** | Bottoms-up vs tops-down with delta explanation |

## Process

1. **Lock the ARR waterfall definitions** - one source of truth across finance, CS, and sales
2. **Build the leading-indicator pack** with named thresholds, not just charts
3. **Decompose drivers** with explicit attribution; refresh quarterly
4. **Stand up cohort retention** with segment cuts that match motion design
5. **Wire economics** into the operating cadence - not just board prep
6. **Diagnose monthly**: anomaly → hypothesis → owner → action

## Tips

1. **One ARR definition** - every team must agree on what counts as ARR
2. **Cohort > snapshot** - retention totals lie; cohorts don't
3. **Always reason-code** churn and contraction; otherwise the diagnostic loop is closed
4. **Leading indicators with no threshold** are decoration
5. **CAC payback is the most honest growth metric** - easy to game, hard to fake

## Pairs With

- **customer-analytics** - Engagement and behavioral cohorts feed NRR decomposition
- **revenue-forecasting** - Drivers and leading indicators inform the forecast
- **customer-success** - Health-score distribution is a top GRR driver
- **budget-allocator** - Economics inform reallocation decisions
