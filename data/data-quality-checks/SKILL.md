---
name: Data Quality Checks
description: Comprehensive guide to data quality validation, testing frameworks, anomaly detection, and data observability for production data pipelines
---

# Data Quality Checks

## What is Data Quality?

**Data Quality:** Ensuring data is accurate, complete, consistent, and reliable for business use.

### Dimensions of Data Quality
```
Accuracy:     Data is correct
Completeness: No missing values
Consistency:  Same across systems
Timeliness:   Data is fresh
Validity:     Conforms to rules
Uniqueness:   No duplicates
```

### Why Data Quality Matters
- **Bad decisions:** Wrong data → wrong insights
- **Broken pipelines:** Invalid data breaks downstream
- **Lost trust:** Users stop trusting data
- **Compliance:** Regulations require data quality

---

## Types of Data Quality Checks

### Schema Validation
```python
# Check column exists
assert "customer_id" in df.columns

# Check data type
assert df.schema["customer_id"].dataType == IntegerType()

# Check column count
assert len(df.columns) == 10
```

### Completeness Checks
```python
# No nulls in required columns
null_count = df.filter(col("customer_id").isNull()).count()
assert null_count == 0, f"Found {null_count} null customer_ids"

# Minimum row count
row_count = df.count()
assert row_count > 1000, f"Expected >1000 rows, got {row_count}"
```

### Uniqueness Checks
```python
# No duplicates
total_rows = df.count()
unique_rows = df.select("customer_id").distinct().count()
assert total_rows == unique_rows, f"Found {total_rows - unique_rows} duplicates"
```

### Range Checks
```python
# Values within expected range
invalid_ages = df.filter((col("age") < 0) | (col("age") > 120)).count()
assert invalid_ages == 0, f"Found {invalid_ages} invalid ages"

# Amount is positive
invalid_amounts = df.filter(col("amount") < 0).count()
assert invalid_amounts == 0, f"Found {invalid_amounts} negative amounts"
```

### Referential Integrity
```python
# Foreign key exists
orders_df = spark.read.table("orders")
customers_df = spark.read.table("customers")

orphan_orders = orders_df.join(
    customers_df,
    orders_df.customer_id == customers_df.customer_id,
    "left_anti"
).count()

assert orphan_orders == 0, f"Found {orphan_orders} orders without customers"
```

### Format Validation
```python
# Email format
import re

email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
invalid_emails = df.filter(
    ~col("email").rlike(email_pattern)
).count()

assert invalid_emails == 0, f"Found {invalid_emails} invalid emails"

# Date format
invalid_dates = df.filter(
    ~col("order_date").cast("date").isNotNull()
).count()

assert invalid_dates == 0, f"Found {invalid_dates} invalid dates"
```

---

## Great Expectations

### Setup
```python
from great_expectations.dataset import SparkDFDataset

# Wrap DataFrame
ge_df = SparkDFDataset(df)
```

### Common Expectations
```python
# Column exists
ge_df.expect_column_to_exist("customer_id")

# No nulls
ge_df.expect_column_values_to_not_be_null("customer_id")

# Unique values
ge_df.expect_column_values_to_be_unique("customer_id")

# Values in set
ge_df.expect_column_values_to_be_in_set(
    "status",
    ["pending", "completed", "cancelled"]
)

# Range
ge_df.expect_column_values_to_be_between(
    "age",
    min_value=0,
    max_value=120
)

# Regex
ge_df.expect_column_values_to_match_regex(
    "email",
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)

# Row count
ge_df.expect_table_row_count_to_be_between(
    min_value=1000,
    max_value=1000000
)
```

### Validation
```python
# Run all expectations
results = ge_df.validate()

# Check if passed
if results["success"]:
    print("All checks passed!")
else:
    print("Some checks failed:")
    for result in results["results"]:
        if not result["success"]:
            print(f"  - {result['expectation_config']['expectation_type']}")
```

### Data Docs
```bash
# Generate HTML documentation
great_expectations docs build
```

---

## dbt Tests

### Schema Tests
```yaml
# models/schema.yml
version: 2

models:
  - name: customers
    columns:
      - name: customer_id
        tests:
          - unique
          - not_null
      
      - name: email
        tests:
          - not_null
          - unique
      
      - name: status
        tests:
          - accepted_values:
              values: ['active', 'inactive', 'suspended']
      
      - name: created_at
        tests:
          - not_null
          - dbt_utils.expression_is_true:
              expression: "<= current_date"
```

### Custom Tests
```sql
-- tests/assert_positive_revenue.sql
select *
from {{ ref('fct_orders') }}
where total_amount < 0
```

### Relationships Test
```yaml
models:
  - name: orders
    columns:
      - name: customer_id
        tests:
          - relationships:
              to: ref('customers')
              field: customer_id
```

---

## Anomaly Detection

### Statistical Anomalies
```python
from scipy import stats
import numpy as np

# Z-score (standard deviations from mean)
df_pd = df.toPandas()
z_scores = np.abs(stats.zscore(df_pd['amount']))
anomalies = df_pd[z_scores > 3]  # >3 std devs

print(f"Found {len(anomalies)} anomalies")
```

### Time Series Anomalies
```python
# Detect sudden spikes/drops
daily_counts = df.groupBy("date").count().orderBy("date")

# Calculate moving average
from pyspark.sql.window import Window

window = Window.orderBy("date").rowsBetween(-7, 0)
daily_counts = daily_counts.withColumn(
    "moving_avg",
    avg("count").over(window)
)

# Flag anomalies (>2x moving average)
anomalies = daily_counts.filter(
    col("count") > col("moving_avg") * 2
)
```

### Null Rate Anomalies
```python
# Track null rate over time
null_rates = df.groupBy("date").agg(
    (sum(when(col("email").isNull(), 1).otherwise(0)) / count("*")).alias("null_rate")
)

# Alert if null rate > 5%
high_null_days = null_rates.filter(col("null_rate") > 0.05)
```

---

## Data Observability

### Freshness Checks
```python
from datetime import datetime, timedelta

# Check data freshness
latest_timestamp = df.agg(max("created_at")).collect()[0][0]
now = datetime.now()
age = now - latest_timestamp

# Alert if data is >24 hours old
assert age < timedelta(hours=24), f"Data is {age} old (stale!)"
```

### Volume Checks
```python
# Check row count is within expected range
today_count = df.filter(col("date") == current_date()).count()
expected_min = 10000
expected_max = 100000

assert expected_min <= today_count <= expected_max, \
    f"Row count {today_count} outside expected range [{expected_min}, {expected_max}]"
```

### Distribution Checks
```python
# Check value distribution
status_dist = df.groupBy("status").count().collect()

# Expected distribution
expected = {
    "active": (0.7, 0.9),      # 70-90%
    "inactive": (0.05, 0.2),   # 5-20%
    "suspended": (0.0, 0.1)    # 0-10%
}

total = df.count()
for row in status_dist:
    status = row["status"]
    count = row["count"]
    pct = count / total
    
    if status in expected:
        min_pct, max_pct = expected[status]
        assert min_pct <= pct <= max_pct, \
            f"{status}: {pct:.1%} outside expected range [{min_pct:.1%}, {max_pct:.1%}]"
```

---

## Data Quality Frameworks

### Great Expectations
```python
import great_expectations as ge

# Create context
context = ge.get_context()

# Create expectation suite
suite = context.create_expectation_suite("my_suite")

# Add expectations
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name="my_suite"
)

validator.expect_column_values_to_not_be_null("customer_id")
validator.expect_column_values_to_be_unique("customer_id")

# Save suite
validator.save_expectation_suite()

# Run validation
results = context.run_checkpoint(checkpoint_name="my_checkpoint")
```

### dbt Tests
```bash
# Run all tests
dbt test

# Run tests for specific model
dbt test --select customers

# Run tests in CI/CD
dbt test --fail-fast
```

### Monte Carlo
```python
# SaaS data observability platform
# Automatic anomaly detection
# No code required
```

### Soda
```yaml
# checks.yml
checks for customers:
  - row_count > 1000
  - missing_count(customer_id) = 0
  - duplicate_count(customer_id) = 0
  - invalid_count(email) = 0:
      valid format: email
  - freshness(created_at) < 24h
```

```bash
# Run checks
soda scan -d my_datasource -c configuration.yml checks.yml
```

---

## Implementing Data Quality Pipeline

### Pipeline Structure
```python
def run_quality_checks(df, checks):
    """Run data quality checks and return results"""
    results = []
    
    for check in checks:
        try:
            check(df)
            results.append({
                "check": check.__name__,
                "status": "PASS",
                "error": None
            })
        except AssertionError as e:
            results.append({
                "check": check.__name__,
                "status": "FAIL",
                "error": str(e)
            })
    
    return results

# Define checks
def check_no_nulls(df):
    null_count = df.filter(col("customer_id").isNull()).count()
    assert null_count == 0, f"Found {null_count} nulls"

def check_no_duplicates(df):
    total = df.count()
    unique = df.select("customer_id").distinct().count()
    assert total == unique, f"Found {total - unique} duplicates"

def check_row_count(df):
    count = df.count()
    assert count > 1000, f"Expected >1000 rows, got {count}"

# Run checks
checks = [check_no_nulls, check_no_duplicates, check_row_count]
results = run_quality_checks(df, checks)

# Log results
for result in results:
    if result["status"] == "FAIL":
        print(f"❌ {result['check']}: {result['error']}")
    else:
        print(f"✅ {result['check']}")

# Fail pipeline if any check failed
if any(r["status"] == "FAIL" for r in results):
    raise Exception("Data quality checks failed")
```

### Quarantine Bad Data
```python
# Separate good and bad data
good_data = df.filter(
    col("customer_id").isNotNull() &
    col("email").rlike(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
)

bad_data = df.subtract(good_data)

# Write good data to production
good_data.write.format("delta").mode("append").save("/prod/customers")

# Write bad data to quarantine
bad_data.write.format("delta").mode("append").save("/quarantine/customers")

# Alert on bad data
if bad_data.count() > 0:
    send_alert(f"Found {bad_data.count()} bad records in quarantine")
```

---

## Monitoring and Alerting

### Metrics to Track
```
Freshness: How old is the data?
Volume: Row count per day
Completeness: % of non-null values
Uniqueness: % of unique values
Validity: % of values passing validation
Schema changes: Columns added/removed/changed
```

### Alerting Rules
```python
# Alert if data is stale
if data_age > timedelta(hours=24):
    send_alert("Data is stale")

# Alert if volume drops >50%
if today_count < yesterday_count * 0.5:
    send_alert("Volume dropped significantly")

# Alert if null rate increases >10%
if today_null_rate > yesterday_null_rate + 0.1:
    send_alert("Null rate increased")
```

### Dashboard
```
Metrics Dashboard:
- Data freshness (last updated)
- Row count trend (7 days)
- Null rate trend (7 days)
- Test pass rate (% passing)
- Failed tests (list)
```

---

## Best Practices

### 1. Test Early and Often
```
Bronze layer: Schema validation
Silver layer: Completeness, uniqueness
Gold layer: Business logic validation
```

### 2. Fail Fast
```python
# Stop pipeline if critical checks fail
if critical_check_failed:
    raise Exception("Critical check failed, stopping pipeline")
```

### 3. Quarantine Bad Data
```
Don't drop bad data
→ Quarantine for investigation
→ Fix and reprocess
```

### 4. Monitor Trends
```
Track metrics over time
Alert on anomalies
Investigate root cause
```

### 5. Document Expectations
```yaml
# Document what "good" data looks like
customers:
  - customer_id: unique, not null
  - email: valid format, unique
  - age: 0-120
  - status: active, inactive, suspended
```

---

## Summary

**Data Quality:** Ensuring data is accurate, complete, consistent

**Dimensions:**
- Accuracy, Completeness, Consistency
- Timeliness, Validity, Uniqueness

**Check Types:**
- Schema validation
- Completeness checks
- Uniqueness checks
- Range checks
- Referential integrity
- Format validation

**Frameworks:**
- Great Expectations (Python)
- dbt tests (SQL)
- Soda (YAML)
- Monte Carlo (SaaS)

**Anomaly Detection:**
- Statistical (Z-score)
- Time series (moving average)
- Null rate tracking

**Data Observability:**
- Freshness checks
- Volume checks
- Distribution checks

**Best Practices:**
- Test early and often
- Fail fast on critical checks
- Quarantine bad data
- Monitor trends
- Document expectations
