---
name: telecli
description: This skill should be used when the user asks to "send a Telegram message", "poll for Telegram updates", "check Telegram bot status", "respond to Telegram messages", "react to messages", "manage Telegram bot", or mentions Telegram Bot API operations. Provides comprehensive guidance for using the tg CLI to interact with Telegram bots.
---

# Telecli - Telegram Bot CLI

Control Telegram bots via the `tg` command-line interface. All commands output JSON for easy parsing and automation.

## Setup

Configure the bot token (one-time setup):

```bash
# Global config (recommended)
tg config token <your_bot_token>

# Local config (per-directory)
tg config token <your_bot_token> --local

# Or use environment variable
export TELEGRAM_BOT_TOKEN="your_bot_token"
```

Get a bot token from [@BotFather](https://t.me/BotFather) on Telegram.

## Core Commands

### Bot Info

```bash
tg me                    # Get bot information
tg config token          # Show configured tokens
tg config path           # Show config file paths
```

### Polling for Updates

```bash
# Wait indefinitely for updates (loops with 50s timeout until updates arrive)
tg updates poll

# With offset (skip already-processed updates)
tg updates poll --offset 729538157

# Single poll with explicit timeout (for scripts/hooks)
tg updates poll --timeout 5
```

**Polling loop pattern:**
1. Call `tg updates poll` (blocks until updates arrive)
2. Process returned messages
3. Calculate next offset: `max(update_id) + 1`
4. Repeat with `--offset <next_offset>`

### Sending Messages

```bash
# Simple text message
tg message send <chat_id> "Hello!"

# Reply to a specific message
tg message send <chat_id> "Thanks!" --reply-to <message_id>

# With HTML formatting
tg message send <chat_id> "<b>Bold</b> text" --parse-mode HTML

# Forward a message
tg message forward <to_chat_id> <from_chat_id> <message_id>

# Edit a message
tg message edit <chat_id> <message_id> "Updated text"

# Delete a message
tg message delete <chat_id> <message_id>
```

### Reactions

```bash
# Add reaction to a message
tg reaction set <chat_id> <message_id> "👍"
tg reaction set <chat_id> <message_id> "😂"
```

### Media

```bash
# Send photo
tg photo send <chat_id> /path/to/image.jpg
tg photo send <chat_id> /path/to/image.jpg --caption "Nice photo!"

# Send document
tg document send <chat_id> /path/to/file.pdf

# Send voice message
tg voice send <chat_id> /path/to/audio.ogg

# Download file from Telegram
tg file download <file_id> /path/to/save
```

### Chat Management

```bash
# Get chat info
tg chat get <chat_id>

# Get chat member count
tg chat members <chat_id>

# Get chat administrators
tg chat admins <chat_id>

# Leave a chat
tg chat leave <chat_id>
```

## Update Processing

Updates from `tg updates poll` return JSON with this structure:

```json
{
  "ok": true,
  "result": [
    {
      "update_id": 729538157,
      "message": {
        "message_id": 123,
        "from": {
          "id": 12345678,
          "first_name": "User",
          "username": "username"
        },
        "chat": {
          "id": -123456789,
          "title": "Group Name",
          "type": "group"
        },
        "date": 1704067200,
        "text": "Hello bot!"
      }
    }
  ]
}
```

**Key fields:**
- `update_id`: Use max + 1 as next offset
- `message.chat.id`: Target for replies
- `message.message_id`: Use for replies/reactions
- `message.from`: Sender information
- `message.text`: Message content

**Update types:**
- `message`: New message
- `edited_message`: Edited message
- `callback_query`: Inline button press
- `inline_query`: Inline mode query

## Common Patterns

### Reply to Messages

```bash
# Extract info from update
chat_id=$(echo "$update" | jq -r '.message.chat.id')
message_id=$(echo "$update" | jq -r '.message.message_id')
text=$(echo "$update" | jq -r '.message.text')

# Send reply
tg message send "$chat_id" "You said: $text" --reply-to "$message_id"
```

### Continuous Polling Loop

```bash
offset=""
while true; do
  # Blocks until updates arrive (no --timeout = infinite polling)
  result=$(tg updates poll $offset)

  # Process updates
  echo "$result" | jq -c '.result[]' | while read update; do
    # Handle each update
    chat_id=$(echo "$update" | jq -r '.message.chat.id')
    text=$(echo "$update" | jq -r '.message.text')

    # Respond to messages
    if [ -n "$text" ]; then
      tg message send "$chat_id" "Received: $text"
    fi
  done

  # Update offset
  new_offset=$(echo "$result" | jq '[.result[].update_id] | max + 1 // empty')
  if [ -n "$new_offset" ]; then
    offset="--offset $new_offset"
  fi
done
```

### Check for Mentions

```bash
# Check if bot was mentioned
if echo "$text" | grep -qi "@BotUsername"; then
  tg message send "$chat_id" "You called?"
fi
```

## Error Handling

All commands return JSON with `ok` field:

```json
{"ok": true, "result": {...}}   # Success
{"ok": false, "error": "..."}   # Error
```

Check `ok` field before processing results:

```bash
result=$(tg message send 123 "Hello")
if echo "$result" | jq -e '.ok' > /dev/null; then
  echo "Message sent!"
else
  echo "Error: $(echo "$result" | jq -r '.error')"
fi
```

## Additional Resources

### Reference Files

For complete command reference with all options:

- **`references/commands.md`** - Full command reference with all flags and options

### Chat ID Types

- **Positive numbers**: Private chats (user IDs)
- **Negative numbers**: Groups and supergroups
- **@username**: Public channels/groups with usernames
