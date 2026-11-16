---
name: n8n-automation
description: "Use when setting up workflow automation, connecting APIs, building AI pipelines, or automating repetitive tasks with 400+ integrations. Triggers on: 'n8n', 'workflow automation', 'tự động hóa', 'kết nối API', 'no-code automation', 'zapier alternative', 'trigger webhook', 'schedule job', 'ai pipeline automation', 'integrate services'."
---

# n8n Automation Skill

Workflow automation với 400+ integrations — visual + code, self-hostable, AI-native.
Source: [n8n-io/n8n](https://github.com/n8n-io/n8n) (189K⭐, Sustainable Use License)

## Khởi động nhanh

```bash
# Docker (khuyên dùng)
docker volume create n8n_data
docker run -d --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  docker.n8n.io/n8nio/n8n

# npx (test nhanh, không cần cài)
npx n8n
```

Mở editor: http://localhost:5678

## Workflow

### Step 1 — Tạo workflow cơ bản (qua UI)

1. Click **New Workflow**
2. Thêm trigger node (Webhook / Schedule / Manual)
3. Thêm action nodes (HTTP Request, Send Email, Slack...)
4. Kết nối nodes bằng dây
5. Click **Execute** để test
6. **Activate** để chạy production

### Step 2 — Workflow qua code (n8n API)

```bash
# Import workflow từ JSON
curl -X POST http://localhost:5678/api/v1/workflows \
  -H "X-N8N-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d @workflow.json

# Kích hoạt workflow
curl -X POST http://localhost:5678/api/v1/workflows/{id}/activate \
  -H "X-N8N-API-KEY: your-api-key"
```

### Step 3 — Webhook trigger

```json
{
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "my-webhook",
        "httpMethod": "POST"
      }
    },
    {
      "name": "Process Data",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "jsCode": "return items.map(item => ({ json: { processed: true, ...item.json } }))"
      }
    }
  ]
}
```

Nhận data tại: `http://localhost:5678/webhook/my-webhook`

### Step 4 — AI Agent workflow

```
Trigger (Webhook/Chat) 
  → AI Agent node (LangChain)
      → Tools: HTTP Request, Code, Database...
  → Send result (Slack/Email/Webhook)
```

Trong n8n UI:
1. Thêm **AI Agent** node
2. Chọn model (Claude, GPT, Gemini)
3. Attach tools: **HTTP Request Tool**, **Calculator**, **Wikipedia**
4. Kết nối với trigger và output

### Step 5 — Custom node với JavaScript

```javascript
// Trong Code node
const items = $input.all()
const results = []

for (const item of items) {
  const data = item.json
  
  // Gọi external API
  const response = await $http.request({
    method: 'POST',
    url: 'https://api.example.com/process',
    body: { text: data.content },
    json: true,
  })
  
  results.push({ json: { ...data, processed: response.result } })
}

return results
```

## Patterns phổ biến

### Slack → AI → reply

```
Slack trigger (mention bot)
  → Extract message text
  → Claude/GPT (AI node)
  → Send Slack message (reply in thread)
```

### Form → process → email

```
Form trigger (Typeform/webhook)
  → Validate data (Code node)
  → Save to Airtable/Notion
  → Send confirmation email (Gmail/Sendgrid)
```

### Schedule + scrape + report

```
Schedule trigger (mỗi ngày 8am)
  → HTTP Request (scrape pages)
  → Code node (parse data)
  → AI Summary (Claude node)
  → Send report (Telegram/Slack)
```

## Biến môi trường

```bash
# docker-compose.yml
environment:
  - N8N_BASIC_AUTH_ACTIVE=true
  - N8N_BASIC_AUTH_USER=admin
  - N8N_BASIC_AUTH_PASSWORD=secret
  - N8N_HOST=n8n.yourdomain.com
  - N8N_PROTOCOL=https
  - WEBHOOK_URL=https://n8n.yourdomain.com
  - N8N_ENCRYPTION_KEY=your-32-char-key
```

## Self-host với Docker Compose

```yaml
version: '3.8'
services:
  n8n:
    image: docker.n8n.io/n8nio/n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=localhost
      - N8N_PORT=5678
    volumes:
      - n8n_data:/home/node/.n8n
    restart: unless-stopped

volumes:
  n8n_data:
```

## API key setup (cho n8n API)

Settings → n8n API → Create API Key → dùng header `X-N8N-API-KEY`
