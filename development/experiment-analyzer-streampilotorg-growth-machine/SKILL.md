---
name: experiment-analyzer
description: Analyze completed growth experiment results, validate hypotheses, generate insights, and suggest follow-up experiments. Use when experiments are completed, when the user asks about results or learnings, or when discussing what to do next based on experiment outcomes.
allowed-tools: [Read, Write, Grep, Glob]
---

# Experiment Analyzer Skill

Analyze completed growth experiments, extract insights, and drive continuous learning.

## When to Activate

This skill should activate when:
- User marks experiment as "completed"
- User asks "what did we learn?"
- User mentions "results", "outcomes", or "analysis"
- User asks "what should we do next?"
- User wants to compare multiple experiments
- User asks about experiment success rates

## Analysis Framework

### 1. Result Classification

**Win (Positive + Significant)**
- Result is better than baseline
- Statistical significance ≥ 95%
- Change is meaningful (usually ≥5%)

**Loss (Negative + Significant)**
- Result is worse than baseline
- Statistical significance ≥ 95%
- Change is meaningful

**Inconclusive**
- Statistical significance < 95%
- Not enough data to make decision
- Sample size may be insufficient

**Neutral**
- Minimal change (< ±2%)
- No meaningful impact either way
- May indicate hypothesis was off

### 2. Hypothesis Validation

Compare original hypothesis to results:

**Hypothesis Components:**
- Proposed change → Was it implemented as planned?
- Target audience → Did we reach the right users?
- Expected outcome → Did we hit the target?
- Rationale → Was our reasoning correct?

**Validation Questions:**
- Did we achieve the expected outcome? (Yes/No/Partially)
- Was the underlying assumption correct?
- What surprised us?
- What would we do differently?

### 3. ICE Score Retrospective

Compare predicted vs actual:

**Impact Score Validation:**
- Predicted Impact: [original score]
- Actual Impact: [calculate based on results]
- Delta: [difference]
- Learning: Was our impact prediction accurate?

**Confidence Score Validation:**
- Predicted Confidence: [original score]
- Outcome: [win/loss/inconclusive]
- Learning: Was our confidence justified?

**Ease Score Validation:**
- Predicted Ease: [original score]
- Actual Time: [if tracked]
- Learning: Was implementation as easy as expected?

### 4. Insight Generation

**Key Questions:**
- **What worked?** Specific elements that drove success
- **What didn't work?** Elements that failed or harmed metrics
- **What was surprising?** Unexpected findings
- **What patterns emerge?** Connections to other experiments
- **What new questions arise?** Areas to investigate further

**Secondary Metrics:**
- Review all secondary metrics tracked
- Look for unintended positive effects
- Watch for negative side effects
- Consider holistic impact

### 5. Follow-up Experiment Suggestions

Based on the outcome, suggest 2-3 follow-up experiments:

**For Wins:**
- **Scale:** Roll out to 100% of users
- **Amplify:** Make the winning element more prominent
- **Extend:** Apply pattern to related areas
- **Optimize:** Test variations to improve further

**For Losses:**
- **Pivot:** Try alternative approach to same problem
- **Investigate:** Run research to understand why
- **Revert:** Document and move on
- **Learn:** Apply learnings to future experiments

**For Inconclusive:**
- **Re-run:** Increase sample size or duration
- **Simplify:** Test smaller version to isolate variable
- **Segment:** Test with specific user segments
- **Refine:** Adjust hypothesis based on early signals

## Analysis Process

### Step 1: Load and Validate

```
1. Read experiment JSON from completed/archived folder
2. Verify results data exists:
   - Primary metric
   - Baseline value
   - Result value
   - Statistical significance
   - Sample size
   - Duration
3. Check if hypothesis is documented
4. Review ICE scores
```

### Step 2: Calculate Key Metrics

```
Change Percentage = ((Result - Baseline) / Baseline) × 100

Result Classification:
- IF change% > 2% AND significance >= 95% → Win
- IF change% < -2% AND significance >= 95% → Loss
- IF significance < 95% → Inconclusive
- IF abs(change%) < 2% → Neutral
```

### Step 3: Generate Insights

```
1. Classify result (Win/Loss/Inconclusive/Neutral)
2. Validate hypothesis against results
3. Review ICE score predictions
4. Extract key learnings
5. Identify surprising findings
6. Check secondary metrics
7. Look for patterns across related experiments
```

### Step 4: Create Follow-up Ideas

```
1. Based on result type, brainstorm 2-3 follow-ups
2. For each follow-up:
   - Draft hypothesis
   - Explain rationale (reference current learnings)
   - Suggest category
   - Provide preliminary ICE estimate
3. Prioritize follow-ups by potential impact
```

### Step 5: Generate Report

```
1. Create markdown analysis report
2. Include:
   - Summary (result classification, key numbers)
   - Hypothesis validation
   - ICE score retrospective
   - Key insights (bulleted list)
   - Secondary metrics review
   - Recommendations
   - Follow-up experiment ideas
3. Save to experiments/archive/[id]_analysis.md
4. Update experiment JSON with learnings
```

## Analysis Output Template

```markdown
# Experiment Analysis: [Title]

**Date:** [Analysis date]
**Experiment ID:** [id]
**Status:** [Win/Loss/Inconclusive/Neutral] ✓/✗/?/○

## Summary

- **Primary Metric:** [metric name]
- **Baseline:** [baseline value]
- **Result:** [result value]
- **Change:** [+/-X%]
- **Statistical Significance:** [XX%]
- **Sample Size:** [count]
- **Duration:** [days]

## Hypothesis Validation

### Original Hypothesis
[Full hypothesis statement]

### Validation
- **Expected Outcome:** [what we expected]
- **Actual Outcome:** [what happened]
- **Hypothesis Validated:** [Yes/No/Partially]

**Analysis:**
[Explanation of whether and why hypothesis was validated]

## ICE Score Retrospective

| Component | Predicted | Actual/Assessment | Accuracy |
|-----------|-----------|------------------|----------|
| Impact | [score] | [calculate from results] | [good/overestimated/underestimated] |
| Confidence | [score] | [based on outcome] | [justified/overconfident/underconfident] |
| Ease | [score] | [based on actual effort] | [accurate/harder/easier] |

**Learnings for Future Scoring:**
- [What we learned about predicting impact]
- [What we learned about confidence]
- [What we learned about ease]

## Key Insights

1. **[Primary insight]** - [Explanation with data]
2. **[Secondary insight]** - [Explanation]
3. **[Surprising finding]** - [What we didn't expect]

## Secondary Metrics

| Metric | Change | Interpretation |
|--------|--------|----------------|
| [metric 1] | [+/-X%] | [Good/Bad/Neutral] |
| [metric 2] | [+/-X%] | [Good/Bad/Neutral] |

**Side Effects:**
- Positive: [Any unexpected positive impacts]
- Negative: [Any unexpected negative impacts]

## Recommendations

### Immediate Actions
- [ ] [Action item 1]
- [ ] [Action item 2]

### Strategic Implications
[Broader implications for product/growth strategy]

## Follow-up Experiment Ideas

### 1. [Experiment Title]
**Category:** [category]

**Hypothesis:**
[Full hypothesis following template]

**Rationale:**
[Why this follow-up based on current learnings]

**Preliminary ICE:**
- Impact: [score] - [reasoning]
- Confidence: [score] - [reasoning]
- Ease: [score] - [reasoning]
- **Total: [score]**

---

### 2. [Experiment Title]
[Repeat format]

---

### 3. [Experiment Title]
[Repeat format]

## Related Experiments

[List any related experiments and their outcomes for pattern recognition]

## Notes

[Any additional context, edge cases, or considerations]
```

## Cross-Experiment Analysis

When user asks to analyze multiple experiments:

### Metrics to Calculate:
- **Success Rate:** % of wins out of completed experiments
- **Category Performance:** Which funnel stages have best win rate?
- **ICE Score Accuracy:** How well do high-ICE experiments perform?
- **Average Impact:** What's the typical metric improvement?
- **Cycle Time:** Average days from backlog → completed

### Pattern Recognition:
- Which types of experiments succeed most?
- Which audience segments respond best?
- Which testing methods are most reliable?
- What confidence levels actually predict success?

### Portfolio View:
```markdown
# Experiment Portfolio Analysis

## Overview
- Total Experiments: [count]
- Completed: [count]
- Win Rate: [X%]
- Average Change: [+X%]

## By Category
| Category | Experiments | Win Rate | Avg Impact |
|----------|-------------|----------|------------|
| Acquisition | [count] | [X%] | [+X%] |
| Activation | [count] | [X%] | [+X%] |
| Retention | [count] | [X%] | [+X%] |
| Revenue | [count] | [X%] | [+X%] |
| Referral | [count] | [X%] | [+X%] |

## ICE Score Performance
- Experiments with ICE > 500: [X% win rate]
- Experiments with ICE 300-500: [X% win rate]
- Experiments with ICE < 300: [X% win rate]

**Learning:** [Are high ICE scores actually better predictors?]

## Top Performers
1. [Experiment] - [+X%] change
2. [Experiment] - [+X%] change
3. [Experiment] - [+X%] change

## Key Patterns
- [Pattern 1 discovered across experiments]
- [Pattern 2]
- [Pattern 3]

## Recommendations
[Strategic recommendations based on portfolio analysis]
```

## Integration Points

- Automatically trigger when `/experiment-update` sets status to "completed"
- Work with ICE scorer skill to validate predictions
- Inform hypothesis generator with learnings
- Feed into metrics calculator for portfolio analysis

## Continuous Improvement

After each analysis:
- Store learnings in a knowledge base
- Update ICE scoring calibration
- Refine hypothesis templates
- Build pattern library
- Improve follow-up suggestions
