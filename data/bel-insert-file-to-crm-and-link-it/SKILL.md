---
name: bel-insert-file-to-crm-and-link-it
description: This skill should be used when inserting files (images, PDFs, Excel files, documents) into the CRM database and linking them to companies, people, events, or sales opportunities. The skill handles base64 encoding, hash calculation, MIME type detection, and SQL insertion automatically through a Python script.
---

# BEL Insert File to CRM and Link It

## Overview

This skill provides a streamlined workflow for inserting files into the CRM database's `data_files` table. It handles all technical details including file encoding, hash calculation, MIME type detection, and database insertion through a robust Python script.

The skill is designed to avoid polluting the agent's context window by executing file operations through an external script rather than inline code generation.

## When to Use This Skill

Use this skill when:
- The user asks to insert/upload/save a file to the CRM database
- The user wants to link a file (image, PDF, Excel, document) to a company, person, event, or opportunity
- The user mentions "save to CRM", "upload to database", "store in CRM"
- The user provides files and asks to associate them with CRM entities
- The user mentions company_site, person, event, or sales_opportunity with file operations

## Core Capabilities

### 1. Automatic File Processing

The `scripts/insert_file_to_crm.py` script handles:
- **Base64 encoding**: Converts binary file data to text for database storage
- **SHA256 hashing**: Calculates integrity hash for deduplication and verification
- **MIME type detection**: Automatically determines file type from extension
- **File type categorization**: Maps MIME types to categories (image, document, spreadsheet, other)
- **SQL generation**: Creates properly formatted INSERT statements
- **Database execution**: Executes SQL through psql command

### 2. Supported File Types

**Images**: .jpg, .jpeg, .png, .gif
**Documents**: .pdf, .docx, .doc, .txt
**Spreadsheets**: .xlsx, .xls, .csv
**Other**: Any binary file (handled as 'application/octet-stream')

### 3. Flexible Linking

Files can be linked to one or more CRM entities:
- **Companies** (company_site_id)
- **People** (person_id)
- **Events** (event_id)
- **Sales Opportunities** (sales_opportunity_id)

At least one link must be specified when inserting a file.

## Workflow

### Step 1: Identify the File and Link

Determine:
- **File path**: Where is the file located?
- **Link target**: Which CRM entity should the file be linked to?
  - Company ID (most common)
  - Person ID
  - Event ID
  - Opportunity ID

### Step 2: Gather Optional Metadata

Ask the user or infer:
- **Description**: Human-readable description of the file
- **Tags**: Comma-separated tags for categorization (e.g., "contract,signed" or "workshop,photo")

If the user doesn't provide these, make reasonable inferences:
- Description: "Workshop photo" for event images, "CRM data spreadsheet" for Excel files
- Tags: Derive from file content or context

### Step 3: Execute the Script

Run `scripts/insert_file_to_crm.py` with appropriate arguments:

```bash
python3 scripts/insert_file_to_crm.py <file_path> \
    --company-id <id> \
    --description "<description>" \
    --tags "<tag1>,<tag2>,<tag3>"
```

**Required arguments:**
- `file_path`: Path to the file to insert
- At least one of: `--company-id`, `--person-id`, `--event-id`, `--opportunity-id`

**Optional arguments:**
- `--description`: Description of the file
- `--tags`: Comma-separated tags
- `--dry-run`: Generate SQL without executing (for testing)

### Step 4: Verify Success

The script outputs:
- ✅ Success message with inserted file ID
- ❌ Error message if insertion fails

Confirm with the user that the file was inserted successfully.

## Examples

### Example 1: Insert Workshop Photo for Company

```bash
python3 scripts/insert_file_to_crm.py \
    DATA_FROM_USER/workshop_photo.jpg \
    --company-id 1 \
    --description "Workshop/Seminar-Foto: Diskussionsrunde mit mehreren Teilnehmern" \
    --tags "workshop,meeting,photo"
```

### Example 2: Insert Excel File with CRM Data

```bash
python3 scripts/insert_file_to_crm.py \
    DATA_FROM_USER/leads.xlsx \
    --company-id 1 \
    --description "CRM Lead-Management Datenbank mit 139 Kontakten" \
    --tags "crm,leads,contacts"
```

### Example 3: Insert Contract for Person

```bash
python3 scripts/insert_file_to_crm.py \
    contracts/signed_contract.pdf \
    --person-id 42 \
    --company-id 1 \
    --description "Signed customer contract" \
    --tags "contract,signed,legal"
```

### Example 4: Dry Run (Test Without Inserting)

```bash
python3 scripts/insert_file_to_crm.py \
    DATA_FROM_USER/document.pdf \
    --company-id 1 \
    --description "Test document" \
    --dry-run
```

## Schema Reference

For detailed schema information, refer to `references/data_files_schema.md`, which includes:
- Complete table structure
- Column definitions and data types
- JSONB tag structure
- Common MIME types
- Example queries

## Tips

1. **Context-Efficient**: Always use the Python script instead of generating inline code. This keeps the agent's context window clean.

2. **MIME Type Detection**: The script automatically detects MIME types. No need to specify them manually.

3. **Multiple Files**: To insert multiple files, run the script multiple times (potentially in parallel with shell background jobs).

4. **Tag Strategy**: Use consistent tags for easier querying:
   - Document type: "contract", "invoice", "report"
   - Status: "draft", "signed", "final"
   - Category: "workshop", "meeting", "sales"

5. **Error Handling**: If insertion fails, the script provides clear error messages. Common issues:
   - File not found
   - Missing link (no company/person/event/opportunity ID)
   - Database connection error
   - Permission issues

6. **Schema Access**: Use the `bel-crm-schema-write-db` skill if complex SQL queries are needed beyond simple file insertion.

## Resources

### scripts/insert_file_to_crm.py
Python script that handles all file processing and database insertion. Execute this script to insert files - do not rewrite the logic inline.

### references/data_files_schema.md
Complete schema documentation for the `data_files` table, including column definitions, JSONB structures, and example queries.
