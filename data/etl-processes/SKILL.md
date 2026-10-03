---
name: etl-processes
description: Implement Extract, Transform, Load processes with best practices for data warehousing and analytics. Handle data quality, schema evolution, and performance.
triggers:
- /etl
- /data warehouse
---

# ETL Process Implementation

This skill covers implementing Extract, Transform, Load (ETL) processes with focus on data quality, performance, and maintainability for analytics workloads.

## When to use this skill

Use this skill when you need to:
- Build data warehouse ETL processes
- Migrate data between systems
- Prepare data for analytics and reporting
- Implement data cleansing and standardization
- Create data mart loading processes

## Prerequisites

- Source system access and understanding
- Target data warehouse design
- ETL tool or programming framework
- Understanding of data modeling (star schema, snowflake)

## Guidelines

### ETL vs ELT

**ETL (Extract, Transform, Load)**
- Transform before loading
- Best for: Complex transformations, data quality critical
- Tools: Informatica, Talend, Python pandas

**ELT (Extract, Load, Transform)**
- Load raw data first, transform in warehouse
- Best for: Cloud data warehouses, big data
- Tools: dbt, Fivetran, Matillion

### Extraction Strategies

**Full Extract**
- Extract all data every run
- Use for: Small tables, initial loads
- Cons: Resource intensive, slow

**Incremental Extract**
- Extract only changed data
- Methods: CDC, timestamp columns, checksums
- Use for: Large tables, frequent updates

```python
# Incremental extraction example
def extract_incremental(table, last_extract_time):
    query = f"""
        SELECT * FROM {table}
        WHERE updated_at > '{last_extract_time}'
        OR created_at > '{last_extract_time}'
    """
    return execute_query(query)
```

### Transformation Patterns

**Cleansing**
- Remove duplicates
- Handle null values (impute or flag)
- Standardize formats (dates, phone numbers)
- Validate against reference data

**Enrichment**
- Join with dimension tables
- Calculate derived metrics
- Add surrogate keys
- Apply business rules

**Aggregation**
- Pre-compute summaries
- Roll up to different granularities
- Pivot/unpivot data structures

### Loading Strategies

**Full Load**
- Truncate and load (for small dimensions)
- Use for: Reference data, slowly changing dimensions Type 1

**Incremental Load**
- Insert new records
- Update changed records (SCD Type 2)
- Delete orphaned records

```sql
-- SCD Type 2 implementation
MERGE INTO dim_customers AS target
USING staging_customers AS source
ON target.customer_id = source.customer_id
WHEN MATCHED AND target.hash <> source.hash THEN
    UPDATE SET end_date = CURRENT_DATE, is_current = FALSE
WHEN NOT MATCHED THEN
    INSERT (customer_id, name, email, start_date, is_current)
    VALUES (source.customer_id, source.name, source.email, CURRENT_DATE, TRUE);
```

### Data Quality Framework

**Dimensions of Data Quality**
- Completeness: Are all required fields populated?
- Uniqueness: Are there duplicate records?
- Validity: Do values conform to expected formats?
- Consistency: Is data consistent across systems?
- Timeliness: Is data fresh and up-to-date?

**Implementation**
```python
def validate_data(df):
    checks = {
        'completeness': df.notnull().mean() > 0.95,
        'uniqueness': df['id'].is_unique,
        'validity': df['email'].str.contains('@').all(),
        'freshness': df['created_at'].max() > datetime.now() - timedelta(days=1)
    }
    return checks
```

### Best Practices

**Performance Optimization**
- Use bulk loading APIs
- Process data in batches
- Implement parallel processing
- Use appropriate indexing on target tables

**Error Handling**
- Implement retry logic
- Log all transformation errors
- Continue processing valid records
- Alert on critical failures

**Monitoring**
- Track row counts (source vs target)
- Monitor job duration trends
- Alert on SLA breaches
- Maintain audit trails

## Examples

See the `examples/` directory for:
- `scd-type2.sql` - Slowly Changing Dimension implementation
- `incremental-load.py` - Change data capture pattern
- `data-quality-checks.py` - Data validation framework
- `dbt-models/` - dbt transformation models

## References

- [Kimball Data Warehouse Toolkit](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/books/)
- [dbt documentation](https://docs.getdbt.com/)
- [AWS ETL best practices](https://docs.aws.amazon.com/prescriptive-guidance/latest/load-data-warehouse-redshift/etl-process.html)
- [Data quality framework](https://www.ibm.com/topics/data-quality)
