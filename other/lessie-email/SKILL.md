---
name: lessie-email
metadata:
  version: 1.1.0
  tags: [email, outreach, bulk-send, drafts, inbox]
description: >
  Send, manage, and automate emails across multiple providers (Gmail, Outlook,
  Official Email) via MCP. Use this skill whenever the user wants to send emails, check
  inbox, manage email threads, create bulk email campaigns, manage drafts, or
  check email accounts and quotas. Trigger this skill when the user mentions
  sending mail, checking inbox, email campaigns, drafts, follow-ups, read/unread
  status, or email automation. Requires MCP server configuration.
---

# Lessie Email — Multi-Provider Email Management

## Setup

Add the Lessie Email MCP server to your MCP config (Claude Code `~/.claude.json`, Cursor `~/.cursor/mcp.json`, Codex `~/.codex/config.toml`, etc.):

```json
{
  "mcpServers": {
    "lessie-email-mcp": {
      "command": "npx",
      "args": ["-y", "@lessie/mcp-server"],
      "env": {
        "LESSIE_REMOTE_MCP_URL": "https://app.lessie.ai/email-api/mcp-public/mcp"
      }
    }
  }
}
```

### Uninstall

Remove the `"lessie-email"` entry from your MCP config and run `rm -rf ~/.lessie/`.

## Version check

Run this check once at the start of each session. Non-blocking — if any command fails, skip silently.

1. Read current local version from this file's metadata `version` field above.
2. Fetch remote version:
   ```bash
   curl -sf --max-time 5 https://raw.githubusercontent.com/LessieAI/lessie-skill/main/lessie-email/SKILL.md | head -5 | grep 'version:' | head -1 | awk '{print $2}'
   ```
3. If the remote version is newer → tell the user:
   > ⬆️ A newer version of lessie-email skill is available ({current} → {remote}). Run this command to update:
   > ```
   > npx skills add LessieAI/lessie-skill -y -g
   > ```
4. If versions match or check fails → skip, say nothing.

## Authorization

1. **Directly call `use_lessie`** to perform the desired action — skip authorization if already connected.
2. **If `use_lessie` fails** (e.g., returns "not authorized" or "remote MCP server not connected") → call `authorize` to start the OAuth flow:
   - `authorize` returns an authorization URL. Tell the user you need to open a browser for Lessie login/registration, and open it using the appropriate system command:
     - macOS: `open "<url>"`
     - Linux: `xdg-open "<url>"`
     - Windows: `start "<url>"`
   - Tell the user the browser has been opened and they need to complete login/registration.
   - After the user confirms, call `authorize` again to verify the connection.
   - If authorization fails (timeout, denied, port conflict), follow the diagnostic hints returned by `authorize` and retry.
3. **After authorization succeeds** → retry the original `use_lessie` call.

### Troubleshooting: Authorization repeatedly fails

**Root cause**: stale `lessie-mcp-server` processes from old sessions occupy the callback port (19836), forcing port fallback and corrupting OAuth client state.

**Fix** — kill stale processes and clear storage, then re-authorize:

```bash
ps aux | grep 'lessie-mcp-server' | grep -v grep | awk '{print $2}' | xargs kill 2>/dev/null
rm -rf ~/.lessie/
lsof -i :19836 | grep LISTEN  # should return nothing
```

Always inform the user before opening the browser — never silently redirect.

## Quick start

After setup, try:

- "Show me my email accounts and unread counts"
- "Send an email from alice@company.com to bob@example.com about the Q2 report"
- "List my recent email threads"
- "Create a bulk email campaign to these 50 contacts"
- "Draft an email to the engineering team about the sprint review"
- "Mark all emails in this thread as read"

## Tools overview

### Email Accounts

| Tool | When to use |
|------|-------------|
| `list_email_accounts_with_unread` | View all linked email accounts with unread counts |

### Email Operations

| Tool | When to use |
|------|-------------|
| `send_email` | Send an email (supports HTML, CC/BCC, attachments, replies) |
| `get_email_detail` | View full email details (content, delivery status, read status) |
| `list_sent_emails` | Browse sent emails with cursor pagination |
| `get_email_quota` | Check daily sending quota for a specific email address |
| `delete_email` | Soft-delete an email |
| `set_email_read_status` | Mark an email as read or unread |

### Thread Management

| Tool | When to use |
|------|-------------|
| `list_threads` | Browse email conversations (all/read/unread filtering) |
| `get_thread_messages` | View all messages in a conversation thread |
| `delete_thread` | Soft-delete an entire conversation thread |
| `set_thread_read_status` | Mark all emails in a thread as read or unread |

### Drafts

| Tool | When to use |
|------|-------------|
| `create_draft` | Create a new email draft |
| `update_draft` | Update an existing draft (subject, content, recipients, etc.) |
| `delete_draft` | Delete a draft |
| `list_drafts` | Browse drafts with cursor pagination |

### Bulk Email Tasks

| Tool | When to use |
|------|-------------|
| `create_task` | Create a bulk email send task (auto-schedules per recipient) |
| `list_tasks` | Browse bulk tasks with progress info |
| `get_task_detail` | View task details with delivery/open/fail stats per recipient |
| `delete_task` | Delete a bulk email task |
| `pause_task` | Pause a running bulk email task |
| `resume_task` | Resume a paused bulk email task |

## Agent behavior rules

### Before sending emails

1. **Always check accounts first**: Call `list_email_accounts_with_unread` to get available sender addresses.
2. **No email accounts bound**: If the account list is empty, tell the user they have no email accounts linked yet and guide them to visit **https://app.lessie.ai/** to bind an email account. Open the URL using the appropriate system command:
   - macOS: `open "https://app.lessie.ai/"`
   - Linux: `xdg-open "https://app.lessie.ai/"`
   - Windows: `start "https://app.lessie.ai/"`
   Then ask the user to return after binding and retry.
3. **Always check quota**: Call `get_email_quota` for the chosen sender to confirm quota is sufficient.
4. **Never guess email addresses**: Only use addresses returned by the account list.

### Replying to emails

1. Get the thread context: call `get_thread_messages` to see the conversation.
2. Use the `thread_id` and `reply_to_message_id` from the last message.
3. Pass both when calling `send_email` for a proper threaded reply.

### Draft workflow

1. Create a draft with `create_draft` — specify sender, recipients, subject, and content.
2. Update the draft with `update_draft` if changes are needed.
3. When ready, use `send_email` with the finalized content (drafts are not sent directly).
4. Delete the draft with `delete_draft` after sending or if no longer needed.

### Bulk task management

- After creating a task with `create_task`, monitor progress with `get_task_detail`.
- Use `pause_task` to temporarily halt a running campaign (e.g., if issues are found).
- Use `resume_task` to continue a paused campaign.
- Use `delete_task` to permanently remove a task.

### Gmail/Outlook specific

- When calling `get_email_detail`, `delete_email`, `get_thread_messages` for Gmail/Outlook accounts, always pass the `email` parameter.
- The system auto-routes to the correct provider API based on the email address.

## Key constraints

- Cursor pagination: all list endpoints use `cursor` + `size` — pass `next_cursor` from previous response.
- Default page size: 20 (max 100).
- Email content: provide at least `text_content` or `html_content` — if only text is provided, HTML is auto-generated.
- Attachments require pre-uploaded S3 keys with `s3key`, `filename`, `mime_type`, `size`.
- Bulk tasks auto-schedule sends across time to respect quotas and avoid spam.
