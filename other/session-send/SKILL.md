---
name: session-send
description: Send a message to another running Claude Code session via file-based message queue. Enables inter-session communication.
user-invocable: true
argument-hint: "<session-id> <message>"
---

# Session Send

Send a message to another running Claude Code session. Since Claude Code has no native inter-session messaging, this uses a file-based message queue that sessions can poll.

## Architecture

Messages are exchanged via a shared directory:

```
~/.claude/mailbox/
├── <session-id>/
│   ├── inbox/
│   │   ├── <timestamp>-<from-session>.msg.json
│   │   └── ...
│   └── outbox/
│       └── <timestamp>-<to-session>.msg.json
```

## Sending a message

### Step 1 — Verify the target session is active

```bash
for f in ~/.claude/sessions/*.json; do
  jq -r 'select(.sessionId | startswith("'"$TARGET_ID"'")) | [.pid, .sessionId, .cwd] | @tsv' "$f" 2>/dev/null
done
```

If no active session matches, warn the user and offer to leave a message anyway.

### Step 2 — Create the message

```bash
MAILBOX="${HOME}/.claude/mailbox/${TARGET_SESSION_ID}/inbox"
mkdir -p "$MAILBOX"

TIMESTAMP=$(date +%s%N | cut -c1-13)
FROM_SESSION="${CLAUDE_SESSION_ID:-unknown}"
MSG_FILE="${MAILBOX}/${TIMESTAMP}-${FROM_SESSION}.msg.json"

cat > "$MSG_FILE" << EOF
{
  "from": "$FROM_SESSION",
  "to": "$TARGET_SESSION_ID",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "message": "$MESSAGE_TEXT",
  "cwd": "$(pwd)",
  "status": "unread"
}
EOF
```

### Step 3 — Confirm delivery

```bash
if [ -f "$MSG_FILE" ]; then
  echo "Message delivered to mailbox: $MSG_FILE"
  echo "The target session needs to run /session-check to see it."
else
  echo "ERROR: Failed to write message"
fi
```

## Arguments

Parse `$ARGUMENTS` for:
- First argument: target session ID (full or partial — resolve via sessions/*.json)
- Remaining arguments: the message text

## Limitations

- This is **asynchronous** — the target session must actively check its mailbox
- No guarantee the target session will read the message (it needs to run `/session-check`)
- Messages persist on disk until manually cleaned up
- For the target to respond, it should use `/session-send <your-session-id> <reply>`

## Cleanup

Remove old messages:

```bash
find ~/.claude/mailbox -name "*.msg.json" -mtime +7 -delete
```

## Related skills

- `/session-list` — find sessions to message
- `/session-read` — inspect what a session is doing before messaging it
- `/session-check` — check your own mailbox for incoming messages
