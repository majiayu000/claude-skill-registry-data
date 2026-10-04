---
name: gws-gmail-users-messages-get
description: "Gmail: Get a specific message by ID with configurable format."
---

# gmail users messages get

Get a specific message by ID. Supports multiple output formats to control token usage.

## Usage

```bash
gws gmail users messages get --params '<JSON>'
```

## Parameters (`--params` JSON)

| Parameter         | Required | Default | Description                                                            |
| ----------------- | -------- | ------- | ---------------------------------------------------------------------- |
| `userId`          | ✓        | —       | The user's email address or `"me"` for the authenticated user          |
| `id`              | ✓        | —       | The Gmail message ID                                                   |
| `format`          | —        | `full`  | Response format: `full`, `metadata`, `minimal`, `raw`                  |
| `metadataHeaders` | —        | —       | Array of header names to include (only used with `format: "metadata"`) |

## Format Options

| Format     | Returns                                      | Token Cost |
| ---------- | -------------------------------------------- | ---------- |
| `minimal`  | ID, thread ID, labels only                   | Very low   |
| `metadata` | Headers only (filtered by `metadataHeaders`) | Low        |
| `full`     | Headers + parsed body parts (base64 encoded) | High       |
| `raw`      | Entire RFC 2822 message as base64            | Very high  |

## Examples

```bash
# Get full message
gws gmail users messages get --params '{"userId": "me", "id": "19ea3ab6ef5d5f9f", "format": "full"}'

# Get only specific headers (best for security analysis)
gws gmail users messages get --params '{"userId": "me", "id": "19ea3ab6ef5d5f9f", "format": "metadata", "metadataHeaders": ["From", "To", "Subject", "Date", "Authentication-Results", "Received-SPF", "DKIM-Signature", "Reply-To", "Return-Path"]}'

# Get minimal info (just labels and thread ID)
gws gmail users messages get --params '{"userId": "me", "id": "19ea3ab6ef5d5f9f", "format": "minimal"}'
```

## Tips

- Use `format: "metadata"` with `metadataHeaders` to fetch only the headers you need — dramatically reduces token usage.
- **To read a body, don't decode `full` yourself — use the `gws gmail +read` helper.** It base64-decodes, handles multipart/alternative, and converts HTML to plain text automatically:

  ```bash
  gws gmail +read --id <ID>             # plain-text body
  gws gmail +read --id <ID> --headers   # body prefixed with From/To/Subject/Date
  gws gmail +read --id <ID> --html | grep -oE 'href="[^"]+"'   # links
  gws gmail +read --id <ID> --format json | jq '.body'         # structured
  ```

  Only reach for `format: "full"` here (raw base64url body parts) when you need part-level MIME structure that `+read` doesn't expose.
- Pair with `gws gmail users messages list` to discover message IDs first.
