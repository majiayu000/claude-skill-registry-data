---
type: Skill
name: design-communications
description: Manage multi-channel communications — SMS, email, WhatsApp messages and contacts. Covers message tracking, contact management, delivery status, and media attachments. Use when working with channel messages, managing contacts, tracking communication threads, or troubleshooting message delivery.
license: Proprietary. See LICENSE.txt
metadata:
  type: Skill
---

# NV oOS Pro Toolkit Communications

The Pro Toolkit Communications system provides multi-channel messaging
infrastructure built on WordPress Custom Post Types. It manages the full
communication lifecycle: **contact discovery → message composition → delivery
tracking → thread history**. All entities are stored as CPT records accessible
via the `toolkit_cpt` MCP tool.

## WP-CLI Commands

Key `mcp-ai` WP-CLI commands for communications operations. Run via `terminal`:

| Command | Use for |
|---|---|
| `wp mcp-ai cron` | Verify message delivery cron jobs, check retry schedules |
| `wp mcp-ai queue` | Inspect outbound message queue, retry failed deliveries |
| `wp mcp-ai health` | Validate channel configuration (SMS gateway, email SMTP, WhatsApp API) |
| `wp mcp-ai log` | View message delivery logs, troubleshoot delivery failures |

## When to use this skill

Trigger when ANY of the following is true:

- Viewing, searching, or filtering channel messages or contacts.
- Creating or updating contact profiles with channel handles (SMS, email, WhatsApp).
- Sending or tracking outbound messages across any channel.
- Reviewing inbound messages and routing them to the appropriate team or agent.
- Troubleshooting message delivery status (sent → delivered → read → failed).
- Managing media attachments on messages (images, documents, audio).
- Building communication threads — linking related messages by contact or context.
- Searching for all messages from a specific contact or across a date range.
- Checking a contact's last seen timestamp or communication history.
- Linking a channel contact to a WordPress user account.

## Mental model — Communications entities and lifecycle

The communications system is organized around two core entities linked by contact:

```
CONTACT ──(has many)──→ MESSAGES
   │                       │
   ├── user_id (WP user)   ├── direction (inbound/outbound)
   ├── channel             ├── status (sent/delivered/read/failed)
   ├── handle              ├── media_ids (attachments)
   └── last_seen           └── contact_id (link back)
```

**Relationships:**
- A **Contact** (`mcp_chan_contact`) represents a person on a specific channel. One
  person may have multiple contacts (e.g., SMS at one number, WhatsApp at another).
- A **Message** (`mcp_chan_message`) is always associated with exactly one contact
  via `_chan_msg_contact_id`. The direction indicates inbound (from contact) or
  outbound (to contact).
- A **Contact** can be linked to a WordPress user via `_chan_contact_user_id`,
  enabling authenticated, role-aware communication.
- **Media attachments** are stored as an array of WordPress attachment IDs in
  `_chan_msg_media_ids`.

## Communications Entity Types

All communications entities are managed through the **`toolkit_cpt`** MCP tool. Use the
appropriate `post_type` slug for each entity:

| CPT Slug | Label | Purpose | Key Meta Fields |
|---|---|---|---|
| `mcp_chan_message` | Channel Messages | Individual messages across all channels with delivery tracking | `_chan_msg_contact_id`, `_chan_msg_direction`, `_chan_msg_status`, `_chan_msg_media_ids` |
| `mcp_chan_contact` | Channel Contacts | Contact profiles per channel with handle and user linking | `_chan_contact_user_id`, `_chan_contact_channel`, `_chan_contact_handle`, `_chan_contact_last_seen` |

### Channel Message Meta Fields (detailed)

| Field | Type | Description | Example / Enum |
|---|---|---|---|
| `_chan_msg_contact_id` | integer | Post ID of the associated contact | `42` |
| `_chan_msg_direction` | string | Message direction | `"inbound"`, `"outbound"` |
| `_chan_msg_status` | string | Delivery/read status | `"sent"`, `"delivered"`, `"read"`, `"failed"` |
| `_chan_msg_media_ids` | array | WordPress attachment IDs for media | `[123, 456]` |

**Message status lifecycle:**
```
draft → sent → delivered → read
                ↘ failed (with retry)
```

### Channel Contact Meta Fields (detailed)

| Field | Type | Description | Example / Enum |
|---|---|---|---|
| `_chan_contact_user_id` | integer | WordPress user ID (0 if unlinked) | `1` |
| `_chan_contact_channel` | string | Communication channel | `"sms"`, `"email"`, `"whatsapp"` |
| `_chan_contact_handle` | string | Contact address on the channel | `"+15551234567"`, `"user@example.com"` |
| `_chan_contact_last_seen` | string | ISO 8601 timestamp of last activity | `"2026-08-12T14:30:00+00:00"` |

## Available Tools

All communications operations use the **`toolkit_cpt`** MCP tool. This is the single
interface for all communications CRUD operations.

### Discovery

```
# List all available communications post types
toolkit_cpt(action: "list_types")

# Get field schema for messages or contacts
toolkit_cpt(action: "get_schema", post_type: "mcp_chan_message")
toolkit_cpt(action: "get_schema", post_type: "mcp_chan_contact")
```

### Reading records

```json
// List recent messages (most recent first)
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "list_items",
    "post_type": "mcp_chan_message",
    "orderby": "date",
    "order": "DESC",
    "per_page": 20,
    "page": 1
  }
}

// Find messages for a specific contact
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "list_items",
    "post_type": "mcp_chan_message",
    "filters": [
      { "key": "_chan_msg_contact_id", "value": "42" }
    ]
  }
}

// Find contacts by channel type
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "list_items",
    "post_type": "mcp_chan_contact",
    "filters": [
      { "key": "_chan_contact_channel", "value": "whatsapp" }
    ]
  }
}

// Search contacts by handle (phone number or email)
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "list_items",
    "post_type": "mcp_chan_contact",
    "search": "+15551234567"
  }
}

// Get a single message or contact
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "get_item",
    "post_type": "mcp_chan_message",
    "item_id": 789
  }
}
```

### Creating records

```json
// Create a new contact
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "create_item",
    "post_type": "mcp_chan_contact",
    "fields": {
      "title": "Alice Chen - WhatsApp",
      "_chan_contact_user_id": 5,
      "_chan_contact_channel": "whatsapp",
      "_chan_contact_handle": "+15559876543",
      "_chan_contact_last_seen": "2026-08-12T10:00:00+00:00"
    }
  }
}

// Create an outbound message with media attachments
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "create_item",
    "post_type": "mcp_chan_message",
    "fields": {
      "title": "Order confirmation #1042",
      "content": "Hi Alice, your order has shipped! Track it here: https://track.example.com/1042",
      "_chan_msg_contact_id": 42,
      "_chan_msg_direction": "outbound",
      "_chan_msg_status": "sent",
      "_chan_msg_media_ids": [301, 302]
    }
  }
}

// Log an inbound message
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "create_item",
    "post_type": "mcp_chan_message",
    "fields": {
      "title": "Inquiry about return policy",
      "content": "What's your return window for electronics?",
      "_chan_msg_contact_id": 42,
      "_chan_msg_direction": "inbound",
      "_chan_msg_status": "delivered"
    }
  }
}
```

### Updating records

```json
// Update message delivery status
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "update_item",
    "post_type": "mcp_chan_message",
    "item_id": 789,
    "fields": {
      "_chan_msg_status": "read"
    }
  }
}

// Update contact's last seen timestamp
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "update_item",
    "post_type": "mcp_chan_contact",
    "item_id": 42,
    "fields": {
      "_chan_contact_last_seen": "2026-08-12T14:45:00+00:00"
    }
  }
}

// Link a contact to a WordPress user
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "update_item",
    "post_type": "mcp_chan_contact",
    "item_id": 42,
    "fields": {
      "_chan_contact_user_id": 12
    }
  }
}
```

### Deleting records

```json
// Delete a message (permanent)
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "delete_item",
    "post_type": "mcp_chan_message",
    "item_id": 789
  }
}
```

**⚠️ Warning:** Deleting a message is permanent. Consider archiving via status
change or using `update_item` to set a custom field instead, to preserve the
communication thread for audit purposes.

## Common Workflows

### Contact onboarding workflow

```
1. Receive first message:  Identified via channel webhook or manual entry.
2. Search for existing:    list_items(mcp_chan_contact, search: "<handle>")
3. If new contact:         create_item(mcp_chan_contact, with channel, handle, user_id)
4. If existing contact:    update_item(mcp_chan_contact, last_seen timestamp)
5. Log message:            create_item(mcp_chan_message, direction: "inbound", contact_id)
6. Link to WP user:        update_item(mcp_chan_contact, _chan_contact_user_id) if authenticated
```

### Message thread view

```
1. Find contact:       list_items(mcp_chan_contact, search: "<phone or email>")
2. Get all messages:   list_items(mcp_chan_message,
                         filters: [{key: "_chan_msg_contact_id", value: "<contact_id>"}],
                         orderby: "date", order: "ASC", per_page: 50)
3. Review thread:      Messages are sorted chronologically. Check status for delivery issues.
```

### Delivery troubleshooting

```
1. Find failed messages:  list_items(mcp_chan_message,
                            filters: [{key: "_chan_msg_status", value: "failed"}])
2. Check contact:         get_item(mcp_chan_contact, item_id: <contact_id>)
3. Verify channel:        Confirm _chan_contact_channel and _chan_contact_handle are valid.
4. Retry or escalate:     If handle is correct, check gateway config with wp mcp-ai health.
                          If handle is invalid, update contact with corrected handle.
```

### Multi-channel contact deduplication

```
1. Search all contacts:   list_items(mcp_chan_contact, search: "<name or handle>")
2. Check for duplicates:  Same person may appear under sms, email, and whatsapp.
3. Link to WP user:       If the person has a WP account, set _chan_contact_user_id
                          on ALL their contact records to unify identity.
4. Cross-reference:       Use _chan_contact_user_id to find all contacts for a user.
```

## Critical Rules

- **Always use `get_schema` first** before creating or updating a record to verify available field keys and types.
- **`_chan_msg_contact_id` is required** for every message — never create an orphaned message without a contact link.
- **Message status transitions are directional** — `sent → delivered → read`. Never skip statuses; each transition should be observable.
- **`_chan_contact_handle` must be globally unique per channel** — two contacts cannot share the same handle on the same channel type.
- **`_chan_contact_user_id` is `0` for unlinked contacts** — do not leave it null or unset.
- **`_chan_msg_media_ids` is a JSON array** — always pass as `[301, 302]`, not a comma-separated string.
- **`_chan_contact_last_seen` uses ISO 8601** — always include timezone offset (e.g., `"2026-08-12T14:30:00+00:00"`).
- **Inbound messages should NOT be created manually in production** — they arrive via channel webhooks. Manual creation is for testing and data migration only.
- **Failed messages can be retried** — before retrying, verify the contact handle and channel configuration are valid.

## Common Mistakes

```
WRONG — creating a message without a contact link
{ "action": "create_item", "post_type": "mcp_chan_message",
  "fields": { "title": "Hello", "content": "Hi there!", "_chan_msg_status": "sent" } }
// Missing _chan_msg_contact_id — the message is orphaned.

RIGHT — always link messages to a contact
{ "action": "create_item", "post_type": "mcp_chan_message",
  "fields": { "title": "Hello", "content": "Hi there!", "_chan_msg_contact_id": 42,
  "_chan_msg_direction": "outbound", "_chan_msg_status": "sent" } }

WRONG — skipping delivery status lifecycle
// Setting _chan_msg_status directly to "read" when the message was just created.
// The status flow must follow: sent → delivered → read.

RIGHT — progress status through each stage
1. create_item: _chan_msg_status: "sent"
2. update_item: _chan_msg_status: "delivered"  (gateway confirms delivery)
3. update_item: _chan_msg_status: "read"       (contact opens message)

WRONG — duplicate contact handles on the same channel
// Two contacts with _chan_contact_channel: "sms" and _chan_contact_handle: "+15551234567"
// This creates ambiguity about which contact thread a message belongs to.

RIGHT — search before creating, update instead of duplicating
1. list_items(mcp_chan_contact, search: "+15551234567")
2. If found: update_item to refresh last_seen. If not found: create_item.

WRONG — using non-ISO 8601 timestamps for last_seen
// "2026-08-12 14:30" or "Aug 12, 2026" — these won't sort or compare correctly.

RIGHT — always use ISO 8601 with timezone
// "_chan_contact_last_seen": "2026-08-12T14:30:00+00:00"

WRONG — passing media IDs as a string
// "_chan_msg_media_ids": "301,302" — this won't deserialize as an array.

RIGHT — pass media IDs as a JSON array
// "_chan_msg_media_ids": [301, 302]
```

## Cross-References

- Run `design-crm` to link communication threads to CRM leads, deals, and customers.
- Run `design-email-marketing` for bulk email campaign sending and sequence design.
- Run `design-social-publishing` for social media channel publishing (separate from 1:1 channel messaging).
- Run `design-pro-workflow-builder` to automate communication workflows (auto-reply, routing, escalation).
- Run `wp-security-audit` on any message handling code — communications data may contain PII and must be access-controlled.

## What This Skill Does NOT Cover

- Email marketing campaigns and newsletter sequences — use `design-email-marketing`.
- Social media publishing (Twitter/X, Facebook, Instagram, LinkedIn) — use `design-social-publishing`.
- Gmail inbox integration — use `search_gmail` for Gmail-specific queries.
- Channel gateway configuration (Twilio, WhatsApp Business API, SMTP) — this is infrastructure-level setup, not CPT data management.
- Real-time message delivery — the `toolkit_cpt` tool manages records. Actual message transport is handled by the channel gateway and WordPress Action Scheduler.
- Message templating and variable substitution — use `design-pro-workflow-builder` for message template workflows.
