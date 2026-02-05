---
name: discord-get-messages
description: Retrieve messages from Discord channels via the Discord API. Use this skill when the user wants to read, search, or analyze messages from a Discord channel.
---

# Discord Get Messages

Retrieve messages from Discord channels using the Discord API v10. This skill supports pagination, filtering by message count, and retrieving message history.

## When to Use This Skill

Use this skill when the user wants to:
- Read recent messages from a Discord channel
- Get message history for analysis
- Search for specific messages in a channel
- Retrieve messages before or after a specific message ID
- Export channel conversation history

## Prerequisites

- `DISCORD_BOT_TOKEN` environment variable must be set
- Bot must be a member of the target server
- Bot must have "Read Message History" permission in the target channel
- Valid Discord channel ID (18-19 digit snowflake ID)

## Instructions

When the user requests to retrieve Discord messages:

1. **Validate Requirements**
   - Confirm `DISCORD_BOT_TOKEN` is set in environment
   - Verify channel ID is provided (18-19 digit number)
   - Validate limit parameter (1-100 messages)

2. **Prepare Query Parameters**
   - `limit`: Number of messages to retrieve (default: 50, max: 100)
   - `before`: Get messages before this message ID (for pagination)
   - `after`: Get messages after this message ID
   - `around`: Get messages around this message ID

3. **Make the API Request**
   Use the following curl command structure:

   ```bash
   curl -X GET "https://discord.com/api/v10/channels/{CHANNEL_ID}/messages?limit=50" \
     -H "Authorization: Bot ${DISCORD_BOT_TOKEN}"
   ```

   Replace:
   - `{CHANNEL_ID}` with the actual channel ID
   - `limit=50` with desired message count (1-100)

4. **Process Response**
   - Messages are returned in reverse chronological order (newest first)
   - Each message contains: id, content, author, timestamp, attachments, embeds
   - Filter or format messages as requested by user

5. **Handle Response Codes**
   - 200 Success: Messages retrieved successfully
   - 401 Unauthorized: Invalid bot token
   - 403 Forbidden: Missing "Read Message History" permission
   - 404 Not Found: Channel doesn't exist or bot can't see it

6. **Present Results**
   - Format messages in a readable way
   - Show author, timestamp, and content
   - Include attachment URLs if present
   - Summarize if many messages retrieved

## Query Parameters

### Limit
```bash
?limit=10  # Get 10 most recent messages (default: 50, max: 100)
```

### Before (Pagination)
```bash
?before=1234567890123456789&limit=50  # Get 50 messages before this message ID
```

### After
```bash
?after=1234567890123456789&limit=50  # Get 50 messages after this message ID
```

### Around
```bash
?around=1234567890123456789&limit=50  # Get 50 messages around this message ID
```

## Message Object Structure

Each message returned contains:
```json
{
  "id": "1234567890123456789",
  "channel_id": "123456789012345678",
  "author": {
    "id": "987654321098765432",
    "username": "Username",
    "discriminator": "0000",
    "avatar": "avatar_hash"
  },
  "content": "Message text content",
  "timestamp": "2025-10-20T12:00:00.000000+00:00",
  "edited_timestamp": null,
  "tts": false,
  "mention_everyone": false,
  "mentions": [],
  "mention_roles": [],
  "attachments": [],
  "embeds": [],
  "reactions": [],
  "pinned": false,
  "type": 0
}
```

## Formatting Output

### Simple Format
```
[2025-10-20 12:00] Username: Message content here
[2025-10-20 11:55] OtherUser: Another message
```

### Detailed Format
```
Message ID: 1234567890123456789
Author: Username#0000 (987654321098765432)
Timestamp: 2025-10-20T12:00:00.000000+00:00
Content: Message text content here
Attachments: image.png (https://cdn.discordapp.com/...)
```

## Filtering and Processing

### Filter by Author
After retrieving messages, filter by author ID or username:
```bash
# Get messages then filter in output
curl ... | jq '.[] | select(.author.username == "TargetUser")'
```

### Filter by Content
Search for specific keywords in message content:
```bash
# Get messages then search content
curl ... | jq '.[] | select(.content | contains("keyword"))'
```

### Get Only Text Messages
Exclude system messages and embeds:
```bash
# Filter message type 0 (default text messages)
curl ... | jq '.[] | select(.type == 0)'
```

## Pagination Strategy

To retrieve more than 100 messages:

1. Get first batch: `?limit=100`
2. Get oldest message ID from response
3. Get next batch: `?before={oldest_id}&limit=100`
4. Repeat until all messages retrieved or desired count reached

**Example:**
```bash
# First batch
curl "https://discord.com/api/v10/channels/{CHANNEL_ID}/messages?limit=100" \
  -H "Authorization: Bot ${DISCORD_BOT_TOKEN}"

# Get oldest message ID from response (e.g., 1234567890123456789)

# Next batch
curl "https://discord.com/api/v10/channels/{CHANNEL_ID}/messages?before=1234567890123456789&limit=100" \
  -H "Authorization: Bot ${DISCORD_BOT_TOKEN}"
```

## Error Handling

### Common Errors

**401 Unauthorized**
- Check that `DISCORD_BOT_TOKEN` is set correctly
- Verify token hasn't expired

**403 Forbidden**
- Bot needs "Read Message History" permission
- Bot needs "View Channel" permission
- Check channel permission overrides

**404 Not Found**
- Channel ID is incorrect
- Channel was deleted
- Bot doesn't have access to channel

**400 Bad Request**
- Invalid limit parameter (must be 1-100)
- Invalid message ID format for before/after/around

## Rate Limiting

- Discord allows 5 requests per 5 seconds per channel
- Implement delays between requests when paginating
- Wait 1 second between pagination requests

## Security Notes

- Never expose the bot token in messages or logs
- Respect user privacy when handling message content
- Don't store messages longer than necessary
- Follow Discord's Terms of Service regarding data retention

## Performance Tips

- Use `limit` parameter to reduce response size
- Retrieve only the messages you need
- Cache results if querying the same channel multiple times
- Use pagination for large history retrieval

## Examples

See `examples.md` for detailed usage scenarios.

## API Reference

- Endpoint: `GET /channels/{channel.id}/messages`
- Discord API Version: v10
- Documentation: https://discord.com/developers/docs/resources/channel#get-channel-messages
