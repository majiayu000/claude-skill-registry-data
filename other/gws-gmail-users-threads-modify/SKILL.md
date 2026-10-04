---
name: gws-gmail-users-threads-modify
description: "Gmail: Modify the labels applied to a specific thread."
---

# gmail users threads modify

Modify the labels applied to a specific thread. This changes the labels on all messages currently in the thread.

## Usage

```bash
gws gmail users threads modify --params '<JSON_PARAMS>' --json '<JSON_BODY>'
```

## Parameters (`--params` JSON)

| Parameter | Required | Default | Description                                                   |
| --------- | -------- | ------- | ------------------------------------------------------------- |
| `userId`  | ✓        | —       | The user's email address or `"me"` for the authenticated user |
| `id`      | ✓        | —       | The Gmail thread ID                                           |

## Request Body (`--json` JSON)

| Field            | Type             | Description                                  |
| ---------------- | ---------------- | -------------------------------------------- |
| `addLabelIds`    | Array of strings | List of label IDs to add to the thread.      |
| `removeLabelIds` | Array of strings | List of label IDs to remove from the thread. |

## Examples

```bash
# Archive an entire thread (remove INBOX from all messages in the thread)
gws gmail users threads modify --params '{"userId": "me", "id": "19ea3ab6ef5d5f9f"}' --json '{"removeLabelIds": ["INBOX"]}'

# Apply a custom label to a thread
gws gmail users threads modify --params '{"userId": "me", "id": "19ea3ab6ef5d5f9f"}' --json '{"addLabelIds": ["triage/todo"]}'
```

## Tips

- Modifying a thread affects all messages currently in that thread.
- If you want to modify only a single message in a thread without affecting others, use `gws gmail users messages modify`.
