---
name: td-data-profiling
description: Comprehensive data profiling and quality assessment using Teradata ClearScape Analytics descriptive statistics functions
---

# Teradata Data Profiling and Quality Analytics

| **Skill Name** | Teradata Data Profiling and Quality Analytics |
|----------------|--------------|
| **Description** | Comprehensive data profiling and quality assessment using Teradata ClearScape Analytics descriptive statistics functions |
| **Category** | Data Quality & Profiling |
| **Functions** | TD_UnivariateStatistics, TD_Frequency, TD_Histogram, TD_ColumnSummary, TD_Correlation |

## Core Capabilities

- **Complete data profiling workflow** from basic statistics to advanced quality metrics
- **Automated descriptive statistics** using Teradata ClearScape Analytics functions
- **Comprehensive data quality assessment** with actionable insights
- **Column-level profiling** for both numeric and categorical variables
- **Distribution analysis** including quartiles, percentiles, skewness, and kurtosis
- **Missing value detection** and completeness metrics
- **Outlier identification** using statistical methods (IQR, Z-score)
- **Correlation analysis** for numeric features
- **Frequency distributions** for categorical variables
- **Data type validation** and consistency checks
- **Business-ready reports** with quality scores and recommendations

## Data Profiling Workflow

This skill automatically analyzes your provided table to generate comprehensive data profiling reports using Teradata's descriptive statistics functions.

### 1. Table Discovery and Metadata Analysis
- **Schema Detection**: Automatically retrieves table structure and column definitions
- **Data Type Classification**: Identifies numeric, categorical, date/time, and text columns
- **Column Count and Names**: Catalogs all available columns for profiling
- **Table Size Assessment**: Determines row count and storage characteristics
- **Primary Key Detection**: Identifies unique identifiers and key columns

### 2. Univariate Statistics (Numeric Columns)
Using **TD_UnivariateStatistics** and native SQL functions:
- **Central Tendency**: Mean, Median, Mode
- **Dispersion**: Standard Deviation, Variance, Range, IQR
- **Distribution Shape**: Skewness, Kurtosis
- **Position Measures**: Minimum, Maximum, Quartiles (Q1, Q2, Q3)
- **Percentiles**: 1st, 5th, 10th, 25th, 50th, 75th, 90th, 95th, 99th
- **Count Statistics**: Total count, Non-null count, Null count, Distinct count
- **Coefficient of Variation**: Relative variability measure

### 3. Categorical Variable Profiling
Using **TD_Frequency** and aggregation functions:
- **Cardinality**: Count of unique/distinct values
- **Frequency Distribution**: Value counts and percentages
- **Mode Detection**: Most common values (Top 10)
- **Rare Value Detection**: Values with frequency < 1%
- **Missing Values**: Null count and percentage
- **Entropy Calculation**: Measure of information content
- **Category Balance**: Distribution uniformity assessment

### 4. Distribution Analysis
Using **TD_Histogram** and statistical functions:
- **Histogram Generation**: Bin-based distribution visualization data
- **Distribution Type Detection**: Normal, Skewed, Bimodal, Uniform
- **Normality Assessment**: Statistical tests and indicators
- **Outlier Detection**: IQR method, Z-score method, Modified Z-score
- **Density Estimation**: Value concentration patterns

### 5. Data Quality Metrics
- **Completeness**: Percentage of non-null values per column
- **Uniqueness**: Distinct value ratio and duplicate detection
- **Validity**: Data type conformance and range validation
- **Consistency**: Pattern matching and format validation
- **Accuracy Indicators**: Statistical anomaly detection
- **Quality Score**: Overall column quality rating (0-100)

### 6. Correlation Analysis (Numeric Columns)
Using **TD_Correlation** and correlation functions:
- **Pearson Correlation**: Linear relationship strength
- **Correlation Matrix**: All numeric column pairs
- **Highly Correlated Pairs**: |correlation| > 0.7
- **Multicollinearity Detection**: VIF (Variance Inflation Factor) indicators

### 7. Missing Value Analysis
- **Column-level Missing Patterns**: Per-column null statistics
- **Missing Value Heatmap Data**: Row-wise missing patterns
- **Completeness Score**: Overall data completeness percentage
- **Missing Value Recommendations**: Imputation strategy suggestions

### 8. Outlier Detection and Analysis
- **IQR Method**: Q1 - 1.5*IQR and Q3 + 1.5*IQR boundaries
- **Z-Score Method**: Values beyond ±3 standard deviations
- **Modified Z-Score**: Median-based robust outlier detection
- **Outlier Count and Percentage**: Per-column outlier statistics
- **Outlier Impact Assessment**: Influence on mean and standard deviation

## How to Use This Skill

1. **Provide Your Table Information**:
   ```
   "Profile table: database_name.table_name"
   or
   "Analyze data quality for: my_customer_data"
   or
   "Generate comprehensive profiling report for: sales_database.transactions_table"
   ```

2. **The Skill Will**:
   - Automatically detect all columns and their data types
   - Execute comprehensive profiling across all applicable columns
   - Generate descriptive statistics using Teradata ClearScape Analytics functions
   - Produce data quality scores and recommendations
   - Create detailed profiling reports with actionable insights

3. **Example Requests**:
   ```
   "Profile my table: retail_db.customer_transactions"
   "Generate data quality report for: analytics.sales_data"
   "Analyze the data distribution in: warehouse.product_inventory"
   "Check data quality and completeness for: marketing.customer_profiles"
   ```

## Skill Instructions for Table Profiling

When a user provides a table name, follow this comprehensive workflow:

### Step 1: Table Discovery
```sql
-- Get table metadata and structure
SHOW COLUMNS FROM {user_database}.{user_table};

-- Get table statistics
SELECT
    DatabaseName,
    TableName,
    CreateTimeStamp,
    LastAlterTimeStamp
FROM DBC.TablesV
WHERE DatabaseName = '{user_database}'
  AND TableName = '{user_table}';

-- Get row count and basic metrics
SELECT COUNT(*) as total_rows
FROM {user_database}.{user_table};
```

### Step 2: Column Classification
Automatically classify columns into:
- **Numeric Columns**: INTEGER, BIGINT, DECIMAL, FLOAT, NUMBER types
- **Categorical Columns**: CHAR, VARCHAR with moderate cardinality (< 50 distinct values)
- **Date/Time Columns**: DATE, TIMESTAMP, TIME types
- **Text Columns**: VARCHAR, CLOB with high cardinality (free text)
- **Boolean Columns**: Binary or Yes/No type fields

### Step 3: Execute Profiling Workflow
Run comprehensive profiling scripts in sequence:
1. **basic_profiling.sql** - Row counts, column counts, basic metrics
2. **numeric_profiling.sql** - Univariate statistics for all numeric columns
3. **categorical_profiling.sql** - Frequency analysis for categorical columns
4. **distribution_analysis.sql** - Histogram and distribution characteristics
5. **quality_assessment.sql** - Missing values, outliers, consistency checks
6. **correlation_analysis.sql** - Correlation matrix for numeric columns
7. **comprehensive_report.sql** - Consolidated profiling report

### Step 4: Generate Quality Report
Produce a comprehensive report including:
- **Executive Summary**: High-level data quality scores
- **Column Profiles**: Detailed statistics per column
- **Data Quality Issues**: Identified problems and recommendations
- **Distribution Insights**: Statistical characteristics of data
- **Correlation Insights**: Relationships between variables
- **Action Items**: Prioritized data quality improvements

## Input Requirements

### Data Requirements
- **Source table**: Any Teradata table with data to profile
- **Column variety**: Support for numeric, categorical, date, and text columns
- **Minimum sample size**: At least 10 rows for meaningful statistics (100+ recommended)
- **Table access**: READ permission on the target table

### Technical Requirements
- **Teradata Vantage** with ClearScape Analytics enabled
- **Database permissions**: SELECT on target database/table
- **Function access**: TD_UnivariateStatistics, TD_Frequency, TD_Histogram, TD_ColumnSummary, TD_Correlation
- **Temporary table space**: For intermediate profiling results

## Output Formats

### Generated Reports
- **Comprehensive Profiling Report**: Multi-section detailed analysis
- **Data Quality Dashboard Data**: Metrics suitable for visualization
- **Column-Level Statistics**: Individual column profiles
- **Distribution Visualizations**: Histogram data and box plot statistics
- **Correlation Matrices**: Numeric column relationships
- **Quality Score Cards**: Overall and per-column quality ratings

### Profiling Tables Created
- **{table_name}_profile_numeric**: Numeric column statistics
- **{table_name}_profile_categorical**: Categorical column frequencies
- **{table_name}_profile_quality**: Data quality metrics
- **{table_name}_profile_outliers**: Identified outlier records
- **{table_name}_profile_correlation**: Correlation matrix
- **{table_name}_profile_summary**: Executive summary report

### SQL Scripts Generated
- **Complete profiling workflow** customized for your table structure
- **Parameterized queries** using actual column names from your table
- **Ready-to-execute SQL** with proper error handling
- **Cleanup procedures** for temporary objects

## Data Profiling Use Cases Supported

1. **Initial Data Discovery**: Understanding new datasets before analysis
2. **Data Quality Assessment**: Identifying issues before ETL or modeling
3. **Data Migration Validation**: Comparing source and target data characteristics
4. **Ongoing Data Monitoring**: Tracking data quality over time
5. **Feature Engineering Guidance**: Identifying transformation needs for ML
6. **Reporting and Documentation**: Generating data dictionaries and profiles
7. **Compliance and Auditing**: Documenting data characteristics for regulations
8. **Data Cleansing Planning**: Prioritizing data quality improvement efforts

## Descriptive Statistics Functions Used

### TD_UnivariateStatistics
- Comprehensive univariate analysis for numeric columns
- Generates mean, median, mode, std dev, variance, quartiles
- Calculates skewness and kurtosis for distribution shape
- Provides count statistics including nulls and distinct values

### TD_Frequency
- Frequency distribution analysis for categorical variables
- Identifies most common and rare values
- Calculates value percentages and cumulative frequencies
- Supports grouped frequency analysis

### TD_Histogram
- Creates histogram bins for numeric distributions
- Configurable bin count and width
- Generates frequency counts per bin
- Supports equal-width and equal-frequency binning

### TD_ColumnSummary
- Quick summary statistics across multiple columns
- Identifies data types and null percentages
- Calculates basic statistics (min, max, mean)
- Provides overview of table characteristics

### TD_Correlation
- Pearson correlation coefficient calculation
- Correlation matrix generation for multiple columns
- Identifies linear relationships between variables
- Supports partial correlation analysis

## Best Practices Applied

- **Comprehensive Coverage**: Profile all relevant columns automatically
- **Performance Optimization**: Efficient queries for large datasets
- **Statistical Rigor**: Use industry-standard statistical methods
- **Actionable Insights**: Provide recommendations, not just numbers
- **Business Context**: Interpret statistics in business terms
- **Quality Scoring**: Quantify data quality for tracking and comparison
- **Documentation**: Clear explanations of all metrics and findings
- **Scalability**: Handle tables from small to very large efficiently
- **Error Handling**: Graceful handling of edge cases and data issues
- **Reproducibility**: Consistent results for repeated profiling

## Example Usage

```sql
-- Example: Comprehensive Data Profiling Workflow
-- Replace 'your_table' with actual table name

-- 1. Initial table discovery
SELECT COUNT(*) as row_count,
       COUNT(DISTINCT customer_id) as unique_customers
FROM your_database.your_table;

-- 2. Numeric column profiling using TD_UnivariateStatistics
SELECT * FROM TD_UnivariateStatistics(
    ON your_database.your_table
    USING
    TargetColumns('age', 'income', 'purchase_amount', 'credit_score')
) AS dt;

-- 3. Categorical column profiling using TD_Frequency
SELECT * FROM TD_Frequency(
    ON your_database.your_table
    USING
    TargetColumns('customer_segment', 'region', 'product_category')
    TopK(10)
) AS dt;

-- 4. Distribution analysis using TD_Histogram
SELECT * FROM TD_Histogram(
    ON your_database.your_table
    USING
    TargetColumn('purchase_amount')
    NumBins(20)
) AS dt;

-- 5. Correlation analysis using TD_Correlation
SELECT * FROM TD_Correlation(
    ON your_database.your_table
    USING
    TargetColumns('age', 'income', 'purchase_amount', 'credit_score')
) AS dt;

-- (Detailed SQL provided by the skill)
```

## Scripts Included

### Core Profiling Scripts
- **`basic_profiling.sql`**: Table-level statistics and row counts
- **`numeric_profiling.sql`**: TD_UnivariateStatistics for numeric columns
- **`categorical_profiling.sql`**: TD_Frequency analysis for categorical columns
- **`distribution_analysis.sql`**: TD_Histogram and distribution metrics
- **`quality_assessment.sql`**: Missing values, duplicates, validity checks
- **`correlation_analysis.sql`**: TD_Correlation matrix for numeric features
- **`outlier_detection.sql`**: Multiple outlier detection methods
- **`comprehensive_report.sql`**: Consolidated profiling report generation

### Utility Scripts
- **`table_discovery.sql`**: Metadata extraction and column classification
- **`data_quality_scoring.sql`**: Quality score calculation algorithms
- **`profiling_summary.sql`**: Executive summary generation
- **`cleanup.sql`**: Remove temporary profiling tables

### Advanced Analytics Scripts
- **`time_series_profiling.sql`**: Temporal data profiling for date columns
- **`text_profiling.sql`**: Text column analysis (length, patterns, uniqueness)
- **`pattern_detection.sql`**: Data pattern and format analysis
- **`comparison_profiling.sql`**: Compare profiles across tables or time periods

## Quality Metrics Defined

### Completeness Score (0-100)
- 100: No missing values in any column
- 90-99: < 10% missing values
- 70-89: 10-30% missing values
- < 70: > 30% missing values (requires attention)

### Uniqueness Score (0-100)
- Based on distinct value ratio
- 100: All values unique (potential key column)
- 50-99: Good variety
- < 50: Low variety or many duplicates

### Validity Score (0-100)
- Data type conformance
- Range validation (within expected bounds)
- Format consistency
- Business rule compliance

### Overall Quality Score (0-100)
- Weighted average of Completeness, Uniqueness, and Validity
- 90-100: Excellent quality
- 70-89: Good quality, minor issues
- 50-69: Fair quality, attention needed
- < 50: Poor quality, significant issues

## Profiling Report Structure

### 1. Executive Summary
- Total rows and columns
- Overall quality score
- Critical issues count
- Profiling timestamp

### 2. Numeric Column Profiles
Per column:
- Basic statistics (mean, median, std dev)
- Distribution characteristics
- Outlier count and percentage
- Missing value percentage
- Quality score

### 3. Categorical Column Profiles
Per column:
- Unique value count (cardinality)
- Top 10 most frequent values
- Rare value count (< 1% frequency)
- Missing value percentage
- Quality score

### 4. Data Quality Issues
- Missing value patterns
- Duplicate records
- Outliers by column
- Invalid values
- Consistency violations

### 5. Distribution Insights
- Distribution types identified
- Skewness and kurtosis interpretation
- Normality assessment
- Transformation recommendations

### 6. Correlation Insights
- Highly correlated pairs (|r| > 0.7)
- Potential multicollinearity
- Feature redundancy detection
- Relationship strength matrix

### 7. Recommendations
- Data cleansing priorities
- Feature engineering suggestions
- Data quality improvement actions
- Monitoring recommendations

## Limitations and Disclaimers

- **Sample Size**: Very small tables (< 10 rows) may produce unreliable statistics
- **Performance**: Large tables (> 100M rows) may require sampling for efficiency
- **Data Types**: Binary large objects (BLOBs) and complex types have limited profiling
- **Domain Knowledge**: Statistical findings require business context for proper interpretation
- **Dynamic Data**: Profiles are point-in-time snapshots; data may change
- **Function Availability**: Requires ClearScape Analytics functions to be enabled
- **Computational Resources**: Complex profiling may consume significant resources

## Quality Checks and Validations

### Automated Validations
- **Table Existence**: Verify table exists before profiling
- **Column Access**: Confirm SELECT permissions on all columns
- **Function Availability**: Check TD_ functions are accessible
- **Data Type Support**: Validate columns are profilable
- **Sample Size**: Ensure sufficient data for statistics

### Manual Review Points
- **Business Rule Validation**: Verify metrics align with domain expectations
- **Outlier Legitimacy**: Confirm outliers are errors vs. valid extreme values
- **Missing Value Causes**: Understand why data is missing (systemic vs. random)
- **Distribution Interpretation**: Contextualize statistical findings
- **Quality Threshold Setting**: Define acceptable quality levels per use case

## Updates and Maintenance

- **Version Compatibility**: Tested with Teradata Vantage 17.x and above
- **ClearScape Analytics**: Optimized for latest ClearScape Analytics features
- **Performance Tuning**: Regular query optimization for large-scale profiling
- **Best Practices**: Updated with industry standards and community feedback
- **Documentation**: Enhanced with real-world profiling examples and case studies
- **Function Updates**: Aligned with new Teradata descriptive statistics capabilities

## Integration with Analytics Workflows

This profiling skill integrates seamlessly with:
- **Data Preparation**: Inform cleaning and transformation strategies
- **Feature Engineering**: Guide feature creation and selection
- **Model Training**: Validate data before ML modeling (preprocessing for decision trees, regression, etc.)
- **Model Evaluation**: Compare training vs. production data distributions
- **Data Monitoring**: Track data quality degradation over time
- **Compliance Reporting**: Generate documentation for data governance

---

*This skill provides production-ready comprehensive data profiling and quality assessment using Teradata ClearScape Analytics with industry-leading statistical rigor and business-focused insights.*
