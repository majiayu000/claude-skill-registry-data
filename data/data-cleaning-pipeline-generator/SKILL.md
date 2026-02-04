---
name: data-cleaning-pipeline-generator
description: Generates data cleaning pipelines for pandas/polars with handling for missing values, duplicates, outliers, type conversions, and data validation. Use when user asks to "clean data", "generate data pipeline", "handle missing values", or "remove duplicates from dataset".
allowed-tools: [Write, Read, Bash]
---

# Data Cleaning Pipeline Generator

Generates comprehensive data cleaning and preprocessing pipelines using pandas, polars, or PySpark with best practices for handling messy data.

## When to Use

- "Clean my dataset"
- "Generate data cleaning pipeline"
- "Handle missing values"
- "Remove duplicates"
- "Fix data types"
- "Detect and remove outliers"

## Instructions

### 1. Analyze Dataset

```python
import pandas as pd

# Load data
df = pd.read_csv('data.csv')

# Basic info
print(df.info())
print(df.describe())
print(df.head())

# Check for issues
print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicates:")
print(f"Total duplicates: {df.duplicated().sum()}")

print("\nData types:")
print(df.dtypes)
```

### 2. Generate Pandas Cleaning Pipeline

**Complete Pipeline:**
```python
import pandas as pd
import numpy as np
from datetime import datetime

class DataCleaningPipeline:
    """Data cleaning pipeline for pandas DataFrames."""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.original_shape = df.shape
        self.cleaning_log = []

    def log(self, message: str):
        """Log cleaning steps."""
        self.cleaning_log.append(f"[{datetime.now()}] {message}")
        print(message)

    def remove_duplicates(self, subset=None, keep='first'):
        """Remove duplicate rows."""
        before = len(self.df)
        self.df = self.df.drop_duplicates(subset=subset, keep=keep)
        removed = before - len(self.df)
        self.log(f"Removed {removed} duplicate rows")
        return self

    def handle_missing_values(self, strategy='auto'):
        """Handle missing values based on strategy."""
        missing = self.df.isnull().sum()
        columns_with_missing = missing[missing > 0]

        for col in columns_with_missing.index:
            missing_pct = (missing[col] / len(self.df)) * 100

            if missing_pct > 50:
                self.log(f"Dropping column '{col}' ({missing_pct:.1f}% missing)")
                self.df = self.df.drop(columns=[col])
                continue

            if self.df[col].dtype in ['int64', 'float64']:
                # Numeric columns
                if strategy == 'mean':
                    fill_value = self.df[col].mean()
                elif strategy == 'median':
                    fill_value = self.df[col].median()
                else:  # auto
                    fill_value = self.df[col].median()
                self.df[col] = self.df[col].fillna(fill_value)
                self.log(f"Filled '{col}' with {strategy}: {fill_value:.2f}")
            else:
                # Categorical columns
                if strategy == 'mode':
                    fill_value = self.df[col].mode()[0]
                else:  # auto
                    fill_value = 'Unknown'
                self.df[col] = self.df[col].fillna(fill_value)
                self.log(f"Filled '{col}' with: {fill_value}")

        return self

    def fix_data_types(self, type_mapping=None):
        """Convert columns to appropriate data types."""
        if type_mapping is None:
            type_mapping = {}

        for col in self.df.columns:
            if col in type_mapping:
                try:
                    self.df[col] = self.df[col].astype(type_mapping[col])
                    self.log(f"Converted '{col}' to {type_mapping[col]}")
                except Exception as e:
                    self.log(f"Failed to convert '{col}': {e}")
            else:
                # Auto-detect dates
                if 'date' in col.lower() or 'time' in col.lower():
                    try:
                        self.df[col] = pd.to_datetime(self.df[col])
                        self.log(f"Converted '{col}' to datetime")
                    except:
                        pass

        return self

    def remove_outliers(self, columns=None, method='iqr', threshold=1.5):
        """Remove outliers using IQR or Z-score method."""
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns

        before = len(self.df)

        for col in columns:
            if method == 'iqr':
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - threshold * IQR
                upper = Q3 + threshold * IQR
                mask = (self.df[col] >= lower) & (self.df[col] <= upper)
            else:  # z-score
                z_scores = np.abs((self.df[col] - self.df[col].mean()) / self.df[col].std())
                mask = z_scores < threshold

            self.df = self.df[mask]

        removed = before - len(self.df)
        self.log(f"Removed {removed} outlier rows using {method} method")
        return self

    def normalize_text(self, columns=None):
        """Normalize text columns (lowercase, strip whitespace)."""
        if columns is None:
            columns = self.df.select_dtypes(include=['object']).columns

        for col in columns:
            self.df[col] = self.df[col].str.strip().str.lower()
            self.log(f"Normalized text in '{col}'")

        return self

    def encode_categorical(self, columns=None, method='label'):
        """Encode categorical variables."""
        if columns is None:
            columns = self.df.select_dtypes(include=['object']).columns

        for col in columns:
            if method == 'label':
                self.df[col] = pd.Categorical(self.df[col]).codes
                self.log(f"Label encoded '{col}'")
            elif method == 'onehot':
                dummies = pd.get_dummies(self.df[col], prefix=col)
                self.df = pd.concat([self.df.drop(columns=[col]), dummies], axis=1)
                self.log(f"One-hot encoded '{col}'")

        return self

    def validate_ranges(self, range_checks):
        """Validate numeric columns are within expected ranges."""
        for col, (min_val, max_val) in range_checks.items():
            invalid = ((self.df[col] < min_val) | (self.df[col] > max_val)).sum()
            if invalid > 0:
                self.log(f"WARNING: {invalid} values in '{col}' outside range [{min_val}, {max_val}]")
                # Remove invalid rows
                self.df = self.df[(self.df[col] >= min_val) & (self.df[col] <= max_val)]

        return self

    def generate_report(self):
        """Generate cleaning report."""
        report = f"""
Data Cleaning Report
====================

Original Shape: {self.original_shape}
Final Shape: {self.df.shape}
Rows Removed: {self.original_shape[0] - self.df.shape[0]}
Columns Removed: {self.original_shape[1] - self.df.shape[1]}

Cleaning Steps:
"""
        for step in self.cleaning_log:
            report += f"  - {step}\n"

        return report

    def get_cleaned_data(self):
        """Return cleaned DataFrame."""
        return self.df


# Usage
pipeline = DataCleaningPipeline(df)
cleaned_df = (
    pipeline
    .remove_duplicates()
    .handle_missing_values(strategy='auto')
    .fix_data_types()
    .remove_outliers(method='iqr', threshold=1.5)
    .normalize_text()
    .validate_ranges({'age': (0, 120), 'price': (0, 1000000)})
    .get_cleaned_data()
)

print(pipeline.generate_report())
cleaned_df.to_csv('cleaned_data.csv', index=False)
```

### 3. Polars Pipeline (Faster for Large Data)

```python
import polars as pl

# Load data
df = pl.read_csv('data.csv')

# Cleaning pipeline
cleaned_df = (
    df
    # Remove duplicates
    .unique()
    # Handle missing values
    .with_columns([
        pl.col('age').fill_null(pl.col('age').median()),
        pl.col('name').fill_null('Unknown'),
    ])
    # Fix data types
    .with_columns([
        pl.col('date').str.strptime(pl.Date, '%Y-%m-%d'),
        pl.col('amount').cast(pl.Float64),
    ])
    # Remove outliers
    .filter(
        (pl.col('age') >= 0) & (pl.col('age') <= 120)
    )
    # Normalize text
    .with_columns([
        pl.col('name').str.to_lowercase().str.strip(),
        pl.col('email').str.to_lowercase(),
    ])
)

# Save
cleaned_df.write_csv('cleaned_data.csv')
```

### 4. PySpark Pipeline (For Big Data)

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, mean, trim, lower
from pyspark.sql.types import IntegerType, DoubleType

spark = SparkSession.builder.appName('DataCleaning').getOrCreate()

# Load data
df = spark.read.csv('data.csv', header=True, inferSchema=True)

# Cleaning pipeline
cleaned_df = (
    df
    # Remove duplicates
    .dropDuplicates()
    # Handle missing values
    .fillna({
        'age': df.select(mean('age')).collect()[0][0],
        'name': 'Unknown',
    })
    # Fix data types
    .withColumn('age', col('age').cast(IntegerType()))
    .withColumn('amount', col('amount').cast(DoubleType()))
    # Remove outliers
    .filter((col('age') >= 0) & (col('age') <= 120))
    # Normalize text
    .withColumn('name', trim(lower(col('name'))))
    .withColumn('email', trim(lower(col('email'))))
)

# Save
cleaned_df.write.csv('cleaned_data', header=True, mode='overwrite')
```

### 5. Data Quality Checks

```python
def data_quality_checks(df):
    """Run comprehensive data quality checks."""
    report = []

    # Check 1: Missing values
    missing = df.isnull().sum()
    if missing.sum() > 0:
        report.append(f"⚠️  Missing values found:\n{missing[missing > 0]}")

    # Check 2: Duplicates
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        report.append(f"⚠️  {duplicates} duplicate rows found")

    # Check 3: Data types
    expected_types = {
        'age': 'int64',
        'amount': 'float64',
        'date': 'datetime64[ns]',
    }
    for col, expected in expected_types.items():
        if col in df.columns and df[col].dtype != expected:
            report.append(f"⚠️  Column '{col}' has type {df[col].dtype}, expected {expected}")

    # Check 4: Value ranges
    if 'age' in df.columns:
        invalid_age = ((df['age'] < 0) | (df['age'] > 120)).sum()
        if invalid_age > 0:
            report.append(f"⚠️  {invalid_age} invalid age values")

    # Check 5: Unique identifiers
    if 'id' in df.columns:
        if df['id'].duplicated().any():
            report.append(f"⚠️  Duplicate IDs found")

    # Check 6: Consistency
    if 'email' in df.columns:
        invalid_email = ~df['email'].str.contains('@', na=False)
        if invalid_email.sum() > 0:
            report.append(f"⚠️  {invalid_email.sum()} invalid email addresses")

    if report:
        print("Data Quality Issues:")
        for issue in report:
            print(issue)
    else:
        print("✅ All quality checks passed!")

    return len(report) == 0

# Run checks
data_quality_checks(cleaned_df)
```

### 6. Automated Cleaning Function

```python
def auto_clean_dataframe(df, config=None):
    """Automatically clean DataFrame with sensible defaults."""
    if config is None:
        config = {
            'remove_duplicates': True,
            'handle_missing': True,
            'remove_outliers': True,
            'fix_types': True,
            'normalize_text': True,
        }

    print(f"Original shape: {df.shape}")

    if config['remove_duplicates']:
        df = df.drop_duplicates()
        print(f"After removing duplicates: {df.shape}")

    if config['handle_missing']:
        # Numeric: fill with median
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            df[col] = df[col].fillna(df[col].median())

        # Categorical: fill with mode or 'Unknown'
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if df[col].mode().empty:
                df[col] = df[col].fillna('Unknown')
            else:
                df[col] = df[col].fillna(df[col].mode()[0])
        print(f"After handling missing values: {df.shape}")

    if config['remove_outliers']:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            df = df[(df[col] >= Q1 - 1.5 * IQR) & (df[col] <= Q3 + 1.5 * IQR)]
        print(f"After removing outliers: {df.shape}")

    if config['normalize_text']:
        text_cols = df.select_dtypes(include=['object']).columns
        for col in text_cols:
            df[col] = df[col].str.strip().str.lower()

    return df

# Usage
cleaned_df = auto_clean_dataframe(df)
```

### 7. Save Pipeline Configuration

```yaml
# data_cleaning_config.yaml
cleaning_pipeline:
  remove_duplicates:
    enabled: true
    subset: ['id', 'email']
    keep: 'first'

  missing_values:
    strategy: auto
    drop_threshold: 50  # Drop columns with >50% missing
    numeric_fill: median
    categorical_fill: mode

  outliers:
    method: iqr
    threshold: 1.5
    columns: ['age', 'price', 'quantity']

  data_types:
    age: int64
    price: float64
    date: datetime64
    email: string

  text_normalization:
    lowercase: true
    strip_whitespace: true
    remove_special_chars: false

  validation:
    ranges:
      age: [0, 120]
      price: [0, 1000000]
    required_columns: ['id', 'name', 'email']
```

### Best Practices

**DO:**
- Always keep original data
- Log all cleaning steps
- Validate data quality
- Handle missing values appropriately
- Remove duplicates early
- Check for outliers
- Validate data types
- Document assumptions

**DON'T:**
- Delete original data
- Fill all missing with zeros
- Ignore outliers
- Mix data types
- Skip validation
- Overfit to training data
- Remove too many rows
- Forget to save cleaned data

## Checklist

- [ ] Loaded and inspected data
- [ ] Removed duplicates
- [ ] Handled missing values
- [ ] Fixed data types
- [ ] Removed/handled outliers
- [ ] Normalized text fields
- [ ] Validated data quality
- [ ] Generated cleaning report
- [ ] Saved cleaned data
