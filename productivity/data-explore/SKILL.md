---
name: data-explore
description: Profile and explore datasets -- schema inference, distributions, missing values, outliers, correlations. Use when starting work with a new dataset or investigating data quality issues.
---

# Data Exploration Skill

When exploring a dataset, follow this structured approach. Adapt based on whether the data is tabular (CSV/DataFrame), image-based, or text.

## 1. Schema and Structure

First, understand what you're working with:

- Load a sample (first 5 rows + last 5 rows)
- Column names, dtypes, and count of non-null values
- Dataset dimensions (rows x columns)
- Memory usage
- Identify the target variable if this is a supervised learning task

For tabular data:
```python
df.info()
df.describe(include='all')
df.head()
df.dtypes.value_counts()
```

## 2. Missing Values

Map the missing data landscape:

- Count and percentage of missing values per column
- Pattern analysis: are values Missing Completely At Random (MCAR), Missing At Random (MAR), or Missing Not At Random (MNAR)?
- Identify columns with >50% missing (candidates for dropping)
- Check if missingness correlates with the target variable

```python
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_report = pd.DataFrame({'count': missing, 'pct': missing_pct})
missing_report[missing_report['count'] > 0].sort_values('pct', ascending=False)
```

## 3. Distribution Analysis

For each feature, characterize its distribution:

**Numerical features:**
- Min, max, mean, median, std
- Skewness and kurtosis
- Identify if log-transform would help (right-skewed data)

**Categorical features:**
- Cardinality (number of unique values)
- Value counts for top-10 categories
- Identify rare categories (<1% frequency)

## 4. Outlier Detection

Flag potential outliers:

- IQR method: values below Q1 - 1.5*IQR or above Q3 + 1.5*IQR
- Z-score method: values with |z| > 3
- Domain-specific checks (e.g., negative ages, future dates)

```python
Q1 = df[col].quantile(0.25)
Q3 = df[col].quantile(0.75)
IQR = Q3 - Q1
outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]
```

## 5. Correlations and Relationships

Identify feature relationships:

- Pearson correlation matrix for numerical features
- Flag highly correlated pairs (|r| > 0.8) as candidates for feature selection
- Check correlation with target variable
- For categorical features, use chi-squared test or Cramer's V

## 6. Data Quality Score

Summarize findings with a quality assessment:

- Completeness: % of non-null values across all cells
- Uniqueness: % of columns with no duplicates (where expected)
- Consistency: any type mismatches or encoding issues
- Validity: % of values within expected ranges

Present the final summary as a structured report.
