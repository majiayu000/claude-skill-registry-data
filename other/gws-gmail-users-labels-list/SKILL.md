---
name: gws-gmail-users-labels-list
description: "Gmail: List all labels in the user's mailbox."
---

# gmail users labels list

List all labels (both system labels like INBOX, UNREAD, and custom user labels) in the user's mailbox.

## Usage

```bash
gws gmail users labels list --params '<JSON>'
```

## Parameters (`--params` JSON)

| Parameter | Required | Default | Description |
| --------- | -------- | ------- | ----------- |
| `userId`  | ✓        | —       | The user's email address or `"me"` for the authenticated user |

## Examples

```bash
# List all labels
gws gmail users labels list --params '{"userId": "me"}'
```

## Tips

- Returns a list of label objects containing their `id`, `name`, `type` (e.g. `system` or `user`), and configuration details.
- Useful for discovering the exact label IDs to use in filtering (e.g., when listing messages) or modifying labels (e.g., when updating messages).
