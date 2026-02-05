---
name: discord-list-channels
description: List all channels in a Discord guild/server via the Discord API. Use this skill when the user wants to see all channels, find specific channels, or audit server structure.
---

# Discord List Channels

List all channels in a Discord guild (server) using the Discord API v10. This skill retrieves all channels including text channels, voice channels, categories, announcement channels, and stage channels.

## When to Use This Skill

Use this skill when the user wants to:
- List all channels in a Discord server
- Find a specific channel by name
- Get channel IDs for use with other operations
- Audit server channel structure
- Filter channels by type (text, voice, category)
- Export channel list for documentation

## Prerequisites

- `DISCORD_BOT_TOKEN` environment variable must be set
- Bot must be a member of the target server
- Bot must have "View Channels" permission (basic permission, usually granted by default)
- Valid Discord guild ID (18-19 digit snowflake ID)

## Channel Types

Channels are returned with the following type values:

| Type | Value | Description |
|------|-------|-------------|
| GUILD_TEXT | 0 | Text channel |
| GUILD_VOICE | 2 | Voice channel |
| GUILD_CATEGORY | 4 | Category (organizes channels) |
| GUILD_ANNOUNCEMENT | 5 | Announcement channel |
| GUILD_STAGE_VOICE | 13 | Stage channel |
| GUILD_FORUM | 15 | Forum channel |

## Instructions

When the user requests to list Discord channels:

1. **Validate Requirements**
   - Confirm `DISCORD_BOT_TOKEN` is set in environment
   - Verify guild ID is provided (18-19 digit number)

2. **Make the API Request**
   Use the following curl command structure:

   ```bash
   curl -X GET "https://discord.com/api/v10/guilds/{GUILD_ID}/channels" \
     -H "Authorization: Bot ${DISCORD_BOT_TOKEN}"
   ```

   Replace `{GUILD_ID}` with the actual guild ID.

3. **Process Response**
   - Channels are returned as an array
   - Each channel includes: id, name, type, position, parent_id, permission_overwrites
   - Sort or filter as requested by user

4. **Handle Response Codes**
   - 200 Success: Channels retrieved successfully
   - 401 Unauthorized: Invalid bot token
   - 403 Forbidden: Bot not in server or missing permissions
   - 404 Not Found: Guild doesn't exist

5. **Present Results**
   - Group channels by category if applicable
   - Show channel names, types, and IDs
   - Format output in a readable structure
   - Highlight requested channels if searching

## Response Structure

Each channel object contains:
```json
{
  "id": "123456789012345678",
  "type": 0,
  "guild_id": "987654321098765432",
  "position": 0,
  "permission_overwrites": [],
  "name": "general",
  "topic": "General discussion",
  "nsfw": false,
  "last_message_id": "111222333444555666",
  "parent_id": null
}
```

Additional fields for voice channels:
```json
{
  "bitrate": 64000,
  "user_limit": 0,
  "rtc_region": null
}
```

## Filtering Channels

### By Type
Filter channels to show only specific types:

```bash
# Get all channels then filter by type
curl -s "https://discord.com/api/v10/guilds/{GUILD_ID}/channels" \
  -H "Authorization: Bot ${DISCORD_BOT_TOKEN}" | \
  jq '.[] | select(.type == 0)'  # Text channels only
```

Type filters:
- `.type == 0` - Text channels
- `.type == 2` - Voice channels
- `.type == 4` - Categories
- `.type == 5` - Announcement channels
- `.type == 13` - Stage channels

### By Name
Search for channels by name:

```bash
# Get channels and search by name
curl -s "https://discord.com/api/v10/guilds/{GUILD_ID}/channels" \
  -H "Authorization: Bot ${DISCORD_BOT_TOKEN}" | \
  jq '.[] | select(.name | contains("general"))'
```

### By Category
List channels in a specific category:

```bash
# Get channels in category with parent_id
curl -s "https://discord.com/api/v10/guilds/{GUILD_ID}/channels" \
  -H "Authorization: Bot ${DISCORD_BOT_TOKEN}" | \
  jq '.[] | select(.parent_id == "category_id_here")'
```

## Organizing Output

### Group by Category
Organize channels by their parent category:

```bash
# List all channels grouped by category
CHANNELS=$(curl -s "https://discord.com/api/v10/guilds/{GUILD_ID}/channels" \
  -H "Authorization: Bot ${DISCORD_BOT_TOKEN}")

# Get categories
echo "$CHANNELS" | jq -r '.[] | select(.type == 4) | .name + " (ID: " + .id + ")"'

# Get channels in each category
for CATEGORY_ID in $(echo "$CHANNELS" | jq -r '.[] | select(.type == 4) | .id'); do
  echo "Channels in category $CATEGORY_ID:"
  echo "$CHANNELS" | jq -r ".[] | select(.parent_id == \"$CATEGORY_ID\") | \"  - \" + .name"
done
```

### Sort by Position
Channels have a `position` field for sorting:

```bash
curl -s "https://discord.com/api/v10/guilds/{GUILD_ID}/channels" \
  -H "Authorization: Bot ${DISCORD_BOT_TOKEN}" | \
  jq 'sort_by(.position)'
```

## Output Formats

### Simple List
```
Channels in server 123456789012345678:
- general (text)
- announcements (announcement)
- voice-chat (voice)
- Community (category)
```

### Detailed List
```
=== Text Channels ===
general (ID: 111222333444555666)
  Topic: General discussion
  NSFW: No

announcements (ID: 111222333444555667)
  Topic: Server updates
  NSFW: No

=== Voice Channels ===
voice-chat (ID: 111222333444555668)
  User Limit: None
  Bitrate: 64kbps

=== Categories ===
Community (ID: 111222333444555669)
```

### Hierarchical List
```
📁 Community (Category)
  💬 general-chat (Text)
  💬 help (Text)
  🔊 Voice Room 1 (Voice)

📁 Administration (Category)
  💬 mod-chat (Text)
  💬 admin-only (Text)

💬 welcome (Text) - No category
📢 announcements (Announcement) - No category
```

### CSV Export
```csv
Channel ID,Name,Type,Category,Topic
111222333444555666,general,text,Community,General discussion
111222333444555667,voice-chat,voice,Community,
111222333444555668,announcements,announcement,,Server updates
```

## Channel Type Labels

When displaying channels, use these labels:

| Type Value | Display Label | Emoji |
|------------|---------------|-------|
| 0 | Text | 💬 |
| 2 | Voice | 🔊 |
| 4 | Category | 📁 |
| 5 | Announcement | 📢 |
| 13 | Stage | 🎙️ |
| 15 | Forum | 💭 |

## Error Handling

### Common Errors

**401 Unauthorized**
- Check that `DISCORD_BOT_TOKEN` is set correctly
- Verify token hasn't expired

**403 Forbidden**
- Bot must be a member of the server
- Bot needs "View Channels" permission
- Check server-level permissions

**404 Not Found**
- Guild ID is incorrect
- Guild was deleted
- Bot is not in the server

## Use Cases

### Find Channel by Name
User wants to find a channel ID by its name.

### Audit Server Structure
User wants to see all channels organized by category.

### Filter by Type
User wants to see only voice channels or only text channels.

### Export Channel List
User wants to export all channel names and IDs for documentation.

### Check Permissions
User wants to see which channels the bot has access to.

## Security Notes

- The bot can only see channels it has permission to view
- Private channels may not appear if bot lacks access
- Permission overwrites don't affect this endpoint's visibility

## Performance

- This endpoint returns all channels in one request
- No pagination needed
- Response is typically fast even for large servers
- Consider caching results for frequently accessed servers

## Best Practices

1. **Cache Results** - Store channel list if querying frequently
2. **Filter Client-Side** - Get all channels once, then filter in code
3. **Sort by Position** - Respect Discord's channel ordering
4. **Group by Category** - Present channels in their organizational structure
5. **Show Channel Types** - Make it clear which channels are text vs voice
6. **Include IDs** - Always show channel IDs for reference
7. **Handle Empty Results** - Check for servers with no channels (rare but possible)

## Examples

See `examples.md` for detailed usage scenarios.

## API Reference

- Endpoint: `GET /guilds/{guild.id}/channels`
- Discord API Version: v10
- Documentation: https://discord.com/developers/docs/resources/guild#get-guild-channels
