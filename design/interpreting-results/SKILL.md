---
name: interpreting-results
description: Component skill for systematic result interpretation with intellectual honesty in DataPeeker analysis sessions
---

# Interpreting Results

## Purpose

This component skill guides rigorous, intellectually honest interpretation of query results. Use it when:
- Analyzing query outputs to draw conclusions
- Need to avoid premature or biased interpretations
- Considering alternative explanations before committing to conclusions
- Referenced by process skills requiring result interpretation

## Prerequisites

- Query executed and results obtained
- Query documented with rationale (use `writing-queries` skill)
- Understanding of data source and quality (use `understanding-data` skill)
- Analysis context and goals clearly defined

## Result Interpretation Process

Create a TodoWrite checklist for the 6-step interpretation framework:

```
Phase 1: Understand Context
Phase 2: Describe Patterns
Phase 3: Generate Alternative Explanations
Phase 4: Assess Significance
Phase 5: State Conclusions with Caveats
Phase 6: Identify Follow-up Questions
```

Mark each phase as you complete it. Document all interpretations in numbered markdown files.

---

## Phase 1: Understand Context

**Goal:** Ground interpretation in business and analytical context before looking for patterns.

### Recall Analytical Question

Before interpreting results, explicitly state:

```markdown
## Context for Interpretation

**Original Question:** [What we set out to answer]

**Why This Matters:** [Business context and decisions that depend on this answer]

**Hypothesis (if applicable):** [What we expected to find, and why]

**Data Period:** [Time range covered by results]

**Filters Applied:** [Any exclusions or subsets]

**Known Data Limitations:** [Quality issues, missing data, coverage gaps]
```

### Consider External Factors

Ask yourself:

1. **What was happening during this time period?**
   - Seasonality (holidays, end-of-quarter, etc.)
   - Business changes (promotions, product launches, policy changes)
   - External events (economy, weather, competition)

2. **How might this affect results?**
   - Example: High December sales might be holiday-driven, not a trend
   - Example: Spike in refunds might correlate with product recall

3. **What context is needed to interpret these numbers?**
   - Industry benchmarks
   - Historical performance
   - Comparable segments or time periods

**Document:** External factors that might explain or confound results.

### Define Success Criteria

Before calling results "good" or "bad", define what you're comparing to:

```markdown
## Success Criteria

**Comparing to:**
- Historical baseline: [e.g., "Q1 2023 had $500K revenue"]
- Target/goal: [e.g., "Target was 10% growth"]
- Industry benchmark: [e.g., "Industry average conversion is 2.5%"]
- Control group: [e.g., "Comparing treatment to control segment"]

**Threshold for meaningful difference:**
- [e.g., "Need >5% difference to be operationally significant"]
```

**Don't proceed to pattern identification without context.**

---

## Phase 2: Describe Patterns

**Goal:** Objectively describe what the data shows before explaining why.

### Start with Descriptive Statements

Describe results using neutral, factual language:

**DO:**
- "Category A has 2.3x the revenue of Category B ($450K vs $195K)"
- "Sales declined 15% from January to February (10,234 → 8,699 units)"
- "Day-of-week distribution ranges from 12.8% (Sunday) to 16.2% (Friday)"
- "Top 3 products account for 45% of total revenue"

**DON'T:**
- "Category A is performing well" (What's the baseline?)
- "Sales are dropping" (Implies negative trend without context)
- "Friday is the best day" (Best by what measure? Compared to what?)
- "These products are successful" (Define success first)

### Identify Pattern Types

Categorize what you observe:

**Magnitude patterns:**
```markdown
- Absolute values: [e.g., "Total revenue: $1.2M"]
- Relative comparisons: [e.g., "Region A is 3x larger than Region B"]
- Distributions: [e.g., "80% of revenue from 20% of customers"]
```

**Time patterns:**
```markdown
- Trends: [e.g., "Monthly growth averaged 5% over 6 months"]
- Cycles: [e.g., "Weekly pattern peaks mid-week, dips on weekends"]
- Anomalies: [e.g., "March 15 spike to 3x normal daily volume"]
```

**Relationship patterns:**
```markdown
- Correlations: [e.g., "Higher price segments have lower order counts"]
- Segments: [e.g., "B2B customers have 4x higher average order value than B2C"]
- Thresholds: [e.g., "Sharp drop-off in conversion above $100 price point"]
```

### Quantify Patterns Precisely

Use specific numbers, not vague terms:

**Vague:** "Sales increased significantly"
**Precise:** "Sales increased 23% (1,234 → 1,518 units), a gain of 284 units"

**Vague:** "Most customers prefer Category A"
**Precise:** "58% of customers (2,340 of 4,034) purchased from Category A"

**Vague:** "There's a big difference between segments"
**Precise:** "Segment 1 average: $127, Segment 2 average: $89, difference of $38 (43%)"

### Check for Data Artifacts

Before accepting patterns as real, verify they're not artifacts:

```sql
-- Verify: Is this pattern real or a data issue?

-- Check for row count consistency
SELECT COUNT(*) FROM results;  -- Does this match expectations?

-- Check for NULL inflation
SELECT COUNT(*) - COUNT(column_name) as null_count FROM results;

-- Check for duplicate records
SELECT COUNT(*) as total_rows, COUNT(DISTINCT id) as unique_ids FROM results;

-- Check for incomplete periods
SELECT MIN(date), MAX(date), COUNT(DISTINCT date) as date_count FROM results;
```

**Document:** Any data quality issues that might create misleading patterns.

---

## Phase 3: Generate Alternative Explanations

**Goal:** Consider multiple explanations before committing to one.

This is the most critical phase for intellectual honesty. **Premature explanation is the enemy of good analysis.**

### Brainstorm Alternative Hypotheses

For each pattern identified, generate at least 3 possible explanations:

```markdown
## Pattern: Friday has 16.2% of weekly sales vs 12.8% on Sunday

### Possible Explanations:

1. **Consumer behavior:** People shop more on Fridays (payday, preparing for weekend)
   - Testable: Do other metrics (sessions, conversion rate) also peak Friday?

2. **Business operations:** We run promotions on Fridays
   - Testable: Check promotion calendar, compare promoted vs non-promoted Fridays

3. **Data artifact:** Incomplete weeks in dataset skew day-of-week calculation
   - Testable: Count how many of each weekday are in dataset

4. **Seasonality interaction:** Dataset includes holiday weeks where Friday patterns differ
   - Testable: Split analysis into holiday vs non-holiday weeks

5. **Geographic mix:** Different time zones make "Friday" broader (Friday in US, Saturday in Asia)
   - Testable: Segment by customer timezone if available
```

### Use the "Why Might This NOT Be True?" Test

For your preferred explanation, actively argue against it:

```markdown
## Preferred Explanation: Customers shop more on Fridays due to payday

### Why this might be WRONG:

- Many customers have direct deposit on different days
- Weekend shopping (Sat/Sun) should be higher if it's leisure time
- No evidence yet that Friday shoppers are paid-on-Friday workers
- Pattern might be driven by small number of large B2B orders
- Could be specific to this dataset's time period only

### What would convince me this is RIGHT:

- [ ] Friday pattern consistent across multiple months/quarters
- [ ] Segmentation shows pattern strongest for consumer (not B2B) purchases
- [ ] Individual customer purchase history shows Friday preference
- [ ] Pattern persists after removing outlier large orders
- [ ] Industry data confirms Friday shopping peak
```

### Consider Confounding Variables

Identify factors that might explain the pattern instead of your hypothesis:

**Template:**

```markdown
## Potential Confounds

1. **[Confound name]:** [How it could explain the pattern]
   - Test: [How to rule this in/out]

Example:

1. **Marketing send schedule:** Email campaigns go out Thursday, driving Friday purchases
   - Test: Compare Friday sales on campaign weeks vs non-campaign weeks

2. **Product mix:** High-value products launched mid-dataset period
   - Test: Segment analysis into before/after product launch

3. **Measurement error:** Weekend orders processed Monday, suppressing Sunday counts
   - Test: Check order_date vs processed_date, validate weekend entries
```

### The "And" vs "Or" Test

Distinguish between:
- **Exclusive explanations** (A OR B is true, not both)
- **Contributing factors** (A AND B AND C all contribute)

```markdown
## Explanation Type

This pattern is likely caused by:
- [ ] Single dominant factor (identify the ONE cause)
- [x] Multiple contributing factors (list all contributors)

If multiple factors:
- Factor 1: [Estimated contribution]
- Factor 2: [Estimated contribution]
- Factor 3: [Estimated contribution]

Testable: Can we quantify each factor's contribution?
```

---

## Phase 4: Assess Significance

**Goal:** Determine if patterns are meaningful before acting on them.

### Statistical Significance (Directional)

While we can't run formal statistical tests without additional tools, we can reason about significance:

```markdown
## Significance Assessment

**Sample size:**
- [e.g., "Based on 10,234 orders over 90 days"]
- [Is this enough data to trust the pattern?]

**Effect size:**
- [e.g., "15% difference between segments"]
- [Is the difference large enough to matter?]

**Consistency:**
- [e.g., "Pattern appears in 8 of 10 months"]
- [Is this stable or fluctuating wildly?]

**Variance:**
- [e.g., "Group A: 100 ± 45, Group B: 150 ± 12"]
- [Do ranges overlap significantly?]
```

### Practical Significance

Even if a pattern is statistically real, is it actionable?

**Questions to ask:**

1. **Is the difference large enough to matter operationally?**
   ```markdown
   - Finding: Segment A has 2% higher conversion than Segment B
   - Volume: Segment B is 50x larger
   - Practical significance: Optimizing Segment B (even with lower rate) has
     25x more impact than Segment A
   - Conclusion: Pattern is real but not the priority
   ```

2. **Can we actually act on this finding?**
   ```markdown
   - Finding: Customers in ZIP codes starting with "9" have higher LTV
   - Actionability: We can't control customer ZIP codes
   - Practical significance: Low - interesting but not actionable
   - Alternative: Look for correlated factors we CAN influence
   ```

3. **What's the cost/benefit of acting?**
   ```markdown
   - Finding: 3% revenue increase if we extend hours to 10pm
   - Cost: Staffing, utilities for extra 2 hours
   - Benefit: 3% of $1M = $30K annual revenue increase
   - Margin: Estimated $8K net profit after costs
   - Assessment: Marginally significant, requires testing
   ```

### Error Bar Reasoning

Without formal confidence intervals, reason about uncertainty:

```markdown
## Uncertainty Assessment

**Data quality confidence:** [High/Medium/Low]
- [Any known issues with data accuracy?]

**Sample representativeness:** [High/Medium/Low]
- [Does this sample represent the broader population?]
- [Any selection bias in how data was collected?]

**Temporal stability:** [High/Medium/Low]
- [Will this pattern hold next month? Next year?]
- [Dependent on temporary conditions?]

**Overall confidence in pattern:** [High/Medium/Low]
- [Considering all factors, how confident are we this is real?]
```

---

## Phase 5: State Conclusions with Caveats

**Goal:** Make clear, hedged claims that accurately represent certainty level.

### Use Appropriate Hedging Language

Match your language to your confidence level:

**High confidence:**
- "The data clearly shows..."
- "We can conclude that..."
- "This pattern is consistent and robust..."

**Medium confidence:**
- "The data suggests..."
- "This pattern appears to indicate..."
- "The most likely explanation is..."

**Low confidence:**
- "There is weak evidence that..."
- "One possible interpretation is..."
- "We observe a pattern, but it could be explained by..."

**Inappropriate hedging:**
- Avoid: "The data proves..." (data doesn't prove, it provides evidence)
- Avoid: "Obviously this means..." (if it's obvious, you don't need data)
- Avoid: "This clearly demonstrates..." (unless confidence is truly high)

### Separate Observation from Inference

Structure conclusions to distinguish facts from interpretations:

```markdown
## Conclusions

### What We Observed (Facts)
- Friday sales averaged 16.2% of weekly total (vs 14.3% expected if uniform)
- This pattern appeared in 11 of 12 months studied
- Friday average order value ($127) is similar to weekly average ($124)
- Friday transaction count is 18% higher than Sunday (2,340 vs 1,980)

### What We Infer (Interpretations)
- Friday traffic increase (not AOV increase) drives higher sales
- Pattern is stable across most months (except December outlier)
- This is likely a behavioral pattern, not a pricing or promotion effect

### Confidence Level: Medium-High
- Strong evidence for Friday traffic pattern
- Insufficient data on WHY (customer motivation unclear)
- Need to rule out confounds (marketing calendar, staffing changes)
```

### Explicitly State Limitations

Every conclusion should include what you DON'T know:

```markdown
## Caveats and Limitations

**What this analysis does NOT tell us:**
- [e.g., "We don't know if Friday shoppers are different people or same
   people shopping more frequently"]
- [e.g., "We can't determine causation from this correlation"]
- [e.g., "This dataset doesn't include abandoned carts, only completed purchases"]

**Assumptions we made:**
- [e.g., "Assumed all timestamps are in local timezone"]
- [e.g., "Treated returns as separate from original purchase date"]

**Data quality concerns:**
- [e.g., "First two weeks of January had incomplete data"]
- [e.g., "Product category field was NULL for 5% of records"]

**Generalizability limits:**
- [e.g., "This analysis covers only online sales, not in-store"]
- [e.g., "Time period includes major pandemic shifts, may not represent normal behavior"]
```

### The "So What?" Test

Force yourself to state the implications clearly:

```markdown
## Implications

**For decision-makers:**
- [What should they DO differently based on this finding?]
- [What should they STOP doing?]
- [What remains uncertain that needs more investigation?]

Example:

**For marketing team:**
- Consider scheduling campaigns for Thursday delivery (to catch Friday traffic)
- Don't assume Friday success will translate to other days
- Test: Run A/B test with campaign timing to validate causal relationship

**For ops team:**
- Current Friday staffing appears adequate (no degradation in service metrics)
- Monitor: Watch for Friday capacity constraints as volume grows

**For analytics team:**
- Investigate: Why do customers shop more on Fridays?
- Build: Day-of-week forecasting model to improve inventory planning
```

---

## Phase 6: Identify Follow-up Questions

**Goal:** Turn conclusions into next analytical steps.

### Generate "Next-Level" Questions

Good analysis creates more questions than it answers:

```markdown
## Follow-up Questions

### Questions to deepen understanding:
1. [Question that drills into WHY pattern exists]
   - Data needed: [What data would answer this?]
   - Query approach: [How would we query for this?]

2. [Question that tests alternative explanation]
   - Data needed: [...]
   - Query approach: [...]

### Questions to test generalizability:
3. [Does this pattern hold in different segments?]
   - Segment by: [Customer type, product category, region, etc.]

4. [Is this pattern stable over time?]
   - Test: [Earlier time periods, recent vs historical]

### Questions to assess actionability:
5. [Can we influence this pattern?]
   - Experiment: [What intervention could we test?]

6. [What's the ROI of acting on this finding?]
   - Calculate: [Revenue impact, cost, net benefit]
```

### Prioritize Follow-up Questions

Not all questions are equally valuable:

```markdown
## Question Prioritization

**High Priority (Do Next):**
- [Questions that directly inform pending decisions]
- [Questions that could refute our main conclusion]
- [Questions that are cheap/fast to answer with existing data]

**Medium Priority (Do Eventually):**
- [Questions that deepen understanding but don't change decisions]
- [Questions that require additional data collection]

**Low Priority (Backlog):**
- [Interesting but not actionable]
- [Questions that would take significant effort for marginal insight]
```

### Design Follow-up Analyses

For high-priority questions, sketch the analysis:

```markdown
## Proposed Follow-up Analysis

**Question:** Does Friday pattern vary by customer segment?

**Hypothesis:** Business customers drive Friday peak (ordering for next week)

**Data needed:**
- Customer segment field (B2B vs B2C)
- Order data with day-of-week already calculated

**Query approach:**
```sql
-- Compare day-of-week patterns by segment
SELECT
  customer_segment,
  day_of_week,
  COUNT(*) as order_count,
  SUM(amount) as revenue,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY customer_segment), 2) as pct_of_segment
FROM orders_with_dow
GROUP BY customer_segment, day_of_week
ORDER BY customer_segment, day_of_week;
```

**Expected outcome:**
- If hypothesis correct: B2B will show stronger Friday peak than B2C
- If hypothesis wrong: Pattern will be similar across segments
- Alternative: Entirely different day-of-week pattern by segment

**Decision impact:**
- If B2B-driven: Focus Friday capacity on B2B fulfillment
- If B2C-driven: Focus Friday capacity on consumer experience
```

---

## Documentation Requirements

After completing all 6 phases, create an interpretation summary:

```markdown
## Result Interpretation Summary

### Context
- Question: [What we set out to answer]
- Data: [What we analyzed]
- Time period: [Coverage]

### Key Findings
1. [Finding 1 with supporting numbers]
2. [Finding 2 with supporting numbers]
3. [Finding 3 with supporting numbers]

### Interpretation
[2-3 paragraph narrative explaining what findings mean]

### Confidence Assessment
- Overall confidence: [High/Medium/Low]
- Key uncertainties: [What remains unknown]
- Supporting evidence: [What makes us confident]
- Contradicting evidence: [What makes us uncertain]

### Caveats
- [Limitation 1]
- [Limitation 2]
- [Limitation 3]

### Recommendations
1. [Actionable recommendation with rationale]
2. [Actionable recommendation with rationale]
3. [Further investigation needed]

### Follow-up Questions
- High priority: [Question 1]
- High priority: [Question 2]
- Medium priority: [Question 3]
```

---

## Common Interpretation Pitfalls

### Pitfall 1: Confirmation Bias

**Problem:** Seeing what you expect to see, ignoring contradictory evidence.

**Example:**
- Hypothesis: "Campaign increased sales"
- Finding: Sales up 10% during campaign
- Bias: Concluding campaign worked without checking control group
- Missed: Sales were up 12% overall that week (campaign underperformed!)

**Prevention:**
- Always generate alternative explanations (Phase 3)
- Actively look for evidence against your hypothesis
- Use comparison groups (before/after, treatment/control)

### Pitfall 2: Correlation ≠ Causation

**Problem:** Assuming that because A and B move together, A causes B.

**Example:**
- Finding: "Higher-priced products have lower return rates"
- Causal claim: "Raising prices will reduce returns" (WRONG!)
- Reality: Quality drives both price and returns (confound)

**Prevention:**
- Distinguish correlation from causation in language
- Identify potential confounding variables
- Design experiments to test causation (not just observe correlation)

### Pitfall 3: Cherry-Picking

**Problem:** Highlighting patterns that support your story, hiding those that don't.

**Example:**
- Finding: Segment A had 20% growth, Segment B had 5% growth, Segment C declined 8%
- Cherry-pick: "We're seeing strong growth in key segments!" (only mention A & B)
- Honest: "Mixed results: growth in 2 of 3 segments, overall trend uncertain"

**Prevention:**
- Report all segments, not just interesting ones
- Include negative/null findings
- Predefine what you'll measure before looking at data

### Pitfall 4: Texas Sharpshooter Fallacy

**Problem:** Finding patterns in noise, then creating explanations post-hoc.

**Example:**
- Finding: "Sales spike every 3rd Tuesday when temperature is above 75°F"
- Reality: Random noise, but you found a pattern in 3 instances
- Test: Does pattern predict NEXT 3rd Tuesday above 75°F? (Probably not)

**Prevention:**
- Test patterns on hold-out data (future time period)
- Ask: "Would I have predicted this pattern before seeing data?"
- Calculate: How many patterns did I check? (Multiple comparisons problem)

### Pitfall 5: Ignoring Base Rates

**Problem:** Misinterpreting percentages without considering absolute numbers.

**Example:**
- Finding: "New product line has 50% higher conversion rate!" (2% vs 3%)
- Ignored: New line has 1/100th the traffic of main line
- Reality: Absolute impact is tiny (20 vs 5,000 conversions)

**Prevention:**
- Report both percentages and absolute numbers
- Consider volume when assessing significance
- Calculate absolute impact, not just relative change

### Pitfall 6: Simpson's Paradox

**Problem:** Aggregate trends that reverse when data is segmented.

**Example:**
- Aggregate: Treatment group has worse outcomes than control
- Segmented: Treatment is better in EVERY segment
- Cause: Treatment group had more severe cases (confound)

**Prevention:**
- Segment data by key dimensions
- Check if aggregate pattern holds within segments
- Identify potential confounding factors

### Pitfall 7: Survivorship Bias

**Problem:** Analyzing only data that "survived" to be recorded, missing the full picture.

**Example:**
- Finding: "Our top customers have 80% retention rate!"
- Missed: You only analyzed customers who made it to "top" status
- Reality: 95% of customers churned before becoming "top"

**Prevention:**
- Define population carefully (all customers vs top customers)
- Analyze attrition/dropout before looking at survivors
- Include "failed" cases in analysis

---

## When to Revisit Interpretation

Re-run portions of this skill when:
- New data becomes available (test if conclusions hold)
- Stakeholders challenge your conclusions (strengthen with alternative explanations)
- You're about to make a major decision based on findings (verify confidence level)
- Follow-up analyses contradict initial findings (update interpretation)

---

## Integration with Process Skills

Process skills reference this component skill with:

```markdown
Use the `interpreting-results` component skill to systematically interpret query outputs, ensuring intellectual honesty and avoiding premature conclusions.
```

This ensures analysts:
1. Consider context before interpreting patterns
2. Describe patterns objectively before explaining them
3. Generate multiple alternative explanations
4. Assess both statistical and practical significance
5. State conclusions with appropriate caveats
6. Identify valuable follow-up questions

Rigorous interpretation is the difference between data analysis and data-driven storytelling.
