---
name: paperless
description: Search and manage documents in Paperless-ngx document management system. Use when the user asks about documents, invoices, receipts, tax forms, bills, or wants to search their document library.
allowed-tools: Bash, Read
---

# Paperless-ngx

Interact with Paperless-ngx document management system via CLI.

## Setup

Environment: `~/.secrets.env` (PAPERLESS_URL, PAPERLESS_TOKEN) - loaded by
wrapper.

## CLI Discovery

Run `paperless-cli --help` to see available commands. Run
`paperless-cli <command> --help` for detailed usage of any command.

## Capabilities

The CLI supports:

- **Search**: Full-text search with filters (date ranges, tags, correspondents)
- **Browse**: List recent documents, inbox items
- **Read**: Get document details and extracted text content
- **Organize**: Add/remove tags, edit metadata (title, correspondent, type)
- **Find related**: Discover similar documents
- **Download**: Save original files locally
- **Metadata**: List tags, correspondents, document types, stats

## Workflow

1. Search or list to find documents
2. Get document by ID to read full content
3. Add/remove tags to organize
4. Find similar documents for related items
5. Download originals when needed

## Notes

- Flags must come BEFORE positional arguments
- Document IDs are integers returned from search/list results
