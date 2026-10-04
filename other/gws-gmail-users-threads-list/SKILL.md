---
name: gws-gmail-users-threads-list
description: "Gmail: List threads in a user's mailbox with optional filtering."
---

# gmail users threads list

List threads in a user's mailbox. Returns thread IDs and snippet previews. Each thread groups related messages in a conversation.

## Usage

```bash
gws gmail users threads list --params '<JSON>'
```

## Parameters (`--params` JSON)

| Parameter          | Required | Default | Description                                                                              |
| ------------------ | -------- | ------- | ---------------------------------------------------------------------------------------- |
| `userId`           | ✓        | —       | The user's email address or `"me"` for the authenticated user                            |
| `maxResults`       | —        | 100     | Maximum number of threads to return (1–500)                                              |
| `q`                | —        | —       | Gmail search query, same syntax as the Gmail search box (e.g. `"is:unread from:alice"`)  |
| `labelIds`         | —        | —       | Array of label IDs to filter by. Only threads with **all** specified labels are returned  |
| `pageToken`        | —        | —       | Token for the next page of results (from a previous response's `nextPageToken`)          |
| `includeSpamTrash` | —        | false   | Include threads from SPAM and TRASH in results                                           |

## Global Flags

| Flag           | Description                                                          |
| -------------- | -------------------------------------------------------------------- |
| `--format`     | Output format: `json` (default), `table`, `yaml`, `csv`             |
| `--page-all`   | Auto-paginate through all results, outputting one JSON line per page |
| `--page-limit` | Maximum number of pages to fetch when using `--page-all` (default: 10) |
| `--dry-run`    | Show the request that would be sent without executing it             |

## Examples

```bash
# List the 5 most recent threads
gws gmail users threads list --params '{"userId": "me", "maxResults": 5}'

# Search for threads from a specific sender
gws gmail users threads list --params '{"userId": "me", "q": "from:notifications@github.com"}'

# List unread inbox threads
gws gmail users threads list --params '{"userId": "me", "q": "is:unread", "labelIds": ["INBOX"], "maxResults": 10}'
```

## Response Shape

```json
{
  "threads": [
    { "id": "19ea3ab6ef5d5f9f", "snippet": "Your order has been...", "historyId": "50817087" },
    { "id": "19ea336ce5191c04", "snippet": "Reminder: Content older...", "historyId": "50816320" }
  ],
  "nextPageToken": "...",
  "resultSizeEstimate": 42
}
```

- `threads[].id` — Use with `gws gmail users threads get` to fetch the full conversation.
- `threads[].snippet` — Short preview of the most recent message.
- `nextPageToken` — Pass as `pageToken` in the next request to get the next page.

## Tips

- Threads group related messages (replies, forwards) into a single conversation.
- The `q` parameter supports the full [Gmail search syntax](https://support.google.com/mail/answer/7190).
- Use threads instead of messages when you need conversation context (e.g., relationship analysis across a reply chain).

## See Also

- [gws-gmail-users-threads-get](../gws-gmail-users-threads-get/SKILL.md) — Get a full thread
- [gws-gmail-users-messages-list](../gws-gmail-users-messages-list/SKILL.md) — List individual messages
