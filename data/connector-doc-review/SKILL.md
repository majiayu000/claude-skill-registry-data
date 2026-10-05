---
name: connector-doc-review
description: Review and fix OpenMetadata connector documentation against JSON schema and source code. Validates availableFeatures, permissions, yaml.mdx configuration, and overall completeness. Automatically fixes gaps.
user-invocable: true
argument-hint: "<connector-name> [--service-type=database|pipeline|dashboard|messaging|storage|search|mlmodel] [--version=v1.13.x|v2.0.x|v2.1.x-SNAPSHOT|all] [--dry-run]"
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - Edit
  - Write
  - Agent
---

# Connector Documentation Review & Fix Skill

## When to Activate

When a user asks to review, validate, audit, or fix connector documentation — checking it against the actual JSON schema and ingestion source code.

## Arguments

- **connector-name** (required): Name of the connector (e.g., `redshift`, `dynamodb`, `bigquery`, `airflow`, `looker`, `kafka`)
- **--service-type** (optional): One of `database`, `pipeline`, `dashboard`, `messaging`, `storage`, `search`, `mlmodel`. Default: auto-detect from connector name.
- **--version** (optional): Which version to review. Default: `all` (reviews v1.13.x, v2.0.x).
- **--dry-run** (optional): Only report issues, don't fix them.

## Directory References

```
DOCS_ROOT     = .                          # The docs-om repo (current working directory)
OM_ROOT       = ../OpenMetadata            # Sibling directory to docs-om
SCHEMA_ROOT   = ${OM_ROOT}/openmetadata-spec/src/main/resources/json/schema/entity/services
SOURCE_ROOT   = ${OM_ROOT}/ingestion/src/metadata/ingestion/source
```

## Review Process

### Phase 1: Gather Ground Truth from Code

#### Step 1.1: Read the JSON Schema

Read the connector's JSON schema to extract the canonical list of capabilities and configuration fields.

```
Schema file: ${SCHEMA_ROOT}/connections/${service_type}/${connectorName}Connection.json
```

Extract:
1. **All properties** — field names, types, descriptions, required fields, defaults
2. **`supports*` boolean flags** — these define what the connector can do
3. **Filter pattern fields** — `schemaFilterPattern`, `tableFilterPattern`, `storedProcedureFilterPattern`, etc.
4. **`sampleDataStorageConfig`** — presence indicates Sample Data support
5. **Authentication references** — `$ref` to auth schemas (basicAuth, iamAuthConfig, awsCredentials, gcpCredentials, etc.). Build a list of supported authentication types (e.g., "Basic Auth", "IAM Auth", "OAuth2", "API Key", "GCP Credentials") from the `authType` property's `oneOf`/`anyOf` references.
6. **SSL configuration** — `sslMode`, `sslConfig`, `verifySSL`
7. **Required fields** — the `required` array

Also read the parent service schema to verify the connector is registered:
```
Service schema: ${SCHEMA_ROOT}/${serviceType}Service.json
```

#### Step 1.2: Read the Source Code

Read these files for the connector:

```
${SOURCE_ROOT}/${service_type}/${connector_name}/metadata.py    — Source class, capabilities
${SOURCE_ROOT}/${service_type}/${connector_name}/connection.py  — Connection, test steps, permissions
${SOURCE_ROOT}/${service_type}/${connector_name}/service_spec.py — Service spec (lineage, usage, profiler classes)
```

Extract:
1. **Test connection steps** — the `test_fn` dictionary in `test_connection()`. Each key represents a permission/capability the connector validates.
2. **Service spec classes** — which source classes are registered (lineage_source_class, usage_source_class, profiler_class). Their presence confirms feature support.
3. **Source class mixins/base classes** — what the source extends (e.g., `LifeCycleQueryMixin`, `MultiDBSource`, `CommonNoSQLSource`)
4. **Owner extraction** — search for `yield_tag` or owner-related methods in the source to determine if Owners/Tags are supported
5. **Any permission-related comments or docstrings** — hints about required IAM roles, database grants, etc.

Also check for:
```
${SOURCE_ROOT}/${service_type}/${connector_name}/queries.py     — SQL queries (for permission requirements)
${SOURCE_ROOT}/${service_type}/${connector_name}/client.py      — API client (for REST connectors)
```

#### Step 1.3: Build the Feature Truth Table

Using the schema and code, build a definitive feature map:

**For Database Connectors:**

| Schema Signal | Available Feature String | Unavailable Feature String |
|---|---|---|
| `supportsMetadataExtraction: true` | "Metadata" | — |
| `supportsUsageExtraction: true` | "Query Usage" | "Query Usage" if false |
| `supportsLineageExtraction: true` | "View Lineage" or "Lineage" | "Lineage" if false |
| `supportsViewLineageExtraction: true` | "View Column-level Lineage" or "Column-level Lineage" | "Column-level Lineage" if false |
| `supportsProfiler: true` | "Data Profiler" | "Data Profiler" if false |
| `supportsDBTExtraction: true` | "dbt" | "dbt" if false |
| `supportsDataDiff: true` | "Data Quality" | "Data Quality" if false |
| `storedProcedureFilterPattern` present | "Stored Procedures" | "Stored Procedures" if absent |
| `sampleDataStorageConfig` present | "Sample Data" | "Sample Data" if absent |
| `supportsProfiler: true` (implicit) | "Auto-Classification" | "Auto-Classification" if profiler false |
| Check source code for owner extraction | "Owners" if supported | "Owners" if not |
| Check source code for tag extraction | "Tags" if supported | "Tags" if not |

**For Pipeline Connectors:**

| Schema Signal | Available Feature String |
|---|---|
| Always | "Pipelines" |
| Check code for status extraction | "Pipeline Status" |
| `supportsLineageExtraction: true` or lineage source in spec | "Lineage" |
| Check code for owner extraction | "Owners" |
| Check code for usage tracking | "Usage" |
| Check code for tag extraction | "Tags" |

**For Dashboard Connectors:**

| Schema Signal | Available Feature String |
|---|---|
| Always | "Dashboards", "Charts" |
| Check code for datamodel extraction | "Datamodels" |
| Check code for project support | "Projects" |
| `supportsLineageExtraction: true` or lineage source in spec | "Lineage" |
| Check code for column lineage | "Column Lineage" |
| Check code for owner extraction | "Owners" |
| Check code for usage tracking | "Usage" |
| Check code for tag extraction | "Tags" |

**For Messaging Connectors:**

| Schema Signal | Available Feature String |
|---|---|
| Always | "Topics" |
| Check for sample data support | "Sample Data" |

**For Storage Connectors:**

| Schema Signal | Available Feature String |
|---|---|
| Always | "Metadata" |
| Check code for structured containers | "Structured Containers" |
| Check code for unstructured containers | "Unstructured Containers" |

**For Search Connectors:**

| Schema Signal | Available Feature String |
|---|---|
| Always | "Search Indexes" |
| Check for sample data support | "Sample Data" |

**For ML Model Connectors:**

| Schema Signal | Available Feature String |
|---|---|
| Always | "ML Features" |
| Check for hyperparameters | "Hyperparameters" |
| Check for ML store | "ML Store" |

### Phase 2: Read Current Documentation

For each version being reviewed (v1.13.x, v2.0.x):

#### Step 2.1: Read the Main Connector Page

```
${DOCS_ROOT}/${version}/connectors/${service_type}/${connector_name}.mdx
```

Extract:
1. **`availableFeatures`** array from `<ConnectorDetailsHeader>`
2. **`unavailableFeatures`** array from `<ConnectorDetailsHeader>`
3. **`stage`** value (PROD or BETA)
4. **Requirements section** — documented permissions, grants, IAM policies
5. **Connection details section** — documented configuration fields
6. **Sections present** — which optional sections exist (Query Usage, Lineage, Data Profiler, Data Quality, dbt, Troubleshooting)
7. **Authentication type callout** — check if an `<Info>` callout listing supported authentication types exists near the top of the page (after the intro text, before the table of contents)

#### Step 2.2: Read the YAML Page

```
${DOCS_ROOT}/${version}/connectors/${service_type}/${connector_name}/yaml.mdx
```

If it exists, extract:
1. **YAML example** in the CodePanel — all configuration fields shown
2. **ContentSection definitions** — field descriptions in the ContentPanel
3. **Optional sections** — Query Usage, Lineage, Data Profiler, Auto-Classification, Data Quality
4. **ConnectorDetailsHeader** — should match the main page

#### Step 2.3: Check Navigation Registration

```
${DOCS_ROOT}/docs.json
```

Verify:
1. The main connector page is registered in navigation
2. The yaml.mdx page is registered (if it exists)
3. Pages are in the correct version section

### Phase 3: Compare and Identify Issues

Run these validation checks and categorize findings:

#### Check 1: Available Features Accuracy

Compare `availableFeatures` in docs against the truth table from Phase 1.

- **MISSING**: Feature should be available (per schema/code) but is NOT in `availableFeatures`
- **INCORRECT**: Feature is in `availableFeatures` but should NOT be (per schema/code)
- **WRONG_LIST**: Feature is in `unavailableFeatures` but should be in `availableFeatures`, or vice versa

Severity: **WARNING** for each mismatch.

#### Check 2: Unavailable Features Completeness

Verify that features NOT supported are listed in `unavailableFeatures`. A feature that is neither available nor unavailable is confusing to users.

Severity: **SUGGESTION** for missing entries in unavailableFeatures.

#### Check 3: Permission Documentation

Compare documented permissions against:
- Test connection steps (from `connection.py`)
- SQL queries executed (from `queries.py`)
- API calls made (from `client.py` or source code)

Check for:
- **MISSING_PERMISSION**: A permission required by code but not documented
- **EXTRA_PERMISSION**: A permission documented but not actually needed
- **UNCLEAR_PERMISSION**: Permission listed without explanation of why it's needed

For database connectors, verify documented SQL grants match the queries. For cloud connectors (AWS/GCP/Azure), verify IAM policy actions match API calls.

Severity: **WARNING** for missing permissions, **SUGGESTION** for unclear ones.

#### Check 4: YAML Configuration Completeness

Compare the YAML example in `yaml.mdx` against the JSON schema properties:

- **MISSING_FIELD**: A schema property (especially required ones) not shown in YAML example
- **EXTRA_FIELD**: A field in YAML that doesn't exist in schema
- **WRONG_DEFAULT**: Default value in YAML doesn't match schema default
- **MISSING_DESCRIPTION**: A ContentSection is missing for a documented field
- **OUTDATED_DESCRIPTION**: ContentSection description doesn't match schema description

Severity: **WARNING** for missing required fields, **SUGGESTION** for optional ones.

#### Check 5: Section Completeness

Based on the feature truth table, verify the documentation has the right sections:

- If `supportsUsageExtraction: true` → Query Usage section should exist
- If `supportsLineageExtraction: true` → Lineage section should exist
- If `supportsProfiler: true` → Data Profiler section should exist
- If `supportsDBTExtraction: true` → dbt section or link should exist
- If `supportsDataDiff: true` → Data Quality section should exist

Severity: **WARNING** for missing sections.

#### Check 6: Cross-Version Consistency

If reviewing all versions, check that features and permissions are consistent across versions (unless a known version difference exists).

Severity: **SUGGESTION** for inconsistencies.

#### Check 7: Authentication Type Highlighting

Verify that the supported authentication types are highlighted at the top of the page using an `<Info>` callout. This callout should appear after the intro text and before the table of contents, listing each authentication method the connector supports (derived from the `authType` property in the JSON schema).

Expected format:
```jsx
<Info>
**Supported Authentication Types:**
- **Basic Auth** — Username and password authentication
- **IAM Auth** — AWS IAM-based authentication with automatic temporary credential retrieval (supports both Provisioned Clusters and Serverless Workgroups)
</Info>
```

Common authentication type labels by schema reference:
- `basicAuth.json` → **Basic Auth** — Username and password authentication
- `iamAuthConfig.json` → **IAM Auth** — AWS IAM-based authentication with automatic temporary credential retrieval
- `awsCredentials.json` → **AWS Credentials** — AWS access key, secret key, and optional session token
- `gcpCredentials.json` → **GCP Credentials** — Google Cloud service account authentication
- `azureCredentials.json` → **Azure Credentials** — Azure service principal or managed identity authentication
- OAuth2 references → **OAuth 2.0** — Token-based authentication
- API key/token references → **API Key** — API key or token authentication

Check for:
- **MISSING_AUTH_CALLOUT**: No `<Info>` callout with authentication types exists at the top
- **INCOMPLETE_AUTH_CALLOUT**: Callout exists but is missing authentication types that the schema supports
- **STALE_AUTH_CALLOUT**: Callout lists authentication types not supported by the schema

Severity: **WARNING** for missing callout, **SUGGESTION** for incomplete/stale.

This check applies to both the main page and the yaml.mdx page.

### Phase 4: Report Findings

Present a structured report:

```markdown
## Connector Documentation Review: {connector_name}

### Ground Truth (from schema + code)

**Service Type**: {service_type}
**Schema File**: {path}
**Source Files**: {paths}

**Supported Features**: [list]
**Unsupported Features**: [list]
**Required Permissions**: [list with explanations]
**Required Configuration Fields**: [list]

### Findings

#### {version}

| # | Check | Severity | Finding | Current | Expected |
|---|-------|----------|---------|---------|----------|
| 1 | Features | WARNING | Missing "Data Quality" in availableFeatures | [...] | [...] |
| 2 | Permissions | WARNING | Missing dynamodb:DescribeTable | - | Required for metadata extraction |
| ... | | | | | |

### Summary

- **Warnings**: {count} (should fix)
- **Suggestions**: {count} (nice to have)
```

### Phase 5: Fix Issues (unless --dry-run)

After presenting the report, fix all findings automatically:

#### 5a. Fix Available/Unavailable Features

Edit the `<ConnectorDetailsHeader>` component in both the main page and yaml.mdx to match the truth table. Ensure both pages use identical feature arrays.

#### 5b. Fix Permissions Documentation

Add missing permissions with clear explanations. Format as:
- For AWS: IAM policy JSON with action descriptions
- For databases: SQL GRANT statements with explanations
- For REST APIs: Required API scopes/roles

Make permissions user-friendly:
- Group by capability (metadata extraction, profiling, lineage)
- Explain WHY each permission is needed
- Provide copy-pasteable policy/grant blocks

#### 5c. Fix YAML Configuration

Update the YAML example to include all schema properties with correct defaults. Update ContentSection descriptions to match schema descriptions.

#### 5d. Fix Missing Sections

Add missing documentation sections using the standard snippet pattern. Import the appropriate shared snippets.

#### 5e. Fix Authentication Type Callout

If the `<Info>` callout for authentication types is missing or incomplete, add or update it in both the main page and yaml.mdx. Insert it after the intro sentence ("In this section, we provide guides and references to use the {connector} connector.") and before the table of contents. Derive the authentication types from the JSON schema's `authType` property. Use the label mapping from Check 7. For connectors with cloud-specific auth (IAM, GCP, Azure), include relevant details like supported deployment types.

#### 5f. Ensure Cross-Version Consistency

Apply the same fixes across all versions being reviewed.

### Phase 6: Verify Fixes

After applying fixes:
1. Re-read the modified files to confirm changes look correct
2. Verify ConnectorDetailsHeader has matching features in both main and yaml pages
3. Verify all required fields are in the YAML example
4. Present a before/after summary

```
Before: 5 warnings, 3 suggestions
After:  0 warnings, 0 suggestions

Fixed:
#1 WARNING  Added "Data Quality" to availableFeatures
#2 WARNING  Added dynamodb:DescribeTable to permissions
#3 WARNING  Added missing hostPort field to YAML example
...
```

## Feature String Reference

### Database Connectors - All Possible Features
```
Available: "Metadata", "Query Usage", "Data Profiler", "Data Quality", "dbt",
           "View Lineage" | "Lineage", "View Column-level Lineage" | "Column-level Lineage",
           "Stored Procedures", "Sample Data", "Auto-Classification",
           "Owners", "Tags"

Unavailable: same strings for features NOT supported
```

### Pipeline Connectors
```
Available/Unavailable: "Pipelines", "Pipeline Status", "Lineage", "Owners", "Usage", "Tags"
```

### Dashboard Connectors
```
Available/Unavailable: "Dashboards", "Charts", "Datamodels", "Projects",
                       "Lineage", "Column Lineage", "Owners", "Usage", "Tags"
```

### Messaging Connectors
```
Available/Unavailable: "Topics", "Sample Data"
```

### Storage Connectors
```
Available/Unavailable: "Metadata", "Structured Containers", "Unstructured Containers"
```

### Search Connectors
```
Available/Unavailable: "Search Indexes", "Sample Data"
```

### ML Model Connectors
```
Available/Unavailable: "ML Features", "Hyperparameters", "ML Store"
```

## Schema Flag to Feature Mapping (Database)

| JSON Schema Flag | Default | Maps To |
|---|---|---|
| `supportsMetadataExtraction` | `true` | "Metadata" |
| `supportsUsageExtraction` | `true` | "Query Usage" |
| `supportsLineageExtraction` | `true` | "View Lineage" or "Lineage" |
| `supportsViewLineageExtraction` | `true` | "View Column-level Lineage" or "Column-level Lineage" |
| `supportsProfiler` | `true` | "Data Profiler" |
| `supportsDBTExtraction` | `true` | "dbt" |
| `supportsDataDiff` | `true` | "Data Quality" |
| `supportsSystemProfile` | `false` | (no direct feature, informational) |
| `supportsQueryComment` | `true` | (no direct feature, informational) |
| `supportsDatabase` | `true` | (no direct feature, structural) |
| `storedProcedureFilterPattern` | (present/absent) | "Stored Procedures" |
| `sampleDataStorageConfig` | (present/absent) | "Sample Data" |
| `supportsProfiler` (implicit) | same as profiler | "Auto-Classification" |

## Permission Documentation Best Practices

When documenting permissions, follow these guidelines:

### Database Connectors (SQL)
```markdown
### Requirements

To extract metadata, the user needs the following permissions:

#### Metadata Ingestion
- `USAGE` on schemas — to list and access schemas
- `SELECT` on tables — to read table metadata and sample data

#### Profiler & Data Quality
- `SELECT` on tables — to run profiling queries

#### Usage & Lineage
- Access to query history views (e.g., `pg_stat_statements`, `stl_query`)
```

### Cloud Connectors (AWS)
```markdown
### Requirements

The IAM user/role needs the following permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "service:ListAction",     // Required for: discovering resources
        "service:DescribeAction", // Required for: extracting metadata
        "service:ReadAction"      // Required for: profiling/sampling
      ],
      "Resource": "*"
    }
  ]
}
```
```

### Cloud Connectors (GCP)
```markdown
### Requirements

The service account needs the following roles:
- `roles/viewer` — for metadata extraction
- `roles/bigquery.dataViewer` — for profiling and sampling
```

## YAML Documentation Best Practices

### ContentSection Pattern
Each configuration field should have a ContentSection with:
1. **Bold field name** matching the YAML key
2. **Description** matching or expanding on the schema description
3. **Type info** for non-obvious fields
4. **Link to relevant docs** for complex fields (auth, SSL, etc.)

### YAML Example Requirements
- All `required` schema fields MUST appear in the YAML example
- Optional fields with non-null defaults SHOULD appear
- Sensitive fields should use placeholder values: `"{password}"`, `"{access_key}"`
- Filter patterns should show the default include/exclude
- Comments should be minimal — only for non-obvious fields

### Section Ordering in yaml.mdx
1. Frontmatter
2. Imports
3. ConnectorDetailsHeader (must match main page)
4. Table of Contents
5. External Ingestion Deployment snippet
6. Requirements (Python + connector-specific)
7. Metadata Ingestion (CodePreview with YAML)
8. Query Usage (if supported)
9. Lineage (if supported)
10. Data Profiler (if supported)
11. Auto-Classification (if supported)
12. Data Quality (if supported)
13. dbt Integration (link)
