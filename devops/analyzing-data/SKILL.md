---
name: analyzing-data
description: Performs comprehensive data analysis including statistical analysis, visualization, pattern detection, and report generation. Use when the user asks to analyze data, find patterns, generate insights, create visualizations, or mentions data analysis, statistics, or data science tasks.
---

# Data Analyzer

This skill performs comprehensive data analysis with statistical methods, visualizations, and automated reporting.

## When to Use This Skill

Invoke this skill when the user:
- Asks to analyze a dataset
- Wants statistical insights
- Needs data visualization
- Requests pattern detection
- Mentions data analysis, statistics, or data science
- Wants to generate analysis reports

## Analysis Workflow

### Step 1: Data Understanding

**Initial Assessment:**
1. Identify data format (CSV, JSON, Excel, etc.)
2. Determine data size and structure
3. Understand business context
4. Clarify analysis objectives

**Use the analysis script:**
```bash
python scripts/analyze.py data.csv --explore
```

### Step 2: Data Quality Check

**Validation:**
- [ ] Data loads successfully
- [ ] Required columns present
- [ ] Data types appropriate
- [ ] Missing values identified
- [ ] Outliers detected
- [ ] Duplicates checked

**Quality Report:**
```bash
python scripts/analyze.py data.csv --quality-report
```

### Step 3: Statistical Analysis

Perform analysis based on data type and objectives.

**For Descriptive Statistics:**
- Mean, median, mode
- Standard deviation, variance
- Quartiles and ranges
- Distribution shape

**For Correlation Analysis:**
- Pearson correlation
- Spearman rank correlation
- Covariance matrix

**For Advanced Analysis:**
See REFERENCE.md for:
- Hypothesis testing procedures
- Regression analysis methods
- Time series analysis
- Clustering algorithms

### Step 4: Visualization

Create appropriate visualizations:

**Univariate Analysis:**
- Histograms for distributions
- Box plots for outliers
- Bar charts for categories

**Bivariate Analysis:**
- Scatter plots for relationships
- Line charts for trends
- Heatmaps for correlations

**Multivariate Analysis:**
- Pair plots
- 3D visualizations
- Dimensionality reduction plots

**Generate visualizations:**
```bash
python scripts/analyze.py data.csv --visualize --output-dir ./charts
```

### Step 5: Report Generation

Create analysis report using templates from FORMS.md:

```bash
cat FORMS.md  # View available report templates
python scripts/analyze.py data.csv --report executive-summary
```

## Analysis Types

### Pattern 1: Exploratory Data Analysis (EDA)

**Objective:** Understand data characteristics and relationships

**Steps:**
1. Load and preview data
2. Generate summary statistics
3. Check distributions
4. Identify correlations
5. Detect outliers
6. Document insights

**Quick EDA:**
```bash
python scripts/analyze.py data.csv --eda
```

### Pattern 2: Comparative Analysis

**Objective:** Compare groups or time periods

**Steps:**
1. Define groups/periods
2. Calculate group statistics
3. Test for significant differences
4. Visualize comparisons
5. Interpret results

See REFERENCE.md section "Statistical Testing" for test selection.

### Pattern 3: Trend Analysis

**Objective:** Identify patterns over time

**Steps:**
1. Prepare time series data
2. Check for seasonality
3. Calculate moving averages
4. Fit trend lines
5. Forecast future values

See REFERENCE.md section "Time Series Methods" for details.

### Pattern 4: Predictive Modeling

**Objective:** Build models to predict outcomes

**Steps:**
1. Feature engineering
2. Train/test split
3. Model selection
4. Training and validation
5. Performance evaluation

See REFERENCE.md section "Machine Learning" for model details.

## Data Type Handling

**Numerical Data:**
- Summary statistics
- Distribution analysis
- Correlation analysis
- Regression modeling

**Categorical Data:**
- Frequency tables
- Cross-tabulations
- Chi-square tests
- Category encoding

**Time Series Data:**
- Trend decomposition
- Seasonality detection
- Autocorrelation
- Forecasting

**Text Data:**
- Frequency analysis
- Sentiment analysis
- Topic modeling
- See REFERENCE.md section "Text Analytics"

## Common Issues and Solutions

**Issue: Missing Values**
- Strategy 1: Remove rows (if <5% missing)
- Strategy 2: Impute with mean/median/mode
- Strategy 3: Use advanced imputation (KNN, MICE)
- See REFERENCE.md section "Missing Data Handling"

**Issue: Outliers**
- Detection: IQR method, Z-score, isolation forest
- Action: Remove, cap, or transform
- Context: Business rules may define valid outliers

**Issue: Imbalanced Data**
- Resampling techniques
- Class weights
- Synthetic data generation (SMOTE)

**Issue: High Dimensionality**
- Feature selection
- PCA or t-SNE
- Domain knowledge filtering

## Output Formats

The skill can generate reports in multiple formats:

**Executive Summary:**
- Key findings (3-5 bullets)
- Critical metrics
- Recommendations
- See FORMS.md template "Executive Summary"

**Technical Report:**
- Methodology
- Detailed results
- Statistical tests
- Visualizations
- See FORMS.md template "Technical Report"

**Dashboard Format:**
- Interactive visualizations
- Key metrics at a glance
- Drill-down capability

**Generate specific format:**
```bash
python scripts/analyze.py data.csv --format executive
python scripts/analyze.py data.csv --format technical
python scripts/analyze.py data.csv --format dashboard
```

## Validation Checklist

Before finalizing analysis:

- [ ] Data quality verified
- [ ] Appropriate methods selected
- [ ] Assumptions validated
- [ ] Results interpreted correctly
- [ ] Visualizations clear and labeled
- [ ] Report matches requested format
- [ ] Recommendations actionable

## Analysis Scope

**Quick Analysis (5-10 min):**
- Basic statistics
- Simple visualizations
- Key findings only

**Standard Analysis (20-40 min):**
- Comprehensive statistics
- Multiple visualizations
- Correlation analysis
- Formatted report

**Deep Analysis (1-2 hours):**
- Advanced modeling
- Hypothesis testing
- Multiple methodologies
- Executive + technical reports

Ask user for preferred scope if unclear.

## Example Analysis

**Input:** sales_data.csv with columns: date, product, region, quantity, revenue

**Output:**

### Key Findings
1. Revenue increased 23% year-over-year
2. Product A accounts for 45% of total revenue
3. Western region shows strongest growth (31%)
4. Seasonal peak in Q4 (38% of annual sales)

### Statistical Summary
- Mean daily revenue: $12,450
- Median daily revenue: $11,200
- Standard deviation: $3,890
- 95% of days: $5,000 - $20,000

### Visualizations Generated
- Revenue trend line (2023-2024)
- Product revenue pie chart
- Regional comparison bar chart
- Seasonal pattern heatmap

### Recommendations
1. Increase inventory for Product A in Q4
2. Investigate Western region success factors
3. Plan marketing campaigns for Q2-Q3 (slower periods)

## Advanced Features

For complex scenarios, this skill integrates with:

**REFERENCE.md sections:**
- Statistical Methods Library
- Machine Learning Algorithms
- Time Series Techniques
- Text Analytics Methods

**FORMS.md templates:**
- Executive Summary Template
- Technical Report Template
- Dashboard Layout Template

**Scripts:**
- `scripts/analyze.py` - Main analysis engine
- `scripts/visualize.py` - Visualization generator
- `scripts/report.py` - Report formatter

## Getting Started

**Simple analysis:**
```bash
python scripts/analyze.py your_data.csv
```

**With options:**
```bash
python scripts/analyze.py your_data.csv \
  --explore \
  --visualize \
  --report executive \
  --output-dir ./results
```

**Help:**
```bash
python scripts/analyze.py --help
```

For detailed methodology and advanced techniques, see REFERENCE.md.
For report templates and output examples, see FORMS.md.
