---
name: session-check
description: Check your mailbox for incoming messages from other Claude Code sessions. Poll for inter-session communication.
user-invocable: true
argument-hint: "[--mark-read] [--from session-id]"
---

# Session Check

Check your current session's mailbox for messages from other Claude Code sessions.

## How it works

Messages are stored at `~/.claude/mailbox/<your-session-id>/inbox/`. Each message is a JSON file with sender, timestamp, and content.

## Check for messages

### Find your session ID

Your session ID is available from the active sessions file:

```bash
jq -r 'select(.pid == '$$') | .sessionId' ~/.claude/sessions/*.json 2>/dev/null
```

If that doesn't resolve (subshell PID mismatch), list all active sessions and pick the one matching your CWD:

```bash
for f in ~/.claude/sessions/*.json; do
  jq -r '[.sessionId, .cwd] | @tsv' "$f" 2>/dev/null
done
```

### Read inbox

```bash
SESSION_ID="<your-session-id>"
INBOX="${HOME}/.claude/mailbox/${SESSION_ID}/inbox"

if [ -d "$INBOX" ] && [ "$(ls -A "$INBOX" 2>/dev/null)" ]; then
  for msg in "$INBOX"/*.msg.json; do
    jq -r '[.timestamp, .from[0:12], .status, .message[0:120]] | @tsv' "$msg" 2>/dev/null
  done | column -t -s$'\t'
else
  echo "No messages."
fi
```

### Read a specific message in full

```bash
cat "$INBOX/<filename>.msg.json" | jq .
```

### Mark messages as read

```bash
for msg in "$INBOX"/*.msg.json; do
  jq '.status = "read"' "$msg" > "$msg.tmp" && mv "$msg.tmp" "$msg"
done
```

### Filter by sender

```bash
for msg in "$INBOX"/*.msg.json; do
  jq -r --arg from "$FROM_SESSION" 'select(.from | startswith($from))' "$msg" 2>/dev/null
done
```

## Reply

To reply to a message, use `/session-send <from-session-id> <reply text>`.

## Arguments

Parse `$ARGUMENTS` for:
- `--mark-read`: mark all messages as read after displaying
- `--from <session-id>`: show only messages from a specific session
- `--unread`: show only unread messages (default behavior)
- `--all`: show all messages including read ones

## Automatic polling

You can combine this with the built-in `/loop` skill to poll periodically:

```
/loop 2m /session-check
```

This will check for new messages every 2 minutes.
