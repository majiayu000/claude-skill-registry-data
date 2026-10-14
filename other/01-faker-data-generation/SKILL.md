---
name: faker-data-generation
description: Generate synthetic data with Faker for Bronze layer testing with configurable data corruption. Use when creating test data for data quality validation, testing DLT expectations, or simulating production-like datasets. Supports realistic data generation with intentional corruption patterns mapped to specific DQ expectations.
clients: [ide_cli, genie_code]
bundle_resource: jobs
deploy_verb: bundle_deploy
deploy_note: "Synthetic data generation runs inside the Bronze load job (notebook_task); deploy via `bundle deploy --target dev` (runDatabricksCli on Genie Code)."
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "2.0"
  domain: bronze
  role: worker
  pipeline_stage: 2
  pipeline_stage_name: bronze
  called_by:
    - bronze-layer-setup
  standalone: true
  last_verified: "2026-02-07"
  volatility: low
  upstream_sources:
    - name: "databricks-agent-skills"
      repo: "databricks/databricks-agent-skills"
      paths:
        - "skills/databricks-synthetic-data-gen/SKILL.md"
      relationship: "extended"
      last_synced: "2026-08-30"
      sync_commit: "ca92a6c"
---
# Faker Data Generation Patterns

## Overview

When generating synthetic data for Databricks Bronze layer tables, use Faker with **configurable data corruption** to test Silver layer data quality expectations.

## Upstream: Synthetic Data Generation Workflow

The upstream `databricks-synthetic-data-gen` skill in Databricks Agent Skills introduces a file-based workflow:

### File-Based Execution
1. Write Python code to a local file (e.g., `scripts/generate_data.py`)
2. Execute on Databricks using the `run_python_file_on_databricks` MCP tool
3. If execution fails, edit the local file and re-execute

### Context Reuse
The first execution auto-selects a running cluster and creates an execution context. Reuse `cluster_id` and `context_id` for follow-up calls (faster: ~1s vs ~15s).

### Raw Data Only
By default, generate raw transactional data only — no `total_x`, `sum_x`, `avg_x` fields. SDP pipelines compute aggregations downstream.

### Volume-First Storage
Save data to Volumes as parquet files, not directly to tables:
```python
VOLUME_PATH = f"/Volumes/{CATALOG}/{SCHEMA}/raw_data"
spark.createDataFrame(df).write.mode("overwrite").parquet(f"{VOLUME_PATH}/table_name")
```

### Dynamic Date Ranges
Generate data for the last ~6 months from today using `datetime.now() - timedelta(days=180)`.

## When to Use This Skill

Use when:
- Creating test data for data quality validation
- Testing DLT expectations with intentional violations
- Simulating production-like datasets for development/staging
- Validating referential integrity between dimensions and facts

## Core Principles

1. **Realistic Data**: Use Faker with non-linear distributions and temporal patterns
2. **Referential Integrity**: Maintain proper FK relationships between dimensions and facts
3. **Configurable Corruption**: Add intentional data quality issues for testing
4. **DQ Mapping**: Each corruption type maps to specific DLT expectations
5. **Row Coherence**: Attributes within a row must correlate logically
6. **Raw Data Only**: Generate transactional records -- aggregation happens in Gold
7. **Reproducible**: Always seed both `np.random.seed()` and `Faker.seed()`
8. **Documentation**: Document corruption patterns and their DQ impacts

## Critical Rules

### Standard Function Signature

```python
def generate_<entity>_data(
    dimension_keys: dict,
    num_records: int = 1000,
    corruption_rate: float = 0.05
) -> list:
    """
    Generate fake <entity> data with realistic patterns.
    
    Args:
        dimension_keys: Dictionary containing dimension keys for referential integrity
        num_records: Number of records to generate
        corruption_rate: Percentage of records to intentionally corrupt (0.0 to 1.0)
        
    Returns:
        List of <entity> dictionaries
    """
    fake = Faker()
    records = []
    
    print(f"\nGenerating {num_records} <entities> (corruption rate: {corruption_rate*100}%)")
    
    for i in range(num_records):
        # Generate valid data first
        record_data = generate_valid_record(fake, dimension_keys)
        
        # Apply corruption if selected
        should_corrupt = random.random() < corruption_rate
        
        if should_corrupt:
            record_data = apply_corruption(record_data, corruption_rate)
        
        records.append(record_data)
    
    return records
```

### 🔴 MANDATORY: Seed for Reproducibility

**EVERY generation script MUST seed both numpy and Faker:**

```python
import numpy as np
from faker import Faker

SEED = 42
np.random.seed(SEED)
Faker.seed(SEED)
fake = Faker()
```

**Why:** Without seeding, re-running generation produces different data, making debugging impossible and breaking snapshot tests.

### 🔴 MANDATORY: Non-Linear Distributions

**NEVER use `random.uniform()` for values. Real data is never uniformly distributed:**

```python
# ❌ WRONG - Uniform (unrealistic)
prices = [random.uniform(10, 1000) for _ in range(N)]

# ✅ CORRECT - Log-normal for monetary values (prices, salaries, amounts)
prices = np.random.lognormal(mean=4.5, sigma=0.8, size=N)

# ✅ CORRECT - Exponential for durations (resolution time, session length)
durations = np.random.exponential(scale=24, size=N)

# ✅ CORRECT - Weighted categorical (not equal probability)
regions = np.random.choice(
    ['North', 'South', 'East', 'West'],
    size=N, p=[0.40, 0.25, 0.20, 0.15]
)
```

### 🔴 MANDATORY: Dynamic Date Range (Last 6 Months)

```python
from datetime import datetime, timedelta

END_DATE = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
START_DATE = END_DATE - timedelta(days=180)
```

**Why:** Ensures data feels current for demos and dashboards, with enough history for trend analysis.

### 🔴 MANDATORY: Row Coherence

**Attributes within a row MUST correlate logically:**

```python
# ✅ CORRECT - tier drives amount, priority, and behavior
if tier == 'Enterprise':
    amount = np.random.lognormal(7, 0.8)        # Higher amounts
    priority = np.random.choice(['Critical', 'High', 'Medium'], p=[0.3, 0.5, 0.2])
else:
    amount = np.random.lognormal(3.5, 0.6)      # Lower amounts
    priority = np.random.choice(['High', 'Medium', 'Low'], p=[0.2, 0.5, 0.3])

# ❌ WRONG - independent random values (no correlation)
amount = random.uniform(10, 10000)  # Amount unrelated to tier
priority = random.choice(['Critical', 'High', 'Medium', 'Low'])  # Random priority
```

### 🔴 MANDATORY: Raw Data Only (No Pre-Aggregated Fields)

**Generate one row per event/transaction. NEVER add aggregated columns:**

```python
# ❌ WRONG - pre-aggregated fields (aggregation belongs in Gold layer)
{"customer_id": cid, "total_orders": 47, "total_revenue": 12500.00, "avg_order_value": 265.95}

# ✅ CORRECT - one row per transaction
{"order_id": "ORD-000001", "customer_id": cid, "amount": 150.00, "order_date": "2025-10-15"}
```

**Why:** The Medallion pipeline (Silver DLT → Gold MERGE) computes aggregations downstream.

### 🔴 MANDATORY: Weighted Sampling for Facts

**Dimension characteristics MUST drive fact generation volume and behavior:**

```python
# Build weighted lookup from dimensions
tier_weights = customers_pdf["tier"].map({'Enterprise': 5.0, 'Pro': 2.0, 'Free': 1.0})
customer_weights = (tier_weights / tier_weights.sum()).tolist()
customer_ids = customers_pdf["customer_id"].tolist()

# Enterprise customers generate 5x more events than Free
cid = np.random.choice(customer_ids, p=customer_weights)
```

### Corruption Pattern Structure

```python
# Determine if this record should be corrupted for DQ testing
should_corrupt = random.random() < corruption_rate

if should_corrupt:
    # Apply various DQ violations to test expectations
    corruption_type = random.choice([
        'corruption_type_1',
        'corruption_type_2',
        'corruption_type_3',
    ])
    
    if corruption_type == 'corruption_type_1':
        # Will fail: <expectation_name>
        field = invalid_value  # Description of violation
```

### Comments Must Include

1. **Corruption type name**: Descriptive identifier
2. **DQ expectation failed**: Which expectation(s) this triggers
3. **Violation description**: What makes the data invalid

## Parameter Handling

### Function Parameters

```python
def get_parameters():
    """Get parameters from notebook widgets or command line."""
    try:
        # Try Databricks widgets first (notebook mode)
        catalog = dbutils.widgets.get("catalog")
        schema = dbutils.widgets.get("schema")
        num_records = int(dbutils.widgets.get("num_records"))
        corruption_rate = float(dbutils.widgets.get("corruption_rate"))
    except:
        # Fall back to command line arguments or defaults
        catalog = "default_catalog"
        schema = "default_schema"
        num_records = 1000
        corruption_rate = 0.05  # 5% corruption by default
        
        for arg in sys.argv[1:]:
            if arg.startswith("--catalog="):
                catalog = arg.split("=")[1]
            elif arg.startswith("--schema="):
                schema = arg.split("=")[1]
            elif arg.startswith("--num_records="):
                num_records = int(arg.split("=")[1])
            elif arg.startswith("--corruption_rate="):
                corruption_rate = float(arg.split("=")[1])
    
    return catalog, schema, num_records, corruption_rate
```

### Job Configuration (YAML)

```yaml
tasks:
  - task_key: generate_data
    environment_key: default
    notebook_task:
      notebook_path: ../src/layer/generate_data.py
      base_parameters:
        catalog: ${var.catalog}
        schema: ${var.schema}
        num_records: "1000"
        corruption_rate: "0.05"  # 5% corruption for DQ testing
```

## Quick Patterns

### Corruption Type Categories

1. **Missing Required Fields** - Null or empty required fields
2. **Invalid Format/Length** - Wrong format or below minimum length
3. **Out of Range Values** - Excessive or negative values
4. **Business Logic Violations** - Field relationships that violate rules
5. **Temporal Issues** - Dates too old or in the future
6. **Referential Integrity Issues** - Missing or invalid foreign keys

### Dimension vs Fact Patterns

**Dimensions** are referenced by facts, so must be generated first. Use locale-specific Faker for realistic data.

**Facts** reference dimensions, so dimensions must exist first. Load dimension keys for referential integrity.

## Data Volume Guidance

Generate enough records so patterns survive downstream aggregation (daily/weekly/regional GROUP BY):

| Grain | Minimum Records | Rationale |
|---|---|---|
| Daily time series | 50-100/day | Trends visible after weekly rollup |
| Per category | 500+ per category | Statistical significance in charts |
| Per customer | 5-20 events/customer | Customer-level analysis works |
| Total rows | 10K-50K minimum | Patterns survive GROUP BY |

```python
# Example: 180 days of data
N_CUSTOMERS = 2500      # Dimension
N_ORDERS = 25000        # ~10 orders/customer, ~139/day
N_TICKETS = 8000        # ~44/day, enough for weekly trends
```

## Common Mistakes to Avoid

### ❌ DON'T: Use uniform distributions

```python
# BAD - everything equally likely (unrealistic)
prices = [random.uniform(10, 1000) for _ in range(N)]
regions = [random.choice(['N', 'S', 'E', 'W']) for _ in range(N)]
```

### ✅ DO: Use realistic distributions

```python
# GOOD - log-normal for values, weighted for categories
prices = np.random.lognormal(mean=4.5, sigma=0.8, size=N)
regions = np.random.choice(['N', 'S', 'E', 'W'], size=N, p=[0.4, 0.25, 0.2, 0.15])
```

### ❌ DON'T: Generate flat temporal data

```python
# BAD - ignores weekends, holidays, seasonality
dates = [fake.date_between(start_date='-6m', end_date='today') for _ in range(N)]
```

### ✅ DO: Add temporal patterns

```python
# GOOD - weekday/weekend/holiday/spike effects
def get_daily_multiplier(date, us_holidays):
    mult = 1.0
    if date.weekday() >= 5: mult *= 0.6          # Weekend drop
    if date in us_holidays: mult *= 0.3           # Holiday drop
    mult *= 1 + 0.15 * (date.month - 6) / 6      # Q4 seasonality
    return max(0.1, mult * np.random.normal(1, 0.1))
```

### ❌ DON'T: Add pre-aggregated fields

```python
# BAD - aggregation belongs in Gold layer
{"customer_id": cid, "total_orders": 47, "avg_csat": 4.2}
```

### ✅ DO: Generate raw transactional records

```python
# GOOD - one row per event
{"order_id": "ORD-001", "customer_id": cid, "amount": 150.00}
```

### ❌ DON'T: Apply corruption before generating valid data

```python
# BAD - hard to maintain
if should_corrupt:
    field = generate_invalid_field()
else:
    field = generate_valid_field()
```

### ✅ DO: Generate valid data first, then corrupt

```python
# GOOD - clean separation
field = generate_valid_field()

if should_corrupt:
    field = corrupt_field(field)  # Modify valid data
```

### ❌ DON'T: Hardcode corruption without comments

```python
# BAD - no DQ mapping
if corruption_type == 'bad_data':
    field = None
```

### ✅ DO: Document which expectation fails

```python
# GOOD - clear DQ mapping
if corruption_type == 'null_required_field':
    # Will fail: valid_field_name
    field = None
```

### ❌ DON'T: Use magic numbers

```python
# BAD - unclear threshold
if random.random() < 0.05:
    # What is 0.05?
```

### ✅ DO: Use named parameter

```python
# GOOD - explicit parameter
should_corrupt = random.random() < corruption_rate
```

## Testing Scenarios

### Development: High Corruption
```yaml
corruption_rate: "0.10"  # 10% for thorough testing
```

### Staging: Realistic Corruption
```yaml
corruption_rate: "0.05"  # 5% production-like
```

### Production: No Synthetic Corruption
```yaml
corruption_rate: "0.0"  # Real data only
```

## Validation Checklist

### Realism (CRITICAL)
- [ ] `np.random.seed(SEED)` AND `Faker.seed(SEED)` called at script top
- [ ] Monetary values use log-normal distribution (NOT uniform)
- [ ] Duration values use exponential distribution (NOT uniform)
- [ ] Categorical values use weighted probabilities (NOT equal)
- [ ] Row coherence: tier→amount, priority→resolution_time→CSAT correlations exist
- [ ] Time patterns: weekday/weekend/holiday/seasonality multipliers applied
- [ ] Dynamic date range: last 6 months from `datetime.now()`
- [ ] No pre-aggregated fields (`total_x`, `sum_x`, `avg_x`)
- [ ] Data volume: 10K-50K rows minimum, 50-100/day for time series

### Corruption
- [ ] `corruption_rate` parameter added with default 0.05 (5%)
- [ ] Each corruption type has comment: `# Will fail: <expectation_name>`
- [ ] Corruption types map 1:1 to DLT expectations
- [ ] Valid data generated FIRST, then corrupted

### Structure
- [ ] Parameter handling uses `dbutils.widgets.get()` (NOT argparse)
- [ ] Job YAML includes `corruption_rate` parameter
- [ ] Dimensions generated BEFORE facts
- [ ] Weighted sampling: dimension characteristics drive fact volume
- [ ] Referential integrity maintained (facts reference valid dimension keys)
- [ ] Validation prints at end (distribution checks, corruption stats)

## Required Libraries

```python
# ✅ ALWAYS include these in environment dependencies
dependencies:
  - "Faker==22.0.0"
  - "holidays>=0.40"
  - "numpy>=1.24.0"
  - "pandas>=2.0.0"
```

Use pandas for generation (faster row-by-row logic), convert to Spark DataFrame for saving to Delta tables.

## Reference Files

- **[Faker Providers](references/faker-providers.md)** - Detailed provider examples, corruption patterns, non-linear distribution patterns, time-based pattern functions, row coherence patterns, data volume guidance, and complete implementation examples. Includes locale-specific providers, business-specific providers, and domain-specific constants.

- **[Generate Data Script](scripts/generate_data.py)** - Data generation utility with standard function signatures, numpy-based distributions, weighted sampling, temporal patterns, seeding, and parameter handling. Includes `generate_dimension_data()`, `generate_fact_data()`, `apply_corruption()`, `get_daily_multiplier()`, and `get_parameters()` functions.

## References

- [Faker Documentation](https://faker.readthedocs.io/)
- [DLT Expectations](https://docs.databricks.com/aws/en/dlt/expectations)
