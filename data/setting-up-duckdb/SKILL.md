---
name: setting-up-duckdb
description: Set up and configure DuckDB databases. Use when user needs to create databases, configure settings, or initialize DuckDB projects.
---

# DuckDB Setup

## Overview

This skill helps set up and configure DuckDB databases for analytics workloads. It handles database creation, extension management, configuration tuning, and project initialization with best practices.

## When to Use

Activate this skill when the user:
- Wants to create a new DuckDB database
- Needs to configure DuckDB settings (memory, threads, etc.)
- Asks about DuckDB extensions and how to install them
- Wants to initialize a project with DuckDB
- Needs help with DuckDB connection strings or paths
- Asks about DuckDB file formats (.duckdb, .db)

## Instructions

### 1. Determine Database Location

Ask or infer:
- **In-memory**: For temporary analysis, use `:memory:`
- **Persistent file**: For saved data, use `.duckdb` extension (recommended) or `.db`
- **Read-only**: Append `?access_mode=read_only` for shared access

### 2. Create the Database

**Python (recommended):**
```python
import duckdb

# Persistent database
con = duckdb.connect('my_database.duckdb')

# In-memory
con = duckdb.connect(':memory:')

# With configuration
con = duckdb.connect('my_database.duckdb', config={
    'threads': 4,
    'memory_limit': '4GB'
})
```

**CLI:**
```bash
duckdb my_database.duckdb
```

### 3. Configure Settings

Common configuration options:
```sql
-- Memory and performance
SET memory_limit = '4GB';
SET threads = 4;
SET temp_directory = '/tmp/duckdb';

-- File handling
SET enable_object_cache = true;
SET preserve_insertion_order = true;

-- Output formatting
SET max_expression_depth = 1000;
```

### 4. Install Extensions

DuckDB has powerful extensions. Install as needed:
```sql
-- Install and load extensions
INSTALL httpfs;   -- Read from S3, HTTP, etc.
LOAD httpfs;

INSTALL parquet;  -- Parquet support (built-in but can be explicit)
LOAD parquet;

INSTALL json;     -- JSON support
LOAD json;

INSTALL spatial;  -- Geospatial functions
LOAD spatial;

INSTALL excel;    -- Excel file support
LOAD excel;
```

### 5. Set Up Data Sources

**Local files:**
```sql
-- CSV
CREATE TABLE my_table AS SELECT * FROM read_csv('data.csv');

-- Parquet
CREATE TABLE my_table AS SELECT * FROM read_parquet('data.parquet');

-- JSON
CREATE TABLE my_table AS SELECT * FROM read_json('data.json');
```

**Remote sources (requires httpfs):**
```sql
SET s3_region = 'us-east-1';
SET s3_access_key_id = 'your_key';
SET s3_secret_access_key = 'your_secret';

CREATE TABLE my_table AS
SELECT * FROM read_parquet('s3://bucket/path/file.parquet');
```

### 6. Protect Sensitive Data with .gitignore

**CRITICAL:** DuckDB databases can contain sensitive data. Always ensure they are excluded from version control.

When setting up DuckDB in a git repository, **always** add these entries to `.gitignore`:

```gitignore
# DuckDB
*.duckdb
*.duckdb.wal
db/
```

**Why this matters:**
- `.duckdb` files contain all your data—potentially PII, credentials, or proprietary information
- `.duckdb.wal` (Write-Ahead Log) files contain recent transactions and can expose sensitive data
- The `db/` directory is a common convention for database storage

**Before creating any database**, check if a `.gitignore` exists and update it:

```python
from pathlib import Path

def ensure_gitignore_excludes_duckdb(repo_root: Path = None):
    """Ensure .gitignore excludes DuckDB files."""
    if repo_root is None:
        repo_root = Path.cwd()

    gitignore_path = repo_root / ".gitignore"

    duckdb_entries = [
        "# DuckDB",
        "*.duckdb",
        "*.duckdb.wal",
        "db/",
    ]

    existing_content = ""
    if gitignore_path.exists():
        existing_content = gitignore_path.read_text()

    # Check what's missing
    missing = [entry for entry in duckdb_entries
               if entry not in existing_content and not entry.startswith("#")]

    if missing:
        with open(gitignore_path, "a") as f:
            if existing_content and not existing_content.endswith("\n"):
                f.write("\n")
            f.write("\n".join(duckdb_entries) + "\n")
        print(f"Updated .gitignore with DuckDB exclusions")
```

### 7. Project Structure Recommendation

For projects using DuckDB:
```
project/
├── .gitignore        # Must exclude *.duckdb, *.duckdb.wal, db/
├── data/
│   ├── raw/          # Source data files
│   └── processed/    # Transformed data
├── db/
│   └── analytics.duckdb
├── sql/
│   ├── schema.sql    # Table definitions
│   ├── views.sql     # View definitions
│   └── queries/      # Saved queries
└── scripts/
    └── init_db.py    # Database initialization
```

## Configuration Reference

| Setting | Default | Description |
|---------|---------|-------------|
| `memory_limit` | 75% of RAM | Maximum memory usage |
| `threads` | # of cores | Parallel execution threads |
| `temp_directory` | system temp | Location for spill files |
| `default_order` | ASC | Default sort order |
| `enable_progress_bar` | false | Show query progress |
| `enable_object_cache` | false | Cache metadata |

## Common Extensions

| Extension | Purpose |
|-----------|---------|
| `httpfs` | HTTP/S3/GCS file access |
| `parquet` | Parquet file support |
| `json` | JSON file support |
| `spatial` | Geospatial functions |
| `excel` | Excel file support |
| `sqlite` | SQLite compatibility |
| `postgres` | PostgreSQL scanner |
| `mysql` | MySQL scanner |
| `fts` | Full-text search |
| `icu` | Unicode collation |

## Examples

### Example 1: Basic Analytics Database

**User:** "I want to set up a DuckDB database for analyzing CSV sales data"

**Response:**
```python
import duckdb

# Create persistent database
con = duckdb.connect('sales_analytics.duckdb')

# Configure for analytics workload
con.execute("""
    SET memory_limit = '4GB';
    SET threads = 4;
""")

# Import CSV data
con.execute("""
    CREATE TABLE sales AS
    SELECT * FROM read_csv('sales_data.csv',
        header=true,
        auto_detect=true
    );
""")

# Verify import
print(con.execute("SELECT COUNT(*) FROM sales").fetchone())
```

### Example 2: Multi-Source Data Warehouse

**User:** "Set up DuckDB to read from S3 and local parquet files"

**Response:**
```python
import duckdb

con = duckdb.connect('warehouse.duckdb')

# Install and configure S3 access
con.execute("""
    INSTALL httpfs;
    LOAD httpfs;
    SET s3_region = 'us-west-2';
""")

# For AWS credentials (if not using instance profile)
# con.execute("SET s3_access_key_id = 'your_key'")
# con.execute("SET s3_secret_access_key = 'your_secret'")

# Create tables from multiple sources
con.execute("""
    CREATE TABLE cloud_data AS
    SELECT * FROM read_parquet('s3://my-bucket/data/*.parquet');

    CREATE TABLE local_data AS
    SELECT * FROM read_parquet('local_files/*.parquet');
""")
```

### Example 3: Read-Only Shared Database

**User:** "Multiple processes need to read from the same DuckDB file"

**Response:**
```python
import duckdb

# Each process connects in read-only mode
con = duckdb.connect('shared.duckdb', read_only=True)

# Or via connection string
con = duckdb.connect('shared.duckdb?access_mode=read_only')

# Queries work normally
results = con.execute("SELECT * FROM my_table").fetchdf()
```

## Troubleshooting

**Database locked error:**
- Only one write connection allowed at a time
- Use read-only mode for concurrent reads
- Close connections when done

**Out of memory:**
- Increase `memory_limit`
- Use `SET temp_directory` for disk spilling
- Process data in chunks

**Extension not found:**
- Run `INSTALL extension_name` first
- Check DuckDB version compatibility
- Some extensions require specific builds

## Bundled Resources

- `scripts/init_duckdb.py` — Database initialization script
- `assets/schema_template.sql` — Template for schema definitions
- `references/extensions.md` — Detailed extension documentation
