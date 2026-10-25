---
name: outlook
description: Work with the user's Outlook mailbox, calendar, contacts and tasks through the outlook MCP server. Use for reading or triaging email, drafting and sending, replying, scheduling meetings, finding free time, contact lookup and task tracking.
---

# Outlook

Tools come from the `outlook` MCP server (Outlook desktop on Windows). Keep calls cheap: list first, read only what you need.

## Token-lean workflow

1. `mail_list` returns one line per message. Narrow it with `query`, `from`, `since`, `unread` instead of paging through everything. Leave `preview` at 0 unless you must triage by content.
2. Read with `mail_get`. Bodies are cleaned and capped; pass `body_offset` for the rest. Ask for `headers=true` only when you need addresses or routing info.
3. Act in batches: `mail_update`, `mail_move` and `mail_delete` take many ids in one call.
4. For long threads use `mail_thread` (trimmed bodies) instead of reading each message.

## Sending safely

- Default to a draft: `mail_draft_save`, `mail_reply`, `mail_forward` save drafts unless `send=true`.
- Only `mail_send`, `mail_draft_send` or `send=true` actually send. Do that only when the user said to send, and after they have seen the recipients and text.
- With several accounts, call `status` once, then pass `account`. If Outlook cannot honour it the tool fails without sending.
- Never invent addresses. Resolve names with `recipient_resolve` or `contacts_search`.
- No signature is added automatically; include it in the body if the user wants one.

## Calendar

- `calendar_events` for a date range (recurring meetings are expanded).
- `calendar_free_busy` to find slots, optionally across attendees.
- `calendar_event_create` with attendees saves an unsent meeting unless `send_invites=true`.
- Edit or delete one occurrence of a recurring event by passing `occurrence_start`.
- `calendar_respond` accepts, tentatively accepts or declines a meeting request (message id from the inbox).

## Contacts and tasks

- `contacts_search`, `contact_get`, `contact_save`, `recipient_resolve` (also searches the company address list on Exchange).
- `tasks_list`, `task_save` (create, edit, complete), `task_delete`.

## Limits worth knowing

- Classic Outlook only; the new Outlook for Windows has no COM interface.
- Out-of-office, mail rules and signatures are not exposed by Outlook's object model.
- Dates are local time. Use ISO 8601 (`2026-10-30T14:00`).
