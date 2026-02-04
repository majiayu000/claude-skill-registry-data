---
name: metadata-manager
description: Use this skill when creating or updating DAG configurations (dags.yaml), schema.yaml, and metadata.yaml files for BigQuery tables. Handles creating new DAGs when needed and coordinates test updates when queries are modified (invokes sql-test-generator as needed). Works with bigquery-etl-core, query-writer, and sql-test-generator skills.
---

# Metadata Manager

**Composable:** Works with bigquery-etl-core (for conventions), query-writer (for queries), and sql-test-generator (for test updates)
**When to use:** Creating/updating DAG configurations, schema.yaml and metadata.yaml files, coordinating test updates when queries are modified

## Overview

Generate and manage schema.yaml, metadata.yaml files, and DAG configurations following Mozilla BigQuery ETL conventions. This skill handles:
- Creating new DAGs when no suitable existing DAG is found
- Generating schema and metadata files for new tables with intelligent descriptions
  - Gets schema structure from /sql directory or DataHub
  - Gets descriptions from Glean Dictionary (for `_live`/`_stable`), /sql directory, or DataHub
  - **Proactively detects ANY missing descriptions and asks user if they want to add them to source tables**
  - **Auto-generates missing descriptions when adding new tables or editing existing queries**
  - Improves descriptions with context and clarity
  - Recommends updates to source tables when descriptions are unclear
- Coordinating test updates when queries are modified (handles simple updates directly, invokes sql-test-generator for complex fixture creation)

**For comprehensive documentation, see:**
- Creating derived datasets: https://mozilla.github.io/bigquery-etl/cookbooks/creating_a_derived_dataset/
- Scheduling reference: https://mozilla.github.io/bigquery-etl/reference/scheduling/
- Recommended practices: https://mozilla.github.io/bigquery-etl/reference/recommended_practices/

## 🚨 REQUIRED READING - Start Here

**BEFORE creating or modifying metadata/schema/DAG files, READ these references:**

1. **Schema Discovery:** READ `references/schema_discovery_guide.md` (for schema generation)
   - Priority order: /sql → Glean Dictionary → DataHub (last resort/validation)
   - Token-efficient patterns for getting source schemas
   - When to use each source

2. **DAG Discovery:** READ `references/dag_discovery.md`
   - How to find the right Airflow DAG for your table
   - Common DAG patterns

3. **DAG Creation:** READ `references/dag_creation_guide.md` (when creating new DAGs)
   - When to create a new DAG vs reuse existing
   - Complete DAG creation workflow
   - Configuration options and best practices

4. **Metadata YAML Guide:** READ `references/metadata_yaml_guide.md`
   - All metadata.yaml options and their meanings
   - Scheduling configuration
   - Partitioning and clustering options
   - Ownership and labels

5. **Schema YAML Guide:** READ `references/schema_yaml_guide.md`
   - Field types and modes (REQUIRED, NULLABLE, REPEATED)
   - Nested and repeated structures
   - Description best practices

6. **Schema Description Improvements:** READ `references/schema_description_improvements.md`
   - When to improve source descriptions
   - How to recommend updates to source tables
   - Description improvement checklist

7. **Glean Dictionary Patterns:** READ `references/glean_dictionary_patterns.md` (for _live/_stable tables)
   - Token-efficient extraction from large files
   - Finding Glean Dictionary files
   - Common table patterns

## 📋 Templates - Copy These Structures

**When creating a new DAG, READ and COPY from these templates:**

- **Daily scheduled DAG?** → READ `assets/dag_template_daily.yaml`
  - Most common pattern for daily processing at 2 AM UTC

- **Hourly scheduled DAG?** → READ `assets/dag_template_hourly.yaml`
  - For real-time or frequent processing (every hour)

- **Custom schedule DAG?** → READ `assets/dag_template_custom.yaml`
  - For weekly, multi-hour, or specific time requirements

**When creating metadata.yaml, READ and COPY from these templates:**

- **Daily partitioned table?** → READ `assets/metadata_template_daily_partitioned.yaml`
  - Most common pattern for daily aggregations

- **Hourly partitioned table?** → READ `assets/metadata_template_hourly_partitioned.yaml`
  - For real-time or hourly aggregations

- **Full refresh table?** → READ `assets/metadata_template_full_refresh.yaml`
  - For tables that recalculate all data each run

**When creating schema.yaml, READ and COPY from these templates:**

- **Simple flat schema?** → READ `assets/schema_template_basic.yaml`
  - Basic field types and descriptions

- **Nested/repeated fields?** → READ `assets/schema_template_with_nested.yaml`
  - RECORD types and array structures

## Quick Start

### Creating New Table Metadata

**Step 1: Find or create the appropriate DAG (use this priority order)**
1. **FIRST:** Search local `dags.yaml` files using grep for keywords related to the dataset/product
2. **SECOND:** Check `references/dag_discovery.md` for common DAG patterns
3. **IF NO SUITABLE DAG EXISTS:** Create a new DAG
   - **READ `references/dag_creation_guide.md` for when to create vs reuse**
   - Present DAG options to the user (existing similar DAG vs new DAG)
   - If creating new DAG:
     - Choose template: `assets/dag_template_daily.yaml`, `dag_template_hourly.yaml`, or `dag_template_custom.yaml`
     - Infer values from context (dataset name, product area, similar tables)
     - Ask user to confirm/modify: schedule, owner, start_date, impact tier
     - Add new DAG entry to the **bottom** of `dags.yaml`
     - Validate with `./bqetl dag validate <dag_name>`

**Step 2: Create directory structure**
```bash
./bqetl query create <dataset>.<table> --dag <dag_name>
```

**Step 3: Create metadata.yaml**
- Use templates from `assets/` as a starting point
- Choose the appropriate template based on partitioning strategy
- Customize with owners, description, labels, scheduling, and BigQuery config
- See `references/metadata_yaml_guide.md` for detailed options

**Step 4: Create schema.yaml with intelligent descriptions**
- **If query.sql exists:** Run `./bqetl query schema update <dataset>.<table>` to auto-generate structure
- **Get source table schemas** using priority order (see `references/schema_discovery_guide.md`):
  1. Check `/sql` directory for schema structure (ALWAYS FIRST)
  2. Use DataHub for schema structure (when not in `/sql`)
- **Get descriptions** using priority order:
  1. Glean Dictionary for `_live`/`_stable` table descriptions via https://dictionary.telemetry.mozilla.org/
  2. `/sql` directory schema.yaml files for derived tables
  3. DataHub for descriptions (when not in above sources)
  - **IMPORTANT:** Glean Dictionary provides descriptions only, NOT schemas
- **Apply base schema descriptions (RECOMMENDED):**
  - Run: `./bqetl query schema update <dataset>.<table> --use-global-schema`
  - For ads data: `./bqetl query schema update <dataset>.<table> --use-dataset-schema --use-global-schema`
  - Auto-populates descriptions for standard fields (submission_date, client_id, dau, etc.)
  - See "Using Base Schemas for Auto-Populating Descriptions" section below for details
- **Check for ANY missing descriptions:**
  - **For source tables:** Notify user and ask if they want to generate descriptions for source tables
  - **For new tables or editing existing queries:** Auto-generate ANY missing descriptions (no asking)
  - This improves metadata completeness for all downstream consumers
- **Use source descriptions as base** and improve them:
  - Add context specific to derived table
  - Clarify transformations
  - Fill gaps in source descriptions
- **Generate recommendations** for source table description updates when needed
- See `references/schema_description_improvements.md` for improvement workflow
- See `references/glean_dictionary_patterns.md` for token-efficient Glean Dictionary usage

**Step 5: Deploy schema (if updating existing table)**
```bash
./bqetl query schema deploy <dataset>.<table>
```

### Updating Existing Queries

When modifying an existing query.sql, follow the test update workflow:

**1. Check for existing tests:**
```bash
ls tests/sql/<project>/<dataset>/<table>/
```

**2. Update the query.sql file** with your changes

**3. Update schema.yaml if output changed:**
```bash
./bqetl query schema update <dataset>.<table>
```
- Review changes
- Add descriptions for new fields

**4. If tests exist, update them:**
- **New source tables added?** → **Invoke sql-test-generator skill** to add fixtures to ALL tests
- **Source tables removed?** → Delete fixture files
- **Output schema changed?** → Update expect.yaml
- **Logic changed?** → Review and update test data/expectations

**5. Run tests:**
```bash
pytest tests/sql/<project>/<dataset>/<table>/ -v
```

**6. Handle test failures:**
- ✅ Expected failures (schema/logic changes) → Update expect.yaml
- ✅ Missing fixtures → **Invoke sql-test-generator skill**
- ❌ Production queries (thousands of rows) → **STOP, invoke sql-test-generator skill**
- ❌ Unexpected failures → Debug query changes

See `../query-writer/references/test_update_workflow.md` for complete details and the query modification checklist.

## DAG Management

### When to Create a New DAG

Before creating a new DAG, **always search for existing DAGs** that could be reused. Create a new DAG only when:
- **New product or service** requires isolated pipeline
- **Different scheduling requirements** than existing DAGs
- **Unique dependencies** that don't fit existing DAGs
- **Team ownership boundaries** require separate control

**DO NOT create a new DAG if** an existing DAG covers the same product area or schedule.

### Creating a New DAG

When no suitable DAG exists:

**1. Present options to the user:**
- List similar existing DAGs (if any close matches)
- Propose creating a new DAG with inferred configuration

**2. Choose appropriate template:**
- **Daily DAG** (`assets/dag_template_daily.yaml`) - Most common for daily aggregations
- **Hourly DAG** (`assets/dag_template_hourly.yaml`) - For real-time/frequent processing
- **Custom schedule** (`assets/dag_template_custom.yaml`) - Weekly, multi-hour, or specific times

**3. Gather required information:**
- **DAG name:** `bqetl_<product>` or `bqetl_<product>_<schedule>`
- **Schedule:** When should it run? (cron format or interval like "3h")
- **Owner:** Email address of primary owner
- **Start date:** When should processing begin? (YYYY-MM-DD)
- **Impact tier:** tier_1 (critical), tier_2 (important), tier_3 (nice-to-have)
- **Description:** Purpose, data sources, important notes

**4. Add DAG to dags.yaml:**
- Add new entry at the **bottom** of `dags.yaml`
- Use template as base and customize with gathered information
- Include all required fields: schedule_interval, default_args, owner, start_date, email, tags

**5. Validate:**
```bash
./bqetl dag validate <dag_name>
```

**See `references/dag_creation_guide.md` for:**
- Complete DAG creation workflow
- Configuration reference (schedules, retries, impact tiers)
- Common patterns and examples
- Best practices and troubleshooting

## Schema Files (schema.yaml)

Schema files define BigQuery table structure with field names, types, modes, and descriptions.

**Quick reference:**
- Common types: STRING, INTEGER, FLOAT, BOOLEAN, DATE, TIMESTAMP, RECORD, NUMERIC
- Modes: NULLABLE (default), REQUIRED, REPEATED (for arrays)
- Descriptions are **required** for all fields in new schemas
- For nested fields, use RECORD type with nested `fields:` list

### Using Base Schemas for Auto-Populating Descriptions

**Location:**
- Global schema: `bigquery_etl/schema/global.yaml` (common telemetry fields)
- Dataset schemas: `bigquery_etl/schema/<dataset_name>.yaml` (dataset-specific fields)

**Apply base schema descriptions:**
```bash
# Use global schema for common fields (submission_date, client_id, etc.)
./bqetl query schema update <dataset>.<table> --use-global-schema

# Use dataset-specific schema (e.g., ads_derived.yaml for ads data)
./bqetl query schema update <dataset>.<table> --use-dataset-schema

# Use both (dataset schema takes priority over global schema)
./bqetl query schema update <dataset>.<table> --use-dataset-schema --use-global-schema
```

**How it works:**
1. **Matches fields by name or alias** - If your query has `sub_date`, it matches `submission_date` via alias
2. **Applies descriptions** - Copies description from base schema to your schema.yaml
3. **Warns about overwrites** - Shows which existing descriptions were replaced
4. **Recommends canonical names** - Suggests renaming aliased fields (e.g., `sub_date` → `submission_date`)
5. **Identifies missing descriptions** - Lists fields not found in base schemas

**Priority order:** Dataset schema → Global schema → Missing description warning

**Example global.yaml fields:**
- `submission_date`, `client_id`, `country`, `sample_id`, `normalized_channel`
- `dau`, `wau`, `mau` (activity metrics)
- `attribution_campaign`, `attribution_source`, `attribution_medium`
- See full list: `bigquery_etl/schema/global.yaml`

**Example ads_derived.yaml fields:**
- `impressions`, `clicks`, `revenue`, `cpm`, `click_rate`
- `campaign_id`, `advertiser`, `creative_id`, `flight_id`
- `partner_name`, `provider`, `rate_type`
- See full list: `bigquery_etl/schema/ads_derived.yaml`

**Preview before applying (use helper script):**
```bash
# Preview what descriptions would be applied without making changes
python scripts/preview_base_schema.py <dataset>.<table>
```

### Intelligent Schema Generation

When generating schemas for derived tables, follow this workflow:

**1. Discover source table schemas (use priority order):**
   - **FIRST:** `/sql` directory for schema structure
   - **SECOND:** DataHub for schema structure (when not in `/sql`)

**2. Discover descriptions (use priority order):**
   - **FIRST:** Glean Dictionary for `_live`/`_stable` table descriptions via https://dictionary.telemetry.mozilla.org/
   - **SECOND:** `/sql` directory schema.yaml files for derived tables
   - **THIRD:** DataHub for descriptions (when not in above sources)
   - **IMPORTANT:** Glean Dictionary provides descriptions only, NOT schemas

**3. Apply base schema descriptions (RECOMMENDED for standard fields):**
   - **After** generating initial schema, use base schemas to auto-populate descriptions
   - Run: `./bqetl query schema update <dataset>.<table> --use-global-schema`
   - For ads data, also use: `--use-dataset-schema` (applies `ads_derived.yaml`)
   - This ensures consistent descriptions for common fields like `submission_date`, `client_id`, etc.
   - Preview changes first: `python scripts/preview_base_schema.py <dataset>.<table>`
   - See "Using Base Schemas for Auto-Populating Descriptions" section above for details

**4. Check for ANY missing descriptions:**
   - Detect missing descriptions in source tables or target table
   - **For source table missing descriptions:** Notify user and ask if they want to generate descriptions for source tables
   - **For new tables or editing existing queries:** Auto-generate ANY missing descriptions without asking
   - This proactively improves metadata completeness

**5. Use source descriptions as base:**
   - Copy descriptions from source tables
   - Maintain consistency across derived tables

**6. Improve descriptions when needed:**
   - Add context specific to derived table
   - Clarify transformations or aggregations
   - Simplify technical jargon
   - Fill gaps in source descriptions

**7. Recommend source updates (for existing descriptions):**
   - When source description exists but is unclear or incomplete
   - When improved description would benefit all downstream tables
   - Generate clear recommendations for source table owners

**See `references/schema_discovery_guide.md` for:**
- Complete schema discovery priority order
- How to efficiently search `/sql`, Glean Dictionary, and DataHub
- Token-efficient patterns for large files

**See `references/glean_dictionary_patterns.md` for:**
- Finding Glean Dictionary files
- Token-efficient extraction for large tables
- Common table patterns (_live, _stable, events, metrics)

**See `references/schema_description_improvements.md` for:**
- When to improve descriptions
- How to recommend source table updates
- Description improvement checklist

**Auto-generate from query:**
```bash
./bqetl query schema update <dataset>.<table>
```

**See `references/schema_yaml_guide.md` for:**
- Complete field type reference
- Nested/repeated field examples
- Description best practices
- Common telemetry field patterns

## Metadata Files (metadata.yaml)

Metadata files define table ownership, scheduling, partitioning, and BigQuery configuration.

**Required fields:**
- `friendly_name` - Human-readable table name
- `description` - Multi-line description of purpose
- `owners` - List of email addresses and/or GitHub teams (e.g., `mozilla/ads_data_team`)
  - **Use team detection script to find relevant teams:**
    ```bash
    python scripts/detect_teams.py
    ```
  - Recommends teams based on existing metadata files in `/sql`
  - Teams provide better coverage than individual emails
  - **See "Script Maintenance" section below for testing and troubleshooting**

**Common sections:**
- `labels` - application, schedule, table_type, dag, owner1
- `scheduling` - dag_name, date_partition_parameter, start_date
- `bigquery.time_partitioning` - type, field, expiration_days
- `bigquery.clustering` - fields for clustering (max 4)

**See `references/metadata_yaml_guide.md` for:**
- Complete scheduling options
- Partitioning strategies (day/hour)
- Clustering best practices
- Common label values
- Data retention policies

## Integration with Other Skills

### Works with bigquery-etl-core
- References core skill for conventions and patterns
- Uses common metadata structures and labeling

### Works with query-writer
- **After query-writer creates queries:** Use metadata-manager to generate schema/metadata
- Runs schema extraction from query output
- **Invocation:** After query.sql is written

### Works with sql-test-generator
- **When queries are modified:** Coordinates test update workflow
- **Handles simple updates directly:** expect.yaml changes, removing fixtures for deleted tables
- **Delegates complex fixture creation:** Invokes sql-test-generator for new source tables, JOINs, or production query issues
- **Invocation:** When new source tables added, tests query production, or complex test fixtures needed

### Typical Workflows

**Creating new table:**
1. query-writer creates query.sql
2. **metadata-manager** generates schema.yaml and metadata.yaml
3. metadata-manager invokes sql-test-generator for tests

**Updating existing query:**
1. Modify query.sql
2. **metadata-manager** updates schema.yaml
3. **metadata-manager** coordinates test updates (handles simple updates, invokes sql-test-generator for complex fixture creation)
4. Run tests to validate

## Key Commands Reference

```bash
# Create new query directory with templates
./bqetl query create <dataset>.<table> --dag <dag_name>

# Auto-generate/update schema from query output
./bqetl query schema update <dataset>.<table>

# Deploy schema to BigQuery (updates existing table)
./bqetl query schema deploy <dataset>.<table>

# Validate query and metadata
./bqetl query validate <dataset>.<table>

# Run tests
pytest tests/sql/<project>/<dataset>/<table>/ -v
```

## Best Practices

### ⚠️ Configuration Standards

**CRITICAL: Only use documented configurations or patterns from existing metadata files.**

- **DO:** Reference Mozilla BigQuery ETL documentation
- **DO:** Copy patterns from existing metadata.yaml files in `/sql`
- **DO:** Use configurations seen in templates in `assets/`
- **DO NOT:** Invent new configuration options
- **DO NOT:** Use undocumented fields or values

When uncertain about a configuration:
1. Check `references/metadata_yaml_guide.md`
2. Search existing metadata files: `grep -r "field_name" sql/*/metadata.yaml`
3. Ask user if the configuration is supported

### For metadata.yaml
- List at least 2 owners for redundancy (individuals and/or GitHub teams like `mozilla/team_name`)
- Use `python scripts/detect_teams.py` to find relevant GitHub teams (see "Script Maintenance" for testing)
- Write clear descriptions explaining purpose and use cases
- Use consistent labels matching similar tables
- Set appropriate partitioning and clustering for query patterns
- Consider data retention policies (expiration_days)

### For schema.yaml
- Always include descriptions for all fields
- **Use base schemas** to auto-populate standard field descriptions:
  - Run `./bqetl query schema update <dataset>.<table> --use-global-schema` for common fields
  - Ensures consistent descriptions across tables
  - Saves time writing descriptions for standard fields like `submission_date`, `client_id`, etc.
- Use appropriate types (DATE for dates, not STRING)
- Default to NULLABLE mode unless truly required
- Order fields as they appear in query SELECT
- Group related fields together
- Document units, formats, and constraints in descriptions

### For test updates
- **Always run tests after query changes**
- Invoke sql-test-generator for new source tables or complex changes
- Update expect.yaml for schema/output changes
- Add new test scenarios for new logic paths
- Never commit tests that query production tables

## Helper Scripts

This skill provides helper scripts in `scripts/`:
- **`detect_teams.py`** - Find GitHub teams from metadata.yaml files
- **`datahub_lineage.py`** - Generate DataHub lineage query parameters
- **`preview_base_schema.py`** - Preview base schema matches before applying

**See `references/script_maintenance.md` for:**
- Testing all scripts
- Auto-update workflow when scripts fail
- Common issues and solutions
- Adding new scripts

## Reference Examples

**In the repository:**
- Simple metadata: `sql/moz-fx-data-shared-prod/mozilla_vpn_derived/users_v1/metadata.yaml`
- Partitioned metadata: `sql/moz-fx-data-shared-prod/telemetry_derived/clients_daily_event_v1/metadata.yaml`
- Simple schema: `sql/moz-fx-data-shared-prod/mozilla_vpn_derived/users_v1/schema.yaml`
- Complex schema: `sql/moz-fx-data-shared-prod/telemetry_derived/event_events_v1/schema.yaml`

**In this skill:**
- See `assets/` directory for metadata and schema templates
- See `references/` directory for complete documentation

### DataHub Usage (CRITICAL for Token Efficiency)

**BEFORE using any DataHub MCP tools (`mcp__datahub-cloud__*`), you MUST:**
- **READ `../bigquery-etl-core/references/datahub_best_practices.md`** - Token-efficient patterns for schema and DAG discovery
- Always prefer local files (dags.yaml, metadata.yaml, schema.yaml) over DataHub queries

**Schema Discovery Priority:**
1. **FIRST:** `/sql` directory (schema.yaml files)
2. **SECOND:** DataHub (when schema not in `/sql`)

**Description Discovery Priority (for `_live`/`_stable` tables):**
1. **FIRST:** Glean Dictionary via https://dictionary.telemetry.mozilla.org/
2. **SECOND:** DataHub (when descriptions not in Glean Dictionary)

**IMPORTANT:** Glean Dictionary provides **descriptions only**, NOT schemas. Always get schema structure from `/sql` or DataHub.

**Use DataHub for:**
- Schema structure when not available in `/sql`
- Field descriptions when not in Glean Dictionary (for `_live`/`_stable` tables) or `/sql`
- Lineage/dependencies when can't infer from bqetl:
  - Tables from Glean telemetry or older telemetry sources
  - Syndicated datasets (directories without query.sql/query.py/view.sql)
  - These are often from dev teams' postgres databases in their own projects
  - Check metadata.yaml for available information first

**For lineage queries, use the helper script:**
```bash
python scripts/datahub_lineage.py <table_identifier>
```

This provides parameters for efficient DataHub queries that return only essential lineage information.

**See "Script Maintenance" section below for testing and troubleshooting.**
