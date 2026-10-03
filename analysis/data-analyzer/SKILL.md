---
name: data-analyzer
description: Advanced data analysis, pattern detection, and insight generation from structured and unstructured datasets. Use when the user wants to analyze data, perform statistical analysis, find insights, detect patterns, identify anomalies, compare segments, test hypotheses, or generate data-driven recommendations. Triggers on phrases like 'analyze data', 'data analysis', 'find insights', 'analyze dataset', 'statistical analysis', 'find patterns', 'compare groups', 'test hypothesis', 'correlation analysis', or 'trend analysis'.
license: MIT
metadata:
  title: Data Analyzer
  category: market-competitive
  status: active
  origin: theseus
  invoke: agent
  runtime: tools
  supports_llm: true
  max_turns: 10
  output: "pursuits/{slug}/02_intel/data_analysis.md"
  upstream: govcon-capture-vibe/.github/skills/data-analyzer
---
# Data Analyzer

## Capture-insights adapter (no KG)

**Run** from Agent Skills or chat ("analyze this dataset", "find patterns", "trend analysis").

- **Deterministic EDA:** profiles CSV/JSON in pursuit Studio + `competitive_intel_obligation.json` when present.
- **Market slice:** DuckDB `usaspending_prime_awards` summary for active NAICS (top recipients/agencies).
- **Workflows:** EDA (default), trend, comparative, anomaly — inferred from inquiry phrasing.
- **Outputs:** `02_intel/data_analysis.json` + `.md`; optional LLM narrative when smart model on.
- **No invented stats** — every number traces to a file path or DuckDB query.


Expert data analysis agent that processes structured and unstructured datasets to extract
meaningful insights, identify patterns, detect anomalies, and generate data-driven
recommendations.

**This is a domain-agnostic platform primitive.** Let the data determine the analytical
approach — do not impose a domain lens. Govcon-specific variants (e.g., `workload-analyzer`)
build on this foundation via skill composition.

**References (load when needed):**

- `references/statistical-methods.md` — Descriptive + inferential statistics, effect size measures
- `references/visualization-guide.md` — Chart selection guide, design principles
- `references/pitfalls.md` — Common analytical pitfalls and how to avoid them
- `assets/report_template.md` — Report structure template for output

---

## Workflow 1: Exploratory Data Analysis (EDA)

**Objective:** Understand dataset structure, quality, and preliminary patterns.

1. **Data Profiling** — dimensions, column types, completeness, cardinality, ranges, summary statistics (mean, median, mode, std dev)
2. **Data Quality Assessment** — missing data patterns (MCAR/MAR/MNAR), duplicates, outliers, consistency issues; document each with severity rating
3. **Univariate Analysis** — distribution per variable, skewness/kurtosis, outlier detection (IQR, Z-score)
4. **Bivariate Analysis** — correlations (Pearson, Spearman), scatter plots for continuous pairs, cross-tabulations for categorical pairs
5. **Multivariate Analysis** — correlation matrices, dimensionality assessment, cluster tendency
6. **Initial Insights** — key patterns, surprising findings, hypotheses for further investigation, data limitations

> Load `references/statistical-methods.md` for formula reference and test selection guidance.

**Deliverable:** EDA report with summary statistics, visualizations, and preliminary insights.

---

## Workflow 2: Pattern Detection & Trend Analysis

**Objective:** Identify meaningful patterns, trends, and relationships.

1. **Time Series Analysis** (if temporal data) — trend direction, seasonality, cyclical patterns, anomaly detection, decompose into trend/seasonal/residual
2. **Segmentation Analysis** — natural groupings, segment profiling and characterization, cross-metric comparison
3. **Correlation & Causation** — correlation strength and significance, investigation of causal mechanisms, control for confounders; document the distinction explicitly
4. **Anomaly Detection** — statistical outliers, contextual anomalies, point vs. collective anomalies; determine whether each is an error or a finding
5. **Pattern Validation** — stability across subsets, sensitivity analysis, confidence intervals, significance testing

**Deliverable:** Pattern analysis report with validated findings.

---

## Workflow 3: Statistical Hypothesis Testing

**Objective:** Rigorously test hypotheses using appropriate statistical methods.

1. **Hypothesis Formulation** — define H0 and H1, specify significance level (α = 0.05 default), identify appropriate test
2. **Test Selection** — means: t-test/ANOVA; proportions: chi-square/Fisher's; correlation: Pearson/Spearman; distribution: K-S/Shapiro-Wilk; load `references/statistical-methods.md` for full decision tree
3. **Assumptions Checking** — normality, homogeneity of variance, independence, sample size adequacy; use non-parametric alternatives if assumptions are violated
4. **Test Execution** — compute test statistic, p-value, effect size (Cohen's d, η², R²), confidence intervals
5. **Result Interpretation** — distinguish statistical significance from practical significance; translate to plain-language implications

**Deliverable:** Statistical test report with methodology, results, and interpretation.

---

## Workflow 4: Comparative Analysis

**Objective:** Compare groups, segments, or time periods to identify differences and drivers.

1. **Define Comparison** — groups to compare, metrics, baseline vs. target, success criteria
2. **Segment Performance** — key metrics per segment, rank by performance, quantify gaps
3. **Driver Analysis** — factors explaining differences, quantified contribution per driver, confounding controls
4. **Benchmarking** — vs. historical performance, external standards, or best-in-class; calculate gaps to each benchmark
5. **Recommendations** — close performance gaps; distinguish quick wins from strategic initiatives; quantify expected impact

**Deliverable:** Comparative analysis report with driver identification and action plan.

---

## Workflow 5: Insight Synthesis & Storytelling

**Objective:** Transform analytical findings into clear, actionable insights.

1. **Insight Identification** — review all findings; identify the "so what"; prioritize by impact; group into themes
2. **Insight Structuring** — for each finding: Observation → Insight → Implication → Recommendation (answer first, then supporting detail)
3. **Evidence Assembly** — key statistics, supporting visualizations, benchmarks, confidence levels
4. **Narrative Development** — clear, jargon-free storyline with logical flow from problem to recommendation; anticipate counterarguments
5. **Visualization Design** — appropriate chart types, annotated key insights; load `references/visualization-guide.md` for chart selection
6. **Actionability** — specific actions, owners, timelines, success metrics, quantified expected impact

**Deliverable:** Executive-ready insight report. Use `assets/report_template.md` as the output structure.

---

## Quick Reference

| Action               | Trigger phrase                         |
| -------------------- | -------------------------------------- |
| Full EDA             | "Analyze this dataset comprehensively" |
| Quick summary        | "Summarize key statistics"             |
| Pattern detection    | "Find patterns in this dataset"        |
| Hypothesis test      | "Test if [A] affects [B]"              |
| Comparative analysis | "Compare [group A] vs [group B]"       |
| Correlation analysis | "What correlates with [variable]?"     |
| Anomaly detection    | "Find anomalies in this data"          |
| Trend analysis       | "Analyze trends over time"             |

---

## Best Practices

- **Start with questions** — define what you are trying to learn before examining the data
- **Document assumptions** — be explicit about data limitations and analytical choices
- **Visualize early and often** — charts reveal patterns that tables hide
- **Communicate uncertainty** — use confidence intervals, p-values, and error bars
- **Beware spurious correlations** — correlation is not causation; see `references/pitfalls.md`
- **Validate with domain knowledge** — ensure insights align with subject-matter expertise
- **Iterate** — analysis is rarely linear; loop back when findings raise new questions

## Pre-Delivery Checklist

- [ ] Data quality assessed and documented
- [ ] Appropriate statistical tests selected and executed
- [ ] Test assumptions verified
- [ ] Statistical vs. practical significance both addressed
- [ ] Visualizations are clear, accurate, and annotated
- [ ] Limitations and caveats explicitly stated
- [ ] Recommendations are specific and quantifiable
- [ ] Report structured using `assets/report_template.md`
