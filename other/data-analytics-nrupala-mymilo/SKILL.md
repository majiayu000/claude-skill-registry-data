---
name: data-analytics
description: Turn data into decisions — question framing, exploratory analysis, statistical care, insights that change actions.
version: 1
triggers: data analysis, analyze data, exploratory analysis, statistics, insights
category: Thinking & decisions
blurb: Turn data into decisions — frame the question, analyze carefully, land insights that change actions.
archetype: knowledge
example: Analyze this dataset and tell me what actually matters.
---

# Data Analytics

Analysis that doesn't change a decision is decoration. Frame the question, respect the data, and land on an action someone owns.

## When to use
- Business/product/operations questions with data behind them.
- Ad-hoc deep dives; recurring reports (make them earn their cadence).
- Reviewing someone's analysis before it drives a decision.

## Method
1. **Frame the question**: decision first — who decides what, by when, and what data would change it? No decision → probably no analysis.
2. **Know the data**: provenance, coverage, definitions (a metric with two definitions is a bug), gaps and biases — before computing anything.
3. **Descriptive, honestly**: distributions before averages; segments before totals; trends on comparable windows (no cherry-picked baselines).
4. **Then diagnostic**: what moved the metric — decomposition, cohort views; correlation ≠ cause; triangulate mechanisms.
5. **Statistical care when inferring**: sample size/power, confidence, practical vs statistical significance, multiple-comparisons awareness.
6. **Insight → action**: so-what → recommendation with expected effect, owner, and measurement plan; state uncertainty plainly.
7. **Report like an engineer**: one page — question, data, method, finding, recommendation, caveats; charts per `data-visualization`; numbers reproducible.
8. **Close the loop**: after the action, predicted vs actual; update the model of the world.

## Quality gates
- [ ] Decision + owner named before analysis.
- [ ] Data provenance/definitions documented; segments + distributions shown.
- [ ] Inference claims carry uncertainty; multiple-comparison risk checked.
- [ ] Recommendation has owner + measurement plan; results reproducible.

## Red lines
- No analysis without a question; no causal claims from observational data alone; no charts that oversell.

## Related
`product-analytics` · `data-visualization` · `decision-making`.
