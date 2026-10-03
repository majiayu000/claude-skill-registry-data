---
name: whatsapp-log-reader
description: "Use when the user asks to read/list/show the WhatsApp messages received by the bot, inspect gateway WhatsApp logs, or audit what the bot received (including messages it did not reply to)."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [whatsapp, logs, gateway, audit, messages]
    related_skills: [hermes-whatsapp]
---

# WhatsApp Log Reader

## Overview

Reads the WhatsApp / Telegram messages that the Hermes gateway received, directly from the
gateway logs under `$HERMES_HOME/logs/gateway.log*` (default `~/.hermes`). This is the authoritative
record of everything that arrived on WhatsApp — **including messages the bot had
no permission to reply to**. Useful for auditing, debugging, or answering
"what did the group send me?"

## When to Use

- "Read received WhatsApp messages" / "what did people send me on WhatsApp?"
- Audit what the bot received (groups, users)
- Find a specific message from a user or date
- Check whether a message was actually received (even if there was no reply)

## Script

Path: `$HERMES_HOME/scripts/read_all.py` (default `~/.hermes`)

The script reads **WhatsApp, Telegram, or both**, depending on `--platform`
(highest priority) / the `MSG_PLATFORM` env var / default `whatsapp`.

```bash
# WhatsApp only (default)
python3 "${HERMES_HOME:-$HOME/.hermes}/scripts/read_all.py"

# Telegram only
python3 "${HERMES_HOME:-$HOME/.hermes}/scripts/read_all.py" --platform telegram

# Both platforms
python3 "${HERMES_HOME:-$HOME/.hermes}/scripts/read_all.py" --platform all

# Via env var (overrides the default only)
MSG_PLATFORM=all python3 "${HERMES_HOME:-$HOME/.hermes}/scripts/read_all.py"

# Last 7 days, readable format grouped by date
python3 "${HERMES_HOME:-$HOME/.hermes}/scripts/read_all.py" --days 7

# Filter by user
python3 "${HERMES_HOME:-$HOME/.hermes}/scripts/read_all.py" --user "Yoel"

# Filter by chat (group ID)
python3 "${HERMES_HOME:-$HOME/.hermes}/scripts/read_all.py" --chat "120363411854253534@g.us"

# Raw one-line format
python3 "${HERMES_HOME:-$HOME/.hermes}/scripts/read_all.py" --raw

# Cap how many messages are shown
python3 "${HERMES_HOME:-$HOME/.hermes}/scripts/read_all.py" --days 30 --limit 50
```

On display, a flag indicates the platform: 🟢 = WhatsApp, 🔵 = Telegram.

## How It Works

- Reads `gateway.log` plus rotated files (`gateway.log.1/2/3`)
- Regex-matches lines `inbound message: platform=whatsapp user=... chat=... msg='...'`
- Returns date/time, user, chat, and message content

## Media / Images

Media messages (photos, videos, stickers…) appear in the log as
`[image received]` (or `msg=''`). The script:

1. Detects the media marker (`[image received]`, `[video received]`, `[sticker received]`, … or an empty message)
2. Looks up the real file under `$HERMES_HOME/cache/images/` by **matching the message timestamp to the file's modification time** (~180s tolerance window)
3. Prints the file's **absolute path** under the message

```
### 2026-08-21
**10:38** — Acher Klein : [image received]
   📁 `$HERMES_HOME/cache/images/img_038d532291bd.jpg`
```

⚠️ The script shows the media file *path*, not its contents — to inspect the
image visually, use a separate vision tool on that path.

## 🔧 Upstream code improvement (rebase this)

The media path is **also** exposed directly in gateway logs after the change
below. Include it in any PR / share so the timestamp heuristic can be dropped.

**File:** `gateway/run.py`
**Function:** `_handle_message_with_agent`
**Lines:** ~11989–11996 (in the installed version; may vary by
version — search for `_msg_preview = (event.text or "")[:80]` and the
`logger.info("inbound message: ...")` just below).

```python
# above logger.info("inbound message: ..."):
_media_paths = getattr(event, "media_urls", None) or []
_media_preview = " | media=" + ",".join(str(p) for p in _media_paths[:3]) if _media_paths else ""
```

Then add `%s` (`_media_preview`) to the log format string.
Concretely, replace these 3 logger lines:

```python
logger.info(
    "inbound message: platform=%s user=%s chat=%s msg=%r%s reply_to_id=%s reply_to_text=%r",
    _platform_name, source.user_name or source.user_id or "unknown",
    source.chat_id or "unknown", _msg_preview, _media_preview, _reply_id, _reply_txt,
)
```

Log result:
```
inbound message: platform=whatsapp user=Acher user=... msg='[image received]' | media=$HERMES_HOME/cache/images/img_xxx.jpg reply_to_id=...
```

Covers **all** platforms (WhatsApp, Telegram, Signal…) because the handler
is generic and reads `event.media_urls` (shared across adapters).
⚠️ Requires a gateway restart to take effect.

## Common Pitfalls

1. **Names with spaces** — user names contain spaces
   (`Acher Klein`). The regex captures everything after `user=` until ` chat=`.
2. **Telegram messages** — the log mixes telegram and whatsapp. The script
   keeps only `platform=whatsapp`.
3. **Rotated logs** — older messages may live in `gateway.log.1/.2/.3`
   depending on size. The script reads all of them.
4. **Privacy** — these messages come from other people. Do not
   share them outside the context of the system owner.

## Verification Checklist

- [ ] Non-empty output when messages exist
- [ ] Dates grouped correctly
- [ ] `--user` filters by name
- [ ] Both `--raw` and the readable format work
