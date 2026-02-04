---
name: bel-download-file-from-crm-db
description: This skill should be used when the user wants to download or retrieve a file from the CRM database and save it to the filesystem. Triggers on requests like "download the contract from CRM", "save the database file to disk", "get the PDF from the database", or "retrieve the attachment from CRM". Uses the bel-crm-db skill for schema knowledge.
---

# Download File from CRM Database

Download files stored in the CRM PostgreSQL database and save them to the filesystem in `_RESULTS_FROM_AGENT/`.

## When to Use This Skill

Use this skill when the user wants to:
- Download a file from the CRM database to disk
- Retrieve a document/image/PDF stored in the database
- Save a database attachment to the filesystem
- Export file data from the CRM

**Trigger phrases:**
- "Download the contract from the database"
- "Save the file from CRM to disk"
- "Get me the PDF from database ID 123"
- "Retrieve the attachment for company X"
- "Export the image from the database"

**Do NOT use this skill if:**
- The user only wants to view/open a file (use `bel-open-file` instead)
- The user wants to see a file from the database (use `bel-show-crm-file` instead)
- The file is already on disk (no download needed)

## How to Use This Skill

### Step 1: Use the CRM Database Skill for Schema Knowledge

To understand the database structure and query files, invoke the `bel-crm-db` skill first to get access to table schemas and connection details.

### Step 2: Identify the File to Download

Determine the `file_id` from the database. This may require querying tables that link to files:

**Common junction tables:**
- Files linked to companies: `company_site_file` table
- Files linked to people: `person_file` table
- Files linked to events: `event_file` table
- Files linked to opportunities: `sales_opportunity_file` table

**Example query to find files:**
```sql
-- Find all files for a company
SELECT f.file_id, f.file_name, f.mime_type, f.file_size
FROM file f
JOIN company_site_file csf ON f.file_id = csf.file_id
WHERE csf.company_site_id = 123;
```

### Step 3: Download the File

Execute the download script with the `file_id`:

```bash
python scripts/download_file_from_db.py <file_id>
```

**Options:**
```bash
# Download with custom output directory
python scripts/download_file_from_db.py 456 --output-dir /custom/path

# Quiet mode (only output file path)
python scripts/download_file_from_db.py 456 --quiet
```

### Step 4: Report Results to User

Inform the user where the file was saved:

```
✅ File downloaded successfully!
   File path: _RESULTS_FROM_AGENT/contract.pdf
   Original name: contract.pdf
   MIME type: application/pdf
   Size: 245,832 bytes
```

## Technical Details

### Database Schema

The script queries the `file` table with this structure:

```sql
CREATE TABLE file (
    file_id SERIAL PRIMARY KEY,
    file_hash VARCHAR(64) UNIQUE NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    mime_type VARCHAR(127),
    file_data BYTEA NOT NULL,
    file_size INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### File Storage

- **Default location:** `_RESULTS_FROM_AGENT/`
- **Filename collision handling:** Appends `_1`, `_2`, etc. if file exists
- **Path traversal protection:** Sanitizes filenames before saving

### Database Connection

The script uses environment variables for database connection:
- `POSTGRES_URL` (preferred): Full connection string
- Or individual variables: `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`

## Error Handling

Common errors:
- **File not found:** `file_id` doesn't exist in database
- **Connection error:** Database credentials incorrect or server unavailable
- **Permission error:** Insufficient write permissions for output directory
- **Disk space:** Insufficient space for large files

## Integration with Other Skills

This skill integrates with:
- **`bel-crm-db`**: For schema knowledge and querying file metadata
- **`bel-open-file`**: To open the downloaded file after saving
- **`bel-show-crm-file`**: Orchestration skill that uses both download and open

## Example Workflows

### Workflow 1: Download a specific file by ID
```
User: "Download file ID 789 from the database"

1. Use bel-crm-db to understand schema
2. Run: python scripts/download_file_from_db.py 789
3. Report the saved file path to user
```

### Workflow 2: Find and download a company's contract
```
User: "Download the contract for Acme Corp"

1. Use bel-crm-db to query:
   - Find company_site_id for "Acme Corp"
   - Find file_id via company_site_file junction table
2. Run: python scripts/download_file_from_db.py <file_id>
3. Report results to user
```

### Workflow 3: Download multiple files
```
User: "Download all images for event ID 5"

1. Query event_file junction table for all file_ids
2. Loop through each file_id:
   - python scripts/download_file_from_db.py <file_id>
3. Report all downloaded file paths
```
