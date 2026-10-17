---
name: eda-report
description: >
  Run exploratory data analysis on a dataset and produce a structured report. Use when the user says
  "explore this dataset", "EDA on X", "analyze this data", "what's in this dataset", "summarize
  this data", "first look at the data", "understand this dataset before modeling", "data quality check",
  "describe this dataframe", or wants to understand a new dataset before building models or dashboards.
---

## Overview

Based on **"Practical Statistics for Data Scientists"** by Peter Bruce, Andrew Bruce, and Peter Gedeck. The core principle: before any modeling or analysis, you must understand the distribution, shape, and quality of your data. Skipping EDA leads to models trained on dirty data, misunderstood distributions, and insights that collapse under scrutiny. Structured EDA forces you to ask the right questions before committing to an approach.

## Workflow

### Step 1: Load and audit the dataset

Start with the basics - shape, types, and completeness.

```python
import pandas as pd

df = pd.read_csv("data.csv")

print(f"Shape: {df.shape}")
print(f"\nDtypes:\n{df.dtypes}")
print(f"\nMissing values:\n{df.isnull().sum()}")
print(f"\nDuplicate rows: {df.duplicated().sum()}")
```

Document:
- Row count and column count
- Percentage of missing values per column (flag any column > 5% missing)
- Columns with wrong inferred types (e.g., zip codes as integers)
- Duplicate row count

### Step 2: Profile each variable

Separate numeric from categorical. Apply the right summary stats to each.

**Numeric columns:**
```python
df.describe(percentiles=[0.01, 0.25, 0.5, 0.75, 0.99])
```
Check: mean vs median spread (skew signal), min/max for outlier flags, p1 and p99 for tail behavior.

**Categorical columns:**
```python
for col in df.select_dtypes("object").columns:
    print(f"{col}: {df[col].nunique()} unique | top: {df[col].value_counts().head(3).to_dict()}")
```
Check: cardinality (high cardinality = encoding decision needed), frequency of top values, presence of "unknown" / "other" / blank strings masking nulls.

### Step 3: Visualize distributions

One plot per numeric column. Do not skip this step - summary stats hide bimodal distributions, spikes at round numbers, and data entry artifacts.

```python
import matplotlib.pyplot as plt

df.hist(bins=30, figsize=(14, 10))
plt.tight_layout()
plt.savefig("distributions.png")
```

Flag columns that show:
- Heavy skew (log-transform candidate)
- Bimodal peaks (two subpopulations mixed)
- Spikes at 0, -1, or 999 (sentinel values)
- Values outside domain range (e.g., age = 200)

### Step 4: Analyze relationships and correlation

Check pairwise correlations among numeric features. Identify multicollinearity before modeling.

```python
import seaborn as sns

corr = df.select_dtypes("number").corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
plt.savefig("correlation_heatmap.png")
```

Flag:
- Any pair with |r| > 0.85 (multicollinearity risk)
- Target variable correlations (feature relevance signal)
- Surprising zero-correlations where you expected a relationship

### Step 5: Identify data quality issues and document decisions

Produce a written audit log. This is the deliverable, not just the charts.

For each issue found, record:
- Column name
- Issue type (missing, outlier, wrong type, duplicate, encoding ambiguity)
- Prevalence (count and % of rows affected)
- Recommended action (drop, impute, cap, flag, leave)

Example audit log format:
```
| Column       | Issue              | Rows Affected | Action          |
|--------------|-------------------|---------------|-----------------|
| income       | 3.2% missing       | 320 / 10,000  | Median impute   |
| zip_code     | Stored as float   | All           | Cast to string  |
| session_time | Max = 86,400 sec  | 12 rows       | Cap at 3,600    |
```

### Step 6: Write the EDA summary

Structured output for stakeholders or the next analyst.

**Sections to include:**
1. Dataset overview (rows, columns, time range if applicable)
2. Target variable distribution (if supervised task)
3. Key quality issues and planned treatments
4. Notable patterns (correlations, subpopulations, outliers)
5. Recommended next steps (feature engineering, additional data needed, modeling approach)

Keep the summary under 1 page. Charts go in the appendix.

## Anti-Patterns

**1. Skipping EDA and going straight to modeling**
Bad: Fitting a model on raw data, then debugging why predictions are wrong.
Good: Spending 20% of project time on EDA. Problems found here are 10x cheaper to fix than after a model is built.

**2. Reporting only means and standard deviations**
Bad: "Average age = 34.2, std = 12.1"
Good: Include percentiles and a histogram. A mean of 34 with a bimodal distribution at 18 and 55 tells a completely different story.

**3. Treating "unknown" strings as valid values**
Bad: Including "unknown", "N/A", "-", and "" as distinct categories.
Good: Standardize all null representations to NaN before profiling. Write a null-normalization function and run it first.

**4. EDA with no documented decisions**
Bad: Exploring data in a notebook but not recording what you found or what you plan to do about it.
Good: Every issue gets a row in the audit log with a decision. The audit log is a first-class deliverable.

## Quality Checklist

- [ ] Row count, column count, and missing value percentages documented
- [ ] Every numeric column has descriptive stats including p1, p25, p75, p99
- [ ] Every categorical column has cardinality and top-value frequency
- [ ] Distribution plots generated for all numeric columns
- [ ] Correlation heatmap produced and high-correlation pairs flagged
- [ ] Audit log written with issue, prevalence, and action for each finding
- [ ] EDA summary written with recommended next steps
