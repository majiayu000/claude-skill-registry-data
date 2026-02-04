---
name: data-lake-management
description: Data Lake architecture and management including medallion architecture (bronze/silver/gold zones), data catalog with AWS Glue, partitioning strategies, schema evolution, data quality, governance, cost optimization, S3 lifecycle policies, data retention, compliance, query optimization with Athena, data formats (Parquet, ORC, Avro), incremental processing, CDC patterns, and production best practices for scalable data lakes.
---

# Data Lake Management Skill

## Purpose

Design, build, and maintain production-grade data lakes on AWS using medallion architecture, ensuring data quality, governance, and cost optimization.

## When to Use This Skill

Auto-activates when working with:
- Data lake architecture design
- Medallion architecture (Bronze/Silver/Gold)
- AWS S3 data organization
- AWS Glue Data Catalog
- Data partitioning strategies
- Schema evolution
- Data quality and governance
- Cost optimization
- Query performance tuning

## Core Concepts

### Medallion Architecture

```
Bronze Zone (Raw)
├── Immutable source data
├── Original format
├── Minimal validation
└── Append-only

Silver Zone (Cleaned)
├── Validated and cleaned
├── Deduplicated
├── Standardized schema
└── Business rules applied

Gold Zone (Curated)
├── Aggregated
├── Business-ready
├── Optimized for queries
└── Subject-oriented
```

### S3 Data Organization

```
s3://data-lake-{env}/
├── bronze/                      # Raw zone
│   ├── source_system_1/
│   │   ├── table_name/
│   │   │   ├── year=2025/
│   │   │   │   ├── month=11/
│   │   │   │   │   ├── day=04/
│   │   │   │   │   │   └── data.parquet
│   ├── _metadata/               # Metadata and manifests
│   └── _dlq/                    # Dead letter queue
├── silver/                      # Processed zone
│   ├── domain_1/
│   │   ├── entity_name/
│   │   │   ├── date=2025-11-04/
│   │   │   │   └── part-*.parquet
├── gold/                        # Curated zone
│   ├── analytics/
│   │   ├── daily_aggregates/
│   │   ├── monthly_reports/
└── temp/                        # Temporary processing
```

## Quick Start Examples

### 1. Bronze Zone Ingestion

```python
import boto3
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime
import json

class BronzeIngestion:
    """Ingest raw data to bronze zone."""

    def __init__(self, bucket: str, source_system: str):
        self.s3 = boto3.client('s3')
        self.bucket = bucket
        self.source_system = source_system

    def ingest(self, data: list, table_name: str):
        """Ingest data with partitioning by ingestion date."""
        now = datetime.now()
        partition_path = f"year={now.year}/month={now.month:02d}/day={now.day:02d}"

        # Convert to Arrow Table
        table = pa.Table.from_pylist(data)

        # Add metadata
        metadata = {
            b'ingestion_timestamp': now.isoformat().encode(),
            b'source_system': self.source_system.encode(),
            b'record_count': str(len(data)).encode()
        }
        table = table.replace_schema_metadata(metadata)

        # Write to S3
        s3_path = f"s3://{self.bucket}/bronze/{self.source_system}/{table_name}/{partition_path}/data.parquet"

        pq.write_to_dataset(
            table,
            root_path=s3_path,
            filesystem=pa.fs.S3FileSystem(),
            compression='snappy',
            use_dictionary=True,
            write_statistics=True
        )

        # Update Glue Data Catalog
        self.update_catalog(table_name, partition_path)

    def update_catalog(self, table_name: str, partition: str):
        """Update Glue Data Catalog with new partition."""
        glue = boto3.client('glue')

        try:
            glue.create_partition(
                DatabaseName='bronze',
                TableName=f"{self.source_system}_{table_name}",
                PartitionInput={
                    'Values': partition.split('/'),
                    'StorageDescriptor': {
                        'Location': f"s3://{self.bucket}/bronze/{self.source_system}/{table_name}/{partition}/",
                        'InputFormat': 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat',
                        'OutputFormat': 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat',
                        'SerdeInfo': {
                            'SerializationLibrary': 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
                        }
                    }
                }
            )
        except glue.exceptions.AlreadyExistsException:
            pass  # Partition already exists
```

### 2. Silver Zone Processing (PySpark)

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from delta.tables import DeltaTable

class SilverZoneProcessor:
    """Process bronze to silver with Delta Lake."""

    def __init__(self):
        self.spark = (SparkSession.builder
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
            .getOrCreate())

    def process_incremental(self, bronze_table: str, silver_path: str, primary_key: str):
        """Incremental processing with deduplication and SCD Type 2."""

        # Read bronze (new records only)
        df_bronze = (self.spark.read
            .format("delta")
            .load(bronze_table)
            .filter(col("processed") == False))

        # Clean and transform
        df_cleaned = (df_bronze
            # Remove corrupt records
            .filter(col("_corrupt_record").isNull())

            # Standardize schema
            .select(
                col("id").cast("string").alias("id"),
                col("timestamp").cast("timestamp"),
                col("value").cast("double"),
                to_json(col("metadata")).alias("metadata_json")
            )

            # Add processing metadata
            .withColumn("processed_at", current_timestamp())
            .withColumn("is_active", lit(True))
            .withColumn("valid_from", col("timestamp"))
            .withColumn("valid_to", lit(None).cast("timestamp"))

            # Deduplicate (keep latest per key)
            .withColumn("row_num",
                row_number().over(
                    Window.partitionBy(primary_key)
                    .orderBy(col("timestamp").desc())
                )
            )
            .filter(col("row_num") == 1)
            .drop("row_num")
        )

        # Merge into silver (SCD Type 2)
        if DeltaTable.isDeltaTable(self.spark, silver_path):
            delta_table = DeltaTable.forPath(self.spark, silver_path)

            # Close out old records
            delta_table.alias("target").merge(
                df_cleaned.alias("source"),
                f"target.{primary_key} = source.{primary_key} AND target.is_active = true"
            ).whenMatchedUpdate(
                condition="source.timestamp > target.valid_from",
                set={
                    "is_active": "false",
                    "valid_to": "source.timestamp"
                }
            ).execute()

            # Insert new records
            delta_table.alias("target").merge(
                df_cleaned.alias("source"),
                f"target.{primary_key} = source.{primary_key} AND target.is_active = true"
            ).whenNotMatchedInsert(
                values={
                    col: f"source.{col}" for col in df_cleaned.columns
                }
            ).execute()
        else:
            # Initial load
            df_cleaned.write.format("delta").save(silver_path)

        # Mark bronze records as processed
        (df_bronze
            .withColumn("processed", lit(True))
            .write.format("delta").mode("overwrite").save(bronze_table))

        # Optimize delta table
        delta_table.optimize().executeCompaction()
```

### 3. Gold Zone Aggregation

```python
class GoldZoneAggregator:
    """Create business-ready aggregated tables."""

    def create_daily_summary(self, silver_path: str, gold_path: str, date: str):
        """Daily aggregation for analytics."""

        df_silver = spark.read.format("delta").load(silver_path)

        df_gold = (df_silver
            .filter(col("date") == date)
            .filter(col("is_active") == True)

            # Business aggregations
            .groupBy("date", "category", "region")
            .agg(
                count("*").alias("total_count"),
                sum("value").alias("total_value"),
                avg("value").alias("avg_value"),
                min("value").alias("min_value"),
                max("value").alias("max_value"),
                stddev("value").alias("stddev_value"),
                approx_count_distinct("user_id").alias("unique_users")
            )

            # Add derived metrics
            .withColumn("value_per_user", col("total_value") / col("unique_users"))

            # Add metadata
            .withColumn("created_at", current_timestamp())
            .withColumn("data_version", lit("1.0"))
        )

        # Write with overwrite for specific partition
        (df_gold.write
            .format("delta")
            .mode("overwrite")
            .option("replaceWhere", f"date = '{date}'")
            .partitionBy("date")
            .save(gold_path))

        # Create/update Athena table
        self.create_athena_table(gold_path, "daily_summary")
```

## Data Quality Framework

```python
from great_expectations.dataset import SparkDFDataset
import great_expectations as ge

class DataQualityValidator:
    """Data quality validation with Great Expectations."""

    def validate_silver_data(self, df):
        """Validate silver zone data quality."""

        ge_df = SparkDFDataset(df)

        # Schema validation
        ge_df.expect_column_to_exist("id")
        ge_df.expect_column_to_exist("timestamp")
        ge_df.expect_column_to_exist("value")

        # Data validation
        ge_df.expect_column_values_to_not_be_null("id")
        ge_df.expect_column_values_to_be_unique("id")
        ge_df.expect_column_values_to_be_between("value", min_value=0, max_value=1000000)

        # Business rules
        ge_df.expect_column_values_to_match_regex("email", r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

        # Get validation results
        results = ge_df.validate()

        if not results.success:
            failed_expectations = [exp for exp in results.results if not exp.success]
            raise DataQualityError(f"Validation failed: {failed_expectations}")

        return results
```

## Resource Files

### [resources/partitioning-strategies.md](resources/partitioning-strategies.md)
- Partition key selection
- Multi-level partitioning
- Partition pruning optimization
- Partition size management

### [resources/schema-evolution.md](resources/schema-evolution.md)
- Schema versioning
- Backward compatibility
- Column addition/removal
- Data type changes

### [resources/cost-optimization.md](resources/cost-optimization.md)
- S3 storage classes
- Lifecycle policies
- Compression formats
- Query optimization

### [resources/data-governance.md](resources/data-governance.md)
- Access control (Lake Formation)
- Data lineage tracking
- Compliance (GDPR, HIPAA)
- Data retention policies

### [resources/query-optimization.md](resources/query-optimization.md)
- Athena query tuning
- Partition pruning
- Columnar format benefits
- Caching strategies

## Best Practices

- Partition by date for time-series data
- Use Parquet with Snappy compression
- Implement schema evolution carefully
- Monitor data quality continuously
- Use Delta Lake for ACID transactions
- Implement data lineage tracking
- Set up lifecycle policies for cost control
- Use Glue Data Catalog for discoverability
- Implement incremental processing
- Monitor query costs and optimize
- Use proper access controls
- Document data schemas
- Implement data retention policies

## Common Patterns

### Incremental Processing with Bookmarks
```python
# Read with bookmark
bookmark = get_bookmark("my_job")
df_new = spark.read.parquet(source).filter(col("timestamp") > bookmark)

# Process
df_processed = transform(df_new)

# Write and update bookmark
df_processed.write.parquet(target)
update_bookmark("my_job", df_new.agg(max("timestamp")).collect()[0][0])
```

### Data Catalog Registration
```python
glue.create_table(
    DatabaseName='silver',
    TableInput={
        'Name': 'events',
        'StorageDescriptor': {
            'Columns': schema_columns,
            'Location': 's3://data-lake/silver/events/',
            'InputFormat': 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat',
            'OutputFormat': 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat',
            'SerdeInfo': {
                'SerializationLibrary': 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
            }
        },
        'PartitionKeys': [
            {'Name': 'date', 'Type': 'string'}
        ]
    }
)
```

---

**Status**: Production-Ready
**Last Updated**: 2025-11-04
**Architecture**: Medallion (Bronze → Silver → Gold)
