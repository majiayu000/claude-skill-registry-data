---
name: autoviz
version: 1.0.0
description: Automatic exploratory data analysis and visualization with a single line of code - generates comprehensive charts, detects patterns, and exports to HTML/notebooks
author: workspace-hub
category: data-analysis
capabilities:
  - One-line automatic EDA
  - Feature distribution analysis
  - Correlation detection and visualization
  - Outlier identification and highlighting
  - Automated chart type selection
  - Export to HTML and Jupyter notebooks
  - Support for large datasets with sampling
  - Categorical and numerical feature analysis
tools:
  - autoviz
  - pandas
  - matplotlib
  - seaborn
  - plotly
tags: [autoviz, eda, exploratory-data-analysis, visualization, automated, charts, correlation, distribution, outliers, feature-analysis]
platforms: [python]
related_skills:
  - ydata-profiling
  - pandas-data-processing
  - polars
  - plotly
  - streamlit
---

# AutoViz Automatic EDA Skill

Master AutoViz for instant exploratory data analysis with a single line of code. Generate comprehensive visualizations, detect patterns, identify outliers, and export publication-ready charts automatically.

## When to Use This Skill

### USE AutoViz when:
- **Quick EDA** - Need rapid insights into a new dataset
- **Initial exploration** - Starting analysis on unfamiliar data
- **Pattern discovery** - Automatically detect relationships between variables
- **Presentation prep** - Need charts quickly for stakeholder meetings
- **Large datasets** - Built-in sampling handles big data efficiently
- **Feature analysis** - Understanding distribution and importance of features
- **Correlation hunting** - Finding relationships without manual chart creation
- **Report generation** - Export comprehensive HTML reports

### DON'T USE AutoViz when:
- **Custom visualizations** - Need highly specific chart designs
- **Interactive dashboards** - Use Streamlit or Dash instead
- **Real-time data** - Streaming visualization requirements
- **Production systems** - Charts for automated pipelines (use Plotly/Altair)
- **Precise statistical tests** - Need formal hypothesis testing
- **Domain-specific plots** - Specialized visualizations not in standard EDA

## Prerequisites

```bash
# Basic installation
pip install autoviz

# With all visualization backends
pip install autoviz matplotlib seaborn plotly bokeh

# Using uv (recommended)
uv pip install autoviz pandas matplotlib seaborn plotly

# Jupyter notebook support
pip install autoviz ipywidgets notebook

# Verify installation
python -c "from autoviz import AutoViz_Class; print('AutoViz ready!')"
```

## Core Capabilities

### 1. Basic One-Line EDA

**Simplest Usage:**
```python
from autoviz import AutoViz_Class

# Initialize AutoViz
AV = AutoViz_Class()

# Automatic visualization with one line
# Returns a dataframe and generates all charts
df_analyzed = AV.AutoViz(
    filename="data.csv",
    sep=",",
    depVar="",  # Target variable (optional)
    dfte=None,  # Pass DataFrame directly instead of filename
    header=0,
    verbose=1,  # 0=minimal, 1=medium, 2=detailed output
    lowess=False,
    chart_format="svg",
    max_rows_analyzed=150000,
    max_cols_analyzed=30
)

print(f"Analyzed {df_analyzed.shape[0]} rows, {df_analyzed.shape[1]} columns")
```

**From DataFrame:**
```python
from autoviz import AutoViz_Class
import pandas as pd

# Load your data
df = pd.read_csv("sales_data.csv")

# Or create sample data
df = pd.DataFrame({
    "revenue": [100, 200, 150, 300, 250, 400, 350, 500],
    "units": [10, 20, 15, 30, 25, 40, 35, 50],
    "category": ["A", "B", "A", "B", "A", "B", "A", "B"],
    "region": ["North", "South", "East", "West", "North", "South", "East", "West"],
    "profit": [20, 40, 30, 60, 50, 80, 70, 100],
    "customer_age": [25, 35, 45, 55, 30, 40, 50, 60]
})

# Initialize and visualize
AV = AutoViz_Class()

# Pass DataFrame directly using dfte parameter
df_result = AV.AutoViz(
    filename="",  # Empty when using dfte
    sep=",",
    depVar="profit",  # Optional: specify target variable
    dfte=df,
    header=0,
    verbose=1,
    chart_format="png"
)
```

**With Target Variable Analysis:**
```python
from autoviz import AutoViz_Class
import pandas as pd

# Classification dataset
df_classification = pd.DataFrame({
    "feature_1": [1.2, 2.3, 1.5, 3.4, 2.1, 4.5, 3.2, 5.1],
    "feature_2": [0.5, 1.2, 0.8, 2.1, 1.0, 3.2, 2.4, 4.0],
    "feature_3": ["low", "medium", "low", "high", "medium", "high", "medium", "high"],
    "target": [0, 0, 0, 1, 0, 1, 1, 1]
})

AV = AutoViz_Class()

# Specify target variable for focused analysis
df_analyzed = AV.AutoViz(
    filename="",
    sep=",",
    depVar="target",  # Target variable for classification
    dfte=df_classification,
    header=0,
    verbose=2,  # More detailed output
    chart_format="svg"
)

# Regression dataset
df_regression = pd.DataFrame({
    "size": [1000, 1500, 1200, 2000, 1800, 2500, 2200, 3000],
    "bedrooms": [2, 3, 2, 4, 3, 4, 4, 5],
    "location": ["urban", "suburban", "urban", "rural", "suburban", "rural", "suburban", "rural"],
    "age": [5, 10, 3, 15, 8, 20, 12, 25],
    "price": [200000, 280000, 220000, 350000, 300000, 380000, 340000, 420000]
})

# Analyze with continuous target
df_analyzed = AV.AutoViz(
    filename="",
    sep=",",
    depVar="price",  # Continuous target
    dfte=df_regression,
    header=0,
    verbose=1,
    chart_format="png"
)
```

### 2. Chart Format and Output Options

**Different Chart Formats:**
```python
from autoviz import AutoViz_Class
import pandas as pd

df = pd.read_csv("data.csv")
AV = AutoViz_Class()

# SVG format (vector, scalable)
df_svg = AV.AutoViz(
    filename="",
    dfte=df,
    chart_format="svg",  # Scalable vector graphics
    verbose=1
)

# PNG format (raster, good for presentations)
df_png = AV.AutoViz(
    filename="",
    dfte=df,
    chart_format="png",  # PNG images
    verbose=1
)

# HTML format (interactive, for web)
df_html = AV.AutoViz(
    filename="",
    dfte=df,
    chart_format="html",  # Interactive HTML
    verbose=1
)

# Bokeh backend for interactive plots
df_bokeh = AV.AutoViz(
    filename="",
    dfte=df,
    chart_format="bokeh",  # Bokeh interactive
    verbose=1
)

# Server mode (for Jupyter notebooks)
df_server = AV.AutoViz(
    filename="",
    dfte=df,
    chart_format="server",  # Inline in notebook
    verbose=1
)
```

**Saving Charts to Directory:**
```python
from autoviz import AutoViz_Class
import pandas as pd
import os

# Create output directory
output_dir = "analysis_output"
os.makedirs(output_dir, exist_ok=True)

df = pd.read_csv("data.csv")
AV = AutoViz_Class()

# Save all charts to specified directory
df_analyzed = AV.AutoViz(
    filename="",
    dfte=df,
    chart_format="png",
    save_plot_dir=output_dir,  # Directory to save plots
    verbose=1
)

# List generated files
for file in os.listdir(output_dir):
    print(f"Generated: {file}")
```

### 3. Handling Large Datasets

**Sampling Strategies:**
```python
from autoviz import AutoViz_Class
import pandas as pd
import numpy as np

# Create large dataset
np.random.seed(42)
large_df = pd.DataFrame({
    "feature_" + str(i): np.random.randn(500000)
    for i in range(20)
})
large_df["category"] = np.random.choice(["A", "B", "C", "D"], 500000)
large_df["target"] = np.random.randint(0, 2, 500000)

print(f"Dataset size: {large_df.shape}")

AV = AutoViz_Class()

# Control sampling with max_rows_analyzed
df_analyzed = AV.AutoViz(
    filename="",
    dfte=large_df,
    max_rows_analyzed=100000,  # Sample 100K rows
    max_cols_analyzed=25,  # Limit columns analyzed
    verbose=1,
    chart_format="png"
)

# For very large datasets, use smaller sample
df_analyzed_small = AV.AutoViz(
    filename="",
    dfte=large_df,
    max_rows_analyzed=50000,  # Smaller sample for speed
    max_cols_analyzed=15,
    verbose=0,  # Minimal output
    chart_format="svg"
)
```

**Memory-Efficient Analysis:**
```python
from autoviz import AutoViz_Class
import pandas as pd

def analyze_large_file(file_path: str, sample_size: int = 100000) -> pd.DataFrame:
    """
    Analyze large files efficiently with sampling.

    Args:
        file_path: Path to CSV file
        sample_size: Number of rows to sample

    Returns:
        Analyzed DataFrame
    """
    # Read only a sample for initial analysis
    total_rows = sum(1 for _ in open(file_path)) - 1  # Exclude header

    if total_rows > sample_size:
        # Calculate skip probability
        skip_prob = 1 - (sample_size / total_rows)

        # Read with sampling
        df = pd.read_csv(
            file_path,
            skiprows=lambda i: i > 0 and np.random.random() < skip_prob
        )
    else:
        df = pd.read_csv(file_path)

    print(f"Sampled {len(df)} rows from {total_rows} total")

    AV = AutoViz_Class()
    return AV.AutoViz(
        filename="",
        dfte=df,
        verbose=1,
        chart_format="png"
    )

# Usage
# df_result = analyze_large_file("huge_dataset.csv", sample_size=75000)
```

### 4. Feature Analysis and Distribution Plots

**Understanding Feature Distributions:**
```python
from autoviz import AutoViz_Class
import pandas as pd
import numpy as np

# Create dataset with various distributions
np.random.seed(42)
df = pd.DataFrame({
    # Normal distribution
    "normal": np.random.normal(100, 15, 1000),

    # Skewed distribution
    "skewed": np.random.exponential(50, 1000),

    # Bimodal distribution
    "bimodal": np.concatenate([
        np.random.normal(30, 5, 500),
        np.random.normal(70, 5, 500)
    ]),

    # Uniform distribution
    "uniform": np.random.uniform(0, 100, 1000),

    # Categorical with different frequencies
    "category_balanced": np.random.choice(["A", "B", "C"], 1000),
    "category_imbalanced": np.random.choice(
        ["Common", "Rare", "Very Rare"],
        1000,
        p=[0.8, 0.15, 0.05]
    ),

    # Target variable
    "target": np.random.choice([0, 1], 1000, p=[0.7, 0.3])
})

AV = AutoViz_Class()

# AutoViz will automatically:
# 1. Detect distribution types
# 2. Create appropriate histograms
# 3. Show box plots for numerical features
# 4. Create bar charts for categorical features
# 5. Highlight potential outliers

df_analyzed = AV.AutoViz(
    filename="",
    dfte=df,
    depVar="target",
    verbose=2,
    chart_format="svg"
)
```

**Categorical Feature Analysis:**
```python
from autoviz import AutoViz_Class
import pandas as pd
import numpy as np

# Dataset with multiple categorical features
df = pd.DataFrame({
    "product_category": np.random.choice(
        ["Electronics", "Clothing", "Food", "Home", "Sports"],
        1000
    ),
    "customer_segment": np.random.choice(
        ["Premium", "Standard", "Budget"],
        1000,
        p=[0.2, 0.5, 0.3]
    ),
    "region": np.random.choice(
        ["North", "South", "East", "West"],
        1000
    ),
    "channel": np.random.choice(
        ["Online", "Store", "Mobile"],
        1000
    ),
    "revenue": np.random.exponential(500, 1000),
    "quantity": np.random.randint(1, 20, 1000)
})

AV = AutoViz_Class()

# AutoViz creates:
# - Bar charts for each categorical variable
# - Cross-tabulation visualizations
# - Category vs numerical variable plots

df_analyzed = AV.AutoViz(
    filename="",
    dfte=df,
    depVar="revenue",
    verbose=1,
    chart_format="png"
)
```

### 5. Correlation Detection

**Automatic Correlation Analysis:**
```python
from autoviz import AutoViz_Class
import pandas as pd
import numpy as np

# Create dataset with known correlations
np.random.seed(42)
n = 1000

# Base variables
x1 = np.random.randn(n)
x2 = np.random.randn(n)

df = pd.DataFrame({
    "x1": x1,
    "x2": x2,
    # Strongly correlated with x1
    "y1": x1 * 2 + np.random.randn(n) * 0.5,
    # Moderately correlated with x2
    "y2": x2 + np.random.randn(n) * 1.5,
    # Negatively correlated
    "y3": -x1 + np.random.randn(n) * 0.8,
    # No correlation
    "y4": np.random.randn(n),
    # Non-linear relationship
    "y5": x1 ** 2 + np.random.randn(n) * 0.5,
    # Target
    "target": (x1 + x2 > 0).astype(int)
})

AV = AutoViz_Class()

# AutoViz generates:
# 1. Correlation heatmap
# 2. Scatter plots for highly correlated pairs
# 3. Pair plots for feature relationships

df_analyzed = AV.AutoViz(
    filename="",
    dfte=df,
    depVar="target",
    verbose=2,
    chart_format="svg"
)
```

**Correlation with Lowess Smoothing:**
```python
from autoviz import AutoViz_Class
import pandas as pd
import numpy as np

# Dataset with non-linear relationships
np.random.seed(42)
x = np.linspace(0, 10, 500)

df = pd.DataFrame({
    "x": x,
    "linear": 2 * x + np.random.randn(500) * 2,
    "quadratic": x ** 2 + np.random.randn(500) * 5,
    "sinusoidal": 10 * np.sin(x) + np.random.randn(500) * 2,
    "logarithmic": 5 * np.log(x + 1) + np.random.randn(500),
    "target": x + np.random.randn(500)
})

AV = AutoViz_Class()

# Enable lowess smoothing to see trends
df_analyzed = AV.AutoViz(
    filename="",
    dfte=df,
    depVar="target",
    lowess=True,  # Enable lowess smoothing
    verbose=1,
    chart_format="png"
)
```

### 6. Outlier Detection and Highlighting

**Automatic Outlier Identification:**
```python
from autoviz import AutoViz_Class
import pandas as pd
import numpy as np

# Create dataset with outliers
np.random.seed(42)
n = 1000

# Normal data with injected outliers
revenue = np.concatenate([
    np.random.normal(1000, 200, n - 20),  # Normal values
    np.random.uniform(3000, 5000, 10),    # High outliers
    np.random.uniform(-500, 0, 10)        # Low outliers
])

units = np.concatenate([
    np.random.normal(50, 10, n - 15),
    np.random.uniform(150, 200, 15)       # Outliers
])

df = pd.DataFrame({
    "revenue": revenue,
    "units": units,
    "cost": np.abs(revenue * 0.6 + np.random.randn(n) * 100),
    "category": np.random.choice(["A", "B", "C"], n),
    "region": np.random.choice(["North", "South", "East", "West"], n)
})

AV = AutoViz_Class()

# AutoViz automatically:
# 1. Detects outliers using IQR method
# 2. Highlights them in box plots
# 3. Shows them in scatter plots
# 4. Reports outlier counts

df_analyzed = AV.AutoViz(
    filename="",
    dfte=df,
    verbose=2,
    chart_format="svg"
)
```

**Custom Outlier Analysis Wrapper:**
```python
from autoviz import AutoViz_Class
import pandas as pd
import numpy as np

def analyze_with_outlier_report(df: pd.DataFrame, target: str = "") -> dict:
    """
    Run AutoViz and provide detailed outlier report.

    Args:
        df: Input DataFrame
        target: Target variable name (optional)

    Returns:
        Dictionary with analysis results and outlier info
    """
    # Calculate outliers before visualization
    outlier_info = {}
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]

        outlier_info[col] = {
            "count": len(outliers),
            "percentage": len(outliers) / len(df) * 100,
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
            "min_outlier": outliers[col].min() if len(outliers) > 0 else None,
            "max_outlier": outliers[col].max() if len(outliers) > 0 else None
        }

    # Run AutoViz
    AV = AutoViz_Class()
    df_analyzed = AV.AutoViz(
        filename="",
        dfte=df,
        depVar=target,
        verbose=1,
        chart_format="png"
    )

    return {
        "analyzed_df": df_analyzed,
        "outlier_report": outlier_info,
        "total_outliers": sum(info["count"] for info in outlier_info.values())
    }

# Usage
# result = analyze_with_outlier_report(df, target="revenue")
# print(f"Total outliers found: {result['total_outliers']}")
```

### 7. Export to HTML and Notebooks

**HTML Report Generation:**
```python
from autoviz import AutoViz_Class
import pandas as pd
import os

def generate_html_report(
    df: pd.DataFrame,
    output_dir: str,
    report_name: str = "eda_report",
    target: str = ""
) -> str:
    """
    Generate comprehensive HTML report with AutoViz.

    Args:
        df: Input DataFrame
        output_dir: Directory for output files
        report_name: Name for the report
        target: Target variable (optional)

    Returns:
        Path to generated report
    """
    os.makedirs(output_dir, exist_ok=True)

    AV = AutoViz_Class()

    # Generate HTML charts
    df_analyzed = AV.AutoViz(
        filename="",
        dfte=df,
        depVar=target,
        chart_format="html",
        save_plot_dir=output_dir,
        verbose=1
    )

    # Create summary HTML
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{report_name} - AutoViz EDA Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #333; }}
            .summary {{ background: #f5f5f5; padding: 15px; border-radius: 5px; }}
            .chart-container {{ margin: 20px 0; }}
        </style>
    </head>
    <body>
        <h1>{report_name}</h1>

        <div class="summary">
            <h2>Dataset Summary</h2>
            <p>Rows: {len(df):,}</p>
            <p>Columns: {len(df.columns)}</p>
            <p>Numeric columns: {len(df.select_dtypes(include=['number']).columns)}</p>
            <p>Categorical columns: {len(df.select_dtypes(include=['object', 'category']).columns)}</p>
            <p>Target variable: {target if target else 'Not specified'}</p>
        </div>

        <h2>Column Information</h2>
        <table border="1" style="border-collapse: collapse;">
            <tr><th>Column</th><th>Type</th><th>Non-Null</th><th>Unique</th></tr>
    """

    for col in df.columns:
        html_content += f"""
            <tr>
                <td>{col}</td>
                <td>{df[col].dtype}</td>
                <td>{df[col].notna().sum()}</td>
                <td>{df[col].nunique()}</td>
            </tr>
        """

    html_content += """
        </table>

        <h2>Generated Charts</h2>
        <p>Charts have been saved to the output directory.</p>
    </body>
    </html>
    """

    report_path = os.path.join(output_dir, f"{report_name}.html")
    with open(report_path, "w") as f:
        f.write(html_content)

    return report_path

# Usage
# report_path = generate_html_report(df, "output/eda", "sales_analysis", "revenue")
# print(f"Report saved to: {report_path}")
```

**Jupyter Notebook Integration:**
```python
# In Jupyter Notebook
from autoviz import AutoViz_Class
import pandas as pd

# Load data
df = pd.read_csv("data.csv")

# Initialize AutoViz
AV = AutoViz_Class()

# Use 'server' format for inline display in notebooks
%matplotlib inline

df_analyzed = AV.AutoViz(
    filename="",
    dfte=df,
    depVar="target",
    chart_format="server",  # Display inline in notebook
    verbose=1
)

# Alternative: Use bokeh for interactive plots in notebooks
df_analyzed = AV.AutoViz(
    filename="",
    dfte=df,
    depVar="target",
    chart_format="bokeh",  # Interactive Bokeh plots
    verbose=1
)
```

**Export to Notebook File:**
```python
from autoviz import AutoViz_Class
import pandas as pd
import nbformat as nbf
import os

def create_eda_notebook(
    df: pd.DataFrame,
    output_path: str,
    dataset_name: str = "dataset"
) -> str:
    """
    Create a Jupyter notebook with AutoViz EDA.

    Args:
        df: Input DataFrame
        output_path: Path for output notebook
        dataset_name: Name for the dataset

    Returns:
        Path to created notebook
    """
    nb = nbf.v4.new_notebook()

    cells = [
        nbf.v4.new_markdown_cell(f"# Exploratory Data Analysis: {dataset_name}"),

        nbf.v4.new_code_cell("""
from autoviz import AutoViz_Class
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
"""),

        nbf.v4.new_markdown_cell("## Load Data"),

        nbf.v4.new_code_cell(f"""
# Data is pre-loaded
df = pd.read_csv("{dataset_name}.csv")  # Update path as needed
print(f"Dataset shape: {{df.shape}}")
df.head()
"""),

        nbf.v4.new_markdown_cell("## AutoViz Analysis"),

        nbf.v4.new_code_cell("""
AV = AutoViz_Class()

df_analyzed = AV.AutoViz(
    filename="",
    dfte=df,
    chart_format="server",
    verbose=1
)
"""),

        nbf.v4.new_markdown_cell("## Summary Statistics"),

        nbf.v4.new_code_cell("""
df.describe()
"""),

        nbf.v4.new_markdown_cell("## Missing Values"),

        nbf.v4.new_code_cell("""
missing = df.isnull().sum()
missing[missing > 0].sort_values(ascending=False)
""")
    ]

    nb.cells = cells

    with open(output_path, "w") as f:
        nbf.write(nb, f)

    return output_path

# Usage
# notebook_path = create_eda_notebook(df, "eda_analysis.ipynb", "sales_data")
```

## Complete Examples

### Example 1: Sales Data EDA Pipeline

```python
from autoviz import AutoViz_Class
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def sales_eda_pipeline(
    data_path: str,
    output_dir: str,
    target_column: str = "revenue"
) -> dict:
    """
    Complete EDA pipeline for sales data using AutoViz.

    Args:
        data_path: Path to sales data CSV
        output_dir: Directory for output files
        target_column: Target variable for analysis

    Returns:
        Dictionary with analysis results
    """
    os.makedirs(output_dir, exist_ok=True)

    # Load data
    print("Loading data...")
    df = pd.read_csv(data_path)

    # Basic data info
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")

    # Data type summary
    dtype_summary = df.dtypes.value_counts()
    print(f"\nData types:\n{dtype_summary}")

    # Missing values
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_df = pd.DataFrame({
        "missing_count": missing,
        "missing_pct": missing_pct
    })
    missing_df = missing_df[missing_df["missing_count"] > 0]

    if len(missing_df) > 0:
        print(f"\nMissing values:\n{missing_df}")
    else:
        print("\nNo missing values found")

    # Run AutoViz
    print("\nRunning AutoViz analysis...")
    AV = AutoViz_Class()

    df_analyzed = AV.AutoViz(
        filename="",
        dfte=df,
        depVar=target_column if target_column in df.columns else "",
        chart_format="png",
        save_plot_dir=output_dir,
        max_rows_analyzed=100000,
        verbose=1
    )

    # Calculate additional statistics
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    stats = {
        "shape": df.shape,
        "memory_mb": df.memory_usage(deep=True).sum() / 1024**2,
        "missing_values": missing.sum(),
        "numeric_columns": len(numeric_cols),
        "categorical_columns": len(df.columns) - len(numeric_cols)
    }

    if target_column in df.columns:
        target_stats = df[target_column].describe().to_dict()
        stats["target_stats"] = target_stats

    # Save summary
    summary_path = os.path.join(output_dir, "eda_summary.txt")
    with open(summary_path, "w") as f:
        f.write(f"EDA Summary - {datetime.now()}\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Dataset: {data_path}\n")
        f.write(f"Shape: {df.shape}\n")
        f.write(f"Memory: {stats['memory_mb']:.2f} MB\n\n")
        f.write("Columns:\n")
        for col in df.columns:
            f.write(f"  - {col}: {df[col].dtype}\n")

    print(f"\nAnalysis complete! Results saved to: {output_dir}")

    return {
        "dataframe": df_analyzed,
        "statistics": stats,
        "output_dir": output_dir
    }

# Generate sample data for testing
def generate_sample_sales_data(n_rows: int = 10000) -> pd.DataFrame:
    """Generate sample sales data for testing."""
    np.random.seed(42)

    dates = pd.date_range(
        start="2024-01-01",
        end="2025-12-31",
        periods=n_rows
    )

    return pd.DataFrame({
        "date": dates,
        "product_id": np.random.randint(1000, 9999, n_rows),
        "category": np.random.choice(
            ["Electronics", "Clothing", "Food", "Home", "Sports"],
            n_rows
        ),
        "region": np.random.choice(
            ["North", "South", "East", "West"],
            n_rows
        ),
        "revenue": np.random.exponential(500, n_rows),
        "units": np.random.randint(1, 50, n_rows),
        "cost": np.random.exponential(300, n_rows),
        "customer_age": np.random.normal(40, 15, n_rows).astype(int),
        "is_promotion": np.random.choice([0, 1], n_rows, p=[0.7, 0.3])
    })

# Usage
# sample_df = generate_sample_sales_data(10000)
# sample_df.to_csv("sample_sales.csv", index=False)
# results = sales_eda_pipeline("sample_sales.csv", "sales_eda_output", "revenue")
```

### Example 2: Machine Learning Feature Analysis

```python
from autoviz import AutoViz_Class
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification, make_regression
import os

def ml_feature_analysis(
    X: pd.DataFrame,
    y: pd.Series,
    task_type: str = "classification",
    output_dir: str = "ml_eda"
) -> dict:
    """
    Analyze features for machine learning using AutoViz.

    Args:
        X: Feature DataFrame
        y: Target Series
        task_type: 'classification' or 'regression'
        output_dir: Output directory

    Returns:
        Analysis results dictionary
    """
    os.makedirs(output_dir, exist_ok=True)

    # Combine features and target
    df = X.copy()
    df["target"] = y

    print(f"Feature Analysis for {task_type}")
    print(f"Features: {len(X.columns)}")
    print(f"Samples: {len(X)}")

    # Feature statistics
    feature_stats = []
    for col in X.columns:
        stats = {
            "feature": col,
            "dtype": str(X[col].dtype),
            "missing": X[col].isnull().sum(),
            "unique": X[col].nunique(),
            "mean": X[col].mean() if np.issubdtype(X[col].dtype, np.number) else None,
            "std": X[col].std() if np.issubdtype(X[col].dtype, np.number) else None
        }
        feature_stats.append(stats)

    feature_stats_df = pd.DataFrame(feature_stats)

    # Run AutoViz
    AV = AutoViz_Class()

    df_analyzed = AV.AutoViz(
        filename="",
        dfte=df,
        depVar="target",
        chart_format="png",
        save_plot_dir=output_dir,
        verbose=2
    )

    # Calculate feature correlations with target
    numeric_cols = X.select_dtypes(include=[np.number]).columns
    correlations = {}

    for col in numeric_cols:
        corr = df[col].corr(df["target"])
        correlations[col] = corr

    corr_df = pd.DataFrame.from_dict(
        correlations, orient="index", columns=["correlation"]
    ).sort_values("correlation", key=abs, ascending=False)

    # Save feature importance summary
    corr_df.to_csv(os.path.join(output_dir, "feature_correlations.csv"))
    feature_stats_df.to_csv(os.path.join(output_dir, "feature_statistics.csv"))

    print(f"\nTop correlated features:")
    print(corr_df.head(10))

    return {
        "analyzed_df": df_analyzed,
        "feature_stats": feature_stats_df,
        "correlations": corr_df,
        "output_dir": output_dir
    }

# Generate classification dataset
def create_classification_dataset(n_samples: int = 5000) -> tuple:
    """Create sample classification dataset."""
    X, y = make_classification(
        n_samples=n_samples,
        n_features=15,
        n_informative=8,
        n_redundant=3,
        n_classes=2,
        random_state=42
    )

    feature_names = [f"feature_{i}" for i in range(X.shape[1])]
    X_df = pd.DataFrame(X, columns=feature_names)

    # Add categorical features
    X_df["category_1"] = np.random.choice(["A", "B", "C"], n_samples)
    X_df["category_2"] = np.random.choice(["Low", "Medium", "High"], n_samples)

    y_series = pd.Series(y, name="target")

    return X_df, y_series

# Generate regression dataset
def create_regression_dataset(n_samples: int = 5000) -> tuple:
    """Create sample regression dataset."""
    X, y = make_regression(
        n_samples=n_samples,
        n_features=12,
        n_informative=6,
        noise=10,
        random_state=42
    )

    feature_names = [f"feature_{i}" for i in range(X.shape[1])]
    X_df = pd.DataFrame(X, columns=feature_names)

    # Add categorical features
    X_df["region"] = np.random.choice(["North", "South", "East", "West"], n_samples)
    X_df["segment"] = np.random.choice(["Premium", "Standard", "Budget"], n_samples)

    y_series = pd.Series(y, name="target")

    return X_df, y_series

# Usage
# X, y = create_classification_dataset(5000)
# results = ml_feature_analysis(X, y, "classification", "classification_eda")

# X, y = create_regression_dataset(5000)
# results = ml_feature_analysis(X, y, "regression", "regression_eda")
```

### Example 3: Multi-Dataset Comparison

```python
from autoviz import AutoViz_Class
import pandas as pd
import numpy as np
import os
from datetime import datetime

def compare_datasets(
    datasets: dict,
    output_dir: str = "comparison_output"
) -> dict:
    """
    Compare multiple datasets using AutoViz.

    Args:
        datasets: Dictionary of {name: DataFrame}
        output_dir: Output directory

    Returns:
        Comparison results
    """
    os.makedirs(output_dir, exist_ok=True)

    comparison_results = {}
    AV = AutoViz_Class()

    for name, df in datasets.items():
        print(f"\n{'='*50}")
        print(f"Analyzing: {name}")
        print(f"{'='*50}")

        # Create dataset-specific output directory
        dataset_dir = os.path.join(output_dir, name.replace(" ", "_"))
        os.makedirs(dataset_dir, exist_ok=True)

        # Run AutoViz
        df_analyzed = AV.AutoViz(
            filename="",
            dfte=df,
            chart_format="png",
            save_plot_dir=dataset_dir,
            verbose=1
        )

        # Collect statistics
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        stats = {
            "rows": len(df),
            "columns": len(df.columns),
            "numeric_columns": len(numeric_cols),
            "categorical_columns": len(df.columns) - len(numeric_cols),
            "missing_values": df.isnull().sum().sum(),
            "memory_mb": df.memory_usage(deep=True).sum() / 1024**2
        }

        # Numeric column statistics
        if len(numeric_cols) > 0:
            stats["numeric_summary"] = df[numeric_cols].describe().to_dict()

        comparison_results[name] = {
            "stats": stats,
            "output_dir": dataset_dir
        }

    # Create comparison summary
    summary_data = []
    for name, result in comparison_results.items():
        row = {"dataset": name}
        row.update(result["stats"])
        summary_data.append(row)

    summary_df = pd.DataFrame(summary_data)
    summary_path = os.path.join(output_dir, "comparison_summary.csv")
    summary_df.to_csv(summary_path, index=False)

    print(f"\n{'='*50}")
    print("Comparison Summary")
    print(f"{'='*50}")
    print(summary_df[["dataset", "rows", "columns", "missing_values", "memory_mb"]])

    return {
        "results": comparison_results,
        "summary": summary_df,
        "output_dir": output_dir
    }

# Create sample datasets for comparison
def create_comparison_datasets() -> dict:
    """Create multiple datasets for comparison."""
    np.random.seed(42)

    # Dataset 1: Sales Q1
    df_q1 = pd.DataFrame({
        "revenue": np.random.exponential(1000, 5000),
        "units": np.random.randint(1, 100, 5000),
        "category": np.random.choice(["A", "B", "C"], 5000),
        "region": np.random.choice(["North", "South"], 5000),
        "month": np.random.choice(["Jan", "Feb", "Mar"], 5000)
    })

    # Dataset 2: Sales Q2 (different distribution)
    df_q2 = pd.DataFrame({
        "revenue": np.random.exponential(1200, 6000),  # Higher revenue
        "units": np.random.randint(5, 120, 6000),      # More units
        "category": np.random.choice(["A", "B", "C", "D"], 6000),  # New category
        "region": np.random.choice(["North", "South", "East"], 6000),
        "month": np.random.choice(["Apr", "May", "Jun"], 6000)
    })

    # Dataset 3: Customer data
    df_customers = pd.DataFrame({
        "age": np.random.normal(40, 15, 3000).astype(int),
        "income": np.random.exponential(50000, 3000),
        "tenure_months": np.random.randint(1, 120, 3000),
        "segment": np.random.choice(["Premium", "Standard", "Budget"], 3000),
        "is_active": np.random.choice([0, 1], 3000, p=[0.2, 0.8])
    })

    return {
        "Sales Q1": df_q1,
        "Sales Q2": df_q2,
        "Customer Data": df_customers
    }

# Usage
# datasets = create_comparison_datasets()
# comparison = compare_datasets(datasets, "multi_dataset_comparison")
```

## Integration Examples

### AutoViz with Streamlit

```python
import streamlit as st
from autoviz import AutoViz_Class
import pandas as pd
import os
import tempfile

st.set_page_config(page_title="AutoViz EDA Tool", layout="wide")

st.title("AutoViz Exploratory Data Analysis")

# File upload
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Data Preview")
    st.dataframe(df.head(100))

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Rows", f"{len(df):,}")
    with col2:
        st.metric("Columns", len(df.columns))

    # Target variable selection
    target = st.selectbox(
        "Select target variable (optional)",
        ["None"] + list(df.columns)
    )

    if st.button("Run AutoViz Analysis"):
        with st.spinner("Generating visualizations..."):
            # Create temp directory for outputs
            with tempfile.TemporaryDirectory() as tmpdir:
                AV = AutoViz_Class()

                df_analyzed = AV.AutoViz(
                    filename="",
                    dfte=df,
                    depVar="" if target == "None" else target,
                    chart_format="png",
                    save_plot_dir=tmpdir,
                    verbose=0
                )

                # Display generated charts
                st.subheader("Generated Visualizations")

                for file in os.listdir(tmpdir):
                    if file.endswith(".png"):
                        st.image(os.path.join(tmpdir, file))

        st.success("Analysis complete!")
```

### AutoViz with Polars

```python
from autoviz import AutoViz_Class
import polars as pl
import pandas as pd

def autoviz_polars(lf: pl.LazyFrame, target: str = "", **kwargs) -> pd.DataFrame:
    """
    Run AutoViz on Polars LazyFrame.

    Args:
        lf: Polars LazyFrame
        target: Target variable name
        **kwargs: Additional AutoViz parameters

    Returns:
        Analyzed DataFrame
    """
    # Collect LazyFrame to DataFrame, then convert to pandas
    df_polars = lf.collect()
    df_pandas = df_polars.to_pandas()

    AV = AutoViz_Class()

    return AV.AutoViz(
        filename="",
        dfte=df_pandas,
        depVar=target,
        **kwargs
    )

# Usage
# lf = pl.scan_csv("data.csv")
# df_analyzed = autoviz_polars(lf, target="revenue", chart_format="png")
```

## Best Practices

### 1. Sample Large Datasets

```python
# GOOD: Use sampling for initial exploration
AV.AutoViz(
    filename="",
    dfte=large_df,
    max_rows_analyzed=50000,  # Sample for speed
    verbose=1
)

# AVOID: Analyzing millions of rows directly
# This will be slow and may crash
```

### 2. Specify Target Variable When Available

```python
# GOOD: Specify target for focused analysis
AV.AutoViz(
    filename="",
    dfte=df,
    depVar="target_column",  # Enables target-specific charts
    verbose=1
)

# LESS USEFUL: No target specified
# Still works but misses target-related insights
```

### 3. Choose Appropriate Chart Format

```python
# For presentations: PNG
chart_format="png"

# For reports/web: HTML
chart_format="html"

# For notebooks: server or bokeh
chart_format="server"

# For scalable graphics: SVG
chart_format="svg"
```

### 4. Organize Output

```python
# GOOD: Save to organized directory
import os
output_dir = f"eda_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
os.makedirs(output_dir, exist_ok=True)

AV.AutoViz(
    filename="",
    dfte=df,
    save_plot_dir=output_dir,
    chart_format="png"
)
```

## Troubleshooting

### Common Issues

**Issue: Charts not displaying in Jupyter**
```python
# Solution: Use server format
%matplotlib inline
AV.AutoViz(filename="", dfte=df, chart_format="server")
```

**Issue: Memory error with large dataset**
```python
# Solution: Reduce sample size
AV.AutoViz(
    filename="",
    dfte=df,
    max_rows_analyzed=25000,  # Reduce sample
    max_cols_analyzed=15      # Limit columns
)
```

**Issue: Too many charts generated**
```python
# Solution: Limit columns analyzed
df_subset = df[["col1", "col2", "col3", "target"]]
AV.AutoViz(filename="", dfte=df_subset)
```

**Issue: Categorical columns not recognized**
```python
# Solution: Convert to proper dtype
df["category"] = df["category"].astype("category")
AV.AutoViz(filename="", dfte=df)
```

**Issue: Date columns causing issues**
```python
# Solution: Convert to datetime or extract features
df["date"] = pd.to_datetime(df["date"])
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df_features = df.drop(columns=["date"])
AV.AutoViz(filename="", dfte=df_features)
```

## Version History

- **1.0.0** (2026-01-17): Initial release
  - Basic one-line EDA functionality
  - Chart format options (png, svg, html, bokeh, server)
  - Large dataset handling with sampling
  - Feature distribution analysis
  - Correlation detection
  - Outlier identification
  - HTML and notebook export
  - Complete pipeline examples
  - Integration with Streamlit and Polars
  - Best practices and troubleshooting

## Resources

- **Official Documentation**: https://github.com/AutoViML/AutoViz
- **PyPI**: https://pypi.org/project/autoviz/
- **Tutorial**: https://towardsdatascience.com/autoviz-a-new-tool-for-automated-visualization-ec9c1744a6ad
- **Examples**: https://github.com/AutoViML/AutoViz/tree/master/examples

---

**Automate your exploratory data analysis with AutoViz - one line of code, comprehensive insights!**
