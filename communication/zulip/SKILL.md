---
name: zulip
description: Interact with Zulip chat platform via REST API and Python client. Use when you need to read messages from streams/topics, send messages to channels or users, manage DM conversations, list users, or integrate with Zulip organizations for team communication workflows.
---

# Zulip Integration

Interact with Zulip chat platform for team communication.

## Setup

### 1. Install Python Client

```bash
pip install zulip
```

### 2. Create Configuration File

Create `~/.config/zulip/zuliprc`:

```ini
[api]
email=bot@example.zulipchat.com
key=YOUR_API_KEY_HERE
site=https://example.zulipchat.com
```

Get credentials from Zulip admin panel (Settings → Bots).

### 3. Verify Connection

```bash
python scripts/zulip_client.py streams
```

## Quick Start

### Using the Helper Script

The `scripts/zulip_client.py` provides common operations:

**List streams:**
```bash
python scripts/zulip_client.py streams
python scripts/zulip_client.py streams --json
```

**Read messages:**
```bash
# Recent stream messages (by name)
python scripts/zulip_client.py messages --stream "General" --num 10

# By stream ID (more reliable, use 'streams' to find IDs)
python scripts/zulip_client.py messages --stream-id 42 --num 10

# Specific topic
python scripts/zulip_client.py messages --stream "General" --topic "Updates"

# Private messages
python scripts/zulip_client.py messages --type private --num 5

# Mentions
python scripts/zulip_client.py messages --type mentioned
```

**Note:** Stream names may have descriptions that look like part of the name. Use `--stream-id` for unambiguous identification.

**Send messages:**
```bash
# To stream
python scripts/zulip_client.py send --type stream --to "General" --topic "Updates" --content "Hello!"

# Private message (user_id)
python scripts/zulip_client.py send --type private --to 123 --content "Hi there"
```

**List users:**
```bash
python scripts/zulip_client.py users
python scripts/zulip_client.py users --json
```

### Using Python Client Directly

```python
import zulip

client = zulip.Client(config_file="~/.config/zulip/zuliprc")

# Read messages
result = client.get_messages({
    "anchor": "newest",
    "num_before": 10,
    "num_after": 0,
    "narrow": [{"operator": "stream", "operand": "General"}]
})

# Send to stream
client.send_message({
    "type": "stream",
    "to": "General",
    "topic": "Updates",
    "content": "Message text"
})

# Send DM
client.send_message({
    "type": "private",
    "to": [user_id],
    "content": "Private message"
})
```

### Using curl

```bash
# List streams
curl -u "bot@example.com:KEY" https://example.zulipchat.com/api/v1/streams

# Get messages
curl -u "bot@example.com:KEY" -G \
  "https://example.zulipchat.com/api/v1/messages" \
  --data-urlencode 'anchor=newest' \
  --data-urlencode 'num_before=20' \
  --data-urlencode 'num_after=0' \
  --data-urlencode 'narrow=[{"operator":"stream","operand":"General"}]'

# Send message
curl -X POST "https://example.zulipchat.com/api/v1/messages" \
  -u "bot@example.com:KEY" \
  --data-urlencode 'type=stream' \
  --data-urlencode 'to=General' \
  --data-urlencode 'topic=Updates' \
  --data-urlencode 'content=Hello!'
```

## Common Workflows

### Monitor Stream for New Messages

```python
def get_latest_messages(client, stream_name, last_seen_id=None):
    narrow = [{"operator": "stream", "operand": stream_name}]
    
    if last_seen_id:
        # Get only messages after last seen
        request = {
            "anchor": last_seen_id,
            "num_before": 0,
            "num_after": 100,
            "narrow": narrow
        }
    else:
        # Get recent messages
        request = {
            "anchor": "newest",
            "num_before": 20,
            "num_after": 0,
            "narrow": narrow
        }
    
    result = client.get_messages(request)
    return result["messages"]
```

### Reply to Topic

```python
def reply_to_message(client, original_message, reply_text):
    """Reply in the same stream/topic as original message."""
    client.send_message({
        "type": "stream",
        "to": original_message["display_recipient"],
        "topic": original_message["subject"],
        "content": reply_text
    })
```

### Search Messages

```python
def search_messages(client, keyword, stream=None):
    narrow = [{"operator": "search", "operand": keyword}]
    
    if stream:
        narrow.append({"operator": "stream", "operand": stream})
    
    result = client.get_messages({
        "anchor": "newest",
        "num_before": 50,
        "num_after": 0,
        "narrow": narrow
    })
    
    return result["messages"]
```

### Get User ID by Email

```python
def get_user_id(client, email):
    """Find user_id by email address."""
    result = client.get_members()
    
    for user in result["members"]:
        if user["email"] == email:
            return user["user_id"]
    
    return None
```

## Message Formatting

Zulip uses Markdown:

- **Bold:** `**text**`
- **Italic:** `*text*`
- **Code:** `` `code` ``
- **Code block:** ` ```language\ncode\n``` `
- **Quote:** `> quoted text`
- **Mention user:** `@**Full Name**`
- **Link stream:** `#**stream-name**`
- **Link:** `[text](url)`

## Advanced Features

### Upload and Share Files

```python
with open("file.pdf", "rb") as f:
    result = client.upload_file(f)
    file_url = result["uri"]

# Share in message
client.send_message({
    "type": "stream",
    "to": "General",
    "topic": "Files",
    "content": f"Check out [this file]({file_url})"
})
```

### React to Messages

```python
# Add reaction
client.add_reaction({
    "message_id": 123,
    "emoji_name": "thumbs_up"
})

# Remove reaction
client.remove_reaction({
    "message_id": 123,
    "emoji_name": "thumbs_up"
})
```

## Reference

See `references/api-quick-reference.md` for complete API documentation, endpoints, and examples.

## Troubleshooting

**Config file not found:**
- Ensure `~/.config/zulip/zuliprc` exists with correct format
- Check file permissions (should be readable)

**Authentication failed:**
- Verify API key is correct
- Check bot is active in Zulip admin panel
- Ensure site URL matches organization URL

**Empty messages array:**
- Bot might not be subscribed to the stream
- Use `client.get_subscriptions()` to check subscriptions
- Admin may need to add bot to private streams

**Rate limit errors:**
- Standard limit: 200 requests/minute
- Message limit: ~20-30/minute
- Add delays between bulk operations
- Check `Retry-After` header on 429 responses
