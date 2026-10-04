---
name: sqlite
description: Create and query SQLite databases for local data storage, CSV processing, and data staging. No external credentials needed — works with files in the Space.
version: 1.0.0
allowed-tools: Bash, Read
metadata:
  credentials: []
---

# SQLite Skill

Use SQLite for local data storage, CSV processing, and data staging. No credentials needed — databases are just files.

## Quick Start

```bash
# Create a database and query it
sqlite3 data.db "CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, title TEXT, body TEXT, created_at TEXT DEFAULT (datetime('now')))"
sqlite3 data.db "INSERT INTO notes (title, body) VALUES ('First Note', 'Hello world')"
sqlite3 data.db "SELECT * FROM notes"
```

## Prerequisites

`sqlite3` is pre-installed. No credentials or setup needed.

```bash
sqlite3 --version
```

## Core Recipes

### Create a Database

```bash
sqlite3 data.db "CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT UNIQUE,
  created_at TEXT DEFAULT (datetime('now'))
)"
```

### Query Data

```bash
sqlite3 data.db "SELECT * FROM users"
```

### Insert Data

```bash
sqlite3 data.db "INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')"
```

### List Tables

```bash
sqlite3 data.db ".tables"
```

### Show Schema

```bash
sqlite3 data.db ".schema"
```

### Count Rows

```bash
sqlite3 data.db "SELECT count(*) FROM users"
```

## CSV Import & Export

### Import CSV to New Table

```bash
sqlite3 data.db <<'EOF'
.mode csv
.import data.csv users
EOF
```

### Export Table to CSV

```bash
sqlite3 data.db <<'EOF'
.headers on
.mode csv
.output users.csv
SELECT * FROM users;
.output stdout
EOF
```

### Export Query Results to CSV

```bash
sqlite3 -header -csv data.db "SELECT id, name, email FROM users WHERE created_at > '2024-01-01'" > recent_users.csv
```

## JSON Operations

### Export as JSON

```bash
sqlite3 data.db -json "SELECT * FROM users LIMIT 100" > users.json
```

### Query JSON columns (SQLite 3.38+)

```bash
sqlite3 data.db "SELECT json_extract(metadata, '$.name') AS name FROM records"
```

## Formatting Options

### Column Mode (pretty tables)

```bash
sqlite3 -column -header data.db "SELECT * FROM users LIMIT 10"
```

### JSON Output

```bash
sqlite3 -json data.db "SELECT * FROM users"
```

## Data Staging Patterns

Use SQLite as a local staging database to process data from other sources.

### Stage API Results

```bash
sqlite3 staging.db "CREATE TABLE IF NOT EXISTS api_results (id TEXT, data TEXT, fetched_at TEXT DEFAULT (datetime('now')))"

RESULT=$(curl -s https://api.example.com/data)
sqlite3 staging.db "INSERT INTO api_results (id, data) VALUES ('batch-1', '$(echo $RESULT | sed "s/'/''/g")')"
```

### Process Large CSVs

```bash
sqlite3 :memory: <<'EOF'
.mode csv
.import large_file.csv data
.headers on
.mode csv
.output filtered.csv
SELECT * FROM data WHERE status = 'active' AND amount > 100;
.output stdout
EOF
```

### In-Memory Processing

```bash
sqlite3 :memory: "SELECT 1+1 AS result"
```

## Advanced Recipes

### Attach Multiple Databases

```bash
sqlite3 main.db <<'EOF'
ATTACH DATABASE 'archive.db' AS archive;
SELECT m.*, a.notes FROM main.users m LEFT JOIN archive.user_notes a ON m.id = a.user_id;
EOF
```

### Full-Text Search

```bash
sqlite3 data.db <<'EOF'
CREATE VIRTUAL TABLE IF NOT EXISTS docs_fts USING fts5(title, body);
INSERT INTO docs_fts (title, body) VALUES ('README', 'This is the readme content');
SELECT * FROM docs_fts WHERE docs_fts MATCH 'readme';
EOF
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `no such table` | Table doesn't exist | Run `.tables` to see available tables |
| `database is locked` | Another process has a lock | Wait or check for other sqlite3 processes |
| `UNIQUE constraint failed` | Duplicate value | Use `INSERT OR IGNORE` or `INSERT OR REPLACE` |
| `no such column` | Wrong column name | Run `.schema tablename` to check columns |
| `attempt to write a readonly database` | File permissions | Check file ownership and permissions |

## Tips

- **Use `:memory:`** for throwaway data processing — no cleanup needed
- **Use `sqlite3 -json`** for easy integration with other tools
- **Import CSVs first** — SQLite is great for filtering/joining CSV data
- **Use as staging** — pull data from APIs/databases into SQLite, process locally, export results
- **WAL mode** — use `PRAGMA journal_mode=WAL` for better concurrent read performance
- **File location** — databases are just files in the Space, easily shareable and portable
- **Backup** — just copy the `.db` file
