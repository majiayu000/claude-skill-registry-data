---
name: delta-live-tables
description: Delta Live Tables (DLT) pipeline patterns and examples for building declarative, self-healing data pipelines with automatic quality enforcement and lineage tracking.
triggers:
  - delta live tables
  - dlt pipeline
  - declarative pipelines
  - streaming tables
  - materialized views
category: streaming
---

# Delta Live Tables Skill

## Overview

Delta Live Tables (DLT) is a declarative framework for building reliable, maintainable, and testable data processing pipelines. It automatically manages infrastructure, error handling, data quality, and monitoring.

**Key Benefits:**
- Declarative pipeline definitions
- Automatic dependency resolution
- Built-in data quality checks
- Real-time monitoring and lineage
- Simplified error recovery
- Automatic schema evolution

## When to Use This Skill

Use Delta Live Tables when you need to:
- Build production data pipelines with minimal operational overhead
- Implement complex data quality rules
- Create streaming and batch pipelines with unified syntax
- Track data lineage automatically
- Simplify pipeline maintenance and debugging
- Enforce SLAs with expectations

## Core Concepts

### 1. Tables vs Views

**Streaming Tables**: Process data incrementally using structured streaming
```python
@dlt.table(
    comment="Raw sensor events ingested in real-time",
    table_properties={"quality": "bronze"}
)
def sensor_events_raw():
    return (
        spark.readStream
            .format("cloudFiles")
            .option("cloudFiles.format", "json")
            .load("/mnt/source/sensors/")
    )
```

**Materialized Views**: Computed from queries on other tables/views
```python
@dlt.view(
    comment="Cleaned sensor events with quality checks"
)
def sensor_events_cleaned():
    return (
        dlt.read_stream("sensor_events_raw")
            .filter(col("sensor_id").isNotNull())
            .withColumn("timestamp", to_timestamp(col("event_time")))
    )
```

### 2. Expectations (Data Quality)

**Three enforcement levels:**

**warn**: Log violations but continue processing
```python
@dlt.table
@dlt.expect("valid_sensor_id", "sensor_id IS NOT NULL")
def sensor_data():
    return dlt.read("sensor_events_cleaned")
```

**drop**: Silently drop violating records
```python
@dlt.table
@dlt.expect_or_drop("valid_temperature", "temperature BETWEEN -50 AND 150")
def valid_sensor_readings():
    return dlt.read("sensor_data")
```

**fail**: Stop pipeline on violations
```python
@dlt.table
@dlt.expect_or_fail("no_null_ids", "sensor_id IS NOT NULL")
def critical_sensor_data():
    return dlt.read("sensor_events_cleaned")
```

### 3. Incremental Processing

**Streaming Tables** automatically handle incremental processing:
```python
@dlt.table
def orders_incremental():
    return (
        dlt.read_stream("orders_raw")
            .select("order_id", "customer_id", "amount", "order_date")
    )
```

**Apply Changes** for CDC (Change Data Capture):
```python
dlt.create_streaming_table("customers_current")

dlt.apply_changes(
    target="customers_current",
    source="customers_cdc",
    keys=["customer_id"],
    sequence_by="updated_at",
    stored_as_scd_type=2  # Slowly Changing Dimension Type 2
)
```

## Implementation Patterns

### Pattern 1: Multi-Hop Pipeline (Bronze-Silver-Gold)

**Bronze Layer (Raw Ingestion):**
```python
import dlt
from pyspark.sql.functions import *

@dlt.table(
    name="bronze_sales_raw",
    comment="Raw sales data ingested from cloud storage",
    table_properties={
        "quality": "bronze",
        "pipelines.autoOptimize.managed": "true"
    }
)
def bronze_sales():
    return (
        spark.readStream
            .format("cloudFiles")
            .option("cloudFiles.format", "json")
            .option("cloudFiles.schemaLocation", "/mnt/schemas/sales")
            .load("/mnt/landing/sales/")
            .withColumn("ingestion_timestamp", current_timestamp())
            .withColumn("source_file", input_file_name())
    )
```

**Silver Layer (Cleaned & Validated):**
```python
@dlt.table(
    name="silver_sales_validated",
    comment="Validated and cleaned sales data",
    table_properties={"quality": "silver"}
)
@dlt.expect_or_drop("valid_sale_id", "sale_id IS NOT NULL")
@dlt.expect_or_drop("positive_amount", "amount > 0")
@dlt.expect("valid_email", "email RLIKE '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}$'")
def silver_sales():
    return (
        dlt.read_stream("bronze_sales_raw")
            .select(
                col("sale_id"),
                col("customer_id"),
                col("amount").cast("decimal(10,2)"),
                lower(trim(col("email"))).alias("email"),
                to_timestamp(col("sale_timestamp")).alias("sale_timestamp"),
                col("ingestion_timestamp")
            )
            .dropDuplicates(["sale_id"])
    )
```

**Gold Layer (Business Aggregates):**
```python
@dlt.table(
    name="gold_daily_sales_summary",
    comment="Daily sales aggregates for reporting",
    table_properties={"quality": "gold"}
)
@dlt.expect_or_fail("valid_date", "sale_date IS NOT NULL")
def gold_daily_sales():
    return (
        dlt.read("silver_sales_validated")
            .groupBy(
                to_date(col("sale_timestamp")).alias("sale_date"),
                col("customer_id")
            )
            .agg(
                count("*").alias("transaction_count"),
                sum("amount").alias("total_amount"),
                avg("amount").alias("avg_amount"),
                min("sale_timestamp").alias("first_transaction"),
                max("sale_timestamp").alias("last_transaction")
            )
    )
```

### Pattern 2: Change Data Capture (CDC)

```python
import dlt
from pyspark.sql.functions import *

# Bronze: Ingest CDC events
@dlt.table(
    name="bronze_customer_cdc",
    comment="Customer CDC events from upstream system"
)
def customer_cdc_bronze():
    return (
        spark.readStream
            .format("delta")
            .option("readChangeFeed", "true")
            .option("startingVersion", 0)
            .table("source.customers")
    )

# Silver: Apply changes with SCD Type 2
dlt.create_streaming_table(
    name="silver_customers_current",
    comment="Current customer records with history",
    table_properties={
        "quality": "silver",
        "delta.enableChangeDataFeed": "true"
    }
)

dlt.apply_changes(
    target="silver_customers_current",
    source="bronze_customer_cdc",
    keys=["customer_id"],
    sequence_by="updated_timestamp",
    apply_as_deletes=expr("operation = 'DELETE'"),
    except_column_list=["operation", "source_timestamp"],
    stored_as_scd_type=2
)

# Gold: Active customers only
@dlt.table(
    name="gold_active_customers",
    comment="Currently active customer records"
)
def active_customers():
    return (
        dlt.read("silver_customers_current")
            .filter(col("__END_AT").isNull())  # SCD Type 2: current records
            .filter(col("status") == "active")
            .select(
                "customer_id",
                "name",
                "email",
                "segment",
                "lifetime_value",
                col("__START_AT").alias("valid_from")
            )
    )
```

### Pattern 3: Complex Data Quality Rules

```python
import dlt
from pyspark.sql.functions import *

@dlt.table(
    name="silver_orders_validated",
    comment="Orders with comprehensive quality checks"
)
# Basic expectations
@dlt.expect("valid_order_id", "order_id IS NOT NULL")
@dlt.expect_or_drop("positive_amount", "total_amount > 0")
@dlt.expect_or_drop("valid_quantity", "quantity > 0 AND quantity < 1000")

# Email format validation
@dlt.expect("valid_email_format",
    "customer_email RLIKE '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}$'"
)

# Date range validation
@dlt.expect_or_drop("order_date_in_range",
    "order_date >= '2020-01-01' AND order_date <= current_date()"
)

# Referential integrity
@dlt.expect_or_fail("valid_customer",
    "customer_id IN (SELECT customer_id FROM LIVE.silver_customers_current)"
)

# Business rules
@dlt.expect("reasonable_unit_price",
    "unit_price >= 0.01 AND unit_price <= 100000"
)

# Composite validation
@dlt.expect("amount_matches_calculation",
    "ABS(total_amount - (quantity * unit_price)) < 0.01"
)

def orders_validated():
    return (
        dlt.read_stream("bronze_orders_raw")
            .select(
                "order_id",
                "customer_id",
                "customer_email",
                col("total_amount").cast("decimal(10,2)"),
                col("quantity").cast("int"),
                col("unit_price").cast("decimal(10,2)"),
                to_date(col("order_date")).alias("order_date"),
                current_timestamp().alias("validated_at")
            )
    )
```

### Pattern 4: Streaming Joins

```python
@dlt.table(
    name="gold_enriched_transactions",
    comment="Transactions enriched with customer and product data"
)
def enriched_transactions():
    transactions = dlt.read_stream("silver_transactions")
    customers = dlt.read("silver_customers_current")
    products = dlt.read("silver_products")

    return (
        transactions
            .join(
                customers,
                transactions.customer_id == customers.customer_id,
                "left"
            )
            .join(
                products,
                transactions.product_id == products.product_id,
                "left"
            )
            .select(
                transactions["*"],
                customers["customer_name"],
                customers["customer_segment"],
                products["product_name"],
                products["category"]
            )
    )
```

## Pipeline Configuration

### DLT Pipeline Settings (YAML)

```yaml
# databricks.yml or pipeline configuration
name: sales_pipeline
target: production_db
storage: /mnt/dlt/sales_pipeline

clusters:
  - label: default
    num_workers: 4
    node_type_id: i3.xlarge
    spark_conf:
      spark.databricks.delta.preview.enabled: "true"
      spark.databricks.delta.properties.defaults.enableChangeDataFeed: "true"

libraries:
  - notebook:
      path: /Workspace/pipelines/bronze_ingestion
  - notebook:
      path: /Workspace/pipelines/silver_transformation
  - notebook:
      path: /Workspace/pipelines/gold_aggregation

configuration:
  source_path: /mnt/landing/sales
  checkpoint_path: /mnt/checkpoints/sales

continuous: false  # Set to true for continuous processing
development: false  # Set to true for development mode

notifications:
  - email_recipients:
      - data-team@company.com
    on_failure: true
    on_success: false
```

### Runtime Configuration

```python
# Access pipeline configuration in notebooks
source_path = spark.conf.get("source_path")
checkpoint_path = spark.conf.get("checkpoint_path")

@dlt.table
def configured_ingestion():
    return (
        spark.readStream
            .format("cloudFiles")
            .option("cloudFiles.format", "json")
            .load(source_path)
    )
```

## Monitoring and Observability

### Event Log Queries

```python
# Query DLT event log
event_log_path = f"{storage_location}/system/events"

events_df = (
    spark.read
        .format("delta")
        .load(event_log_path)
)

# Data quality metrics
quality_metrics = (
    events_df
        .filter(col("event_type") == "flow_progress")
        .select(
            col("timestamp"),
            col("details.flow_progress.metrics.num_output_rows").alias("output_rows"),
            col("details.flow_progress.data_quality.dropped_records").alias("dropped_records"),
            col("details.flow_progress.data_quality.expectations").alias("expectations")
        )
)

quality_metrics.show()
```

### Custom Metrics

```python
@dlt.table
def monitored_pipeline():
    df = dlt.read_stream("source_data")

    # Log custom metrics
    row_count = df.count()
    spark.conf.set("pipeline.custom_metric.row_count", row_count)

    return df
```

## Testing Strategies

### Unit Testing

```python
# tests/test_dlt_transformations.py
import pytest
from pyspark.sql import SparkSession

def test_silver_transformation():
    spark = SparkSession.builder.getOrCreate()

    # Create test data
    test_data = [
        ("1", "customer@example.com", 100.50),
        ("2", "INVALID_EMAIL", 200.00),
        ("3", None, -50.00)  # Invalid data
    ]

    df = spark.createDataFrame(test_data, ["sale_id", "email", "amount"])

    # Apply transformation logic (extracted from DLT notebook)
    result = transform_to_silver(df)

    # Assertions
    assert result.count() == 1  # Only valid records
    assert result.filter(col("email").contains("@")).count() == 1
```

### Integration Testing

```python
# tests/test_dlt_pipeline.py
def test_pipeline_expectations():
    """Test that expectations are properly defined."""
    from databricks.sdk import WorkspaceClient

    w = WorkspaceClient()

    pipeline = w.pipelines.get(pipeline_id="your-pipeline-id")
    update = w.pipelines.start_update(pipeline_id=pipeline.pipeline_id)

    # Wait for completion
    update = w.pipelines.get_update(
        pipeline_id=pipeline.pipeline_id,
        update_id=update.update_id
    )

    # Verify expectations
    assert update.state == "COMPLETED"
    assert update.data_quality_metrics.passed_records > 0
```

## Best Practices

### 1. Pipeline Organization
```
/pipelines/
  ├── bronze/
  │   ├── ingest_sales.py
  │   └── ingest_customers.py
  ├── silver/
  │   ├── validate_sales.py
  │   └── validate_customers.py
  └── gold/
      ├── daily_aggregates.py
      └── customer_features.py
```

### 2. Naming Conventions
- Use descriptive table names: `bronze_sales_raw`, `silver_sales_validated`
- Add layer prefix: `bronze_`, `silver_`, `gold_`
- Include domain: `sales`, `customers`, `products`

### 3. Data Quality Strategy
- **Bronze**: Minimal quality checks (schema validation)
- **Silver**: Comprehensive validation and cleansing
- **Gold**: Business rule validation and aggregate checks

### 4. Error Handling
```python
@dlt.table
def resilient_processing():
    return (
        dlt.read_stream("source")
            .withColumn(
                "processing_status",
                when(col("id").isNull(), "invalid")
                .when(col("amount") < 0, "invalid")
                .otherwise("valid")
            )
    )

# Separate invalid records for review
@dlt.table
def invalid_records():
    return (
        dlt.read("resilient_processing")
            .filter(col("processing_status") == "invalid")
    )
```

### 5. Performance Optimization
```python
@dlt.table(
    table_properties={
        "pipelines.autoOptimize.zOrderCols": "customer_id,order_date",
        "delta.autoOptimize.optimizeWrite": "true",
        "delta.autoOptimize.autoCompact": "true"
    }
)
def optimized_table():
    return dlt.read_stream("source")
```

## Complete Examples

See `/examples/` directory for complete implementations:
- `complete-dlt-pipeline/`: Full Bronze-Silver-Gold pipeline
- `cdc-pipeline/`: Change Data Capture with SCD Type 2
- `streaming-aggregation/`: Real-time windowed aggregations

## Common Pitfalls to Avoid

❌ **Don't:**
- Mix streaming and batch reads without understanding implications
- Forget to set appropriate expectation levels (warn/drop/fail)
- Ignore data quality metrics in event logs
- Use SELECT * in production pipelines
- Hard-code paths and configurations

✅ **Do:**
- Use parameterized configurations
- Implement comprehensive data quality checks
- Monitor pipeline metrics and SLAs
- Test transformations independently
- Document expectations and business rules
- Use appropriate clustering strategies

## Related Skills

- `medallion-architecture`: Layer design patterns
- `data-quality`: Great Expectations integration
- `testing-patterns`: Pipeline testing strategies
- `cicd-workflows`: Automated deployment

## References

- [Delta Live Tables Documentation](https://docs.databricks.com/delta-live-tables/index.html)
- [DLT Expectations](https://docs.databricks.com/delta-live-tables/expectations.html)
- [DLT API Reference](https://docs.databricks.com/dev-tools/api/python/latest/dlt.html)
- [DLT Best Practices](https://docs.databricks.com/delta-live-tables/best-practices.html)
