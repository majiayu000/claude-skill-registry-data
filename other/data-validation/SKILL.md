---
name: data-validation
description: Implement comprehensive data validation, quality checks, and testing frameworks. Ensure data integrity and reliability across pipelines.
triggers:
- /data validation
- /data quality
---

# Data Validation and Quality

This skill provides comprehensive approaches to validating data quality, implementing testing frameworks, and ensuring data reliability throughout your pipelines.

## When to use this skill

Use this skill when you need to:
- Implement data quality checks in pipelines
- Create data validation frameworks
- Set up automated data testing
- Monitor data quality metrics
- Ensure compliance with data standards

## Prerequisites

- Understanding of data schemas and business rules
- Access to data quality tools (Great Expectations, Soda, custom)
- Knowledge of statistical methods for data analysis
- Integration points in data pipelines

## Guidelines

### Validation Categories

**Schema Validation**
- Column existence and order
- Data type correctness
- Nullability constraints
- Format validation (regex patterns)

```python
import pandera as pa
from pandera import Column, Check

schema = pa.DataFrameSchema({
    "id": Column(int, nullable=False),
    "email": Column(str, Check.str_matches(r"^[^@]+@[^@]+$"), nullable=False),
    "age": Column(int, Check.greater_than(0), Check.less_than(150), nullable=True),
    "created_at": Column(pa.DateTime, nullable=False)
})

validated_df = schema.validate(df)
```

**Content Validation**
- Range checks (min/max values)
- Uniqueness constraints
- Referential integrity
- Business rule validation

**Statistical Validation**
- Distribution analysis
- Outlier detection
- Trend analysis
- Anomaly detection

### Validation Frameworks

**Great Expectations**
```python
import great_expectations as gx

context = gx.get_context()
suite = context.add_expectation_suite("my_suite")

# Add expectations
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite=suite
)

validator.expect_column_values_to_not_be_null("id")
validator.expect_column_values_to_be_between("age", 0, 150)
validator.expect_column_values_to_match_regex("email", r"^[^@]+@[^@]+$")
validator.expect_column_mean_to_be_between("salary", 50000, 150000)

validator.save_expectation_suite()
```

**Soda Core**
```yaml
# checks.yml
checks for dataset:
  - row_count > 0
  - duplicate_count(id) = 0
  - missing_count(email) < 5
  - invalid_percent(email) < 1%:
      valid format: email
  - avg(age) between 18 and 100
```

### Validation Strategies

**Pre-Load Validation**
- Validate raw data before transformation
- Reject or quarantine bad records
- Log validation failures

**Post-Transform Validation**
- Validate after business rules applied
- Ensure data warehouse constraints
- Check aggregate correctness

**Continuous Monitoring**
- Schedule validation jobs
- Track quality metrics over time
- Alert on degradation

### Data Quality Dimensions

**Completeness**
- Percentage of populated fields
- Required field coverage
- Historical completeness trends

**Accuracy**
- Match with source of truth
- Business rule compliance
- Cross-system consistency

**Consistency**
- Format standardization
- Unit consistency
- Naming conventions

**Timeliness**
- Data freshness
- Update frequency
- Latency monitoring

### Implementation Best Practices

**Validation Layers**
```
Source → Schema Validation → Business Rules → Statistical Checks → Target
              ↓                      ↓                  ↓
         Reject Bad Data       Flag Warnings      Alert Anomalies
```

**Error Handling**
- Categorize failures (critical, warning, info)
- Implement quarantine tables for bad records
- Provide detailed error messages
- Enable quick failure recovery

**Testing**
- Unit tests for validation rules
- Integration tests for full pipelines
- Data diff tests between environments
- Regression testing for schema changes

### Monitoring and Alerting

**Metrics to Track**
- Validation pass/fail rates
- Data quality scores
- Processing times
- Error frequencies by category

**Alert Conditions**
- Critical validation failures
- Quality score drops below threshold
- Unusual error patterns
- SLA breaches

## Examples

See the `examples/` directory for:
- `great-expectations-suite.py` - Complete GE suite setup
- `pandera-schema.py` - Runtime schema validation
- `custom-validator.py` - Building custom validation framework
- `quality-dashboard.py` - Quality metrics visualization

## References

- [Great Expectations documentation](https://docs.greatexpectations.io/)
- [Soda Core documentation](https://docs.soda.io/)
- [Pandera documentation](https://pandera.readthedocs.io/)
- [Data quality metrics](https://towardsdatascience.com/data-quality-metrics-6-metrics-to-measure-data-quality/)
