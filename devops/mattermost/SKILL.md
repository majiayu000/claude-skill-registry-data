---
name: mattermost
description: "Self-hosted open-source collaboration platform — chat, bots, webhooks, plugins, AI integration, Slack/Teams alternative with full data control. Triggers on: 'mattermost', 'self-hosted slack alternative', 'open source teams alternative', 'mattermost bot', 'mattermost webhook', 'mattermost plugin', 'mattermost API', 'mattermost integration', 'AI agent mattermost', 'deploy mattermost', 'mattermost docker', 'mattermost kubernetes', 'enterprise chat self-hosted', 'mattermost AI features', 'mattermost incoming webhook', 'mattermost slash command'."
origin: mattermost/mattermost
license: MIT + Enterprise (dual)
version: "1.0.0"
compatibility: "yana-ai >= 0.41.0"
allowed-tools: Bash, Read, Write, WebFetch
---

# Mattermost
# Source: mattermost/mattermost
# Tier: TIER 3 — PRODUCTIVITY

Platform chat tự host, open core — kiểm soát toàn bộ data, tích hợp AI agent qua webhook/plugin.

**Do NOT use for:** `openai--slack--*` (Slack cloud), `terminal--slack-bot-builder` (Slack API).

---

## Tổng quan

```
Mattermost = tự host + open source + enterprise features
  ✅ Data không rời server của bạn
  ✅ GDPR/HIPAA compliance tự kiểm soát
  ✅ 700+ integrations (GitHub, Jira, Jenkins, PagerDuty...)
  ✅ AI features tích hợp sẵn
  ✅ Webhooks + Slash commands + REST API + Plugins
```

**Tech stack:** TypeScript 49% + Go 41% — monorepo, production-grade.

---

## Triển khai nhanh

```bash
# Docker (dev/staging)
docker run --name mattermost \
  -p 8065:8065 \
  -v /local/data:/mattermost/data \
  mattermost/mattermost-team-edition:latest

# Kiểm tra
curl http://localhost:8065/api/v4/system/ping

# Production — Docker Compose (có PostgreSQL)
git clone https://github.com/mattermost/docker
cd docker
cp env.example .env
# Chỉnh .env: MM_SQLSETTINGS_DATASOURCE, domain, ports
docker compose -f docker-compose.yml -f docker-compose.without-nginx.yml up -d
```

```bash
# Kubernetes / Helm
helm repo add mattermost https://helm.mattermost.com
helm install mattermost mattermost/mattermost \
  --set mattermostEnvs.MM_SQLSETTINGS_DATASOURCE="postgres://..." \
  --set global.mattermost.enterpriseLicenseSecret=""
```

---

## Bot & AI agent integration

### Incoming Webhook (cách đơn giản nhất)

```bash
# Tạo webhook trong UI: Integrations → Incoming Webhooks → Add

# Gửi message từ agent
curl -X POST https://your.mattermost.com/hooks/WEBHOOK_TOKEN \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "town-square",
    "username": "YanaBot",
    "icon_emoji": ":robot_face:",
    "text": "### Yana AI Report\n**Status:** All 87 agents healthy"
  }'
```

### Slash Command (agent nhận lệnh từ người dùng)

```bash
# Tạo slash command: Integrations → Slash Commands
# Callback URL → endpoint của agent

# Agent nhận POST payload:
# {
#   "token": "...",
#   "channel_id": "...",
#   "user_name": "tam",
#   "command": "/yana",
#   "text": "status check"
# }

# Express handler
app.post('/yana-command', (req, res) => {
  const { text, user_name } = req.body
  const result = runYanaCommand(text)
  res.json({
    response_type: 'in_channel',
    text: `@${user_name}: ${result}`
  })
})
```

### REST API — đọc/ghi channel

```typescript
const MM_URL = 'https://your.mattermost.com'
const TOKEN = process.env.MATTERMOST_BOT_TOKEN

// Gửi message programmatically
async function postMessage(channelId: string, message: string) {
  const res = await fetch(`${MM_URL}/api/v4/posts`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${TOKEN}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ channel_id: channelId, message }),
  })
  return res.json()
}

// Đọc messages
async function getChannelPosts(channelId: string, perPage = 20) {
  const res = await fetch(
    `${MM_URL}/api/v4/channels/${channelId}/posts?per_page=${perPage}`,
    { headers: { Authorization: `Bearer ${TOKEN}` } }
  )
  return res.json()
}
```

### WebSocket — real-time events

```typescript
import WebSocket from 'ws'

const ws = new WebSocket(`wss://your.mattermost.com/api/v4/websocket`)

ws.on('open', () => {
  // Authenticate
  ws.send(JSON.stringify({
    seq: 1,
    action: 'authentication_challenge',
    data: { token: process.env.MATTERMOST_BOT_TOKEN }
  }))
})

ws.on('message', (data) => {
  const event = JSON.parse(data.toString())
  if (event.event === 'posted') {
    const post = JSON.parse(event.data.post)
    if (post.message.startsWith('/yana')) {
      handleYanaCommand(post)
    }
  }
})
```

---

## Plugin development

```go
// Go plugin — full server-side access
package main

import (
    "github.com/mattermost/mattermost/server/public/plugin"
)

type YanaPlugin struct{ plugin.MattermostPlugin }

func (p *YanaPlugin) MessageWillBePosted(c *plugin.Context, post *model.Post) (*model.Post, string) {
    // Intercept messages, call Yana AI, inject response
    if strings.HasPrefix(post.Message, "@yana") {
        response := callYanaAgent(post.Message)
        p.API.CreatePost(&model.Post{
            ChannelId: post.ChannelId,
            Message:   response,
        })
    }
    return post, ""
}

func main() { plugin.ClientMain(&YanaPlugin{}) }
```

---

## AI features tích hợp sẵn (Mattermost AI Copilot)

```
Mattermost AI Copilot plugin (built-in):
  - Thread summarization
  - Meeting notes
  - Sentiment analysis trên channel
  - Custom AI backend (OpenAI, Anthropic, Azure, local Ollama)

Config:
  System Console → Plugins → AI Copilot
  → AI Backend: Claude (Anthropic API)
  → Model: claude-sonnet-4-6
```

---

## Khác Slack/Teams thế nào

| Feature | Mattermost | Slack | Teams |
|---------|-----------|-------|-------|
| Self-hosted | ✅ | ❌ | ❌ (limited) |
| Source code | Open core | ❌ | ❌ |
| Data residency | 100% tự kiểm | Vendor | Vendor |
| Webhook pricing | Free | 10K msg/mo free | Limited |
| Plugin customization | Sâu (Go/TS) | Trung bình | Trung bình |
| HIPAA compliance | ✅ (tự host) | $ | $ |

---

## Anti-Fake-Pass Checks

```
❌ FAIL nếu dùng MM_SQLSETTINGS_DATASOURCE với SQLite trong production (không hỗ trợ)
❌ FAIL nếu bot token để lộ trong client-side code (phải server-side only)
❌ FAIL nếu webhook URL expose ra public mà không có token verification
✅ PASS khi: /api/v4/system/ping trả về {"status":"OK","is_leader":true}
✅ PASS khi: bot gửi được message + nhận được WebSocket event
```

## See also

- `terminal--slack-bot-builder` — Slack cloud API (khác Mattermost self-hosted)
- `agent-communication-policy.md` — inter-agent message format
- `api-security-gate.md` — webhook token validation
