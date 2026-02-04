---
name: digital-samba
description: Build video conferencing integrations using Digital Samba's API and SDK. Use when creating meeting rooms, embedding video calls, generating participant tokens, managing recordings, or integrating real-time collaboration features. Triggers include "Digital Samba", "video conferencing API", "embed video calls", "meeting room integration", "WebRTC iframe", "participant tokens".
---

# Digital Samba Integration

Build video conferencing into your applications using Digital Samba's prebuilt infrastructure. No WebRTC/Janus/TURN setup required.

## Two Integration Approaches

1. **REST API** - Server-side room/session/participant management
2. **Embedded SDK** - Client-side iframe control and event handling

## Quick Start

### 1. Create a Room (Server-side)
```bash
curl -X POST https://api.digitalsamba.com/api/v1/rooms \
  -H "Authorization: Bearer {DEVELOPER_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"friendly_url": "my-meeting", "privacy": "public"}'
```

### 2. Generate Access Token (Server-side)
```javascript
const jwt = require('jsonwebtoken');

const token = jwt.sign({
  td: "team-uuid",      // Your team ID
  rd: "room-uuid",      // Room ID from step 1
  u: "John Doe",        // User display name
  role: "moderator"     // Optional: user role
}, DEVELOPER_KEY, { algorithm: 'HS256' });
```

### 3. Embed the Room (Client-side)
```html
<iframe 
  allow="camera; microphone; display-capture; autoplay;" 
  src="https://yourteam.digitalsamba.com/my-meeting?token={jwt}"
  allowfullscreen="true">
</iframe>
```

### 4. Control with SDK (Optional)
```javascript
import DigitalSambaEmbedded from '@digitalsamba/embedded-sdk';

const sambaFrame = DigitalSambaEmbedded.createControl({ 
  url: roomUrl,
  frame: document.getElementById('video-frame')
});

sambaFrame.on('userJoined', (e) => console.log(`${e.data.name} joined`));
sambaFrame.load();
```

## When to Use What

| Need | Use |
|------|-----|
| Create/delete rooms | REST API |
| User authentication | JWT tokens |
| Embed video UI | iframe + SDK |
| Start/stop recording | REST API or SDK |
| React to events | SDK events |
| Manage participants | REST API |
| Customize UI | Room settings API |

## Reference Documentation

For detailed information, see these reference files:

- **[api-reference.md](api-reference.md)** - Complete REST API endpoints
- **[sdk-reference.md](sdk-reference.md)** - SDK methods, events, properties
- **[patterns.md](patterns.md)** - Common integration patterns with examples
- **[jwt-tokens.md](jwt-tokens.md)** - Authentication deep-dive

## Key Concepts

### Room Types
- **Public**: Anyone with URL can join (enters name on join screen)
- **Private**: Requires JWT token to join

### Roles & Permissions
Assign roles via JWT `role` field. Common roles:
- `moderator` - Full control (mute others, recording, etc.)
- `speaker` - Can present and speak
- `attendee` - View/listen only (configurable)

### Authentication Flow
1. **Developer key** → Server-side API calls only
2. **JWT tokens** → Client-side room access
3. **Never expose developer key to browsers**

## Common Errors

| Code | Meaning | Solution |
|------|---------|----------|
| 401 | Invalid/missing key | Check Authorization header |
| 403 | Insufficient permissions | Verify role/permissions |
| 404 | Room not found | Check room UUID/URL |
| 422 | Validation error | Check request body |

## Check for Updates

To check if your installed skill is up to date:

1. **Local version**: `cat .claude/skills/digital-samba/VERSION`
2. **Latest version**: `curl -s https://api.github.com/repos/digitalsamba/digital-samba-skill/releases/latest | grep '"tag_name"'`

**To update (submodule install):**
```bash
git submodule update --remote .claude/skills/digital-samba
```

**To update (manual install):** Re-clone and copy skill files from https://github.com/digitalsamba/digital-samba-skill

## Resources

- API Reference: https://developer.digitalsamba.com/rest-api/
- SDK NPM: https://www.npmjs.com/package/@digitalsamba/embedded-sdk
- Dashboard: https://dashboard.digitalsamba.com
- Skill Releases: https://github.com/digitalsamba/digital-samba-skill/releases
