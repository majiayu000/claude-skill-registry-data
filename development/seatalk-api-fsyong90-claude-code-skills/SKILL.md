---
name: seatalk-api
description: Use this skill when working with Seatalk (Sea's enterprise messaging platform) integrations, bot development, group chat automation, or messaging APIs.
---

# Seatalk Open Platform API

Use this skill when working with Seatalk (Sea's enterprise messaging platform) integrations, bot development, group chat automation, or messaging APIs.

## Quick Reference

### Base URL
```
https://openapi.seatalk.io
```

### Authentication
```bash
# Get access token (expires in 7200 seconds / 2 hours)
POST https://openapi.seatalk.io/auth/app_access_token
Content-Type: application/json

{
  "app_id": "your_app_id",
  "app_secret": "your_app_secret"
}

# Response
{
  "code": 0,
  "app_access_token": "c8bda0f77ef940c5bea9f23b2d7fc0d8",
  "expire": 1590581487
}

# Use token in requests
Authorization: Bearer {app_access_token}
```

### Rate Limits

| API | Limit |
|-----|-------|
| Most APIs | 1000/min |
| Get Access Token | 600/hour |
| Send Message to Bot User | 300/min |
| Send Message to Group Chat | 100/min |
| Get Group Info | 100/min |
| Get Chat History | 100/min |
| Get Thread by Thread ID | 100/min |
| Create Group Chat | 100/day, 10/min |
| Add/Remove Group Members | 10 groups/min |

## Core APIs

### Send Message to Group Chat
```bash
POST https://openapi.seatalk.io/messaging/v2/group_chat
Content-Type: application/json
Authorization: Bearer {token}

# Text message
{
  "group_id": "abc123",
  "message": {
    "tag": "text",
    "text": {
      "format": 1,  // 1=Markdown, 2=Plain
      "content": "Hello **world**!"
    }
  }
}

# Image message (Base64, max 5MB)
{
  "group_id": "abc123",
  "message": {
    "tag": "image",
    "image": {
      "content": "base64_encoded_image_data"
    }
  }
}

# Interactive message card
{
  "group_id": "abc123",
  "message": {
    "tag": "interactive_message",
    "interactive_message": {
      "elements": [
        {"element_type": "title", "title": {"text": "Card Title"}},
        {"element_type": "description", "description": {"text": "Description here"}},
        {"element_type": "button", "button": {"button_type": "callback", "text": "Click Me", "value": "action1"}}
      ]
    }
  }
}

# Thread reply (include thread_id)
{
  "group_id": "abc123",
  "thread_id": "thread_message_id",
  "message": {...}
}
```

### Send Message to Bot User (1-on-1)
```bash
POST https://openapi.seatalk.io/messaging/v2/single_chat
Content-Type: application/json
Authorization: Bearer {token}

{
  "employee_code": "e_12345678",
  "message": {
    "tag": "text",
    "text": {
      "format": 1,
      "content": "Hello from bot!"
    }
  },
  "usable_platform": "all"  // "all", "mobile", or "desktop"
}
```

### Send Service Notice
```bash
POST https://openapi.seatalk.io/messaging/v2/service_notice/send_message
Content-Type: application/json
Authorization: Bearer {token}

{
  "tag": "interactive_message",
  "interactive_message": {
    "default": {
      "elements": [
        {"element_type": "title", "title": {"text": "Notice Title"}},
        {"element_type": "description", "description": {"text": "Notice content"}}
      ]
    }
  },
  "employee_codes": ["emp1", "emp2"]  // 1-50 recipients
}
```

### Create Group Chat
```bash
POST https://openapi.seatalk.io/messaging/v2/group_chat/create_group
Content-Type: application/json
Authorization: Bearer {token}

{
  "group_owner": "owner_employee_code",
  "group_member_list": [
    {"employee_code": "member1", "role": 0},  // 0=member, 1=admin
    {"employee_code": "member2", "role": 1}
  ],
  "group_name": "My Group",
  "group_settings": {
    "chat_history_for_new_members": 2  // 0=Off, 1=24h, 2=7days
  }
}

# Response
{
  "code": 0,
  "group_id": "NTk2NjAxMDUyMzMz",
  "users_not_added": []
}
```

### Get Group Info
```bash
GET https://openapi.seatalk.io/messaging/v2/group_chat/info?group_id=abc123
Authorization: Bearer {token}

# Response includes: group_name, group_settings, group_user_list, group_bot_list
```

### Get Chat History
```bash
GET https://openapi.seatalk.io/messaging/v2/group_chat/history?group_id=abc123&page_size=50
Authorization: Bearer {token}

# Returns messages from past 7 days only, reverse chronological order
# Message types: text, image, file, video, combined_forwarded_message_history
```

### Get Thread by Thread ID
```bash
GET https://openapi.seatalk.io/messaging/v2/group_chat/get_thread_by_thread_id?group_id=abc123&thread_id=thread123
Authorization: Bearer {token}

# Returns thread messages from past 7 days
```

### Get Employee Profile
```bash
GET https://openapi.seatalk.io/contacts/v2/profile?employee_code=123&employee_code=456
Authorization: Bearer {token}

# Batch up to 500 employee codes
# Returns: employee_code, seatalk_id, name, email, departments, etc.
```

### Add Group Members
```bash
POST https://openapi.seatalk.io/messaging/v2/group_chat/add_group_members
Content-Type: application/json
Authorization: Bearer {token}

{
  "group_id": "abc123",
  "employee_codes": ["emp1", "emp2", "emp3"]  // 1-30 members
}
```

## Event Callbacks

### Setup Callback URL
1. Configure callback URL in SeaTalk Open Platform
2. SeaTalk sends verification POST with `seatalk_challenge`
3. Respond with HTTP 200 and same challenge value within 5 seconds

### Verify Signature
```python
import hashlib

def verify_signature(request_body: str, signing_secret: str, signature_header: str) -> bool:
    computed = hashlib.sha256((request_body + signing_secret).encode()).hexdigest()
    return computed.lower() == signature_header.lower()
```

### Event Types
- `event_verification` - Callback URL verification
- `new_bot_subscriber` - User subscribed to bot
- `message_from_bot_subscriber` - Message from user in 1-on-1 chat
- `interactive_message_click` - User clicked interactive card button
- `bot_added_to_group_chat` - Bot added to group
- `bot_removed_from_group_chat` - Bot removed from group
- `new_mentioned_message_received_from_group_chat` - Bot mentioned in group

### Event Payload Example
```json
{
  "event_id": "1234567",
  "event_type": "bot_added_to_group_chat",
  "timestamp": 1687764109,
  "app_id": "your_app_id",
  "event": {
    "group": {
      "group_id": "group123",
      "group_name": "Test Group",
      "group_settings": {...}
    },
    "inviter": {
      "seatalk_id": "123456",
      "employee_code": "e_123",
      "email": "user@company.com"
    }
  }
}
```

## Interactive Message Cards

### Element Types
| Element | Properties | Limits |
|---------|-----------|--------|
| title | text | 1-120 chars, max 3 per card |
| description | text, format (1=MD, 2=plain) | 1-1000 chars, max 5 per card |
| button | button_type, text, value | 1-50 chars text, max 5 total |
| button_group | array of 1-3 buttons | max 3 groups per card |
| image | content (Base64) | max 5MB, max 3 per card |

### Button Types
- **callback**: Passes `value` to callback URL when clicked
- **redirect**: Navigates to app page via `mobile_link` or `desktop_link`

```json
// Callback button
{
  "element_type": "button",
  "button": {
    "button_type": "callback",
    "text": "Approve",
    "value": "approved"
  }
}

// Redirect button
{
  "element_type": "button",
  "button": {
    "button_type": "redirect",
    "text": "View Details",
    "mobile_link": {"type": "web", "path": "https://app.com/details"},
    "desktop_link": {"type": "web", "path": "https://app.com/details"}
  }
}
```

## Threading Messages

### Terminology
- **Thread**: Collection of root message and replies
- **Root Message**: A message with replies (thread_id == message_id)
- **Thread Reply**: A reply to root (thread_id != message_id)

### Reply to Thread
Include `thread_id` in your message request. Note: @all not allowed in thread replies.

### Thread Limitations
- Only past 7 days retrievable
- Requires SeaTalk v3.44.5+
- Root message must be <7 days old

## Error Codes

| Code | Description |
|------|-------------|
| 0 | Success |
| 101 | Rate limit exceeded |
| 102 | Invalid input |
| 3001 | User not found |
| 3002 | User not in service scope |
| 3003 | User not signed in |
| 4010 | Message not in thread |
| 4012 | No permission |
| 7000 | Group not found |
| 7001 | Bot not in group |
| 7002 | Group full |

## Files in This Skill

- `references/authentication.md` - Auth flow and token management
- `references/messaging.md` - All messaging APIs
- `references/group_chat.md` - Group management APIs
- `references/contacts.md` - Employee and department APIs
- `references/events.md` - Event callbacks and webhooks
- `references/interactive_cards.md` - Interactive message card building
