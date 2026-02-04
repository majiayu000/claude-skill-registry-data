---
name: gcmd
description: Export and access Google Drive files (docs, sheets, meeting notes)
---

# Google Drive CLI (gcmd) Skill

Quick reference for using `gcmd` CLI tool to work with Google Drive files.

**Repository:** `/Users/ben/git/gcmd`

## Overview

`gcmd` is a Python CLI tool for working with Google Drive from the command line. Useful for:
- Exporting Google Docs as markdown for processing/archival
- Listing and searching Drive files
- Downloading files
- Viewing file metadata, permissions, and comments
- Reviewing document feedback and collaboration

## When to Use This Skill

Use this skill when:
- User asks to export Google Docs as markdown
- User provides a Google Drive URL and wants to read/access the content
- User asks to search for files in Google Drive
- User wants to view file permissions or comments on Google Docs
- User mentions "meeting notes" or "Gemini notes" from Google Meet
- User asks to list recent Google Drive files

## Common Commands

All commands must be run from the gcmd directory with `uv run gcmd`.

### Export Google Docs as Markdown

**RECOMMENDED: Export to /tmp/ for easy reading by Claude Code**

```bash
cd /Users/ben/git/gcmd
uv run gcmd export "https://docs.google.com/document/d/FILE_ID/edit" -o /tmp/
# Creates: /tmp/Document Title.md (uses document title as filename)
```

**Export to specific file path:**
```bash
uv run gcmd export FILE_ID -o /tmp/meeting-notes.md
# Creates: /tmp/meeting-notes.md
```

**Export all tabs as separate files:**
```bash
uv run gcmd export --all-tabs FILE_ID -o /tmp/
# Creates: /tmp/Document Title - Tab1.md, /tmp/Document Title - Tab2.md, etc.
```

**How `-o` works:**
- **Without `-o`**: Saves to `/Users/ben/git/gcmd/` using document title + `.exported.md`
- **With `-o /tmp/`** (directory): Saves to `/tmp/` using document title + `.md` extension (no `.exported`)
- **With `-o /tmp/file.md`** (file): Saves to exact path `/tmp/file.md`

After exporting, ALWAYS read the file to provide the user with the content.

### List and Search Files

```bash
cd /Users/ben/git/gcmd

# List recent files (default 20, sorted by modified date)
uv run gcmd list

# Search for files by name or content
uv run gcmd list -q "quarterly report"

# List only Google Docs
uv run gcmd list -t docs

# List with verbose details
uv run gcmd list -v -n 10

# List only folders
uv run gcmd list -t folders

# List Google Sheets
uv run gcmd list -t sheets
```

### View File Info

```bash
cd /Users/ben/git/gcmd

# Basic file metadata
uv run gcmd info "https://docs.google.com/document/d/FILE_ID/edit"

# Detailed info with permissions, tabs, structure, and comments
uv run gcmd info -v "https://docs.google.com/document/d/FILE_ID/edit"

# Show only comments (without other verbose details)
uv run gcmd info --show-comments "https://docs.google.com/document/d/FILE_ID/edit"

# Also works with just file ID
uv run gcmd info FILE_ID -v
```

**Detailed info shows:**
- File metadata (name, type, size, dates)
- Owner and last modifier
- All permissions (users, groups, domains, public links)
- Your capabilities (can edit, comment, share, download, etc.)
- Document tabs (for multi-tab Google Docs)
- Document outline with all headings
- **Comments and replies** with quoted text, authors, timestamps, and status (resolved/deleted)

### Download Files

```bash
cd /Users/ben/git/gcmd

# Download to current directory
uv run gcmd download FILE_ID

# Download to specific path
uv run gcmd download FILE_ID -o ~/Downloads/myfile.pdf

# Works with URLs
uv run gcmd download "https://drive.google.com/file/d/FILE_ID/view"
```

## URL Format Support

All commands accept multiple URL formats:

```bash
# Google Docs
https://docs.google.com/document/d/FILE_ID/edit
https://docs.google.com/document/d/FILE_ID/edit?tab=t.0

# Google Sheets
https://docs.google.com/spreadsheets/d/FILE_ID/edit

# Google Slides
https://docs.google.com/presentation/d/FILE_ID/edit

# Drive files
https://drive.google.com/file/d/FILE_ID/view

# Just the file ID
FILE_ID
```

## Workflow Example

When user provides a Google Drive URL:

1. **Export the document to /tmp/**:
   ```bash
   cd /Users/ben/git/gcmd
   uv run gcmd export "URL" -o /tmp/
   ```

2. **Read the exported file**:
   The file will be in `/tmp/` with the document title as filename.

3. **Provide the content to the user** or answer their questions about it.

4. **Optional cleanup**: After helping the user, you can delete the exported file:
   ```bash
   rm /tmp/exported-filename.md
   ```

## Common Workflow Examples

### Find and export a document

```bash
cd /Users/ben/git/gcmd

# Search for the document
uv run gcmd list -q "MCP Server Analysis" -t docs

# Get detailed info (tabs, structure)
uv run gcmd info -v "https://docs.google.com/document/d/FILE_ID/edit"

# Export all tabs to /tmp/ for easy reading
uv run gcmd export --all-tabs FILE_ID -o /tmp/
```

### Check permissions on shared docs

```bash
cd /Users/ben/git/gcmd

# View detailed permissions
uv run gcmd info -v FILE_ID

# Shows:
# - Who has access (users, groups, domains, public)
# - Permission levels (owner, writer, reader, commenter)
# - Your capabilities (can edit, share, download, etc.)
```

### Review document feedback

```bash
cd /Users/ben/git/gcmd

# View all comments and replies on a document
uv run gcmd info --show-comments "https://docs.google.com/document/d/FILE_ID/edit"

# Shows:
# - All comments with quoted/highlighted text
# - Authors and timestamps
# - Replies with their authors
# - Status (resolved, deleted)
# - Total comment count
```

### List recent work documents

```bash
cd /Users/ben/git/gcmd

# List recent Google Docs with details
uv run gcmd list -t docs -v -n 20
```

## Key Features

- **URL support**: All commands accept full Google Drive URLs or file IDs
- **Native markdown export**: Preserves formatting (headings, tables, links, bold, italic)
- **Multi-tab documents**: Use `--all-tabs` to export each tab separately
- **Detailed info**: View permissions, sharing, capabilities, document structure
- **Comments access**: View all comments and replies with quoted text, authors, and timestamps
- **Auto-naming**: Exported files use `.exported.md` extension (auto-ignored by git) when no `-o` specified

## Authentication

- **Credentials location**: `~/.config/gcmd/credentials.json`
- **Token location**: `~/.config/gcmd/token.json`

If authentication fails, delete token and re-authenticate:
```bash
rm ~/.config/gcmd/token.json
cd /Users/ben/git/gcmd
uv run gcmd list  # Will trigger new auth flow
```

## Important Notes

1. **Always use `/tmp/` for exports** - Makes files easy to find and read
2. **Always run from gcmd directory** - Commands require `cd /Users/ben/git/gcmd`
3. **Use `uv run gcmd`** - Not just `gcmd`
4. **Read exported files** - After exporting, read the file and provide content to user
5. **Clean up after** - Delete exported files from /tmp/ when done

## Troubleshooting

**"credentials.json not found"**: Follow setup steps to create OAuth credentials (see gcmd README)

**"Authentication failed"**: Delete token and re-authenticate:
```bash
rm ~/.config/gcmd/token.json
cd /Users/ben/git/gcmd
uv run gcmd list
```

**"Not a Google Doc"**: Use `download` command instead of `export` for non-Doc files

**Browser won't open**: The CLI will provide a manual URL to paste in your browser

## Tips

1. **Running commands:** Always use `uv run gcmd` from the gcmd directory
2. **Export location:** Always use `-o /tmp/` when exporting so files are in a predictable location for easy reading
3. **File naming:** Without `-o`, exported files use `.exported.md` extension (auto-ignored by git). With `-o /dir/`, uses `.md`
4. **Multi-tab documents:** Use `--all-tabs` to export each tab as a separate file
5. **Verbose mode:** Use `-v` for detailed information (permissions, structure, comments, etc.)
6. **Comments:** Use `--show-comments` to view just comments without other verbose details
7. **Search:** The `-q` flag searches both file names and content
