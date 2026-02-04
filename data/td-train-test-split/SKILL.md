---
name: td-train-test-split
description: Data splitting for model validation using TD_TrainTestSplit
---

# Teradata Train-Test Split

| **Skill Name** | Teradata Train-Test Split |
|----------------|--------------|
| **Description** | Data splitting for model validation using TD_TrainTestSplit |
| **Category** | Preprocessing Analytics |
| **Function** | TD_TrainTestSplit |

## Core Capabilities

- **Complete analytical workflow** from data exploration to model deployment
- **Automated preprocessing** including scaling, encoding, and train-test splitting
- **Advanced TD_TrainTestSplit implementation** with parameter optimization
- **Comprehensive evaluation metrics** and model validation
- **Production-ready SQL generation** with proper table management
- **Error handling and data quality checks** throughout the pipeline
- **Business-focused interpretation** of analytical results

## Table Analysis Workflow

This skill automatically analyzes your provided table to generate optimized SQL workflows. Here's how it works:

### 1. Table Structure Analysis
- **Column Detection**: Automatically identifies all columns and their data types
- **Data Type Classification**: Distinguishes between numeric, categorical, and text columns
- **Primary Key Identification**: Detects unique identifier columns
- **Missing Value Assessment**: Analyzes data completeness

### 2. Feature Engineering Recommendations
- **Numeric Features**: Identifies columns suitable for scaling and normalization
- **Categorical Features**: Detects columns requiring encoding (one-hot, label encoding)
- **Target Variable**: Helps identify the dependent variable for modeling
- **Feature Selection**: Recommends relevant features based on data types

### 3. SQL Generation Process
- **Dynamic Column Lists**: Generates column lists based on your table structure
- **Parameterized Queries**: Creates flexible SQL templates using your table schema
- **Table Name Integration**: Replaces placeholders with your actual table names
- **Database Context**: Adapts to your database and schema naming conventions

## How to Use This Skill

1. **Provide Your Table Information**:
   ```
   "Analyze table: database_name.table_name"
   or
   "Use table: my_data with target column: target_var"
   ```

2. **The Skill Will**:
   - Query your table structure using `SHOW COLUMNS FROM table_name`
   - Analyze data types and suggest appropriate preprocessing
   - Generate complete SQL workflow with your specific column names
   - Provide optimized parameters based on your data characteristics

## Input Requirements

### Data Requirements
- **Source table**: Teradata table with analytical data
- **Target column**: Dependent variable for preprocessing analysis
- **Input data**: Properly formatted Teradata table
- **Column specifications**: Appropriate data types for analysis

### Technical Requirements
- **Teradata Vantage** with ClearScape Analytics enabled
- **Database permissions**: CREATE, DROP, SELECT on working database
- **Function access**: TD_TrainTestSplit

## Output Formats

### Generated Tables
- **Preprocessed data tables** with proper scaling and encoding
- **Train/test split tables** for model validation
- **Processed results** from TD_TrainTestSplit analysis
- **Summary statistics** and transformation parameters

### SQL Scripts
- **Complete workflow scripts** ready for execution
- **Parameterized queries** for different datasets
- **Table management** with proper cleanup procedures

## Preprocessing Use Cases Supported

1. **Model validation**: Comprehensive analysis workflow
2. **Data partitioning**: Comprehensive analysis workflow
3. **Cross-validation**: Comprehensive analysis workflow

## Best Practices Applied

- **Data validation** before analysis execution
- **Proper feature scaling** and categorical encoding
- **Train-test splitting** with stratification when appropriate
- **Cross-validation** for robust model evaluation
- **Parameter optimization** using systematic approaches
- **Residual analysis** and diagnostic checks
- **Business interpretation** of statistical results
- **Documentation** of methodology and assumptions

## Example Usage

```sql
-- Example workflow for Teradata Train-Test Split
-- Replace 'your_table' with actual table name

-- 1. Data exploration and validation
SELECT COUNT(*),
       COUNT(DISTINCT your_id_column),
       AVG(your_target_column),
       STDDEV(your_target_column)
FROM your_database.your_table;

-- 2. Execute complete preprocessing workflow
-- (Detailed SQL provided by the skill)
```

## Scripts Included

### Core Analytics Scripts
- **`preprocessing.sql`**: Data preparation and feature engineering
- **`table_analysis.sql`**: Automatic table structure analysis
- **`complete_workflow_template.sql`**: End-to-end workflow template
- **`evaluation.sql`**: Model validation and metrics calculation

### Utility Scripts
- **`data_quality_checks.sql`**: Comprehensive data validation
- **`parameter_tuning.sql`**: Systematic parameter optimization
- **`diagnostic_queries.sql`**: Model diagnostics and interpretation

## Limitations and Disclaimers

- **Data quality**: Results depend on input data quality and completeness
- **Sample size**: Minimum sample size requirements for reliable results
- **Feature selection**: Manual feature engineering may be required
- **Computational resources**: Large datasets may require optimization
- **Business context**: Statistical results require domain expertise for interpretation
- **Model assumptions**: Understand underlying mathematical assumptions

## Quality Checks

### Automated Validations
- **Data completeness** verification before analysis
- **Statistical assumptions** testing where applicable
- **Model convergence** monitoring during training
- **Prediction quality** assessment using validation data
- **Performance metrics** calculation and interpretation

### Manual Review Points
- **Feature selection** appropriateness for business problem
- **Model interpretation** alignment with domain knowledge
- **Results validation** against business expectations
- **Documentation** completeness for reproducibility

## Updates and Maintenance

- **Version compatibility**: Tested with latest Teradata Vantage releases
- **Performance optimization**: Regular query performance reviews
- **Best practices**: Updated based on analytics community feedback
- **Documentation**: Maintained with latest ClearScape Analytics features
- **Examples**: Updated with real-world use cases and scenarios

---

*This skill provides production-ready preprocessing analytics using Teradata ClearScape Analytics TD_TrainTestSplit with comprehensive data science best practices.*
