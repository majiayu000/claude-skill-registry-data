---
name: google-drive-management
description: Manages Google Drive files and folders through the Drive API. Search for files, read content, create and update documents, organize folders, manage permissions, and sync files. Use when working with Google Drive, uploading/downloading files, searching Drive content, or managing Drive organization.
---

# Google Drive Management

Comprehensive Google Drive integration enabling search, file operations, folder management, permissions control, and content synchronization through the Google Drive API v3.

## Quick Start

When asked to work with Google Drive:

1. **Authenticate**: Set up OAuth2 credentials (one-time setup)
2. **Search files**: Find files by name, type, or content
3. **Read content**: Download and read file contents
4. **Create/Update**: Upload new files or modify existing ones
5. **Organize**: Create folders and move files
6. **Share**: Manage permissions and sharing

## Prerequisites

### One-Time Setup

**1. Enable Google Drive API:**
```bash
# Visit Google Cloud Console
# https://console.cloud.google.com/

# Enable Drive API for your project
# APIs & Services > Enable APIs and Services > Google Drive API
```

**2. Create OAuth2 Credentials:**
```bash
# In Google Cloud Console:
# APIs & Services > Credentials > Create Credentials > OAuth client ID
# Application type: Desktop app
# Download credentials as credentials.json
```

**3. Install Dependencies:**
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client --break-system-packages
```

**4. Initial Authentication:**
```bash
python scripts/authenticate.py
# Opens browser for Google sign-in
# Saves token.json for future use
```

See [reference/setup-guide.md](reference/setup-guide.md) for detailed setup instructions.

## Core Operations

### Search for Files

**Basic search:**
```bash
python scripts/search_files.py --query "name contains 'report'"
```

**Search patterns:**
```python
# By name
query = "name contains 'Q4 Report'"

# By type
query = "mimeType = 'application/vnd.google-apps.spreadsheet'"

# By folder
query = "'FOLDER_ID' in parents"

# Modified recently
query = "modifiedTime > '2025-01-01T00:00:00'"

# Combination
query = "name contains 'budget' and mimeType contains 'spreadsheet'"
```

**Common searches:**
```bash
# Find all PDFs
python scripts/search_files.py --type pdf

# Find files modified today
python scripts/search_files.py --modified-today

# Find files in specific folder
python scripts/search_files.py --folder "Project Documents"

# Search file content (for Google Docs/Sheets)
python scripts/search_files.py --content "quarterly review"
```

See [reference/search-patterns.md](reference/search-patterns.md) for comprehensive query syntax.

### Read File Content

**Download files:**
```bash
# Google Docs/Sheets/Slides
python scripts/download_file.py --file-id FILE_ID --format pdf
python scripts/download_file.py --file-id FILE_ID --format docx
python scripts/download_file.py --file-id FILE_ID --format xlsx

# Binary files (PDFs, images, etc.)
python scripts/download_file.py --file-id FILE_ID --output ./local-file.pdf
```

**Read Google Docs as text:**
```bash
# Export as plain text
python scripts/read_doc.py --file-id FILE_ID

# Export as markdown
python scripts/read_doc.py --file-id FILE_ID --format markdown
```

**Read Sheets data:**
```bash
# Get sheet as CSV
python scripts/read_sheet.py --file-id FILE_ID --sheet "Sheet1"

# Get specific range
python scripts/read_sheet.py --file-id FILE_ID --range "A1:D10"
```

### Create and Upload Files

**Create Google Docs:**
```bash
# Create new Doc
python scripts/create_doc.py --title "Meeting Notes" --content "..."

# Create from template
python scripts/create_from_template.py --template-id TEMPLATE_ID --title "Q4 Report"
```

**Upload files:**
```bash
# Upload any file
python scripts/upload_file.py --file ./local-file.pdf --folder-id FOLDER_ID

# Upload with metadata
python scripts/upload_file.py --file ./data.csv --name "Sales Data Q4" --description "Quarterly sales figures"
```

**Create Sheets:**
```bash
# Create with data
python scripts/create_sheet.py --title "Budget 2025" --data data.csv

# Create from scratch
python scripts/create_sheet.py --title "Tracking Sheet" --headers "Date,Task,Status,Owner"
```

### Update Files

**Update Google Docs:**
```bash
# Append content
python scripts/update_doc.py --file-id FILE_ID --append "New section..."

# Replace content
python scripts/update_doc.py --file-id FILE_ID --content "Complete new content"

# Update specific paragraph
python scripts/update_doc.py --file-id FILE_ID --find "old text" --replace "new text"
```

**Update Sheets:**
```bash
# Update range
python scripts/update_sheet.py --file-id FILE_ID --range "A1:B10" --values data.csv

# Append rows
python scripts/update_sheet.py --file-id FILE_ID --append --values new_data.csv
```

### Folder Management

**Create folders:**
```bash
# Create folder
python scripts/create_folder.py --name "Project Alpha" --parent PARENT_ID

# Create nested structure
python scripts/create_folder.py --path "Projects/2025/Q1/Project Alpha"
```

**Move files:**
```bash
# Move to folder
python scripts/move_file.py --file-id FILE_ID --folder-id FOLDER_ID

# Move multiple files
python scripts/move_files.py --files file1_id,file2_id,file3_id --folder-id FOLDER_ID
```

**List folder contents:**
```bash
# List files in folder
python scripts/list_folder.py --folder-id FOLDER_ID

# Recursive listing
python scripts/list_folder.py --folder-id FOLDER_ID --recursive
```

### Permissions and Sharing

**Share files:**
```bash
# Share with specific user
python scripts/share_file.py --file-id FILE_ID --email user@example.com --role writer

# Share with anyone with link
python scripts/share_file.py --file-id FILE_ID --anyone --role reader

# Share with domain
python scripts/share_file.py --file-id FILE_ID --domain company.com --role commenter
```

**Permission roles:**
- `owner` - Full control
- `organizer` - Can organize files (Drive folders)
- `fileOrganizer` - Can organize files
- `writer` - Can edit
- `commenter` - Can comment
- `reader` - View only

**List permissions:**
```bash
# View who has access
python scripts/list_permissions.py --file-id FILE_ID
```

**Revoke access:**
```bash
# Remove permission
python scripts/revoke_permission.py --file-id FILE_ID --email user@example.com
```

## Common Workflows

### Workflow 1: Sync Project Files

**Scenario:** Keep local project synced with Drive folder

```bash
# Download entire folder
python scripts/sync_folder.py --folder-id FOLDER_ID --local ./project --download

# Upload changes
python scripts/sync_folder.py --folder-id FOLDER_ID --local ./project --upload

# Bidirectional sync
python scripts/sync_folder.py --folder-id FOLDER_ID --local ./project --sync
```

### Workflow 2: Batch Process Documents

**Scenario:** Convert all Docs in folder to PDF

```bash
# Export all docs
python scripts/batch_export.py --folder-id FOLDER_ID --format pdf --output ./exports/
```

### Workflow 3: Organize Files by Type

**Scenario:** Move files to type-specific folders

```bash
# Auto-organize
python scripts/organize_files.py --source-folder FOLDER_ID --by-type
```

### Workflow 4: Backup Drive Content

**Scenario:** Create local backup of Drive files

```bash
# Full backup
python scripts/backup_drive.py --output ./backup/ --include-versions

# Incremental backup
python scripts/backup_drive.py --output ./backup/ --since-last-backup
```

### Workflow 5: Search and Process

**Scenario:** Find all spreadsheets with "budget" and export data

```bash
# Search and process
python scripts/search_and_process.py \
  --query "name contains 'budget' and mimeType contains 'spreadsheet'" \
  --action export \
  --format csv \
  --output ./budgets/
```

## File Type Reference

### MIME Types

**Google Workspace:**
```python
MIME_TYPES = {
    'doc': 'application/vnd.google-apps.document',
    'sheet': 'application/vnd.google-apps.spreadsheet',
    'slide': 'application/vnd.google-apps.presentation',
    'form': 'application/vnd.google-apps.form',
    'folder': 'application/vnd.google-apps.folder',
}
```

**Export formats:**
```python
EXPORT_FORMATS = {
    'doc': ['pdf', 'docx', 'odt', 'rtf', 'txt', 'html', 'epub'],
    'sheet': ['pdf', 'xlsx', 'ods', 'csv', 'tsv', 'html'],
    'slide': ['pdf', 'pptx', 'odp', 'txt'],
}
```

**Common MIME types:**
```python
'application/pdf' - PDF
'image/jpeg' - JPEG image
'image/png' - PNG image
'text/plain' - Plain text
'application/zip' - ZIP archive
'video/mp4' - MP4 video
```

## Search Query Syntax

### Operators

```python
# Equals
"name = 'Budget.xlsx'"

# Contains
"name contains 'report'"

# Not equals
"mimeType != 'application/vnd.google-apps.folder'"

# Greater/Less than (dates)
"modifiedTime > '2025-01-01T00:00:00'"
"createdTime < '2024-12-31T23:59:59'"

# In (parents, owners)
"'FOLDER_ID' in parents"
"'user@example.com' in owners"

# Logical operators
"name contains 'Q4' and mimeType contains 'spreadsheet'"
"name contains 'draft' or name contains 'review'"
"not name contains 'old'"
```

### Field Options

```python
# File properties
name, mimeType, fullText, modifiedTime, createdTime
trashed, starred, hidden, viewed

# Ownership/sharing
owners, writers, readers, parents

# Special
sharedWithMe, visibility
```

See [reference/search-patterns.md](reference/search-patterns.md) for complete query reference.

## API Rate Limits

**Drive API quotas:**
- **Queries per day:** 1,000,000,000
- **Queries per 100 seconds per user:** 1,000
- **Queries per 100 seconds:** 10,000

**Best practices:**
- Use batch requests for multiple operations
- Implement exponential backoff for rate limit errors
- Cache file IDs and metadata when possible
- Use partial responses to reduce data transfer

## Error Handling

**Common errors:**

```python
# 401 - Authentication failed
# Solution: Re-run authentication, check token.json

# 403 - Insufficient permissions
# Solution: Check OAuth scopes, request additional permissions

# 404 - File not found
# Solution: Verify file ID, check if file was deleted

# 429 - Rate limit exceeded
# Solution: Implement exponential backoff, reduce request frequency

# 500 - Backend error
# Solution: Retry with exponential backoff
```

**Retry logic:**
```python
import time
from googleapiclient.errors import HttpError

def retry_request(request, max_retries=3):
    for attempt in range(max_retries):
        try:
            return request.execute()
        except HttpError as e:
            if e.resp.status in [429, 500, 503]:
                wait = (2 ** attempt) + random.random()
                time.sleep(wait)
            else:
                raise
    raise Exception("Max retries exceeded")
```

## Security Best Practices

1. **Never commit credentials:**
   ```bash
   # Add to .gitignore
   credentials.json
   token.json
   client_secret*.json
   ```

2. **Use minimal scopes:**
   ```python
   # Only request needed permissions
   SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
   ```

3. **Secure token storage:**
   ```bash
   # Set proper permissions
   chmod 600 token.json
   ```

4. **Rotate credentials regularly:**
   ```bash
   # Delete old token to force re-authentication
   rm token.json
   python scripts/authenticate.py
   ```

## OAuth Scopes

**Available scopes:**
```python
# Full access
'https://www.googleapis.com/auth/drive'

# Read-only
'https://www.googleapis.com/auth/drive.readonly'

# File access (create/modify files created by app)
'https://www.googleapis.com/auth/drive.file'

# Metadata only
'https://www.googleapis.com/auth/drive.metadata.readonly'

# App data folder
'https://www.googleapis.com/auth/drive.appdata'

# Specific types
'https://www.googleapis.com/auth/drive.photos.readonly'
```

Choose the most restrictive scope that meets your needs.

## Scripts Reference

The `scripts/` directory contains utilities for all operations:

**Authentication:**
- `authenticate.py` - Initial OAuth setup
- `refresh_token.py` - Refresh expired token

**Search:**
- `search_files.py` - Search Drive with queries
- `find_by_name.py` - Quick name-based search
- `find_recent.py` - Find recently modified files

**File Operations:**
- `download_file.py` - Download files
- `upload_file.py` - Upload files
- `read_doc.py` - Read Google Doc content
- `read_sheet.py` - Read Sheets data
- `create_doc.py` - Create new Doc
- `create_sheet.py` - Create new Sheet
- `update_doc.py` - Update Doc content
- `update_sheet.py` - Update Sheet data

**Organization:**
- `create_folder.py` - Create folders
- `move_file.py` - Move files
- `list_folder.py` - List folder contents
- `organize_files.py` - Auto-organize by type

**Sharing:**
- `share_file.py` - Share files/folders
- `list_permissions.py` - View permissions
- `revoke_permission.py` - Remove access

**Advanced:**
- `sync_folder.py` - Sync folders
- `backup_drive.py` - Backup Drive content
- `batch_export.py` - Batch operations
- `search_and_process.py` - Search with actions

See individual scripts for detailed usage.

## Best Practices

1. **Search before upload:** Check if file exists to avoid duplicates
2. **Use folders:** Organize files in logical folder structures
3. **Set metadata:** Add descriptions and properties for better searchability
4. **Batch operations:** Process multiple files in single API call when possible
5. **Cache file IDs:** Store IDs locally to avoid repeated searches
6. **Handle pagination:** Use pageToken for large result sets
7. **Export regularly:** Backup important documents locally
8. **Monitor quotas:** Track API usage to stay within limits

## Integration Examples

See [examples/](examples/) for complete workflows:
- [examples/project-sync.md](examples/project-sync.md) - Project folder synchronization
- [examples/document-workflow.md](examples/document-workflow.md) - Document creation and collaboration
- [examples/data-processing.md](examples/data-processing.md) - Sheets data processing
- [examples/backup-strategy.md](examples/backup-strategy.md) - Comprehensive backup approach

## Troubleshooting

**"Token has been expired or revoked"**
```bash
rm token.json
python scripts/authenticate.py
```

**"Insufficient permissions"**
- Check SCOPES in scripts/authenticate.py
- May need to request additional permissions
- Delete token.json and re-authenticate with new scopes

**"File not found"**
- File may be in trash
- Check if you have access
- Verify file ID is correct

**"Rate limit exceeded"**
- Implement delays between requests
- Use batch operations
- Check your quota usage in Google Cloud Console

## Reference Documentation

For detailed information:
- [reference/setup-guide.md](reference/setup-guide.md) - Complete setup instructions
- [reference/search-patterns.md](reference/search-patterns.md) - Query syntax reference
- [reference/api-reference.md](reference/api-reference.md) - API method documentation
- [reference/mime-types.md](reference/mime-types.md) - Complete MIME type reference
