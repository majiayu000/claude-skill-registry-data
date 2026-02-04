---
name: bigquery-etl-core
description: The core skill for working within the bigquery-etl repository. Use this skill when understanding project structure, conventions, and common patterns. Works with model-requirements, query-writer, metadata-manager, sql-test-generator, and bigconfig-generator skills.
---

# BigQuery ETL Core

**Composable:** Foundation skill that works with model-requirements, query-writer, metadata-manager, sql-test-generator, and bigconfig-generator skills
**When to use:** Understanding project structure, conventions, common patterns, and finding schema descriptions for construction

## Project Overview

The bigquery-etl project manages BigQuery table definitions, queries, and associated metadata for Mozilla. Similar to dbt, the repository maintains query definitions with associated metadata and schemas.

Each table/query typically consists of three files:
- `query.sql` OR `query.py` - The query definition (SQL or Python)
- `metadata.yaml` - Metadata about scheduling, ownership, and dependencies (see metadata-manager skill)
- `schema.yaml` - BigQuery schema definition with field types and descriptions (see metadata-manager skill)

**Note:** Most tables use `query.sql` (~95%). Use `query.py` for API calls, multi-project queries, or complex Python operations. See query-writer skill for details.

## 🚨 REQUIRED READING - Start Here

**When starting work in bigquery-etl, READ these foundational references:**

1. **Naming Conventions:** READ `references/naming_conventions.md`
   - Table naming patterns
   - Dataset organization
   - Version suffix conventions

2. **Dataset Organization:** READ `references/dataset_naming_conventions.md`
   - Common dataset suffixes (_derived, _stable, _live)
   - When to use each dataset type
   - Dataset naming rules

3. **Schema Resources:** READ `references/discovery_resources.md`
   - Schema description sources (Glean Dictionary, ProbeInfo API, DataHub)
   - Priority order for schema lookup during construction
   - Common mozfun UDFs

4. **Privacy Guidelines:** READ `references/privacy_guidelines.md`
   - Data handling requirements
   - PII considerations
   - Workgroup access patterns

## Directory Structure

```
sql/{project}/{dataset}/{table_name}/
├── query.sql OR query.py
├── metadata.yaml
└── schema.yaml
```

See `assets/directory_structure_example.txt` for detailed examples.

**Key principles:**
- Always flat: `sql/{project}/{dataset}/{table_name}/`
- Never use subdirectories within table directories
- Table names always include version suffix (`_v1`, `_v2`, etc.)

## Schema & Description Resources for Construction

### Finding Schema Descriptions

**Priority order for schema lookup during construction:**

1. **Local files first:** Check `sql/*/schema.yaml` and `metadata.yaml` files
   - Most reliable and up-to-date source
   - Contains field descriptions written by table owners

2. **Glean Dictionary:** For `_live` and `_stable` tables
   - URL: https://dictionary.telemetry.mozilla.org/
   - Contains metric descriptions from Glean schema definitions
   - Use WebFetch with targeted prompts to extract specific field descriptions

3. **ProbeInfo API:** For Glean metric metadata
   - Endpoints: `https://probeinfo.telemetry.mozilla.org/glean/{product}/metrics`
   - Provides metric definitions and descriptions programmatically
   - Use for validating metric references in queries

4. **DataHub MCP:** Only as last resort
   - **MUST READ `references/datahub_best_practices.md` BEFORE any DataHub queries**
   - Use for schema lookup when not available in local files or Glean Dictionary
   - Extract ONLY necessary fields (column names, types, descriptions)
   - Use for downstream impact analysis when modifying tables

**See `references/discovery_resources.md` for:**
- Detailed guidance on each schema source
- ProbeInfo API endpoints and usage patterns
- Glean Dictionary URL patterns for different products
- DataHub MCP best practices for construction
- Common mozfun UDFs
- Key documentation links

## Naming Conventions

**Table Names:**
- Use snake_case with version suffix: `clients_daily_event_v1`
- Common suffixes: `_daily`, `_hourly`, `_aggregates`, `_summary`

**Field Names:**
- Use snake_case: `submission_date`, `client_id`, `n_total_events`
- Prefix counts with `n_`: `n_events`, `n_sessions`
- Standard Mozilla fields: `submission_date`, `client_id`, `sample_id`, `normalized_channel`, `normalized_country_code`, `app_version`

**See `references/naming_conventions.md` for:**
- Complete naming patterns and conventions
- Reserved/common patterns to avoid
- BigQuery project naming conventions

## Dataset Organization

**See `references/dataset_naming_conventions.md` for:**
- Dataset naming patterns by suffix (`_derived`, `_external`, etc.)
- Common dataset prefixes by product/source
- Table versioning patterns
- Incremental vs full refresh query patterns

## Privacy & Data Handling

Mozilla follows strict data privacy policies:
- No PII in derived tables
- Use client-level identifiers (`client_id`) not individual identifiers
- Respect data retention policies (~2 years for client-level data)
- Label client-level tables with `table_type: client_level` in metadata.yaml

**See `references/privacy_guidelines.md` for:**
- Key principles from Mozilla's data platform
- Geo IP lookup and user agent parsing policies
- Best practices for data handling
- Deletion request support
- Sample ID usage for sampling

## BigQuery & Mozilla Conventions

### Partitioning & Clustering

- Most tables use day partitioning on `submission_date`
- Clustering improves query performance for filtered/joined fields
- See metadata-manager skill for detailed partitioning and clustering configuration

### Common UDFs (mozfun)

Browse available functions: https://mozilla.github.io/bigquery-etl/mozfun/

Common functions:
- `mozfun.map.get_key()` - Extract values from key-value maps
- `mozfun.norm.truncate_version()` - Normalize version strings
- `mozfun.stats.mode_last()` - Statistical mode calculation

UDF source code in `sql/mozfun/` directory.

## Glean Overview

Glean is Mozilla's product analytics & telemetry solution, providing consistent measurement across all Mozilla products.

**Key concepts:**
- **Metric types**: Counter, boolean, string, event, etc.
- **Pings**: Collections of metrics (e.g., `baseline`, `events`, `metrics`)
- **Applications**: Products using Glean (Fenix, Focus, Firefox iOS, etc.)

**Common Glean datasets in BigQuery:**
- Pattern: `{app_id}.{ping_name}` (e.g., `org_mozilla_fenix.baseline`)
- All have auto-generated schemas based on metric definitions

**See `references/glean_overview.md` for:**
- What is Glean and how it differs from Firefox Desktop Telemetry
- Glean SDK and metric type details
- Common Glean datasets in BigQuery
- When to use Glean Dictionary

## bigquery-etl CLI Commands

**See `references/bqetl_cli_commands.md` for:**
- Key bqetl CLI commands for query creation, validation, schema updates
- How to find the right DAG for scheduling
- Backfill creation commands

## Best Practices

**General principles:**
- Always include field descriptions in schema.yaml (see metadata-manager skill)
- Add header comments explaining query purpose (see query-writer skill)
- Reference bug/ticket numbers for context
- Document any data exclusions or filtering logic

**See `assets/query_structure_example.sql` for standard query structure.**

**Version migration:**
- Create new `_v2` table when making breaking schema changes
- Keep `_v1` running during migration period
- Update views to point to new version
- Coordinate with downstream consumers before deprecating old version

**For detailed best practices, see:**
- Query writing: query-writer skill
- Metadata configuration: metadata-manager skill
- Performance optimization: https://docs.telemetry.mozilla.org/cookbooks/bigquery/optimization.html
- Recommended practices: https://mozilla.github.io/bigquery-etl/reference/recommended_practices/

## Integration with Other Skills

**bigquery-etl-core** serves as the foundation skill that other skills build upon:

### Works with model-requirements
- Provides naming conventions for new tables and datasets
- Supplies common field naming patterns for requirements gathering
- Offers privacy guidelines for data model planning

### Works with query-writer
- Provides project structure and naming conventions
- Supplies common patterns and mozfun UDF references
- Offers schema description lookup guidance for construction

### Works with metadata-manager
- Provides DAG naming patterns and scheduling conventions
- Supplies partitioning and clustering best practices
- Offers ownership and labeling patterns

### Works with sql-test-generator
- Provides test structure and fixture naming conventions
- Supplies common table patterns for test creation
- Offers query parameter conventions

### Works with bigconfig-generator
- Provides table naming conventions for Bigeye monitoring configuration
- Supplies dataset organization patterns
- Offers field naming standards for data quality checks

**This skill is always available and does not need to be explicitly invoked** - it provides foundational knowledge that other skills reference.

## Reference Examples

Real query examples in the repository:
- **Simple query**: `sql/moz-fx-data-shared-prod/mozilla_vpn_derived/users_v1/query.sql`
- **Aggregation with GROUP BY**: `sql/moz-fx-data-shared-prod/telemetry_derived/clients_daily_event_v1/query.sql`
- **Complex query with CTEs**: `sql/moz-fx-data-shared-prod/telemetry_derived/event_events_v1/query.sql`
- **Python ETL (INFORMATION_SCHEMA)**: `sql/moz-fx-data-shared-prod/monitoring_derived/bigquery_table_storage_v1/query.py`
- **Python ETL (External API)**: `sql/moz-fx-data-shared-prod/bigeye_derived/user_service_v1/query.py`

For more examples, explore the `sql/moz-fx-data-shared-prod/` directory.

## Bundled Resources

### References
- `references/discovery_resources.md` - Schema description sources (Glean Dictionary, ProbeInfo API, DataHub MCP), priority order for construction, documentation links
- `references/naming_conventions.md` - Complete naming patterns for tables, fields, and projects
- `references/dataset_naming_conventions.md` - Dataset organization and versioning patterns
- `references/privacy_guidelines.md` - Mozilla data privacy policies and best practices
- `references/glean_overview.md` - Glean SDK concepts and BigQuery dataset structures
- `references/bqetl_cli_commands.md` - Key CLI commands and DAG discovery

### DataHub Usage (CRITICAL for Token Efficiency)

**BEFORE using any DataHub MCP tools (`mcp__datahub-cloud__*`), you MUST:**
- **READ `references/datahub_best_practices.md`** - Comprehensive token optimization strategies
- Follow priority order: local files → documentation → DataHub (only as last resort)
- Use search-first patterns and extract minimal fields from responses

### Assets
- `assets/query_structure_example.sql` - Standard query.sql structure with common patterns
- `assets/directory_structure_example.txt` - File organization examples
