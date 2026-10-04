---
name: gws-gmail-users-labels-create
description: "Gmail: Create a custom label in the user's mailbox."
---

# gmail users labels create

Create a new custom label in the user's mailbox.

## Usage

```bash
gws gmail users labels create --params '<JSON_PARAMS>' --json '<JSON_BODY>'
```

## Parameters (`--params` JSON)

| Parameter | Required | Default | Description                                                   |
| --------- | -------- | ------- | ------------------------------------------------------------- |
| `userId`  | ✓        | —       | The user's email address or `"me"` for the authenticated user |

## Request Body (`--json` JSON)

| Field                   | Type   | Required | Description                                                                                                  |
| ----------------------- | ------ | -------- | ------------------------------------------------------------------------------------------------------------ |
| `name`                  | String | ✓        | The name of the label (can use slashes for hierarchy, e.g. `"triage/action-required"`).                      |
| `labelListVisibility`   | String | —        | Visibility of the label in the Gmail sidebar. Allowed values: `labelShow`, `labelShowIfUnread`, `labelHide`. |
| `messageListVisibility` | String | —        | Visibility of messages with this label in the message list. Allowed values: `show`, `hide`.                  |

## Examples

```bash
# Create a basic custom label
gws gmail users labels create --params '{"userId": "me"}' --json '{"name": "triage/action-required"}'

# Create a custom label with sidebar visibility settings
gws gmail users labels create --params '{"userId": "me"}' --json '{"name": "Projects/Design", "labelListVisibility": "labelShowIfUnread", "messageListVisibility": "show"}'
```

## Tips

- If creating a nested/hierarchical label (e.g. `"Parent/Child"`), the parent label does not need to exist beforehand; Gmail will construct the tree automatically.
- Label names are case-sensitive.
