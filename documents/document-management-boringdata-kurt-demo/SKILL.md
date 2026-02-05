---
name: document-management
description: Manage Kurt documents - list, query, retrieve content, delete, find duplicates. Use CLI commands, Python API, or direct SQL queries.
---

# Document Management

## Overview

This skill provides comprehensive document management for Kurt's SQLite database. You can list documents with filters, retrieve full content, delete documents, find duplicates, and run custom SQL queries for analysis.

Kurt stores document metadata (title, URL, author, categories, dates, content fingerprints) in SQLite, while actual content is stored as markdown files in the `sources/` directory.

## Quick Start

```bash
# List all documents
kurt content list

# Get document details
kurt content get-metadata 44ea066e  # Partial UUID works

# View statistics
kurt document stats
```

```python
# Python API
from kurt.document import list_documents, get_document

# List with filters
docs = list_documents(status="FETCHED", limit=10)

# Get document
doc = get_document("44ea066e")
```

## Three Ways to Work with Documents

1. **CLI** - Interactive commands for daily use
2. **Python API** - Programmatic access for scripts and agents
3. **SQL** - Direct queries for analysis and bulk operations

## ⚠️ Critical: Content Path Handling

**The #1 mistake**: `content_path` in the database is **relative** to the source directory!

```python
# ❌ WRONG - content_path is relative, file won't be found
content = Path(doc['content_path']).read_text()

# ✅ CORRECT - prepend source directory
from kurt.config import load_config
from pathlib import Path

config = load_config()
source_base = config.get_absolute_source_path()  # Usually ./sources/
content = (source_base / doc['content_path']).read_text()

# ✅ CORRECT - quick method if you're in project root
content = Path(f"./sources/{doc['content_path']}").read_text()
```

**Storage structure:**
- Database stores: `content_path = "example.com/blog/post.md"` (relative)
- Actual file location: `./sources/example.com/blog/post.md`
- Default source directory: `./sources/` (configurable in `.kurt` config)

## Core Operations

### List Documents

List and filter documents by status, URL pattern, or other criteria.

**CLI:**
```bash
# List all documents
kurt content list

# Filter by status
kurt content list --status FETCHED --limit 10

# Filter by URL pattern
kurt content list --url-prefix "https://example.com"
kurt content list --url-contains "blog"

# Combine filters
kurt content list --url-prefix "https://example.com" --url-contains "article"
```

**Python:**
```python
from kurt.document import list_documents
from kurt.models.models import IngestionStatus

# List all
docs = list_documents(limit=10)

# Filter by status and URL
docs = list_documents(
    status=IngestionStatus.FETCHED,
    url_prefix="https://example.com"
)
```

**SQL:**
```sql
-- List all documents
SELECT id, title, source_url, ingestion_status FROM documents;

-- Filter by URL pattern
SELECT * FROM documents WHERE source_url LIKE 'https://example.com%';
```

See [scripts/list_documents.py](scripts/list_documents.py) for more examples.

### Get Document Details

Retrieve metadata for a specific document using full or partial UUID.

**CLI:**
```bash
kurt content get-metadata 44ea066e  # Partial UUID works
```

**Python:**
```python
from kurt.document import get_document

doc = get_document("44ea066e")
print(f"Title: {doc['title']}")
print(f"URL: {doc['source_url']}")
print(f"Status: {doc['ingestion_status']}")
```

See [scripts/get_document.py](scripts/get_document.py) for more examples.

### Access Document Content

Read the actual markdown content from the filesystem.

**Python:**
```python
from kurt.document import get_document
from kurt.config import load_config
from pathlib import Path

# Get document and build full path
doc = get_document("44ea066e")
config = load_config()
content_path = config.get_absolute_source_path() / doc['content_path']

# Read content
content = content_path.read_text()
print(content)
```

**Bash:**
```bash
# Get content_path from database
CONTENT_PATH=$(sqlite3 .kurt/kurt.sqlite \
  "SELECT content_path FROM documents WHERE id LIKE '44ea066e%'")

# Read the file
cat "./sources/${CONTENT_PATH}"
```

See [scripts/read_content.py](scripts/read_content.py) for more examples.

### Delete Documents

Remove documents from database and optionally delete content files.

**CLI:**
```bash
# Delete database record only
kurt document delete 44ea066e

# Delete database record and content file
kurt document delete 44ea066e --delete-content
```

**Python:**
```python
from kurt.document import delete_document

# Delete with content
delete_document("44ea066e", delete_content=True)
```

See [scripts/delete_document.py](scripts/delete_document.py) for more examples.

### View Statistics

Get document counts, status breakdown, and storage usage.

**CLI:**
```bash
kurt document stats
```

**Python:**
```python
from kurt.document import get_document_stats

stats = get_document_stats()
print(f"Total documents: {stats['total_count']}")
print(f"Fetched: {stats['fetched_count']}")
```

## Advanced Operations

### Find Duplicate Content

Identify documents with identical content using content hashes.

**SQL:**
```sql
-- Find duplicates by content hash
SELECT content_hash, COUNT(*) as count,
       GROUP_CONCAT(title, ' | ') as titles
FROM documents
WHERE content_hash IS NOT NULL
GROUP BY content_hash
HAVING COUNT(*) > 1;
```

**Python:**
```python
import sqlite3

conn = sqlite3.connect('.kurt/kurt.sqlite')
cursor = conn.execute("""
    SELECT content_hash, COUNT(*) as count
    FROM documents
    GROUP BY content_hash
    HAVING count > 1
""")

for hash, count in cursor:
    print(f"Hash {hash}: {count} duplicates")
```

See [scripts/find_duplicates.py](scripts/find_duplicates.py) for more examples.

### Query Metadata with SQL

Extract and analyze metadata fields stored as JSON.

**SQL:**
```sql
-- Find documents by author
SELECT title, json_extract(author, '$[0]') as author_name
FROM documents
WHERE author IS NOT NULL;

-- Find documents by category
SELECT title, categories
FROM documents
WHERE json_extract(categories, '$') LIKE '%technology%';

-- Documents published in 2024
SELECT title, published_date
FROM documents
WHERE published_date LIKE '2024%';
```

See [scripts/sql_queries.sql](scripts/sql_queries.sql) for more examples.

### Export Documents

Export document data to JSON for backup or analysis.

**Python:**
```python
from kurt.document import list_documents
import json

# Export all documents
docs = list_documents()
with open('export.json', 'w') as f:
    json.dump(docs, f, indent=2, default=str)

# Export filtered subset
fetched_docs = list_documents(status="FETCHED")
with open('fetched_only.json', 'w') as f:
    json.dump(fetched_docs, f, indent=2, default=str)
```

See [scripts/export_documents.py](scripts/export_documents.py) for more examples.

## Quick Reference

| Task | CLI | Python API |
|------|-----|------------|
| List documents | `kurt content list` | `list_documents()` |
| Filter by URL | `--url-prefix https://...` | `url_prefix="https://..."` |
| Get document | `kurt content get-metadata <id>` | `get_document(document_id)` |
| Read content | N/A | `Path(f"./sources/{doc['content_path']}").read_text()` |
| Delete document | `kurt document delete <id>` | `delete_document(document_id)` |
| View stats | `kurt document stats` | `get_document_stats()` |
| Find duplicates | SQL query | See scripts/find_duplicates.py |
| Export to JSON | N/A | `json.dump(list_documents(), ...)` |

## Python API Reference

```python
from kurt.document import (
    list_documents,      # List/filter documents
    get_document,        # Get by ID (partial UUID supported)
    delete_document,     # Delete document
    get_document_stats,  # Get statistics
)

# list_documents(status=None, url_prefix=None, url_contains=None, limit=100, offset=0)
# Returns: List[dict] with document metadata

# get_document(document_id: str)
# Returns: dict with document metadata
# Supports partial UUIDs (e.g., "44ea066e")

# delete_document(document_id: str, delete_content: bool = False)
# Returns: None
# Set delete_content=True to also remove the markdown file

# get_document_stats()
# Returns: dict with counts and statistics
```

## Database Schema

See [kurt-core/src/kurt/models/models.py](../../../kurt-core/src/kurt/models/models.py) - `Document` class

**Key fields:**
- `id` (TEXT) - UUID primary key
- `title` (TEXT) - Document title
- `source_url` (TEXT) - Original URL (unique)
- `content_path` (TEXT) - Relative path to markdown file
- `ingestion_status` (TEXT) - NOT_FETCHED, FETCHED, ERROR
- `content_hash` (TEXT) - SHA256 for deduplication
- `author` (JSON) - List of authors
- `published_date` (TEXT) - ISO date string
- `categories` (JSON) - List of categories/tags
- `language` (TEXT) - ISO 639-1 language code
- `description` (TEXT) - Meta description

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Document not found" | Check `kurt content list` or use more UUID chars |
| "Ambiguous ID" | Use more characters: `44ea066eca` instead of `44ea` |
| Metadata is null | Document not fetched yet - run `kurct content fetch <id>` |
| Content file not found | `content_path` is relative - prepend `./sources/` |
| Wrong content path | Check source directory: `cat .kurt` |

**Debugging content paths:**
```bash
# Check configuration
cat .kurt

# List actual files
find ./sources -name "*.md"

# Compare DB vs filesystem
sqlite3 .kurt/kurt.sqlite "SELECT content_path FROM documents LIMIT 5"
ls -la ./sources/
```

## Next Steps

- For content ingestion, see the **ingest-content-skill**
- For custom queries, see [scripts/sql_queries.sql](scripts/sql_queries.sql)
- For data export, see [scripts/export_documents.py](scripts/export_documents.py)
