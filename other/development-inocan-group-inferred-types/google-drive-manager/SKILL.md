---
name: google-drive-manager
description: Expert in Google Drive file management. Use when searching, copying, moving, uploading, downloading, sharing, or managing files and folders in Google Drive.
---

# Google Drive Manager Skill

Expert in managing Google Drive files and folders with comprehensive operations including search, copy, move, upload, download, share, and delete.

## Core Capabilities

- Search files by name, query, or MIME type
- Upload files to Google Drive
- Download files from Google Drive (with smart export for Google Workspace files)
- Copy files with optional renaming and parent folder
- Move files between folders
- Create and delete folders
- Share files with specific permissions (users, groups, or anyone with the link)
- List, add, and remove file permissions
- Get detailed file information including full path hierarchy
- List folder contents (browse files and subfolders inside any folder)
- Rename files and folders

## When to Use This Skill

Use this skill when users request:
- "Search for files named 'report' in Google Drive"
- "Upload this document to my Drive"
- "Download the file with ID xyz123"
- "Copy this spreadsheet to another folder"
- "Move this file to the Reports folder"
- "Create a new folder called 'Q4 Reports'"
- "Share this file with user@example.com as editor"
- "Get information about this Drive file"
- "Where is this file located?" or "Show me the path of this file" (use info command)
- "In which folder is this file located?" or "What's the folder path for this file?" (use info command)
- "Who has access to this file?" or "List permissions for this file"
- "Make this file public" or "Share with anyone who has the link"
- "Remove public access" or "Make this file private again"
- "Remove user@example.com access to this file"
- "List all files in this folder" or "Show me what's in folder XYZ"
- "Rename this file to..." or "Change the folder name to..."

**IMPORTANT:** When the user provides only a document/file title without a file ID (e.g., "check document XYZ", "look at the v3 file", "compare with report ABC"), ALWAYS use this skill to search for the file first to get its file ID before performing any operations with other skills (like google-docs-manager).

## Available Tools

### Drive Manager Binary (gdrive)

**Location:** `~/.claude/skills/google-drive-manager/scripts/gdrive`

**Binary:** Go-based command-line tool for Google Drive operations. No Python installation required.

**Source Code:** `~/projects/new/gdrive/` (see CLAUDE.md for build instructions)

**Usage:**
```bash
# Search files
~/.claude/skills/google-drive-manager/scripts/gdrive search QUERY [--type TYPE] [--max N]

# File operations
~/.claude/skills/google-drive-manager/scripts/gdrive file copy FILE [NEW_NAME] [--parent FOLDER] [--id]
~/.claude/skills/google-drive-manager/scripts/gdrive file delete FILE [--id]
~/.claude/skills/google-drive-manager/scripts/gdrive file download FILE [LOCAL_FOLDER] [--id] [--overwrite]
~/.claude/skills/google-drive-manager/scripts/gdrive file info FILE [--id]
~/.claude/skills/google-drive-manager/scripts/gdrive file move FILE TARGET_FOLDER [--id]
~/.claude/skills/google-drive-manager/scripts/gdrive file rename FILE NEW_NAME [--id]
~/.claude/skills/google-drive-manager/scripts/gdrive file upload LOCAL_FILE REMOTE_FOLDER [--id]
~/.claude/skills/google-drive-manager/scripts/gdrive file share FILE EMAIL [--role ROLE] [--id] [--no-notify] [--message MSG]
~/.claude/skills/google-drive-manager/scripts/gdrive file share-public FILE [--role ROLE] [--id]
~/.claude/skills/google-drive-manager/scripts/gdrive file permissions FILE [--id]
~/.claude/skills/google-drive-manager/scripts/gdrive file remove-permission FILE PERMISSION_ID [--id]
~/.claude/skills/google-drive-manager/scripts/gdrive file remove-public FILE [--id]

# Folder operations
~/.claude/skills/google-drive-manager/scripts/gdrive folder create FOLDER_PATH
~/.claude/skills/google-drive-manager/scripts/gdrive folder list FOLDER [--id]
~/.claude/skills/google-drive-manager/scripts/gdrive folder upload LOCAL_DIR REMOTE_FOLDER [--id]
~/.claude/skills/google-drive-manager/scripts/gdrive folder download FOLDER LOCAL_FOLDER [--id] [--overwrite] [--new-only] [--parallel N]
```

**CRITICAL: The `--id` Flag**

When working with file or folder IDs (instead of paths), you **MUST** use the `--id` flag:

```bash
# CORRECT - Using file ID with --id flag
~/.claude/skills/google-drive-manager/scripts/gdrive file info 1iAinUz-fQB0G-juO3khaWxmxK-3EbPRq --id

# INCORRECT - Using file ID without --id flag (will fail)
~/.claude/skills/google-drive-manager/scripts/gdrive file info 1iAinUz-fQB0G-juO3khaWxmxK-3EbPRq

# When using paths, do NOT use --id flag
~/.claude/skills/google-drive-manager/scripts/gdrive file info "My Drive/Documents/file.pdf"
```

**When to use `--id` flag:**
- When the FILE, FOLDER, or TARGET_FOLDER parameter is a Drive ID (e.g., `1iAinUz-fQB0G-juO3khaWxmxK-3EbPRq`)
- IDs are returned by search commands and file info
- For `move` and `copy` with `--parent`, use `--id` if both source AND destination are IDs

**When NOT to use `--id` flag:**
- When using file/folder paths (e.g., `My Drive/Documents/file.pdf`)
- When using relative paths

**Path Format:**
- Paths use forward slashes: `My Drive/Documents/Reports`
- File IDs also work: `1abc123xyz`
- All paths are resolved automatically

**Examples:**
```bash
# Search for files
~/.claude/skills/google-drive-manager/scripts/gdrive search "Q4 Report"
~/.claude/skills/google-drive-manager/scripts/gdrive search "budget 2024" --max 20
~/.claude/skills/google-drive-manager/scripts/gdrive search Passeport --type image,pdf
~/.claude/skills/google-drive-manager/scripts/gdrive search "My Project" --type folder

# Upload and download (by path)
~/.claude/skills/google-drive-manager/scripts/gdrive file upload document.pdf "My Drive/Documents"
~/.claude/skills/google-drive-manager/scripts/gdrive file download "My Drive/Reports/Q4.pdf" ~/Downloads/

# Upload and download (by ID)
~/.claude/skills/google-drive-manager/scripts/gdrive file upload document.pdf 1abc123xyz --id
~/.claude/skills/google-drive-manager/scripts/gdrive file download 1abc123xyz ~/Downloads/ --id

# Copy and move (by path)
~/.claude/skills/google-drive-manager/scripts/gdrive file copy "My Drive/Report.pdf" "Report Copy.pdf"
~/.claude/skills/google-drive-manager/scripts/gdrive file copy "Report.pdf" --parent "My Drive/Archive"
~/.claude/skills/google-drive-manager/scripts/gdrive file move "Report.pdf" "My Drive/Documents"

# Copy and move (by ID)
~/.claude/skills/google-drive-manager/scripts/gdrive file copy 1abc123xyz "Report Copy.pdf" --id
~/.claude/skills/google-drive-manager/scripts/gdrive file copy 1abc123xyz --parent 1xyz789 --id
~/.claude/skills/google-drive-manager/scripts/gdrive file move 1abc123xyz 1xyz789 --id

# Folder operations (by path)
~/.claude/skills/google-drive-manager/scripts/gdrive folder create "My Drive/Projects/2024/Q4"
~/.claude/skills/google-drive-manager/scripts/gdrive folder list "My Drive/Documents"
~/.claude/skills/google-drive-manager/scripts/gdrive folder upload ~/projects/myapp "My Drive/Backups"

# Folder operations (by ID)
~/.claude/skills/google-drive-manager/scripts/gdrive folder list 138RciDLCoBxQBOxijPfnYwih-qOI2p1d --id
~/.claude/skills/google-drive-manager/scripts/gdrive folder upload ~/projects/myapp 1abc123xyz --id
~/.claude/skills/google-drive-manager/scripts/gdrive folder download 1abc123xyz ~/Downloads/ --id

# Permissions (by path)
~/.claude/skills/google-drive-manager/scripts/gdrive file share "Report.pdf" user@example.com --role writer
~/.claude/skills/google-drive-manager/scripts/gdrive file share-public "Presentation.pptx" --role reader
~/.claude/skills/google-drive-manager/scripts/gdrive file permissions "Report.pdf"
~/.claude/skills/google-drive-manager/scripts/gdrive file remove-public "Report.pdf"

# Permissions (by ID)
~/.claude/skills/google-drive-manager/scripts/gdrive file share 1abc123xyz user@example.com --role writer --id
~/.claude/skills/google-drive-manager/scripts/gdrive file share-public 1abc123xyz --role reader --id
~/.claude/skills/google-drive-manager/scripts/gdrive file permissions 1abc123xyz --id
~/.claude/skills/google-drive-manager/scripts/gdrive file remove-public 1abc123xyz --id
```

**How It Works:**
- Pure Go binary with no dependencies
- Uses OAuth2 for authentication
- Credentials stored at `~/.credentials/google_credentials.json`
- Token cached at `~/.credentials/google_token.json`
- Fast and lightweight

**Operations:**

1. **Search**: Find files by name or type with filters (supports shortcuts: image, audio, video, prez, doc, spreadsheet, txt, pdf, folder)
2. **File Upload**: Upload local files to Drive with optional parent folder
3. **File Download**: Download files from Drive (auto-converts Google Workspace files)
4. **File Copy**: Create copies with optional renaming and destination folder
5. **File Move**: Move files between folders
6. **File Rename**: Rename files without moving them
7. **File Delete**: Delete files or folders
8. **File Info**: Get detailed metadata including path, size, type, owners
9. **File Share**: Share with specific users (reader/writer/commenter roles)
10. **Share Public**: Make files accessible to anyone with the link
11. **Permissions**: List all permissions on a file
12. **Remove Permission**: Remove specific permission by ID
13. **Remove Public**: Remove public access
14. **Folder Create**: Create folder paths (like mkdir -p)
15. **Folder List**: List folder contents
16. **Folder Upload**: Upload entire directories recursively
17. **Folder Download**: Download entire folders recursively

## Prerequisites

### System Requirements
- **GCP Project** with Drive API enabled
- **Google OAuth Credentials** stored in `~/.credentials/`
- **gdrive binary** (pre-compiled, included in scripts folder)

### Google Cloud Setup

1. **Enable Drive API:**
   ```bash
   gcloud services enable drive.googleapis.com
   ```

2. **Create OAuth Credentials:**
   - Go to Google Cloud Console (https://console.cloud.google.com/)
   - Navigate to APIs & Services > Credentials
   - Create OAuth 2.0 Client ID (Desktop application type)
   - Download credentials as JSON file
   - Save to `~/.credentials/google_credentials.json`

3. **First-time Authentication:**
   ```bash
   # Create credentials directory
   mkdir -p ~/.credentials

   # Copy downloaded credentials
   cp ~/Downloads/client_secret_*.json ~/.credentials/google_credentials.json

   # Run any command - will open browser for OAuth consent
   ~/.claude/skills/google-drive-manager/scripts/gdrive search test

   # Token saved to ~/.credentials/google_token.json for future use
   ```

4. **Subsequent Runs:**
   - Token automatically refreshed when expired
   - No browser interaction needed
   - Seamless authentication

### Installation
**No installation required!** The gdrive binary is:
- Pre-compiled and ready to use
- Standalone with no dependencies
- Fast and lightweight
- Cross-platform compatible

## Common Workflows

### 1. Search for Files

```bash
# Search by name
~/.claude/skills/google-drive-manager/scripts/gdrive search "Q4 Report"

# Search with type filter
~/.claude/skills/google-drive-manager/scripts/gdrive search report --type pdf

# Search with max results
~/.claude/skills/google-drive-manager/scripts/gdrive search "budget 2024" --max 20

# Search for multiple types
~/.claude/skills/google-drive-manager/scripts/gdrive search contract --type doc,pdf
```

**Output:**
```
Searching for: Q4 Report

📄 Q4 Report Final
   ID: 1abc123xyz
   Type: application/pdf
   Modified: 2024-12-15

📄 Q4 Report Draft
   ID: 1def456uvw
   Type: application/vnd.google-apps.document
   Modified: 2024-12-14
```

### 2. Upload Files

```bash
# Upload to root
~/.claude/skills/google-drive-manager/scripts/gdrive file upload report.pdf "My Drive"

# Upload to specific folder (by path)
~/.claude/skills/google-drive-manager/scripts/gdrive file upload report.pdf "My Drive/Documents"

# Upload to specific folder (by ID)
~/.claude/skills/google-drive-manager/scripts/gdrive file upload report.pdf 1abc123xyz --id

# Upload entire folder (by path)
~/.claude/skills/google-drive-manager/scripts/gdrive folder upload ~/myproject "My Drive/Backups"

# Upload entire folder (by ID)
~/.claude/skills/google-drive-manager/scripts/gdrive folder upload ~/myproject 1abc123xyz --id
```

### 3. Download Files

```bash
# Download by path to current directory
~/.claude/skills/google-drive-manager/scripts/gdrive file download "My Drive/Reports/Q4.pdf"

# Download by path to specific location
~/.claude/skills/google-drive-manager/scripts/gdrive file download "My Drive/Reports/Q4.pdf" ~/Downloads/

# Download by ID
~/.claude/skills/google-drive-manager/scripts/gdrive file download 1abc123xyz ~/Downloads/ --id

# Download entire folder (by path)
~/.claude/skills/google-drive-manager/scripts/gdrive folder download "My Drive/Projects/MyApp" ~/Downloads/

# Download entire folder (by ID)
~/.claude/skills/google-drive-manager/scripts/gdrive folder download 1abc123xyz ~/Downloads/ --id
```

### 4. Copy Files

```bash
# Copy with new name (by path)
~/.claude/skills/google-drive-manager/scripts/gdrive file copy "Report.pdf" "Report Copy.pdf"

# Copy with new name (by ID)
~/.claude/skills/google-drive-manager/scripts/gdrive file copy 1abc123xyz "Report Copy.pdf" --id

# Copy to different folder (by path)
~/.claude/skills/google-drive-manager/scripts/gdrive file copy "Report.pdf" --parent "My Drive/Archive"

# Copy to different folder (by ID)
~/.claude/skills/google-drive-manager/scripts/gdrive file copy 1abc123xyz --parent 1xyz789 --id

# Copy with both new name and location (by path)
~/.claude/skills/google-drive-manager/scripts/gdrive file copy "My Drive/Report.pdf" "Q4 Report Copy.pdf" --parent "My Drive/Archive"

# Copy with both new name and location (by ID)
~/.claude/skills/google-drive-manager/scripts/gdrive file copy 1abc123xyz "Q4 Report Copy.pdf" --parent 1xyz789 --id
```

### 5. Move and Rename Files

```bash
# Move file to folder (by path)
~/.claude/skills/google-drive-manager/scripts/gdrive file move "Report.pdf" "My Drive/Documents"

# Move file to folder (by ID)
~/.claude/skills/google-drive-manager/scripts/gdrive file move 1abc123xyz 1xyz789 --id

# Rename file (by path)
~/.claude/skills/google-drive-manager/scripts/gdrive file rename "Report.pdf" "Final Report.pdf"

# Rename file (by ID)
~/.claude/skills/google-drive-manager/scripts/gdrive file rename 1abc123xyz "Final Report.pdf" --id
```

### 6. Share Files

```bash
# Share as reader (default) - by path
~/.claude/skills/google-drive-manager/scripts/gdrive file share "Report.pdf" user@example.com

# Share as reader (default) - by ID
~/.claude/skills/google-drive-manager/scripts/gdrive file share 1abc123xyz user@example.com --id

# Share as writer - by path
~/.claude/skills/google-drive-manager/scripts/gdrive file share "Report.pdf" user@example.com --role writer

# Share as writer - by ID
~/.claude/skills/google-drive-manager/scripts/gdrive file share 1abc123xyz user@example.com --role writer --id

# Share as commenter - by path
~/.claude/skills/google-drive-manager/scripts/gdrive file share "Report.pdf" user@example.com --role commenter

# Share as commenter - by ID
~/.claude/skills/google-drive-manager/scripts/gdrive file share 1abc123xyz user@example.com --role commenter --id
```

### 7. Manage File Permissions

```bash
# List all permissions for a file (by path)
~/.claude/skills/google-drive-manager/scripts/gdrive file permissions "Report.pdf"

# List all permissions for a file (by ID)
~/.claude/skills/google-drive-manager/scripts/gdrive file permissions 1abc123xyz --id
```

**Output:**
```
Permissions for: Report.pdf

🌐 Anyone with the link - reader
   ID: anyoneWithLink

👤 john@example.com - writer
   ID: 12345678901234567890

👤 owner@example.com - owner
   ID: 11111111111111111111
```

**Share with anyone (make public):**
```bash
# Reader access (default) - by path
~/.claude/skills/google-drive-manager/scripts/gdrive file share-public "Report.pdf"

# Reader access (default) - by ID
~/.claude/skills/google-drive-manager/scripts/gdrive file share-public 1abc123xyz --id

# Writer access - by path
~/.claude/skills/google-drive-manager/scripts/gdrive file share-public "Report.pdf" --role writer

# Writer access - by ID
~/.claude/skills/google-drive-manager/scripts/gdrive file share-public 1abc123xyz --role writer --id
```

**Remove public access:**
```bash
# By path
~/.claude/skills/google-drive-manager/scripts/gdrive file remove-public "Report.pdf"

# By ID
~/.claude/skills/google-drive-manager/scripts/gdrive file remove-public 1abc123xyz --id
```

**Remove specific permission:**
```bash
# First, list permissions to get the permission ID (by path)
~/.claude/skills/google-drive-manager/scripts/gdrive file permissions "Report.pdf"

# Then remove the specific permission using its ID (by path)
~/.claude/skills/google-drive-manager/scripts/gdrive file remove-permission "Report.pdf" 12345678901234567890

# Or by file ID
~/.claude/skills/google-drive-manager/scripts/gdrive file permissions 1abc123xyz --id
~/.claude/skills/google-drive-manager/scripts/gdrive file remove-permission 1abc123xyz 12345678901234567890 --id
```

## Best Practices

### Using File/Folder IDs vs Paths
- **ALWAYS use --id flag with IDs:** When using file or folder IDs, you MUST include the `--id` flag
- **Paths don't need --id:** When using paths like `My Drive/Documents/file.pdf`, do NOT use `--id`
- **Get IDs from search:** Use search commands to find file IDs
- **IDs are more reliable:** IDs work even if files are renamed or moved
- **Paths are more readable:** Paths are easier to understand but can break if files move

### File Search
- **Use type filters:** Use shortcuts (image, pdf, doc, folder) for faster filtering
- **Limit results:** Use --max to control the number of results (default 50)
- **Specific queries:** More specific search terms return better results
- **Multiple types:** Combine types with commas: `--type pdf,doc`

### File Upload/Download
- **Use paths:** Paths are easier to read than file IDs
- **Parent folders:** Organize uploads with --parent flag
- **Folder operations:** Use folder upload/download for entire directories
- **Auto-convert:** Google Workspace files automatically convert on download

### File Management
- **Search first:** Find files with search before operating on them
- **Use info:** Get detailed file information including full path
- **Verify deletes:** Check file info before deleting
- **Paths vs IDs:** Both work, but paths are more readable

### Permission Management
- **List first:** Check current permissions before making changes
- **Permission IDs:** Note the ID when removing specific access
- **Public access:** Be careful with share-public - anyone with link can access
- **Role selection:** Choose appropriate role (reader/writer/commenter)

### Performance
- **Binary speed:** Go binary is fast and lightweight
- **No dependencies:** No Python or package installation needed
- **Token caching:** Authentication tokens are cached and auto-refreshed
- **API quotas:** Be mindful of Google Drive API quotas for high-volume operations

## How to Respond to Drive Requests

When users request Drive operations:

1. **Identify the operation:**
   - Search, upload, download, copy, move, share, delete, info, permissions, remove-permission, share-anyone, or remove-public

2. **Gather required parameters:**
   - File IDs (from search or provided by user)
   - File paths (for upload/download)
   - Folder IDs (for move/parent operations)
   - Email addresses (for sharing)

3. **Run the appropriate command:**
   - Execute the script with proper arguments
   - Monitor output for progress and errors
   - Report results to user

4. **Handle file IDs:**
   - If user doesn't provide file ID, search first
   - Extract ID from Drive URLs if provided
   - Confirm file details before destructive operations

5. **Handle errors:**
   - Check authentication if OAuth errors occur
   - Verify file IDs if not found
   - Confirm API access if permission errors occur

## Example Interactions

### Example 1: Search and Download

**User:** "Find the Q4 report PDF and download it"

**Response:**
```
I'll search for the Q4 report PDF in your Google Drive.
```

**Execute:**
```bash
~/.claude/skills/google-drive-manager/scripts/gdrive search "Q4 report" --type pdf
```

**Report results:**
```
Found: Q4 Report Final.pdf (ID: 1abc123xyz)

Downloading...
```

**Execute:**
```bash
~/.claude/skills/google-drive-manager/scripts/gdrive file download 1abc123xyz ~/Downloads/ --id
```

**Final response:**
```
✅ Downloaded Q4 Report Final.pdf to ~/Downloads/q4_report.pdf
```

### Example 2: Upload and Share

**User:** "Upload presentation.pptx and share it with team@example.com as editor"

**Response:**
```
I'll upload presentation.pptx to Google Drive and share it with team@example.com.
```

**Execute:**
```bash
~/.claude/skills/google-drive-manager/scripts/gdrive file upload presentation.pptx "My Drive"
```

**Then share (using the file path):**
```bash
~/.claude/skills/google-drive-manager/scripts/gdrive file share "presentation.pptx" team@example.com --role writer
```

**Or if you have the file ID from search/upload output:**
```bash
~/.claude/skills/google-drive-manager/scripts/gdrive file share 1abc123xyz team@example.com --role writer --id
```

**Final response:**
```
✅ Uploaded presentation.pptx
✅ Shared with team@example.com as editor
```

### Example 3: Find File Location

**User:** "Where is 'La révolution française' located in my Drive?"

**Response:**
```
I'll search for the file and show you its location.
```

**Execute:**
```bash
~/.claude/skills/google-drive-manager/scripts/gdrive search "révolution" --type doc
```

**Report results:**
```
Found: La révolution française et l'empire de 1729-1815

Getting details...
```

**Execute:**
```bash
~/.claude/skills/google-drive-manager/scripts/gdrive file info 10JCVDuzryv3n2jnFpQHaGUrATGVe8MTX0QKfbHId7Z8 --id
```

**Final response:**
```
File: La révolution française et l'empire de 1729-1815
Type: Google Docs
Path: Shared with me / La révolution française et l'empire de 1729-1815
Owner: morand.amira

This file is shared with you by morand.amira.
```

### Example 4: Manage File Permissions

**User:** "Make my presentation public so anyone can view it, then show me who has access"

**Response:**
```
I'll make your presentation accessible to anyone with the link.
```

**Execute:**
```bash
~/.claude/skills/google-drive-manager/scripts/gdrive search presentation --type prez --max 5
```

**Report results:**
```
Found: presentation.pptx

Making it public...
```

**Execute (by path):**
```bash
~/.claude/skills/google-drive-manager/scripts/gdrive file share-public "presentation.pptx" --role reader
```

**Or by ID:**
```bash
~/.claude/skills/google-drive-manager/scripts/gdrive file share-public 1abc123xyz --role reader --id
```

**Then list permissions (by path):**
```bash
~/.claude/skills/google-drive-manager/scripts/gdrive file permissions "presentation.pptx"
```

**Or by ID:**
```bash
~/.claude/skills/google-drive-manager/scripts/gdrive file permissions 1abc123xyz --id
```

**Final response:**
```
✅ File is now public!

Permissions:
🌐 Anyone with the link - reader
👤 owner@example.com - owner

Anyone with the link can now view your presentation.
```

**User follow-up:** "Actually, remove the public access"

**Execute (by path):**
```bash
~/.claude/skills/google-drive-manager/scripts/gdrive file remove-public "presentation.pptx"
```

**Or by ID:**
```bash
~/.claude/skills/google-drive-manager/scripts/gdrive file remove-public 1abc123xyz --id
```

**Response:**
```
✅ Public access removed! The file is now private.
```

## Troubleshooting

### "Google OAuth credentials not found"
```bash
# Create credentials directory
mkdir -p ~/.credentials

# Download OAuth credentials from Google Cloud Console
# Save to ~/.credentials/google_credentials.json
```

The binary will provide instructions if credentials are missing.

### "Permission denied" errors
```bash
# Ensure Drive API is enabled
gcloud services enable drive.googleapis.com

# Verify OAuth scopes in credentials
# OAuth client should be configured for Desktop application type
```

### "File not found"
- Verify file path or ID is correct
- Try searching for the file first
- Ensure you have access to the file
- Check that file is not deleted or in trash

### "Insufficient permissions" when managing permissions
- You can only manage permissions on files you own
- Files shared with you cannot have their permissions modified
- Contact the file owner if you need to change permissions

### "Quota exceeded"
- Check Google Cloud Console for quota limits
- Consider requesting quota increase for high-volume operations
- Implement delays between batch operations

### Re-authenticate
```bash
# Delete token to trigger new OAuth flow
rm ~/.credentials/google_token.json

# Run any command to re-authenticate
~/.claude/skills/google-drive-manager/scripts/gdrive search test
```

### Binary execution issues
```bash
# Ensure binary has execute permissions
chmod +x ~/.claude/skills/google-drive-manager/scripts/gdrive

# Check binary works
~/.claude/skills/google-drive-manager/scripts/gdrive --help
```

## Technical Details

### Type Shortcuts

The binary supports convenient type shortcuts:
- `image` - All image types (JPEG, PNG, GIF, etc.)
- `audio` - Audio files
- `video` - Video files
- `prez` - Presentations (Google Slides, PowerPoint)
- `doc` - Documents (Google Docs, Word)
- `spreadsheet` - Spreadsheets (Google Sheets, Excel)
- `txt` - Text files
- `pdf` - PDF files
- `folder` - Folders

You can also use explicit MIME types like `image/jpeg`, `application/pdf`.

### Path Resolution

The binary automatically resolves paths:
- `My Drive/Documents/Report.pdf` - Full path
- `Documents/Report.pdf` - Relative to My Drive
- `1abc123xyz` - Direct file ID
- Supports both forward slashes and spaces in names

### Smart Export

When downloading Google Workspace files, automatic conversion:
- Google Docs → PDF
- Google Sheets → XLSX
- Google Slides → PPTX

### Permission Roles

Available roles for sharing:
- `reader` - Can view and download
- `writer` - Can edit
- `commenter` - Can comment but not edit
- `owner` - Full control (transfer ownership)

## Security & Privacy

- **OAuth authentication:** Secure OAuth 2.0 flow
- **Local credentials:** Stored in `~/.credentials/`
- **Token caching:** Automatic refresh when expired
- **No data storage:** Binary doesn't log or store file content
- **HTTPS:** All API calls use secure HTTPS

## Dependencies

**None!** The gdrive binary is:
- Standalone executable
- No runtime dependencies
- No Python, Node.js, or other runtimes needed
- Built with Go for maximum portability

## Response Approach

To accomplish Drive management tasks:

1. Identify the specific operation requested
2. Gather required parameters (file IDs, paths, etc.)
3. Search for files if IDs not provided
4. Execute the appropriate command
5. Monitor output for progress and errors
6. Report results with relevant file information
7. Handle errors with appropriate troubleshooting steps
