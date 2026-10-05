---
type: Skill
name: gws-docs
version: 1.0.0
description: Google Docs skill for creating, reading, and updating documents via the gws CLI. Covers document creation, content retrieval, batch updates, and sharing.
license: Apache-2.0
compatibility: Claude Code, Cursor, Gemini CLI, Codex CLI
---

# Google Docs (gws-docs)

> **PREREQUISITE:** Read the `gws-shared` skill for auth, global flags, and security rules.

Read and write Google Docs using the `gws` CLI.

```bash
gws docs <resource> <method> [flags]
```

## Quick Examples

```bash
# Create a new blank document
gws docs documents create \
  --json '{"title": "Meeting Notes — March 2026"}'

# Get document content (returns full JSON including body segments)
gws docs documents get \
  --params '{"documentId": "DOCUMENT_ID"}'

# Append text to a document
gws docs documents batchUpdate \
  --params '{"documentId": "DOCUMENT_ID"}' \
  --json '{
    "requests": [
      {
        "insertText": {
          "location": {"index": 1},
          "text": "New paragraph content here.\n"
        }
      }
    ]
  }'

# Insert a heading
gws docs documents batchUpdate \
  --params '{"documentId": "DOCUMENT_ID"}' \
  --json '{
    "requests": [
      {
        "insertText": {
          "location": {"index": 1},
          "text": "Section Title\n"
        }
      },
      {
        "updateParagraphStyle": {
          "range": {"startIndex": 1, "endIndex": 14},
          "paragraphStyle": {"namedStyleType": "HEADING_1"},
          "fields": "namedStyleType"
        }
      }
    ]
  }'

# Replace placeholder text (template fill-in)
gws docs documents batchUpdate \
  --params '{"documentId": "DOCUMENT_ID"}' \
  --json '{
    "requests": [
      {
        "replaceAllText": {
          "containsText": {"text": "{{CLIENT_NAME}}", "matchCase": false},
          "replaceText": "Acme Corp"
        }
      }
    ]
  }'

# Insert a table
gws docs documents batchUpdate \
  --params '{"documentId": "DOCUMENT_ID"}' \
  --json '{
    "requests": [
      {
        "insertTable": {
          "rows": 3,
          "columns": 3,
          "location": {"index": 1}
        }
      }
    ]
  }'
```

## Helper Commands

| Command | Description |
|---------|-------------|
| `gws docs +write` | Append text to a document (simplified) |

## Common batchUpdate Request Types

| Request type | What it does |
|-------------|-------------|
| `insertText` | Insert text at a specific index |
| `deleteContentRange` | Remove a range of content |
| `replaceAllText` | Find and replace throughout document |
| `insertPageBreak` | Insert a page break |
| `updateParagraphStyle` | Apply a heading or paragraph style |
| `updateTextStyle` | Bold, italic, font, size |
| `insertTable` | Insert a table |
| `insertInlineImage` | Embed an image |
| `createNamedRange` | Mark a range for later reference |

## Reading Document Content

The `documents.get` response contains a `body.content` array of structural elements:

```json
{
  "documentId": "...",
  "title": "My Document",
  "body": {
    "content": [
      { "paragraph": { "elements": [{ "textRun": { "content": "Hello\n" } }] } }
    ]
  }
}
```

Extract plain text with `jq`:

```bash
gws docs documents get --params '{"documentId": "DOC_ID"}' \
  | jq '[.. | .textRun?.content? // empty] | join("")'
```

## Key API Resources

### documents
`get`, `create`, `batchUpdate`

## Discovering More

```bash
gws docs --help
gws schema docs.documents.batchUpdate
gws schema docs.documents.get
```
