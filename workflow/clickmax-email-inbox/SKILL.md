---
name: clickmax-email-inbox
description: Use when the user asks whether a connected company e-mail mailbox is working, wants to change its sender name, signature or Sent-folder sync, or wants to bring the mailbox's recent e-mail history into Conversations.
---

## When this applies

A company mailbox (IMAP/SMTP, e.g. `vendas@`) connected so its e-mails land in Conversations: health check, sending settings (sender name, signature, Sent-folder sync) and the one-time import of recent history.

Not this skill:

- connecting, disconnecting or changing the password/servers of a mailbox -> only in the web app (mailbox page, Atualizar credenciais); never ask the user for a password
- e-mail campaigns/automation e-mails sent through verified sending domains -> `email_sender_signatures_list` + `clickmax-flows`
- validating a contact's e-mail address -> `clickmax-leads`

## Key assumptions

- mailbox id = `id` of a `mcp__plugin_clickmax_clickmax__channel_instances_list` row with `channel = email`; several mailboxes per workspace are normal -> `displayName` is the mailbox address, ask when ambiguous
- visibility: only the workspace owner reaches every mailbox; everyone else (admins too) only those granted to them -> 404 = "not visible to you" as much as "does not exist"
- healthy = `failingSince = null`. Failing -> `lastErrorCode`: `auth_failed` = password refused (usually needs an APP password, normal account password does not work) | `tls_error` = port vs secure option mismatch | `host_not_found` / `connection_refused` / `timeout` = server wrong or down | `credential_unreadable` = re-enter credentials | `host_not_allowed` = server on a private address
- settings update is PARTIAL: omitted = unchanged; `null`/empty = clear. Applies to the next sends only
- signature = composer markup (`*bold*`, `_italic_`, `~strike~`, `- item`, `[text](https://...)`) + optional logo URL that must be `https://`; appended at the end of every reply from that mailbox
- Sent-folder sync mirrors only what is sent AFTER turning it on, and only for contacts that already have an e-mail conversation in that mailbox
- history import: `days = 7 | 30`, ONE SHOT per mailbox forever (409 afterwards, even to widen 7 -> 30), background (~10 e-mails/min), inbox only. Creates contacts and conversations for senders that have none; no unread, no automations, no AI reply; closed conversations stay closed; newsletters/no-reply/automatic e-mails skipped

## Thought process

1. Resolve the mailbox; read `mcp__plugin_clickmax_clickmax__email_mailboxes_get` before any change.
2. Health questions -> translate `lastErrorCode` + `failingSince` into a cause and the user's fix (credentials are fixed by the user in the web app).
3. History import is irreversible and single-use: confirm 7 vs 30 days, and only after `lastSuccessAt` is set.

## Execute guide

- Health: `mcp__plugin_clickmax_clickmax__channel_instances_list` -> pick `channel = email` -> `mcp__plugin_clickmax_clickmax__email_mailboxes_get` with `id`. Report `lastSuccessAt` (last good sync) or `failingSince` + cause.
- Sender name / signature: `mcp__plugin_clickmax_clickmax__email_mailboxes_settings_update` with `id` + only the fields the user asked for. Show the final text back; to remove, send `null`.
- Sent-folder sync: same tool with `syncSentFolder`. Explain the forward-only, existing-conversations-only scope before turning it on.
- History: `mcp__plugin_clickmax_clickmax__email_mailboxes_get` -> `historyImport` must be null and `lastSuccessAt` non-null -> confirm the window -> `mcp__plugin_clickmax_clickmax__email_mailboxes_history_import_start` with `id` + `days`. Progress later via `mcp__plugin_clickmax_clickmax__email_mailboxes_get` (`processed` of `total`; `completedAt` = done).

## Report

- One line per mailbox: address -> Connected (last sync time) | Failing since X (cause in plain words + what the user must do).
- After a settings change: list each changed field with its new value ("sem assinatura" when cleared).
- After starting the import: window, "runs in the background", rough duration, and that old e-mails do not notify or trigger automations.
- Never paste server usernames unless asked; never mention passwords.

## Warnings

- Starting the import on a mailbox that never synced (`lastSuccessAt = null`) spends the single shot and imports nothing.
- The import can create many contacts at once (every human sender of the window); say so before confirming.
- `fromName` cannot contain line breaks; a non-https logo is refused.

## Anti-patterns

- Asking for or handling the mailbox password, or promising to "reconnect" it through the chat.
- Retrying the import after a 409 or offering "30 days now" after 7 days were imported.
- Sending all settings fields when the user asked to change one (blanking a signature by accident).
- Treating 404 as "the mailbox was deleted" without considering access.

---

Clickmax skill revision: `b8294822a4d6`
