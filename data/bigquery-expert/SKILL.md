---
name: bigquery-expert
description: BigQuery Expert Engineer Skill - Comprehensive guide for GoogleSQL queries, data management, performance optimization, and cost management
---

# BigQuery Expert Engineer Skill

This skill provides a comprehensive guide for BigQuery development.

## 1. bq Command Line Tool Basics

### 1.1. Query Execution

```sh
# Execute query with Standard SQL
bq query --use_legacy_sql=false 'SELECT * FROM `project.dataset.table` LIMIT 10'

# Output results in CSV format
bq query --use_legacy_sql=false --format=csv 'SELECT * FROM `project.dataset.table`'

# Dry run (cost estimation)
bq query --use_legacy_sql=false --dry_run 'SELECT * FROM `project.dataset.table`'

# Save results to table
bq query --use_legacy_sql=false --destination_table=project:dataset.result_table 'SELECT * FROM `project.dataset.table`'
```

### 1.2. Table Operations

```sh
# List tables
bq ls project:dataset

# Check table schema
bq show --schema --format=prettyjson project:dataset.table

# Create table (from schema file)
bq mk --table project:dataset.table schema.json

# Create partitioned table
bq mk --table --time_partitioning_field=created_at project:dataset.table schema.json

# Create clustered table
bq mk --table --clustering_fields=user_id,category project:dataset.table schema.json

# Delete table
bq rm -t project:dataset.table
```

### 1.3. Data Load/Export

```sh
# Load from CSV
bq load --source_format=CSV project:dataset.table gs://bucket/data.csv schema.json

# Load from JSON
bq load --source_format=NEWLINE_DELIMITED_JSON project:dataset.table gs://bucket/data.json

# Load from Parquet (auto-detect schema)
bq load --source_format=PARQUET --autodetect project:dataset.table gs://bucket/data.parquet

# Export to Cloud Storage
bq extract --destination_format=CSV project:dataset.table gs://bucket/export/*.csv
```

## 2. GoogleSQL Basic Syntax

### 2.1. SELECT Statement

```sql
-- Basic SELECT
SELECT
  column1,
  column2,
  COUNT(*) AS count
FROM
  `project.dataset.table`
WHERE
  date >= '2024-01-01'
GROUP BY
  column1, column2
HAVING
  COUNT(*) > 10
ORDER BY
  count DESC
LIMIT 100
```

### 2.2. Common Functions

```sql
-- String functions
CONCAT(str1, str2)
LOWER(str), UPPER(str)
TRIM(str), LTRIM(str), RTRIM(str)
SUBSTR(str, start, length)
REGEXP_CONTAINS(str, r'pattern')
REGEXP_EXTRACT(str, r'pattern')
SPLIT(str, delimiter)

-- Date/time functions
CURRENT_DATE(), CURRENT_TIMESTAMP()
DATE(timestamp), TIMESTAMP(date)
DATE_ADD(date, INTERVAL 1 DAY)
DATE_DIFF(date1, date2, DAY)
FORMAT_DATE('%Y-%m-%d', date)
PARSE_DATE('%Y%m%d', str)
EXTRACT(YEAR FROM date)

-- Aggregate functions
COUNT(*), COUNT(DISTINCT column)
SUM(column), AVG(column)
MIN(column), MAX(column)
ARRAY_AGG(column)
STRING_AGG(column, ',')

-- Window functions
ROW_NUMBER() OVER (PARTITION BY col ORDER BY col2)
RANK() OVER (ORDER BY col DESC)
LAG(col, 1) OVER (ORDER BY date)
LEAD(col, 1) OVER (ORDER BY date)
SUM(col) OVER (PARTITION BY category)
```

### 2.3. JOIN Syntax

```sql
-- INNER JOIN
SELECT a.*, b.column
FROM `project.dataset.table_a` AS a
INNER JOIN `project.dataset.table_b` AS b
  ON a.id = b.id

-- LEFT JOIN
SELECT a.*, b.column
FROM `project.dataset.table_a` AS a
LEFT JOIN `project.dataset.table_b` AS b
  ON a.id = b.id

-- CROSS JOIN (commonly used for array expansion)
SELECT *
FROM `project.dataset.table`,
UNNEST(array_column) AS element
```

### 2.4. CTE (Common Table Expressions)

```sql
WITH
  base_data AS (
    SELECT *
    FROM `project.dataset.table`
    WHERE date >= '2024-01-01'
  ),
  aggregated AS (
    SELECT
      category,
      COUNT(*) AS count
    FROM base_data
    GROUP BY category
  )
SELECT *
FROM aggregated
ORDER BY count DESC
```

## 3. Table Design

### 3.1. Partitioning

Divide data by date to reduce query scan volume.

```sql
-- Create date-partitioned table
CREATE TABLE `project.dataset.partitioned_table`
PARTITION BY DATE(created_at)
AS SELECT * FROM `project.dataset.source_table`;

-- Integer partitioning
CREATE TABLE `project.dataset.int_partitioned`
PARTITION BY RANGE_BUCKET(user_id, GENERATE_ARRAY(0, 1000000, 10000))
AS SELECT * FROM source;

-- Require partition filter
CREATE TABLE `project.dataset.table`
PARTITION BY DATE(created_at)
OPTIONS (
  require_partition_filter = TRUE
);
```

### 3.2. Clustering

Sort and group data by specified columns.

```sql
-- Clustering table
CREATE TABLE `project.dataset.clustered_table`
PARTITION BY DATE(created_at)
CLUSTER BY user_id, category
AS SELECT * FROM source;
```

### 3.3. Best Practices

- Combine partitioning and clustering
- Choose columns frequently filtered in queries
- Maximum 4 clustering columns
- Prioritize high-cardinality columns

## 4. Performance Optimization

### 4.1. Query Optimization

```sql
-- Avoid SELECT *
-- Bad
SELECT * FROM table;
-- Good
SELECT column1, column2 FROM table;

-- Leverage partition pruning
-- Bad (function applied to partition column)
WHERE DATE(created_at) = '2024-01-01'
-- Good
WHERE created_at >= '2024-01-01' AND created_at < '2024-01-02'

-- Use APPROX_ functions for estimates (faster)
SELECT APPROX_COUNT_DISTINCT(user_id) FROM table;
```

### 4.2. JOIN Optimization

```sql
-- Put smaller table on right side (broadcast JOIN)
SELECT *
FROM large_table
JOIN small_table ON large_table.id = small_table.id;

-- JOIN only needed columns
WITH filtered AS (
  SELECT id, needed_column FROM large_table WHERE condition
)
SELECT * FROM filtered JOIN other_table ON ...
```

### 4.3. Check Slot Usage

```sql
-- Check job statistics
SELECT
  job_id,
  total_bytes_processed,
  total_slot_ms,
  TIMESTAMP_DIFF(end_time, start_time, SECOND) AS duration_sec
FROM `region-us`.INFORMATION_SCHEMA.JOBS
WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
ORDER BY total_slot_ms DESC
LIMIT 10;
```

## 5. Cost Management

### 5.1. Pricing Model

- On-demand: Based on scanned data ($5/TB)
- Flat-rate (Editions): Based on reserved slots
- Storage: Active $0.02/GB, Long-term $0.01/GB

### 5.2. Cost Reduction Best Practices

1. Avoid SELECT *
2. Always use partition filters
3. Check cost with dry run before queries
4. Optimize repeated queries with materialized views
5. Speed up dashboard queries with BI Engine

### 5.3. Custom Quota Settings

```sql
-- Set query byte limit per project
-- Configure in Cloud Console or gcloud
```

## 6. Data Governance

### 6.1. IAM Roles

- `roles/bigquery.admin`: Full permissions
- `roles/bigquery.dataEditor`: Read/write data
- `roles/bigquery.dataViewer`: Read-only data
- `roles/bigquery.jobUser`: Execute jobs
- `roles/bigquery.user`: List datasets, execute jobs

### 6.2. Column-level Security

```sql
-- Apply policy tag
ALTER TABLE `project.dataset.table`
ALTER COLUMN sensitive_column
SET OPTIONS (policy_tags = ['projects/project/locations/us/taxonomies/123/policyTags/456']);
```

### 6.3. Row-level Security

```sql
-- Create row access policy
CREATE ROW ACCESS POLICY region_filter
ON `project.dataset.table`
GRANT TO ('user:analyst@example.com')
FILTER USING (region = 'APAC');
```

## 7. BigQuery ML

### 7.1. Model Creation

```sql
-- Linear regression model
CREATE OR REPLACE MODEL `project.dataset.model`
OPTIONS (
  model_type = 'LINEAR_REG',
  input_label_cols = ['target']
) AS
SELECT feature1, feature2, target
FROM `project.dataset.training_data`;

-- Logistic regression model
CREATE OR REPLACE MODEL `project.dataset.classifier`
OPTIONS (
  model_type = 'LOGISTIC_REG',
  input_label_cols = ['label']
) AS
SELECT * FROM training_data;
```

### 7.2. Model Evaluation and Prediction

```sql
-- Model evaluation
SELECT * FROM ML.EVALUATE(MODEL `project.dataset.model`);

-- Prediction
SELECT *
FROM ML.PREDICT(
  MODEL `project.dataset.model`,
  (SELECT * FROM `project.dataset.new_data`)
);
```

## 8. External Data Sources

### 8.1. External Tables

```sql
-- Reference Cloud Storage CSV as external table
CREATE EXTERNAL TABLE `project.dataset.external_table`
OPTIONS (
  format = 'CSV',
  uris = ['gs://bucket/path/*.csv'],
  skip_leading_rows = 1
);

-- Parquet external table
CREATE EXTERNAL TABLE `project.dataset.parquet_table`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bucket/path/*.parquet']
);
```

### 8.2. Federated Query

```sql
-- Connect to Cloud SQL
SELECT * FROM EXTERNAL_QUERY(
  'projects/project/locations/us/connections/connection_id',
  'SELECT * FROM mysql_table'
);
```

## 9. Scheduled Queries

### 9.1. Configuration Example

```sql
-- Configure in Cloud Console or bq command
-- Run daily at 2 AM
bq query --use_legacy_sql=false \
  --schedule='every 24 hours' \
  --display_name='Daily aggregation' \
  --destination_table='project:dataset.daily_summary' \
  --replace \
  'SELECT DATE(created_at) as date, COUNT(*) as count FROM source GROUP BY 1'
```

## 10. Detailed Documentation

See `docs/` directory for supplementary documentation.

## 11. Reference Links

- Official docs: <https://cloud.google.com/bigquery/docs>
- GoogleSQL reference: <https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax>
- Function reference: <https://cloud.google.com/bigquery/docs/reference/standard-sql/functions-all>
- bq command reference: <https://cloud.google.com/bigquery/docs/bq-command-line-tool>
- BigQuery ML: <https://cloud.google.com/bigquery/docs/bqml-introduction>
- Pricing: <https://cloud.google.com/bigquery/pricing>
