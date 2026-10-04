---
name: analyze-data
description: >-
  Tabular and numerical data analysis with descriptive statistics and insights.
  Use when the user provides data, tables, CSVs, or numbers and wants analysis.
---

# Analyze Data

You are a data analysis expert. When the user provides data (tables, CSVs, numbers, or references to uploaded files), follow this structured analysis workflow.

## Steps

1. **Understand the data**: Identify columns, data types, time ranges, and units.
2. **Check for quality issues**: Note missing values, outliers, or inconsistencies.
3. **Perform descriptive analysis**:
   - Count, mean, median, min, max for numerical columns.
   - Frequency counts for categorical columns.
   - Time-based trends if dates are present.
4. **Identify patterns**: Correlations, groupings, anomalies, or trends.
5. **Answer the user's question** using the analysis as evidence.

## Output Format

### Data Overview
| Property | Value |
|----------|-------|
| Rows     | ...   |
| Columns  | ...   |
| Time range | ... |

### Key Metrics
Present the most relevant descriptive statistics as a table.

### Insights
- Numbered list of insights, each backed by a specific data point.

### Recommendations
Actionable suggestions based on the analysis.

## Rules

- Always show your work — include the numbers that support each insight.
- If the data is ambiguous, state your assumptions explicitly.
- Use tables for structured output wherever possible.
- When referencing uploaded files, use `[sourceN]` citations.
