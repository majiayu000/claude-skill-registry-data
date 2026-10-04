---
name: eda
description: Exploratory data analysis
license: MIT
compatibility: opencode
metadata:
  audience: data-analysts
  category: data-science
---

## What I do

- Explore datasets to understand structure
- Identify patterns and relationships
- Detect anomalies and outliers
- Generate summary statistics
- Create visualizations for data understanding
- Form and test hypotheses
- Guide feature selection for modeling

## When to use me

Use me when:
- Starting a new data analysis project
- Understanding data before modeling
- Identifying data quality issues
- Discovering patterns in data
- Preparing for feature engineering

## Key Concepts

### EDA Process
1. **Data Collection**: Load and understand data
2. **Data Description**: Summary statistics
3. **Data Cleaning**: Handle missing, outliers
4. **Univariate Analysis**: Single variable patterns
5. **Bivariate Analysis**: Relationships between variables
6. **Multivariate Analysis**: Complex relationships

### Python EDA Example
```python
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("data.csv")

# Basic statistics
print(df.describe())
print(df.dtypes)
print(df.isnull().sum())

# Distribution analysis
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Histogram
sns.histplot(df["age"], kde=True, ax=axes[0, 0])

# Box plot for outliers
sns.boxplot(x="income", y="education", data=df, ax=axes[0, 1])

# Correlation heatmap
corr = df.select_dtypes(include=[np.number]).corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=axes[1, 0])

# Scatter with regression
sns.regplot(x="age", y="income", data=df, ax=axes[1, 1])

plt.tight_layout()
plt.show()

# Categorical analysis
print(df["category"].value_counts())
print(pd.crosstab(df["category"], df["outcome"]))
```

### Key Metrics
- **Central tendency**: Mean, median, mode
- **Spread**: Std dev, variance, IQR
- **Shape**: Skewness, kurtosis
- **Correlation**: Pearson, Spearman
