---
name: elastic-claude
description: Index and search project knowledge. Use when starting a new task to find related prior work, when ingesting documents or chats, or when searching project history for context.
---

# Elastic-Claude

Local search infrastructure for project knowledge.

## CLI Commands

### Add an entry

```bash
# From file path (preferred - Rust reads the file)
elastic-claude add -t <type> -p <file_path> [-m '<json_metadata>']

# Inline content (for small content)
elastic-claude add -t <type> -c "<content>" [-m '<json_metadata>']

# From stdin
cat <file> | elastic-claude add -t <type> [-m '<json_metadata>']
```

Arguments:
- `-t, --entry-type`: Entry type (e.g., "document", "chat", "code")
- `-p, --path`: Read content from file (also sets file_path in DB)
- `-c, --content`: Inline content (conflicts with -p)
- `-m, --metadata`: JSON metadata (optional)

Example:
```bash
elastic-claude add -t document -p /path/to/file.md -m '{"project": "my-project", "title": "My Doc", "category": "docs"}'
```

### Search entries

```bash
elastic-claude search "<query>"
```

Returns matching entries with snippets, scores, and metadata.

### Save current chat session

```bash
# Get path to current chat file
elastic-claude current-chat --path-only

# Ingest current chat with metadata (always include project)
elastic-claude current-chat -m '{"project": "my-project", "title": "Session title", "tags": ["topic1", "topic2"]}'
```

Auto-detects the current Claude session and ingests the chat file.

### Get entry by ID

```bash
# Get full entry details
elastic-claude get <id>

# Get just the content
elastic-claude get <id> --content-only

# Show tsvector tokens (for debugging search)
elastic-claude get <id> --tsv
```

## Workflow for Ingesting Documents

When asked to ingest files:

1. Determine the project name from the current working directory or ask the user
2. Read each file's content
3. Extract metadata from content and path:
   - project: **always include** - the project/repo name
   - title: from first heading or filename
   - category: from directory path
   - tags: from content keywords
4. Call `elastic-claude add` for each file

Example for a markdown file:
```bash
elastic-claude add -t document -p /path/to/file.md -m '{"project": "CQR", "title": "Extracted Title", "category": "documentation"}'
```

## Workflow for Searching

When asked to find information:

1. Run `elastic-claude search "<relevant keywords>"`
2. Review the results (snippets, file paths, metadata)
3. If needed, read the full files for more context
4. Summarize findings for the user

## Schema Reference

See [references/schema.md](references/schema.md) for database schema details.

Entry types:
- `document`: Markdown docs, READMEs, etc.
- `chat`: Chat session transcripts
- `code`: Code snippets or files
