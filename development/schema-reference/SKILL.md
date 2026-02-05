---
name: schema-reference
description: Automatically reference and validate schemas from both legacy data sources and medallion layer data sources (bronze, silver, gold) before generating PySpark transformation code. This skill should be used proactively whenever PySpark ETL code generation is requested, ensuring accurate column names, data types, business logic, and cross-layer mappings are incorporated into the code.
---

# Schema Reference

## Overview

This skill provides comprehensive schema reference capabilities for the medallion architecture data lake. It automatically queries DuckDB warehouse, parses data dictionary files, and extracts business logic before generating PySpark transformation code. This ensures all generated code uses correct column names, data types, relationships, and business rules.

**Use this skill proactively before generating any PySpark transformation code to avoid schema errors and ensure business logic compliance.**

## Workflow

When generating PySpark transformation code, follow this workflow:

### 1. Identify Source and Target Tables

Determine which tables are involved in the transformation:
- **Bronze Layer**: Raw ingestion tables (e.g., `bronze_cms.b_cms_case`)
- **Silver Layer**: Validated tables (e.g., `silver_cms.s_cms_case`)
- **Gold Layer**: Analytical tables (e.g., `gold_data_model.g_x_mg_statsclasscount`)

### 2. Query Source Schema

Use `scripts/query_duckdb_schema.py` to get actual column names and data types from DuckDB:

```bash
python scripts/query_duckdb_schema.py \
  --database bronze_cms \
  --table b_cms_case
```

This returns:
- Column names (exact spelling and case)
- Data types (BIGINT, VARCHAR, TIMESTAMP, etc.)
- Nullable constraints
- Row count

**When to use**:
- Before reading from any table
- To verify column existence
- To understand data types for casting operations
- To check if table exists in warehouse

### 3. Extract Business Logic from Data Dictionary

Use `scripts/extract_data_dictionary.py` to read business rules and constraints:

```bash
python scripts/extract_data_dictionary.py cms_case
```

This returns:
- Column descriptions with business context
- Primary and foreign key relationships
- Default values and common patterns
- Data quality rules (e.g., "treat value 1 as NULL")
- Validation constraints

**When to use**:
- Before implementing transformations
- To understand foreign key relationships for joins
- To identify default values and data quality rules
- To extract business logic that must be implemented

### 4. Compare Schemas Between Layers

Use `scripts/schema_comparison.py` to identify transformations needed:

```bash
python scripts/schema_comparison.py \
  --source-db bronze_cms --source-table b_cms_case \
  --target-db silver_cms --target-table s_cms_case
```

This returns:
- Common columns between layers
- Columns only in source (need to be dropped or transformed)
- Columns only in target (need to be created)
- Inferred column mappings (e.g., `cms_case_id` → `s_cms_case_id`)

**When to use**:
- When transforming data between layers
- To identify required column renaming
- To discover missing columns that need to be added
- To validate transformation completeness

### 5. Reference Schema Mapping Conventions

Read `references/schema_mapping_conventions.md` for layer-specific naming patterns:
- How primary keys are renamed across layers
- Foreign key consistency rules
- Junction table naming conventions
- Legacy warehouse mapping

**When to use**:
- When uncertain about naming conventions
- When working with cross-layer joins
- When mapping to legacy warehouse schema

### 6. Reference Business Logic Patterns

Read `references/business_logic_patterns.md` for common transformation patterns:
- Extracting business logic from data dictionaries
- Choice list mapping (enum resolution)
- Deduplication strategies
- Cross-source joins
- Conditional logic implementation
- Aggregation with business rules

**When to use**:
- When implementing business rules from data dictionaries
- When applying standard transformations (deduplication, timestamp standardization)
- When creating gold layer analytical tables
- When uncertain how to implement a business rule

### 7. Generate PySpark Code

With schema and business logic information gathered, generate PySpark transformation code following the ETL class pattern:

```python
class TableName:
    def __init__(self, bronze_table_name: str):
        self.bronze_table_name = bronze_table_name
        self.silver_database_name = f"silver_{self.bronze_table_name.split('.')[0].split('_')[-1]}"
        self.silver_table_name = self.bronze_table_name.split(".")[-1].replace("b_", "s_")
        self.extract_sdf = self.extract()
        self.transform_sdf = self.transform()
        self.load()

    @synapse_error_print_handler
    def extract(self):
        logger.info(f"Extracting {self.bronze_table_name}")
        return spark.table(self.bronze_table_name)

    @synapse_error_print_handler
    def transform(self):
        logger.info(f"Transforming {self.silver_table_name}")
        sdf = self.extract_sdf
        # Apply transformations based on schema and business logic
        # 1. Rename primary key (from schema comparison)
        # 2. Apply data quality rules (from data dictionary)
        # 3. Standardize timestamps (from schema)
        # 4. Deduplicate (based on business rules)
        # 5. Add row hash (standard practice)
        return sdf

    @synapse_error_print_handler
    def load(self):
        logger.info(f"Loading {self.silver_database_name}.{self.silver_table_name}")
        TableUtilities.save_as_table(
            sdf=self.transform_sdf,
            table_name=self.silver_table_name,
            database_name=self.silver_database_name
        )
        logger.success(f"Successfully loaded {self.silver_database_name}.{self.silver_table_name}")
```

## Quick Reference

### List All Tables

See all available tables in DuckDB warehouse:

```bash
python scripts/query_duckdb_schema.py --list
python scripts/query_duckdb_schema.py --list --database silver_cms
```

### Common Use Cases

**Use Case 1: Creating a Silver Table from Bronze**

```bash
# 1. Check bronze schema
python scripts/query_duckdb_schema.py --database bronze_cms --table b_cms_case

# 2. Get business logic
python scripts/extract_data_dictionary.py cms_case

# 3. Compare with existing silver (if updating)
python scripts/schema_comparison.py \
  --source-db bronze_cms --source-table b_cms_case \
  --target-db silver_cms --target-table s_cms_case

# 4. Generate PySpark code with correct schema and business logic
```

**Use Case 2: Creating a Gold Table from Multiple Silver Tables**

```bash
# 1. Check each silver table schema
python scripts/query_duckdb_schema.py --database silver_cms --table s_cms_case
python scripts/query_duckdb_schema.py --database silver_fvms --table s_fvms_incident

# 2. Get business logic for each source
python scripts/extract_data_dictionary.py cms_case
python scripts/extract_data_dictionary.py fvms_incident

# 3. Identify join keys from foreign key relationships in data dictionaries

# 4. Generate PySpark code with cross-source joins
```

**Use Case 3: Updating an Existing Transformation**

```bash
# 1. Compare current schemas
python scripts/schema_comparison.py \
  --source-db bronze_cms --source-table b_cms_case \
  --target-db silver_cms --target-table s_cms_case

# 2. Identify new columns or changed business logic
python scripts/extract_data_dictionary.py cms_case

# 3. Update PySpark code accordingly
```

## Decision Tree

```
User requests PySpark code generation
         |
         v
    [Skill Activated]
         |
         v
    What layer transformation?
         |
    +----+----+----+
    |    |    |    |
Bronze Silver Gold Other
    |    |    |    |
    v    v    v    v
Query schema for all involved tables
         |
         v
Extract business logic from data dictionaries
         |
         v
Compare schemas if transforming between layers
         |
         v
Reference mapping conventions and business logic patterns
         |
         v
Generate PySpark code with:
  - Correct column names
  - Proper data types
  - Business logic implemented
  - Standard error handling
  - Proper logging
```

## Key Principles

1. **Always verify schemas first**: Never assume column names or types without querying

2. **Extract business logic from data dictionaries**: Business rules must be implemented, not guessed

3. **Follow naming conventions**: Use schema mapping conventions for layer-specific prefixes

4. **Use TableUtilities**: Leverage existing utility methods for common operations

5. **Apply standard patterns**: Follow the ETL class pattern and use standard decorators

6. **Log comprehensively**: Include table/database names in all log messages

7. **Handle errors gracefully**: Use `@synapse_error_print_handler` decorator

## Environment Setup

### Prerequisites

- DuckDB warehouse must exist at `/workspaces/data/warehouse.duckdb`
- Data dictionary files must exist at `.claude/data_dictionary/`
- Python packages: `duckdb` (for schema querying)

### Verify Setup

```bash
# Check DuckDB warehouse exists
ls -la /workspaces/data/warehouse.duckdb

# Check data dictionary exists
ls -la .claude/data_dictionary/

# Build DuckDB warehouse if missing
make build_duckdb
```

## Resources

### scripts/

This skill includes three Python scripts for schema querying and analysis:

**`query_duckdb_schema.py`**
- Query DuckDB warehouse for table schemas
- List all tables in a database or across all databases
- Get column names, data types, nullability, and row counts
- Executable without loading into context

**`extract_data_dictionary.py`**
- Parse data dictionary markdown files
- Extract schema information, business logic, and constraints
- Show primary key and foreign key relationships
- Identify default values and data quality rules

**`schema_comparison.py`**
- Compare schemas between layers (bronze → silver → gold)
- Identify common columns, source-only columns, target-only columns
- Infer column mappings based on naming conventions
- Validate transformation completeness

### references/

This skill includes two reference documents for detailed guidance:

**`schema_mapping_conventions.md`**
- Medallion architecture layer structure and conventions
- Primary key and foreign key naming patterns
- Table naming conventions across layers
- Legacy warehouse mapping rules
- Common transformation patterns between layers

**`business_logic_patterns.md`**
- How to extract business logic from data dictionary descriptions
- Common transformation patterns (deduplication, choice lists, timestamps)
- ETL class pattern implementation with business logic
- Testing business logic before deployment
- Logging and error handling best practices

---

**Note**: This skill automatically activates when PySpark transformation code generation is requested. Scripts are used as needed to query schemas and extract business logic before code generation.
