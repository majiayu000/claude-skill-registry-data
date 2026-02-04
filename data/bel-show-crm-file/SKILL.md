---
name: bel-show-crm-file
description: This skill should be used when the user wants to view, display, or show a file stored in the CRM database. This is an orchestration skill that combines downloading from the database and opening with the OS default application. Triggers on requests like "show me the contract from CRM", "display the image from the database", "view the PDF for company X", or "open the attachment from the database".
---

# Show File from CRM Database

View files stored in the CRM database by downloading them to disk and opening them in the default application. This is an orchestration skill that combines the download and open workflows.

## When to Use This Skill

Use this skill when the user wants to:
- **View** a file from the CRM database
- **Display** a document/image/PDF from the database
- **Show** an attachment stored in the database
- **Open** a file that's currently in the database

**Trigger phrases:**
- "Show me the contract from the database"
- "Display the PDF for company Acme Corp"
- "View the image from CRM"
- "Open the attachment for event ID 5"
- "Let me see the file in the database"
- "Show the document stored for person ID 123"

**Do NOT use this skill if:**
- The user only wants to download (use `bel-download-file-from-crm-db`)
- The file is already on disk (use `bel-open-file`)
- The user explicitly says "download" but not "view/show/display"

## How to Use This Skill

This skill orchestrates two other skills in sequence. **Do NOT write a new script** - instead, use the existing skills.

### Workflow Overview

```
1. Download file from database → 2. Open file with OS default app
   (bel-download-file-from-crm-db)    (bel-open-file)
```

### Step-by-Step Process

#### Step 1: Invoke the Download Skill

Use the `bel-download-file-from-crm-db` skill to download the file from the database:

1. Use `bel-crm-db` to query and find the `file_id`
2. Execute: `python scripts/download_file_from_db.py <file_id>`
3. Capture the saved file path from the output

#### Step 2: Invoke the Open Skill

Use the `bel-open-file` skill to open the downloaded file:

1. Take the file path from Step 1
2. Execute: `python scripts/open_file.py <file_path>`
3. The file opens in the default application

### Complete Example

```bash
# User: "Show me the contract for company ID 42"

# Step 1: Download from database
python /path/to/bel-download-file-from-crm-db/scripts/download_file_from_db.py 789 --quiet
# Output: _RESULTS_FROM_AGENT/contract.pdf

# Step 2: Open the file
python /path/to/bel-open-file/scripts/open_file.py _RESULTS_FROM_AGENT/contract.pdf
# File opens in default PDF viewer
```

## Integration Strategy

This skill **does not have its own scripts** - it coordinates existing skills:

**Required skills:**
1. `bel-crm-db` - For database schema and querying
2. `bel-download-file-from-crm-db` - For downloading files
3. `bel-open-file` - For opening files

**Coordination pattern:**
```python
# Pseudo-code for the workflow
file_id = query_database_for_file_id(entity_identifier)
file_path = download_file_from_db(file_id)
open_file(file_path)
```

## Example Workflows

### Workflow 1: Show a specific file by ID
```
User: "Show me file ID 789 from the database"

1. Invoke: bel-download-file-from-crm-db
   - python scripts/download_file_from_db.py 789 --quiet
   - Result: _RESULTS_FROM_AGENT/document.pdf

2. Invoke: bel-open-file
   - python scripts/open_file.py _RESULTS_FROM_AGENT/document.pdf
   - File opens in PDF viewer

3. Report to user: "✅ Opened document.pdf"
```

### Workflow 2: Show a company's contract
```
User: "Show me the contract for Acme Corp"

1. Use bel-crm-db to query:
   - Find company_site_id for "Acme Corp"
   - Find file_id via company_site_file junction table
   - Result: file_id = 456

2. Invoke: bel-download-file-from-crm-db
   - python scripts/download_file_from_db.py 456 --quiet
   - Result: _RESULTS_FROM_AGENT/acme_contract.pdf

3. Invoke: bel-open-file
   - python scripts/open_file.py _RESULTS_FROM_AGENT/acme_contract.pdf
   - Contract opens in PDF viewer

4. Report to user: "✅ Opened acme_contract.pdf for Acme Corp"
```

### Workflow 3: Show an event image
```
User: "Display the image from event 5"

1. Use bel-crm-db to query:
   - Find file_id via event_file where event_id = 5
   - Result: file_id = 234

2. Invoke: bel-download-file-from-crm-db
   - python scripts/download_file_from_db.py 234 --quiet
   - Result: _RESULTS_FROM_AGENT/event_photo.jpg

3. Invoke: bel-open-file
   - python scripts/open_file.py _RESULTS_FROM_AGENT/event_photo.jpg
   - Image opens in default viewer

4. Report to user: "✅ Opened event_photo.jpg"
```

## Error Handling

Handle errors at each step:

**Step 1 - Download errors:**
- File ID not found in database
- Database connection failure
- Disk space issues

**Step 2 - Open errors:**
- File not found (download failed silently)
- No default application for file type
- Permission denied

**Recovery strategy:**
- If download fails, report error and stop
- If open fails, inform user where file was saved so they can open manually

## When to Use Each Skill

Decision tree for file operations:

```
User wants to work with a file
    │
    ├─ File is in database?
    │   ├─ Yes: User wants to view/show/display?
    │   │   ├─ Yes → Use bel-show-crm-file (this skill)
    │   │   └─ No (just download) → Use bel-download-file-from-crm-db
    │   │
    │   └─ No: File already on disk
    │       └─ User wants to open? → Use bel-open-file
```

## Technical Notes

**This skill is orchestration only:**
- No custom scripts needed
- Chains existing skills together
- Provides a user-friendly workflow for common use case
- Simplifies the "view database file" operation

**Benefits of this approach:**
- Single skill for the most common scenario
- Reuses existing, tested scripts
- Clear separation of concerns
- Easy to maintain and extend
