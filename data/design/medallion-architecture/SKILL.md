---
name: medallion-architecture
description: Bronze/Silver/Gold layer design patterns and templates for building scalable data lakehouse architectures. Includes incremental processing, data quality checks, and optimization strategies.
triggers:
  - medallion architecture
  - bronze silver gold
  - data lakehouse layers
  - multi-hop architecture
category: architecture
---

# Medallion Architecture Skill

## Overview

The medallion architecture (also called multi-hop architecture) is a design pattern for organizing data in a lakehouse using three progressive layers:

- **Bronze (Raw)**: Ingested data in its original format
- **Silver (Refined)**: Cleansed and conformed data
- **Gold (Curated)**: Business-level aggregates and features

## When to Use This Skill

Use this skill when you need to:
- Design a new data pipeline with proper layering
- Migrate from traditional ETL to lakehouse architecture
- Implement incremental processing patterns
- Build a scalable data platform
- Ensure data quality at each layer

## Architecture Principles

### 1. Bronze Layer (Raw)
**Purpose**: Store raw data exactly as received from source systems

**Characteristics:**
- Immutable historical record
- Schema-on-read approach
- Metadata enrichment (_ingested_at, _source_file)
- Minimal transformations
- Full audit trail

**Use Cases:**
- Data recovery
- Reprocessing requirements
- Audit compliance
- Debugging data issues

### 2. Silver Layer (Refined)
**Purpose**: Cleansed, validated, and standardized data

**Characteristics:**
- Schema enforcement
- Data quality checks
- Deduplication
- Standardization
- Type conversions
- Business rules applied

**Use Cases:**
- Downstream analytics
- Feature engineering
- Data science modeling
- Operational reporting

### 3. Gold Layer (Curated)
**Purpose**: Business-level aggregates optimized for consumption

**Characteristics:**
- Highly aggregated
- Optimized for queries
- Business KPIs
- Feature tables
- Production-ready datasets

**Use Cases:**
- Dashboards and BI
- ML model serving
- Real-time applications
- Executive reporting

## Implementation Patterns

### Pattern 1: Batch Processing

**Bronze Layer:**
```python
def ingest_to_bronze(source_path: str, target_table: str):
    """Ingest raw data to Bronze layer."""
    df = (spark.read
        .format("cloudFiles")
        .option("cloudFiles.format", "parquet")
        .load(source_path)
        .withColumn("_ingested_at", current_timestamp())
        .withColumn("_source_file", input_file_name())
    )
    
    (df.write
        .format("delta")
        .mode("append")
        .option("mergeSchema", "true")
        .saveAsTable(target_table)
    )
```

**Silver Layer:**
```python
def process_to_silver(bronze_table: str, silver_table: str):
    """Transform Bronze to Silver with quality checks."""
    bronze_df = spark.read.table(bronze_table)
    
    silver_df = (bronze_df
        .dropDuplicates(["id"])
        .filter(col("id").isNotNull())
        .withColumn("email", lower(trim(col("email"))))
        .withColumn("created_date", to_date(col("created_at")))
        .withColumn("quality_score", 
            when(col("email").rlike(r"^[\w\.-]+@[\w\.-]+\.\w+$"), 1.0)
            .otherwise(0.5)
        )
    )
    
    (silver_df.write
        .format("delta")
        .mode("overwrite")
        .saveAsTable(silver_table)
    )
```

**Gold Layer:**
```python
def aggregate_to_gold(silver_table: str, gold_table: str):
    """Aggregate Silver to Gold business metrics."""
    silver_df = spark.read.table(silver_table)
    
    gold_df = (silver_df
        .groupBy("customer_segment", "region")
        .agg(
            count("*").alias("customer_count"),
            sum("lifetime_value").alias("total_ltv"),
            avg("quality_score").alias("avg_quality")
        )
        .withColumn("updated_at", current_timestamp())
    )
    
    (gold_df.write
        .format("delta")
        .mode("overwrite")
        .saveAsTable(gold_table)
    )
```

### Pattern 2: Incremental Processing

**Bronze (Streaming):**
```python
(spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .load(source_path)
    .withColumn("_ingested_at", current_timestamp())
    .writeStream
    .format("delta")
    .option("checkpointLocation", checkpoint_path)
    .trigger(availableNow=True)
    .toTable(bronze_table)
)
```

**Silver (Incremental Merge):**
```python
from delta.tables import DeltaTable

def incremental_silver_merge(bronze_table: str, silver_table: str, watermark: str):
    """Incrementally merge new Bronze data into Silver."""
    
    # Get new records since last watermark
    new_records = (spark.read.table(bronze_table)
        .filter(col("_ingested_at") > watermark)
    )
    
    # Transform
    transformed = transform_to_silver(new_records)
    
    # Merge into Silver
    silver = DeltaTable.forName(spark, silver_table)
    
    (silver.alias("target")
        .merge(
            transformed.alias("source"),
            "target.id = source.id"
        )
        .whenMatchedUpdateAll()
        .whenNotMatchedInsertAll()
        .execute()
    )
```

## Data Quality Patterns

### Quality Checks at Each Layer

**Bronze:**
- File completeness check
- Row count validation
- Schema drift detection

**Silver:**
- Null value checks
- Data type validation
- Business rule validation
- Referential integrity
- Duplicate detection

**Gold:**
- Aggregate accuracy
- KPI threshold checks
- Trend anomaly detection
- Completeness validation

### Quality Check Implementation

```python
def validate_silver_quality(table_name: str) -> Dict[str, bool]:
    """Run quality checks on Silver table."""
    df = spark.read.table(table_name)
    
    checks = {
        "no_null_ids": df.filter(col("id").isNull()).count() == 0,
        "valid_emails": df.filter(
            ~col("email").rlike(r"^[\w\.-]+@[\w\.-]+\.\w+$")
        ).count() == 0,
        "no_duplicates": df.count() == df.select("id").distinct().count(),
        "within_date_range": df.filter(
            (col("created_date") < "2020-01-01") |
            (col("created_date") > current_date())
        ).count() == 0
    }
    
    return checks
```

## Optimization Strategies

### Bronze Layer Optimization
```sql
-- Partition by ingestion date
CREATE TABLE bronze.raw_events
USING delta
PARTITIONED BY (ingestion_date)
AS SELECT *, current_date() as ingestion_date FROM source;

-- Enable auto-optimize
ALTER TABLE bronze.raw_events
SET TBLPROPERTIES (
    'delta.autoOptimize.optimizeWrite' = 'true',
    'delta.autoOptimize.autoCompact' = 'true'
);
```

### Silver Layer Optimization
```sql
-- Z-ORDER for common filters
OPTIMIZE silver.customers
ZORDER BY (customer_segment, region, created_date);

-- Enable Change Data Feed
ALTER TABLE silver.customers
SET TBLPROPERTIES (delta.enableChangeDataFeed = true);
```

### Gold Layer Optimization
```sql
-- Liquid clustering for query performance
CREATE TABLE gold.customer_metrics
USING delta
CLUSTER BY (customer_segment, date)
AS SELECT * FROM aggregated_metrics;

-- Optimize and vacuum
OPTIMIZE gold.customer_metrics;
VACUUM gold.customer_metrics RETAIN 168 HOURS;
```

## Complete Example

See `/templates/bronze-silver-gold/` for a complete implementation including:
- Project structure
- Bronze ingestion scripts
- Silver transformation logic
- Gold aggregation queries
- Data quality tests
- Deployment configuration

## Best Practices

1. **Idempotency**: Ensure pipelines can be re-run safely
2. **Incrementality**: Process only new/changed data
3. **Quality Gates**: Block bad data from progressing
4. **Schema Evolution**: Handle schema changes gracefully
5. **Monitoring**: Track pipeline health and data quality
6. **Documentation**: Document data lineage and transformations
7. **Testing**: Unit test transformations, integration test pipelines

## Common Pitfalls to Avoid

❌ **Don't:**
- Mix transformation logic across layers
- Skip Bronze layer to "save storage"
- Over-aggregate too early
- Ignore data quality in Silver
- Hard-code business logic in Bronze

✅ **Do:**
- Keep Bronze immutable
- Enforce quality in Silver
- Optimize Gold for consumption
- Use incremental processing
- Implement proper monitoring

## Related Skills

- `delta-live-tables`: Declarative pipeline orchestration
- `data-quality`: Great Expectations integration
- `testing-patterns`: Pipeline testing strategies
- `cicd-workflows`: Deployment automation

## References

- [Databricks Medallion Architecture](https://docs.databricks.com/lakehouse/medallion.html)
- [Delta Lake Best Practices](https://docs.delta.io/latest/best-practices.html)
