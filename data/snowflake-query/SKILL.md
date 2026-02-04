---
name: snowflake-query
description: "Execute SQL queries against Snowflake data warehouse using Python connector. Supports password, key-pair, and SSO/OAuth authentication. Use for ad-hoc queries, data extraction, and schema exploration. Output in JSON, table, or CSV format."
license: MIT
---

# Snowflake Query Execution

## Overview

Execute SQL queries against Snowflake with support for:
- Multiple authentication methods (password, key-pair, SSO/OAuth)
- Flexible output formats (JSON, table, CSV)
- Connection parameter overrides
- Query timeout and row limits

## Quick Start

### 1. Set Environment Variables

```bash
# Required
export SNOWFLAKE_ACCOUNT="your-account.region"
export SNOWFLAKE_USER="your_username"

# Password authentication
export SNOWFLAKE_PASSWORD="your_password"

# Optional defaults
export SNOWFLAKE_DATABASE="MY_DB"
export SNOWFLAKE_SCHEMA="PUBLIC"
export SNOWFLAKE_WAREHOUSE="COMPUTE_WH"
export SNOWFLAKE_ROLE="ANALYST"
```

### 2. Run Query

```bash
# Inline query (JSON output)
uvx --with snowflake-connector-python python scripts/query.py \
  --query "SELECT * FROM my_table"

# From file with table output
uvx --with snowflake-connector-python --with tabulate python scripts/query.py \
  --file query.sql --format table

# Export to CSV
uvx --with snowflake-connector-python python scripts/query.py \
  --query "SELECT * FROM my_table" --format csv --output result.csv
```

## Authentication Methods

### Password Authentication

Set `SNOWFLAKE_PASSWORD` environment variable.

```bash
export SNOWFLAKE_PASSWORD="your_password"
```

### Key-Pair Authentication

```bash
# Option 1: File path
export SNOWFLAKE_PRIVATE_KEY_PATH="/path/to/rsa_key.p8"

# Option 2: Base64-encoded key content
export SNOWFLAKE_PRIVATE_KEY_RAW="<base64-encoded-key>"

# Optional: If key is encrypted
export SNOWFLAKE_PRIVATE_KEY_PASSPHRASE="passphrase"
```

### SSO/OAuth Authentication

```bash
# Browser-based SSO
export SNOWFLAKE_AUTHENTICATOR="externalbrowser"

# OAuth token
export SNOWFLAKE_AUTHENTICATOR="oauth"
export SNOWFLAKE_OAUTH_TOKEN="your_oauth_token"
```

## CLI Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--query` | `-q` | SQL query string | - |
| `--file` | `-f` | SQL file path | - |
| `--format` | - | Output format (json/table/csv) | json |
| `--output` | `-o` | Output file path | stdout |
| `--limit` | `-l` | Row limit | 100 |
| `--no-limit` | - | Disable row limit | false |
| `--database` | - | Override database | env |
| `--schema` | - | Override schema | env |
| `--warehouse` | - | Override warehouse | env |
| `--role` | - | Override role | env |
| `--timeout` | - | Query timeout (seconds) | 300 |
| `--dry-run` | - | Test connection only | false |
| `--verbose` | `-v` | Verbose output | false |

## Output Formats

### JSON (default)

```json
{
  "status": "success",
  "query_id": "01b12345-...",
  "execution_time_ms": 234,
  "row_count": 3,
  "columns": ["id", "name", "created_at"],
  "rows": [
    {"id": 1, "name": "Alice", "created_at": "2024-01-01"},
    {"id": 2, "name": "Bob", "created_at": "2024-01-02"}
  ]
}
```

### Table

```
+----+-------+------------+
| id | name  | created_at |
+----+-------+------------+
|  1 | Alice | 2024-01-01 |
|  2 | Bob   | 2024-01-02 |
+----+-------+------------+
```

### CSV

```csv
id,name,created_at
1,Alice,2024-01-01
2,Bob,2024-01-02
```

## Examples

### Basic Query

```bash
uvx --with snowflake-connector-python python scripts/query.py \
  -q "SELECT CURRENT_TIMESTAMP()"
```

### Schema Exploration

```bash
uvx --with snowflake-connector-python --with tabulate python scripts/query.py \
  -q "SHOW TABLES IN SCHEMA my_db.public" --format table
```

### Data Export

```bash
uvx --with snowflake-connector-python python scripts/query.py \
  -f export.sql --format csv -o data.csv --no-limit
```

### Connection Test

```bash
uvx --with snowflake-connector-python python scripts/query.py --dry-run
```

### Override Connection Parameters

```bash
uvx --with snowflake-connector-python python scripts/query.py \
  -q "SELECT * FROM table" \
  --database PROD_DB \
  --schema ANALYTICS \
  --warehouse LARGE_WH
```

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `SNOWFLAKE_ACCOUNT` | Yes | Account identifier (e.g., abc12345.us-east-1) |
| `SNOWFLAKE_USER` | Yes | Username |
| `SNOWFLAKE_PASSWORD` | Auth* | Password (for password auth) |
| `SNOWFLAKE_PRIVATE_KEY_PATH` | Auth* | Private key file path (for key-pair auth) |
| `SNOWFLAKE_PRIVATE_KEY_RAW` | Auth* | Base64-encoded private key |
| `SNOWFLAKE_PRIVATE_KEY_PASSPHRASE` | No | Private key passphrase |
| `SNOWFLAKE_AUTHENTICATOR` | Auth* | externalbrowser or oauth |
| `SNOWFLAKE_OAUTH_TOKEN` | No | OAuth token (when authenticator=oauth) |
| `SNOWFLAKE_DATABASE` | No | Default database |
| `SNOWFLAKE_SCHEMA` | No | Default schema |
| `SNOWFLAKE_WAREHOUSE` | No | Default warehouse |
| `SNOWFLAKE_ROLE` | No | Default role |

*Auth: At least one authentication method is required.

## Dependencies

Run with uvx to automatically handle dependencies:

```bash
# Basic (JSON/CSV output)
uvx --with snowflake-connector-python python scripts/query.py ...

# With table output
uvx --with snowflake-connector-python --with tabulate python scripts/query.py ...
```

## Error Handling

Errors are output in JSON format:

```json
{
  "status": "error",
  "error_code": "AUTH_FAILED",
  "error_message": "Authentication failed: incorrect username or password"
}
```

### Exit Codes

| Code | Description |
|------|-------------|
| 0 | Success |
| 1 | Configuration error (missing env vars, invalid options) |
| 2 | Authentication error |
| 3 | Connection error |
| 4 | Query error (SQL syntax, permissions) |
| 5 | Output error (file write failed) |
