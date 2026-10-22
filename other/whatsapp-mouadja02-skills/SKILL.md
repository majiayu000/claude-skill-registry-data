---
name: whatsapp
description: >-
  Routes WhatsApp work to the right tool: wacrawl for read-only local history and search, wacli for
  live sync, sending, and chat or group changes, with safety rules for sending. Use for any WhatsApp
  history, search, read, or send request.
source: "https://github.com/steipete/agent-scripts"
attribution: "steipete/agent-scripts by Peter Steinberger"
version: "1.0.0"
license: MIT
---

# WhatsApp

> **Attribution:** Sourced from [steipete/agent-scripts](https://github.com/steipete/agent-scripts) by [Peter Steinberger](https://github.com/steipete).

Use this as the first stop for WhatsApp work. Keep the source boundary sharp:

- **Archive/local history**: use `wacrawl` — read-only, best local history, no network, no sending.
- **Live/sending**: use `wacli` — linked-device accounts, live sync, auth, sending, chat/group mutations.

## Routing

- Primary WhatsApp reads/search/history → `wacrawl`
- Alt accounts or live sends → `wacli --account NAME`
- Sending, reactions, archive/pin/mark-read, group mutations → `wacli` only after **explicit user intent**

## Safety

- Never send or mutate WhatsApp state unless explicitly requested.
- Prefer read-only `wacli` commands for inspection: pass `--read-only` or set `WACLI_READONLY=1`.
- Do not write into WhatsApp Desktop's app container.
- Report source freshness, account name, and known gaps when answering from local stores.

## Common Commands (Archive/wacrawl)

```bash
# Status and sync
wacrawl status
wacrawl doctor
wacrawl sync

# Unread triage
wacrawl chats --limit 20
wacrawl unread --limit 20
wacrawl --json unread --limit 100

# Search and slice messages
wacrawl messages --after 2025-01-01 --limit 50
wacrawl messages --chat JID --asc --limit 100
wacrawl --json search "query"
wacrawl search "query" --after 2025-01-01 --from-them
```

## Common Commands (Live/wacli)

```bash
# Account discovery
wacli accounts list --json
wacli --account me auth status --read-only --json

# Read-only inspection
wacli --account me chats list --read-only --json
wacli --account me messages list --read-only --json --limit 50
wacli --account me messages search --read-only --json "query"

# Send (only when explicitly requested)
wacli --account me send text --to JID_OR_NAME --message "message"
```

## Notes

- `wacrawl` = WhatsApp Desktop archive (most complete history).
- `wacli` = linked-device protocol client (live, alt accounts).
- JID format: `[country][phone]@s.whatsapp.net` for individuals, `[id]@g.us` for groups.
