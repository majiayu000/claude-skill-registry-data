---
name: markdown-confluence-sync
description: Sync markdown projects to Confluence using the markdown_confluence tool. Use for publishing, crawling, and managing Confluence pages from local markdown files.
---

# Markdown Confluence Sync

Synchronize local markdown projects with Confluence using the `markdown-confluence` CLI tool.

## Tool Location

```bash
/Users/tylerstapler/Documents/personal-wiki/tools/markdown_confluence/.venv/bin/markdown-confluence
```

## Quick Reference

### Environment Variables (Required for Authentication)

```bash
export CONFLUENCE_BASE_URL="https://betfanatics.atlassian.net"
export ATLASSIAN_USER_NAME="tyler.stapler@betfanatics.com"
# ATLASSIAN_API_TOKEN must be set (retrieved from keychain/secrets)
```

### Core Commands

| Command | Purpose |
|---------|---------|
| `publish` | Upload markdown to Confluence |
| `crawl page` | Download a single Confluence page |
| `crawl page-tree` | Download page and descendants |
| `handle-deleted` | Manage deleted local files |
| `validate-links` | Check broken links |

## Publishing Workflow

### 1. Setup Configuration

Create `.markdown-confluence.json` in your project:

```json
{
  "confluence": {
    "base_url": "https://betfanatics.atlassian.net",
    "parent_id": "PARENT_PAGE_ID",
    "username": "tyler.stapler@betfanatics.com"
  },
  "publish": {
    "folder_to_publish": ".",
    "frontmatter_from_document_start": true,
    "resolve_relative_links": true,
    "respect_link_dependencies": true
  }
}
```

### 2. Add Frontmatter to Markdown Files

```markdown
---
connie-title: "Custom Page Title"
connie-page-id: "123456"        # Existing page ID (auto-added after first publish)
connie-parent-id: "789012"      # Override parent page
connie-publish: true            # Set false to skip
---

# Your Content Here
```

### 3. Publish Commands

```bash
# Always dry-run first
CONFLUENCE_BASE_URL="https://betfanatics.atlassian.net" \
ATLASSIAN_USER_NAME="tyler.stapler@betfanatics.com" \
/Users/tylerstapler/Documents/personal-wiki/tools/markdown_confluence/.venv/bin/markdown-confluence \
publish . --config .markdown-confluence.json --dry-run --verbose

# Actual publish
/Users/tylerstapler/Documents/personal-wiki/tools/markdown_confluence/.venv/bin/markdown-confluence \
publish . --config .markdown-confluence.json --verbose

# Force update unchanged content
publish . --config .markdown-confluence.json --force

# Stop on first error
publish . --config .markdown-confluence.json --fail-fast
```

## Crawling Confluence

### Download Single Page

```bash
CONFLUENCE_BASE_URL="https://betfanatics.atlassian.net" \
ATLASSIAN_USER_NAME="tyler.stapler@betfanatics.com" \
/Users/tylerstapler/Documents/personal-wiki/tools/markdown_confluence/.venv/bin/markdown-confluence \
crawl page PAGE_ID_OR_URL --output ./output_dir --verbose
```

### Download Page Tree

```bash
markdown-confluence crawl page-tree PAGE_ID --output ./output_dir --max-depth 3 --verbose
```

## Key Publish Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Preview without publishing |
| `--verbose` / `-v` | Increase output detail |
| `--force` | Force update unchanged pages |
| `--fail-fast` | Stop on first error |
| `--delete-archived` | Delete archived pages |
| `--force-hierarchy` | Use directory structure for hierarchy |
| `--update-frontmatter` | Update frontmatter with corrected IDs |
| `--pattern "**/*.md"` | Filter files to publish |
| `--exclude "**/draft/**"` | Exclude patterns |

## Frontmatter Fields

| Field | Purpose |
|-------|---------|
| `connie-title` | Custom page title |
| `connie-page-id` | Existing page ID (for updates) |
| `connie-parent-id` | Parent page ID |
| `connie-parent-page-id` | Alternative parent field |
| `connie-publish` | Enable/disable publishing |
| `connie-skip-link-resolution` | Skip link resolution |

## Common Workflows

### New Project Setup

1. Create project directory with markdown files
2. Create `.markdown-confluence.json` with parent page ID
3. Run `--dry-run` to verify structure
4. Publish - frontmatter will be auto-updated with page IDs

### Update Existing Project

1. Edit markdown files
2. Run publish (tool detects changes via hashing)
3. Use `--force` if content unchanged but needs update

### Troubleshooting

- **400 Bad Request**: Parent page may have corrupted format
- **Duplicate title**: Add unique `connie-title` in frontmatter
- **Page not found**: Page ID invalid, tool will auto-create new page
- **Archived pages**: Use `--delete-archived` to recreate

## Features

- Mermaid diagram rendering
- Wikilink support (`[[page]]` and `[[page|title]]`)
- Relative link resolution between markdown files
- Directory hierarchy to page hierarchy mapping
- Asset/image handling
- Content hashing for efficient updates
