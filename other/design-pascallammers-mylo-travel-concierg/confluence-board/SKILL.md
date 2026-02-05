---
name: confluence-board
description: "Manage Confluence pages and spaces. Use when the user wants to: (1) List, create, update, or delete Confluence pages, (2) Search content across spaces, (3) View or manage spaces, (4) Read or update page content, (5) Manage page attachments. Requires environment variables CONFLUENCE_URL, CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN, and optionally CONFLUENCE_SPACES_FILTER."
---

# Confluence Page Management

Manage Confluence pages, spaces, and content via the Confluence REST API.

## Environment Variables

Required:
- `CONFLUENCE_URL`: Confluence instance URL (e.g., `https://company.atlassian.net/wiki`)
- `CONFLUENCE_USERNAME`: Confluence username/email
- `CONFLUENCE_API_TOKEN`: API token from https://id.atlassian.com/manage-profile/security/api-tokens

Optional:
- `CONFLUENCE_SPACES_FILTER`: Comma-separated space keys to filter by default (e.g., `DEV,DOCS`)

## Quick Start

Use `scripts/confluence_api.py` for all Confluence operations:

```bash
# List spaces
python scripts/confluence_api.py spaces

# List pages in a space
python scripts/confluence_api.py pages --space DEV

# Search for content
python scripts/confluence_api.py search "meeting notes"

# Get page details
python scripts/confluence_api.py get 12345

# Create a page
python scripts/confluence_api.py create DEV "My New Page" --body "Page content here"

# Update a page
python scripts/confluence_api.py update 12345 --title "New Title" --body "Updated content"
```

## Page Operations

### List Pages
```bash
python scripts/confluence_api.py pages [options]
  --space, -s      Space key(s), comma-separated
  --title, -t      Filter by title (contains)
  --label, -l      Filter by label
  --max            Max results (default: 50)
  --verbose, -v    Show detailed output
```

### Get Page Details
```bash
python scripts/confluence_api.py get PAGE_ID
python scripts/confluence_api.py get PAGE_ID --content  # Include body content
```

### Create Page
```bash
python scripts/confluence_api.py create SPACE "Title" [options]
  --body, -b       Page body content (plain text or HTML)
  --parent, -p     Parent page ID
  --labels, -l     Labels (space-separated)
```

### Update Page
```bash
python scripts/confluence_api.py update PAGE_ID [options]
  --title, -t      New title
  --body, -b       New body content
  --append, -a     Append to existing content instead of replacing
  --labels, -l     New labels
```

### Delete Page
```bash
python scripts/confluence_api.py delete PAGE_ID
```

### Add Comment
```bash
python scripts/confluence_api.py comment PAGE_ID "Comment text"
```

## Space Operations

### List Spaces
```bash
python scripts/confluence_api.py spaces [--type global|personal]
```

### Get Space Details
```bash
python scripts/confluence_api.py space SPACE_KEY
```

### List Space Pages
```bash
python scripts/confluence_api.py space-pages SPACE_KEY [-v]
```

## Search Operations

### Search Content
```bash
python scripts/confluence_api.py search "query" [options]
  --space, -s      Limit to space(s)
  --type, -t       Content type (page, blogpost, comment)
  --max            Max results (default: 25)
```

### Search with CQL
```bash
python scripts/confluence_api.py search --cql 'type=page AND space=DEV AND title~"meeting"'
```

## Label Operations

### Get Page Labels
```bash
python scripts/confluence_api.py labels PAGE_ID
```

### Add Labels
```bash
python scripts/confluence_api.py add-labels PAGE_ID label1 label2 label3
```

### Remove Label
```bash
python scripts/confluence_api.py remove-label PAGE_ID label_name
```

## Attachment Operations

### List Attachments
```bash
python scripts/confluence_api.py attachments PAGE_ID
```

### Download Attachment
```bash
python scripts/confluence_api.py download PAGE_ID "filename.pdf" --output ./downloads/
```

## Common Workflows

### Documentation Review
```bash
# Find all pages updated in the last week
python scripts/confluence_api.py search --cql 'type=page AND lastModified >= now("-7d")' -v

# Get specific page content
python scripts/confluence_api.py get 12345 --content
```

### Create Documentation
```bash
# Create a new page under a parent
python scripts/confluence_api.py create DEV "API Documentation" \
  --parent 12345 \
  --body "<h1>API Reference</h1><p>Documentation content...</p>" \
  --labels api documentation

# Update existing page
python scripts/confluence_api.py update 67890 --body "Updated content" --append
```

### Content Organization
```bash
# List all pages with a specific label
python scripts/confluence_api.py search --cql 'type=page AND label="meeting-notes"'

# Add labels to categorize pages
python scripts/confluence_api.py add-labels 12345 reviewed approved
```

## CQL Examples

Custom queries with `--cql`:

```bash
# Pages modified by current user
python scripts/confluence_api.py search --cql 'type=page AND contributor=currentUser()'

# Recently created pages
python scripts/confluence_api.py search --cql 'type=page AND created >= now("-30d") ORDER BY created DESC'

# Pages with specific label in space
python scripts/confluence_api.py search --cql 'type=page AND space=DEV AND label="important"'

# Full-text search
python scripts/confluence_api.py search --cql 'text~"deployment guide"'
```
