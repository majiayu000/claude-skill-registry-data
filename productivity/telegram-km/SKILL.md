---
name: telegram_KM
description: >
  Interact with Telegram — read and send messages, browse chats, search conversations,
  manage contacts, check unread messages, and control the Telegram desktop app.
  Uses your real Telegram account via Telethon — full access to all chats, DMs, groups,
  and channels. No bot needed. Use this skill whenever the user mentions Telegram,
  asks about messages in a Telegram chat, wants to send a Telegram message, check
  Telegram notifications, search Telegram conversations, or automate any Telegram
  workflow. Triggers on: "check Telegram", "send a Telegram message", "what's new on
  Telegram", "search Telegram", "my Telegram chats", "Telegram notifications",
  "post to Telegram", or any task involving Telegram communication.
requiredSources:
  - telegram
---
# Telegram

Control Telegram via the `telegram` CLI. Uses Telethon to connect as your real user account — full access to all chats, groups, channels, and contacts. No bot needed.

## CLI Discovery

Locate the binary before any operation:

```bash
TELEGRAM_BIN=$(which telegram 2>/dev/null || \
  find /opt/homebrew/bin /usr/local/bin ~/.local/bin -name telegram -type f 2>/dev/null | head -1)
echo "${TELEGRAM_BIN:-NOT FOUND}"
```

On Mac Studio as of 2026-05-02, `telegram`, `telegram-cli`, and `tg` were absent from `PATH`; Telegram Desktop is at `/Applications/Telegram.app` but exposes no CLI. If `NOT FOUND`: skip this skill until the binary is restored. Do not assume `/opt/homebrew/bin/telegram` exists.

## Pre-Flight Check

Run before any Telegram operation:

```bash
telegram status --json --no-input
```

Expected: `{"connected": true, "username": "..."}`.

- `"connected": false` → run `telegram login`
- Command not found → run CLI Discovery above
- Hangs > 10s → Ctrl-C; `ping -c 3 web.telegram.org`; retry once; if still stuck, check VPN/firewall

Verify session file exists:

```bash
ls -la ~/.telegram-cli/telegram.session
```

Missing file = never logged in or session wiped → `telegram login`.

## First-Time Login

```bash
telegram login
# Enter phone number → verification code → optional 2FA password
```

One-time only. Session persists at `~/.telegram-cli/telegram.session` — no re-auth needed.

## Usage Pattern

Always use `--json --no-input` for programmatic access:

```bash
telegram <command> [args] --json --no-input
```

Check exit code after every write command:

```bash
telegram send @username "Hey!" --no-input; echo "exit: $?"
```

Non-zero = failed. Read stderr for details: `telegram send ... 2>&1`.

## Automation Policy

**Never ask for confirmation before:**
- Reading messages, listing chats, checking unread, searching — all read-only
- Sending or forwarding a message the user explicitly named a target for

**Pause before:**
- Sending to a target the user did not name (ambiguous match)
- Mass sends / bulk forwards touching many chats at once
- Any action involving credentials or gateway restart

## Common Workflows

### List all chats
```bash
telegram chats --limit 30 --json --no-input
```

### Read messages from a chat
```bash
telegram messages "Saved Messages" --limit 20 --json --no-input
telegram messages @durov --limit 10 --json --no-input
```

### Send a message
```bash
telegram send "My Group" "Hello everyone!" --no-input
```

Verify delivery (check `out: true` on the last message):
```bash
telegram messages "My Group" --limit 1 --json --no-input | \
  python3 -c "import json,sys; m=json.load(sys.stdin); print('sent' if m and m[0].get('out') else 'NOT confirmed')"
```

### Search messages
```bash
telegram search "meeting notes" --json --no-input
telegram search "budget" "Work Group" --json --no-input
```

### Check unread
```bash
telegram unread --json --no-input
```

### Multi-step: check unread → read top chat
```bash
TOP=$(telegram unread --json --no-input | python3 -c "
import json, sys
chats = json.load(sys.stdin)
print(chats[0]['name'] if chats else '')
")
[ -n "$TOP" ] && telegram messages "$TOP" --limit 20 --json --no-input
```

### Parse JSON output
```bash
# Extract text of each message
telegram messages @username --limit 10 --json --no-input | \
  python3 -c "import json,sys; [print(m['text']) for m in json.load(sys.stdin) if m.get('text')]"

# With jq
telegram chats --limit 20 --json --no-input | jq '.[].name'
```

## Failure Recovery

| Symptom | Cause | Fix |
|---------|-------|-----|
| `command not found: telegram` | Binary not on PATH | Run CLI discovery; skip skill until restored |
| `{"connected": false}` | Session expired or no session | `telegram login` |
| `~/.telegram-cli/telegram.session` missing | Never logged in or wiped | `telegram login` |
| Command hangs > 10s | Network/VPN or Telegram outage | Ctrl-C; `ping -c 3 web.telegram.org`; retry |
| Non-zero exit on send | Chat name mismatch or API error | `telegram chats --json --no-input \| jq '.[].name'` to find exact name |
| `PEER_ID_INVALID` | Wrong chat identifier format | Use `telegram chats` to get valid ID or exact name |
| `FloodWaitError: N seconds` | Telegram rate limit | Wait N seconds; do not retry immediately |
| JSON parse error | Partial output or error mixed in | `telegram <cmd> --json --no-input 2>&1 \| head -20` to inspect raw |

## Command Reference

| Command | Args | Description |
|---------|------|-------------|
| `login` | — | One-time phone verification |
| `status` | — | Check connection status |
| `me` | — | Your user info |
| `chats` | — | List all chats (--limit N) |
| `messages` | `<chat>` | Read messages (name, @user, or ID) |
| `send` | `<chat> "text"` | Send a message |
| `reply` | `<chat> <msg_id> "text"` | Reply |
| `search` | `"query" [chat]` | Search messages |
| `contacts` | — | List contacts |
| `unread` | — | Show unread chats |
| `forward` | `<from> <msg_id> <to>` | Forward a message |
| `pin` | `<chat> <msg_id>` | Pin a message |
| `media` | `<chat>` | List media files |
| `navigate` | `<user_or_chat>` | Open in Telegram app |
| `screenshot` | `[file]` | Screenshot Telegram window |

## Guidelines

- Chat args accept **partial name matches**, **@usernames**, or numeric IDs
- Uses your REAL user account — full access, same as the app
- Session is permanent at `~/.telegram-cli/telegram.session`
- Parse JSON output with `python3 -c "import json,sys; ..."` or `jq`
- Do not restart the Telegram gateway from within a Telegram-controlled session
