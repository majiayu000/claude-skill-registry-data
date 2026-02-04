---
name: Using Telegram Notifications
description: This skill enables Telegram notifications for Claude Code sessions, alerting you when tasks complete. Use this when you want to walk away from your computer and be notified on your phone when Claude finishes or needs input.
allowed-tools: [Bash, Read]
---

# Using Telegram Notifications

Get notified on your phone when Claude Code completes tasks or needs input.

## What This Skill Does

- Starts the local webhook server (Claude-Code-Remote daemon)
- Establishes ngrok tunnel for Telegram webhooks
- Enables per-session notification opt-in
- Sends task completion notifications to Telegram
- **Supports swipe-reply** - reply directly to notifications without typing `/cmd TOKEN`
- Falls back to `/cmd TOKEN` format for expired or old notifications

## Architecture Overview

```
┌─────────────────┐    hooks    ┌──────────────────┐
│  Claude Code    │───────────▶│  Webhook Server  │
│   (session)     │            │  (localhost:3001)│
└─────────────────┘            └────────┬─────────┘
                                        │
                                        ▼
                               ┌──────────────────┐
                               │    ngrok tunnel  │
                               └────────┬─────────┘
                                        │
                                        ▼
                               ┌──────────────────┐
                               │   Telegram API   │
                               │  (sends to user) │
                               └──────────────────┘
```

**Flow:**
1. `on-session-start.sh` hook registers session with daemon (captures PID, start_time, tmux pane_id)
2. `/notify-telegram` opts session into notifications
3. `on-stop.sh` / `on-subagent-stop.sh` hooks send stop events
4. Daemon forwards to Telegram via bot API
5. Daemon validates session liveness every 60s (PID + start_time check) and cleans up dead sessions

## Prerequisites

1. **Claude-Code-Remote repository** cloned locally
   - Location: `~/Code/Claude-Code-Remote` (or your preferred location)
   - Branch: `develop`

2. **Telegram bot** configured in Claude-Code-Remote
   - `.env` file with `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`

3. **ngrok** installed with a reserved domain
   - Free tier works but requires manual URL updates
   - Reserved domain recommended for stable webhook URL

4. **Hooks configured** in Claude Code settings
   - Already configured if using this dotfiles repo

## Starting the System

### Step 1: Start the Webhook Server

```bash
cd ~/Code/Claude-Code-Remote
lsof -ti :3001 | xargs kill -9 2>/dev/null; sleep 2 && node start-telegram-webhook.js
```

The `lsof` prefix kills any existing process on port 3001 before starting.

**Expected output:**
```
[Telegram-Webhook-Server] [INFO] Starting Telegram webhook server...
[Telegram-Webhook-Server] [INFO] Configuration:
[Telegram-Webhook-Server] [INFO] - Port: 3001
[Telegram-Webhook-Server] [INFO] - Chat ID: xxxxxxxxx
[Telegram-Webhook-Server] [INFO] - Webhook Secret: Configured
...
```

Keep this running in a dedicated terminal or tmux pane.

### Step 2: Start ngrok Tunnel

In a separate terminal:

```bash
pkill -f ngrok; sleep 2 && ngrok http 3001 --url=rehabilitative-joanie-undefeatedly.ngrok-free.dev
```

The `pkill` prefix kills any existing ngrok process before starting.

**Note:** Replace the URL with your own ngrok domain. If you don't have a reserved domain, ngrok will provide a random URL and you'll need to update the webhook configuration in Claude-Code-Remote.

**Expected output:**
```
Session Status                online
Account                       ...
Forwarding                    https://rehabilitative-joanie-undefeatedly.ngrok-free.dev -> http://localhost:3001
```

Keep this running alongside the webhook server.

### Step 3: Opt Into Notifications

In your Claude Code session, run:

```
/notify-telegram myproject
```

The label (e.g., `myproject`) helps identify which session sent the notification when you have multiple sessions running.

**Verification:**
- Claude will confirm registration
- You should see log output in the webhook server terminal:
  ```
  [TelegramWebhook] [INFO] Notifications enabled for session: <session-id> (myproject)
  ```

## How Notifications Work

### Session Registration

When a Claude Code session starts, the `on-session-start.sh` hook:
1. Creates session tracking files in `~/.claude/runtime/sessions/<session_id>/`
2. Creates pane-map entry (in tmux) or ppid-map entry for session lookup
3. Notifies the daemon of the new session

### Opt-In via /notify-telegram

Running `/notify-telegram <label>`:
1. Looks up the current session ID via pane-map (tmux) or ppid-map (fallback)
2. Registers with the daemon for notifications
3. Writes `notify_label` file for hooks to read

### Stop Events

When Claude stops (task complete or waiting for input):
1. `on-stop.sh` hook fires
2. Reads session_id from hook input (most reliable)
3. Falls back to ppid-map if needed
4. Extracts Claude's last message from transcript
5. Sends to daemon, which forwards to Telegram

### Replying to Notifications

**Swipe-reply (recommended):**
1. Swipe on the notification message in Telegram
2. Type your reply (e.g., "continue" or "yes")
3. Send - the system routes it to the correct Claude session

**How it works:**
- When sending notifications, the daemon stores `message_id -> token` in SQLite
- When you reply to a message, Telegram includes `reply_to_message.message_id`
- The daemon looks up the token and routes your command to the right session
- Message-to-token mappings have 24h TTL
- Command tokens also expire after 24 hours

**Fallback (`/cmd TOKEN`):**
- If the notification is old (>24h) or you've already replied to it
- Use the `/cmd TOKEN <command>` format shown in the notification
- Or use the inline buttons (Continue, Yes, No, Exit)

## Troubleshooting

### Issue: No notification received

**Check webhook server is running:**
```bash
curl -s http://127.0.0.1:3001/health
# Should return JSON with status
```

**Check ngrok is forwarding:**
```bash
curl -s http://127.0.0.1:4040/api/tunnels | jq '.tunnels[0].public_url'
```

**Check session is registered:**
```bash
curl -s http://127.0.0.1:3001/sessions | jq
```

**Check notify_label exists:**
```bash
# Find your session
ls -lt ~/.claude/runtime/ppid-map/ | head -3
cat ~/.claude/runtime/ppid-map/<your-ppid>

# Check notify_label
session_id=$(cat ~/.claude/runtime/ppid-map/<your-ppid>)
cat ~/.claude/runtime/sessions/$session_id/notify_label
```

### Issue: Wrong session receiving notifications

**Possible causes:**

1. **Stale session files** - Old ppid-map or pane-map entries pointing to wrong session
2. **Stale tmux transport data** - If tmux windows were renumbered, the stored `session:window.pane` may point to the wrong pane

**Solutions:**

**Clean up old runtime files:**
```bash
# Remove old ppid-map entries (keep recent ones)
find ~/.claude/runtime/ppid-map -type f -mtime +1 -delete

# Or clean all and restart Claude Code
rm -rf ~/.claude/runtime/ppid-map/*
rm -rf ~/.claude/runtime/pane-map/*
rm -rf ~/.claude/runtime/sessions/*
```

**Restart affected sessions:**
Sessions capture tmux `pane_id` (e.g., `%47`) at startup, which is stable within a tmux server's lifetime. If a session was started before this fix, restart it to pick up proper pane_id tracking.

**Check daemon logs:**
```bash
# Look for injection target issues
cat /tmp/claude/tasks/<daemon-task>.output | grep -E "(inject|target)"
```

### Issue: "Session not found" from daemon

**Cause:** Session didn't register at startup

**Solution:**
1. Restart Claude Code session
2. Re-run `/notify-telegram <label>`

### Issue: Webhook server won't start

**Check port 3001:**
```bash
lsof -i :3001
# Kill any conflicting process
```

**Check .env configuration:**
```bash
cd ~/Code/Claude-Code-Remote
cat .env | grep TELEGRAM
```

### Issue: ngrok tunnel errors

**If using reserved domain:**
- Ensure domain matches exactly (including `.ngrok-free.dev` vs `.app`)
- Check ngrok dashboard for domain status

**If using random URL:**
- Update webhook URL in `.env` after each ngrok restart
- Restart webhook server after changing URL

### Issue: Swipe-reply not working

**"Token expired" message:**
- Command tokens expire after 24 hours
- Use `/cmd TOKEN` format from the notification if available, or wait for next notification

**Reply sent but Claude didn't receive it:**
- Check webhook server logs for injection errors
- Look for `[WARN] nvim injection failed` followed by tmux fallback attempts
- If pane_id is missing, restart the Claude session to capture it

**Check webhook server logs:**
```bash
# Look for injection attempts and errors
cat /tmp/claude/tasks/<daemon-task>.output | tail -50
```

**Check SQLite mapping:**
```bash
# In Claude-Code-Remote directory
sqlite3 src/data/message-tokens.db "SELECT * FROM message_tokens ORDER BY created_at DESC LIMIT 5;"
```

## Runtime File Structure

```
~/.claude/runtime/
├── pane-map/                    # Maps <socket>-<pane> → session_id (preferred in tmux)
│   ├── default-4                # tmux socket "default", pane %4 → session_id
│   └── default-7                # tmux socket "default", pane %7 → session_id
├── ppid-map/                    # Maps PPID → session_id (fallback)
│   ├── 12345                    # Contains session_id
│   └── 67890
└── sessions/
    └── <session-id>/
        ├── transcript_path      # Path to JSONL transcript
        ├── ppid                  # Parent PID for reference
        └── notify_label         # Label for notifications (if opted in)
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `/notify-telegram <label>` | Opt current session into notifications |
| `node start-telegram-webhook.js` | Start webhook server |
| `ngrok http 3001 --url=<your-domain>` | Start tunnel |

| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Health check |
| `GET /sessions` | List registered sessions |
| `POST /sessions/enable-notify` | Enable notifications for session |
| `POST /stop` | Receive stop events from hooks |
| `POST /session-start` | Receive session start events |

## Best Practices

1. **Use meaningful labels**: Label sessions by project/task (e.g., `backend-refactor`, `e2e-tests`)

2. **Keep services in tmux**: Run webhook server and ngrok in dedicated tmux panes so they survive terminal closes

3. **Monitor webhook server logs**: Useful for debugging notification issues

4. **Clean up periodically**: Remove old runtime files to prevent stale session issues

## Related Skills

- **configuring-neovim** - For nvim RPC integration (ccremote plugin)
- **fixing-tmux-socket-issues** - For tmux-related troubleshooting
