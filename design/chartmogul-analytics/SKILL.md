---
name: chartmogul-analytics
description: Guide revenue analysis using ChartMogul reports. Use when discussing MRR, ARR, churn, retention, cohorts, or subscription metrics. Helps select the right report and interpret results.
---

Guide revenue conversations by recommending specific ChartMogul reports and surfacing key insights. Focus on answering the user's actual question, not cataloging metrics.

## Decision Framework

Before recommending a report, determine:

1. **What question are they answering?** Growth, retention, unit economics, or comparison?
2. **What granularity matters?** Trend over time, point-in-time snapshot, or cohort breakdown?
3. **Do they need segmentation?** By plan, geography, customer attribute?

## Report Selection

### Growth Questions

- "How is MRR/ARR trending?" → **MRR chart** with movement breakdown
- "Where is growth coming from?" → **MRR Movements** (new business vs expansion)
- "What's our net new MRR?" → **Net MRR Movements** (aggregates per customer)

### Retention Questions

- "Are we retaining revenue?" → **Net MRR Retention** (target: >100%)
- "How much are we losing to churn?" → **Gross MRR Retention** (excludes expansion)
- "When do customers churn?" → **Customer Retention cohort** by signup month

### Churn Investigation

- "Why are we churning?" → **Cohort analysis** segmented by plan or attribute
- "Is churn improving?" → Compare cohorts vertically (same month across vintages)
- "Logo vs revenue churn?" → **Customer Churn Rate** vs **Net MRR Churn Rate**

### Unit Economics

- "What's a customer worth?" → **LTV**
- "Are we pricing well?" → **ARPA** (all customers) vs **ASP** (new business only)

### Benchmarking

- "How do we compare?" → **Benchmarks** filtered by ARR or ARPA range

## Key Distinctions

**Gross vs Net MRR Retention**: Gross excludes expansion (max 100%). Net includes expansion (can exceed 100%). If GRR declining but NRR stable, expansion is masking retention problems.

**ARPA vs ASP**: ARPA includes renewals and expansions. ASP only counts first purchase. Divergence indicates upsell success or pricing changes.

**MRR Movements vs Net MRR Movements**: MRR Movements shows every subscription change. Net MRR Movements aggregates per customer, revealing "Subscribed & Churned" cases.

## Cohort Analysis

Six cohort types: Customer Retention, Net MRR Retention, Customer Churn, Net MRR Churn, Quantity Retention, Quantity Churn.

**Reading cohorts:**

- **Vertical**: Same time point across cohorts (is retention improving?)
- **Horizontal**: Single cohort over time (when do they churn?)
- **Curve shapes**: Flat = healthy, Smile = normal stabilization, Declining = investigate

Don't mix annual and monthly subscriptions in the same cohort.

## Segmentation Options

- **Plans / Plan Groups**: Tier-level comparison
- **Geography**: Country-level filtering
- **Billing Interval**: Monthly vs annual
- **Custom Attributes**: Any attribute you've added to customers

## Interpreting Results

- **NRR > 100%**: Expansion exceeds churn (strong signal to investors)
- **5% monthly churn**: Compounds to ~46% annual loss
- **>85% customer retention**: Companies at this level grow 1.5-3x faster

## MRR Movement Types

| Movement     | Direction | Meaning                              |
| ------------ | --------- | ------------------------------------ |
| New Business | Growth    | First subscription from new customer |
| Expansion    | Growth    | Upgrade or add-on                    |
| Reactivation | Growth    | Returning churned customer           |
| Contraction  | Loss      | Downgrade                            |
| Churn        | Loss      | Cancellation                         |

**Net New MRR** = New Business + Expansion + Reactivation − Contraction − Churn
