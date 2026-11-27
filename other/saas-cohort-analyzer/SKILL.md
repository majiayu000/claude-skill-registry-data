---
name: saas-cohort-analyzer
description: "Performs rigorous Software as a Service (SaaS) cohort analysis: retention curves, Lifetime Value (LTV), Customer Acquisition Cost (CAC) payback, Net Revenue Retention (NRR), Gross Revenue Retention (GRR), and expansion versus churn decomposition with dollar-weighted and logo-weighted views. Use when diagnosing retention problems, forecasting Annual Recurring Revenue (ARR), evaluating pricing changes, segmenting customer health, validating product-market fit, or preparing board and investor key-performance-indicator reports."
---

# SaaS Cohort Analyzer

> Cohort math is the single most truthful lens on a subscription business - this skill makes it defensible.

## What this skill is

A repeatable workflow that takes raw subscription data and produces a complete cohort report for a Software as a Service (SaaS) business: retention curves, Lifetime Value (LTV), Customer Acquisition Cost (CAC) payback, Net Revenue Retention (NRR), Gross Revenue Retention (GRR), and the revenue movement bridge. It segments by acquisition channel, Ideal Customer Profile (ICP), and contract type, and flags the easy mistakes (survivorship bias, re-segmentation drift, dollar-logo divergence) before they end up in a board deck.

## What it solves

- Blended NRR numbers that hide segment-level decay
- LTV calculations using revenue (not contribution margin) - overstating returns
- Cohort cherry-picking where only the best months get reported
- Survivorship bias from reporting only cohorts that finished the window
- Confusing logo churn with revenue churn - they tell very different stories

## When to invoke

- Diagnosing whether a retention drop is structural or compositional
- Forecasting next-year Annual Recurring Revenue (ARR) from current cohort behavior
- Evaluating whether a pricing or packaging change actually improved retention
- Preparing the retention section of a board deck or investor update
- Validating product-market fit by comparing later cohorts versus earlier ones

## Phase 1: Define the cohort dimensions

Confirm before any numbers move:
- **Cohort unit**: signup month, first-paid month, contract start, fiscal quarter
- **Population**: all customers, ICP-only, segment (small and medium business / mid-market / enterprise), self-serve versus sales-led
- **Window**: month 0 through month N (12, 24, 36)
- **Revenue type**: Monthly Recurring Revenue (MRR) versus Annual Recurring Revenue (ARR); Net Revenue Retention (NRR) versus Gross Revenue Retention (GRR)
- **Inclusion rules**: trial-to-paid threshold? internal accounts excluded? refunds netted?

Document every exclusion. Report both filtered and unfiltered counts.

## Phase 2: Build the retention matrix

Produce three matrices side-by-side:

- **Logo retention (percent)** - customers active in month N / cohort starting customers
- **Gross Dollar Retention (GDR, percent)** - revenue from cohort in month N / starting revenue, capped at 100% (excludes expansion)
- **Net Dollar Retention (NDR, percent)** - same as GDR but includes expansion, contraction, and churn

Plot each as a curve with at least 6 cohorts overlaid. Look for:
- Smiling curve (NDR > 100%) → expansion engine
- Cliff at month N → annual contract renewal point
- Improving later cohorts → product-market fit signal

## Phase 3: Decompose the movement

For each cohort and period, build the bridge:

| Movement | Definition | Dollar impact | Percent of starting MRR |
|----------|-----------|---------:|------------------:|
| Starting MRR | Cohort MRR at month 0 | $X | 100% |
| Seat or plan expansion | Same logos, more revenue | +$ | x% |
| Reactivations | Re-engaged churned accounts | +$ | x% |
| Contractions | Downgrades or seat loss | −$ | x% |
| Voluntary churn | Customer canceled | −$ | x% |
| Involuntary churn | Payment failure | −$ | x% |
| **Ending MRR** | **Sum** | **$Y** | **NRR%** |

This bridge is the most under-used artifact in SaaS reporting. Always show it.

## Phase 4: LTV and CAC payback

Use contribution-margin LTV (not revenue LTV):

```
LTV = Average Revenue Per Account (ARPA) × Gross margin / Monthly churn rate
```

For high-NRR businesses, use the NRR-adjusted variant:

```
LTV (NRR-adjusted) = ARPA × Gross margin × (1 / (1 + r − NRR_monthly))
```

```
CAC payback (months) = CAC / (ARPA × Gross margin)
```

Benchmarks:
- Small and medium business: under 12 months healthy
- Mid-market: under 18 months healthy
- Enterprise: under 24 months healthy
- LTV/CAC ratio: > 3× is the bar, > 5× is exceptional, < 1× is structural unprofitability

## Phase 5: Segmentation cuts

Re-run the cohort analysis sliced by:
- Acquisition channel (paid, organic, partner, outbound, product-led growth)
- ICP fit score
- Onboarding completion (activated within 30 days versus not)
- Contract length (monthly versus annual)
- Annual Contract Value (ACV) band (< $10k, $10-50k, $50-250k, $250k+)

The blended number always hides the variance - surface the best and worst segment.

## Phase 6: Diagnostics and red flags

- **Survivorship bias**: are you reporting NRR only on fully-completed cohorts?
- **Re-segmentation drift**: have customers moved between segments? Lock segment at cohort creation.
- **Logo versus dollar divergence**: dollar retention much greater than logo retention means concentration risk
- **Late-cohort improvement**: is it real, or is it legacy-plan price increases?

## Output

- Cohort triangles for logos, GDR, and NRR (last 24 months)
- Movement bridge for the most recent quarter
- One-page summary: blended NRR / GRR, LTV, CAC payback, LTV/CAC ratio, with 4-quarter trend
- Top 3 retention drivers and top 3 churn drivers from the segmentation cuts
- Recommended intervention for each churn driver
- Explicit "what we don't know" - data gaps

## Operating rules

**Always**
- Report both logo and dollar metrics
- Show the cohort triangle, not just blended averages
- Use contribution-margin LTV
- Decompose NRR into expansion versus contraction versus churn
- Flag survivorship and re-segmentation biases

**Never**
- Quote NRR without naming the cohort window
- Use trailing-12 churn × 12 as annualized - use the actual cohort
- Hide involuntary churn inside voluntary
- Compare cohorts of different acquisition mix without normalizing
- Confuse logo churn with revenue churn
