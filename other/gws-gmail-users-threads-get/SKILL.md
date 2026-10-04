---
name: gws-gmail-users-threads-get
description: "Gmail: Get a specific thread and all its messages."
---

# gmail users threads get

Get a specific thread by ID. Returns all messages in the thread, useful for understanding conversation context.

## Usage

```bash
gws gmail users threads get --params '<JSON>'
```

## Parameters (`--params` JSON)

| Parameter          | Required | Default | Description                                                            |
| ------------------ | -------- | ------- | ---------------------------------------------------------------------- |
| `userId`           | ✓        | —       | The user's email address or `"me"` for the authenticated user          |
| `id`               | ✓        | —       | The thread ID                                                          |
| `format`           | —        | `full`  | Response format: `full`, `metadata`, `minimal`                         |
| `metadataHeaders`  | —        | —       | Array of header names to include (only used with `format: "metadata"`) |

## Format Options

| Format     | Returns                                                | Token Cost |
| ---------- | ------------------------------------------------------ | ---------- |
| `minimal`  | IDs and labels for each message in the thread          | Very low   |
| `metadata` | Headers only for each message (filtered)               | Low        |
| `full`     | Headers + parsed body parts for each message           | High       |

## Examples

```bash
# Get full thread with all messages
gws gmail users threads get --params '{"userId": "me", "id": "19ea3ab6ef5d5f9f", "format": "full"}'

# Get thread metadata only (headers for each message)
gws gmail users threads get --params '{"userId": "me", "id": "19ea3ab6ef5d5f9f", "format": "metadata", "metadataHeaders": ["From", "To", "Subject", "Date"]}'

# Get minimal thread info (just message IDs and labels)
gws gmail users threads get --params '{"userId": "me", "id": "19ea3ab6ef5d5f9f", "format": "minimal"}'
```

## Response Shape

```json
{
  "id": "19ea3ab6ef5d5f9f",
  "historyId": "50817087",
  "messages": [
    {
      "id": "19ea3ab6ef5d5f9f",
      "threadId": "19ea3ab6ef5d5f9f",
      "labelIds": ["INBOX", "UNREAD"],
      "payload": { ... }
    },
    {
      "id": "19ea3cd8a1b2e3f4",
      "threadId": "19ea3ab6ef5d5f9f",
      "payload": { ... }
    }
  ]
}
```

## Tips

- Thread ID often matches the first message ID in the thread.
- Use `format: "metadata"` to get conversation flow (who replied when) without loading full bodies.
- Pair with `gws gmail users threads list` to discover thread IDs.

## See Also

- [gws-gmail-users-threads-list](../gws-gmail-users-threads-list/SKILL.md) — List threads
- [gws-gmail-users-messages-get](../gws-gmail-users-messages-get/SKILL.md) — Get a single message
