---
name: imessage
description: Send, read, export iMessage/SMS via imsg and chat.db.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [iMessage, SMS, messaging, macOS, Apple]
prerequisites:
  commands: [imsg]
---

# iMessage

Use `imsg` to read and send iMessage/SMS via macOS Messages.app.

## Prerequisites

- **macOS** with Messages.app signed in
- Install: `brew install steipete/tap/imsg`
- Grant Full Disk Access for terminal (System Settings → Privacy → Full Disk Access)
- Grant Automation permission for Messages.app when prompted

## When to Use

- User asks to send an iMessage or text message
- Reading iMessage conversation history
- Checking recent Messages.app chats
- Sending to phone numbers or Apple IDs
- Exporting message history to files → see Export Full History

## When NOT to Use

- Telegram/Discord/Slack/WhatsApp messages → use the appropriate gateway channel
- Group chat management (adding/removing members) → not supported
- Bulk/mass messaging → always confirm with user first

## Quick Reference

### List Chats

```bash
imsg chats --limit 10 --json
```

### View History

```bash
# By chat ID
imsg history --chat-id 1 --limit 20 --json

# With attachments info
imsg history --chat-id 1 --limit 20 --attachments --json
```

### Send Messages

```bash
# Text only
imsg send --to "+14155551212" --text "Hello!"

# With attachment
imsg send --to "+14155551212" --text "Check this out" --file /path/to/image.jpg

# Force iMessage or SMS
imsg send --to "+14155551212" --text "Hi" --service imessage
imsg send --to "+14155551212" --text "Hi" --service sms
```

### Watch for New Messages

```bash
imsg watch --chat-id 1 --attachments
```

## Export Full History

`imsg` has no export command, and `imsg history` only returns messages that still have a
chat row. Every conversation the user deleted from Messages is invisible to it even though
its rows remain in `chat.db` — on a real Mac that gap is most of the history (measured:
5,129 messages via imsg vs 23,673 rows in the database, 74% of them orphaned). Never
export via `imsg chats` + `imsg history` per chat and call it "your message history".

Read the database directly, read-only so Messages.app is undisturbed:

```bash
sqlite3 "file:$HOME/Library/Messages/chat.db?mode=ro" "select count(*) from message;"
```

Then run the exporter that already exists instead of writing one:

```bash
imsg-export all ~/imessage-export       # export → README → audit; exits 1 if the audit fails
imsg-export export ~/imessage-export    # export only
imsg-export verify ~/imessage-export    # audit only
```

Installed as a uv tool (`~/.local/bin/imsg-export`), source `<imsg-export-repo>`,
published as `imsg-export`. On a machine without it:
`uvx imsg-export all <dir>`. Flags: `--db PATH` for a copied or mounted database,
`--no-contacts` to skip the optional `imsg` lookup for contact names. Stdlib only.

It writes `messages.jsonl`, `all-messages.csv`, `chats.json`, timestamped per-chat
transcripts, orphaned-conversation transcripts, recovered attachments with a `manifest.csv`,
and `summary.json`. If it is unavailable, rebuild from `references/history-export.md`
rather than writing a chat-join query from scratch.

Reconcile before reporting, and reconcile by identity rather than count:

- every `message.ROWID` in the database is present in `messages.jsonl`, and no row in the
  export is absent from the database
- text matches the database on every row whose `text` is non-null (about half of rows store
  their body only in `attributedBody`)
- one `attachments/manifest.csv` row per `message_attachment_join` row

A matching line count alone still hides a dropped conversation when another chat
double-counts, so always set-diff the ids both ways. Then say plainly what is unrecoverable:
purged attachment blobs are gone from disk, but the message row, filename and timestamp
survive and every reference is listed in the manifest — do not imply a lossless backup.

Schema, the Apple epoch, `attributedBody` decoding and reaction-guid formats are in
`references/history-export.md`.

## Service Options

- `--service imessage` — Force iMessage (requires recipient has iMessage)
- `--service sms` — Force SMS (green bubble)
- `--service auto` — Let Messages.app decide (default)

## Rules

1. **Always confirm recipient and message content** before sending
2. **Never send to unknown numbers** without explicit user approval
3. **Verify file paths** exist before attaching
4. **Don't spam** — rate-limit yourself
5. **Exports: attribute honestly.** Deleted conversations keep their message rows but lose
   their chat record, so the counterparty is gone for messages you _sent_. Bucket those as
   unattributed; do not reconstruct conversations by time proximity and present it as history.

## Example Workflow

User: "Text mom that I'll be late"

```bash
# 1. Find mom's chat
imsg chats --limit 20 --json | jq '.[] | select(.displayName | contains("Mom"))'

# 2. Confirm with user: "Found Mom at +1555123456. Send 'I'll be late' via iMessage?"

# 3. Send after confirmation
imsg send --to "+1555123456" --text "I'll be late"
```
