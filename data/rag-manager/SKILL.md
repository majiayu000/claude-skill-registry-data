---
name: rag-manager
description: Expert in managing RAG (Retrieval-Augmented Generation) indices for L'Oréal's BTDP infrastructure. **TRIGGER THIS SKILL when user asks:** "list RAG", "create RAG", "delete RAG", "search RAG", "available RAG indices", or any operation involving RAG index management (list, create, delete, search).
---

# RAG Manager

Expert in managing RAG (Retrieval-Augmented Generation) indices using the BTDP RAG API.

## What is RAG?

RAG (Retrieval-Augmented Generation) indices provide semantic search capabilities over BigQuery tables. Instead of exact string matching, RAG uses embeddings to find semantically similar records based on natural language queries.

## When to Use RAG

- **Semantic Search**: Find records based on meaning, not just exact keywords
- **Fast Lookups**: Quick retrieval without writing SQL queries
- **Natural Language**: Search using conversational queries
- **Fuzzy Matching**: Find similar terms even with typos or variations

## Helper Scripts

This skill includes efficient shell scripts for all RAG operations. **ALWAYS use these scripts instead of direct curl commands** to ensure reliability and proper error handling.

Available scripts in `~/.claude/skills/rag-manager/`:
- `rag_list.sh` - List all available RAG indices
- `rag_search.sh` - Search a RAG index with a query
- `rag_create.sh` - Create a new RAG index
- `rag_delete.sh` - Delete a RAG index

## RAG Operations

### List Available RAG Indices

**USE THE SCRIPT** (recommended):

```bash
~/.claude/skills/rag-manager/rag_list.sh [output_format]

# Output formats: json (default), summary

# Example - JSON output:
~/.claude/skills/rag-manager/rag_list.sh json

# Example - Summary (just names and counts):
~/.claude/skills/rag-manager/rag_list.sh summary
```

**Script Output**:
- JSON format: Full RAG configuration details including source tables, fields, record counts, and last update timestamps
- Summary format: Simple list with index names and record counts

**Response Structure (JSON)**:
```json
{
  "configurations": [
    {
      "object_name": "groups_v1",
      "source_table": "itg-btdpfront-gbl-ww-pd.btdp_ds_c2_0a1_gcpassets_eu_pd.groups_v1",
      "fields_included": ["group_id"],
      "task_type": "SEMANTIC_SIMILARITY",
      "last_update": "2025-11-18T17:15:37.419000+00:00",
      "record_count": 12808,
      "table_size_bytes": 80664063,
      "workflow_name": "rag-refresh-groups_v1",
      "state_machine_name": "rag-monitor-groups_v1"
    }
  ],
  "total_count": 13
}
```

### Search a RAG Index

**USE THE SCRIPT** (recommended):

```bash
~/.claude/skills/rag-manager/rag_search.sh <index_name> <query> [limit] [output_file]

# Example - basic search:
~/.claude/skills/rag-manager/rag_search.sh groups_v1 "explorationaladvanced" 10

# Example - search with output to file:
~/.claude/skills/rag-manager/rag_search.sh smo_table_v1 "GCP costs" 5 /tmp/results.json

# Example - search for projects:
~/.claude/skills/rag-manager/rag_search.sh projects_v3 "btdp exploration" 10
```

**Parameters**:
- `index_name`: Name of the RAG index to search (get from `rag_list.sh`)
- `query`: Natural language search query (semantic search)
- `limit`: Maximum number of results to return (default: 10)
- `output_file`: Optional file path to save results

**Script Output**:
- Displays query, index name, and result count
- Outputs JSON results (formatted)
- If output_file specified, saves to file and shows summary

**Important Search Tips**:
- Don't include redundant index type in query unless meaningful
  - ✅ "GCP datasets" on index `smo_table_v1`
  - ❌ "GCP datasets table" on index `smo_table_v1`
- Use natural language and semantic meaning
- The search is fuzzy - exact matches not required
- Results are ranked by semantic similarity

**Example Response**:
```json
{
  "query": "explorationaladvanced",
  "index_name": "groups_v1",
  "results": [
    {
      "group_id": "data-gcp-exploradvanced-advanced-dv",
      "group_email": "data-gcp-exploradvanced-advanced-dv@loreal.com",
      "distance": 0.234
    }
  ]
}
```

### Create a New RAG Index

**Supported Data Levels:** The RAG API supports **C1 and C2** confidential data levels.
- C1 datasets: `^[a-z0-9]+_ds_c1_.*` (Internal data for everyone)
- C2 datasets: `^[a-z0-9]+_ds_c2_.*` (Restricted data)
- **C3 datasets are NOT supported** due to high sensitivity

**USE THE SCRIPT** (recommended):

```bash
~/.claude/skills/rag-manager/rag_create.sh <table_reference> <object_name> <fields_to_include_comma_separated>

# Example - Create RAG for a C1 table:
~/.claude/skills/rag-manager/rag_create.sh \
  "itg-btdppublished-gbl-ww-pd.btdp_ds_c1_0a1_gcpassets_eu_pd.tables_v2" \
  "tables_rag_v1" \
  "table_id,description"

# Example - Create RAG for Groups (C2 data):
~/.claude/skills/rag-manager/rag_create.sh \
  "itg-btdppublished-gbl-ww-pd.btdp_ds_c2_0a1_gcpassets_eu_pd.groups_v1" \
  "groups_v1" \
  "group_id"
```

**Script Features**:
- Validates dataset is C1 or C2 (rejects C3)
- Shows configuration before creating
- Handles errors gracefully
- Returns creation success/failure with details

**Parameters**:
- `table_reference`: Full BigQuery table reference with **C1 or C2 dataset**
  - Format: `project_id.dataset_id.table_id`
  - Must be from a C1 or C2 dataset
- `object_name`: Name for the RAG index
  - Must start with a letter
  - Alphanumeric and underscores only
  - Will be used as the index identifier
- `fields_to_include`: Comma-separated field names to embed
  - Choose text/string columns for best semantic search
  - Multiple fields will be concatenated for embedding
  - Example: `name,description` or `group_id`

**What happens when you create a RAG index:**
1. Creates a BigQuery embedding table with vector representations
2. Sets up a Cloud Workflow for refreshing embeddings when source data changes
3. Configures a Cloud Scheduler for monitoring table updates
4. Initial embedding process begins (may take time for large tables)

**Example Response**:
```json
{
  "object_name": "my_new_index",
  "source_table": "project.dataset.table",
  "fields_included": ["field1", "field2"],
  "status": "created",
  "workflow_name": "rag-refresh-my_new_index"
}
```

### Delete a RAG Index

**USE THE SCRIPT** (recommended):

```bash
~/.claude/skills/rag-manager/rag_delete.sh <object_name>

# Example:
~/.claude/skills/rag-manager/rag_delete.sh groups_v1
```

**Script Features**:
- Prompts for confirmation before deletion
- Handles errors gracefully
- Returns deletion success/failure
- Cleans up associated resources (workflows, schedulers)

**Parameters**:
- `object_name`: Name of the RAG index to delete (get from `rag_list.sh`)

**Warning**: Deletion is permanent and will remove:
- The embedding table
- The Cloud Workflow for refresh
- The Cloud Scheduler monitoring job

## RAG Index Search Best Practices

### For Group Searches

When searching for Google Cloud Identity groups using RAG:
- The RAG index uses `group_id` field for semantic search (NOT `group_email`)
- **Remove the `@loreal.com` domain** from your search query
- The query returns `group_email` in the results

**Examples**:
```bash
# CORRECT: Search without @loreal.com domain
~/.claude/skills/rag-manager/rag_search.sh groups_v1 "data-gcp-team" 10

# Use partial names
~/.claude/skills/rag-manager/rag_search.sh groups_v1 "btdp datasrv" 10

# Use keywords
~/.claude/skills/rag-manager/rag_search.sh groups_v1 "sales prod" 10
```

### General Search Tips

1. **Use natural language**: "GCP cost analysis tables" instead of "table_cost"
2. **Be specific but not too specific**: "sales data europe" not "sales_eu_prod_v2_table"
3. **Avoid redundancy**: Don't repeat the index type in query
4. **Multiple keywords work**: "btdp exploration project" finds relevant projects
5. **Fuzzy matching**: Typos and variations are handled automatically

## Common RAG Indices Available

| RAG Index | Purpose | Fields Indexed |
|-----------|---------|----------------|
| `groups_v1` | Google Cloud Identity groups | `group_id` |
| `projects_v3` | GCP projects | `project_id_curated` |
| `application_service_name_v1` | Application services | `name` |
| `domains_v1` | Data domains | `domain_name` |
| `it_organizations_v3` | IT organizations | `it_organization` |
| `oa_pass_identities_name_v1` | User identities | `display_name` |
| `gcp_services_v1` | GCP services | `service_description` |
| `gcp_skus_v1` | GCP SKUs | `sku_description` |

Run `~/.claude/skills/rag-manager/rag_list.sh summary` for the current list.

## Configuration

**RAG API Endpoint**: `https://api.loreal.net/global/it4it/btdp-mcprag`

**Authentication**: Uses OAuth access token from `~/.gcp/access_token`

**Token Management**: Ensure your token is valid before running scripts. If you get authentication errors, refresh your token.

## Troubleshooting

### Authentication Errors
```bash
# Ensure token file exists
ls -la ~/.gcp/access_token

# Token should be refreshed regularly by your authentication process
```

### No Results Found
- Try broader search terms
- Check if the index exists with `rag_list.sh`
- Verify the field you're searching is actually indexed
- Try searching with different keywords

### Index Creation Fails
- Verify table is C1 or C2 (not C3)
- Check table exists and you have read permissions
- Ensure field names are correct (case-sensitive)
- Verify object_name follows naming rules (alphanumeric + underscores, starts with letter)
