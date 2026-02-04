---
name: import-content
description: Import existing markdown files into Kurt database. Fix ERROR records, bulk import files, link content to database.
---

# Import Content

## Overview

This skill helps import existing markdown files into Kurt's database when automatic ingestion fails. It's the manual fallback for the auto-import hook and provides bulk operations for fixing ERROR records.

**When to use:**
- Auto-import hook failed
- Manually created/edited markdown files in `/sources/`
- Bulk import from backups or migrations
- Fix ERROR records after WebFetch fallback

## Quick Start

```bash
# Fix single ERROR record
python .claude/scripts/import_markdown.py \
  --document-id 5f403260 \
  --file-path sources/docs.getdbt.com/guides/fusion-quickstart.md

# Extract metadata after import
kurt index 5f403260
```

## Common Workflows

### Workflow 1: Fix ERROR Records After WebFetch

**Scenario:** Used WebFetch to retrieve content, but Kurt DB has ERROR records.

**Steps:**
1. List ERROR records:
   ```bash
   kurt content list --status ERROR
   ```

2. Find corresponding markdown files:
   ```bash
   find sources -name "*.md" -type f
   ```

3. For each ERROR record with a matching file:
   ```bash
   python .claude/scripts/import_markdown.py \
     --document-id <doc-id> \
     --file-path <file-path>

   # Then extract metadata
   kurt index <doc-id>
   ```

4. Verify success:
   ```bash
   kurt content get-metadata <doc-id>
   ```

### Workflow 2: Bulk Import All ERROR Records

**Scenario:** Multiple ERROR records with existing markdown files.

**Create bash script:**
```bash
#!/bin/bash
# Fix all ERROR records with matching files

while read -r doc_id url status; do
  if [ "$status" = "ERROR" ]; then
    # Try to find corresponding file
    # (Implement file finding logic based on URL)

    if [ -f "$file_path" ]; then
      echo "Importing: $doc_id"
      python .claude/scripts/import_markdown.py \
        --document-id "$doc_id" \
        --file-path "$file_path"

      kurt index "$doc_id"
    fi
  fi
done < <(kurt content list)
```

### Workflow 3: Import Manually Created Files

**Scenario:** You created markdown files directly without using kurct content.

**Steps:**
1. Verify file exists and has content
2. Check if document record exists:
   ```bash
   kurt content list --url-contains <domain>
   ```

3. If ERROR record exists, import:
   ```bash
   python .claude/scripts/import_markdown.py \
     --document-id <doc-id> \
     --file-path <file-path>
   ```

4. If no record exists, use kurct content:
   ```bash
   # Create record and import
   kurct content add <url>
   # Then import file content
   python .claude/scripts/import_markdown.py \
     --document-id <new-doc-id> \
     --file-path <file-path>
   ```

## Auto-Import Hook

Files written to `/sources/` or `projects/*/sources/` are automatically imported via PostToolUse hook.

**How it works:**
1. Claude writes markdown file to sources
2. PostToolUse hook triggers
3. Script maps file path → URL
4. Finds ERROR record for URL
5. Updates record to FETCHED
6. Extracts metadata
7. Shows confirmation message

**Hook location:** `.claude/settings.json`

**Script:** `.claude/scripts/auto-import-source.sh`

**Logs:** `.claude/logs/auto-import.log`

## YAML Frontmatter & Metadata Extraction

The import script automatically parses YAML frontmatter from markdown files and populates database metadata fields.

### Supported Metadata Fields

The following frontmatter fields are automatically extracted and stored in Kurt database:

| Frontmatter Field | Database Column | Notes |
|-------------------|-----------------|-------|
| `title` | `title` | Full page title |
| `description` | `description` | Page description/summary |
| `author` | `author` | Single author or list (stored as JSON array) |
| `published_date` | `published_date` | Publication date |
| `date` | `published_date` | Alternative to published_date |
| `last_modified` | `published_date` | Falls back if published_date not found |

### Frontmatter Format

Use YAML frontmatter at the start of markdown files:

```markdown
---
title: "Full Page Title | Site Name"
url: https://example.com/page
description: "Brief description of the page content"
author: "Author Name"
published_date: "2025-05-28"
last_modified: "2025-10-22"
fetched_via: WebFetch
fetched_at: "2025-10-23"
---

# Page Content

[Markdown content here...]
```

### Benefits of Frontmatter

**With frontmatter:**
- ✅ Proper page titles (not URL slugs)
- ✅ Author attribution
- ✅ Publication dates for content freshness tracking
- ✅ Descriptions for search and discovery
- ✅ Same rich metadata as Kurt-fetched content

**Without frontmatter:**
- ⚠️ Title defaults to URL slug or filename
- ⚠️ No author information
- ⚠️ No publication date tracking
- ⚠️ Limited searchability

### Example: With vs Without Metadata

**Document imported without frontmatter:**
```bash
kurt content get-metadata abc123

Title: fusion
Status: FETCHED
Author(s): None
Published: None
Description: None
```

**Document imported with frontmatter:**
```bash
kurt content get-metadata abc123

Title: Quickstart for the dbt Fusion engine | dbt Developer Hub
Status: FETCHED
Author(s): dbt Labs, Inc.
Published: 2025-10-22
Description: Get started with the dbt Fusion engine in minutes...
```

### Extracting Metadata with WebFetch

When using WebFetch as a fallback, always request metadata:

```
WebFetch prompt:
"Extract ALL metadata from this page including:
- Full page title
- Description/meta description
- Author(s)
- Published date or last modified date
- The complete page content as markdown

Return with clear separation between metadata and content."
```

Then save with frontmatter format shown above.

### Requirements

**Python dependencies:**
- `pyyaml` library (auto-installed with Kurt)

If yaml library is not available, frontmatter parsing is skipped gracefully (no errors, but metadata won't be extracted).

### Troubleshooting Frontmatter

**Frontmatter not extracted:**
1. Check format: Must start with `---` on first line
2. Verify YAML syntax: Use quotes for strings with special characters
3. Check logs: `.claude/logs/auto-import.log`
4. Verify yaml library: `python -c "import yaml; print('OK')"`

**Wrong metadata populated:**
1. Check field names (see supported fields table above)
2. Verify date format: Use ISO format `YYYY-MM-DD`
3. Author as list: `author: ["Name 1", "Name 2"]` or `author: "Single Name"`

## Path Mapping

The import script converts file paths to content_path format:

**Organization KB (top-level sources/):**
```
File: sources/docs.getdbt.com/guides/fusion.md
→ content_path: docs.getdbt.com/guides/fusion.md
→ URL: https://docs.getdbt.com/guides/fusion
```

**Project sources:**
```
File: projects/my-project/sources/internal-spec.md
→ content_path: projects/my-project/sources/internal-spec.md
→ URL: (no URL mapping, project-specific)
```

## Troubleshooting

### Auto-Import Didn't Trigger

**Check:**
1. Is file in sources/ directory? `ls sources/`
2. Is file .md extension? `file <path>`
3. Check logs: `cat .claude/logs/auto-import.log`
4. Is Kurt installed? `which kurt`

**Manual fix:**
```bash
python .claude/scripts/import_markdown.py \
  --document-id <doc-id> \
  --file-path <file-path>
```

### No ERROR Record Found

**Cause:** File is new, not from failed fetch

**Solution:** Create document record first
```bash
# If you know the URL:
kurct content add <url>

# Then import content
python .claude/scripts/import_markdown.py \
  --document-id <new-doc-id> \
  --file-path <file-path>
```

### Import Failed: Database Locked

**Cause:** Another Kurt process has DB lock

**Solution:** Wait and retry, or kill other processes
```bash
# Check for running Kurt processes
ps aux | grep kurt

# Wait and retry
sleep 2
python .claude/scripts/import_markdown.py ...
```

### Metadata Extraction Failed

**Cause:** LLM API timeout or rate limit

**Solution:** Retry manually
```bash
# List docs without metadata
kurt content list --status FETCHED

# Re-run indexing
kurt index <doc-id>

# Or batch index all
kurt index --status FETCHED --url-prefix <url>
```

## Quick Reference

| Task | Command |
|------|---------|
| Import single file | `python .claude/scripts/import_markdown.py --document-id <id> --file-path <path>` |
| List ERROR records | `kurt content list --status ERROR` |
| Extract metadata | `kurt index <doc-id>` |
| View import logs | `cat .claude/logs/auto-import.log` |
| Verify import | `kurt content get-metadata <doc-id>` |
| Bulk index | `kurt index --status FETCHED --url-prefix <url>` |

## Integration with Other Skills

**With ingest-content-skill:**
- Use ingest for web content when possible
- Use import when ingest fails (anti-bot protection)
- WebFetch → save to sources → auto-import

**With document-management-skill:**
- List ERROR records to find import candidates
- Verify imports with `kurt content get-metadata`
- Query imported content after indexing

**With project-management-skill:**
- Import sources for projects
- Fix ERROR records in project sources
- Ensure all project content is indexed

## Python API

```python
from pathlib import Path
import sys
sys.path.append('.claude/scripts')
from import_markdown import import_markdown_to_kurt

# Import single file
success = import_markdown_to_kurt(
    document_id="5f403260",
    file_path="sources/docs.getdbt.com/guides/fusion.md"
)

if success:
    print("✓ Import successful")
    # Run metadata extraction
    import subprocess
    subprocess.run(["kurt", "index", "5f403260"])
```

## Best Practices

1. **Always verify file exists** before importing
2. **Check logs** if auto-import seems to fail
3. **Run metadata extraction** after import (kurt index)
4. **Verify with `kurt content get-metadata`** after import
5. **Use bulk operations** for multiple files
6. **Monitor .claude/logs/auto-import.log** for patterns

## Next Steps

- For web content ingestion, see **ingest-content-skill**
- For document queries, see **document-management-skill**
- For metadata extraction, see **document-indexing-skill**
- For project management, see **project-management-skill**
