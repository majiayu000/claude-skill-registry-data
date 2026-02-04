---
name: data-quality-validation
description: Systematic data validation, error detection, cross-source reconciliation, and query correctness checking for analytical work. Use when validating Snowflake queries, catching calculation errors, reconciling metrics across different data sources, checking for null values, ensuring date range validity, detecting statistical anomalies, validating metric calculations (median vs mean, rate normalization), checking aggregation grain (per-record vs per-entity), validating contribution analysis for non-additive metrics, or validating consistency across analysis sections. Essential when reviewing analysis before publication, debugging unexpected results, or ensuring data quality in reports. Triggers include "validate this query", "check for errors", "why don't these numbers match", "should I use median or mean", "why don't contributions sum to 100%", "reconcile these metrics", "verify data quality", or any request to catch potential issues in data or calculations.
---

# Data Quality & Validation

Systematic framework for catching data quality issues, query errors, metric calculation problems, and inconsistencies before they affect analysis results.

## When to Use This Skill

**Proactive Validation (Before Analysis):**
- Reviewing Snowflake queries for correctness
- Validating date ranges for analysis periods
- Checking for null values in critical fields
- Ensuring balanced time periods for experiments
- Verifying data availability before starting work
- Validating metric choice (median vs mean)
- Checking aggregation grain (per-record vs per-entity)

**Reactive Validation (Investigating Issues):**
- Numbers don't match across different sections
- Unexpected results that seem wrong
- Metrics from different tables don't reconcile
- Analysis shows contradictory patterns
- Stakeholder questions results accuracy
- Averages seem inflated or deflated
- Contributions don't sum to 100%

**Pre-Publication Checks:**
- Final review before sharing analysis
- Cross-checking totals against detail sums
- Validating all percentages sum to ~100%
- Ensuring consistent methodology throughout
- Confirming appropriate metric selection

## Validation Philosophy: Inform, Don't Block

**All validations in this skill are INFORMATIONAL - nothing blocks your analysis.**

### What This Means

**✅ Analysis always proceeds**
- Validations note potential issues
- You decide whether to fix or continue
- Work isn't stopped waiting for "perfect" data

**ℹ️ Three types of responses:**

1. **Informational notes** - Data quality observations
   ```
   ℹ️ Data Quality Note: Field has 8% null values.
      Analysis proceeds with 92% of data.
   ```

2. **Warnings with recommendations** - Suggests improvements
   ```
   ⚠️ Period Balance Issue: POST has 23 days (not multiple of 7).
      Recommendation: Use 21 or 28 days to avoid weekday bias.
      Analysis proceeds with current period.
   ```

3. **Questions for clarification** - Confirms your intent
   ```
   ❓ Vertical Filter Check: You mentioned "for sale leads" but 
      query has no filter. Should this include all verticals?
   ```

**🎯 You always control what happens next:**
- Accept the current approach
- Apply recommended fix
- Investigate flagged issues
- Proceed with noted limitations

### Why This Approach

**Faster iteration**
- Don't wait for perfect data
- Proceed with 90%+ completeness
- Refine in subsequent analyses

**You know your context**
- Might have good reasons for approach
- Can prioritize what matters most
- Decide acceptable trade-offs

**Transparency**
- Always aware of data quality
- Can document caveats in results
- Prepared for stakeholder questions

**Learning opportunity**
- Understand best practices
- Build better queries over time
- Recognize patterns to watch for

### What Gets Validated (All Informational)

| Category | What It Checks | User Decides |
|----------|---------------|--------------|
| **Query Correctness** | Missing GROUP BY, division errors, date ranges | Fix now or run as-is |
| **Data Consistency** | Totals match details, percentages sum, contributions | Investigate or proceed |
| **Cross-Source** | Metrics align across tables | Which source to trust |
| **Null Values** | Missing data in fields | Acceptable % or not |
| **Date Balance** | X*7 day periods for experiments | Adjust period or accept bias |
| **Anomalies** | Statistical outliers | Investigate or include |
| **Vertical Filters** | for_sale/for_rent/seller present | Which vertical(s) to include |
| **Metric Calculation** | Median vs mean, rate normalization | Which metric to use |
| **Aggregation Grain** | Per-record vs per-entity | Which aggregation level |
| **Contribution Analysis** | Non-additive metrics (median) | Accept gap or use mean |

### Response Pattern

Every validation follows this structure:
```
[Icon] [Validation Type]:
   - What was detected
   - Why it might matter
   - Recommendation (if applicable)
   
Analysis proceeds [with current approach / with noted limitation].
```

**You'll see:**
- ℹ️ Informational (for awareness)
- ⚠️ Warning (recommended to address, but optional)
- ❓ Question (needs clarification)
- ✓ Validated (all good)

**You'll never see:**
- ❌ Error - Cannot proceed
- 🛑 Analysis blocked
- ⚡ Must fix before continuing

**Bottom line:** This skill helps you make informed decisions, not enforce rigid rules. You stay in control of your analysis.


## Core Workflow

### Standard Validation Process

**Step 1: Query Correctness**
```
Check before running:
→ Are date ranges correct and properly bounded?
→ Do aggregations have proper GROUP BY clauses?
→ Are calculations using correct formulas?
→ Do divisions use NULLIF to prevent errors?
→ Are there any hardcoded values that should be parameters?
```

**Step 2: Data Quality Checks**
```
After retrieving data:
→ Check for NULL values in critical fields (informational)
→ Verify date ranges match what was requested
→ Look for unexpected patterns or anomalies
→ Validate record counts are reasonable
→ Check for duplicate records if unexpected
```

**Step 3: Metric Calculation Validation**
```
Before calculating metrics:
→ Is data skewed? (Use median instead of mean)
→ Comparing rates at same time scale? (Normalize first)
→ Using correct baseline for percentages?
→ Need weighted average instead of simple average?
```

**Step 4: Aggregation Grain Check**
```
When aggregating:
→ Are there multiple records per entity?
→ Should this be per-record or per-entity calculation?
→ Do duplicates affect the metric?
```

**Step 5: Cross-Section Validation**
```
Within the analysis:
→ Do summary totals equal sum of details?
→ Do percentages sum to ~100% (tolerance for rounding)?
→ For non-additive metrics (median), is gap expected?
→ Are metrics consistent across sections?
→ Do related numbers make logical sense together?
```

**Step 6: Cross-Source Reconciliation**
```
When using multiple tables:
→ Document expected relationship between sources
→ Calculate and explain any differences
→ Validate join keys match properly
→ Identify which source is authoritative
```

## Validation Categories

### 1. Query Correctness

**Common Issues:**
- Date ranges don't match analysis definition
- Unbalanced pre/post periods (different # of weeks)
- Missing or incorrect GROUP BY clauses
- Wrong aggregation level (per-record vs per-entity)
- Division without NULLIF protection

**Quick Validation:**
```sql
-- Add to queries as sanity check
SELECT 
    MIN(event_date) as earliest,
    MAX(event_date) as latest,
    COUNT(*) as total_records,
    COUNT(DISTINCT entity_id) as unique_entities,
    CURRENT_DATE() as today
FROM your_table;
```

**See [validation_framework.md](references/validation_framework.md#1-query-correctness-validation) for detailed patterns**


### 2. Data Consistency

**What to Check:**
- Summary totals = sum of detail rows (within 1%)
- Percentages sum to ~100% (within 0.5% for rounding)
- Contribution analysis for non-additive metrics
- Metrics align across all sections
- No contradictory statements in findings

**Pattern:**
```
1. Extract key totals from each section
2. Calculate expected relationships
3. Flag deviations > 1% threshold (informational)
4. Investigate root cause (usually query mismatch)
```

**Special Case: Contribution Analysis for Non-Additive Metrics**

When contributions don't sum to 100%, check if metric is additive:

**Non-Additive Metrics (Gap is EXPECTED):**
- Median, Percentiles (P25, P75, P90)
- Mode, Min/Max
- Ratios (ROAS = Revenue/Spend)
- Geometric mean

**Response for non-additive:**
```
ℹ️ Contribution Analysis Note (MEDIAN decomposition):
   - Sum of contributions: 3.1pp
   - Actual total change: 4.76pp
   - Gap: 1.7pp (36%)
   
This gap is EXPECTED and CORRECT for median analysis.
   
Why: Median is not an additive metric
   - Cannot decompose as simple weighted sums
   - Gap represents interaction effects between segments
   - Contributions show directional impact (which segments pushed median up/down)
   - Magnitudes are approximate, not exact attributions
   
Key insight: All segments contributed to decline, with Paid Search 
having largest impact due to volume (65%) and magnitude (-2.1%).

Analysis proceeds - this is mathematically correct.
```

**Additive Metrics (Should Sum):**
- Mean (arithmetic average)
- Sum, Count
- Proportions (when all categories included)

**Response for additive with gap:**
```
⚠️ Contribution Analysis Issue:
   - Sum of contributions: 3.2%
   - Actual total change: 4.5%
   - Gap: 1.3% (should be <5% for additive metrics)
   
For MEAN decomposition, contributions should sum to total.
Possible causes:
   - Missing segments not included
   - Calculation error in weights
   - Different time periods for segments vs total
   
Recommendation: Verify all segments included and weights sum to 100%.
Analysis proceeds but results may be incomplete.
```

**See [validation_framework.md](references/validation_framework.md#2-data-consistency-validation) for implementation**

### 3. Cross-Source Reconciliation

**When metrics exist in multiple tables:**

```
Step 1: Identify all relevant tables
Step 2: Document expected relationship
        (equal, subset, filtered version, etc.)
Step 3: Calculate conversion/attrition rates
Step 4: Flag unexpected drops (>20% usually indicates issue)
Step 5: Trace sample records through pipeline
```

**See [common_pitfalls.md](references/common_pitfalls.md#pitfall-4-lead-count-mismatches) for real example**

### 4. Null Value Detection

**Informational - Not Blocking:**

Check for null values in critical fields and **inform the user** so they're aware, but allow analysis to proceed.

**Quick Check:**
```sql
-- Template query for null checking
SELECT 
    COUNT(*) as total,
    SUM(CASE WHEN field IS NULL THEN 1 ELSE 0 END) as null_count,
    ROUND(100.0 * null_count / total, 1) as null_pct
FROM your_table;
```

**What to Report:**
- Primary keys: >0% null (note as data quality concern)
- Foreign keys: >5% null (note potential join issues)
- Price/revenue fields: >10% null (note impact on averages/medians)
- Sudden spike in null % (note potential pipeline problem)

**Response Pattern:**
```
ℹ️ Data Quality Note: Field X has 12% null values (1,234 of 10,000 records).
   This may affect averages/medians. Analysis will proceed with available data.
```

**See [validation_framework.md](references/validation_framework.md#4-nullmissing-value-detection) for full framework**

### 5. Date Range & Period Validation

**For Experiments/A/B Tests:**

Critical rule: When day-of-week patterns exist, **periods MUST be X*7 days**

```python
# Quick check
def validate_period_balance(df, date_col, period_col):
    for period in df[period_col].unique():
        n_days = len(df[df[period_col] == period])
        if n_days % 7 != 0:
            print(f"⚠️ {period}: {n_days} days ({n_days/7:.1f} weeks) - UNBALANCED")
            print(f"   Fix: Use {n_days//7 * 7} or {(n_days//7 + 1) * 7} days")
        else:
            print(f"✓ {period}: {n_days} days ({n_days//7} weeks) - BALANCED")
```

**See [common_pitfalls.md](references/common_pitfalls.md#pitfall-3-day-of-week-imbalance) for real impact**


### 6. Anomaly Detection

**Statistical Outlier Detection:**

```python
from scipy import stats

# Z-score method (3σ = 99.7th percentile)
z_scores = np.abs(stats.zscore(data))
outliers = data[z_scores > 3]
```

**What to Flag (Informational):**
- Spend anomalies: >3σ from 30-day mean
- Volume spikes: Day-over-day change >50%
- Performance anomalies: ROAS doubles suddenly
- Zero values: Sustained zeros in active metrics

**See [validation_framework.md](references/validation_framework.md#6-anomaly-detection) for implementation**

### 7. Vertical Filter Validation

**Critical for Real Estate Data:**

When user mentions specific lead types, always verify the vertical filter is present.

**Lead Type Mentions that Trigger Validation:**
- "for sale" or "buy leads" → Check for `vertical = 'for_sale'` or `submitted_lead_vertical = 'for_sale'`
- "for rent" or "rental leads" → Check for `vertical = 'for_rent'`
- "seller leads" → Check for `vertical = 'seller'` or lead category filters

**Validation Pattern:**
```sql
-- CORRECT: Query with vertical filter
SELECT COUNT(*) as leads
FROM leads_table
WHERE event_date >= '2025-10-01'
  AND vertical = 'for_sale';  -- ✓ Vertical filter present

-- INCORRECT: Missing vertical filter
SELECT COUNT(*) as leads  
FROM leads_table
WHERE event_date >= '2025-10-01';  -- ❌ No vertical filter!
```

**What to Do:**
1. **Check the query** for vertical/lead type filters
2. **If missing**, ask user: "I notice there's no vertical filter - should this be limited to for_sale leads, or include all verticals?"
3. **If present**, verify it matches what user mentioned
4. **Common column names**: `vertical`, `submitted_lead_vertical`, `lead_vertical`, `LEAD_VERTICAL`

**Why This Matters:**
- Mixing verticals can skew metrics significantly
- for_sale vs for_rent have different performance characteristics
- Missing filter = including data user didn't intend

**See [validation_framework.md](references/validation_framework.md#7-vertical-filter-validation) for examples**

### 8. Metric Calculation Validation

**Ensures metrics are calculated appropriately for the data distribution:**

**Auto-detect and recommend:**
- Median vs Mean based on skewness
- Rate normalization for time comparisons
- Weighted vs simple averages
- Percentage calculation consistency

**Common Issues:**
```python
# Issue 1: Using mean for skewed data
Data: [$50K, $80K, $90K, $2M, $5M]
Mean: $1.4M (dominated by outliers)
Median: $90K (representative value)
→ Use MEDIAN for price data

# Issue 2: Comparing unnormalized rates
PRE: 102,085 leads / 28 days
POST: 85,953 leads / 21 days
→ Must normalize to same time unit (daily/weekly)

# Issue 3: Wrong percentage base
Calculating "% change" but using different denominators
→ Always use consistent baseline
```

**Validation Pattern:**
```
1. Check data distribution (skewness)
2. If |skewness| > 1.0 and using mean → Recommend median
3. For rate comparisons → Verify same time scale
4. For percentages → Confirm consistent denominator
```

**Response is informational:**
```
ℹ️ Metric Selection Note:
   - Data is highly skewed (skewness: 2.4)
   - Mean: $450,000
   - Median: $285,000
   - Difference: 58% higher mean due to outliers
   
Recommendation: Consider using MEDIAN for more representative value.
Analysis proceeds with current metric.
```

**See [validation_framework.md](references/validation_framework.md#8-metric-calculation-validation) for implementation**

### 9. Aggregation Grain Validation

**Ensures metrics aggregate at the correct entity level:**

**What to check:**
- Are there duplicate records inflating counts?
- Is calculation per-record or per-entity?
- Do multiple records per entity affect metrics?

**Example Issue:**
```
MCD table: 143K records, 62K unique inquiries
Per-record avg EFR: $12.48 (WRONG - includes duplicates)
Per-inquiry avg EFR: $25+ (CORRECT - one per entity)

Problem: Multiple records per inquiry with $0 EFR dilute average
```

**Validation Pattern:**
```
1. Count total records vs unique entities
2. If records > entities × 1.2 (>20% duplication):
   - Calculate metric both ways
   - Compare per-record vs per-entity
   - If >10% difference → Note grain issue
3. Recommend explicit GROUP BY entity_id
```

**Response is informational:**
```
ℹ️ Aggregation Grain Note:
   - 143,245 records but only 62,866 unique inquiries (2.3x duplication)
   - Per-record average: $12.48
   - Per-inquiry average: $25.14
   - Difference: 101% (doubled!)
   
Recommendation: Consider grouping to inquiry level first:
   SELECT inquiry_id, MAX(efr) as efr
   FROM table GROUP BY inquiry_id
   
Analysis proceeds - user can decide if regrouping needed.
```

**See [validation_framework.md](references/validation_framework.md#9-aggregation-grain-validation) for detailed patterns**


## Loading Reference Files

**When to load validation_framework.md:**
- Implementing any validation check
- Need specific SQL/Python patterns
- Building custom validation logic
- First time using a validation category

**When to load common_pitfalls.md:**
- Investigating unexpected results
- Debugging calculation errors
- Learning from past mistakes
- Quick reference for specific error types

## Quick Decision Tree

```
User says "validate this query/analysis"
  ↓
Load validation_framework.md
  ↓
  ├─ Simple query check → Section 1 (Query Correctness)
  ├─ Check consistency → Section 2 (Data Consistency)  
  ├─ Multiple tables → Section 3 (Cross-Source)
  ├─ Missing data? → Section 4 (Null Detection)
  ├─ Experiment dates → Section 5 (Date Range Validation)
  ├─ Unusual patterns → Section 6 (Anomaly Detection)
  ├─ Mentions "for sale" / "buy leads" → Section 7 (Vertical Filter)
  ├─ Metric selection questions → Section 8 (Metric Calculation)
  └─ Multiple records per entity → Section 9 (Aggregation Grain)

User says "why don't these numbers match" or "this seems wrong"
  ↓
Load common_pitfalls.md first
  ↓
Identify which pitfall pattern matches
  ↓
Apply specific fix from that section
  ↓
Then load validation_framework.md for comprehensive check

User mentions specific lead types ("for sale", "rental", "seller")
  ↓
Check Section 7: Vertical Filter Validation
  ↓
Verify query has appropriate vertical filter
  ↓
If missing, confirm with user which vertical(s) to include

User asks "should I use median or mean?" or "how to compare these rates?"
  ↓
Check Section 8: Metric Calculation Validation
  ↓
Analyze data distribution
  ↓
Recommend appropriate metric

User has unexpectedly high/low averages
  ↓
Check Section 9: Aggregation Grain Validation
  ↓
Verify records vs unique entities
  ↓
Confirm aggregation level

User asks "why don't contributions sum to 100%?"
  ↓
Check metric type (Section 2: Contribution Analysis)
  ↓
  ├─ MEDIAN/PERCENTILE → Explain gap is expected
  └─ MEAN/SUM → Check for missing segments
```

## Validation Checklist

**Before Running Analysis:**
- [ ] Date ranges match definition
- [ ] Periods are balanced (X*7 days if day-of-week patterns exist)
- [ ] Critical fields checked for nulls (informational note if high %)
- [ ] Query has proper GROUP BY and NULLIF
- [ ] Vertical filter present when user mentions lead type
- [ ] Metric choice appropriate for data distribution (median for skewed)
- [ ] Aggregation grain specified (per-record vs per-entity)

**During Analysis:**
- [ ] Summary totals = detail sums
- [ ] Percentages sum to ~100% (99.5-100.5% tolerance for rounding)
- [ ] Contribution analysis validated for metric type:
  - [ ] Non-additive (median/percentile): Gap noted as expected
  - [ ] Additive (mean/sum): Gap <5% or explained
- [ ] Anomalies flagged (informational)
- [ ] Cross-section consistency validated
- [ ] Null percentages noted in results (if significant)
- [ ] Rates normalized to same time scale
- [ ] No duplicate entity inflation

**Before Publication:**
- [ ] All queries reviewed for correctness
- [ ] Cross-source reconciliation complete
- [ ] Data quality issues documented
- [ ] Sensitivity analysis performed (for key findings)
- [ ] Metric calculations verified
- [ ] Aggregation level confirmed

## Common Mistakes to Avoid

1. **Assuming data is correct** - Always validate, even if results look reasonable
2. **Ignoring small discrepancies** - 1% differences often indicate bigger issues
3. **Comparing unbalanced periods** - Critical for time-series analysis
4. **Trusting single source** - Cross-validate important metrics
5. **Skipping pre-checks** - Easier to catch errors before analysis than after
6. **Using mean for skewed data** - Price data almost always needs median
7. **Comparing unnormalized rates** - Always use same time scale
8. **Ignoring duplicate records** - Multiple records per entity distort averages
9. **Expecting median contributions to sum to 100%** - Non-additive metrics have gaps

## Integration with Other Skills

**Use with real-estate-marketing-analytics:**
- Validate marketing metrics before analysis
- Check campaign performance calculations
- Reconcile lead counts across systems
- Verify ROAS and EFR calculations
- Ensure proper vertical filtering

**Use with statistical analysis:**
- Validate experimental design
- Verify balanced control/treatment groups
- Validate statistical test prerequisites
- Check metric appropriateness

**Use before creating deliverables:**
- Final validation before reports
- Cross-check before presentations
- Verify before sharing with stakeholders

## Recovery Pattern

**When You Find an Error:**

1. **Stop and Document**
   - What's wrong
   - How discovered
   - Correct approach

2. **Assess Impact**
   - Which sections affected
   - How much numbers change
   - Do conclusions change

3. **Re-run Corrected Analysis**
   - Update all affected queries
   - Validate consistency
   - Re-check everything

4. **Prevent Recurrence**
   - Add to validation checklist
   - Document in common_pitfalls.md
   - Create reusable validation query

## Success Criteria

**You're using this skill effectively when:**
- Catching errors BEFORE stakeholders do
- Proactively validating instead of reactively debugging
- Building validation into standard workflow
- Documenting validation checks performed
- Explaining data quality caveats when presenting results
- Choosing appropriate metrics for data distribution
- Understanding aggregation grain in your queries
- Recognizing when contribution gaps are expected (non-additive metrics)

