---
name: papi
description: Complete WhatsApp automation API with microservices architecture. Send messages, interactive buttons, lists, carousels, polls, manage instances, groups, catalogs and webhooks. Features Admin Panel (free), Phone Calls, RCS Messaging, SMS, Virtual Numbers (Pro).
metadata: {"openclaw":{"emoji":"📱","homepage":"https://papi.api.br","tags":["p-api","papi","whatsapp","automation","messaging","api"]},"minis":{"originalSource":"https://clawskills.sh/skills/rafacpti23-papi","convertedAt":"2026-10-31T22:13:07.375Z","license":"Unknown"}}
---

# PAPI - WhatsApp Connections Hub

![PAPI Logo](https://papi.api.br/logo-official.png)

**The WhatsApp automation you've been waiting for.**

Complete redesign with microservices architecture — modular, scalable, and independent.

🌐 **Official Website:** https://papi.api.br  
🤝 **Partner:** [Mundo Automatik](https://mundoautomatik.com/)

---

## 📑 Table of Contents

1. [Features](#-features)
2. [Configuration](#%EF%B8%8F-configuration)
3. [Authentication](#-authentication)
4. [Main Endpoints](#-main-endpoints)
5. [Detailed References](#-detailed-references)
6. [Credits](#-credits)

---

## ✨ Features

### 📊 Admin Panel (Free)
- Multi-language interface (PT-BR, EN, ES)
- Instance management
- Real-time monitoring
- Behavior configuration
- Usage statistics

### 🔥 Pro Features

| Feature | Capabilities |
|---------|--------------|
| 📞 **Phone Calls** | Chip-based calls, WhatsApp calls, Extension system, Call management |
| 💬 **RCS Messaging** | Rich media sending, Buttons & carousels, Read receipts, Typing indicator |
| 📱 **Call Center** | Chip rotation (30 ports), Bulk SMS sending, Configurable rate limiting |
| ✉️ **Professional SMS** | Individual/bulk sending, Smart chip rotation, Port configuration |
| 🔢 **Virtual Numbers** | Instant purchase, Auto activation, Full management |

---

## ⚙️ Configuration

Before using, configure in TOOLS.md:

```markdown
### PAPI (WhatsApp)
- Base URL: https://your-server.com
- API Key: your-api-key
- Default Instance: instance-name
```

## 🔐 Authentication

All requests require the `x-api-key` header:

```bash
curl -X GET "https://your-server.com/api/instances" \
  -H "x-api-key: YOUR_KEY"
```

---

## 📡 Main Endpoints

### Instances
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/instances` | List all instances |
| POST | `/api/instances` | Create instance `{"id": "name"}` |
| GET | `/api/instances/:id/qr` | Get QR code |
| GET | `/api/instances/:id/status` | Instance status |
| DELETE | `/api/instances/:id` | Remove instance |

### Send Messages

JID format: `5511999999999@s.whatsapp.net`

| Type | Endpoint | Required Fields |
|------|----------|-----------------|
| Text | `POST /send-text` | `jid`, `text` |
| Image | `POST /send-image` | `jid`, `url` or `base64`, `caption` |
| Video | `POST /send-video` | `jid`, `url` or `base64` |
| Audio | `POST /send-audio` | `jid`, `url`, `ptt` |
| Document | `POST /send-document` | `jid`, `url`, `filename` |
| Location | `POST /send-location` | `jid`, `latitude`, `longitude` |
| Contact | `POST /send-contact` | `jid`, `name`, `phone` |
| Sticker | `POST /send-sticker` | `jid`, `url` |
| Reaction | `POST /send-reaction` | `jid`, `messageId`, `emoji` |

### Interactive Messages

| Type | Endpoint | Description |
|------|----------|-------------|
| Buttons | `POST /send-buttons` | quick_reply, cta_url, cta_call, cta_copy |
| List | `POST /send-list` | Menu with sections |
| Carousel | `POST /send-carousel` | Sliding cards (mobile only) |
| Poll | `POST /send-poll` | Voting up to 12 options |

### Groups

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/groups/create` | Create group |
| GET | `/groups/:groupId/metadata` | Group info |
| POST | `/groups/:groupId/participants` | Manage members (add/remove/promote/demote) |

### Webhook

```json
POST /api/instances/:id/webhook
{
  "url": "https://your-server/webhook",
  "enabled": true,
  "events": ["messages", "status"]
}
```

---

## 📚 Detailed References

| File | Content |
|------|---------|
| `references/interactive.md` | Buttons, lists, carousel, polls examples |
| `references/groups.md` | Group management |
| `references/catalog.md` | Product catalog |
| `references/integrations.md` | Typebot, Chatwoot integrations |

---

## 👥 Credits

**Developed by:** Pastorini  
**Website:** https://papi.api.br  
**Partner:** [Mundo Automatik](https://mundoautomatik.com/)  
**Skill maintained by:** @rafacpti23
