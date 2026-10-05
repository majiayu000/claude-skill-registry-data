---
name: data-analysis
description: Analyze, transform, clean, and visualize structured datasets using Python
  REPL, pandas, numpy, and plotting libraries. Trigger with "analyze data", "process
  CSV", "EDA", "generate plots", "statistical summary", or when computing numerical
  results.
argument-hint: <dataset path or analysis goal>
---

<!-- Generated from skills/data-analysis.md by tools/generate_integrations.py. Edit the source file, not this one. -->

# Skill: Data Analysis & Processing

## Purpose
Analyze, transform, and visualize data using computational tools. _Source: Colab (Category A)_

## Tools Required
- Python REPL / code execution _Source: OpenAI (Category C)_
- Data processing libraries (numpy, pandas, scipy) _Source: Colab (Category A)_
- Visualization libraries (matplotlib, plotly, seaborn) _Source: Colab (Category A)_
- File I/O for various formats (CSV, JSON, Excel, Parquet) _Source: Colab (Category A)_

## General Principles
- Use step-by-step computation — never rely on memorized results _Source: Lumo (Category B)_
- For arithmetic: calculate digit by digit before answering _Source: Kiro (Category O)_
- Verify results independently when possible _Source: Anthropic (Category J)_
- Prefer Python REPL over mental calculation for anything non-trivial _Source: OpenAI (Category C)_

## Computation Environment
When using Python for analysis: _Source: Colab (Category A)_
- Available libraries: numpy, scipy, pandas, seaborn, plotly, sympy, mpmath, statsmodels _Source: Colab (Category A)_
- Plotting: use plotly for interactive, matplotlib/seaborn for static _Source: Colab (Category A)_
- REPL is stateful — variables persist between calls _Source: Manus (Category F)_
- Timeout limits apply (typically 45-60s) — break long computations into chunks _Source: Manus (Category P)_

## Data Loading

### File Formats
| Format | Preferred Library | Notes |
|--------|-----------------|-------|
| CSV | pandas `read_csv` | Handle encoding, delimiter detection _Source: Colab (Category A)_ |
| JSON | `json` / pandas `read_json` | Nested structures need normalization _Source: Colab (Category A)_ |
| Excel | `openpyxl` / pandas `read_excel` | Multiple sheets, cell formatting _Source: Colab (Category A)_ |
| Parquet | pandas `read_parquet` | Columnar, efficient for large data _Source: Colab (Category A)_ |
| SQL | pandas `read_sql` | Database connection required _Source: Colab (Category A)_ |

### Data Cleaning
1. Check for nulls/missing values _Source: Colab (Category A)_
2. Validate data types _Source: Amp (Category E)_
3. Handle outliers (flag, don't silently remove) _Source: Amp (Category E)_
4. Normalize formats (dates, strings, numbers) _Source: Amp (Category E)_
5. Deduplicate if appropriate _Source: Amp (Category E)_

## Analysis Patterns

### Exploratory Data Analysis (EDA)
- Shape, dtypes, head/tail _Source: Colab (Category A)_
- Summary statistics (describe) _Source: Colab (Category A)_
- Distribution plots for numeric columns _Source: Colab (Category A)_
- Value counts for categorical columns _Source: Colab (Category A)_
- Correlation matrix for relationships _Source: Colab (Category A)_
- Missing value heatmap _Source: Colab (Category A)_

### Statistical Analysis
- Descriptive statistics: mean, median, std, quartiles _Source: Colab (Category A)_
- Hypothesis testing: t-test, chi-square, ANOVA _Source: Colab (Category A)_
- Regression: linear, logistic _Source: Colab (Category A)_
- Time series: trends, seasonality, decomposition _Source: Colab (Category A)_

### Data Transformation
- Filter rows, select columns _Source: Colab (Category A)_
- Group by + aggregate _Source: Colab (Category A)_
- Pivot / melt _Source: Colab (Category A)_
- Join / merge datasets _Source: Colab (Category A)_
- Apply custom functions _Source: Colab (Category A)_

## Visualization
- Line plots: time series, trends _Source: Colab (Category A)_
- Bar plots: categorical comparisons _Source: Colab (Category A)_
- Scatter plots: relationships between variables _Source: Colab (Category A)_
- Histograms: distributions _Source: Colab (Category A)_
- Heatmaps: correlation, matrices _Source: Colab (Category A)_
- Box plots: distribution comparison _Source: Colab (Category A)_

## Results Communication
- Present key findings prominently _Source: Lumo (Category B)_
- Support with visualizations when helpful _Source: Gemini (Category B)_
- Include uncertainty/confidence where relevant _Source: Anthropic (Category J)_
- Don't over-interpret — let the data speak _Source: Lumo (Category B)_
- Flag data quality issues that affect conclusions _Source: Anthropic (Category J)_

## Reproducibility
- Log transformation steps _Source: Factory (Category O)_
- Document assumptions _Source: Factory (Category O)_
- Note any data filtering/exclusion decisions _Source: Factory (Category O)_
- Random seeds for reproducible sampling _Source: Factory (Category O)_
- Version data processing scripts _Source: Factory (Category O)_
