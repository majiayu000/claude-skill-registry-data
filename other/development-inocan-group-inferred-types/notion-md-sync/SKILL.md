---
name: notion-md-sync
description: Batch upload local Markdown files to Notion via Python script. Optimized for single or multiple files with zero token cost. Direct script execution bypasses LLM parsing, saving significant tokens on large files while preserving formatting (tables, code blocks, rich text).
---

# Notion Markdown Sync

## Purpose

Efficiently sync Markdown files to Notion pages, preserving formatting including tables, code blocks, bold text, links, and inline code. Optimized for batch operations with zero token cost.

## Why Use This Skill vs. notion-workspace

**Token Efficiency**: This skill uses a Python script that directly calls the Notion API, completely bypassing LLM token usage for file parsing and upload. For large Markdown files (many lines) or batch operations (single or multiple files), this can save thousands of tokens compared to using the `notion-workspace` skill's MCP tools, which require Claude to parse and process each file through the LLM.

**Performance**: Direct script execution is 10-100x faster than MCP tool chains.

**Use Cases**:
- ✅ Uploading single or multiple Markdown files at once
- ✅ Large documentation files (>500 lines)
- ✅ Automated pipelines and batch operations
- ✅ When you want zero token cost for the upload operation

**When to use `notion-workspace` instead**:
- Single page creation with custom properties/metadata
- Database queries and complex workspace operations
- Exploratory work requiring search and interaction
- Creating pages from non-Markdown sources

## When to Use This Skill

Invoke this skill when:
- Syncing single or multiple Markdown files to Notion in batch
- Uploading large documentation files (>500 lines) without token costs
- Automating Notion page creation from local Markdown files
- Converting technical documentation to Notion format efficiently

## Core Workflow

### For Batch Operations (Recommended)

Use the Python script in `scripts/sync_md_to_notion.py`:

1. **Set up Notion token** (first time only):
   ```bash
   export NOTION_TOKEN="ntn_your_token_here"
   ```
   See `references/setup.md` for detailed token setup instructions.

2. **Sync files**:
   ```bash
   # Auto-detect parent page (searches by content)
   python3 scripts/sync_md_to_notion.py report.md

   # Specify parent page ID
   python3 scripts/sync_md_to_notion.py --parent 2aee6057-c0cb-815b-ac5f-dd80e1c07d39 report.md

   # Multiple files to same parent
   python3 scripts/sync_md_to_notion.py -p <page-id> file1.md file2.md file3.md

   # All markdown files in directory
   python3 scripts/sync_md_to_notion.py *.md

   # View help and options
   python3 scripts/sync_md_to_notion.py --help
   ```

3. **Script features**:
   - Auto-finds parent pages by content search (when `--parent` not specified)
   - Accepts parent page ID via `--parent` or `-p` flag
   - Converts tables to Notion table blocks
   - Preserves code block syntax highlighting
   - Handles rich text formatting (bold, inline code, links)
   - Processes 100 blocks per request (chunked upload)

### For Single Files with Custom Handling

Use Notion MCP tools directly:
1. Search for parent page: `mcp__notion__API-post-search`
2. Create page: `mcp__notion__API-post-page`
3. Add content blocks: `mcp__notion__API-patch-block-children`

## Script Capabilities

The sync script converts these Markdown elements:

| Markdown | Notion Block Type | Notes |
|----------|------------------|-------|
| `# Heading` | heading_2 | H1 not supported, converted to H2 |
| `## Heading` | heading_2 | Direct conversion |
| `### Heading` | heading_3 | Direct conversion |
| `**bold**` | Rich text with bold annotation | Inline formatting |
| `` `code` `` | Rich text with code annotation | Inline code |
| `[text](url)` | Rich text with link | Clickable links |
| ` ```language\ncode\n``` ` | code block | Preserves language |
| Tables (`\| ... \|`) | table block | Full table structure |
| `- item` or `* item` | bulleted_list_item | Lists |
| `1. item` | bulleted_list_item | Numbered lists converted |

## Decision Guide

```
Need to sync Markdown to Notion?
│
├─ Multiple files
│  └─ Use: scripts/sync_md_to_notion.py
│     (Fast, efficient, no LLM token costs)
│
└─ Single file, quick upload?
   └─ Use: scripts/sync_md_to_notion.py
      (Still fastest even for single files)
```

## Configuration

### Token Setup

The script requires `NOTION_TOKEN` environment variable. See `references/setup.md` for complete setup instructions including:
- Creating Notion integration
- Getting API token
- Sharing pages with integration
- Security best practices

### Parent Page ID

The script supports multiple ways to specify the parent page:

**Option 1: CLI Argument (Recommended)**
```bash
python3 scripts/sync_md_to_notion.py --parent <page-id> file.md
# or short form
python3 scripts/sync_md_to_notion.py -p <page-id> file.md
```

**Option 2: Auto-Detection (Default)**
When `--parent` is not specified, the script searches for a parent page using the first 2 words of the filename.

**Option 3: Find Page ID via Notion MCP**
Use `mcp__notion__API-post-search` to find the page ID:
```
1. Search: mcp__notion__API-post-search with query "Your Page Name"
2. Extract page_id from results
3. Use with --parent flag
```

## Example Workflows

### Batch Documentation Upload

User request: "Upload all 20 markdown files from docs/ to Notion under 'Documentation' page"

Steps:
1. Find parent page ID:
   ```
   Use mcp__notion__API-post-search with query "Documentation"
   Extract page_id from results (e.g., "abc123-...")
   ```

2. Run batch sync with parent page:
   ```bash
   cd docs/
   python3 ~/.claude/skills/notion-md-sync/scripts/sync_md_to_notion.py \
     --parent abc123-def456-... *.md
   ```

### Technical Docs with Tables

User request: "Sync API docs with tables and code to 'API Documentation' page"

Steps:
1. Search for parent: `mcp__notion__API-post-search` with query "API Documentation"
2. Use the page ID with `--parent` flag:

```bash
python3 scripts/sync_md_to_notion.py \
  --parent 2aee6057-c0cb-815b-ac5f-dd80e1c07d39 \
  api-docs/*.md
```

The script automatically handles tables and code blocks. All markdown tables become Notion table blocks with proper structure.

### Quick Single File Upload

User request: "Upload this README.md to Notion"

```bash
# Let script auto-detect parent
python3 scripts/sync_md_to_notion.py README.md

# Or specify parent
python3 scripts/sync_md_to_notion.py -p <page-id> README.md
```

## Troubleshooting

### Token Not Set
**Error**: "NOTION_TOKEN environment variable is not set"
**Solution**: Set token via `export NOTION_TOKEN="ntn_..."` or see `references/setup.md`

### No Parent Page Found
**Error**: "No parent page found"
**Solution**:
- Use `--parent` flag to specify parent page ID explicitly
- Share target pages with integration (for auto-detection)
- Use `mcp__notion__API-post-search` to find the correct page ID

### Permission Denied
**Error**: HTTP 403 Forbidden
**Solution**: Share Notion pages with your integration via page settings → Connections

### Formatting Not Preserved
**Issue**: Bold text or links appear as plain text
**Solution**: Ensure using latest script version with `parse_rich_text()` function (line ~70)

## Performance

| Method | Speed | Token Cost | Best For |
|--------|-------|------------|----------|
| Python Script (this skill) | ⚡⚡⚡ Fast | **Zero** | Batch operations (single or multiple files), large files |
| notion-workspace MCP | ⚡⚡ Medium | **High** (1000+ tokens for large files) | Single files, custom handling |
| LLM Agent Parsing | ⚡ Slow | **Very High** (5000+ tokens) | Complex decision-making |

**Token Savings Example**: Uploading a 2000-line Markdown file with tables and code blocks:
- Using this skill (Python script): **0 tokens**
- Using notion-workspace (MCP tools): **~3000-5000 tokens** (Claude must parse and process the entire file)

## Technical Details

### Script Location
```
~/.claude/skills/notion-md-sync/scripts/sync_md_to_notion.py
```

### CLI Options

```
usage: sync_md_to_notion.py [-h] [-p PARENT_ID] files [files ...]

positional arguments:
  files                 Markdown files to sync

options:
  -h, --help            Show help message and exit
  -p PARENT_ID, --parent PARENT_ID, --parent-id PARENT_ID
                        Parent page ID (will auto-search if not provided)
```

**Examples:**
```bash
# View help
python3 sync_md_to_notion.py --help

# Sync with auto-detected parent
python3 sync_md_to_notion.py file.md

# Sync with specific parent
python3 sync_md_to_notion.py --parent abc123-def456-... file.md

# Short form
python3 sync_md_to_notion.py -p abc123-def456-... *.md
```

### Dependencies
- Python 3.x
- `requests` module (install via `pip install requests`)
- `argparse` module (built-in to Python 3)

### Notion API Version
- Uses Notion API version: 2022-06-28
- Endpoint: https://api.notion.com/v1

## References

- `references/setup.md` - Complete token setup and configuration guide
- Notion API Docs: https://developers.notion.com/reference
- Notion MCP Server: @notionhq/notion-mcp-server
