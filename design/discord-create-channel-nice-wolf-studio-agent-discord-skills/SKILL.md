---
name: discord-create-channel
description: Create new channels in Discord guilds/servers via the Discord API. Use this skill when the user wants to create text channels, voice channels, announcement channels, or categories in a Discord server.
---

# Discord Create Channel

Create new channels in Discord guilds (servers) using the Discord API v10. This skill supports creating text channels, voice channels, announcement channels, stage channels, and categories.

## When to Use This Skill

Use this skill when the user wants to:
- Create a new text channel in a Discord server
- Create a new voice channel for meetings or discussions
- Create an announcement channel for server updates
- Create a category to organize channels
- Set up a new channel with specific permissions
- Create a stage channel for large audio events

## Prerequisites

- `DISCORD_BOT_TOKEN` environment variable must be set
- Bot must be a member of the target server
- Bot must have "Manage Channels" permission in the server
- Valid Discord guild ID (18-19 digit snowflake ID)

## Channel Types

Discord supports the following channel types (use numeric value):

| Type | Value | Description |
|------|-------|-------------|
| GUILD_TEXT | 0 | Text channel |
| GUILD_VOICE | 2 | Voice channel |
| GUILD_CATEGORY | 4 | Category (organizes channels) |
| GUILD_ANNOUNCEMENT | 5 | Announcement channel (one-way communication) |
| GUILD_STAGE_VOICE | 13 | Stage channel (audio events) |

## Instructions

When the user requests to create a Discord channel:

1. **Validate Requirements**
   - Confirm `DISCORD_BOT_TOKEN` is set in environment
   - Verify guild ID is provided (18-19 digit number)
   - Ensure channel name is valid (2-100 characters, lowercase, hyphens/underscores only)
   - Determine channel type (default to text channel if not specified)

2. **Prepare Channel Properties**
   - `name`: Channel name (required, 2-100 chars)
   - `type`: Channel type (0=text, 2=voice, 4=category, 5=announcement, 13=stage)
   - `topic`: Channel topic/description (optional, max 1024 chars for text channels)
   - `parent_id`: Category ID to place channel in (optional)
   - `nsfw`: Whether channel is NSFW (optional, default false)
   - `position`: Sort position (optional)
   - `permission_overwrites`: Permission overrides (optional, array)

3. **Make the API Request**
   Use the following curl command structure:

   ```bash
   curl -X POST "https://discord.com/api/v10/guilds/{GUILD_ID}/channels" \
     -H "Authorization: Bot ${DISCORD_BOT_TOKEN}" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "channel-name",
       "type": 0
     }'
   ```

   Replace:
   - `{GUILD_ID}` with the actual guild ID
   - `"channel-name"` with the desired channel name
   - `0` with the appropriate channel type

4. **Handle Response**
   - 201 Created: Channel created successfully, return channel ID
   - 400 Bad Request: Invalid channel name or parameters
   - 401 Unauthorized: Invalid bot token
   - 403 Forbidden: Missing "Manage Channels" permission
   - 404 Not Found: Guild doesn't exist or bot not in server

5. **Report Results**
   - Confirm channel was created successfully
   - Provide the channel ID for reference
   - Include channel URL for easy access
   - If error occurs, explain the issue clearly

## Channel Name Validation

Discord channel names must follow these rules:
- 2-100 characters in length
- Lowercase letters, numbers, hyphens, and underscores only
- No spaces (use hyphens instead)
- No special characters or emojis

**Valid names:**
- `general`
- `general-chat`
- `voice-room-1`
- `announcements`

**Invalid names:**
- `General Chat` (has spaces and capital letters)
- `chat!` (has special character)
- `a` (too short)
- `café` (has accented character)

## Creating Different Channel Types

### Text Channel (Type 0)
```json
{
  "name": "general-chat",
  "type": 0,
  "topic": "General discussion for all members"
}
```

### Voice Channel (Type 2)
```json
{
  "name": "voice-lounge",
  "type": 2,
  "user_limit": 10
}
```

### Category (Type 4)
```json
{
  "name": "Community",
  "type": 4
}
```

### Announcement Channel (Type 5)
```json
{
  "name": "server-updates",
  "type": 5,
  "topic": "Official server announcements"
}
```

### Stage Channel (Type 13)
```json
{
  "name": "community-stage",
  "type": 13
}
```

## Setting Channel in Category

To place a new channel in an existing category:

```json
{
  "name": "new-channel",
  "type": 0,
  "parent_id": "123456789012345678"
}
```

The `parent_id` is the ID of the category channel.

## Channel Permissions

To set custom permissions when creating a channel:

```json
{
  "name": "private-channel",
  "type": 0,
  "permission_overwrites": [
    {
      "id": "role_id_here",
      "type": 0,
      "allow": "1024",
      "deny": "0"
    }
  ]
}
```

Permission types:
- `type: 0` = Role
- `type: 1` = Member

Common permission values:
- `1024` = View Channel
- `2048` = Send Messages
- `8192` = Read Message History
- `65536` = Mention Everyone

## Error Handling

### Common Errors

**400 Bad Request - Invalid Name**
```json
{
  "code": 50035,
  "errors": {
    "name": {
      "_errors": [
        {
          "code": "BASE_TYPE_BAD_LENGTH",
          "message": "Must be between 2 and 100 in length."
        }
      ]
    }
  }
}
```
**Solution:** Ensure channel name is 2-100 characters and follows naming rules

**403 Forbidden - Missing Permissions**
```json
{
  "code": 50013,
  "message": "Missing Permissions"
}
```
**Solution:** Bot needs "Manage Channels" permission in the server

**404 Not Found - Invalid Guild**
```json
{
  "code": 10004,
  "message": "Unknown Guild"
}
```
**Solution:** Verify guild ID is correct and bot is member of the server

**400 Bad Request - Invalid Category**
```json
{
  "code": 50035,
  "message": "Invalid parent_id"
}
```
**Solution:** Ensure parent_id is a valid category channel ID in the same guild

## Response Object

Successful channel creation returns:
```json
{
  "id": "987654321098765432",
  "type": 0,
  "guild_id": "123456789012345678",
  "position": 0,
  "permission_overwrites": [],
  "name": "new-channel",
  "topic": null,
  "nsfw": false,
  "last_message_id": null,
  "parent_id": null
}
```

## Best Practices

1. **Naming Conventions**
   - Use descriptive, lowercase names
   - Use hyphens to separate words
   - Keep names concise but clear

2. **Organization**
   - Create categories first, then channels within them
   - Use consistent naming across similar channels
   - Set appropriate permissions from the start

3. **Channel Limits**
   - Discord servers have a limit of 500 channels
   - Consider channel count before creating new ones
   - Archive or delete unused channels

4. **Permissions**
   - Set permissions during creation when possible
   - Use role-based permissions over member-specific
   - Inherit category permissions when appropriate

5. **Voice Channels**
   - Set reasonable user limits
   - Consider bitrate for quality
   - Use stage channels for large events

## Security Notes

- Validate guild ID belongs to expected server
- Don't create channels programmatically without user confirmation
- Be cautious with permission overwrites
- Follow Discord's automation guidelines

## Examples

See `examples.md` for detailed usage scenarios.

## API Reference

- Endpoint: `POST /guilds/{guild.id}/channels`
- Discord API Version: v10
- Documentation: https://discord.com/developers/docs/resources/guild#create-guild-channel
