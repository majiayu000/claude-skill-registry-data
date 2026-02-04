---
name: comparative-analysis
description: Systematic comparison of segments, cohorts, or time periods - ensure fair apples-to-apples comparisons, identify meaningful differences, explain WHY differences exist
---

# Comparative Analysis Process

## Overview

This skill guides you through systematic comparison of two or more groups, segments, cohorts, or time periods. Unlike exploratory-analysis (where you discover patterns) or guided-investigation (where you answer broad questions), comparative analysis helps you **rigorously compare** specific groups and **explain** why they differ.

Comparative analysis is appropriate when:
- You need to compare performance between specific segments (regions, products, customer cohorts)
- You want to understand how groups differ across multiple dimensions
- You're evaluating changes before/after an intervention or between time periods
- The user asks "How does X compare to Y?" or "What's different about segment A vs B?"
- You need to make fair, apples-to-apples comparisons with controls for confounding factors

## Prerequisites

Before using this skill, you MUST:
1. Have data imported into SQLite database using the `importing-data` skill
2. Have data quality validated and cleaned using the `cleaning-data` skill (MANDATORY - never skip)
3. Have created an analysis workspace (`just start-analysis comparative-analysis <name>`)
4. Have clearly defined what you're comparing (user must specify comparison groups)
5. Be familiar with the component skills:
   - `understanding-data` - for data profiling
   - `writing-queries` - for SQL query construction
   - `interpreting-results` - for result analysis
   - `creating-visualizations` - for text-based visualizations

## Mandatory Process Structure

You MUST use TodoWrite to track progress through all 5 phases. Create todos at the start:

```markdown
- Phase 1: Define Comparison - pending
- Phase 2: Segment Definition - pending
- Phase 3: Metric Comparison - pending
- Phase 4: Difference Explanation - pending
- Phase 5: Conclusions and Recommendations - pending
```

Update status as you progress. Mark phases complete ONLY after checkpoint verification.

---

## Phase 1: Define Comparison

**CHECKPOINT:** Before proceeding, you MUST have:
- [ ] Clarified what groups/segments/periods are being compared
- [ ] Identified the comparison objective (what question does this answer?)
- [ ] Determined comparison type (segments, cohorts, time periods, before/after)
- [ ] Established what metrics will be compared
- [ ] Documented the comparison framework
- [ ] Saved to `01 - comparison-definition.md`

### Instructions

1. **Clarify the comparison goal with the user**

Ask clarifying questions:
- What specific groups/segments do you want to compare?
- What's the purpose of this comparison? What decision will it inform?
- What differences would be meaningful or actionable?
- Are there specific metrics you care about most?
- What time period should the comparison cover?

2. **Define the comparison framework**

Create `analysis/[session-name]/01-comparison-definition.md` with: ./templates/phase-1.md

3. **Get user confirmation before proceeding**
   - Review comparison definition with user
   - Confirm groups are defined correctly
   - Verify metrics align with user's goals
   - Adjust framework if needed

**Common Rationalization:** "The comparison is obvious, I'll just start querying"
**Reality:** Without explicit definition, you'll make unstated assumptions about what "fair" means.

**Common Rationalization:** "I'll compare everything and see what's different"
**Reality:** Unfocused comparison produces noise. Define specific metrics and materiality thresholds.

---

## Phase 2: Segment Definition

**CHECKPOINT:** Before proceeding, you MUST have:
- [ ] Verified that comparison groups exist in the data
- [ ] Validated group definitions with actual queries
- [ ] Checked for data quality issues within each group
- [ ] Documented group characteristics and sample sizes
- [ ] Confirmed groups are comparable (similar data quality, coverage)
- [ ] Saved to `02 - segment-definition.md`

### Instructions

1. **Validate that groups exist and are well-defined**

Create `analysis/[session-name]/02-segment-definition.md` with: ./templates/phase-2.md

2. **Handle segment definition issues**

If groups are not comparable:
- **Sample size too small:** Consider combining groups, expanding time window, or adjusting comparison
- **Different time periods:** Either align periods or explicitly control for temporal effects
- **Data quality differs:** Document the difference and consider if it invalidates comparison
- **Overlapping groups:** Redefine to ensure groups are mutually exclusive

3. **Document any exclusions or adjustments**

If you exclude outliers, filter dates, or adjust definitions, document clearly:
```markdown
## Adjustments Made for Fair Comparison

1. **Outlier handling:** Excluded 8 transactions >$50,000 as data entry errors (confirmed with field validation)
2. **Date alignment:** Limited both groups to Feb 1 - Apr 30 to match shorter group's coverage
3. **Null handling:** Excluded 127 transactions with NULL customer_id from both groups
```

**Common Rationalization:** "The groups look fine, I'll skip validation"
**Reality:** Unstated data quality issues or sample size problems will invalidate your comparison.

**Common Rationalization:** "Sample sizes are different but that's okay"
**Reality:** Large sample size differences require per-capita normalization. Raw totals are misleading.

---

## Phase 3: Metric Comparison

**CHECKPOINT:** Before proceeding, you MUST have:
- [ ] Calculated all primary metrics for each group
- [ ] Calculated all secondary metrics for each group
- [ ] Computed differences (absolute and percentage) between groups
- [ ] Created comparison visualizations (tables, charts)
- [ ] Identified which metrics differ meaningfully (per materiality threshold)
- [ ] Documented all comparisons with queries and results
- [ ] Saved to `03 - metric-comparison.md`

### Instructions

1. **Compare groups systematically across all metrics**

Create `analysis/[session-name]/03-metric-comparison.md` with: ./templates/phase-3.md

2. **Be rigorous about normalization**

Compare apples-to-apples:
- Use per-customer or per-day metrics, not raw totals (unless groups are identical size)
- Calculate percentages within group (e.g., % of group's revenue by category)
- Use rate metrics (transactions per customer, revenue per transaction)

Wrong: "Northeast has $458K revenue vs Southeast's $392K"
Right: "Northeast has $161/customer vs Southeast's $150/customer (7.5% higher)"

3. **Compute statistical and practical significance**

**Statistical significance:** Is difference larger than random variation would explain?
- With large samples (>1000), small differences can be statistically significant
- Document sample sizes to provide context

**Practical significance:** Is difference large enough to matter for decisions?
- Use materiality threshold from Phase 1
- 5% difference in revenue might be huge for a billion-dollar company, trivial for a startup

4. **Use visualization to make differences clear**

- Side-by-side tables with difference columns
- ASCII bar charts showing relative magnitudes
- Percentage difference callouts

**Common Rationalization:** "I'll just show the raw numbers and let the user interpret"
**Reality:** Your job is interpretation. Show differences clearly and explain what they mean.

**Common Rationalization:** "Northeast has more revenue, that's the answer"
**Reality:** Explain WHY - more customers? Higher spend per customer? Different product mix? Dig deeper.

**Common Rationalization:** "These differences are statistically significant, so they matter"
**Reality:** Statistical significance ≠ practical significance. A 1% difference might be "significant" but not meaningful.

---

## Phase 4: Difference Explanation

**CHECKPOINT:** Before proceeding, you MUST have:
- [ ] Identified the 2-3 most important differences from Phase 3
- [ ] For each difference, investigated potential causes
- [ ] Analyzed confounding factors
- [ ] Ruled out alternative explanations where possible
- [ ] Quantified relative contribution of different factors
- [ ] Documented explanation analysis with supporting queries
- [ ] Saved to `04 - difference-explanation.md`

### Instructions

1. **Focus on the most meaningful differences**

Don't try to explain every small difference. Focus on:
- Differences that exceed materiality threshold
- Differences that are surprising or counter-intuitive
- Differences that inform the comparison objective

2. **Investigate WHY differences exist**

Create `analysis/[session-name]/04-difference-explanation.md` with: ./templates/phase-4.md

3. **Be intellectually honest about causation**

Comparative analysis shows WHAT differs, not always WHY:
- With observational data, you usually can't prove causation
- Multiple explanations may fit the data
- Acknowledge uncertainty and alternative explanations

4. **Decompose complex differences**

When metrics differ, break them into components:
- Revenue = Customers × Revenue per Customer
- Revenue per Customer = Transactions per Customer × Revenue per Transaction
- Identify which component drives the overall difference

**Common Rationalization:** "I found the difference, that's enough"
**Reality:** Finding the difference is half the job. Explaining WHY is equally important.

**Common Rationalization:** "This factor correlates with the difference, so it's the cause"
**Reality:** Correlation ≠ causation. Multiple factors may correlate. Be cautious about causal claims.

**Common Rationalization:** "I'll ignore confounds since I can't measure them"
**Reality:** Acknowledge unmeasured confounds explicitly. They limit your conclusions but shouldn't be ignored.

---

## Phase 5: Conclusions and Recommendations

**CHECKPOINT:** Before proceeding, you MUST have:
- [ ] Summarized key differences and their magnitudes
- [ ] Explained most likely drivers of differences
- [ ] Assessed confidence in findings
- [ ] Identified actionable insights
- [ ] Made specific recommendations based on comparison
- [ ] Documented limitations and caveats
- [ ] Saved to `05 - conclusions-and-recommendations.md`
- [ ] Updated `00 - overview.md` with comparison summary

### Instructions

1. **Synthesize findings into clear conclusions**

Create `analysis/[session-name]/05-conclusions-and-recommendations.md` with: ./templates/phase-5.md

2. **Update overview document**

Update: `00 - overview.md`

Add at the end:

```markdown
## Comparison Summary

**Groups Compared:** [Groups]

**Time Period:** [Date range]

**Comparison Completed:** [Date]

---

## Key Differences Identified

1. **[Difference 1]:** [Brief description with magnitude]
   - Driver: [Primary explanation]
   - Confidence: [High/Medium/Low]

2. **[Difference 2]:** [Brief description with magnitude]
   - Driver: [Primary explanation]
   - Confidence: [High/Medium/Low]

3. **[Difference 3]:** [Brief description with magnitude]
   - Driver: [Primary explanation]
   - Confidence: [High/Medium/Low]

---

## Top Recommendations

1. **[Recommendation 1]:** [One sentence]
   - Expected impact: [Magnitude]

2. **[Recommendation 2]:** [One sentence]
   - Expected impact: [Magnitude]

---

## File Index

- 01 - Comparison Definition
- 02 - Segment Definition
- 03 - Metric Comparison
- 04 - Difference Explanation
- 05 - Conclusions and Recommendations
```

3. **Communicate findings to user**

Present conclusions clearly:
- Lead with directional summary (which group "wins" and why)
- Quantify key differences with specific numbers
- Explain drivers of differences
- Acknowledge uncertainty and limitations
- Provide actionable recommendations
- Suggest follow-up questions

**Common Rationalization:** "I'll just present all the numbers and let the user draw conclusions"
**Reality:** Your job is to interpret and synthesize. Provide clear conclusions, not just data dumps.

**Common Rationalization:** "I'm 100% confident in these conclusions"
**Reality:** Be honest about confidence levels and limitations. Overconfidence undermines credibility.

**Common Rationalization:** "Comparison complete, no follow-up needed"
**Reality:** Comparisons often raise more questions than they answer. Identify high-value follow-up investigations.

---

## Common Rationalizations

### "The groups are obviously different, I'll skip formal definition"
**Why this is wrong:** "Obvious" differences often have unstated assumptions. Explicit definition prevents misunderstandings and ensures you're answering the right question.

**Do instead:** Complete Phase 1 fully. Define groups, metrics, and materiality thresholds explicitly.

### "Sample sizes look fine, I'll skip validation"
**Why this is wrong:** Sample size is only one aspect. Data quality, temporal alignment, and outliers can invalidate comparisons even with large samples.

**Do instead:** Validate groups thoroughly in Phase 2. Check quality, coverage, and comparability.

### "I'll just compare raw totals"
**Why this is wrong:** Raw totals are misleading when groups have different sizes. $500K vs $400K tells you nothing if one group is 2x the size of the other.

**Do instead:** Normalize by customers, days, or transactions. Compare per-capita or rate metrics.

### "Northeast has higher revenue, that's the finding"
**Why this is wrong:** Stating WHAT differs without explaining WHY provides limited value. The explanation is where actionable insights live.

**Do instead:** Decompose differences. Explain whether higher revenue comes from more customers, higher per-customer value, different mix, etc.

### "These groups are different, so one must be better"
**Why this is wrong:** Different doesn't mean better. Context matters. Lower-revenue group might serve a different market, have different goals, or optimize for different metrics.

**Do instead:** Interpret differences in context. Consider whether "better" is even the right framing.

### "I found a correlation, so that's the cause"
**Why this is wrong:** Correlation ≠ causation. Many factors correlate with outcomes without causing them.

**Do instead:** Be cautious with causal language. Say "associated with" or "correlated with" rather than "caused by" unless you have experimental evidence.

### "I'll ignore the confounds I can't measure"
**Why this is wrong:** Unmeasured confounds don't disappear by ignoring them. They limit what you can conclude.

**Do instead:** Explicitly acknowledge unmeasured confounds in Phase 4. Explain how they limit causal interpretation.

### "I'll recommend that Southeast copy Northeast exactly"
**Why this is wrong:** You don't know if differences are due to replicable practices or immutable characteristics (market size, demographics, etc.).

**Do instead:** Recommend further investigation to understand whether differences are actionable or structural.

### "This comparison answered the question completely"
**Why this is wrong:** Comparisons typically reveal new questions about root causes, generalizability, and interventions.

**Do instead:** Identify high-value follow-up questions in Phase 5. Guide next investigations.

### "Statistical significance means it matters"
**Why this is wrong:** With large samples, tiny differences can be statistically significant but practically meaningless.

**Do instead:** Focus on practical significance (materiality threshold). A 1% difference might be "significant" but not meaningful.

---

## Summary

This skill ensures rigorous, fair comparisons by:

1. **Defining comparisons explicitly:** Clear groups, metrics, and materiality thresholds prevent unstated assumptions
2. **Validating segment quality:** Ensuring groups are comparable prevents invalid comparisons
3. **Comparing systematically:** Multi-metric analysis reveals patterns that single metrics miss
4. **Explaining differences:** Understanding WHY groups differ is as important as knowing WHAT differs
5. **Acknowledging limitations:** Honest assessment of confounds and causation builds credibility
6. **Providing actionable insights:** Converting findings into recommendations and follow-up questions

Follow this process and you'll deliver fair, rigorous comparisons that explain not just WHAT differs but WHY, identify actionable opportunities, and guide follow-up investigations.
