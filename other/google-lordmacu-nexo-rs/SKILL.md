---
name: Google
description: Gmail, Calendar, Tasks, Drive, Contacts (People), and Photos via Google APIs with OAuth refresh tokens.
requires:
  bins: []
  env:
    - GOOGLE_CLIENT_ID
    - GOOGLE_CLIENT_SECRET
    - GOOGLE_REFRESH_TOKEN
---

# Google

Use this skill when Kate needs to read or act on the user's Google
services: email, calendar, tasks, and Drive files.
The `google` extension implements REST API calls; OAuth refresh tokens
are handled via environment variables.

## Use when

- Read, search, or summarize emails
- List/create/update calendar events
- Query or add Tasks items
- List/download/upload Drive files

## Do not use when

- You want write actions without the corresponding operator write flag
  enabled — the tool returns `-32043`
- You want a full Google API catalog — this extension covers only
  Gmail/Calendar/Tasks/Drive

## Tool surface

**21 tools** grouped by service. Reads are unrestricted; writes are gated.

### Status
- `status` — credential presence, endpoints, write-flag state

### Gmail (5 tools)
- `gmail_list(query?, label_ids?, max_results?, include_spam_trash?, page_token?)` — metadata (id + thread_id)
- `gmail_read(id, format?)` — full message (headers, decoded body_text, labels)
- `gmail_search(query, max_results?)` — `list` alias with required query
- `gmail_send(to, subject, body)` — **requires `GOOGLE_ALLOW_SEND=true`**
- `gmail_modify_labels(id, add_labels?, remove_labels?)` — **gated** (mark_read, archive, trash)

### Calendar (5 tools)
- `calendar_list_calendars`
- `calendar_list_events(calendar_id?, time_min?, time_max?, q?, max_results?, single_events?, order_by?)`
- `calendar_create_event(calendar_id?, summary, description?, location?, start, end, time_zone?, attendees?)` — **requires `GOOGLE_ALLOW_CALENDAR_WRITE=true`**
- `calendar_update_event(calendar_id?, event_id, patch)` — **gated**
- `calendar_delete_event(calendar_id?, event_id)` — **gated**

### Tasks (5 tools)
- `tasks_list_lists(max_results?)`
- `tasks_list_tasks(list_id, show_completed?, show_hidden?, max_results?)`
- `tasks_add(list_id, title, notes?, due?)` — **requires `GOOGLE_ALLOW_TASKS_WRITE=true`**
- `tasks_complete(list_id, task_id)` — **gated**
- `tasks_delete(list_id, task_id)` — **gated**

### Drive (6 tools)
- `drive_list(q?, page_size?, fields?, page_token?, spaces?)`
- `drive_get(id, fields?)`
- `drive_download(id, output_path)` — writes to disk; `output_path` must be under `GOOGLE_DRIVE_SANDBOX_ROOT`
- `drive_upload(source_path, name?, parent_id?, mime_type?)` — **requires `GOOGLE_ALLOW_DRIVE_WRITE=true`**; source path must be under sandbox
- `drive_create_folder(name, parent_id?)` — **gated**
- `drive_delete(id)` — **gated**

## Execution guidance

### Read email
1. `gmail_search query:"is:unread newer_than:1d" max_results:10` → ids
2. `gmail_read id:<id>` for each relevant message → body_text + headers
3. Optional: `gmail_modify_labels` to mark as read (gated)

### Daily summary
1. `calendar_list_events time_min:<today 00:00Z> time_max:<tomorrow 00:00Z>` → agenda
2. `tasks_list_tasks list_id:@default show_completed:false` → pending tasks
3. `gmail_search query:"is:unread"` → urgent inbox

### Process a Drive PDF
1. `drive_list q:"mimeType='application/pdf' and name contains 'factura'"` → id
2. `drive_download id:<id> output_path:/sandbox/factura.pdf` → local
3. `pdf-extract.extract_text path:/sandbox/factura.pdf` → text
4. `summarize.summarize_text text:<...>` → summary

### Anti-patterns

- **Do not expose full email body_text** to end users if it contains
  third-party PII; quote only relevant excerpts.
- **Do not loop `tasks_add`** without confirmation; each call persists a row.
- **Do not download files** that exceed memory limits (hard cap ~50 MB in
  blocking reqwest body); use storage flow for larger payloads.

## Required OAuth scopes

`GOOGLE_REFRESH_TOKEN` must be generated with the required scopes.
Recommended setup (full usage):

```
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/gmail.send
https://www.googleapis.com/auth/gmail.modify
https://www.googleapis.com/auth/calendar.readonly
https://www.googleapis.com/auth/calendar.events
https://www.googleapis.com/auth/tasks
https://www.googleapis.com/auth/drive
```

If your token has read-only scopes, write tools may pass local gating
but Google returns `403 insufficient permissions`, surfaced as
`-32012` Forbidden.

## Errors

| Code | Meaning |
|------|----------------|
| -32011 | unauthorized / refresh failed / missing scope for read calls |
| -32012 | forbidden (missing scope for write calls) |
| -32001 | not found (invalid id) |
| -32013 | rate limited (with `retry_after_secs`) |
| -32043 | write denied — set the required write flag |
| -32602 | bad input (path outside sandbox, malformed URL, invalid enum) |
| -32003 / -32005 / -32004 | transport / timeout / circuit open |
