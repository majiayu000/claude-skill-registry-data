---
name: beeper
description: "Beeper cache: contact hints, room lookup, WhatsApp/iMessage traces, FTS."
---

# Beeper

Use for local Beeper history questions, especially vague contact hints across iMessage/WhatsApp bridges.

## Source

- DB: `~/Library/Application Support/BeeperTexts/index.db`
- FTS: `mx_room_messages_fts`

Inspect accounts/rooms before broad searching.

## Workflow

1. Identify likely account/bridge/room from `accounts`, `participants`, room tables.
2. FTS for text discovery.
3. Narrow by date, participant, room.
4. Report room/account names, date spans, confidence.

Probes:

```bash
sqlite3 "$HOME/Library/Application Support/BeeperTexts/index.db" \
  "select * from accounts limit 20;"
```

```bash
sqlite3 "$HOME/Library/Application Support/BeeperTexts/index.db" \
  "select rowid, content from mx_room_messages_fts where mx_room_messages_fts match 'query' limit 20;"
```

Keep results local; DB contains private messages.
