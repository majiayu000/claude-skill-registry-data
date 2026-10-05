---




name: ds-eda
compatibility: opencode
completeness: 95
content-types:
- code
- guidance
- do-dont
- examples
description: '"Provides Performs exploratory data analysis using summary statistics
  distributions, correlations, and descriptive methods to understand dataset characteristic"'
license: MIT
maturity: stable
metadata:
  domain: coding
  output-format: code
  related-skills: ds-correlation-analysis, ds-data-profiling, ds-data-visualization
    ds-dimensionality-reduction ds-missing-data
  role: implementation
  scope: implementation
  triggers: exploratory data analysis, EDA, summary statistics, distributions, data
    exploration, how do i explore data
  archetypes:
  - tactical
  - generation
  anti_triggers:
  - brainstorming
  - vague ideation
  - code golf
  - over-engineering
  response_profile:
    verbosity: low
    directive_strength: high
    abstraction_level: operational
version: "1.0.0"




---




# Exploratory Data Analysis

Comprehensive guide to exploratory data analysis in machine learning and data science workflows.

## When to Use This Skill

- Solving real-world exploratory data analysis problems
- Building machine learning pipelines with exploratory data analysis
- Implementing best practices for exploratory data analysis
- Optimizing model performance using exploratory data analysis techniques
- Learning industry-standard approaches to exploratory data analysis

## When NOT to Use This Skill

- When using pre-built libraries without understanding underlying concepts
- For toy problems that don't require exploratory data analysis rigor
- When domain expertise in specific problem requires different approach
- If your problem doesn't require the complexity this skill provides

## Purpose and Key Concepts

Exploratory Data Analysis is a critical component of the machine learning workflow. This skill covers:

1. **Theoretical foundations** — Mathematical principles and statistical concepts
2. **Practical implementation** — Working code examples and patterns
3. **Common pitfalls** — Mistakes to avoid and how to recover from them
4. **Best practices** — Industry-standard approaches and optimization techniques

## Core Workflow

1. **Understand the problem** — Clearly define what you're solving for
2. **Select approach** — Choose the right technique for your data and constraints
3. **Implement solution** — Write clean, tested code following best practices
4. **Validate results** — Verify your implementation with tests and validation
5. **Optimize performance** — Improve efficiency and accuracy incrementally

## Implementation Patterns

### Pattern 1: Basic Exploratory Data Analysis

```python
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

def perform_basic_eda(df: pd.DataFrame) -> dict:
    """Perform basic exploratory data analysis on a DataFrame."""
    if df.empty:
        raise ValueError("DataFrame cannot be empty")
    
    # Summary statistics
    summary = df.describe().to_dict()
    
    # Correlation matrix for numeric columns
    numeric_cols = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_cols.corr().to_dict() if not numeric_cols.empty else {}
    
    # Missing values count
    missing = df.isnull().sum().to_dict()
    
    # Distribution skewness for numeric columns
    skewness = {col: float(stats.skew(df[col].dropna())) for col in numeric_cols.columns}
    
    return {
        'summary': summary
        'correlations': corr_matrix
        'missing_values': missing
        'skewness': skewness
    }

# BAD vs GOOD Example
# BAD: Ignoring data types and missing values
# bad_results = df.describe().to_dict()
# GOOD: Explicit type filtering, missing value tracking, and statistical validation
# good_results = perform_basic_eda(df)
```

### Pattern 2: Production-Ready Exploratory Data Analysis

```python
import logging
import pandas as pd
import numpy as np
from typing import Any, Dict, List
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)

class ExploratoryDataAnalysis:
    """Production implementation of Exploratory Data Analysis"""
    
    def __init__(self, log_level: int = logging.INFO):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        self.scaler = StandardScaler()
        
    def execute(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Execute Exploratory Data Analysis on data"""
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame")
        if data.empty:
            raise ValueError("Input DataFrame is empty")
            
        results = {
            'shape': data.shape
            'dtypes': data.dtypes.astype(str).to_dict()
            'missing_counts': data.isnull().sum().to_dict()
            'missing_pct': (data.isnull().sum() / len(data) * 100).to_dict()
            'numeric_summary': data.describe().to_dict()
            'categorical_counts': {}
        }
        
        for col in data.select_dtypes(include=['object', 'category']).columns:
            results['categorical_counts'][col] = data[col].value_counts().to_dict()
            
        numeric_data = data.select_dtypes(include=[np.number])
        if not numeric_data.empty:
            results['correlation_matrix'] = numeric_data.corr().to_dict()
            
        self.logger.info(f"EDA completed on {data.shape[0]} rows and {data.shape[1]} columns")
        return results
```

## Best Practices

- ✅ Always validate your implementation on test data
- ✅ Document your assumptions and methodology
- ✅ Use version control for reproducibility
- ✅ Monitor performance metrics in production
- ✅ Periodically review and update your approach
- ✅ Test with edge cases and outliers
- ✅ Log all significant operations for debugging

## Common Pitfalls

| Pitfall | Problem | Solution |
|

---

---

## Constraints

### MUST DO
- Validate all data preprocessing steps are fit-only on training data, never on validation or test sets
- Implement reproducible pipelines with fixed random seeds and deterministic operations where possible
- Report model performance with confidence intervals via bootstrapping or cross-validation across multiple runs
- Log all experiments with parameters, metrics, and artifacts using MLflow or equivalent tracking system

### MUST NOT DO
- Do not evaluate a model on the same data used for training — always hold out a proper test set
- Avoid overfitting to the validation set by limiting hyperparameter search iterations
- Never use features that can only be computed at inference time (look-ahead bias)
- Do not report single-run accuracy without statistical significance testing or error bars


## Live References

> Authoritative documentation links for this skill's domain. The model follows markdown links at load time to resolve external references and inline content.

- [Exploratory Data Analysis — Wikipedia](https://en.wikipedia.org/wiki/Exploratory_data_analysis)
- [EDA in Python (Towards Data Science)](https://towardsdatascience.com/exploratory-data-analysis-in-python/)
- [Pandas Profiling / ydata-profiling](https://docs.profiling.ydata.ai/latest/)
- [Seaborn EDA Examples](https://seaborn.pydata.org/examples/index.html)
- [Kaggle EDA Tutorial](https://www.kaggle.com/learn/data-visualization)