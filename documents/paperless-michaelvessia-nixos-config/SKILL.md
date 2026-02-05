---
name: paperless
description: Search and manage documents in Paperless-ngx document management system. Use when the user asks about documents, invoices, receipts, tax forms, bills, or wants to search their document library.
allowed-tools: Bash, Read
---

# Paperless-ngx

Interact with Paperless-ngx document management system via CLI.

## Setup

Environment: `~/.secrets.env` (PAPERLESS_URL, PAPERLESS_TOKEN) - loaded by wrapper

Run commands via:
```bash
paperless-cli <command>
```

## Commands Reference

See [CLI-REFERENCE.md](CLI-REFERENCE.md) for full command documentation.

### Quick Reference

| Command | Purpose |
|---------|---------|
| `search [query]` | Full-text search with filters |
| `list` | Recent documents, `--inbox` for inbox |
| `get <id>` | Document details and content |
| `download <id>` | Download original file |
| `edit <id>` | Edit title/correspondent/type |
| `similar <id>` | Find similar documents |
| `add-tag <id> <tag>` | Add tag to document |
| `remove-tag <id> <tag>` | Remove tag from document |
| `tags` | List all tags |
| `correspondents` | List all correspondents |
| `types` | List all document types |
| `stats` | System statistics |

## Workflow

1. Start with `search` or `list` to find documents
2. Use `get <id>` to read full content
3. Use `add-tag`/`remove-tag` to organize
4. Use `similar <id>` to find related documents
5. Use `download <id>` to save original files

## Examples

**Important:** Flags must come BEFORE positional arguments (query text).

**"Find my tax documents from 2023"**
```bash
search "tax 2023"
# or with filters (flags before query):
search --tag tax --after 2023-01-01 --before 2024-01-01
```

**"What's in my inbox?"**
```bash
list --inbox
```

**"Show me that W-2"**
```bash
get 1234
```

**"Tag document 1234 as reviewed"**
```bash
add-tag 1234 reviewed --create
```

**"Find similar documents to this receipt"**
```bash
similar 1234
```

**"Download that PDF"**
```bash
download 1234
```
