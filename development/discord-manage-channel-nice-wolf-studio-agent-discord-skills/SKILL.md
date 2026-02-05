---
name: discord-manage-channel
description: Manage and update Discord channels via the Discord API. Use this skill when the user wants to modify channel properties, update names/topics, change permissions, or delete channels.
---

# Discord Manage Channel

Manage and update Discord channels using the Discord API v10. This skill supports modifying channel properties including name, topic, position, permissions, and deleting channels.

## When to Use This Skill

Use this skill when the user wants to:
- Rename a Discord channel
- Update a channel's topic/description
- Change channel permissions
- Move a channel to a different category
- Reorder channel positions
- Toggle NSFW status
- Update voice channel settings (user limit, bitrate)
- Delete a channel

## Prerequisites

- `DISCORD_BOT_TOKEN` environment variable must be set
- Bot must be a member of the target server
- Bot must have "Manage Channels" permission in the server
- Valid Discord channel ID (18-19 digit snowflake ID)

## Instructions

When the user requests to manage a Discord channel:

1. **Validate Requirements**
   - Confirm `DISCORD_BOT_TOKEN` is set in environment
   - Verify channel ID is provided (18-19 digit number)
   - Ensure bot has "Manage Channels" permission
   - Validate any new values (name, topic, etc.)

2. **Determine Operation Type**
   - Update (PATCH): Modify channel properties
   - Delete (DELETE): Remove channel permanently

3. **For Updates - Prepare Payload**
   Include only the fields you want to change:
   - `name`: New channel name (2-100 chars, lowercase, hyphens/underscores)
   - `topic`: New topic (max 1024 chars for text channels)
   - `position`: New sort position (integer)
   - `parent_id`: Move to different category (category channel ID or null)
   - `nsfw`: Toggle NSFW status (true/false)
   - `permission_overwrites`: Update permissions (array)
   - `user_limit`: Voice channel user limit (0-99, 0 = unlimited)
   - `bitrate`: Voice channel bitrate (8000-96000 for non-boosted servers)

4. **Make the API Request**

   **Update Channel (PATCH):**
   ```bash
   curl -X PATCH "https://discord.com/api/v10/channels/{CHANNEL_ID}" \
     -H "Authorization: Bot ${DISCORD_BOT_TOKEN}" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "new-channel-name",
       "topic": "New channel topic"
     }'
   ```

   **Delete Channel (DELETE):**
   ```bash
   curl -X DELETE "https://discord.com/api/v10/channels/{CHANNEL_ID}" \
     -H "Authorization: Bot ${DISCORD_BOT_TOKEN}"
   ```

5. **Handle Response**
   - 200 OK (Update): Channel updated successfully
   - 204 No Content (Delete): Channel deleted successfully
   - 400 Bad Request: Invalid parameters
   - 401 Unauthorized: Invalid bot token
   - 403 Forbidden: Missing "Manage Channels" permission
   - 404 Not Found: Channel doesn't exist

6. **Report Results**
   - Confirm operation completed successfully
   - Show what was changed
   - For deletes, warn that operation is permanent
   - If error occurs, explain clearly

## Updatable Properties

### Text Channels

| Property | Type | Description | Validation |
|----------|------|-------------|------------|
| name | string | Channel name | 2-100 chars, lowercase, hyphens/underscores |
| topic | string | Channel topic | Max 1024 characters |
| position | integer | Sort position | Positive integer |
| parent_id | snowflake | Category ID | Valid category ID or null |
| nsfw | boolean | NSFW status | true or false |
| permission_overwrites | array | Permission overrides | Array of permission objects |

### Voice Channels

| Property | Type | Description | Validation |
|----------|------|-------------|------------|
| name | string | Channel name | 2-100 chars |
| position | integer | Sort position | Positive integer |
| parent_id | snowflake | Category ID | Valid category ID or null |
| user_limit | integer | Max users | 0-99 (0 = unlimited) |
| bitrate | integer | Audio quality | 8000-96000 (higher for boosted) |
| permission_overwrites | array | Permission overrides | Array of permission objects |

### Categories

| Property | Type | Description | Validation |
|----------|------|-------------|------------|
| name | string | Category name | 2-100 chars |
| position | integer | Sort position | Positive integer |
| permission_overwrites | array | Permission overrides | Array of permission objects |

## Common Operations

### Rename Channel
```json
{
  "name": "new-channel-name"
}
```

### Update Topic
```json
{
  "topic": "New channel description or topic"
}
```

### Move to Category
```json
{
  "parent_id": "123456789012345678"
}
```

### Remove from Category
```json
{
  "parent_id": null
}
```

### Toggle NSFW
```json
{
  "nsfw": true
}
```

### Update Voice Settings
```json
{
  "user_limit": 10,
  "bitrate": 64000
}
```

### Update Position
```json
{
  "position": 5
}
```

## Permission Overwrites

To update channel permissions:

```json
{
  "permission_overwrites": [
    {
      "id": "role_or_user_id",
      "type": 0,
      "allow": "1024",
      "deny": "2048"
    }
  ]
}
```

Permission structure:
- `id`: Role ID or User ID
- `type`: 0 for role, 1 for user
- `allow`: Bitwise permission value (permissions to grant)
- `deny`: Bitwise permission value (permissions to deny)

Common permission bits:
- `1024` (0x400): VIEW_CHANNEL
- `2048` (0x800): SEND_MESSAGES
- `4096` (0x1000): SEND_TTS_MESSAGES
- `8192` (0x2000): MANAGE_MESSAGES
- `16384` (0x4000): EMBED_LINKS
- `32768` (0x8000): ATTACH_FILES
- `65536` (0x10000): READ_MESSAGE_HISTORY
- `1048576` (0x100000): CONNECT (voice)
- `2097152` (0x200000): SPEAK (voice)

## Deleting Channels

**IMPORTANT:** Channel deletion is permanent and cannot be undone.

Before deleting:
1. Confirm with user that deletion is intentional
2. Warn that all messages will be lost
3. Suggest archiving as alternative if applicable
4. Verify channel ID is correct

Delete command:
```bash
curl -X DELETE "https://discord.com/api/v10/channels/{CHANNEL_ID}" \
  -H "Authorization: Bot ${DISCORD_BOT_TOKEN}"
```

## Error Handling

### Common Errors

**400 Bad Request - Invalid Name**
```json
{
  "code": 50035,
  "errors": {
    "name": {
      "_errors": [{
        "code": "BASE_TYPE_BAD_LENGTH",
        "message": "Must be between 2 and 100 in length."
      }]
    }
  }
}
```

**403 Forbidden - Missing Permissions**
```json
{
  "code": 50013,
  "message": "Missing Permissions"
}
```

**404 Not Found - Channel Doesn't Exist**
```json
{
  "code": 10003,
  "message": "Unknown Channel"
}
```

**400 Bad Request - Invalid Parent**
```json
{
  "code": 50035,
  "message": "Invalid Form Body - parent_id: Unknown category"
}
```

## Rate Limiting

- Channel updates use a shared rate limit bucket
- Limit: 5 requests per 5 seconds per channel
- For bulk updates, add delays between requests
- Wait 1 second between sequential channel updates

## Audit Log

Channel management actions are recorded in the server's audit log:
- Action type: Channel Update (11) or Channel Delete (12)
- Includes: Who made the change, what changed, when
- Visible to users with "View Audit Log" permission

## Best Practices

1. **Validate Before Updating**
   - Check channel name follows Discord rules
   - Verify parent_id exists before moving
   - Validate permission values

2. **Confirm Destructive Actions**
   - Always confirm before deleting channels
   - Warn about permanent data loss
   - Suggest alternatives when appropriate

3. **Batch Updates Carefully**
   - Add delays to respect rate limits
   - Update multiple properties in one request when possible
   - Handle partial failures gracefully

4. **Permission Management**
   - Use role permissions over user permissions when possible
   - Document permission changes
   - Test permissions after updating

5. **Channel Names**
   - Follow server naming conventions
   - Use lowercase with hyphens
   - Keep names descriptive but concise

6. **Category Organization**
   - Keep related channels in same category
   - Use consistent naming within categories
   - Update category permissions to affect children

## Security Notes

- Validate channel belongs to expected server
- Don't expose channel IDs publicly
- Log channel deletions for audit trail
- Require confirmation for destructive operations
- Respect permission hierarchies

## Response Objects

### Update Response (200 OK)
Returns the updated channel object with all properties.

### Delete Response (204 No Content)
Returns empty response on successful deletion.

## Examples

See `examples.md` for detailed usage scenarios.

## API Reference

- Update Endpoint: `PATCH /channels/{channel.id}`
- Delete Endpoint: `DELETE /channels/{channel.id}`
- Discord API Version: v10
- Documentation: https://discord.com/developers/docs/resources/channel#modify-channel
