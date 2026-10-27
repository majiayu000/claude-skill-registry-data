---
name: data-pipeline-etl
description: "ETL/ELT data pipelines, data lakehouse architecture, Apache Spark/DuckDB transformations, and data quality checks."
---

# Data Pipeline (ETL/ELT) Protocol

1. Extract raw data into immutable bronze/raw storage layers.
2. Transform using DuckDB or Spark with idempotent partition overwrites.
3. Validate data quality rules (Great Expectations, Soda) before publishing to gold analytics layers.
