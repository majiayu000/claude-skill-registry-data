---
name: btdp-it-masterdata-retrieval
description: |-
    Expert in retrieving IT masterdata and data lineage from L'Oréal's BTDP infrastructure. **Use this skill when user asks to search, find, or query for any BTDP/L'Oréal resource including: GCP projects, BigQuery datasets, BigQuery tables, Google Groups, applications, repositories, domains, IT organizations, people/users, GCP services, GCP SKUs, or APIs.** Also use for data lineage queries (upstream/downstream dependencies, parents/children).

    **Trigger keywords:** "search for project", "find the project", "find dataset", "search table", "what is the project", "what is the dataset", "what is the table", "what is the group", "what is the application", "find group", "search application", "show me project", "get project", "list projects", "lineage", "masterdata", "master data", "BTDP", "SDDS"

    **DO NOT use filesystem commands** (find, grep, ls) to search for BTDP resources. Always use this skill's RAG indices, MCP tools, or BigQuery SQL queries instead.
---

# Data Retrieval Specialist

Expert in retrieving IT masterdata from L'Oréal's Beauty Tech Data Platform (BTDP) using various retrieval methods including RAG indices, MCP tools, and SQL queries.

## Quick Decision Tree

```
What type of data?

├── **Lineage** → ./get_lineage.sh <table_full_id> [--parents|--children]
├── People → RAG: oa_pass_identities_name_v1
├── Code/Repos → RAG: smo_repository_v1
├── Applications → RAG: application_service_name_v1 OR SQL on application_service_v1
├── GCP Projects → RAG: smo_project_v1 or RAG: projects_v3
├── GCP Services → RAG: gcp_services_v1
├── GCP SKU → RAG: gcp_skus_v1
├── Datasets → RAG: smo_dataset_v1
├── Tables → RAG: smo_table_v1
├── Domains → RAG: domains_v1
├── IT Orgs → RAG: it_organizations_v3
├── Groups (Google Cloud Identity) → RAG: groups_v1 OR SQL on groups_v1
└── APIs → Use loreal-api-search skill
```

If you have a master data, you are not sure the kind of master data it is (Applications, GCP Service, IT Organization, Domains, People), you should try in the same time the main data type:
- Applications
- GCP Services
- IT Orgs
- Domains
- People

You take the most relevant and clearly mention to the user your assumption.

## Core Retrieval Methods

### 0. Data Lineage (BTDP Data Health Check API)

**When to use**: For table lineage - upstream dependencies (parents) or downstream impact (children)

**Script**: `./get_lineage.sh <table_full_id> [--parents|--children]`

**Flags**:
- `--parents` - Get upstream lineage (source tables)
- `--children` - Get downstream lineage (dependent tables)
- No flag (default) - Get both parents and children

**Authentication**: Uses `gcloud auth print-access-token` automatically

**Response**: JSON with nodes and connections graph from Neo4j

**Examples**:
```bash
# Get both upstream and downstream lineage (default)
./get_lineage.sh itg-btdppublished-gbl-ww-pd.btdp_ds_c1_0a1_gcpassets_eu_pd.tables_v2

# Get only upstream lineage (parents)
./get_lineage.sh itg-btdppublished-gbl-ww-pd.btdp_ds_c1_0a1_gcpassets_eu_pd.tables_v2 --parents

# Get only downstream lineage (children)
./get_lineage.sh itg-btdppublished-gbl-ww-pd.btdp_ds_c1_0a1_gcpassets_eu_pd.tables_v2 --children
```

**Workflow**:
```
User asks: "What is the lineage for tables_v2" or "Show parents of tables_v2"
1. Run ./get_lineage.sh with appropriate flag
2. Parse JSON response (nodes + connections)
3. Present lineage graph to user
```

### 1. RAG Index (Fastest, Semantic Search)

**When to use**: For semantic search over indexed masterdata (groups, projects, domains, applications, etc.)

**How to use**: Use the **rag-manager skill** for all RAG operations:
- List available RAG indices: Use `rag-manager` skill
- Search a RAG index: Use `rag-manager` skill
- Create a new RAG index: Use `rag-manager` skill
- Delete a RAG index: Use `rag-manager` skill

**Available RAG Indices for Masterdata**:
- `groups_v1` - Google Cloud Identity groups (12,808 records)
- `projects_v3` - GCP projects (5,577 records)
- `application_service_name_v1` - Application services (19,936 records)
- `business_application_v1` - Business applications (18,137 records)
- `domains_v1` - Data domains (19 records)
- `it_organizations_v3` - IT organizations (15 records)
- `oa_pass_identities_name_v1` - User identities (309,529 records)
- `smo_dataset_v1` - SMO datasets (30 records)
- `smo_project_v1` - SMO projects (12 records)
- `smo_table_v1` - SMO tables (48 records)

**Example workflow**:
```
User asks: "Find the group for exploradvanced"
1. Trigger rag-manager skill
2. Search groups_v1 index with query "exploradvanced"
3. Return results
```

### 2. MCP Tools (API-based retrieval)

**When to use**: For structured API-based data retrieval

- **APIs**: Use the `loreal-api-search` skill to search L'Oréal API Portal
- **Confluence Pages**: Use `mcp__atlassian__confluence_search` for Confluence content

### 3. SQL Queries (Direct BigQuery access)

**When to use**: For complex filtering, aggregations, or when RAG index is not available

**General SQL Pattern**:

1. **Find the table** using metadata table:
```bash
bq --project_id oa-data-btdpexploration-np query --nouse_legacy_sql --max_rows 10 \
'SELECT table_name AS table_ref
FROM `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_0a1_gcpassets_eu_pd.tables_v2`
WHERE project_id = "itg-btdppublished-gbl-ww-pd"
AND table_id = "{table_to_search}";'
```

2. **Get the schema**:
```bash
bq show --schema --format=prettyjson {table_ref_with_colon}
```

**Important:** When fetching the schema, replace the first dot with a colon.
Example: `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_0a1_gcpassets_eu_pd.tables_v2` becomes `itg-btdppublished-gbl-ww-pd:btdp_ds_c1_0a1_gcpassets_eu_pd.tables_v2`

3. **Execute the query**:
```bash
bq --project_id oa-data-btdpexploration-np query --nouse_legacy_sql --max_rows 10 '{SQL_QUERY}';
```

**Important:** Use `--max_rows` cleverly to ensure not too many results are loaded. For large results, use an intermediate file with stdout redirection.

## Environment Context

### Environments

There are 4 environments in the platform:
- **dv**: Dev/integration project. Developers have full permissions.
- **qa**: Quality assurance/test project. For non-regression tests. Dev team has full access.
- **np**: Pre-production/UAT/staging. Protected like production, with production data regularly loaded.
- **pd**: Production environment. Protected with limited viewer access for dev team.

### SDDS Project

The SDDS (Shared Domain Data Sets) project: `itg-btdppublished-gbl-ww-pd`

The exploration project: `oa-data-btdpexploration-np`
- Can be referred to as "btdp exploration", "btdp explo"
- When user says "show me my ... exploration", search resources in this project

### SDDS Naming Convention

- **SDDS Project**: `itg-btdppublished-gbl-ww-pd`
- **Dataset Naming**: `btdp_ds_c[123]_<domain_number>_<label>_eu_pd`
  - `c1`: Internal data for everyone
  - `c2`: Restricted data
  - `c3`: Very sensitive data with potential company impact
- **Domain Number Pattern**: 3 alphanumeric code where first character is domain_id
  - Example: `0a2` means domain_id 0 which is IT

## Masterdata Type Details

### Groups (Google Cloud Identity)

**Preferred Method**: RAG using `rag-manager` skill with `groups_v1` index

**SQL Fallback Table**: `itg-btdppublished-gbl-ww-pd.btdp_ds_c2_0a1_gcpassets_eu_pd.groups_v1`

**Schema**:
- `pk`: Primary key (INTEGER)
- `group_id`: Group identifier without domain (STRING) - e.g., `data-gcp-exploradvanced-advanced-dv`
- `group_description`: Group description (STRING)
- `group_email`: Full group email with domain (STRING) - e.g., `data-gcp-exploradvanced-advanced-dv@loreal.com`
- `total_members`: Number of members (INTEGER)
- `insert_timestamp`: Last update timestamp (TIMESTAMP)

**Search Tips for Groups**:
- **RAG search**: Use group name/ID without `@loreal.com` domain
  - Example: Search "exploradvanced" not "exploradvanced@loreal.com"
- **SQL search**: Use `group_id` field for pattern matching
  - Use `LOWER()` for case-insensitive search
  - Use `%pattern%` for partial matches

**Example SQL - Search for groups**:
```bash
bq --project_id oa-data-btdpexploration-np query --nouse_legacy_sql --max_rows 20 \
"SELECT group_email, group_id, group_description, total_members
FROM \`itg-btdppublished-gbl-ww-pd.btdp_ds_c2_0a1_gcpassets_eu_pd.groups_v1\`
WHERE LOWER(group_id) LIKE '%exploradvanced%'
LIMIT 20"
```

**Example SQL - Get specific group**:
```bash
bq --project_id oa-data-btdpexploration-np query --nouse_legacy_sql \
"SELECT *
FROM \`itg-btdppublished-gbl-ww-pd.btdp_ds_c2_0a1_gcpassets_eu_pd.groups_v1\`
WHERE group_id = 'data-gcp-exploradvanced-advanced-dv'"
```

### GCP Projects

**Preferred Method**: RAG using `rag-manager` skill with `projects_v3` or `smo_project_v1` index

**SQL Fallback**: Query project metadata tables in SDDS

### Applications

**Preferred Method**: RAG using `rag-manager` skill with `application_service_name_v1` or `business_application_v1` index

**SQL Table**: `itg-btdpfront-gbl-ww-pd.btdp_ds_c1_053_apm_eu_pd.application_service_v1`

### Domains

**Preferred Method**: RAG using `rag-manager` skill with `domains_v1` index

**SQL Table**: `itg-btdpfront-gbl-ww-pd.btdp_ds_c1_0r0_referentials_eu_pd.domains_v1`

### IT Organizations

**Preferred Method**: RAG using `rag-manager` skill with `it_organizations_v3` index

**SQL Table**: `itg-btdpfront-gbl-ww-pd.btdp_ds_c1_0r0_referentials_eu_pd.it_organizations_v3`

### People (User Identities)

**Preferred Method**: RAG using `rag-manager` skill with `oa_pass_identities_name_v1` index

**SQL Table**: `itg-btdpfront-gbl-ww-pd.btdp_ds_c1_058_identity_eu_pd.oa_pass_identities_v1`

### APIs

**Method**: Use the `loreal-api-search` skill to search for APIs in the L'Oréal API Portal.

The skill uses Azure OAuth authentication to access the API Portal and can:
- Search APIs by pattern
- Retrieve API metadata
- Fetch OpenAPI specifications

## Retrieval Strategy (Priority Order)

```
1. RAG Index (fastest, semantic search)
   → Use rag-manager skill for all RAG operations

2. MCP Tools (API-based, structured data)
   → Use loreal-api-search for APIs
   → Use mcp__atlassian__confluence_search for Confluence pages

3. SQL Fallback (direct BigQuery, complex filtering)
   → Find table using metadata
   → Get schema
   → Execute query

4. If still not found
   → Broaden search terms
   → Verify table names
   → Check available RAG indices with rag-manager skill
```

## Common Workflows

### Workflow 0: Get Table Lineage

```
1. User asks: "What is the lineage for tables_v2" or "Show parents of customer_table"
2. Run ./get_lineage.sh with table full ID and appropriate flag
3. Parse response showing nodes (tables) and connections (dependencies)
4. Present lineage graph
```

**Example**:
```bash
# Full lineage
./get_lineage.sh itg-btdppublished-gbl-ww-pd.btdp_ds_c1_0a1_gcpassets_eu_pd.tables_v2

# Only upstream
./get_lineage.sh itg-btdppublished-gbl-ww-pd.btdp_ds_c1_0a1_gcpassets_eu_pd.tables_v2 --parents
```

### Workflow 1: Find a Google Group

```
1. User asks: "Find the group for btdp exploration"
2. Use rag-manager skill to search groups_v1 index
3. If no results, try SQL fallback on groups_v1 table
4. Return group_email and details
```

### Workflow 2: Find a GCP Project

```
1. User asks: "What is the project for btdp exploration"
2. Use rag-manager skill to search projects_v3 or smo_project_v1 index
3. Return project_id and details
```

### Workflow 3: Find an Application

```
1. User asks: "Find the application for sales data"
2. Use rag-manager skill to search application_service_name_v1 index
3. Return application details
```

### Workflow 4: Find a Table in SDDS

```
1. User asks: "What is the table for GCP costs"
2. Use rag-manager skill to search smo_table_v1 index
3. If not in SMO referentials, search metadata table using SQL
4. Return table reference
```

### Workflow 5: Find an API

```
1. User asks: "Find the API for user authentication"
2. Use loreal-api-search skill
3. Return API details and OpenAPI spec if needed
```

## Best Practices

1. **For lineage**: Use `./get_lineage.sh` with appropriate flags (--parents, --children, or both)
2. **Always prefer RAG search** when available for speed and semantic matching
3. **Use rag-manager skill** for all RAG operations (list, search, create, delete)
4. **Use SQL fallback** only when RAG doesn't return results or for complex filtering
5. **Check available RAG indices** using rag-manager skill before deciding on retrieval method
6. **Leverage other skills** (loreal-api-search, rag-manager) to avoid duplication
7. **Use proper case sensitivity** in SQL queries with `LOWER()` for text matching
8. **Limit results** appropriately using `--max_rows` or `LIMIT` clauses
error: cannot format -: Cannot parse: 1:3: ---
error: cannot format -: Cannot parse: 1:3: ---
error: cannot format -: Cannot parse: 1:3: ---
error: cannot format -: Cannot parse: 1:3: ---
error: cannot format -: Cannot parse: 1:3: ---
error: cannot format -: Cannot parse: 1:3: ---
error: cannot format -: Cannot parse: 1:3: ---
