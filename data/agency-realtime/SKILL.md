---
name: agency-realtime
description: Handle real-time communication via WebSocket for live notifications, content collaboration, and approval updates. Use when working with WebSocket handlers, real-time notifications, or live collaboration features.
---

# Social Media Agency Real-Time Layer

## Architecture

```
Dashboard ←WebSocket→ FastAPI WS Handler ←→ Redis PubSub
                                          ←→ Database Events
```

## WebSocket (Notifications & Collaboration)

### Message Protocol

All WebSocket messages use JSON with a `type` field:

```python
# Server → Client (notifications)
{"type": "notification", "category": "approval", "content": "New content awaiting approval", "content_id": "uuid", "timestamp": "..."}
{"type": "notification", "category": "published", "content": "Post published to Instagram", "content_id": "uuid", "timestamp": "..."}
{"type": "notification", "category": "comment", "content": "Manager left feedback on your post", "content_id": "uuid", "timestamp": "..."}
{"type": "notification", "category": "analytics", "content": "Weekly analytics ready for Sunrise Coffee", "client_id": "uuid", "timestamp": "..."}

# Server → Client (collaboration)
{"type": "content_updated", "content_id": "uuid", "field": "body", "value": "...", "updated_by": "user_name"}
{"type": "user_presence", "content_id": "uuid", "users": ["Alice", "Bob"]}

# Client → Server
{"type": "subscribe", "channels": ["notifications", "content:uuid"]}
{"type": "unsubscribe", "channels": ["content:uuid"]}
{"type": "content_edit", "content_id": "uuid", "field": "body", "value": "..."}
{"type": "ping"}

# Server → Client
{"type": "pong"}
{"type": "error", "content": "Something went wrong."}
```

### WebSocket Handler

```python
# src/agency/websocket/notifications.py
from fastapi import WebSocket, WebSocketDisconnect
import json
import redis.asyncio as redis
from agency.config import get_settings

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, user_id: str, websocket: WebSocket):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_to_user(self, user_id: str, message: dict):
        if user_id in self.active_connections:
            for ws in self.active_connections[user_id]:
                await ws.send_json(message)

    async def broadcast_to_org(self, org_id: str, user_ids: list[str], message: dict):
        for uid in user_ids:
            await self.send_to_user(uid, message)

manager = ConnectionManager()

async def handle_notifications(websocket: WebSocket, user_id: str, org_id: str):
    await manager.connect(user_id, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)

            if msg["type"] == "ping":
                await websocket.send_json({"type": "pong"})

            elif msg["type"] == "subscribe":
                pass  # Track channel subscriptions

    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)
```

### Registering WebSocket Route

```python
# In main.py or a dedicated websocket router
from fastapi import WebSocket, Depends
from agency.websocket.notifications import handle_notifications
from agency.dependencies import get_db

@app.websocket("/ws/notifications")
async def websocket_notifications(websocket: WebSocket):
    token = websocket.query_params.get("token")
    user = verify_ws_token(token)
    if not user:
        await websocket.close(code=4001)
        return
    await handle_notifications(websocket, user["sub"], user["org_id"])
```

### Emitting Notifications from Services

```python
# In any service that needs to notify users
from agency.websocket.notifications import manager

async def notify_approval_requested(org_id: str, reviewer_ids: list[str], content_id: str, content_title: str):
    for reviewer_id in reviewer_ids:
        await manager.send_to_user(reviewer_id, {
            "type": "notification",
            "category": "approval",
            "content": f"New content awaiting your approval: {content_title}",
            "content_id": content_id,
            "timestamp": datetime.utcnow().isoformat(),
        })

async def notify_content_published(org_id: str, creator_id: str, content_id: str, platform: str):
    await manager.send_to_user(creator_id, {
        "type": "notification",
        "category": "published",
        "content": f"Your post was published to {platform}",
        "content_id": content_id,
        "timestamp": datetime.utcnow().isoformat(),
    })
```

### Frontend WebSocket Client

```typescript
// lib/socket.ts
export class AgencySocket {
  private ws: WebSocket | null = null;
  private onMessage: (msg: any) => void;
  private reconnectAttempts = 0;
  private maxReconnects = 5;

  constructor(onMessage: (msg: any) => void) {
    this.onMessage = onMessage;
    this.connect();
  }

  private connect() {
    const token = localStorage.getItem("token");
    if (!token) return;

    const wsUrl = process.env.NEXT_PUBLIC_API_URL!.replace("http", "ws");
    this.ws = new WebSocket(`${wsUrl}/ws/notifications?token=${token}`);

    this.ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      this.onMessage(msg);
    };

    this.ws.onclose = () => {
      if (this.reconnectAttempts < this.maxReconnects) {
        this.reconnectAttempts++;
        setTimeout(() => this.connect(), 2000 * this.reconnectAttempts);
      }
    };

    this.ws.onopen = () => {
      this.reconnectAttempts = 0;
      this.send("subscribe", { channels: ["notifications"] });
    };
  }

  send(type: string, data: Record<string, any> = {}) {
    this.ws?.send(JSON.stringify({ type, ...data }));
  }

  close() {
    this.ws?.close();
  }
}
```

### Notification Store (Zustand)

```typescript
// stores/notification-store.ts
import { create } from "zustand";

interface Notification {
  id: string;
  category: string;
  content: string;
  contentId?: string;
  clientId?: string;
  timestamp: string;
  read: boolean;
}

interface NotificationStore {
  notifications: Notification[];
  unreadCount: number;
  addNotification: (notif: Notification) => void;
  markRead: (id: string) => void;
  markAllRead: () => void;
}

export const useNotificationStore = create<NotificationStore>((set) => ({
  notifications: [],
  unreadCount: 0,
  addNotification: (notif) =>
    set((state) => ({
      notifications: [notif, ...state.notifications].slice(0, 50),
      unreadCount: state.unreadCount + 1,
    })),
  markRead: (id) =>
    set((state) => ({
      notifications: state.notifications.map((n) =>
        n.id === id ? { ...n, read: true } : n
      ),
      unreadCount: Math.max(0, state.unreadCount - 1),
    })),
  markAllRead: () =>
    set((state) => ({
      notifications: state.notifications.map((n) => ({ ...n, read: true })),
      unreadCount: 0,
    })),
}));
```

## Redis PubSub for Cross-Process Notifications

When running multiple backend workers, use Redis PubSub to broadcast notifications.

```python
import redis.asyncio as redis
import json
from agency.config import get_settings

class RedisPubSub:
    def __init__(self):
        settings = get_settings()
        self.redis = redis.from_url(settings.redis_url)

    async def publish(self, channel: str, message: dict):
        await self.redis.publish(channel, json.dumps(message))

    async def subscribe(self, channel: str):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(channel)
        return pubsub
```

## Key Rules

1. **WebSocket for real-time notifications** — approval requests, publish confirmations, analytics alerts
2. **Always validate WebSocket token** before accepting connection
3. **Auto-reconnect on disconnect** — up to 5 attempts with exponential backoff
4. **Keep notification history capped** — max 50 in frontend store
5. **Use Redis PubSub** for multi-process notification delivery
6. **Send heartbeat pings** — detect stale connections
7. **Graceful degradation** — app works without WebSocket (polling fallback)
8. **Notification categories** — `approval`, `published`, `comment`, `analytics`, `system`
