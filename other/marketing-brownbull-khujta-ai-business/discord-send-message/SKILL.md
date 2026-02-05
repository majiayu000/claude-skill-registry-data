---
name: discord-send-message
description: Send messages to Discord channels via the Discord API. Use this skill when the user wants to send text messages, notifications, or formatted content to a Discord channel.
---

# Discord Send Message

Send messages to Discord channels using the Discord API v10. This skill supports plain text messages, formatted markdown content, and embeds.

## When to Use This Skill

Use this skill when the user wants to:
- Send a message to a Discord channel
- Post a notification or announcement
- Send formatted text with markdown
- Post embeds with rich content
- Reply to or interact with Discord programmatically

## Prerequisites

- `DISCORD_BOT_TOKEN` environment variable must be set
- Bot must be a member of the target server
- Bot must have "Send Messages" permission in the target channel
- Valid Discord channel ID (18-19 digit snowflake ID)

## Instructions

When the user requests to send a Discord message:

1. **Validate Requirements**
   - Confirm `DISCORD_BOT_TOKEN` is set in environment
   - Verify channel ID is provided (18-19 digit number)
   - Check that message content is not empty

2. **Prepare the Message**
   - Extract the message content from user request
   - Format any markdown if needed (Discord supports markdown)
   - For embeds, structure as JSON with title, description, color, fields, etc.

3. **Make the API Request**
   Use the following curl command structure:

   ```bash
   curl -X POST "https://discord.com/api/v10/channels/{CHANNEL_ID}/messages" \
     -H "Authorization: Bot ${DISCORD_BOT_TOKEN}" \
     -H "Content-Type: application/json" \
     -d '{"content": "Your message here"}'
   ```

   Replace:
   - `{CHANNEL_ID}` with the actual channel ID
   - `"Your message here"` with the actual message content

4. **Handle Response**
   - Success (200): Message sent successfully, return message ID
   - 401 Unauthorized: Invalid bot token
   - 403 Forbidden: Missing permissions or bot not in server
   - 404 Not Found: Channel doesn't exist or bot can't see it
   - 400 Bad Request: Invalid message content

5. **Report Results**
   - Confirm message was sent successfully
   - Provide the message ID for reference
   - If error occurs, explain the issue clearly

## Message Format Options

### Plain Text
```json
{
  "content": "Hello from Claude Code!"
}
```

### Markdown Formatting
```json
{
  "content": "**Bold text** *Italic text* `code` [Link](https://example.com)"
}
```

### Basic Embed
```json
{
  "embeds": [{
    "title": "Notification",
    "description": "This is an embed message",
    "color": 3447003,
    "fields": [
      {
        "name": "Field Name",
        "value": "Field Value",
        "inline": false
      }
    ]
  }]
}
```

### Text + Embed
```json
{
  "content": "Check out this embed:",
  "embeds": [{
    "title": "Title",
    "description": "Description"
  }]
}
```

## Validation Rules

Before sending:
- Message content must not exceed 2000 characters
- Embed description must not exceed 4096 characters
- Embed title must not exceed 256 characters
- Total embed size must not exceed 6000 characters
- Channel ID must be numeric (snowflake format)

## Error Handling

### Common Errors

**401 Unauthorized**
- Check that `DISCORD_BOT_TOKEN` is set correctly
- Verify token hasn't expired or been regenerated

**403 Forbidden**
- Bot needs "Send Messages" permission in channel
- Bot must be added to the server
- Check channel permission overrides

**404 Not Found**
- Channel ID is incorrect
- Channel was deleted
- Bot doesn't have "View Channel" permission

**400 Bad Request**
- Message content is empty or too long
- Invalid JSON in embed structure
- Invalid embed field values

## Security Notes

- Never expose the bot token in messages or logs
- Validate all user input before sending to Discord
- Don't send sensitive information unless channel is private
- Respect Discord's rate limits (5 messages per 5 seconds per channel)

## Examples

See `examples.md` for detailed usage scenarios.

## API Reference

- Endpoint: `POST /channels/{channel.id}/messages`
- Discord API Version: v10
- Documentation: https://discord.com/developers/docs/resources/channel#create-message
