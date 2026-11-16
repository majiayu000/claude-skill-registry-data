---
name: hermes-webui
description: Web UI 3-panel cho AI agent — sessions, chat, file browser. Python + vanilla JS, không framework. Reference architecture cho YAMTAM IO web mode.
triggers:
  - hermes webui
  - hermes-webui
  - web ui for agent
  - 3 panel chat
  - agent web interface
  - session management ui
  - file browser chat
---

# hermes-webui — Agent Web UI Reference

**Source**: github.com/nesquena/hermes-webui ⭐12.6k  
**Stack**: Python + vanilla JS + CSS — no framework, no bundler  
**License**: MIT

## Architecture 3-panel

```
┌─────────────┬──────────────────────┬──────────────────┐
│  Sessions   │  Chat                │  Workspace       │
│  + tags     │  + token ring        │  file browser    │
│  + search   │  + composer footer   │  + inline edit   │
└─────────────┴──────────────────────┴──────────────────┘
```

Token ring: context usage dạng circular — luôn visible.  
Composer footer: model selector, profile, workspace — luôn visible khi gõ.

## Key patterns đáng học cho YAMTAM

### SSE streaming (không WebSocket)

```python
def stream_response(agent_gen):
    for chunk in agent_gen:
        yield f"data: {json.dumps({'content': chunk})}\n\n"
```

```javascript
const es = new EventSource('/api/stream')
es.onmessage = e => appendToken(JSON.parse(e.data).content)
```

### Session management

```javascript
const sessions = await loadSessions()  // JSON files on disk
const filtered = sessions.filter(s =>
    s.tags.includes(tag) || s.title.includes(query)
)
```

### Auth HMAC cookie

```python
import hmac, hashlib
def make_token(secret, ts):
    return hmac.new(secret.encode(), ts.encode(), hashlib.sha256).hexdigest()
```

## So sánh với YAMTAM IO

| Hermes WebUI | YAMTAM IO |
|---|---|
| Session sidebar | App grid |
| Token ring | Dynamic Island |
| Control Center | Dock + Settings app |
| SSE streaming | SSE (đã dùng) |
| File browser | Chưa có |
| 3-panel layout | Phone simulator |

## Cài thử

```bash
git clone https://github.com/nesquena/hermes-webui
cd hermes-webui
pip install -r requirements.txt
python server.py --port 8080
# Cần Hermes Agent chạy trước
```

## Dùng làm gì trong YAMTAM

Không cài trực tiếp — dùng làm **reference** nếu muốn nâng IO từ phone simulator
thành web app thật: pure Python server + vanilla JS, session history, file browser vault.
