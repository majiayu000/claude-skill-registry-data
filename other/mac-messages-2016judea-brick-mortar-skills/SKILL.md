---
name: mac-messages
description: Search and read your Apple Messages (iMessage, SMS, RCS) on a Mac straight from the local chat.db, read-only. Use when asked "what did Sam text me about the lease", "find the message with the gate code", "pull my thread with +1 555 0100 from last March", "list my group chats", "export that conversation to markdown", "what photos did she send", or "find a message I deleted". Resolves contact names through the Contacts database and decodes the attributedBody blob that modern macOS stores instead of plain text.
compatibility: macOS; reads local files only; needs Full Disk Access
---

# Mac Messages (local, read-only)

Everything goes through `scripts/messages.py` (Python 3 stdlib only). Nothing leaves the machine.

```bash
python3 scripts/messages.py chats --limit 40                 # conversations, newest first, each with a #number
python3 scripts/messages.py thread "Sam Rivera" --since 2026-03-01 --until 2026-03-31
python3 scripts/messages.py thread "+1 (555) 010-0123" --limit 100
python3 scripts/messages.py thread '#412'                     # a group chat by its number from `chats`
python3 scripts/messages.py search "gate code" --who "Sam" --deleted
python3 scripts/messages.py attachments "Sam Rivera" --since 2026-01-01
python3 scripts/messages.py export "Sam Rivera" --md sam.md   # markdown, one heading per day
```

`<who>` may be a contact name (partial is fine), a phone in any format, an email (iMessage),
a group chat's name, or a `#number` from `chats`. A person resolves to their 1:1 chats only;
use `chats` and the `#number` for a group.

## Where the data is

| what | path |
|---|---|
| messages | `~/Library/Messages/chat.db` (SQLite, WAL; opened `mode=ro`) |
| attachments | `~/Library/Messages/Attachments/xx/yy/<guid>/<file>` (path in `attachment.filename`, starts with `~`) |
| contact names | `~/Library/Application Support/AddressBook/Sources/*/AddressBook-v22.abcddb` (one per account) |

Joins: `message` -> `chat_message_join` -> `chat`; `message.handle_id` -> `handle.id` (the phone/email);
`chat_handle_join` gives a chat's members; `message_attachment_join` -> `attachment`.
`chat.style` 43 = group, 45 = one-to-one. `chat.service_name` is iMessage, SMS or RCS.

## Schema traps (each one returns a plausible wrong answer)

- **`message.text` is NULL for most modern messages.** The body is in `attributedBody`, an
  NSArchiver typedstream. After the bytes `NSString` comes `... + <len> <utf-8>`; `<len>` is one byte,
  or `0x81` + uint16 LE, or `0x82` + uint32 LE. Read the length; regex-trimming the blob truncates
  long messages and mangles emoji. `decode_body()` does this.
- **Text search must run after decoding.** `WHERE text LIKE` silently misses most messages.
- **Dates** are nanoseconds since 2001-01-01 (older rows: seconds). `ts()` handles both.
- **Recently Deleted** messages lose their `chat_message_join` row and move to
  `chat_recoverable_message_join (chat_id, message_id, delete_date)`. A query that inner-joins
  `chat_message_join` never sees them; the script excludes them by default and includes them with
  `--deleted` (shown as `[DELETED]`). People who clear threads often have most recent history here.
- **Tapbacks are messages** (`associated_message_type` 2000-3007). They are filtered out.
- **U+FFFC** in a body is an inline attachment placeholder; printed as `[attachment]`.
- **Phone formats differ** between `handle.id` (`+15550100123`) and Contacts (`(555) 010-0123`).
  Both are normalised to E.164 before matching (US default; numbers starting `+` keep their code).
- **Attachments may be iCloud-only.** If Messages in iCloud has offloaded them, the path exists in
  the DB but not on disk; the script says "not downloaded".

## Optional: an archive that never prunes

macOS purges Recently Deleted after about 30 days, and deleting on the phone deletes the Mac copy.
`messages.py archive sync` copies every row (deleted ones included) into
`~/Library/Application Support/mac-messages-archive/archive.db` and keeps it forever, marking rows
that later vanish from the Mac as `PURGED`. `messages.py archive search "text"` searches it. To run it
hourly, a launchd agent with `StartInterval` 3600 calling `archive sync` is enough. This is the only
command that writes, and it writes only to its own file.

## Permission (TCC)

`chat.db` is protected by Full Disk Access. Without it you get `unable to open database file` or
`Operation not permitted`. Grant it: System Settings > Privacy & Security > Full Disk Access >
`+` > the app running the agent (Terminal, iTerm, VS Code, Cursor, or the Claude desktop app), then
quit and reopen that app. Check with `ls ~/Library/Messages`.

## Alternative

An iMessage MCP server (several open-source ones read this same `chat.db`) gives the agent the same
reads as tools. Use it if one is installed; this skill needs nothing but Python.

## Limits

Read-only: sending needs AppleScript and Automation permission, out of scope here. Only messages
synced to this Mac exist in `chat.db`.
