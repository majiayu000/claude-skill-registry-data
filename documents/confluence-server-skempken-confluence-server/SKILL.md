---
name: confluence-server
description: This skill enables interaction with Confluence Server/Data Center REST API for documentation retrieval and knowledge management. Use when the user wants to read pages, search content, list spaces, or retrieve documentation from Confluence Server.
---

# Confluence Server

This skill provides tools for interacting with Confluence Server/Data Center's REST API, focusing on documentation retrieval and knowledge aggregation workflows.

## Prerequisites

The following environment variables must be set:

- `CONFLUENCE_URL` - Base URL of the Confluence Server instance (e.g., `https://confluence.example.com`)
- `CONFLUENCE_USER` - Username for authentication
- `CONFLUENCE_TOKEN` - Personal access token for authentication

## Available Commands

The `scripts/confluence_api.py` script provides a CLI for Confluence Server operations. Execute it with Python 3:

```bash
python3 scripts/confluence_api.py <command> [options]
```

### Content Commands

| Command | Description |
|---------|-------------|
| `get-page` | Get a page by ID with content |
| `get-page-by-title` | Get a page by title and space key |
| `list-pages` | List pages in a space |
| `search` | Search content using CQL |
| `get-children` | Get child pages of a page |
| `get-attachments` | List attachments on a page |

### Space Commands

| Command | Description |
|---------|-------------|
| `list-spaces` | List all accessible spaces |
| `get-space` | Get space details |

## Command Usage Examples

### Get Page Content

```bash
# Get page by ID (storage format - XHTML)
python3 scripts/confluence_api.py get-page --page-id 12345

# Get page with rendered HTML view
python3 scripts/confluence_api.py get-page --page-id 12345 --body-format view

# Get page by title and space
python3 scripts/confluence_api.py get-page-by-title --space-key DEV --title "Architecture Overview"
```

### List Pages in Space

```bash
# List pages in a space (first 25)
python3 scripts/confluence_api.py list-pages --space-key DEV

# List pages with custom limit
python3 scripts/confluence_api.py list-pages --space-key DEV --limit 50

# List all pages in space (handles pagination)
python3 scripts/confluence_api.py list-pages --space-key DEV --all
```

### Search Content

```bash
# Search by text
python3 scripts/confluence_api.py search --cql "text ~ 'authentication'"

# Search in specific space
python3 scripts/confluence_api.py search --cql "space = DEV AND text ~ 'API'"

# Search by title
python3 scripts/confluence_api.py search --cql "title ~ 'Setup Guide'"

# Search recent pages (modified in last 7 days)
python3 scripts/confluence_api.py search --cql "type = page AND lastmodified > now('-7d')"

# Search with label
python3 scripts/confluence_api.py search --cql "label = 'architecture'"

# Get all search results
python3 scripts/confluence_api.py search --cql "space = DEV" --all
```

### Get Child Pages

```bash
# Get child pages
python3 scripts/confluence_api.py get-children --page-id 12345

# Get all children (paginated)
python3 scripts/confluence_api.py get-children --page-id 12345 --all
```

### Get Attachments

```bash
python3 scripts/confluence_api.py get-attachments --page-id 12345
```

### List Spaces

```bash
# List all spaces
python3 scripts/confluence_api.py list-spaces

# List only global spaces
python3 scripts/confluence_api.py list-spaces --type global

# List personal spaces
python3 scripts/confluence_api.py list-spaces --type personal
```

### Get Space Details

```bash
python3 scripts/confluence_api.py get-space --space-key DEV
```

## Workflow Guidelines

### Retrieving Documentation

1. Use `list-spaces` to find available documentation spaces
2. Use `list-pages` or `search` to locate specific pages
3. Use `get-page` to retrieve full content
4. Use `get-children` to navigate page hierarchies

### Knowledge Aggregation

1. Use `search` with CQL to find related content across spaces
2. Retrieve multiple pages to aggregate information
3. Use labels in CQL queries for categorized content

### Finding Specific Information

1. Start with a broad CQL search: `text ~ 'keyword'`
2. Narrow down by space: `space = KEY AND text ~ 'keyword'`
3. Retrieve full page content for detailed reading

## CQL Quick Reference

Common CQL patterns:

| Pattern | Description |
|---------|-------------|
| `space = KEY` | Content in specific space |
| `type = page` | Only pages (not blogs, comments) |
| `title ~ "text"` | Title contains text |
| `text ~ "query"` | Full-text search |
| `label = "label"` | Content with specific label |
| `creator = "user"` | Created by user |
| `lastmodified > now('-7d')` | Modified in last 7 days |
| `ancestor = 12345` | Pages under specific parent |

Combine with `AND`, `OR`:
```
space = DEV AND type = page AND text ~ 'API'
```

## Body Formats

| Format | Description |
|--------|-------------|
| `storage` | XHTML storage format (default, for programmatic use) |
| `view` | Rendered HTML (human-readable) |
| `export_view` | Export-ready HTML |
| `styled_view` | Styled HTML with CSS |

## Error Handling

Common errors:

- Missing environment variables: Ensure `CONFLUENCE_URL`, `CONFLUENCE_USER`, and `CONFLUENCE_TOKEN` are set
- Authentication failed: Verify credentials and token permissions
- Page not found: Check page ID or space/title combination
- Permission denied: User lacks access to the content

## Additional Reference

For detailed API documentation, see `references/api_endpoints.md`.
For CQL query reference, see `references/cql_reference.md`.
