---
name: byow-whatsapp
description: "Implement 'Bring Your Own WhatsApp' in web apps — users connect their personal WhatsApp via QR scan to send/receive messages through your app. Covers whatsapp-web.js, Railway deployment, QR auth flow, multi-tenant architecture, and Next.js integration with 54 MCP-parity endpoints. Triggers on 'WhatsApp integration', 'BYOW WhatsApp', 'connect WhatsApp', 'WhatsApp QR code', 'whatsapp-web.js', 'WhatsApp notifications'. Do NOT use for WhatsApp Business API integration, marketing automation at scale, or automated customer support bots."
metadata:
  author: omm
  version: 2.0.0
  category: development
---

# BYOW WhatsApp - Bring Your Own WhatsApp Integration

## Overview

BYOW WhatsApp allows users to connect their personal WhatsApp account to send messages through a web application. Unlike WhatsApp Business API (which requires business verification), this approach:

- Uses the user's existing WhatsApp account
- Requires QR code scanning (like WhatsApp Web)
- Messages appear as sent from the user's phone number
- No WhatsApp Business API approval needed

### When to Use This Skill

| Use Case | Appropriate |
|----------|-------------|
| Chapter/organization notifications | Yes |
| Personal assistant apps | Yes |
| CRM with WhatsApp messaging | Yes |
| Marketing automation at scale | No (use Business API) |
| Automated customer support | No (use Business API) |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                      3-TIER ARCHITECTURE                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [Web App - Vercel/Any Host]                                       │
│       │                                                             │
│       │ HTTPS with API Key                                         │
│       ▼                                                             │
│  [WhatsApp Service - Railway/VPS]  ◄── Persistent Chrome           │
│       │                            ◄── Session in Volume            │
│       │ whatsapp-web.js (puppeteer)                                │
│       ▼                                                             │
│  [WhatsApp Web] ◄── Linked to user's phone                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Why Separate Service?

| Constraint | Solution |
|------------|----------|
| whatsapp-web.js needs persistent Chrome | Railway container (not serverless) |
| Session must survive restarts | Railway volume at `/app/.wwebjs_auth` |
| Puppeteer binary dependencies | Dockerfile with Chromium |
| Connection must stay alive | Long-running Express server |

---

## Template Selection

This skill provides TWO service templates:

| Template | Endpoints | Use Case |
|----------|-----------|----------|
| `whatsapp-service/` | 6 | Basic send-only (notifications, alerts) |
| `whatsapp-service-full/` | **54** | Full MCP parity (read + write + groups + newsletters) |

### When to Use Each

| Feature Needed | Basic | Full |
|----------------|-------|------|
| Send messages | Yes | Yes |
| Bulk messaging | Yes | Yes |
| Read messages | No | Yes |
| Search messages | No | Yes |
| Group management | No | Yes (17 endpoints) |
| Newsletters/Channels | No | Yes (7 endpoints) |
| LID resolution | No | Yes (6 endpoints) |
| Profile/Status | No | Yes (5 endpoints) |
| Reactions/Polls | No | Yes |
| Media download | No | Yes |

**Rule of thumb:** Start with Basic. Upgrade to Full when you need read capabilities or group management.

---

## Full Service Endpoints (54 Total)

The `whatsapp-service-full/` template provides complete parity with WhatsApp MCP:

### Category 1: Messaging (10 endpoints)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/messages/send` | POST | Send text message |
| `/messages/send-file` | POST | Send file/media |
| `/messages/send-audio` | POST | Send audio as voice note |
| `/messages/forward` | POST | Forward a message |
| `/messages/react` | POST | Add emoji reaction |
| `/messages/edit` | PATCH | Edit sent message |
| `/messages/delete` | DELETE | Delete/revoke message |
| `/messages/list` | GET | List messages in chat |
| `/messages/search` | GET | Search messages |
| `/media/download` | POST | Download media from message |

### Category 2: Chats (3 endpoints)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/chats` | GET | List all chats |
| `/chats/:jid` | GET | Get specific chat |
| `/chats/:jid/messages` | GET | Get messages from chat |

### Category 3: Contacts (4 endpoints)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/contacts/search` | GET | Search contacts |
| `/contacts/:jid` | GET | Get contact info |
| `/contacts/:jid/chats` | GET | Get chats with contact |
| `/contacts/:jid/last-interaction` | GET | Get last interaction |

### Category 4: Groups (17 endpoints)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/groups` | GET | List joined groups |
| `/groups` | POST | Create new group |
| `/groups/:jid` | GET | Get group info |
| `/groups/:jid/participants` | GET | Get group participants |
| `/groups/:jid/leave` | POST | Leave group |
| `/groups/:jid/name` | PATCH | Set group name |
| `/groups/:jid/description` | PATCH | Set group description |
| `/groups/:jid/photo` | PATCH | Set group photo |
| `/groups/:jid/members` | POST | Add members |
| `/groups/:jid/members` | DELETE | Remove members |
| `/groups/:jid/admins` | POST | Promote to admin |
| `/groups/:jid/admins` | DELETE | Demote from admin |
| `/groups/:jid/settings/announce` | PATCH | Set announce mode |
| `/groups/:jid/settings/locked` | PATCH | Set locked mode |
| `/groups/join` | POST | Join via invite link |
| `/groups/preview` | POST | Preview invite link |
| `/groups/:jid/invite-link` | GET | Get/reset invite link |

### Category 5: Newsletters (7 endpoints)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/newsletters` | GET | List subscribed newsletters |
| `/newsletters` | POST | Create newsletter |
| `/newsletters/:jid` | GET | Get newsletter info |
| `/newsletters/preview` | POST | Preview newsletter link |
| `/newsletters/:jid/follow` | POST | Follow newsletter |
| `/newsletters/:jid/unfollow` | POST | Unfollow newsletter |
| `/newsletters/:jid/react` | POST | React to newsletter message |

### Category 6: LID Resolution (6 endpoints)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/lid/resolve` | GET | Resolve LID to phone |
| `/lid/phone-to-lid` | GET | Resolve phone to LID |
| `/lid/batch` | POST | Batch resolve LIDs/phones |
| `/lid/cache/stats` | GET | Get cache statistics |
| `/lid/cache/list` | GET | List all mappings |
| `/lid/cache/populate` | POST | Populate from groups |

### Category 7: Profile & Status (5 endpoints)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/profile/status` | PATCH | Set status message |
| `/profile/:jid/picture` | GET | Get profile picture |
| `/profile/users/info` | POST | Get detailed user info |
| `/profile/business/:jid` | GET | Get business profile |
| `/polls` | POST | Create poll |

### Category 8: Utilities (2 endpoints)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/typing` | POST | Send typing indicator |
| `/check` | POST | Check if numbers on WhatsApp |

### System Endpoints (Always Available)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check (no auth) |
| `/connect` | POST | Initialize client, get QR |
| `/status` | GET | Connection status + QR |
| `/disconnect` | POST | Logout and cleanup |

---

## Implementation Workflow

### Step 1: Create WhatsApp Service

**Option A: Basic Service (6 endpoints)**

Use the template in `templates/whatsapp-service/`:

```bash
# Copy template to project
cp -r ~/.claude/skills/byow-whatsapp/templates/whatsapp-service ./whatsapp-service
cd whatsapp-service
npm install
```

Basic service provides these endpoints:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check (no auth) |
| `/connect` | POST | Initialize client, get QR |
| `/status` | GET | Connection status + QR code |
| `/send` | POST | Send single message |
| `/send-bulk` | POST | Send to multiple recipients |
| `/disconnect` | POST | Logout and cleanup |

**Option B: Full Service (54 endpoints)**

Use the template in `templates/whatsapp-service-full/`:

```bash
# Copy template to project
cp -r ~/.claude/skills/byow-whatsapp/templates/whatsapp-service-full ./whatsapp-service
cd whatsapp-service
npm install
npm run build
```

Full service provides all 54 endpoints listed in the [Full Service Endpoints](#full-service-endpoints-54-total) section above. Features:

- **TypeScript** with full type safety
- **Railway-optimized Dockerfile** with Chromium
- **Modular routes** organized by category
- **Error handling** for common WhatsApp errors
- **Same API key authentication** as basic service

### Step 2: Deploy to Railway

To deploy, follow `references/deployment-railway.md`:

1. Create Railway project
2. Add volume at `/app/.wwebjs_auth`
3. Set environment variables
4. Deploy from GitHub or CLI

### Step 3: Integrate with Web App

To integrate with Next.js, use templates in `templates/nextjs-integration/`:

```
templates/nextjs-integration/
├── lib/whatsapp/api-client.ts    # API client for service
├── app/actions/whatsapp.ts       # Server actions
├── components/whatsapp-connect.tsx # QR code UI
└── types/whatsapp.ts             # TypeScript types
```

### Step 4: Add Database Schema (Optional)

For multi-tenant support, use the schema in `templates/database-schema.sql`:

- `whatsapp_connections` - Track per-tenant connections
- `whatsapp_groups` - Store group JIDs
- `whatsapp_templates` - Message templates
- `whatsapp_message_logs` - Audit trail

---

## Connection Flow

```
User clicks "Connect" → Web App → WhatsApp Service
                                       │
                                       ▼
                              Initialize whatsapp-web.js
                                       │
                                       ▼
                              Generate QR as data URL
                                       │
                                       ▼
                              Return QR to Web App
                                       │
                                       ▼
                              Display QR in UI
                                       │
                                       ▼
                              User scans with phone
                                       │
                                       ▼
                              Service receives 'authenticated'
                                       │
                                       ▼
                              Session saved to volume
                                       │
                                       ▼
                              Status becomes 'ready'
```

---

## Key Files Reference

| Need | Reference |
|------|-----------|
| Full architecture details | `references/architecture.md` |
| Railway deployment | `references/deployment-railway.md` |
| Security patterns | `references/security-patterns.md` |
| Basic WhatsApp service (6 endpoints) | `templates/whatsapp-service/` |
| **Full WhatsApp service (54 endpoints)** | `templates/whatsapp-service-full/` |
| Next.js integration | `templates/nextjs-integration/` |
| Database schema | `templates/database-schema.sql` |
| MCP endpoints reference | `/Users/omm/Vaults/Claude Setup/Memory/whatsapp-mcp-endpoints-reference.md` |

---

## Environment Variables

### WhatsApp Service (Railway)

```env
API_KEY=your-secure-api-key
ALLOWED_ORIGINS=https://your-app.vercel.app,http://localhost:3000
PORT=3001
PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser
```

### Web App (Vercel/etc)

```env
WHATSAPP_SERVICE_URL=https://your-service.railway.app
WHATSAPP_API_KEY=your-secure-api-key
```

---

## Common Issues

| Issue | Solution |
|-------|----------|
| QR not generating | Check Chromium path, increase timeout |
| Session not persisting | Verify Railway volume mount |
| "WhatsApp Web is open" | Only one session per account |
| Rate limiting | Add delay between bulk messages (1.5s+) |
| Phone number format | Always convert to `91XXXXXXXXXX@c.us` |

---

## Security Considerations

1. **API Key Authentication** - All endpoints require `X-API-Key` header
2. **CORS Whitelist** - Only allow specific origins
3. **RLS Policies** - Restrict by role (Chair/Admin only)
4. **Session Isolation** - One connection per tenant/chapter
5. **No credential storage** - QR scan only, no passwords

---

## Limitations

- Requires user to scan QR (no automated login)
- One WhatsApp account per service instance
- Session may expire if phone disconnects
- Not suitable for high-volume messaging
- WhatsApp may block if flagged as spam
- Full service has **same capabilities as WhatsApp MCP** (all 54 endpoints)

---

## Related Skills

- `supabase-expert` - For database and RLS policies
- `railway` - For Railway deployment management
