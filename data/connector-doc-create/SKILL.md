---
name: connector-doc-create
description: Create full documentation for a new OpenMetadata connector from scratch — generates main page, yaml.mdx, troubleshooting page, and registers in docs.json navigation. Derives features, permissions, and YAML config from JSON schema and source code.
user-invocable: true
argument-hint: "<connector-name> [--display-name='Display Name'] [--service-type=database|pipeline|dashboard|messaging|storage|search|ml-model] [--stage=PROD|BETA] [--version=v1.13.x|v2.0.x|v2.1.x-SNAPSHOT|all] [--icon=/path/to/icon.svg] [--dry-run]"
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - Edit
  - Write
  - Agent
---

# Connector Documentation Creation Skill

## When to Activate

When a user asks to create, generate, scaffold, or add documentation for a **new** connector — one that exists in source code but doesn't yet have docs pages.

## Arguments

- **connector-name** (required): Slug name of the connector (e.g., `redshift`, `dynamodb`, `bigquery`, `airflow`, `looker`, `kafka`). Must match the directory name in `${SOURCE_ROOT}/${service_type}/`.
- **--display-name** (optional): Human-readable name shown in docs (e.g., `"Amazon Redshift"`, `"Google BigQuery"`). Defaults to title-cased connector-name.
- **--service-type** (optional): One of `database`, `pipeline`, `dashboard`, `messaging`, `storage`, `search`, `ml-model`. Note: use `ml-model` (with hyphen) — this matches the actual directory name. Other types (`api`, `drive`, `metadata`) exist in the repo but are rare; treat them like `pipeline` if encountered. Default: auto-detect from connector name and schema.
- **--stage** (optional): `PROD` or `BETA`. Default: `BETA` for new connectors.
- **--version** (optional): Which version(s) to create docs for. Default: `all` (creates in v1.13.x, v2.0.x).
- **--icon** (optional): Path to icon file under `/public/images/connectors/`. If not given, uses `/public/images/connectors/{connector-name}.svg` as a placeholder.
- **--dry-run** (optional): Only show the plan and generated content — don't write any files.

## Directory References

```
DOCS_ROOT     = .                          # The docs-om repo (current working directory)
OM_ROOT       = ../OpenMetadata            # Sibling directory to docs-om
SCHEMA_ROOT   = ${OM_ROOT}/openmetadata-spec/src/main/resources/json/schema/entity/services
SOURCE_ROOT   = ${OM_ROOT}/ingestion/src/metadata/ingestion/source
```

---

## Creation Process

### Phase 1: Read Ground Truth from Source Code

#### Step 1.1: Read the JSON Schema

```
Schema file: ${SCHEMA_ROOT}/connections/${service_type}/${connectorName}Connection.json
```

Extract:
1. **All properties** — field names, types, descriptions, required fields, defaults
2. **`supports*` boolean flags** — determines available/unavailable features
3. **Filter pattern fields** — `schemaFilterPattern`, `tableFilterPattern`, `storedProcedureFilterPattern`, etc.
4. **`sampleDataStorageConfig`** — presence indicates Sample Data support
5. **Authentication types** — `authType` property's `oneOf`/`anyOf` references:
   - `basicAuth.json` → **Basic Auth**
   - `iamAuthConfig.json` → **IAM Auth**
   - `awsCredentials.json` → **AWS Credentials**
   - `gcpCredentials.json` → **GCP Credentials**
   - `azureCredentials.json` → **Azure Credentials**
6. **SSL fields** — `sslMode`, `sslConfig`, `verifySSL`
7. **Required fields** — the `required` array

Also check the parent service schema to confirm registration:
```
${SCHEMA_ROOT}/${serviceType}Service.json
```

#### Step 1.2: Read the Source Code

Read these files:

```
${SOURCE_ROOT}/${service_type}/${connector_name}/metadata.py    — Source class, capabilities
${SOURCE_ROOT}/${service_type}/${connector_name}/connection.py  — Connection logic, test steps, permissions
${SOURCE_ROOT}/${service_type}/${connector_name}/service_spec.py — Registered source classes
```

Also check if these exist:
```
${SOURCE_ROOT}/${service_type}/${connector_name}/queries.py     — SQL queries (reveals permission requirements)
${SOURCE_ROOT}/${service_type}/${connector_name}/client.py      — REST API client
```

Extract:
1. **Test connection steps** — `test_fn` dict keys in `test_connection()` → permission names
2. **Service spec classes** — lineage_source_class, usage_source_class, profiler_class (confirm feature support)
3. **Mixin/base classes** — what the source extends (e.g., `LifeCycleQueryMixin`, `MultiDBSource`)
4. **Owner/Tag extraction** — search for `yield_tag`, `yield_table_tag`, `get_tag_labels`, owner-related methods
5. **Permission hints** — SQL grants, IAM actions, API scopes in docstrings or comments
6. **Python package name** — `pip install "openmetadata-ingestion[{package}]"` (check pyproject.toml or setup.py if unsure)

#### Step 1.3: Build the Feature Truth Table

Using schema + code, build the definitive feature map:

**For Database Connectors:**

| Signal | Feature |
|---|---|
| `supportsMetadataExtraction: true` (default) | "Metadata" → available |
| `supportsUsageExtraction: true` | "Query Usage" → available |
| `supportsLineageExtraction: true` | "Lineage" or "View Lineage" → available |
| `supportsViewLineageExtraction: true` | "Column-level Lineage" → available |
| `supportsProfiler: true` | "Data Profiler" → available |
| `supportsProfiler: true` (implicit) | "Auto-Classification" → available |
| `supportsDBTExtraction: true` | "dbt" → available |
| `supportsDataDiff: true` | "Data Quality" → available |
| `storedProcedureFilterPattern` present | "Stored Procedures" → available |
| `sampleDataStorageConfig` present | "Sample Data" → available |
| Owner extraction code found | "Owners" → available |
| Tag extraction code found | "Tags" → available |

**For Pipeline Connectors:**

| Signal | Feature |
|---|---|
| Always | "Pipelines" → available |
| Status extraction code found | "Pipeline Status" → available |
| lineage_source_class in service_spec | "Lineage" → available |
| Owner extraction code found | "Owners" → available |
| Tag extraction code found | "Tags" → available |

**For Dashboard Connectors:**

| Signal | Feature |
|---|---|
| Always | "Dashboards", "Charts" → available |
| Datamodel extraction code found | "Datamodels" → available |
| Project extraction code found | "Projects" → available |
| lineage_source_class in service_spec | "Lineage" → available |
| Column lineage code found | "Column Lineage" → available |
| Owner extraction code found | "Owners" → available |
| usage_source_class in service_spec | "Usage" → available |
| Tag extraction code found | "Tags" → available |

**For Messaging Connectors:**

| Signal | Feature |
|---|---|
| Always | "Topics" → available |
| `sampleDataStorageConfig` present | "Sample Data" → available |

**For Storage Connectors:**

| Signal | Feature |
|---|---|
| Always | "Metadata" → available |
| Structured container code found | "Structured Containers" → available |
| Unstructured container code found | "Unstructured Containers" → available |

**For Search Connectors:**

| Signal | Feature |
|---|---|
| Always | "Search Indexes" → available |
| Sample data code found | "Sample Data" → available |

**For ML Model Connectors:**

| Signal | Feature |
|---|---|
| Always | "ML Features" → available |
| Hyperparameter code found | "Hyperparameters" → available |
| ML store code found | "ML Store" → available |

#### Step 1.4: Build the Permissions List

From the extracted code, derive the permission requirements:

- **Database connectors**: Map SQL queries to required GRANT statements. Common pattern:
  - Reading system views/tables → `SELECT` on those views
  - `information_schema` reads → `USAGE` on schema
  - Query history access → specific grants (e.g., `pg_read_all_stats`)
- **AWS connectors**: Map API calls to IAM actions (e.g., `dynamodb:ListTables`, `s3:GetObject`)
- **GCP connectors**: Map API calls to GCP roles/permissions
- **REST API connectors**: Map endpoints to required API scopes/roles

Group permissions by capability:
1. Metadata Ingestion
2. Profiler & Data Quality (if supported)
3. Usage & Lineage (if supported)

#### Step 1.5: Extract YAML Configuration Fields

From the JSON schema `properties`, build a YAML config template:

1. Start with `required` fields — these MUST appear, no comments
2. Add important optional fields with commented-out examples
3. Use placeholder values: `<username>`, `<password>`, `<hostname>`, `<database>`
4. For auth type fields (`oneOf`/`anyOf`): show the most common auth type uncommented, others as commented blocks
5. For filter patterns: show commented-out example with `includes`/`excludes`
6. For SSL: show commented-out block

Build ContentSection entries for each field shown in YAML:
- Match the YAML key name exactly
- Use the schema `description` as the base, expand if needed
- For complex fields (auth, SSL), add links to relevant docs pages

---

### Phase 2: Check for Existing Files

Before creating anything, check:

1. Does `${DOCS_ROOT}/{version}/connectors/${service_type}/${connector_name}.mdx` already exist?
2. Does `${DOCS_ROOT}/{version}/connectors/${service_type}/${connector_name}/yaml.mdx` already exist?
3. Is the connector already registered in `docs.json`?

If files exist, **stop and warn the user** — use the `connector-doc-review` skill instead to update existing docs.

---

### Phase 3: Generate Documentation Files

For each target version (v1.13.x, v2.0.x):

#### Step 3.1: Generate the Main Page (`{connector_name}.mdx`)

**File path:** `${DOCS_ROOT}/{version}/connectors/${service_type}/${connector_name}.mdx`

**Template — varies by service type. Use the correct imports and structure for the connector's service type:**

**Shared imports (all service types):**
```mdx
import { ConnectorDetailsHeader } from '/snippets/components/ConnectorDetailsHeader/ConnectorDetailsHeader.jsx'
import TestConnection from '/snippets/connectors/test-connection.mdx'
import IngestionScheduleAndDeploy from '/snippets/connectors/ingestion-schedule-and-deploy.mdx'
import { MetadataIngestionUi } from '/snippets/components/MetadataIngestionUi.jsx'
```

**Service-type-specific imports for main page:**

| Service Type | ConfigureIngestion | Extra imports |
|---|---|---|
| `database` | `/snippets/connectors/database/configure-ingestion.mdx` | `AdvancedConfiguration` from `/snippets/connectors/database/advanced-configuration.mdx`; `Related` from `/snippets/{version}/connectors/database/related.mdx` |
| `pipeline` | `/snippets/connectors/pipeline/configure-ingestion.mdx` | — |
| `dashboard` | `/snippets/connectors/dashboard/configure-ingestion.mdx` | — |
| `messaging` | `/snippets/connectors/messaging/configure-ingestion.mdx` | — |
| `storage` | `/snippets/connectors/storage/configure-ingestion.mdx` | `Manifest` from `/snippets/connectors/storage/manifest.mdx`; **do NOT use MetadataIngestionUi** |
| `search` | `/snippets/connectors/search/configure-ingestion.mdx` | — |
| `ml-model` | `/snippets/connectors/ml-model/configure-ingestion.mdx` | — |

**Steps block — varies by service type:**

- **Database only**: include `<AdvancedConfiguration />` between Connection Details Step and `<TestConnection />`
- **All types**: include `<TestConnection />`, `<ConfigureIngestion />`, `<IngestionScheduleAndDeploy />`
- **Database only**: include `<Related />` at bottom of page
- **Storage only**: include `<Manifest />` in requirements section (OpenMetadata manifest file is required)

**MetadataIngestionUi**: Used by database, pipeline, dashboard, search, ml-model. **NOT used by storage** (storage uses manual step descriptions instead).

**Full template:**

```mdx
---
title: "{DisplayName} Connector | OpenMetadata {ServiceType} Integration"
description: "Connect {DisplayName} to OpenMetadata with our comprehensive {service_type} connector guide. Step-by-step setup, configuration examples, and metadata extraction tips."
sidebarTitle: Overview
---

{service-type-specific imports — see table above}

<ConnectorDetailsHeader
icon='/public/images/connectors/{connector_name}.svg'
name="{DisplayName}"
stage="{PROD|BETA}"
availableFeatures={[{availableFeatures}]}
unavailableFeatures={[{unavailableFeatures}]} />

In this section, we provide guides and references to use the {DisplayName} connector.

{IF multiple auth types: include <Info> callout listing them}

Configure and schedule {DisplayName} metadata workflows from the OpenMetadata UI:
- [Requirements](#requirements)
- [Metadata Ingestion](#metadata-ingestion)
{IF database AND Query Usage supported: - [Query Usage](/{version}/connectors/ingestion/workflows/usage)}
{IF database AND Profiler supported: - [Data Profiler](/{version}/how-to-guides/data-quality-observability/profiler/profiler-workflow)}
{IF database AND Data Quality supported: - [Data Quality](/{version}/how-to-guides/data-quality-observability/quality)}
{IF database AND Lineage supported: - [Lineage](/{version}/connectors/ingestion/lineage)}
{IF database AND dbt supported: - [dbt Integration](/{version}/connectors/database/dbt)}
- [Troubleshooting](/{version}/connectors/{service_type}/{connector_name}/troubleshooting)

## Requirements

{permissions section — derive from code analysis}
{For DB connectors: SQL GRANT statements}
{For cloud connectors: IAM policy JSON or GCP roles}
{For storage connectors: include Manifest requirement}

## Metadata Ingestion

{IF NOT storage:
<MetadataIngestionUi connector="{DisplayName}" selectServicePath="/public/images/connectors/{connector_name}/select-service.png" addNewServicePath="/public/images/connectors/{connector_name}/add-new-service.png" serviceConnectionPath="/public/images/connectors/{connector_name}/service-connection.png" />
}

# Connection Details

<Steps>
<Step title="Connection Details">

{field-by-field description of each connection property from schema}
{Group auth options under sub-headings if multiple auth types}

</Step>
{IF database: <AdvancedConfiguration />}
<TestConnection />
<ConfigureIngestion />
<IngestionScheduleAndDeploy />
</Steps>

{IF SSL supported:
## Securing {DisplayName} Connection with SSL in OpenMetadata
...SSL configuration instructions...
}

{IF database: <Related />}
```

**Authentication Info Callout** (add after intro paragraph if multiple auth types):

```jsx
<Info>
**Supported Authentication Types:**
- **{Auth Type 1}** — {description}
- **{Auth Type 2}** — {description}
</Info>
```

**Auth type labels:**
- `basicAuth.json` → **Basic Auth** — Username and password authentication
- `iamAuthConfig.json` → **IAM Auth** — AWS IAM-based authentication (supports Provisioned Clusters and Serverless Workgroups)
- `awsCredentials.json` → **AWS Credentials** — AWS access key, secret key, and optional session token
- `gcpCredentials.json` → **GCP Credentials** — Google Cloud service account authentication
- `azureCredentials.json` → **Azure Credentials** — Azure service principal or managed identity authentication

#### Step 3.2: Generate the YAML Page (`{connector_name}/yaml.mdx`)

**File path:** `${DOCS_ROOT}/{version}/connectors/${service_type}/${connector_name}/yaml.mdx`

**Template:**

```mdx
---
title: "Run the {DisplayName} Connector Externally"
description: "Use YAML to configure {DisplayName} {service_type} connections with metadata ingestion, profiling, and schema extraction."
sidebarTitle: Run Externally
mode: "wide"
---

import { ConnectorDetailsHeader } from '/snippets/components/ConnectorDetailsHeader/ConnectorDetailsHeader.jsx'
import { CodePreview, ContentPanel, ContentSection, CodePanel } from '/snippets/components/CodePreview.jsx'
import PythonRequirements from '/snippets/connectors/python-requirements.mdx'
import ExternalIngestionDeployment from '/snippets/{version}/connectors/external-ingestion-deployment.mdx'
import IngestionSinkDef from '/snippets/connectors/yaml/ingestion-sink-def.mdx'
import WorkflowConfigDef from '/snippets/connectors/yaml/workflow-config-def.mdx'
import IngestionCli from '/snippets/connectors/yaml/ingestion-cli.mdx'
import IngestionSink from '/snippets/connectors/yaml/ingestion-sink.mdx'
import WorkflowConfig from '/snippets/connectors/yaml/workflow-config.mdx'
import SourceConfigDef from '/snippets/connectors/yaml/database/source-config-def.mdx'
import SourceConfig from '/snippets/connectors/yaml/database/source-config.mdx'
{IF Query Usage: import QueryUsage from '/snippets/connectors/yaml/query-usage.mdx'}
{IF Lineage: import Lineage from '/snippets/connectors/yaml/lineage.mdx'}
{IF Data Profiler: import DataProfiler from '/snippets/{version}/connectors/yaml/data-profiler.mdx'}
{IF Auto-Classification: import AutoClassification from '/snippets/connectors/yaml/auto-classification.mdx'}
{IF Data Quality: import DataQuality from '/snippets/connectors/yaml/data-quality.mdx'}
{IF AWS auth: import AwsConfigDef from '/snippets/connectors/yaml/common/aws-config-def.mdx'}
{IF GCP auth: import GcpConfigDef from '/snippets/connectors/yaml/common/gcp-config-def.mdx'}

<ConnectorDetailsHeader
icon='/public/images/connectors/{connector_name}.svg'
name="{DisplayName}"
stage="{PROD|BETA}"
availableFeatures={[{same as main page}]}
unavailableFeatures={[{same as main page}]} />

In this section, we provide guides and references to use the {DisplayName} connector.

{same <Info> auth callout as main page if multiple auth types}

Configure and schedule {DisplayName} metadata and profiler workflows from the OpenMetadata UI:
- [Requirements](#requirements)
- [Metadata Ingestion](#metadata-ingestion)
{IF Query Usage: - [Query Usage](#query-usage)}
{IF Lineage: - [Lineage](#lineage)}
{IF Data Profiler: - [Data Profiler](#data-profiler)}
{IF Data Quality: - [Data Quality](#data-quality)}
{IF dbt: - [dbt Integration](#dbt-integration)}

<ExternalIngestionDeployment />

## Requirements

{same permissions section as main page}

### Python Requirements

<PythonRequirements />

To run the {DisplayName} ingestion, you will need to install:

```bash
pip3 install "openmetadata-ingestion[{package_name}]"
```

## Metadata Ingestion

All connectors are defined as JSON Schemas.
[Here](https://github.com/open-metadata/OpenMetadata/blob/main/openmetadata-spec/src/main/resources/json/schema/entity/services/connections/{service_type}/{connectorName}Connection.json)
you can find the structure to create a connection to {DisplayName}.

In order to create and run a Metadata Ingestion workflow, we will follow
the steps to create a YAML configuration able to connect to the source,
process the Entities if needed, and reach the OpenMetadata server.

The workflow is modeled around the following
[JSON Schema](https://github.com/open-metadata/OpenMetadata/blob/main/openmetadata-spec/src/main/resources/json/schema/metadataIngestion/workflow.json)

### 1. Define the YAML Config

<CodePreview>

<ContentPanel>

<ContentSection id={1} title="Source Configuration" lines="1-3">

Configure the source type and service name for your {DisplayName} connector.

</ContentSection>

{one ContentSection per field group, derived from schema properties}

<ContentSection id={N} title="Source Config" lines="{lines}">

<SourceConfigDef />

</ContentSection>

<ContentSection id={N+1} title="Sink Configuration" lines="{lines}">

<IngestionSinkDef />

</ContentSection>

<ContentSection id={N+2} title="Workflow Configuration" lines="{lines}">

<WorkflowConfigDef />

</ContentSection>

</ContentPanel>

<CodePanel fileName="{connector_name}_config.yaml">

```yaml
{full YAML configuration derived from schema}
```

<SourceConfig />

<IngestionSink />

<WorkflowConfig />

</CodePanel>

</CodePreview>

<IngestionCli />

{IF Query Usage: <QueryUsage connector="{connector_name}" />}
{IF Lineage: <Lineage connector="{connector_name}" />}
{IF Data Profiler: <DataProfiler connector="{connector_name}" />}
{IF Auto-Classification: <AutoClassification connector="{connector_name}" />}
{IF Data Quality: <DataQuality />}

{IF dbt:
## dbt Integration

You can learn more about how to ingest dbt models' definitions and their lineage [here](/{version}/connectors/database/dbt).
}
```

**YAML Field Line Numbering**: Count actual YAML lines in your generated CodePanel and reference the correct line ranges in each ContentSection.

**ContentPanel structure differs by service type:**

- **Database connectors**: Wrap `SourceConfigDef`, `IngestionSinkDef`, `WorkflowConfigDef` inside their own `ContentSection` elements at the end of the ContentPanel.
- **Messaging, Pipeline, Dashboard connectors**: Place `SourceConfigDef`, `IngestionSinkDef`, `WorkflowConfigDef` **directly** in the ContentPanel (not in ContentSections), before all field-specific ContentSections. Do NOT give these Def snippets line refs — they render as general description, not tied to specific YAML lines.

Messaging/Pipeline/Dashboard pattern:
```mdx
<ContentPanel>

<SourceConfigDef />
<IngestionSinkDef />
<WorkflowConfigDef />

<ContentSection id={1} title="Source Configuration" lines="1-3">
...
</ContentSection>

{field-specific ContentSections only}

</ContentPanel>
```

#### Step 3.3: Generate the Troubleshooting Page (`{connector_name}/troubleshooting.mdx`)

**File path:** `${DOCS_ROOT}/{version}/connectors/${service_type}/${connector_name}/troubleshooting.mdx`

**Template:**

```mdx
---
title: "{DisplayName} Troubleshooting | OpenMetadata Connector"
description: "Troubleshoot common {DisplayName} connector issues in OpenMetadata — connection failures, permission errors, and ingestion problems."
sidebarTitle: Troubleshooting
---

import Troubleshooting from '/snippets/connectors/troubleshooting.mdx'

<Troubleshooting />
```

If code analysis reveals permission-sensitive operations or known failure modes, add connector-specific sections after `<Troubleshooting />`:

```mdx
## {DisplayName}-Specific Issues

### {Issue Title}
{Description of the issue and resolution}
```

---

### Phase 4: Register in Navigation (`docs.json`)

After generating files, register the connector in `docs.json` for each target version.

#### Step 4.1: Find the Right Insertion Point

Search `docs.json` for the version's connector group. For example, for `v2.0.x` database connectors, find the `"Database Connectors"` group and locate the alphabetically correct position among existing connector groups.

**Search pattern:** Look for the adjacent connector alphabetically (e.g., for `"mssql"`, look for `"mysql"` or `"mongodb"` groups).

#### Step 4.2: Insert the Navigation Group

Insert a new group object at the correct alphabetical position:

```json
{
  "group": "{DisplayName}",
  "pages": [
    "{version}/connectors/{service_type}/{connector_name}",
    "{version}/connectors/{service_type}/{connector_name}/yaml",
    "{version}/connectors/{service_type}/{connector_name}/troubleshooting"
  ]
}
```

Do this for **each** target version in `docs.json`.

---

### Phase 5: Present Plan and Confirm (unless --dry-run skipped)

Before writing any files, present the full plan:

```markdown
## New Connector Documentation: {DisplayName}

### Ground Truth
**Service Type**: {service_type}
**Stage**: {PROD|BETA}
**Python Package**: openmetadata-ingestion[{package}]
**Icon**: /public/images/connectors/{connector_name}.webp

### Feature Matrix
**Available**: {list}
**Unavailable**: {list}

### Auth Types
{list of supported auth types}

### Permissions Required
{summary}

### Files to Create (per version: {versions})
- {version}/connectors/{service_type}/{connector_name}.mdx         ← Main page
- {version}/connectors/{service_type}/{connector_name}/yaml.mdx    ← YAML guide
- {version}/connectors/{service_type}/{connector_name}/troubleshooting.mdx ← Troubleshooting

### Navigation
- docs.json: Add "{DisplayName}" group in {N} version sections

### Notes / Gaps
{any fields or sections that need manual attention — missing icon, unclear permissions, etc.}
```

If `--dry-run`, stop here and show the generated file contents as code blocks without writing.

---

### Phase 6: Write the Files

Write each file using the generated content:

1. Create the directory `{version}/connectors/{service_type}/{connector_name}/` if it doesn't exist
2. Write `{connector_name}.mdx` at the parent level
3. Write `{connector_name}/yaml.mdx`
4. Write `{connector_name}/troubleshooting.mdx`
5. Edit `docs.json` to insert the navigation group at the correct alphabetical position

Repeat for all target versions.

---

### Phase 7: Verify and Report

After writing all files:

1. Re-read each created file to confirm content looks correct
2. Grep `docs.json` to confirm the new pages are registered
3. Check that `availableFeatures` and `unavailableFeatures` are identical between main page and yaml.mdx
4. Check that YAML ContentSection line references are plausible given the YAML length
5. Verify all snippet imports resolve — **known exception**: `/snippets/v1.13.x/connectors/external-ingestion-deployment.mdx` does not exist on disk. This is intentional — all existing v1.13.x connectors use this same path as a placeholder for the snippet that will be created when the version is finalized. Do NOT flag this as an error.

Present a final summary:

```markdown
## Documentation Created: {DisplayName}

### Files Written
- ✓ v1.13.x/connectors/{service_type}/{connector_name}.mdx
- ✓ v1.13.x/connectors/{service_type}/{connector_name}/yaml.mdx
- ✓ v1.13.x/connectors/{service_type}/{connector_name}/troubleshooting.mdx
- ✓ v2.0.x/connectors/{service_type}/{connector_name}.mdx
- ✓ v2.0.x/connectors/{service_type}/{connector_name}/yaml.mdx
- ✓ v2.0.x/connectors/{service_type}/{connector_name}/troubleshooting.mdx
- ✓ docs.json (navigation registered in 2 version sections)

### Feature Matrix
**Available**: {list}
**Unavailable**: {list}

### Manual Follow-up Needed
- [ ] Add connector icon at /public/images/connectors/{connector_name}.webp
- [ ] Add UI screenshots at /public/images/connectors/{connector_name}/
- [ ] Review and refine permissions section with domain expert
- [ ] {any other gaps identified}
```

---

## Content Quality Guidelines

### Requirements Section (Permissions)

Write permissions so they are copy-pasteable and explain the "why":

**For database connectors (SQL):**
```markdown
## Requirements

To extract metadata, the database user needs the following privileges:

#### Metadata Ingestion
```sql
-- Grant usage on all schemas you want to ingest
GRANT USAGE ON SCHEMA <schema_name> TO <user>;
-- Grant select on all tables and views
GRANT SELECT ON ALL TABLES IN SCHEMA <schema_name> TO <user>;
```

#### Usage & Lineage
```sql
-- Required to read query history
GRANT SELECT ON <query_history_view> TO <user>;
```
```

**For AWS connectors (IAM):**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "service:ListX",       // Required for: listing resources during metadata extraction
        "service:DescribeX"    // Required for: reading resource details
      ],
      "Resource": "*"
    }
  ]
}
```

**For GCP connectors:**
```markdown
The service account needs these roles:
- `roles/viewer` — for metadata extraction
- `roles/bigquery.dataViewer` — for profiling and data sampling
```

### Connection Details Section (Main Page)

Each field description should:
- Lead with the field name in bold: `**Username**: ...`
- Explain what value to provide (not just repeat the field name)
- Note if a field is required vs. optional
- For complex fields (auth types), use nested sub-headings
- For enum fields (SSL modes), list each option with a short description

### YAML Configuration Best Practices

- All `required` fields: uncommented with placeholder values
- Important optional fields: uncommented with defaults or placeholders
- Sensitive values: use angle-bracket placeholders: `<password>`, `<api_key>`
- SSL/filter patterns: comment out with `# ` prefix
- Include inline comments for non-obvious fields
- Align `:` for readability within related field groups

---

## Service-Type Reference Tables

### Snippet Paths by Service Type

| Service Type | ConfigureIngestion (main page) | SourceConfigDef (yaml) | SourceConfig (yaml) |
|---|---|---|---|
| `database` | `/snippets/connectors/database/configure-ingestion.mdx` | `/snippets/connectors/yaml/database/source-config-def.mdx` | `/snippets/connectors/yaml/database/source-config.mdx` |
| `pipeline` | `/snippets/connectors/pipeline/configure-ingestion.mdx` | `/snippets/connectors/yaml/pipeline/source-config-def.mdx` | `/snippets/connectors/yaml/pipeline/source-config.mdx` |
| `dashboard` | `/snippets/connectors/dashboard/configure-ingestion.mdx` | `/snippets/connectors/yaml/dashboard/source-config-def.mdx` | `/snippets/connectors/yaml/dashboard/source-config.mdx` |
| `messaging` | `/snippets/connectors/messaging/configure-ingestion.mdx` | `/snippets/connectors/yaml/messaging/source-config-def.mdx` | `/snippets/connectors/yaml/messaging/source-config.mdx` |
| `storage` | `/snippets/connectors/storage/configure-ingestion.mdx` | `/snippets/connectors/yaml/storage/source-config-def.mdx` | `/snippets/connectors/yaml/storage/source-config.mdx` |
| `search` | `/snippets/connectors/search/configure-ingestion.mdx` | `/snippets/connectors/yaml/search/source-config-def.mdx` | `/snippets/connectors/yaml/search/source-config.mdx` |
| `ml-model` | `/snippets/connectors/ml-model/configure-ingestion.mdx` | `/snippets/connectors/yaml/ml-model/source-config-def.mdx` | `/snippets/connectors/yaml/ml-model/source-config.mdx` |

### Behaviour Differences by Service Type

| Feature | database | pipeline | dashboard | messaging | storage | search | ml-model |
|---|---|---|---|---|---|---|---|
| `<AdvancedConfiguration />` in Steps | **YES** | NO | NO | NO | NO | NO | NO |
| `<Related />` at page bottom | **YES** | NO | NO | NO | NO | NO | NO |
| `<MetadataIngestionUi />` | YES | YES | YES | YES | NO | YES | YES |
| `<Manifest />` in requirements | NO | NO | NO | NO | **YES** | NO | NO |
| Post-YAML workflow sections | **YES** (Lineage, DataProfiler, AutoClassification, DataQuality, QueryUsage) | NO | NO | NO | NO | NO | NO |
| Data Profiler import (version-specific) | **YES** — `/snippets/{version}/connectors/yaml/data-profiler.mdx` | NO | NO | NO | NO | NO | NO |
| ContentPanel: Defs in ContentSections | **YES** (database wraps Defs inside ContentSections) | NO (Defs before ContentSections) | NO | NO | NO | NO | NO |

### Post-YAML Workflow Sections (database only)

```mdx
<IngestionCli />
{IF Query Usage: <QueryUsage connector="{connector_name}" />}
{IF Lineage: <Lineage connector="{connector_name}" />}
{IF Data Profiler: <DataProfiler connector="{connector_name}" />}
{IF Auto-Classification: <AutoClassification connector="{connector_name}" />}
{IF Data Quality: <DataQuality />}
```

For all other service types, only `<IngestionCli />` follows the CodePreview block.

### Cloud Provider Config Snippets (for connectors with AWS/GCP/Azure auth)

```
AWS:   import AwsConfigDef from '/snippets/connectors/yaml/common/aws-config-def.mdx'
       import AwsConfig from '/snippets/connectors/yaml/common/aws-config.mdx'
GCP:   import GcpConfigDef from '/snippets/connectors/yaml/common/gcp-config-def.mdx'
       import GcpConfig from '/snippets/connectors/yaml/common/gcp-config.mdx'
Azure: import AzureConfigDef from '/snippets/connectors/yaml/common/azure-config-def.mdx'
       import AzureConfig from '/snippets/connectors/yaml/common/azure-config.mdx'
```

These are used in the CodePanel alongside SourceConfig when the connector authenticates via cloud credentials.

> **Note:** Always verify snippet paths exist in the repo before using them. The `ml-model` directory uses a hyphen — do not write `mlmodel`.

---

## Feature String Reference

### Database Connectors
```
All possible: "Metadata", "Query Usage", "Data Profiler", "Data Quality", "dbt",
              "Lineage", "View Lineage", "Column-level Lineage", "View Column-level Lineage",
              "Stored Procedures", "Stored Procedures Lineage", "Sample Data",
              "Auto-Classification", "Owners", "Tags"
```

### Pipeline Connectors
```
All possible: "Pipelines", "Pipeline Status", "Lineage", "Owners", "Usage", "Tags"
```

### Dashboard Connectors
```
All possible: "Dashboards", "Charts", "Datamodels", "Projects",
              "Lineage", "Column Lineage", "Owners", "Usage", "Tags"
```

### Messaging Connectors
```
All possible: "Topics", "Sample Data"
```

### Storage Connectors
```
All possible: "Metadata", "Structured Containers", "Unstructured Containers"
```

### Search Connectors
```
All possible: "Search Indexes", "Sample Data"
```

### ML Model Connectors (`ml-model`)
```
All possible: "ML Features", "Hyperparameters", "ML Store"
```

---

## Example Invocations

```
# Create docs for a new database connector
connector-doc-create clickhouse --service-type database --display-name "ClickHouse"

# Create docs for a new pipeline connector, BETA stage, only latest version
connector-doc-create airflow --service-type pipeline --stage BETA --version v2.0.x

# Preview what would be created without writing files
connector-doc-create snowflake --dry-run

# Create docs with a custom display name and icon path
connector-doc-create sap-hana --display-name "SAP HANA" --icon /public/images/connectors/sap-hana.webp
```