---
name: trino-cli
description: Trino CLI for TD interactive queries. Covers connection to regional endpoints, batch mode (--execute, --file), output formats (CSV, JSON, TSV), and session properties.
---

# Trino CLI for Treasure Data

## Installation

```bash
curl -o trino https://repo1.maven.org/maven2/io/trino/trino-cli/477/trino-cli-477-executable.jar
chmod +x trino
sudo mv trino /usr/local/bin/
```

Requires Java 11+.

## Connection

```bash
export TD_API_KEY="your_api_key"

trino \
  --server https://api-presto.treasuredata.com \
  --catalog td \
  --user $TD_API_KEY \
  --schema your_database
```

**Regional Endpoints:**
- US: `https://api-presto.treasuredata.com`
- Tokyo: `https://api-presto.treasuredata.co.jp`
- EU: `https://api-presto.eu01.treasuredata.com`

## Batch Mode

```bash
# Single query
trino --server ... --execute "SELECT COUNT(*) FROM events"

# From file
trino --server ... --file queries.sql

# From stdin
echo "SELECT * FROM events LIMIT 10" | trino --server ...
```

## Output Formats

```bash
# CSV for spreadsheets
--output-format CSV_HEADER > results.csv

# JSON for programmatic use
--output-format JSON > results.json

# TSV for data processing
--output-format TSV_HEADER > results.tsv

# Markdown for docs
--output-format MARKDOWN
```

Available: `CSV`, `CSV_HEADER`, `CSV_UNQUOTED`, `TSV`, `TSV_HEADER`, `JSON`, `MARKDOWN`, `NULL`

## Interactive Commands

| Command | Description |
|---------|-------------|
| `USE schema` | Switch database |
| `SHOW SCHEMAS` | List databases |
| `SHOW TABLES` | List tables |
| `DESCRIBE table` | Show structure |
| `EXPLAIN query` | Show plan |

## Configuration File

```bash
# ~/.trino_config
server=https://api-presto.treasuredata.com
catalog=td
user=$TD_API_KEY
schema=sample_datasets
```

## Session Properties

```bash
trino \
  --session query_max_run_time=1h \
  --session query_priority=2 \
  --execute "SELECT ..."
```

## Common Options

| Option | Description |
|--------|-------------|
| `--execute "SQL"` | Run query and exit |
| `--file queries.sql` | Run from file |
| `--output-format` | Output format |
| `--client-request-timeout 30m` | Query timeout |
| `--ignore-errors` | Continue on error |
| `--no-progress` | Disable progress |

## Resources

- https://trino.io/docs/current/client/cli.html
