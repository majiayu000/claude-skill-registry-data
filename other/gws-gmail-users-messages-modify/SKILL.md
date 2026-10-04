---
name: gws-gmail-users-messages-modify
description: "Gmail: Modify the labels applied to a specific message."
---

# gmail users messages modify

Modify the labels applied to a specific message (e.g. add custom labels, archive by removing "INBOX", mark as read by removing "UNREAD").

## Usage

```bash
gws gmail users messages modify --params '<JSON_PARAMS>' --json '<JSON_BODY>'
```

## Parameters (`--params` JSON)

| Parameter | Required | Default | Description                                                   |
| --------- | -------- | ------- | ------------------------------------------------------------- |
| `userId`  | ✓        | —       | The user's email address or `"me"` for the authenticated user |
| `id`      | ✓        | —       | The Gmail message ID                                          |

## Request Body (`--json` JSON)

| Field            | Type             | Description                                   |
| ---------------- | ---------------- | --------------------------------------------- |
| `addLabelIds`    | Array of strings | List of label IDs to add to the message.      |
| `removeLabelIds` | Array of strings | List of label IDs to remove from the message. |

## Examples

```bash
# Mark a message as read (remove UNREAD)
gws gmail users messages modify --params '{"userId": "me", "id": "19ea3ab6ef5d5f9f"}' --json '{"removeLabelIds": ["UNREAD"]}'

# Archive a message (remove INBOX)
gws gmail users messages modify --params '{"userId": "me", "id": "19ea3ab6ef5d5f9f"}' --json '{"removeLabelIds": ["INBOX"]}'

# Add a custom triage label and mark as read
gws gmail users messages modify --params '{"userId": "me", "id": "19ea3ab6ef5d5f9f"}' --json '{"addLabelIds": ["triage/done"], "removeLabelIds": ["UNREAD"]}'
```

## Tips

- Label IDs are case-sensitive. Built-in labels are typically uppercase (e.g., `"INBOX"`, `"UNREAD"`, `"STARRED"`, `"IMPORTANT"`, `"SPAM"`, `"TRASH"`).
- Custom user labels should use their exact name (e.g., `"triage/done"` or `"Work"`).
- Removing `"INBOX"` effectively archives the message.
- To perform modifications on a whole thread of messages, use `gws gmail users threads modify`.
