---
name: sql-test-generator
description: ALWAYS use this skill when users ask to create, generate, or write UNIT TESTS for BigQuery SQL queries. Invoke proactively whenever the request includes "test" or "tests" with a query/table name. This skill is for unit testing ONLY (not data quality checks - use bigconfig-generator for Bigeye monitoring). Works with bigquery-etl-core skill to understand query patterns.
---

# SQL Test Generator (Unit Tests Only)

**Composable:** Works with bigquery-etl-core (for patterns), metadata-manager (for test updates), and query-writer (for query understanding)
**When to use:** Creating/updating unit test fixtures for BigQuery SQL queries, preventing production queries in tests

**NOT for data quality checks:** Use bigconfig-generator skill for Bigeye monitoring. The `checks.sql` file approach is DEPRECATED.

Generate unit test fixtures for BigQuery SQL queries following bigquery-etl conventions. These are development-time tests that validate query logic on small, synthetic data.

**Official Documentation:** https://mozilla.github.io/bigquery-etl/cookbooks/testing/

## Unit Tests vs Data Quality Checks

**CRITICAL DISTINCTION:**

**This skill creates UNIT TESTS:**
- Test query logic during development
- Run on small, synthetic fixtures (not production data)
- Validate transformations, joins, aggregations work correctly
- Part of CI/CD pipeline

**For data quality monitoring (NOT this skill):**
- Use **bigconfig-generator skill** to create Bigeye monitoring configurations
- Monitors production data for quality issues (anomalies, nulls, freshness)
- `checks.sql` files are **DEPRECATED** - do NOT create or update them
- All production data quality checks should be done via Bigeye

## 🚨 REQUIRED READING - Start Here

**BEFORE creating any test fixtures, you MUST read these files:**

1. **CRITICAL FOR SAFETY:** Read `references/preventing_production_queries.md`
   - Prevents accidentally querying production data
   - Explains how to verify fixtures are working correctly
   - Required reading before ANY test creation

2. **UNDERSTAND TEST PATTERNS:** Read `references/test_strategy_patterns.md`
   - Learn which test scenarios are needed for different query types
   - Understand how many tests to create
   - See examples of test coverage strategies

## 📋 Templates - Copy These Structures

**When creating test fixtures, READ and COPY the structure from these template files:**

**For Input Fixtures:**
- **Glean events?** → READ `assets/glean_events_fixture.yaml` and copy its structure
  - Shows proper `client_info`, `events`, and `extra` formatting
  - Use this for any `*_stable.events_v1` or Glean ping tables

- **Legacy telemetry with arrays?** → READ `assets/legacy_array_fixture.yaml`
  - Shows how to structure array fields that get UNNESTed
  - Use for legacy telemetry tables with array columns

- **Simple table?** → READ `assets/simple_test_input.yaml`
  - Basic fixture structure for flat tables

- **UNION ALL query?** → READ both `assets/union_all_fixture1.yaml` AND `assets/union_all_fixture2.yaml`
  - Shows how to create fixtures for multiple data sources
  - Critical: ALL sources need fixtures in the SAME test directory

**For Query Parameters:**
- READ `assets/query_params_example.yaml` - Must be array format, not key-value pairs

**For Expected Output:**
- READ `assets/simple_test_expect.yaml` - Shows array format and NULL handling
- READ `assets/timestamp_example.yaml` - Shows correct TIMESTAMP format (ISO 8601 with timezone)

## Reference Documentation (Read as needed)

- `references/common_test_failures.md` - **READ THIS** when tests fail - Real-world failures and solutions (NULL handling, ordering, timestamps)
- `references/yaml_format_guide.md` - YAML syntax, type inference, nested structures (read if you encounter YAML errors)
- `references/external_documentation.md` - Links to official docs and related resources

### DataHub Usage (CRITICAL for Token Efficiency)

**IMPORTANT: DataHub is for lineage discovery ONLY, NOT for schema lookups**

**For schema discovery, use this priority order:**
1. 🥇 Local `schema.yaml` files in `sql/` directory
2. 🥈 Glean Dictionary for `_live` and `_stable` tables
3. 🥉 BigQuery ETL docs (https://mozilla.github.io/bigquery-etl/)
4. ❌ **NEVER use DataHub for schemas** - use it only for lineage

**When DataHub IS useful:**
- ✅ Discovering upstream/downstream table dependencies
- ✅ Finding which tables are related
- ✅ Understanding table usage patterns

**See these guides:**
- `../metadata-manager/references/schema_discovery_guide.md` - Complete schema discovery workflow
- `../metadata-manager/references/glean_dictionary_patterns.md` - Token-efficient Glean Dictionary usage
- `../metadata-manager/scripts/datahub_lineage.py` - Efficient lineage queries

## Test Structure

Tests live in: `tests/sql/<project>/<dataset>/<table>/<test_name>/`

**Required files:**
- Input fixtures: `<full_table_reference>.yaml` (e.g., `moz-fx-data-shared-prod.telemetry.events.yaml`)
- Expected output: `expect.yaml`
- Query parameters (if needed): `query_params.yaml`

## Critical Requirements

### ⚠️ PREVENTING PRODUCTION QUERIES - READ THIS FIRST ⚠️

**The #1 way tests accidentally query production data:**
- Missing fixture files for ANY table referenced in FROM/JOIN/UNION clauses
- When a fixture is missing, BigQuery falls back to querying the production table

**How to prevent this:**
1. Use `grep -E "FROM|JOIN" query.sql` to identify ALL source tables
2. Create a fixture file for EVERY table found, even if it contributes minimal data
3. If test results show thousands of rows or production-like data, STOP - you're querying production
4. Check the "Initialized" lines in pytest output - every source table should appear

### 1. File Naming - MOST COMMON FAILURE
Input fixtures **must** match how the table is referenced in the query:
- Query uses `moz-fx-data-shared-prod.dataset.table` → file must be `moz-fx-data-shared-prod.dataset.table.yaml`
- Query uses `dataset.table` → file must be `dataset.table.yaml`
- Query uses `table` → file must be `table.yaml`

Wrong naming causes tests to query production BigQuery instead of your fixtures.

### 2. YAML Format
All fixtures must use array syntax (starts with `-`). See `references/yaml_format_guide.md` for details.

```yaml
# Correct - array syntax with dashes
- field1: value1
  field2: value2
```

### 3. Required Fields
- **Input fixtures:** Include ALL fields the query references, even if NULL: `loaded: null`
- **expect.yaml:** **COMPLETELY OMIT** fields that will be NULL - do NOT include them with `field: null`
  - ❌ Wrong: `avg_time_seconds: null`
  - ✅ Correct: omit the field entirely
  - BigQuery does not return NULL fields in results, so including them in expect.yaml will cause test failures
- **CRITICAL for UNION/UNION ALL queries**: You MUST create fixtures for ALL source tables with at least one row of test data. If you want a source to contribute no data, either:
  - Add a fixture with data that gets filtered out by WHERE clauses, OR
  - Create a minimal fixture that passes filters but contributes to the test
  - DO NOT create empty array fixtures (`[]`) - they cause "Schema has no fields" errors
  - DO NOT omit fixture files - missing fixtures cause the query to hit production BigQuery
- Omit `generated_time` columns from `expect.yaml`

### 4. Query Parameters Format
Must be an array (starts with `-`), not key-value pairs. See `assets/query_params_example.yaml` for template.

```yaml
- name: submission_date
  type: DATE
  value: "2024-12-01"
```

### 5. TIMESTAMP Format ⚠️ VERY COMMON FAILURE

**CRITICAL:** BigQuery returns TIMESTAMP and DATETIME fields in ISO 8601 format with timezone.

**In expect.yaml, ALWAYS use ISO 8601 format:**
```yaml
# ✅ CORRECT - ISO 8601 with timezone
- campaign_created_at: "2025-06-01T10:00:00+00:00"
  campaign_updated_at: "2025-07-01T12:00:00+00:00"
```

```yaml
# ❌ WRONG - Missing 'T' and timezone
- campaign_created_at: "2025-06-01 10:00:00"
  campaign_updated_at: "2025-07-01 12:00:00"
```

**Format rules:**
- TIMESTAMP fields: `2025-06-01T10:00:00+00:00` (ISO 8601)
- DATE fields: `2025-06-01` (YYYY-MM-DD)
- With microseconds: `2025-06-01T10:00:00.123456+00:00`

**Input fixtures can use either format, but expect.yaml MUST use ISO 8601.**

See `references/common_test_failures.md` section 3 for details and examples.

## Test Generation Strategy

**See `references/test_strategy_patterns.md` for comprehensive patterns.**

**Quick analysis checklist:**
- Join types (FULL OUTER, LEFT, INNER) → test each branch
- Aggregations/GROUP BY → test single and multiple rows
- CASE/IF logic → test each branch
- UDFs and map operations → test empty, existing, new values
- Incremental logic → test first run vs subsequent runs
- Date-based filtering → test different date ranges
- Version filtering → test both sides of thresholds (use "120.0.0" format)
- **UNION/UNION ALL** → create ONE comprehensive test with fixtures for ALL data sources

**Number of tests:**
- Simple queries: 1 test
- Moderate complexity: 1-2 tests
- Complex (FULL OUTER JOIN, maps, multiple CTEs): 3-5 tests
- UNION ALL queries: 1 comprehensive test per date/filter branch

**Test naming:** Use descriptive snake_case: `test_new_clients_only`, `test_union_all_sources`

## Environment Setup

Before running tests, configure Google Cloud authentication:

```bash
export GOOGLE_PROJECT_ID=bigquery-etl-integration-test
gcloud config set project $GOOGLE_PROJECT_ID
gcloud auth application-default login
```

See https://mozilla.github.io/bigquery-etl/cookbooks/testing/ for more details.

## Workflow

### Step-by-Step Process

1. **Read the required reference files** (from "REQUIRED READING" section above)
   - READ `references/preventing_production_queries.md`
   - READ `references/test_strategy_patterns.md`

2. **Read the query.sql file**

3. **Gather schema information efficiently (use priority order):**
   - **FIRST:** Check local `schema.yaml` files in `sql/` directory for derived tables
   - **SECOND:** Check Glean Dictionary for `_live` and `_stable` tables
     - See `../metadata-manager/references/glean_dictionary_patterns.md` for token-efficient extraction
     - Extract only needed fields (don't read entire large files)
   - **THIRD:** Check https://mozilla.github.io/bigquery-etl/ dataset browser
   - **DataHub MCP: For lineage ONLY, NOT for schemas**
     - Use DataHub to discover upstream/downstream tables
     - Then use priority order above to get schemas for those tables
     - See `../metadata-manager/references/schema_discovery_guide.md` for complete workflow
     - See `../metadata-manager/scripts/datahub_lineage.py` for efficient lineage queries

4. **Identify ALL source tables** - use this command:
   ```bash
   grep -E "FROM|JOIN" query.sql
   ```
   Write down EVERY table you find. This is your checklist.

4. **Determine test scenarios needed** based on query complexity

5. **Read the appropriate template files** for your data sources:
   - For Glean events tables → READ `assets/glean_events_fixture.yaml`
   - For legacy telemetry with arrays → READ `assets/legacy_array_fixture.yaml`
   - For simple tables → READ `assets/simple_test_input.yaml`
   - For query parameters → READ `assets/query_params_example.yaml`
   - For UNION ALL queries → READ `assets/union_all_fixture1.yaml` and `assets/union_all_fixture2.yaml`
   - **For queries with TIMESTAMP fields → READ `assets/timestamp_example.yaml`** (VERY IMPORTANT)

6. **Create test directory and fixtures:**
   - For each test scenario, create a directory: `tests/sql/<project>/<dataset>/<table>/<test_name>/`
   - **Create a fixture file for EVERY source table** from your step 3 checklist
   - **Copy the structure from the template files you read in step 5**
   - Each fixture needs at least one row of data
   - Match the file naming to how the table is referenced in the query

7. **Create expect.yaml and query_params.yaml** (if needed)
   - Use the template structures from step 5

8. **Run the test:**
   ```bash
   pytest tests/sql/<project>/<dataset>/<table>/<test_name>/ -v
   ```

   **Common pytest debugging options:**
   ```bash
   # Stop on first failure (faster debugging)
   pytest tests/sql/.../test_name/ -x

   # Very verbose output (shows individual test details)
   pytest tests/sql/.../test_name/ -vv

   # Show full diff on assertion failures
   pytest tests/sql/.../test_name/ -vv --tb=short

   # Run specific test by pattern
   pytest tests/sql/.../test_name/ -k "test_pattern"

   # Show local variables in traceback
   pytest tests/sql/.../test_name/ -l

   # Combined: stop on first failure with very verbose output
   pytest tests/sql/.../test_name/ -xvv
   ```

9. **Fix common test failures** (if test fails):

   **A. Timestamp format mismatches** (VERY COMMON):
   - If test fails with timestamp format differences like `2025-06-01T10:00:00+00:00` != `2025-06-01 10:00:00`
   - Update expect.yaml to use ISO 8601 format: `2025-06-01T10:00:00+00:00`
   - See `references/common_test_failures.md` section 3 for details

   **B. Ordering issues** (VERY COMMON):
   - If test fails with ordering differences (row order or map/array key order mismatch)
   - Look at the "Actual:" section in pytest output
   - Copy the EXACT order from "Actual:" to your expect.yaml
   - This includes both row-level ordering AND nested field ordering (maps, arrays)
   - See `references/common_test_failures.md` section 2 for detailed examples

10. **Verify you're NOT querying production:**
   - ✅ Check pytest output for "Initialized" lines - count should match your table checklist from step 2
   - ✅ Test should complete in <30 seconds
   - ✅ Results should be small (< 10 rows typically)
   - ❌ If you see thousands of rows, real production IDs, or slow execution → you're querying production!
   - ❌ Missing "Initialized" line for a table → add that fixture file

11. **Ask about data quality monitoring:**
   - After tests pass successfully, check if monitoring exists:
     - Check for bigconfig.yml file: `sql/<project>/<dataset>/<table>/bigconfig.yml`
   - If bigconfig.yml does NOT exist, proactively ask the user:
     - "Would you like to add Bigeye monitoring/data quality checks for this table?"
   - Suggest relevant checks based on table type:
     - Aggregation tables (DAU, MAU, etc.) → freshness, volume/anomaly detection, null checks
     - Event tables → freshness, volume checks
     - Derived tables → freshness, schema validation
   - If user agrees, use **bigconfig-generator skill** to create monitoring configurations
   - **Note:** Only ask if bigconfig.yml doesn't exist - don't ask if monitoring is already configured

### Production Query Checklist
Before finalizing tests, verify:
- [ ] I ran `grep -E "FROM|JOIN" query.sql` to find all source tables
- [ ] I created a fixture file for each source table found
- [ ] I checked pytest output for "Initialized" messages matching each source table
- [ ] Test results are small and match my expect.yaml
- [ ] Test runs quickly (<30 seconds)

**Note:** After running tests, if you need to use metadata-manager or query production tables, switch back to the main project:
```bash
export GOOGLE_PROJECT_ID=mozdata
gcloud config set project $GOOGLE_PROJECT_ID
```

## Example Tests

### Example 1: Simple Query with Join

For a query at `sql/moz-fx-data-shared-prod/dataset/table_v1/query.sql` that joins `telemetry.clients_daily` with the target table:

**Test directory:** `tests/sql/moz-fx-data-shared-prod/dataset/table_v1/test_new_clients/`

**Input fixture:** `moz-fx-data-shared-prod.telemetry.clients_daily.yaml`
```yaml
- client_id: "abc123"
  submission_date: "2025-01-01"
  search_count: 5
```

**Query params:** `query_params.yaml`
```yaml
- name: submission_date
  type: DATE
  value: "2025-01-01"
```

**Expected output:** `expect.yaml`
```yaml
- client_id: "abc123"
  total_searches: 5
  first_seen_date: "2025-01-01"
```

### Example 2: UNION ALL Query with Multiple Sources

For a query that unions three data sources (legacy, glean, and ads):

**Test directory:** `tests/sql/moz-fx-data-shared-prod/dataset/table_v1/test_union_all_sources/`

**IMPORTANT:** Create fixtures for ALL three sources in ONE test directory:

**Fixture 1:** `moz-fx-data-shared-prod.legacy_source.table.yaml`
```yaml
- submission_timestamp: "2024-12-15 10:00:00"
  document_id: "doc1"
  version: "120.0.0"
  event_count: 5
```

**Fixture 2:** `moz-fx-data-shared-prod.glean_source.table.yaml`
```yaml
- submission_timestamp: "2024-12-15 14:30:00"
  document_id: "doc2"
  client_info:
    app_display_version: "121.0.0"
  events:
    - category: "interaction"
      name: "click"
```

**Fixture 3:** `moz-fx-data-shared-prod.ads_source.table.yaml`
```yaml
- submission_hour: "2024-12-15 10:00:00"
  ad_id: 12345
  interaction_type: "impression"
  interaction_count: 100
```

**Query params:** `query_params.yaml`
```yaml
- name: submission_date
  type: DATE
  value: "2024-12-15"
```

**Expected output:** `expect.yaml`
```yaml
- submission_date: "2024-12-15"
  source: "legacy"
  event_count: 5
- submission_date: "2024-12-15"
  source: "glean"
  event_count: 1
- submission_date: "2024-12-15"
  source: "ads"
  event_count: 100
```

## Mozilla-Specific Telemetry Patterns

**See example assets for templates:**
- `assets/glean_events_fixture.yaml` - Glean events with extras structure
- `assets/legacy_array_fixture.yaml` - Legacy telemetry with array fields

### Glean Events with Extras
See `assets/glean_events_fixture.yaml` for complete example. Events use nested structure:
- Access via `events.category`, `events.name`
- Extra fields via `mozfun.map.get_key(events.extra, 'field_name')`

### Legacy Telemetry Arrays
See `assets/legacy_array_fixture.yaml`. Arrays get unnested with `CROSS JOIN UNNEST(tiles)`.

### Version Numbers
**Always use three-part versions** ("121.0.0") to avoid YAML float parsing. See `references/yaml_format_guide.md`.

## Common Errors

**See `references/common_test_failures.md` for real-world examples and solutions.**
**See `references/yaml_format_guide.md` and `references/preventing_production_queries.md` for detailed guides.**

### 1. NULL Fields in expect.yaml ⚠️ COMMON
Including `field: null` in expect.yaml causes test failures because BigQuery omits NULL fields from results.
**Solution:** Completely omit NULL fields from expect.yaml - don't include them at all.
See `references/common_test_failures.md` section 1.

### 2. Non-Deterministic ORDER BY
When ORDER BY fields have duplicate values, row order becomes non-deterministic and tests fail.
**Solution:** Either create test data with different ORDER BY values, or run test to see actual order and update expect.yaml.
See `references/common_test_failures.md` section 2.

### 3. Type Inference Issues
Version numbers like "120.0" parsed as FLOAT64 instead of STRING.
**Solution:** Use three-part versions: "120.0.0" or simple integers: "120"

### 4. Empty Fixture Arrays
Creating `[]` causes "Schema has no fields" errors.
**Solution:** Always include at least one row. To filter out data, use WHERE clause filtering.

### 5. Missing Fixtures Query Production ⚠️ CRITICAL
If ANY source table lacks a fixture, query hits production BigQuery.
**Symptoms:** Thousands of rows, real production values, slow execution (>10 seconds)
**Solution:** Create fixtures for ALL source tables. See `references/preventing_production_queries.md`

### 6. NULL Field Handling (Duplicate - see #1 above)
Omit NULL fields from `expect.yaml` - BigQuery doesn't return them in results.

**Full troubleshooting:** https://mozilla.github.io/bigquery-etl/cookbooks/testing/

## Integration with Other Skills

**sql-test-generator** is invoked by other skills when test fixtures need to be created or updated:

### Works with bigquery-etl-core
- **References** core skill for test structure, naming conventions, and query patterns
- Uses common table patterns for test creation
- **Invocation:** Automatically available as foundation skill

### Invoked by metadata-manager
- **When queries are modified:** metadata-manager detects when test fixtures need updating
- **metadata-manager delegates to sql-test-generator** for:
  - New source tables added to query (JOINs, new FROM clauses)
  - Tests querying production (thousands of rows in output)
  - Creating new test scenarios for new logic
- metadata-manager handles simple updates (expect.yaml changes) directly
- **Invocation pattern:** metadata-manager explicitly invokes sql-test-generator with "Use sql-test-generator skill" instructions

### Works with query-writer
- **After query-writer creates queries:** Use sql-test-generator to create test fixtures
- Analyzes query structure to identify all source tables
- Creates comprehensive test coverage
- **Invocation:** After query.sql is complete, invoke sql-test-generator to create tests

### Coordinates with bigconfig-generator
- **After tests pass:** Check if bigconfig.yml exists for the table
- If bigconfig.yml does NOT exist, proactively ask user if they want data quality monitoring
- Suggests relevant monitoring checks based on table type (aggregation, event, derived)
- If user agrees, delegate to bigconfig-generator skill to create Bigeye configurations
- **Workflow:** sql-test-generator → check for bigconfig.yml → ask user → bigconfig-generator (if approved)

### Typical Invocation Scenarios

**Direct invocation by user:**
- User asks: "Generate tests for query X"
- User asks: "Create test fixtures for table Y"

**Invoked by metadata-manager:**
- Query modified with new JOINs → metadata-manager invokes sql-test-generator
- Tests showing production data → metadata-manager invokes sql-test-generator
- New test scenarios needed → metadata-manager invokes sql-test-generator

**After query-writer:**
- New query.sql created → invoke sql-test-generator to create initial tests

### Key Capabilities

**Prevents production queries:**
- Ensures ALL source tables have fixtures (critical for UNION/UNION ALL queries)
- Detects missing fixtures via "Initialized" lines in pytest output
- Provides clear symptoms of production query issues

**Handles complex queries:**
- UNION ALL with multiple sources
- Nested structures and complex types
- YAML type inference issues (version numbers, etc.)

**Provides best practices:**
- Fixture naming conventions
- Test organization (one comprehensive test vs multiple)
- Production query detection and prevention
