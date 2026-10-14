---
name: 02-merge-patterns
description: Provides production-grade patterns for Gold layer MERGE operations from Silver to Gold tables. Covers column mapping, schema evolution, SCD Type 1/2 patterns, fact table aggregation, and preventing variable naming conflicts with PySpark functions. Use when creating Gold layer MERGE operations, handling column name differences between Silver and Gold, implementing SCD Type 1/2 dimensions, aggregating fact tables, or troubleshooting MERGE errors. Triggers on "Gold merge", "MERGE operation", "upsert Gold", "SCD Type 1", "SCD Type 2", "fact table merge", "Silver to Gold", "column mapping", "schema evolution".
license: Apache-2.0
clients: [ide_cli, genie_code]
bundle_resource: jobs
deploy_verb: bundle_deploy
deploy_note: "Pattern consumed by the Gold merge jobs (notebook_task); deploy via `bundle deploy --target dev` (runDatabricksCli on Genie Code). MERGE src view must .select() every Gold column with lit(None) placeholders for YAML-only columns."
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "1.0.0"
  domain: gold
  role: worker
  pipeline_stage: 4
  pipeline_stage_name: gold-implementation
  called_by:
    - gold-layer-setup
  standalone: true
  last_verified: "2026-02-07"
  volatility: low
  upstream_sources: []  # Stable MERGE SQL patterns
---

# Gold Layer MERGE Patterns

## Core Principle: Schema-Aware Transformations

Gold layer merge operations read from Silver and must handle:
1. Column name differences
2. Data type transformations
3. Business logic calculations
4. SCD Type 2 tracking

## Column Name Mapping Pattern

### Problem: Column Names Differ Between Layers

**Example:** Silver has `company_rcn`, but Gold expects `company_retail_control_number`

### ❌ DON'T: Reference non-existent columns
```python
updates_df = (
    silver_df
    .select(
        "store_number",
        "company_retail_control_number",  # ❌ This column doesn't exist in Silver!
        # ...
    )
)
```

### ✅ DO: Map columns explicitly with withColumn
```python
updates_df = (
    silver_df
    # Map Silver column to Gold column name
    .withColumn("company_retail_control_number", col("company_rcn"))
    .select(
        "store_number",
        "company_retail_control_number",  # ✅ Now this exists
        # ...
    )
)
```

## Variable Naming Conflicts

### Problem: Import Conflicts with Local Variables

**Critical Rule:** NEVER name local variables the same as imported PySpark functions.

### ❌ DON'T: Shadow imported functions
```python
from pyspark.sql.functions import count

def merge_data():
    # Later in the code...
    count = updates_df.count()  # ❌ Shadows the imported 'count' function!
    
    # This will fail:
    df.agg(count("*"))  # Error: 'int' object is not callable
```

### ✅ DO: Use descriptive variable names
```python
from pyspark.sql.functions import count

def merge_data():
    record_count = updates_df.count()  # ✅ No conflict
    
    # This works:
    df.agg(count("*"))  # ✅ Uses the imported function
```

### Common PySpark Functions to Avoid as Variable Names
- `count` → use `record_count`, `row_count`, `num_records`
- `sum` → use `total`, `sum_value`, `aggregated_sum`
- `min` → use `min_value`, `minimum`
- `max` → use `max_value`, `maximum`
- `round` → use `rounded_value`, `result`
- `filter` → use `filtered_df`, `subset`

## Merge Operation Patterns

### SCD Type 1 (Overwrite)

**Use for:** Dimension tables where history doesn't matter

**Template:** See [assets/templates/scd-type1-merge.py](assets/templates/scd-type1-merge.py) for complete pattern.

```python
def merge_dim_product(spark: SparkSession, catalog: str, silver_schema: str, gold_schema: str):
    """Merge dim_product from Silver to Gold (SCD Type 1)."""
    
    silver_table = f"{catalog}.{silver_schema}.silver_product_dim"
    gold_table = f"{catalog}.{gold_schema}.dim_product"
    
    silver_df = spark.table(silver_table)
    
    # Prepare updates with column mappings
    updates_df = (
        silver_df
        .withColumn("product_key", col("upc_code"))  # Business key
        .withColumn("record_updated_timestamp", current_timestamp())
        .select(
            "product_key", "upc_code", "product_description",
            # ... other columns
            "record_updated_timestamp"
        )
    )
    
    delta_gold = DeltaTable.forName(spark, gold_table)
    
    # SCD Type 1: Update all fields when matched
    delta_gold.alias("target").merge(
        updates_df.alias("source"),
        "target.product_key = source.product_key"
    ).whenMatchedUpdateAll(
    ).whenNotMatchedInsertAll(
    ).execute()
    
    record_count = updates_df.count()  # ✅ Good variable name
    print(f"✓ Merged {record_count} records into dim_product")
```

### SCD Type 2 (Historical Tracking)

**Use for:** Dimension tables where you need to track changes over time

**Template:** See [assets/templates/scd-type2-merge.py](assets/templates/scd-type2-merge.py) for complete pattern.

```python
def merge_dim_store(spark: SparkSession, catalog: str, silver_schema: str, gold_schema: str):
    """Merge dim_store from Silver to Gold (SCD Type 2)."""
    
    silver_table = f"{catalog}.{silver_schema}.silver_store_dim"
    gold_table = f"{catalog}.{gold_schema}.dim_store"
    
    silver_df = spark.table(silver_table)
    
    updates_df = (
        silver_df
        # Generate surrogate key
        .withColumn("store_key", md5(concat_ws("||", col("store_id"), col("processed_timestamp"))))
        
        # SCD Type 2 columns
        .withColumn("effective_from", col("processed_timestamp"))
        .withColumn("effective_to", lit(None).cast("timestamp"))
        .withColumn("is_current", lit(True))
        
        # Derived columns
        .withColumn("store_status", 
                   when(col("close_date").isNotNull(), "Closed").otherwise("Active"))
        
        # Column mappings
        .withColumn("company_retail_control_number", col("company_rcn"))
        
        # Timestamps
        .withColumn("record_created_timestamp", current_timestamp())
        .withColumn("record_updated_timestamp", current_timestamp())
        
        .select(
            "store_key", "store_number", "store_name",
            "company_retail_control_number",  # Mapped column
            "effective_from", "effective_to", "is_current",
            # ... other columns
        )
    )
    
    delta_gold = DeltaTable.forName(spark, gold_table)
    
    # SCD Type 2: Only update timestamp for current records
    delta_gold.alias("target").merge(
        updates_df.alias("source"),
        "target.store_number = source.store_number AND target.is_current = true"
    ).whenMatchedUpdate(set={
        "record_updated_timestamp": "source.record_updated_timestamp"
    }).whenNotMatchedInsertAll(
    ).execute()
    
    record_count = updates_df.count()
    print(f"✓ Merged {record_count} records into dim_store")
```

### Fact Table Aggregation

**Use for:** Pre-aggregated fact tables from transactional Silver data

**Template:** See [assets/templates/fact-table-aggregation-merge.py](assets/templates/fact-table-aggregation-merge.py) for complete pattern.

```python
def merge_fact_sales_daily(spark: SparkSession, catalog: str, silver_schema: str, gold_schema: str):
    """Merge fact_sales_daily from Silver to Gold."""
    
    silver_table = f"{catalog}.{silver_schema}.silver_transactions"
    gold_table = f"{catalog}.{gold_schema}.fact_sales_daily"
    
    transactions = spark.table(silver_table)
    
    # Aggregate daily sales
    daily_sales = (
        transactions
        .groupBy("store_number", "upc_code", "transaction_date")
        .agg(
            spark_sum(when(col("quantity_sold") > 0, col("final_sales_price")).otherwise(0)).alias("gross_revenue"),
            spark_sum(col("final_sales_price")).alias("net_revenue"),
            spark_sum(when(col("quantity_sold") > 0, col("quantity_sold")).otherwise(0)).alias("units_sold"),
            count("*").alias("transaction_count"),  # ✅ PySpark function
            # ... more aggregations
        )
        .withColumn("record_created_timestamp", current_timestamp())
        .withColumn("record_updated_timestamp", current_timestamp())
    )
    
    delta_gold = DeltaTable.forName(spark, gold_table)
    
    delta_gold.alias("target").merge(
        daily_sales.alias("source"),
        """target.store_number = source.store_number 
           AND target.upc_code = source.upc_code 
           AND target.transaction_date = source.transaction_date"""
    ).whenMatchedUpdate(set={
        "net_revenue": "source.net_revenue",
        "units_sold": "source.units_sold",
        "transaction_count": "source.transaction_count",
        "record_updated_timestamp": "source.record_updated_timestamp"
    }).whenNotMatchedInsertAll(
    ).execute()
    
    record_count = daily_sales.count()  # ✅ Good variable name
    print(f"✓ Merged {record_count} records into fact_sales_daily")
```

## Schema Evolution Handling

### Data Type Changes

```python
# Example: INT to BIGINT migration
.withColumn("quantity_sold", col("quantity_sold").cast("bigint"))

# Example: DECIMAL to DOUBLE migration
.withColumn("price", col("price").cast("double"))
```

### Adding Derived Columns

```python
# Always calculate in the merge script, not in the target table
.withColumn("total_discount",
           coalesce(col("multi_unit_discount"), lit(0)) +
           coalesce(col("coupon_discount"), lit(0)) +
           coalesce(col("loyalty_discount"), lit(0)))
```

## Error Handling Pattern

```python
def main():
    """Main entry point for Gold layer MERGE operations."""
    
    catalog, silver_schema, gold_schema = get_parameters()
    
    spark = SparkSession.builder.appName("Gold Layer MERGE").getOrCreate()
    
    try:
        # Merge dimensions
        merge_dim_store(spark, catalog, silver_schema, gold_schema)
        merge_dim_product(spark, catalog, silver_schema, gold_schema)
        merge_dim_date(spark, catalog, silver_schema, gold_schema)
        
        # Merge facts
        merge_fact_sales_daily(spark, catalog, silver_schema, gold_schema)
        merge_fact_inventory_snapshot(spark, catalog, silver_schema, gold_schema)
        
        print("\n" + "=" * 80)
        print("✓ Gold layer MERGE completed successfully!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error during Gold layer MERGE: {str(e)}")
        raise
        
    finally:
        spark.stop()
```

## Validation Checklist

Before deploying Gold merge scripts:
- [ ] All Silver column references exist
- [ ] Column mappings are explicit (using `.withColumn()`)
- [ ] No variable names shadow PySpark functions
- [ ] MERGE conditions use correct join keys
- [ ] SCD Type 2 includes `is_current` filter
- [ ] Timestamps are added (`record_created_timestamp`, `record_updated_timestamp`)
- [ ] Error handling with try/except
- [ ] Meaningful print statements for monitoring

## Common Errors and Solutions

### Error: `Column 'X' does not exist`
**Solution:** Check Silver table schema. Add explicit column mapping if names differ.

### Error: `'int' object is not callable` 
**Solution:** Variable name shadows a PySpark function. Rename the variable.

### Error: `Cartesian product detected`
**Solution:** MERGE condition is missing or incorrect. Add proper join keys.

### Error: Schema mismatch during MERGE
**Solution:** Cast columns to match target table schema explicitly.

## References
- [Delta Lake MERGE](https://docs.delta.io/latest/delta-update.html#upsert-into-a-table-using-merge)
- [SCD Type 2 Patterns](https://www.databricks.com/blog/2022/08/22/dimensional-modeling-delta-lake-how-to-manage-slowly-changing-dimensions.html)

---

## Additional Merge Patterns

Beyond the core SCD Type 1/2 and fact aggregation patterns above, these advanced patterns handle specialized table types identified during Gold layer design.

**Design-Driven Pattern Selection:** Select the correct merge pattern based on YAML `table_properties`:

| YAML `grain_type` | YAML `dimension_pattern` | Pattern | Template |
|---|---|---|---|
| `transaction` or `aggregated` | — | Standard fact aggregation | `fact-table-aggregation-merge.py` |
| `accumulating_snapshot` | — | Milestone progression | `accumulating-snapshot-merge.py` |
| `factless` | — | INSERT-only (no measures) | `factless-fact-merge.py` |
| `periodic_snapshot` | — | Full period replacement | `periodic-snapshot-merge.py` |
| — | `junk` | DISTINCT flag extraction | `junk-dimension-populate.py` |
| — | (standard) + `scd_type: 1` | SCD Type 1 | `scd-type1-merge.py` |
| — | (standard) + `scd_type: 2` | SCD Type 2 | `scd-type2-merge.py` |

**Accumulating Snapshot:** Rows are UPDATED as milestones are reached. Milestone columns (e.g., `ship_date`) start NULL and fill in. Lag/duration columns recalculated on each update. See `assets/templates/accumulating-snapshot-merge.py`.

**Factless Fact:** No measure columns — row existence IS the fact. Simple MERGE with INSERT only. COUNT(*) computed in BI layer. See `assets/templates/factless-fact-merge.py`.

**Periodic Snapshot:** One row per entity per snapshot period. Full replacement of each period. Semi-additive measures should NOT be summed across time. See `assets/templates/periodic-snapshot-merge.py`.

**Junk Dimension:** Extract DISTINCT flag combinations from Silver, generate MD5 surrogate key per combination. INSERT only — flag definitions are immutable. See `assets/templates/junk-dimension-populate.py`.

For detailed implementation guidance and checklists, see `01-gold-layer-setup/references/advanced-merge-patterns.md`.

## Reference Files

This skill includes the following template files:

- **assets/templates/scd-type1-merge.py** - Complete SCD Type 1 merge pattern template
- **assets/templates/scd-type2-merge.py** - Complete SCD Type 2 merge pattern template
- **assets/templates/fact-table-aggregation-merge.py** - Fact table aggregation merge template
- **assets/templates/accumulating-snapshot-merge.py** - Accumulating snapshot fact merge template
- **assets/templates/factless-fact-merge.py** - Factless fact table merge template
- **assets/templates/periodic-snapshot-merge.py** - Periodic snapshot fact merge template
- **assets/templates/junk-dimension-populate.py** - Junk dimension population template

---

## Inputs

- Created Gold tables (from `pipeline-workers/01-yaml-table-setup`)
- Silver source tables (from Silver layer DLT pipelines)
- YAML metadata: table inventory from `build_inventory()`, column mappings from `load_column_mappings_from_yaml()`
- COLUMN_LINEAGE.csv for Silver-to-Gold renames

## Outputs

- Populated Gold dimension tables (SCD Type 1 or Type 2)
- Populated Gold fact tables (aggregated or transaction-level)
- Merge execution logs with record counts, deduplication stats

## Pipeline Notes to Carry Forward

- Use `pipeline-workers/03-deduplication` BEFORE every MERGE call (mandatory)
- Merge dimensions FIRST, then facts (dependency order from YAML `foreign_keys`)
- Column mappings extracted from YAML lineage — never hardcode Silver-to-Gold renames
- `spark_sum` alias for `sum` to avoid Python builtin shadowing

## Next Step

Use `pipeline-workers/03-deduplication` before every MERGE call. For fact tables, also use `pipeline-workers/04-grain-validation` after deduplication.
