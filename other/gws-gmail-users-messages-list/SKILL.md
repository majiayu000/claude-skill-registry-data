---
name: gws-gmail-users-messages-list
description: "Gmail: List messages in a user's mailbox with optional filtering."
---

# gmail users messages list

List messages in a user's mailbox. Returns message IDs and thread IDs — use `gws gmail users messages get` to fetch full content.

## Usage

```bash
gws gmail users messages list --params '<JSON>'
```

## Parameters (`--params` JSON)

| Parameter          | Required | Default | Description                                                                               |
| ------------------ | -------- | ------- | ----------------------------------------------------------------------------------------- |
| `userId`           | ✓        | —       | The user's email address or `"me"` for the authenticated user                             |
| `maxResults`       | —        | 100     | Maximum number of messages to return (1–500)                                              |
| `q`                | —        | —       | Gmail search query, same syntax as the Gmail search box (e.g. `"is:unread from:alice"`)   |
| `labelIds`         | —        | —       | Array of label IDs to filter by. Only messages with **all** specified labels are returned |
| `pageToken`        | —        | —       | Token for the next page of results (from a previous response's `nextPageToken`)           |
| `includeSpamTrash` | —        | false   | Include messages from SPAM and TRASH in results                                           |

## Global Flags

| Flag           | Description                                                            |
| -------------- | ---------------------------------------------------------------------- |
| `--format`     | Output format: `json` (default), `table`, `yaml`, `csv`                |
| `--page-all`   | Auto-paginate through all results, outputting one JSON line per page   |
| `--page-limit` | Maximum number of pages to fetch when using `--page-all` (default: 10) |
| `--page-delay` | Delay in milliseconds between page fetches (default: 100)              |
| `--dry-run`    | Show the request that would be sent without executing it               |

## Examples

```bash
# List the 5 most recent messages
gws gmail users messages list --params '{"userId": "me", "maxResults": 5}'

# Search for unread messages from a specific sender
gws gmail users messages list --params '{"userId": "me", "q": "is:unread from:notifications@github.com"}'

# List messages with a specific label
gws gmail users messages list --params '{"userId": "me", "labelIds": ["INBOX"], "maxResults": 10}'

# Auto-paginate through all inbox messages (up to 10 pages)
gws gmail users messages list --params '{"userId": "me", "labelIds": ["INBOX"]}' --page-all

# Dry run to inspect the request
gws gmail users messages list --params '{"userId": "me", "maxResults": 3}' --dry-run
```

## Response Shape

```json
{
  "messages": [
    { "id": "19ea3ab6ef5d5f9f", "threadId": "19ea3ab6ef5d5f9f" },
    { "id": "19ea336ce5191c04", "threadId": "19ea336ce5191c04" }
  ],
  "nextPageToken": "...",
  "resultSizeEstimate": 42
}
```

- `messages[].id` — Use with `gws gmail users messages get` to fetch full content.
- `nextPageToken` — Pass as `pageToken` in the next request to get the next page.
- `resultSizeEstimate` — Approximate total number of matching messages.

## Tips

- Read-only — never modifies your mailbox.
- The `q` parameter supports the full [Gmail search syntax](https://support.google.com/mail/answer/7190): date ranges (`after:2026/06/01`), attachments (`has:attachment`), size (`larger:5M`), etc.
- Returns only IDs by default. Pair with `gws gmail +read` to fetch bodies efficiently.
