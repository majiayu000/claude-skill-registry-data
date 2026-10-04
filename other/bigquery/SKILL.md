---
name: bigquery
description: Query and manage Google BigQuery datasets using the bq CLI and REST API. Run SQL queries, export results, manage tables and datasets in BigQuery.
version: 1.0.0
allowed-tools: Bash
metadata:
  credentials:
    - GOOGLE_APPLICATION_CREDENTIALS_JSON
    - BIGQUERY_PROJECT_ID
---

# BigQuery Skill

Query and manage Google BigQuery datasets using the `bq` CLI tool and REST API.

## Quick Start

```bash
# Run a query
bq query --use_legacy_sql=false --format=json \
  'SELECT count(*) as total FROM `project.dataset.table`'

# List datasets
bq ls --project_id="$BIGQUERY_PROJECT_ID"
```

## Prerequisites

| Variable | Description | Example |
|----------|-------------|---------|
| `GOOGLE_APPLICATION_CREDENTIALS_JSON` | Service account JSON key | `{"type":"service_account","project_id":"my-project",...}` |
| `BIGQUERY_PROJECT_ID` | GCP project ID (optional if in credentials) | `my-project-123` |

### First-Time Setup

The `bq` CLI authenticates via service account. Write the credentials to a file and set the path:

```bash
# Write credentials to file
echo "$GOOGLE_APPLICATION_CREDENTIALS_JSON" > /tmp/gcp-sa.json
export GOOGLE_APPLICATION_CREDENTIALS=/tmp/gcp-sa.json

# Verify access
bq ls --project_id="$BIGQUERY_PROJECT_ID"
```

### Alternative: REST API (No CLI Needed)

If `bq` is not installed, use BigQuery REST API directly with curl:

```bash
# Get access token from service account
ACCESS_TOKEN=$(python3 -c "
import json, time, base64, hashlib, urllib.request
sa = json.loads('''$GOOGLE_APPLICATION_CREDENTIALS_JSON''')
import jwt
token = jwt.encode({
  'iss': sa['client_email'],
  'scope': 'https://www.googleapis.com/auth/bigquery',
  'aud': 'https://oauth2.googleapis.com/token',
  'iat': int(time.time()),
  'exp': int(time.time()) + 3600
}, sa['private_key'], algorithm='RS256')
data = urllib.parse.urlencode({'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer', 'assertion': token}).encode()
resp = json.loads(urllib.request.urlopen('https://oauth2.googleapis.com/token', data).read())
print(resp['access_token'])
")

# Query via REST API
curl -X POST \
  "https://bigquery.googleapis.com/bigquery/v2/projects/$BIGQUERY_PROJECT_ID/queries" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "SELECT count(*) as total FROM `dataset.table`",
    "useLegacySql": false
  }'
```

## Core Recipes (bq CLI)

### Run a Query

```bash
echo "$GOOGLE_APPLICATION_CREDENTIALS_JSON" > /tmp/gcp-sa.json
export GOOGLE_APPLICATION_CREDENTIALS=/tmp/gcp-sa.json

bq query --use_legacy_sql=false --format=json \
  'SELECT * FROM `my_dataset.users` LIMIT 10'
```

### Run a Query with Parameters

```bash
bq query --use_legacy_sql=false --format=json \
  --parameter='name:STRING:John' \
  'SELECT * FROM `my_dataset.users` WHERE name = @name'
```

### List Datasets

```bash
bq ls --project_id="$BIGQUERY_PROJECT_ID" --format=json
```

### List Tables in a Dataset

```bash
bq ls --format=json "$BIGQUERY_PROJECT_ID:my_dataset"
```

### Show Table Schema

```bash
bq show --format=json "$BIGQUERY_PROJECT_ID:my_dataset.users"
```

### Get Table Preview (Head)

```bash
bq head --max_rows=10 "$BIGQUERY_PROJECT_ID:my_dataset.users"
```

### Count Rows

```bash
bq query --use_legacy_sql=false --format=json \
  'SELECT count(*) as total FROM `my_dataset.users`'
```

## Export & Import

### Export Query Results to CSV

```bash
bq query --use_legacy_sql=false --format=csv \
  'SELECT * FROM `my_dataset.users` LIMIT 1000' > users.csv
```

### Export Query Results to JSON

```bash
bq query --use_legacy_sql=false --format=json \
  'SELECT * FROM `my_dataset.users` LIMIT 1000' > users.json
```

### Export Large Table to GCS (then download)

```bash
# Export to Google Cloud Storage
bq extract --destination_format=CSV \
  "$BIGQUERY_PROJECT_ID:my_dataset.users" \
  "gs://my-bucket/exports/users-*.csv"

# Download from GCS
gsutil cp "gs://my-bucket/exports/users-*.csv" ./
```

### Load CSV into BigQuery

```bash
bq load --source_format=CSV --autodetect \
  "$BIGQUERY_PROJECT_ID:my_dataset.new_table" \
  ./data.csv
```

### Load JSON into BigQuery

```bash
bq load --source_format=NEWLINE_DELIMITED_JSON --autodetect \
  "$BIGQUERY_PROJECT_ID:my_dataset.new_table" \
  ./data.jsonl
```

## Schema & Table Management

### Create Dataset

```bash
bq mk --dataset "$BIGQUERY_PROJECT_ID:my_new_dataset"
```

### Create Table from Schema

```bash
bq mk --table "$BIGQUERY_PROJECT_ID:my_dataset.users" \
  name:STRING,email:STRING,age:INTEGER,created_at:TIMESTAMP
```

### Create Table from Query (CTAS)

```bash
bq query --use_legacy_sql=false \
  --destination_table="$BIGQUERY_PROJECT_ID:my_dataset.active_users" \
  'SELECT * FROM `my_dataset.users` WHERE last_login > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)'
```

### Copy Table

```bash
bq cp "$BIGQUERY_PROJECT_ID:dataset.source_table" \
  "$BIGQUERY_PROJECT_ID:dataset.destination_table"
```

### Delete Table

```bash
bq rm -f -t "$BIGQUERY_PROJECT_ID:my_dataset.old_table"
```

## Common Analytics Queries

### Daily Active Users

```bash
bq query --use_legacy_sql=false --format=json '
SELECT
  DATE(event_timestamp) as date,
  COUNT(DISTINCT user_id) as dau
FROM `my_dataset.events`
WHERE event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY date
ORDER BY date DESC
'
```

### Top Pages by Views

```bash
bq query --use_legacy_sql=false --format=json '
SELECT
  page_path,
  COUNT(*) as views,
  COUNT(DISTINCT user_id) as unique_users
FROM `my_dataset.pageviews`
WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
GROUP BY page_path
ORDER BY views DESC
LIMIT 20
'
```

### Revenue Summary

```bash
bq query --use_legacy_sql=false --format=json '
SELECT
  FORMAT_DATE("%Y-%m", date) as month,
  SUM(revenue) as total_revenue,
  COUNT(DISTINCT customer_id) as customers
FROM `my_dataset.transactions`
GROUP BY month
ORDER BY month DESC
LIMIT 12
'
```

## Output Formats

| Flag | Format | Best For |
|------|--------|----------|
| `--format=json` | JSON array | Programmatic use, piping to jq |
| `--format=csv` | CSV | Spreadsheets, further processing |
| `--format=pretty` | Aligned table (default) | Human reading |
| `--format=sparse` | Sparse output | Wide tables |

### Parse JSON Output with jq

```bash
bq query --use_legacy_sql=false --format=json \
  'SELECT name, email FROM `dataset.users` LIMIT 5' | jq '.[].name'
```

## Managed Service Setup

### Google Cloud Console

1. Go to [BigQuery Console](https://console.cloud.google.com/bigquery)
2. Create a service account: IAM → Service Accounts → Create
3. Grant role: `BigQuery Data Viewer` (read) or `BigQuery Data Editor` (read/write)
4. Create JSON key: Service Account → Keys → Add Key → JSON
5. Copy the JSON content to `GOOGLE_APPLICATION_CREDENTIALS_JSON` env var
6. Set `BIGQUERY_PROJECT_ID` to your GCP project ID

### Required IAM Roles

| Role | Permissions |
|------|------------|
| `roles/bigquery.dataViewer` | Read tables and run queries |
| `roles/bigquery.dataEditor` | Read + write tables |
| `roles/bigquery.jobUser` | Run query jobs (required for all queries) |
| `roles/bigquery.admin` | Full access |

**Minimum for read-only**: `bigquery.dataViewer` + `bigquery.jobUser`

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Not found: Dataset` | Dataset doesn't exist | Run `bq ls` to list available datasets |
| `Access Denied` | Insufficient permissions | Check IAM roles, need at least `dataViewer` + `jobUser` |
| `Invalid credentials` | Bad service account JSON | Verify `GOOGLE_APPLICATION_CREDENTIALS_JSON` is valid JSON |
| `Quota exceeded` | Query size/frequency limit | Add LIMIT, use partitioned tables, check billing |
| `Resources exceeded` | Query too large | Break into smaller queries, use `LIMIT` |
| `Table not found` | Wrong project/dataset/table | Use fully qualified name: `project.dataset.table` |
| `bq: command not found` | CLI not installed | Use REST API alternative above, or install Google Cloud SDK |

## Tips

- **Always use `--use_legacy_sql=false`** — standard SQL is more readable and powerful
- **Use `--format=json`** for programmatic processing, pipe to `jq` for filtering
- **Use `LIMIT`** when exploring — BigQuery bills by data scanned, not rows returned
- **Use partitioned tables** — queries on partitioned tables scan less data (cheaper)
- **Use `--dry_run`** to check query cost before running: `bq query --dry_run --use_legacy_sql=false 'SELECT ...'`
- **Backtick table names** in standard SQL: `` `project.dataset.table` ``
- **Cache results**: BigQuery caches query results for 24 hours — repeated queries are free
- **Cost awareness**: BigQuery charges $5/TB scanned. Always preview with `LIMIT` first
