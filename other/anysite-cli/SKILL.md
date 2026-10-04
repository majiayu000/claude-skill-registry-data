---
name: anysite-cli
description: Operate the anysite command-line tool for web data extraction, batch API processing, multi-source dataset pipelines with scheduling/transforms/exports, database operations, and LLM-powered data analysis. Use when users ask to collect data from LinkedIn, Instagram, Twitter, or any web source via CLI; create or run dataset pipelines; schedule automated collection; batch-process API calls; query collected data with SQL; load data into PostgreSQL or SQLite; analyze data with LLM (summarize, classify, enrich, match, deduplicate); or work with anysite commands. Triggers on anysite CLI usage, data collection, dataset creation, scraping, API batch calls, scheduling, database loading, or LLM analysis tasks.
---

# Anysite CLI

Command-line tool for web data extraction, dataset pipelines, and database operations.

## Agent Planning Workflow

**BEFORE planning any data collection task, follow this sequence:**

1. **Discover available endpoints**
   ```bash
   anysite describe --search "<keyword>"   # Search by domain (linkedin, company, user, etc.)
   ```

2. **Select endpoints needed for the task** — identify which endpoints will provide the required data

3. **Inspect each selected endpoint**
   ```bash
   anysite describe /api/linkedin/company  # View input params and output fields
   ```

4. **Only then plan** — now you know the exact parameters, field names, and data structure to build your config or API calls

This prevents errors from wrong endpoint paths, missing required parameters, or incorrect field names in dependencies.

## Best Practices

1. **Use dataset pipelines for multi-step tasks**
   - If a task requires sequential API calls, LLM enrichment, or chained data processing — create a `dataset.yaml` config instead of running multiple ad-hoc commands
   - Dataset pipelines handle dependencies, incremental collection, and error recovery automatically
   - Even for "simple" tasks that grow in scope, a dataset config is easier to maintain
   - Benefits: run history, incremental sync, scheduling, notifications, DB loading

2. **Save data in Parquet format by default** — unless user requests another format or CSV/JSON fits better

3. **Prefer datasets over ad-hoc scripts** — one dataset.yaml replaces dozens of shell commands

## Quick Start Checklist

Before any data collection task:

```bash
# 1. Check CLI is available and see latest changes
anysite --version
anysite changelog --last 1 --json            # Check what's new in this version
# If not found: source .venv/bin/activate or pip install anysite-cli

# 2. Update schema cache (required for endpoint discovery)
anysite schema update

# 3. Verify API key
anysite config get api_key
# If not set: anysite config set api_key sk-xxxxx
```

After upgrading, run `anysite changelog --since <old_version> --json` to discover new features.

## Endpoint Discovery

**ALWAYS discover endpoints before writing API calls or dataset configs:**

```bash
anysite describe                          # List all endpoints
anysite describe --search "company"       # Search with dependency context
anysite describe /api/linkedin/company    # Full details: params, output, connections

```

Search returns matched endpoints plus upstream providers (who can supply input IDs) and downstream consumers (who can use output IDs). Use this to plan endpoint chains for dataset pipelines.

Input params show type, description, examples, and defaults. Array params show item structure:
```
Input parameters:
  * urn                            string      User URN, only fsd_profile urn type is allowed
                                               example: "urn:li:fsd_profile:ACoAABXy1234"
    count                          integer     Number of posts to return
                                               default: 20
    companies                      array[object{type,value}]  Company URNs
                                               example: [{"type": "company", "value": "14064608"}]
```

## Prerequisites

```bash
pip install "anysite-cli[data]"        # DuckDB + PyArrow for dataset commands
pip install "anysite-cli[llm]"         # LLM analysis (openai/anthropic)
pip install "anysite-cli[postgres]"    # PostgreSQL adapter
pip install "anysite-cli[clickhouse]"  # ClickHouse adapter

anysite config set api_key sk-xxxxx   # Configure API key
anysite schema update                  # Update schema cache
anysite llm setup                      # Interactive setup (human)
anysite llm setup --provider openai --api-key sk-xxx --no-test    # Non-interactive (agent)
anysite llm setup --provider anthropic --api-key-env ANTHROPIC_API_KEY --no-test
anysite db add pg --type postgres --host localhost --database mydb --user app --password secret
# Or via env var: anysite db add pg ... --password-env PGPASS
anysite db add ch --type clickhouse --host ch.example.com --port 8443 --database analytics --user app --password secret --ssl
```

## Authentication

```bash
anysite auth login                        # Interactive browser-based OAuth2 (human)
anysite auth login --force --no-browser   # Re-authenticate without confirmation (agent)
anysite auth status                       # Check current auth status
anysite auth status --json                # Machine-readable auth status
anysite auth logout                       # Interactive logout (human)
anysite auth logout --force               # Logout without confirmation (agent)
```

## Single API Call

```bash
anysite api /api/linkedin/user user=satyanadella
anysite api /api/linkedin/company company=anthropic --format table
anysite api /api/linkedin/search/users keywords="CTO" count=50 --format csv --output ctos.csv
anysite api /api/linkedin/user user=satyanadella --fields "name,headline,urn.value" -q | jq
```

### URN/Name Parameter Formats

Parameters like `location`, `current_companies`, `industry` accept two formats:

```bash
# Single name (text search) — resolves to URNs automatically
location="London"
current_companies="Microsoft"

# Multiple URNs (direct) — use JSON array in single quotes
'location=["urn:li:geo:101165590", "urn:li:geo:101282230"]'
'current_companies=["urn:li:company:1035", "urn:li:company:1441"]'
```

**Note:** List of names `["Microsoft", "Google"]` is NOT supported — use either one name OR multiple URNs.

## Batch Processing

```bash
anysite api /api/linkedin/user --from-file users.txt --input-key user \
  --parallel 5 --rate-limit "10/s" --on-error skip --progress --stats
```

## Dataset Pipeline (Multi-Source Collection)

For complex data collection with dependencies, LLM enrichment, scheduling — use dataset pipelines.

### Initialize

```bash
anysite dataset init my-dataset
# Creates my-dataset/dataset.yaml with template config
```

### Six Source Types

1. **Independent** — single API call with static `input`
2. **from_file** — batch calls iterating over input file values
3. **Dependent** — batch calls using values extracted from a parent source
4. **Union (type: union)** — combine records from multiple parent sources into one
5. **LLM (type: llm)** — process parent data through LLM without API calls
6. **SQL (type: sql)** — query a database connection or dataset Parquet files via DuckDB

### Comprehensive Dataset YAML Reference

```yaml
name: my-dataset                    # Dataset name (required)
description: Optional description   # Human-readable description

sources:
  # === TYPE 1: Independent source (single API call) ===
  - id: search_results              # Unique identifier (required)
    endpoint: /api/linkedin/search/users  # API endpoint (required for type: api)
    input:                          # Static API parameters
      keywords: "software engineer"
      count: 50
    parallel: 1                     # Concurrent requests: 1-10 (default: 1)
    rate_limit: "10/s"              # Rate limit: "N/s", "N/m", "N/h"
    on_error: stop                  # Error handling: stop | skip (default: stop)

  - id: search_extra                # Another search (can be combined with union)
    endpoint: /api/linkedin/search/users
    input: { keywords: "data engineer", count: 50 }

  # === TYPE 2: from_file source (batch from file) ===
  - id: companies
    endpoint: /api/linkedin/company
    from_file: companies.txt        # Input file: .txt (line per value), .csv, .jsonl
    file_field: company_slug        # CSV column name (for CSV files only)
    input_key: company              # API parameter to fill with each value
    parallel: 3

  # === TYPE 3: Dependent source (values from parent) ===
  - id: employees
    endpoint: /api/linkedin/company/employees
    dependency:
      from_source: companies        # Parent source ID (required)
      field: urn.value              # Dot-notation path to extract from parent records
      match_by: name                # Alternative: fuzzy match instead of exact field
      dedupe: true                  # Remove duplicate values (default: false)
    input_key: companies            # API parameter for extracted values
    input_template:                 # Transform values before API call
      companies:
        - type: company
          value: "{value}"          # {value} = extracted value placeholder
      count: 5
    refresh: auto                   # Incremental behavior: auto (default) | always | never
                                    # never = skip if data exists

  # === Shorthand for dependent sources ===
  # ${source.field} auto-expands to dependency + input_key:
  - id: profiles
    endpoint: /api/linkedin/user
    input:
      user: ${companies.urn.value}    # Equivalent to dependency + input_key above

  # === TYPE 4: Union source (combine multiple sources) ===
  - id: all_search_results
    type: union                     # Source type: api (default) | union | llm | sql
    sources: [search_results, search_extra]  # Parent source IDs to combine (required)
    dedupe_by: urn.value            # Optional: field path for deduplication (dot-notation)
    # NOTE: type: union cannot have endpoint, dependency, from_file, input_key, input
    # NOTE: all sources in the list must have the same endpoint (same data structure)
    # Records are annotated with _union_source = parent source ID

  # === TYPE 5: LLM source (process parent data without API) ===
  - id: employees_analyzed
    type: llm                       # Source type: api (default) | union | llm | sql
    dependency:
      from_source: employees
      field: name                   # Required by schema (not used for LLM sources)
    llm:                            # LLM enrichment steps (required for type: llm)
      - type: classify              # Step types: classify | enrich | summarize | generate
        categories: "developer,recruiter,executive"  # Comma-separated (omit for auto-detect)
        output_column: role_type    # Output column name (default: category)
        fields: [headline]          # Record fields to include in LLM prompt
      - type: enrich
        add:                        # Field specs (required for enrich)
          - "sentiment:positive/negative/neutral"   # Enum: value1/value2/value3
          - "language:string"                       # Types: string | number | integer | boolean
          - "quality_score:1-10"                    # Range: min-max
        fields: [headline, summary]
        temperature: 0.0            # LLM temperature: 0.0-1.0 (default: 0.0)
        provider: openai            # Provider override: openai | anthropic
        model: gpt-4o-mini          # Model override
      - type: summarize
        max_length: 50              # Max words (default: 100)
        output_column: bio
      - type: generate
        prompt: "Write pitch for {name}"  # Template with {field} placeholders (required)
        output_column: pitch
        temperature: 0.7            # Higher for creative text
    export:                         # Export destinations (runs after Parquet write)
      - type: file
        path: ./output/{{source}}-{{date}}.csv  # Templates: {{date}}, {{source}}, {{dataset}}
        format: csv                 # Format: json | jsonl | csv
    # NOTE: type: llm cannot have endpoint, from_file, input_key, input

  # === TYPE 6: SQL source (query a database) ===
  # Mode A: Named connection (query external database)
  - id: billing_users
    type: sql
    connection: billing            # Named connection from 'anysite db add'
    query: "SELECT name, email FROM subscriptions WHERE status = 'inactive'"
    # query_file: queries/inactive.sql   # Alternative: read SQL from file
    filter: ".email != null"       # All base fields work: filter, llm, transform, export, db_load

  # Mode B: Dataset views (no connection — query Parquet via DuckDB)
  # Each collected source becomes a view by its id (hyphens → underscores)
  - id: enriched_profiles
    type: sql
    query: |
      SELECT u.*, c.description as company_desc
      FROM user_profiles u
      LEFT JOIN company_profiles c ON u._input_value = c._input_value
    # Use for cross-source JOINs within the pipeline — no external DB needed
    # NOTE: type: sql cannot have endpoint, from_file, input_key, input, parallel, rate_limit, on_error

  # === OPTIONAL BLOCKS (any source type) ===
  # THREE-LEVEL FILTERING:
  # Level 1: source.filter — before LLM + Parquet (saves tokens, drops records entirely)
  # Level 2: transform.filter — before exports only (Parquet keeps all records)
  # Level 3: db_load.filter — before DB loading (Parquet keeps all records)
  # All use same syntax: .field op value, booleans (true/false), and/or
  - id: profiles
    endpoint: /api/linkedin/user
    dependency: { from_source: employees, field: internal_id.value }
    input_key: user
    filter: '.follower_count > 100'  # Level 1: early filter (before LLM + Parquet)
    transform:                      # Level 2: export filter (Parquet keeps all)
      filter: '.location != ""'     # Safe expression
      fields:                       # Field selection with dot-notation aliases
        - name
        - urn.value AS urn_id
        - headline
      add_columns:                  # Static columns to inject
        batch: "q1-2026"
    export:
      - type: file
        path: ./output/profiles.csv
        format: csv
      - type: webhook
        url: https://example.com/hook
        headers: { X-Token: abc }
    db_load:                        # Database loading config
      filter: '.active == true'     # Level 3: DB filter (only active to DB)
      table: people                 # Custom table name (default: source ID)
      key: urn.value                # Unique key for diff-based incremental sync
      sync: full                    # Sync mode: full (default) | append (no DELETE)
      fields:                       # Fields to load (default: all except _input_value)
        - name
        - urn.value AS urn_id
        - headline
      exclude: [_input_value, raw_html]  # Fields to skip

storage:
  format: parquet                   # Storage format (only parquet supported)
  path: ./data/                     # Storage directory (relative to dataset.yaml)

schedule:
  cron: "0 9 * * *"                 # Cron expression for scheduling

notifications:
  on_complete:
    - url: "https://hooks.slack.com/xxx"
      headers: { Authorization: "Bearer token" }
  on_failure:
    - url: "https://alerts.example.com/fail"
```

### type: union Source Details

The `type: union` source combines records from multiple parent sources:

- **Requires**: non-empty `sources` list (parent source IDs)
- **Optional**: `dedupe_by` field path for removing duplicates (supports dot-notation)
- **Cannot have**: `endpoint`, `dependency`, `from_file`, `input_key`, `input`
- **Validation**: all parent sources must have the same endpoint (same data structure)
- **Use case**: merge multiple search results before a single dependent source processes them

```yaml
sources:
  - id: search_cto
    endpoint: /api/linkedin/search/users
    input: { keywords: "CTO fintech", count: 50 }

  - id: search_vp
    endpoint: /api/linkedin/search/users
    input: { keywords: "VP Engineering", count: 50 }

  # Union combines all search results
  - id: all_candidates
    type: union
    sources: [search_cto, search_vp]
    dedupe_by: urn.value              # Remove duplicates by URN

  # Single dependent source processes all candidates
  - id: profiles
    endpoint: /api/linkedin/user
    dependency:
      from_source: all_candidates
      field: urn.value
    input_key: user
```

Records from union sources are annotated with `_union_source` (the parent source ID they came from).

### type: llm Source Details

The `type: llm` source processes existing parent data without making API calls:

- **Requires**: `dependency` (parent source) and non-empty `llm` list
- **Cannot have**: `endpoint`, `from_file`, `input_key`, `input`
- **Use case**: Run LLM enrichment on already-collected data, re-analyze with different prompts

```bash
# Collect only the LLM source (reads parent Parquet, applies LLM steps)
anysite dataset collect dataset.yaml --source employees_analyzed
```

### Validate & Collect Commands

```bash
anysite dataset validate dataset.yaml                    # Validate config (catches errors early)
anysite dataset collect dataset.yaml --dry-run          # Preview plan
anysite dataset collect dataset.yaml                     # Run collection
anysite dataset collect dataset.yaml --load-db pg       # Collect + auto-load to DB
anysite dataset collect dataset.yaml --incremental      # Skip already-collected inputs
anysite dataset collect dataset.yaml --source employees # Single source + dependencies
anysite dataset collect dataset.yaml --no-llm           # Skip LLM enrichment steps
anysite dataset collect dataset.yaml --limit 100        # Pilot run: max 100 inputs per source
```

### Incremental Collection (Resume Where You Left Off)

For `from_file` and `dependency` sources, anysite tracks collected input values in `metadata.json`. This enables resuming collection without re-fetching existing data.

**Workflow:**
```bash
# First run — collects all inputs
anysite dataset collect dataset.yaml

# Later: add new items to input file, run with --incremental
anysite dataset collect dataset.yaml --incremental
# → Only new items are collected, existing ones skipped

# Force full re-collection
anysite dataset reset-cursor dataset.yaml
anysite dataset collect dataset.yaml
```

**Per-source `refresh` option:**
```yaml
sources:
  - id: profiles
    refresh: auto      # (default) respects --incremental

  - id: posts
    refresh: always    # always re-collects, ignores --incremental
                       # use for time-sensitive data (feeds, activity)

  - id: companies
    refresh: never     # skip if data exists (any snapshot)
```

**Reset cursor:**
```bash
anysite dataset reset-cursor dataset.yaml                  # all sources
anysite dataset reset-cursor dataset.yaml --source posts   # specific source
```

### Query with DuckDB

```bash
anysite dataset query dataset.yaml --sql "SELECT * FROM companies LIMIT 10"
anysite dataset query dataset.yaml --source profiles --fields "name, urn.value AS id"
anysite dataset query dataset.yaml --source profiles --exclude "_input_value,_parent_source"
anysite dataset query dataset.yaml --interactive        # SQL shell
anysite dataset stats dataset.yaml --source companies
anysite dataset profile dataset.yaml
```

### Load into Database

```bash
anysite dataset load-db dataset.yaml -c pg --drop-existing  # Full load
anysite dataset load-db dataset.yaml -c pg                   # Incremental sync (when db_load.key set)
anysite dataset load-db dataset.yaml -c pg --snapshot 2026-01-15
```

### Compare Snapshots

```bash
anysite dataset diff dataset.yaml --source profiles --key urn.value
anysite dataset diff dataset.yaml --source profiles --key urn.value --from 2026-01-30 --to 2026-02-01
```

### Scheduling & History

```bash
anysite dataset schedule dataset.yaml --incremental --load-db pg  # Generate cron entry
anysite dataset history my-dataset
anysite dataset logs my-dataset --run 42
anysite dataset reset-cursor dataset.yaml                         # Clear incremental state
```

## Database Operations

```bash
# Connection management
anysite db add pg --type postgres --host localhost --database mydb --user app --password secret
anysite db add pg --type postgres --host localhost --database mydb --user app --password-env PGPASS
anysite db add ch --type clickhouse --host ch.example.com --port 8443 --database analytics --user app --password secret --ssl
anysite db add local --type sqlite --path ./data.db
anysite db add replica --type postgres --host replica.example.com --read-only
anysite db list
anysite db test pg

# Data operations
cat data.jsonl | anysite db insert pg --table users --stdin --auto-create
anysite db query pg --sql "SELECT * FROM users" --format table
anysite db query pg --sql "SELECT * FROM users" --format parquet --output users.parquet
anysite db query pg --sql "SELECT * FROM users" --format csv --output "reports/{{date}}/users.csv"

# Pipe API output to database
anysite api /api/linkedin/user user=satyanadella -q --format jsonl \
  | anysite db insert pg --table profiles --stdin --auto-create

# Database discovery (schema introspection, sample data, LLM descriptions)
anysite db discover mydb                              # Discover schema
anysite db discover mydb --with-llm                   # Add LLM table/column descriptions
anysite db discover mydb --tables users,posts         # Filter tables
anysite db discover mydb --exclude-tables _migrations

# View saved catalogs
anysite db catalog                       # List all catalogs
anysite db catalog mydb                  # Show full catalog
anysite db catalog mydb --table users    # Show specific table
anysite db catalog mydb --json           # JSON output for agents
```

Credentials: `--password` saves directly in `~/.anysite/connections.yaml`, `--password-env` references an env var. Direct value takes priority. LLM API keys follow the same pattern via `anysite llm setup`.

Supported databases: SQLite, PostgreSQL, ClickHouse. ClickHouse uses `clickhouse-connect` driver (HTTP protocol, port 8123 default, 8443 for HTTPS/SSL).

## LLM Analysis Commands

Analyze collected dataset records using LLM. Requires `anysite llm setup` first.

Non-interactive setup (for agents):
```bash
anysite llm setup --provider openai --api-key <key> --no-test
anysite llm setup --provider anthropic --api-key-env ANTHROPIC_API_KEY --model claude-sonnet-4-5-20250514 --no-test
```

```bash
anysite llm summarize dataset.yaml --source profiles --fields "name,headline" --format table
anysite llm classify dataset.yaml --source posts --categories "positive,negative,neutral"
anysite llm enrich dataset.yaml --source profiles \
  --add "seniority:junior/mid/senior" --add "is_technical:boolean"
anysite llm generate dataset.yaml --source profiles \
  --prompt "Write intro for {name} who works as {headline}" --temperature 0.7
anysite llm match dataset.yaml --source-a profiles --source-b companies --top-k 3
anysite llm deduplicate dataset.yaml --source profiles --key name --threshold 0.8
anysite llm cache-stats
anysite llm cache-clear
```


Use `anysite describe --search <keyword>` for more endpoints.

## Key Patterns

- **Output formats**: `--format json|jsonl|csv|table|parquet` (parquet requires `--output`)
- **Array params**: `keywords=a,b,c` auto-wraps as `["a","b","c"]`
- **Field selection**: `--fields "name,headline,urn.value"` (dot-notation for nested)
- **Error handling**: `--on-error stop|skip|retry`
- **Config priority**: CLI args > ENV vars > `~/.anysite/config.yaml` > defaults

## References

For detailed option tables and advanced configuration:
- [api-reference.md](references/api-reference.md) — all CLI options
- [llm-reference.md](references/llm-reference.md) — LLM provider config, cache, prompts
- [dataset-guide.md](references/dataset-guide.md) — full YAML schema, advanced features
