---
name: query-writer
description: Use this skill when writing or updating SQL queries (query.sql) or Python ETL scripts (query.py) following Mozilla BigQuery ETL conventions. ALWAYS checks for and updates existing tests when modifying queries. Coordinates downstream updates to schemas and tests. Works with bigquery-etl-core, metadata-manager, and sql-test-generator skills.
---

# Query Writer

**Composable:** Works with bigquery-etl-core (for conventions), metadata-manager (for schemas), and sql-test-generator (for tests)
**When to use:** Writing or updating SQL queries (query.sql) or Python ETL scripts (query.py) following Mozilla BigQuery ETL conventions

## Overview

Generate and update SQL queries and Python ETL scripts for the bigquery-etl repository following Mozilla's conventions. This skill handles:
- Writing new query.sql or query.py files
- Updating existing queries
- **MANDATORY: Checking for and updating existing tests whenever queries are modified**
- Coordinating downstream updates to schemas (via metadata-manager) and tests (via sql-test-generator)

## 🚨 REQUIRED READING - Start Here

**BEFORE writing any query, READ these reference files to understand patterns:**

1. **SQL Conventions:** READ `references/sql_formatting_conventions.md`
   - Mozilla's formatting standards
   - Naming conventions
   - Code organization

2. **Common Patterns:** READ `references/common_query_patterns.md`
   - Standard query structures for different use cases
   - When to use CTEs vs subqueries
   - Aggregation patterns

3. **Partitioning:** READ `references/partitioning_patterns.md`
   - Incremental vs full refresh
   - Date partitioning requirements
   - Parameter usage

## 📋 Templates - Copy These Structures

**When writing queries, READ and COPY from these template files:**

**For SQL Queries:**
- **Basic aggregation?** → READ `assets/basic_query_example.sql`
- **Need CTEs?** → READ `assets/cte_query_example.sql`
- **Joining tables?** → READ `assets/join_example.sql`
- **UNNESTing arrays?** → READ `assets/unnest_example.sql`
- **User-level aggregation?** → READ `assets/user_aggregation_example.sql`

**For Python Queries:**
- **API calls or complex logic?** → READ `assets/python_query_template.py`
- Also READ `references/python_queries.md` for Python-specific patterns

## Schema and Description Lookups for Query Construction

When writing queries, you need both schemas (column names/types) and descriptions. **These come from different sources:**

### Schema Priority (Column Names & Types):
1. **FIRST:** Check local `schema.yaml` files in `sql/` directory
2. **LAST RESORT:** Use DataHub when schema not available locally

### Description Priority:
1. **FIRST:** Check Glean Dictionary for `_live`/`_stable` tables (https://dictionary.telemetry.mozilla.org/)
2. **SECOND:** Check local `metadata.yaml` files in `sql/` directory
3. **LAST RESORT:** Use DataHub when descriptions not available

**IMPORTANT:** Glean Dictionary provides **descriptions ONLY**, not schemas. For schemas of `_live`/`_stable` tables, use local `schema.yaml` files or DataHub.

**When to use each source:**
- **Local `/sql` files:** For schemas and metadata of any derived tables in bqetl (most common)
- **Glean Dictionary:** For descriptions of raw ingestion tables (`_live`, `_stable`) ONLY
- **DataHub:** Last resort for schemas when not available locally, or for descriptions when not in Glean/local files

## 🚨 Configuration Standards

**CRITICAL: Only use documented patterns and configurations!**

When writing queries, **ONLY use query patterns, SQL conventions, and partitioning configurations that are documented in:**
- Reference files in this skill (`references/` directory)
- Example queries in this skill (`assets/` directory)
- Existing patterns found in the `/sql` directory

**DO NOT:**
- Invent new query patterns or configurations that aren't documented
- Assume BigQuery features work the same as other SQL dialects
- Use undocumented partitioning or clustering configurations

**ALWAYS reference existing patterns** in the `/sql` directory to see how similar queries are structured.

**Typical workflow for this skill:**

1. **Gather requirements** - Use model-requirements skill if needed to understand what to build
2. **Write query** - Using this skill (query-writer) following Mozilla conventions
3. **Format query** - Run `./bqetl format <path>` to ensure proper SQL formatting
4. **Validate query** - Run `./bqetl query validate <path>` to check SQL syntax and conventions
5. **Generate schema/metadata** - Use metadata-manager skill to create schema.yaml and metadata.yaml (ONLY if validation passes)
6. **🚨 MANDATORY: Check for and update tests** - ALWAYS look for existing tests and update/create them (see Test Management section below)

## Quick Start

### SQL or Python?

**Use query.sql for:**
- Standard data transformations (95% of tables)
- Aggregations and GROUP BY operations
- Joins, CTEs, window functions
- Standard BigQuery operations

**Use query.py for:**
- API calls to external services
- Complex pandas transformations
- Multi-project queries or INFORMATION_SCHEMA operations
- Custom business logic clearer in Python

### Basic SQL Structure

```sql
-- Brief comment explaining the query's purpose
SELECT
  submission_date,
  sample_id,
  client_id,
  COUNT(*) AS n_total_events,
FROM
  `moz-fx-data-shared-prod.telemetry.events`
WHERE
  submission_date = @submission_date
GROUP BY
  submission_date,
  sample_id,
  client_id
```

**Key conventions:**
- Uppercase SQL keywords
- 2-space indentation
- Each field on its own line
- Always filter on `submission_date = @submission_date` for incremental queries

### Partitioning Requirements

**Incremental queries (most common):**
- Accept `@submission_date` parameter
- Output `submission_date` column matching parameter
- Filter: `WHERE submission_date = @submission_date`

**Full refresh queries:**
- No `@submission_date` parameter
- Set `date_partition_parameter: null` in metadata.yaml

## SQL Formatting

**ALWAYS format SQL queries using the bqetl formatter:**

```bash
# Format a specific query file
./bqetl format sql/moz-fx-data-shared-prod/telemetry_derived/events_daily_v1/query.sql

# Format an entire query directory
./bqetl format sql/moz-fx-data-shared-prod/telemetry_derived/events_daily_v1/

# Check if formatting is correct without modifying files
./bqetl format --check sql/moz-fx-data-shared-prod/telemetry_derived/events_daily_v1/
```

**Why formatting matters:**
- Ensures consistent code style across the repository
- Makes queries easier to read and review
- Required for CI/CD pipeline to pass
- Automatically handles indentation, keyword casing, and line breaks

**When to format:**
- Immediately after writing or modifying any SQL query
- Before running `./bqetl query validate`
- Before committing changes to git

**Note:** The `./bqetl query validate` command includes formatting checks, but it's better to run `./bqetl format` first to automatically fix any formatting issues rather than just checking for them.

## Assets (Examples)

The `/assets` directory contains complete query examples:

- `basic_query_example.sql` - Simple aggregation pattern
- `cte_query_example.sql` - Using CTEs for complex logic
- `user_aggregation_example.sql` - User-level metrics
- `join_example.sql` - Standard JOIN with partition filters
- `unnest_example.sql` - UNNEST for repeated fields
- `python_query_template.py` - Python query structure

## References (Detailed Documentation)

The `/references` directory contains detailed guides:

- `sql_formatting_conventions.md` - Formatting rules, UDF usage, header comments
- `partitioning_patterns.md` - Incremental vs full refresh patterns
- `jinja_templating.md` - Jinja functions and date handling
- `common_query_patterns.md` - Event processing, JOINs, performance tips
- `python_queries.md` - When to use Python, common patterns, best practices
- `external_documentation.md` - Links to official docs and example queries
- `test_update_workflow.md` - Workflow for updating existing queries and coordinating test updates

### DataHub Usage (CRITICAL for Token Efficiency)

**BEFORE using any DataHub MCP tools (`mcp__datahub-cloud__*`), you MUST:**
- **READ `../bigquery-etl-core/references/datahub_best_practices.md`** - Token-efficient query patterns and priority order
- Always prefer local files (schema.yaml, metadata.yaml) over DataHub queries
- Always check Glean Dictionary for `_live`/`_stable` tables before using DataHub

**Use DataHub ONLY for:**
- Schema definitions when not available in `/sql` directory
- Field descriptions when missing (after checking Glean Dictionary → `/sql` hierarchy)
- Lineage/dependencies when can't infer from bqetl (telemetry sources, syndicated datasets)
- Syndicated datasets (directories without query.sql/query.py/view.sql - usually from dev teams' postgres databases)

**When using DataHub:**
- Extract ONLY essential fields (column names/types) from DataHub responses
- Use search → get_entity pattern with limited results
- Check metadata.yaml for syndicated datasets first

## 🚨 Test Management - MANDATORY FOR ALL QUERY UPDATES

**CRITICAL: ALWAYS check for and update existing tests when modifying queries!**

### When Updating Existing Queries

**BEFORE making changes:**
1. **Check for existing tests:**
   ```bash
   ls tests/sql/<project>/<dataset>/<table>/
   ```
2. **Note current source tables:**
   ```bash
   grep -E "FROM|JOIN" sql/<project>/<dataset>/<table>/query.sql
   ```

**AFTER making changes:**
1. **Update schema** (if output structure changed):
   ```bash
   ./bqetl query schema update <dataset>.<table>
   ```
2. **🚨 MANDATORY: Update test fixtures** for ALL existing tests:
   - **New source table added (JOIN, FROM)?** → **MUST use sql-test-generator skill** to add fixtures to ALL test directories
   - **Source table removed?** → Delete its fixture files from all test directories
   - **Output schema changed?** → Update expect.ndjson/expect.yaml in all test directories
   - **Query logic changed?** → Review and update test input data and expected outputs
3. **Run tests:**
   ```bash
   pytest tests/sql/<project>/<dataset>/<table>/ -v
   ```
4. **Fix any failures** - Update fixtures and expectations until tests pass

### When Creating New Queries

**After writing query.sql:**
1. **MUST create unit tests** using sql-test-generator skill
2. Tests validate query logic before deployment
3. Required for CI/CD pipeline

### Common Test Update Scenarios

**Added a new field based on existing source data:**
- Update input data in `<source_table>.ndjson` files to include the field
- Update expected output in `expect.ndjson` files with expected values for the new field
- Update test schema files if needed (`.schema.json` files)

**Added a JOIN to a new table:**
- **MUST use sql-test-generator skill** to create fixtures for the new table in ALL test directories
- Prevents tests from querying production data (which causes failures)
- Ensures proper data types and schema structure

**Changed aggregation logic:**
- Update expected values in `expect.ndjson` to match new calculation logic
- May need to adjust input test data to create meaningful test cases

**For detailed workflow:** See `references/test_update_workflow.md`

## Data Quality Checks vs Unit Tests

**IMPORTANT DISTINCTION:**

**Data Quality Checks (Bigeye):**
- Use **bigconfig-generator skill** to create Bigeye monitoring configurations
- Bigeye monitors production data for quality issues (anomalies, nulls, freshness, etc.)
- `checks.sql` files are **DEPRECATED** and should NOT be used
- All data quality monitoring should be done via Bigeye

**Unit Tests (sql-test-generator):**
- Use **sql-test-generator skill** to create unit test fixtures
- Unit tests validate query logic during development
- Tests run on small, synthetic fixtures (not production data)
- Ensures queries work correctly before deployment
- **MANDATORY: Must be updated whenever queries are modified**

## Integration with Other Skills

**query-writer** works in coordination with other skills:

### Works with bigquery-etl-core
- References core skill for project structure and naming conventions
- Uses common patterns, mozfun UDF references, and metric discovery

### Works with metadata-manager
- **After writing and validating queries:** Use metadata-manager to generate/update schema.yaml
- Creates/updates metadata.yaml with scheduling and ownership

### Works with sql-test-generator
- **After writing and validating queries:** Use sql-test-generator to create unit test fixtures
- Prevents production queries by ensuring complete test coverage

### Works with bigconfig-generator
- **For data quality monitoring:** Use bigconfig-generator to create Bigeye configurations
- Monitors production tables for data quality issues (NOT checks.sql)

### Typical Workflow

**Creating new queries:**
1. **Use query-writer** to write query.sql or query.py
2. **Format the query:** Run `./bqetl format sql/<project>/<dataset>/<table>` to apply Mozilla SQL formatting standards
3. **Validate the query:** Run `./bqetl query validate sql/<project>/<dataset>/<table>` to check for syntax errors and conventions
4. **Invoke metadata-manager** to generate schema.yaml and metadata.yaml (ONLY if validation passes)
5. **Invoke sql-test-generator** to create unit test fixtures
6. Run unit tests and validate query works correctly

**Updating existing queries:**
1. **🚨 FIRST: Check for existing tests:** Run `ls tests/sql/<project>/<dataset>/<table>/` to see what tests exist
2. **Use query-writer** to modify query.sql or query.py
3. **Format the query:** Run `./bqetl format sql/<project>/<dataset>/<table>` to apply formatting
4. **Validate the query:** Run `./bqetl query validate sql/<project>/<dataset>/<table>` to ensure changes are valid
5. **Invoke metadata-manager** to update schema.yaml if output structure changed (ONLY if validation passes)
6. **🚨 MANDATORY: Update tests:**
   - If new source table added (JOIN/FROM): **MUST invoke sql-test-generator** to add fixtures to ALL test directories
   - If source table removed: Delete fixture files from all test directories
   - If output schema changed: Update expect.ndjson in all test directories
   - If query logic changed: Update test input data and expectations
7. **Run tests:** `pytest tests/sql/<project>/<dataset>/<table>/ -v` and fix any failures
8. **See `references/test_update_workflow.md`** for complete test update workflow and checklist

## Performance Essentials

- Filter on partition columns: `WHERE submission_date = @submission_date`
- Avoid `SELECT *` - list only needed columns
- Filter before JOINs to reduce shuffling
- Use `sample_id` for testing: `WHERE sample_id = 0` (1% sample)
- Use approximate functions: `approx_count_distinct()` when exact counts not needed

**For detailed optimization:** https://docs.telemetry.mozilla.org/cookbooks/bigquery/optimization.html

## External Documentation

- Creating derived datasets: https://mozilla.github.io/bigquery-etl/cookbooks/creating_a_derived_dataset/
- Recommended practices: https://mozilla.github.io/bigquery-etl/reference/recommended_practices/
- Common workflows: https://mozilla.github.io/bigquery-etl/cookbooks/common_workflows/
- Query optimization: https://docs.telemetry.mozilla.org/cookbooks/bigquery/optimization.html

## Scripts

The `/scripts` directory is reserved for helper scripts (currently empty).
