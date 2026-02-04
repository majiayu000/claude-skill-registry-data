---
name: sweetviz
version: 1.0.0
description: Automated EDA comparison reports with target analysis, feature comparison, and HTML report generation for pandas DataFrames
author: workspace-hub
category: data-analysis
type: skill
capabilities:
  - One-line automated EDA reports
  - Target variable analysis
  - Feature comparison between datasets
  - Train vs test data comparison
  - Intra-set comparisons (subpopulations)
  - HTML report generation
  - Correlation analysis
  - Missing value visualization
  - Distribution analysis
  - Categorical and numerical analysis
tools:
  - sweetviz
  - pandas
  - numpy
  - matplotlib
tags: [sweetviz, eda, data-analysis, comparison, target-analysis, html-report, feature-comparison, visualization, profiling]
platforms: [python]
related_skills:
  - ydata-profiling
  - autoviz
  - pandas-data-processing
  - polars
  - great-tables
---

# Sweetviz EDA Comparison Skill

Master Sweetviz for automated exploratory data analysis with powerful comparison capabilities, target variable analysis, and beautiful HTML reports. Sweetviz excels at comparing datasets (train vs test) and analyzing features against a target variable.

## When to Use This Skill

### USE Sweetviz when:
- **Dataset comparison** - Comparing train vs test, before vs after, or any two datasets
- **Target variable analysis** - Understanding how features relate to a target
- **Quick EDA reports** - Need comprehensive EDA in one line of code
- **Feature comparison** - Analyzing feature distributions across subsets
- **HTML reports** - Creating shareable, interactive analysis reports
- **Intra-set analysis** - Comparing subpopulations within a dataset
- **Data validation** - Checking for data drift between datasets
- **Feature selection** - Identifying important features for modeling

### DON'T USE Sweetviz when:
- **Very large datasets** - Over 1M rows (use sampling)
- **Streaming data** - Need real-time analysis
- **Deep statistical tests** - Need p-values and hypothesis testing
- **Custom visualizations** - Specific chart requirements
- **Interactive dashboards** - Use Streamlit or Dash instead
- **Text/NLP analysis** - Use dedicated NLP tools

## Prerequisites

```bash
# Basic installation
pip install sweetviz

# Using uv (recommended)
uv pip install sweetviz pandas numpy

# With Jupyter support
pip install sweetviz pandas numpy jupyter

# Verify installation
python -c "import sweetviz as sv; print(f'Sweetviz version: {sv.__version__}')"
```

### System Requirements

- Python 3.6 or higher
- pandas 0.25.3 or higher
- numpy
- matplotlib (for internal plotting)
- Modern web browser (for viewing HTML reports)

## Core Capabilities

### 1. Basic EDA Report (Analyze)

**Single Dataset Analysis:**
```python
import sweetviz as sv
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv("data.csv")

# Generate basic EDA report
report = sv.analyze(df)

# Save HTML report
report.show_html("sweetviz_report.html")

# Show in notebook (auto-opens browser)
report.show_notebook()
```

**With Source Name:**
```python
import sweetviz as sv
import pandas as pd

df = pd.read_csv("sales_data.csv")

# Generate report with custom name
report = sv.analyze(
    source=df,
    pairwise_analysis="auto"  # "on", "off", or "auto"
)

report.show_html("sales_analysis.html", open_browser=True)
```

**Sample Dataset for Examples:**
```python
import sweetviz as sv
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Create comprehensive sample dataset
np.random.seed(42)
n = 5000

df = pd.DataFrame({
    # Numeric features
    "age": np.random.randint(18, 80, n),
    "income": np.random.exponential(50000, n),
    "credit_score": np.random.normal(700, 50, n).clip(300, 850).astype(int),
    "account_balance": np.random.exponential(10000, n),
    "transaction_count": np.random.poisson(15, n),

    # Categorical features
    "gender": np.random.choice(["Male", "Female", "Other"], n, p=[0.48, 0.48, 0.04]),
    "education": np.random.choice(
        ["High School", "Bachelor", "Master", "PhD"],
        n, p=[0.3, 0.4, 0.2, 0.1]
    ),
    "employment_status": np.random.choice(
        ["Employed", "Self-employed", "Unemployed", "Retired"],
        n, p=[0.6, 0.2, 0.1, 0.1]
    ),
    "region": np.random.choice(["North", "South", "East", "West"], n),

    # Date feature
    "join_date": [
        datetime(2020, 1, 1) + timedelta(days=int(d))
        for d in np.random.uniform(0, 1460, n)
    ],

    # Target variable (binary classification)
    "churned": np.random.choice([0, 1], n, p=[0.8, 0.2])
})

# Add some missing values
df.loc[np.random.choice(n, 200), "income"] = np.nan
df.loc[np.random.choice(n, 100), "credit_score"] = np.nan
df.loc[np.random.choice(n, 150), "education"] = np.nan

# Basic analysis
report = sv.analyze(df)
report.show_html("customer_analysis.html")
```

### 2. Target Variable Analysis

**Binary Target Analysis:**
```python
import sweetviz as sv
import pandas as pd
import numpy as np

# Create dataset with target variable
np.random.seed(42)
n = 3000

df = pd.DataFrame({
    "feature_1": np.random.randn(n),
    "feature_2": np.random.exponential(10, n),
    "feature_3": np.random.choice(["A", "B", "C"], n),
    "feature_4": np.random.randint(1, 100, n),
    "target": np.random.choice([0, 1], n, p=[0.7, 0.3])
})

# Analyze with target variable
# Shows how each feature relates to the target
report = sv.analyze(
    source=df,
    target_feat="target"  # Specify target column
)

report.show_html("target_analysis.html")
```

**Continuous Target Analysis:**
```python
import sweetviz as sv
import pandas as pd
import numpy as np

# Regression target example
np.random.seed(42)
n = 2000

# Features that affect the target
x1 = np.random.randn(n)
x2 = np.random.exponential(5, n)
x3 = np.random.choice([0, 1], n)

# Target is a function of features + noise
target = 10 + 2*x1 + 0.5*x2 + 3*x3 + np.random.randn(n)

df = pd.DataFrame({
    "feature_linear": x1,
    "feature_exp": x2,
    "feature_binary": x3,
    "feature_noise": np.random.randn(n),  # Unrelated feature
    "price": target  # Continuous target
})

# Analyze with continuous target
report = sv.analyze(
    source=df,
    target_feat="price"
)

report.show_html("regression_target_analysis.html")
```

**Multi-class Target:**
```python
import sweetviz as sv
import pandas as pd
import numpy as np

np.random.seed(42)
n = 2500

df = pd.DataFrame({
    "feature_1": np.random.randn(n),
    "feature_2": np.random.uniform(0, 100, n),
    "category": np.random.choice(["A", "B", "C"], n),
    "class_label": np.random.choice(
        ["Class_A", "Class_B", "Class_C", "Class_D"],
        n, p=[0.4, 0.3, 0.2, 0.1]
    )
})

# Multi-class target analysis
report = sv.analyze(
    source=df,
    target_feat="class_label"
)

report.show_html("multiclass_analysis.html")
```

### 3. Dataset Comparison (Compare)

**Train vs Test Comparison:**
```python
import sweetviz as sv
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# Create sample dataset
np.random.seed(42)
n = 5000

df = pd.DataFrame({
    "feature_1": np.random.randn(n),
    "feature_2": np.random.exponential(50, n),
    "feature_3": np.random.choice(["X", "Y", "Z"], n),
    "feature_4": np.random.randint(1, 100, n),
    "target": np.random.choice([0, 1], n, p=[0.75, 0.25])
})

# Split into train and test
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

print(f"Train shape: {train_df.shape}")
print(f"Test shape: {test_df.shape}")

# Compare train vs test datasets
comparison_report = sv.compare(
    source=[train_df, "Training Data"],
    compare=[test_df, "Test Data"],
    target_feat="target"
)

comparison_report.show_html("train_test_comparison.html")
```

**Before vs After Comparison:**
```python
import sweetviz as sv
import pandas as pd
import numpy as np

np.random.seed(42)

# Original data with issues
df_before = pd.DataFrame({
    "value": np.concatenate([
        np.random.randn(900),
        np.array([50, -30, 100, 75, -50])  # Outliers
    ]),
    "category": np.random.choice(["A", "B", "C"], 905),
    "score": np.random.uniform(0, 100, 905)
})

# Add missing values
df_before.loc[np.random.choice(905, 80), "value"] = np.nan

# Cleaned data
df_after = df_before.copy()

# Remove outliers using IQR
Q1 = df_after["value"].quantile(0.25)
Q3 = df_after["value"].quantile(0.75)
IQR = Q3 - Q1
df_after = df_after[
    (df_after["value"].isna()) |  # Keep NaN for now
    ((df_after["value"] >= Q1 - 1.5 * IQR) &
     (df_after["value"] <= Q3 + 1.5 * IQR))
]

# Fill missing values
df_after["value"] = df_after["value"].fillna(df_after["value"].median())

# Compare before vs after cleaning
comparison = sv.compare(
    source=[df_before, "Before Cleaning"],
    compare=[df_after, "After Cleaning"]
)

comparison.show_html("cleaning_comparison.html")
```

**Production vs Development Data:**
```python
import sweetviz as sv
import pandas as pd
import numpy as np

np.random.seed(42)

# Development data (historical)
df_dev = pd.DataFrame({
    "feature_1": np.random.randn(3000),
    "feature_2": np.random.exponential(100, 3000),
    "category": np.random.choice(["A", "B", "C"], 3000, p=[0.5, 0.3, 0.2])
})

# Production data (slightly different distribution - data drift)
df_prod = pd.DataFrame({
    "feature_1": np.random.randn(1000) * 1.2 + 0.3,  # Shifted and scaled
    "feature_2": np.random.exponential(120, 1000),    # Different mean
    "category": np.random.choice(["A", "B", "C", "D"], 1000, p=[0.4, 0.3, 0.2, 0.1])  # New category
})

# Detect data drift
drift_report = sv.compare(
    source=[df_dev, "Development"],
    compare=[df_prod, "Production"]
)

drift_report.show_html("data_drift_analysis.html")
```

### 4. Intra-set Comparison (Compare_Intra)

**Compare Subpopulations Within Dataset:**
```python
import sweetviz as sv
import pandas as pd
import numpy as np

np.random.seed(42)
n = 4000

# Create dataset with a categorical variable for splitting
df = pd.DataFrame({
    "age": np.random.randint(18, 70, n),
    "income": np.random.exponential(50000, n),
    "purchases": np.random.poisson(10, n),
    "satisfaction_score": np.random.uniform(1, 5, n),
    "customer_type": np.random.choice(["Premium", "Standard"], n, p=[0.3, 0.7]),
    "churned": np.random.choice([0, 1], n, p=[0.85, 0.15])
})

# Compare Premium vs Standard customers within same dataset
intra_report = sv.compare_intra(
    source_df=df,
    condition_series=df["customer_type"] == "Premium",
    names=["Premium Customers", "Standard Customers"],
    target_feat="churned"
)

intra_report.show_html("customer_type_comparison.html")
```

**Compare by Boolean Condition:**
```python
import sweetviz as sv
import pandas as pd
import numpy as np

np.random.seed(42)
n = 3000

df = pd.DataFrame({
    "age": np.random.randint(18, 80, n),
    "income": np.random.exponential(60000, n),
    "credit_score": np.random.normal(700, 50, n).astype(int),
    "loan_amount": np.random.exponential(20000, n),
    "default": np.random.choice([0, 1], n, p=[0.9, 0.1])
})

# Compare high-income vs low-income customers
median_income = df["income"].median()

income_comparison = sv.compare_intra(
    source_df=df,
    condition_series=df["income"] > median_income,
    names=["High Income", "Low Income"],
    target_feat="default"
)

income_comparison.show_html("income_segment_comparison.html")
```

**Multiple Segment Analysis:**
```python
import sweetviz as sv
import pandas as pd
import numpy as np

np.random.seed(42)
n = 5000

df = pd.DataFrame({
    "age": np.random.randint(18, 80, n),
    "spend": np.random.exponential(500, n),
    "visits": np.random.poisson(5, n),
    "region": np.random.choice(["North", "South", "East", "West"], n),
    "converted": np.random.choice([0, 1], n, p=[0.8, 0.2])
})

# Create age groups
df["age_group"] = pd.cut(
    df["age"],
    bins=[0, 30, 50, 100],
    labels=["Young", "Middle", "Senior"]
)

# Compare Young vs Senior (Middle excluded)
age_comparison = sv.compare_intra(
    source_df=df,
    condition_series=df["age_group"] == "Young",
    names=["Young (18-30)", "Senior (50+)"],
    target_feat="converted"
)

age_comparison.show_html("age_group_comparison.html")
```

### 5. Feature Configuration

**Specifying Feature Types:**
```python
import sweetviz as sv
import pandas as pd
import numpy as np

np.random.seed(42)
n = 2000

df = pd.DataFrame({
    "id": range(1, n + 1),
    "zip_code": np.random.randint(10000, 99999, n),  # Should be categorical
    "rating": np.random.randint(1, 6, n),  # Ordinal (1-5 stars)
    "revenue": np.random.exponential(1000, n),
    "category": np.random.choice(["A", "B", "C"], n),
    "target": np.random.choice([0, 1], n)
})

# Configure feature types
feature_config = sv.FeatureConfig(
    skip=["id"],  # Skip ID column
    force_cat=["zip_code", "rating"],  # Force as categorical
    force_num=[]  # Force as numerical (if needed)
)

report = sv.analyze(
    source=df,
    target_feat="target",
    feat_cfg=feature_config
)

report.show_html("configured_analysis.html")
```

**Skipping Features:**
```python
import sweetviz as sv
import pandas as pd
import numpy as np

np.random.seed(42)
n = 1500

df = pd.DataFrame({
    "user_id": range(n),
    "session_id": [f"sess_{i}" for i in range(n)],
    "email": [f"user_{i}@example.com" for i in range(n)],
    "feature_1": np.random.randn(n),
    "feature_2": np.random.exponential(10, n),
    "outcome": np.random.choice([0, 1], n)
})

# Skip ID and PII columns
config = sv.FeatureConfig(
    skip=["user_id", "session_id", "email"]
)

report = sv.analyze(
    source=df,
    target_feat="outcome",
    feat_cfg=config
)

report.show_html("filtered_analysis.html")
```

### 6. Pairwise Analysis Control

**Controlling Correlation Analysis:**
```python
import sweetviz as sv
import pandas as pd
import numpy as np

np.random.seed(42)
n = 2000

# Dataset with many features
df = pd.DataFrame({
    f"feature_{i}": np.random.randn(n) for i in range(20)
})
df["target"] = np.random.choice([0, 1], n)

# Disable pairwise analysis for speed
report_fast = sv.analyze(
    source=df,
    target_feat="target",
    pairwise_analysis="off"  # Faster, no correlation matrix
)

# Enable pairwise analysis for full correlations
report_full = sv.analyze(
    source=df,
    target_feat="target",
    pairwise_analysis="on"  # Shows feature correlations
)

# Auto mode (default) - enables if < 20 features
report_auto = sv.analyze(
    source=df,
    target_feat="target",
    pairwise_analysis="auto"
)

report_full.show_html("full_pairwise.html")
```

## Complete Examples

### Example 1: ML Dataset Profiling Pipeline

```python
#!/usr/bin/env python3
"""ml_profiling_pipeline.py - Complete ML dataset profiling with Sweetviz"""

import sweetviz as sv
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from datetime import datetime
import os
import json

def ml_profiling_pipeline(
    df: pd.DataFrame,
    target_col: str,
    output_dir: str,
    test_size: float = 0.2,
    id_cols: list = None,
    cat_cols: list = None
) -> dict:
    """
    Complete ML dataset profiling pipeline.

    Args:
        df: Input DataFrame
        target_col: Target variable column name
        output_dir: Directory for output reports
        test_size: Test set proportion
        id_cols: Columns to skip (IDs, etc.)
        cat_cols: Columns to force as categorical

    Returns:
        Dictionary with profiling results
    """
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print(f"Starting ML profiling pipeline")
    print(f"Dataset shape: {df.shape}")
    print(f"Target column: {target_col}")

    results = {
        "timestamp": timestamp,
        "original_shape": df.shape,
        "target_column": target_col,
        "reports": {}
    }

    # Configure features
    feat_cfg = sv.FeatureConfig(
        skip=id_cols or [],
        force_cat=cat_cols or []
    )

    # 1. Full dataset analysis with target
    print("\n1. Generating full dataset analysis...")
    full_report = sv.analyze(
        source=df,
        target_feat=target_col,
        feat_cfg=feat_cfg,
        pairwise_analysis="auto"
    )

    full_path = os.path.join(output_dir, f"full_analysis_{timestamp}.html")
    full_report.show_html(full_path, open_browser=False)
    results["reports"]["full_analysis"] = full_path
    print(f"   Saved: {full_path}")

    # 2. Split data
    print("\n2. Splitting into train/test...")
    train_df, test_df = train_test_split(
        df, test_size=test_size, random_state=42,
        stratify=df[target_col] if df[target_col].nunique() < 20 else None
    )

    results["train_shape"] = train_df.shape
    results["test_shape"] = test_df.shape
    print(f"   Train: {train_df.shape}, Test: {test_df.shape}")

    # 3. Train vs Test comparison
    print("\n3. Generating train vs test comparison...")
    comparison_report = sv.compare(
        source=[train_df, "Training Set"],
        compare=[test_df, "Test Set"],
        target_feat=target_col,
        feat_cfg=feat_cfg
    )

    comparison_path = os.path.join(output_dir, f"train_test_comparison_{timestamp}.html")
    comparison_report.show_html(comparison_path, open_browser=False)
    results["reports"]["train_test_comparison"] = comparison_path
    print(f"   Saved: {comparison_path}")

    # 4. Target class analysis (for classification)
    if df[target_col].nunique() <= 10:
        print("\n4. Generating target class comparison...")

        # Get most common classes
        top_classes = df[target_col].value_counts().nlargest(2).index.tolist()

        if len(top_classes) >= 2:
            class_comparison = sv.compare_intra(
                source_df=df,
                condition_series=df[target_col] == top_classes[0],
                names=[f"Class: {top_classes[0]}", f"Class: {top_classes[1]}"],
                feat_cfg=feat_cfg
            )

            class_path = os.path.join(output_dir, f"class_comparison_{timestamp}.html")
            class_comparison.show_html(class_path, open_browser=False)
            results["reports"]["class_comparison"] = class_path
            print(f"   Saved: {class_path}")

    # 5. Summary statistics
    print("\n5. Calculating summary statistics...")

    results["feature_summary"] = {
        "total_features": len(df.columns) - 1,
        "numeric_features": len(df.select_dtypes(include=[np.number]).columns) - 1,
        "categorical_features": len(df.select_dtypes(include=["object", "category"]).columns),
        "missing_values": df.isnull().sum().sum(),
        "missing_percentage": (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
    }

    # Target distribution
    target_dist = df[target_col].value_counts(normalize=True).to_dict()
    results["target_distribution"] = {str(k): round(v, 4) for k, v in target_dist.items()}

    # Save results JSON
    results_path = os.path.join(output_dir, f"profiling_results_{timestamp}.json")
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n{'='*60}")
    print(f"Pipeline Complete!")
    print(f"Reports saved to: {output_dir}")
    print(f"Results JSON: {results_path}")
    print(f"{'='*60}")

    return results


def create_sample_ml_dataset(n_samples: int = 5000) -> pd.DataFrame:
    """Create sample ML dataset for demonstration."""
    np.random.seed(42)

    df = pd.DataFrame({
        "customer_id": range(1, n_samples + 1),
        "age": np.random.randint(18, 80, n_samples),
        "income": np.random.exponential(50000, n_samples),
        "credit_score": np.random.normal(700, 50, n_samples).clip(300, 850).astype(int),
        "account_age_days": np.random.exponential(365, n_samples).astype(int),
        "num_products": np.random.poisson(3, n_samples),
        "total_transactions": np.random.poisson(50, n_samples),
        "avg_transaction_value": np.random.exponential(100, n_samples),
        "support_tickets": np.random.poisson(2, n_samples),
        "satisfaction_score": np.random.uniform(1, 5, n_samples),
        "tenure_category": np.random.choice(["New", "Regular", "Loyal"], n_samples, p=[0.3, 0.4, 0.3]),
        "channel": np.random.choice(["Online", "Mobile", "Branch"], n_samples),
        "region": np.random.choice(["North", "South", "East", "West"], n_samples),
        "churned": np.random.choice([0, 1], n_samples, p=[0.85, 0.15])
    })

    # Add missing values
    df.loc[np.random.choice(n_samples, 200), "income"] = np.nan
    df.loc[np.random.choice(n_samples, 100), "credit_score"] = np.nan
    df.loc[np.random.choice(n_samples, 150), "satisfaction_score"] = np.nan

    return df


# Example usage
if __name__ == "__main__":
    # Create sample dataset
    df = create_sample_ml_dataset(5000)

    # Run profiling pipeline
    results = ml_profiling_pipeline(
        df=df,
        target_col="churned",
        output_dir="ml_profiling_output",
        test_size=0.2,
        id_cols=["customer_id"],
        cat_cols=["credit_score"]
    )

    print("\nResults Summary:")
    print(f"  Train shape: {results['train_shape']}")
    print(f"  Test shape: {results['test_shape']}")
    print(f"  Target distribution: {results['target_distribution']}")
```

### Example 2: Data Quality Assessment

```python
#!/usr/bin/env python3
"""data_quality_assessment.py - Data quality assessment with Sweetviz"""

import sweetviz as sv
import pandas as pd
import numpy as np
from datetime import datetime
import os
import json

def assess_data_quality(
    df: pd.DataFrame,
    output_dir: str,
    reference_df: pd.DataFrame = None,
    target_col: str = None
) -> dict:
    """
    Comprehensive data quality assessment.

    Args:
        df: DataFrame to assess
        output_dir: Output directory for reports
        reference_df: Reference/baseline dataset for comparison
        target_col: Optional target variable

    Returns:
        Quality assessment results
    """
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    results = {
        "timestamp": timestamp,
        "dataset_shape": df.shape,
        "quality_metrics": {},
        "reports": []
    }

    # 1. Basic quality metrics
    print("Calculating quality metrics...")

    # Completeness
    total_cells = df.shape[0] * df.shape[1]
    missing_cells = df.isnull().sum().sum()
    completeness = (1 - missing_cells / total_cells) * 100

    # Missing by column
    missing_by_col = df.isnull().sum().to_dict()
    missing_pct_by_col = {k: round(v / len(df) * 100, 2) for k, v in missing_by_col.items()}

    # Uniqueness
    duplicate_rows = df.duplicated().sum()
    uniqueness = (1 - duplicate_rows / len(df)) * 100

    # Cardinality
    cardinality = {col: df[col].nunique() for col in df.columns}
    high_cardinality = [col for col, nunique in cardinality.items()
                        if nunique / len(df) > 0.9]
    constant_cols = [col for col, nunique in cardinality.items() if nunique <= 1]

    results["quality_metrics"] = {
        "completeness_score": round(completeness, 2),
        "uniqueness_score": round(uniqueness, 2),
        "total_missing_cells": int(missing_cells),
        "missing_by_column": missing_pct_by_col,
        "duplicate_rows": int(duplicate_rows),
        "high_cardinality_columns": high_cardinality,
        "constant_columns": constant_cols,
        "cardinality": cardinality
    }

    # 2. Generate Sweetviz report
    print("Generating Sweetviz analysis report...")

    # Configure to skip obvious ID columns
    potential_ids = [col for col in df.columns
                     if df[col].nunique() == len(df) or "id" in col.lower()]

    feat_cfg = sv.FeatureConfig(skip=potential_ids)

    analysis_report = sv.analyze(
        source=df,
        target_feat=target_col,
        feat_cfg=feat_cfg,
        pairwise_analysis="auto"
    )

    report_path = os.path.join(output_dir, f"quality_analysis_{timestamp}.html")
    analysis_report.show_html(report_path, open_browser=False)
    results["reports"].append(report_path)

    # 3. Reference comparison (if provided)
    if reference_df is not None:
        print("Generating reference comparison report...")

        comparison_report = sv.compare(
            source=[reference_df, "Reference/Baseline"],
            compare=[df, "Current Dataset"],
            target_feat=target_col,
            feat_cfg=feat_cfg
        )

        comparison_path = os.path.join(output_dir, f"reference_comparison_{timestamp}.html")
        comparison_report.show_html(comparison_path, open_browser=False)
        results["reports"].append(comparison_path)

        # Calculate drift metrics
        drift_metrics = {}
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        for col in numeric_cols:
            if col in reference_df.columns:
                ref_mean = reference_df[col].mean()
                curr_mean = df[col].mean()
                ref_std = reference_df[col].std()

                if ref_std > 0:
                    drift = abs(curr_mean - ref_mean) / ref_std
                    drift_metrics[col] = round(drift, 3)

        results["drift_metrics"] = drift_metrics
        results["significant_drift"] = [
            col for col, score in drift_metrics.items() if score > 0.5
        ]

    # 4. Save results
    results_path = os.path.join(output_dir, f"quality_results_{timestamp}.json")
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2, default=str)

    # 5. Print summary
    print(f"\n{'='*60}")
    print("DATA QUALITY ASSESSMENT SUMMARY")
    print(f"{'='*60}")
    print(f"Dataset Shape: {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"\nQuality Scores:")
    print(f"  Completeness: {completeness:.1f}%")
    print(f"  Uniqueness:   {uniqueness:.1f}%")
    print(f"\nIssues Found:")
    print(f"  Missing values: {missing_cells:,}")
    print(f"  Duplicate rows: {duplicate_rows:,}")
    print(f"  Constant columns: {len(constant_cols)}")
    print(f"  High cardinality: {len(high_cardinality)}")

    if reference_df is not None and results.get("significant_drift"):
        print(f"\nData Drift Warning:")
        print(f"  Significant drift in: {results['significant_drift']}")

    print(f"\nReports saved to: {output_dir}")
    print(f"{'='*60}")

    return results


# Example usage
if __name__ == "__main__":
    np.random.seed(42)
    n = 3000

    # Create current dataset
    df_current = pd.DataFrame({
        "id": range(n),
        "value_a": np.random.randn(n),
        "value_b": np.random.exponential(100, n),
        "category": np.random.choice(["X", "Y", "Z"], n),
        "score": np.random.uniform(0, 100, n)
    })

    # Add some quality issues
    df_current.loc[np.random.choice(n, 200), "value_a"] = np.nan
    df_current.loc[np.random.choice(n, 100), "value_b"] = np.nan

    # Create reference dataset (slightly different)
    df_reference = pd.DataFrame({
        "id": range(n),
        "value_a": np.random.randn(n),
        "value_b": np.random.exponential(100, n),
        "category": np.random.choice(["X", "Y", "Z"], n),
        "score": np.random.uniform(0, 100, n)
    })

    # Run assessment
    results = assess_data_quality(
        df=df_current,
        output_dir="quality_assessment_output",
        reference_df=df_reference
    )
```

### Example 3: Feature Selection Analysis

```python
#!/usr/bin/env python3
"""feature_selection_analysis.py - Feature analysis for ML with Sweetviz"""

import sweetviz as sv
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os

def analyze_features_for_selection(
    df: pd.DataFrame,
    target_col: str,
    output_dir: str
) -> dict:
    """
    Analyze features for selection using Sweetviz.

    Args:
        df: Input DataFrame with features and target
        target_col: Target variable column name
        output_dir: Output directory

    Returns:
        Feature analysis results
    """
    os.makedirs(output_dir, exist_ok=True)

    # Identify feature types
    numeric_features = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = df.select_dtypes(include=["object", "category"]).columns.tolist()

    # Remove target from features
    if target_col in numeric_features:
        numeric_features.remove(target_col)
    if target_col in categorical_features:
        categorical_features.remove(target_col)

    print(f"Analyzing {len(numeric_features)} numeric and {len(categorical_features)} categorical features")

    # 1. Full feature analysis with target
    print("\n1. Generating full feature analysis...")
    full_report = sv.analyze(
        source=df,
        target_feat=target_col,
        pairwise_analysis="on"  # Enable correlation analysis
    )
    full_report.show_html(
        os.path.join(output_dir, "full_feature_analysis.html"),
        open_browser=False
    )

    # 2. Analyze by target classes
    if df[target_col].nunique() <= 10:
        print("\n2. Analyzing feature distributions by target class...")

        target_values = df[target_col].unique()

        if len(target_values) >= 2:
            # Compare top two classes
            class1, class2 = sorted(
                df[target_col].value_counts().nlargest(2).index.tolist()
            )

            class_report = sv.compare_intra(
                source_df=df,
                condition_series=df[target_col] == class1,
                names=[f"Target={class1}", f"Target={class2}"]
            )
            class_report.show_html(
                os.path.join(output_dir, "feature_by_target_class.html"),
                open_browser=False
            )

    # 3. Analyze missing patterns
    missing_cols = df.columns[df.isnull().any()].tolist()

    if missing_cols:
        print(f"\n3. Found {len(missing_cols)} columns with missing values")

        # Create missing indicator for analysis
        df_missing = df.copy()
        for col in missing_cols:
            df_missing[f"{col}_missing"] = df[col].isnull().astype(int)

        # Analyze how missing values relate to target
        missing_cols_indicators = [f"{col}_missing" for col in missing_cols]
        df_subset = df_missing[missing_cols_indicators + [target_col]]

        missing_report = sv.analyze(
            source=df_subset,
            target_feat=target_col
        )
        missing_report.show_html(
            os.path.join(output_dir, "missing_pattern_analysis.html"),
            open_browser=False
        )

    # 4. Calculate basic feature importance indicators
    print("\n4. Calculating feature statistics...")

    feature_stats = []

    for col in numeric_features:
        stats = {
            "feature": col,
            "type": "numeric",
            "missing_pct": df[col].isnull().mean() * 100,
            "unique_ratio": df[col].nunique() / len(df),
            "std": df[col].std(),
            "cv": df[col].std() / df[col].mean() if df[col].mean() != 0 else 0
        }

        # Correlation with target if target is numeric
        if df[target_col].dtype in [np.int64, np.float64]:
            stats["target_correlation"] = df[col].corr(df[target_col])

        feature_stats.append(stats)

    for col in categorical_features:
        stats = {
            "feature": col,
            "type": "categorical",
            "missing_pct": df[col].isnull().mean() * 100,
            "unique_ratio": df[col].nunique() / len(df),
            "n_categories": df[col].nunique()
        }
        feature_stats.append(stats)

    feature_df = pd.DataFrame(feature_stats)
    feature_df.to_csv(
        os.path.join(output_dir, "feature_statistics.csv"),
        index=False
    )

    print(f"\nReports saved to: {output_dir}")

    return {
        "numeric_features": numeric_features,
        "categorical_features": categorical_features,
        "feature_stats": feature_stats,
        "missing_columns": missing_cols
    }


# Example usage
if __name__ == "__main__":
    np.random.seed(42)
    n = 3000

    # Create features with varying importance
    x1 = np.random.randn(n)  # Important
    x2 = np.random.randn(n)  # Important
    x3 = np.random.randn(n)  # Noise

    df = pd.DataFrame({
        "important_feature_1": x1,
        "important_feature_2": x2,
        "noise_feature": x3,
        "categorical_feature": np.random.choice(["A", "B", "C"], n),
        "target": ((x1 + x2) > 0).astype(int)
    })

    # Add missing values
    df.loc[np.random.choice(n, 100), "important_feature_1"] = np.nan

    results = analyze_features_for_selection(
        df=df,
        target_col="target",
        output_dir="feature_analysis_output"
    )
```

## Integration Examples

### Sweetviz with Streamlit

```python
#!/usr/bin/env python3
"""sweetviz_streamlit.py - Streamlit app for Sweetviz reports"""

import streamlit as st
import sweetviz as sv
import pandas as pd
import tempfile
import os

st.set_page_config(page_title="Sweetviz EDA", layout="wide")
st.title("Sweetviz Exploratory Data Analysis")

# File upload
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Data Preview")
    st.dataframe(df.head(100))

    st.subheader("Dataset Info")
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())

    # Analysis options
    st.sidebar.header("Analysis Options")

    target_col = st.sidebar.selectbox(
        "Target Variable (optional)",
        ["None"] + list(df.columns)
    )

    pairwise = st.sidebar.selectbox(
        "Pairwise Analysis",
        ["auto", "on", "off"]
    )

    skip_cols = st.sidebar.multiselect(
        "Columns to Skip",
        list(df.columns)
    )

    if st.button("Generate Report"):
        with st.spinner("Generating Sweetviz report..."):
            feat_cfg = sv.FeatureConfig(skip=skip_cols) if skip_cols else None

            report = sv.analyze(
                source=df,
                target_feat=target_col if target_col != "None" else None,
                feat_cfg=feat_cfg,
                pairwise_analysis=pairwise
            )

            # Save to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
                report.show_html(f.name, open_browser=False)

                with open(f.name, "r") as html_file:
                    html_content = html_file.read()

                os.unlink(f.name)

            # Display in iframe
            st.components.v1.html(html_content, height=800, scrolling=True)
```

### Sweetviz with Jupyter Magic

```python
# In Jupyter notebook
import sweetviz as sv
import pandas as pd

# Load data
df = pd.read_csv("data.csv")

# Quick analysis (opens in new tab)
report = sv.analyze(df)
report.show_notebook()  # Opens in browser from notebook

# Inline display (for newer Jupyter versions)
report.show_notebook(
    w="100%",  # Width
    h="600px",  # Height
    scale=0.8  # Scale factor
)

# For comparison
train_df = df.sample(frac=0.8)
test_df = df.drop(train_df.index)

comparison = sv.compare(
    [train_df, "Train"],
    [test_df, "Test"]
)
comparison.show_notebook()
```

### Sweetviz in Data Pipeline

```python
#!/usr/bin/env python3
"""data_pipeline_sweetviz.py - Integrate Sweetviz in data pipeline"""

import sweetviz as sv
import pandas as pd
import numpy as np
from datetime import datetime
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataPipelineProfiler:
    """Sweetviz profiler for data pipelines."""

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.reports = []

    def profile_stage(
        self,
        df: pd.DataFrame,
        stage_name: str,
        target_col: str = None,
        previous_df: pd.DataFrame = None
    ) -> str:
        """
        Profile data at a pipeline stage.

        Args:
            df: DataFrame at current stage
            stage_name: Name of the pipeline stage
            target_col: Target variable (optional)
            previous_df: DataFrame from previous stage (optional)

        Returns:
            Path to generated report
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if previous_df is not None:
            # Comparison report
            logger.info(f"Generating comparison report for stage: {stage_name}")

            report = sv.compare(
                source=[previous_df, "Before"],
                compare=[df, "After"],
                target_feat=target_col
            )

            report_path = os.path.join(
                self.output_dir,
                f"{stage_name}_comparison_{timestamp}.html"
            )
        else:
            # Single analysis report
            logger.info(f"Generating analysis report for stage: {stage_name}")

            report = sv.analyze(
                source=df,
                target_feat=target_col
            )

            report_path = os.path.join(
                self.output_dir,
                f"{stage_name}_analysis_{timestamp}.html"
            )

        report.show_html(report_path, open_browser=False)
        self.reports.append(report_path)

        logger.info(f"Report saved: {report_path}")
        return report_path

    def generate_summary(self) -> dict:
        """Generate summary of all profiling reports."""
        return {
            "total_reports": len(self.reports),
            "reports": self.reports,
            "output_dir": self.output_dir
        }


# Example pipeline usage
def example_pipeline():
    """Example data pipeline with profiling."""
    profiler = DataPipelineProfiler("pipeline_reports")

    # Stage 1: Raw data
    np.random.seed(42)
    df_raw = pd.DataFrame({
        "value": np.concatenate([np.random.randn(950), [100, -50, np.nan] * 10]),
        "category": np.random.choice(["A", "B", "C"], 980),
        "target": np.random.choice([0, 1], 980)
    })

    profiler.profile_stage(df_raw, "01_raw_data", target_col="target")

    # Stage 2: Missing value handling
    df_cleaned = df_raw.copy()
    df_cleaned["value"] = df_cleaned["value"].fillna(df_cleaned["value"].median())

    profiler.profile_stage(
        df_cleaned, "02_missing_handled",
        target_col="target",
        previous_df=df_raw
    )

    # Stage 3: Outlier removal
    Q1 = df_cleaned["value"].quantile(0.25)
    Q3 = df_cleaned["value"].quantile(0.75)
    IQR = Q3 - Q1

    df_no_outliers = df_cleaned[
        (df_cleaned["value"] >= Q1 - 1.5 * IQR) &
        (df_cleaned["value"] <= Q3 + 1.5 * IQR)
    ]

    profiler.profile_stage(
        df_no_outliers, "03_outliers_removed",
        target_col="target",
        previous_df=df_cleaned
    )

    # Summary
    summary = profiler.generate_summary()
    print(f"\nPipeline profiling complete!")
    print(f"Generated {summary['total_reports']} reports")

    return summary


if __name__ == "__main__":
    example_pipeline()
```

## Best Practices

### 1. Use Target Analysis for ML Projects

```python
# GOOD: Always specify target for ML datasets
report = sv.analyze(df, target_feat="target")

# AVOID: Missing target analysis
report = sv.analyze(df)  # No target relationship shown
```

### 2. Sample Large Datasets

```python
# GOOD: Sample for large datasets
if len(df) > 100000:
    df_sample = df.sample(n=100000, random_state=42)
    report = sv.analyze(df_sample)
else:
    report = sv.analyze(df)

# AVOID: Analyzing huge datasets directly
# report = sv.analyze(df_with_millions_of_rows)  # Very slow
```

### 3. Configure Feature Types Properly

```python
# GOOD: Force categorical for ID-like numeric columns
config = sv.FeatureConfig(
    skip=["customer_id", "transaction_id"],
    force_cat=["zip_code", "area_code", "rating"]
)
report = sv.analyze(df, feat_cfg=config)

# AVOID: Letting Sweetviz treat zip codes as numeric
```

### 4. Use Comparison for Validation

```python
# GOOD: Compare train/test for data leakage detection
comparison = sv.compare(
    [train_df, "Train"],
    [test_df, "Test"],
    target_feat="target"
)

# AVOID: Only analyzing training data
```

### 5. Control Pairwise Analysis

```python
# GOOD: Disable for speed on many features
report = sv.analyze(df, pairwise_analysis="off")  # Fast

# GOOD: Enable when feature correlations matter
report = sv.analyze(df, pairwise_analysis="on")   # Full correlations
```

## Troubleshooting

### Common Issues

**Issue: Report generation is slow**
```python
# Solution 1: Disable pairwise analysis
report = sv.analyze(df, pairwise_analysis="off")

# Solution 2: Sample data
report = sv.analyze(df.sample(50000))

# Solution 3: Skip high-cardinality columns
config = sv.FeatureConfig(skip=["high_card_col"])
report = sv.analyze(df, feat_cfg=config)
```

**Issue: Memory error with large dataset**
```python
# Solution: Process in chunks or sample
sample_size = min(len(df), 100000)
report = sv.analyze(df.sample(sample_size, random_state=42))
```

**Issue: HTML report won't open**
```python
# Solution: Save and open manually
report.show_html("report.html", open_browser=False)
# Then open report.html in browser

# Or specify layout
report.show_html("report.html", layout="vertical")
```

**Issue: Categorical variables treated as numeric**
```python
# Solution: Force categorical type
config = sv.FeatureConfig(force_cat=["zip_code", "rating"])
report = sv.analyze(df, feat_cfg=config)

# Or convert before analysis
df["zip_code"] = df["zip_code"].astype(str)
```

**Issue: Date columns not recognized**
```python
# Solution: Convert to proper datetime
df["date_col"] = pd.to_datetime(df["date_col"])
report = sv.analyze(df)
```

**Issue: Report shows too many categories**
```python
# Sweetviz automatically limits to top categories
# For custom handling, reduce cardinality before analysis
df["category"] = df["category"].apply(
    lambda x: x if x in top_categories else "Other"
)
```

## Version History

- **1.0.0** (2026-01-17): Initial release
  - Basic EDA report generation (analyze)
  - Target variable analysis
  - Dataset comparison (compare)
  - Intra-set comparison (compare_intra)
  - Feature configuration options
  - Pairwise analysis control
  - ML profiling pipeline example
  - Data quality assessment example
  - Feature selection analysis example
  - Streamlit integration
  - Data pipeline integration
  - Best practices and troubleshooting

## Resources

- **Official Documentation**: https://github.com/fbdesignpro/sweetviz
- **PyPI**: https://pypi.org/project/sweetviz/
- **Medium Article**: https://towardsdatascience.com/powerful-eda-exploratory-data-analysis-in-just-two-lines-of-code-using-sweetviz-6c943d32f34

---

**Generate powerful EDA comparison reports with Sweetviz - analyze, compare, and understand your data!**
