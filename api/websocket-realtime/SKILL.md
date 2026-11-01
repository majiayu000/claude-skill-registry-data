---
name: websocket-realtime
description: WebSocket & Realtime Engineer — Institutional capability and runbook for websocket-realtime.
---

# SKILL: WebSocket & Realtime Engineer
## Domain: Unified Stream, Pub/Sub, Live Data, Redis Channels

**Activation triggers:** WebSocket endpoint, live price feed, real-time positions,
signal streaming, notification push, pub/sub channel, Redis streams, connection
management, reconnection logic.

---

## Unified WebSocket Architecture

```
Frontend (React)
  └── useExpertWS() hook
        └── WebSocketManager (singleton)
              └── wss://localhost:8002/ws/expert?token=<jwt>

Expert Backend
  └── /ws/expert (FastAPI WebSocket endpoint)
        └── ConnectionManager
              └── Redis Pub/Sub subscriber
                    ├── channel: positions.<account_id>
                    ├── channel: signals.<provider_id>
                    ├── channel: notifications.<user_id>
                    └── channel: market.prices.<symbol>
```

---

## Backend WebSocket Endpoint

```python
# integral-expert-backend/app/api/v1/ws/expert.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.core.websocket import ConnectionManager
from app.core.auth import get_ws_user   # verify JWT from query param

router = APIRouter()
manager = ConnectionManager()

@router.websocket("/ws/expert")
async def expert_ws_endpoint(
    websocket: WebSocket,
    token: str,
    db: AsyncSession = Depends(get_async_db),
):
    user = await get_ws_user(token, db)
    if not user:
        await websocket.close(code=4001)
        return

    await manager.connect(websocket, user.id)
    try:
        async for message in websocket.iter_json():
            # Handle client → server messages (subscriptions)
            await handle_client_message(message, websocket, user)
    except WebSocketDisconnect:
        pass
    finally:
        await manager.disconnect(websocket, user.id)
```

---

## ConnectionManager with Redis Pub/Sub

```python
# app/core/websocket.py
import asyncio
import json
from typing import DefaultDict, Set
from collections import defaultdict
from fastapi import WebSocket
import aioredis

class ConnectionManager:
    def __init__(self):
        self._connections: DefaultDict[str, Set[WebSocket]] = defaultdict(set)
        self._redis: aioredis.Redis | None = None
        self._pubsub_task: asyncio.Task | None = None

    async def connect(self, ws: WebSocket, user_id: str) -> None:
        await ws.accept()
        self._connections[user_id].add(ws)
        await self._ensure_pubsub()

    async def disconnect(self, ws: WebSocket, user_id: str) -> None:
        self._connections[user_id].discard(ws)
        if not self._connections[user_id]:
            del self._connections[user_id]

    async def broadcast_to_user(self, user_id: str, payload: dict) -> None:
        dead: Set[WebSocket] = set()
        for ws in self._connections.get(user_id, set()):
            try:
                await ws.send_json(payload)
            except Exception:
                dead.add(ws)
        for ws in dead:
            self._connections[user_id].discard(ws)

    async def publish(self, channel: str, payload: dict) -> None:
        """Publish to Redis — picked up by ALL backend instances."""
        if self._redis:
            await self._redis.publish(channel, json.dumps(payload))

    async def _ensure_pubsub(self) -> None:
        if self._pubsub_task and not self._pubsub_task.done():
            return
        self._redis = await aioredis.from_url(settings.REDIS_URL)
        self._pubsub_task = asyncio.create_task(self._pubsub_listener())

    async def _pubsub_listener(self) -> None:
        pubsub = self._redis.pubsub()
        await pubsub.psubscribe("positions.*", "signals.*", "notifications.*")
        async for message in pubsub.listen():
            if message["type"] == "pmessage":
                channel = message["channel"].decode()
                data = json.loads(message["data"])
                # Route to correct user connections
                user_id = channel.split(".")[-1]
                await self.broadcast_to_user(user_id, {"channel": channel, "data": data})
```

---

## Frontend WebSocket Manager (Singleton)

```typescript
// app/src/shared/ws/WebSocketManager.ts
type Handler = (payload: unknown) => void;

class WebSocketManager {
  private ws: WebSocket | null = null;
  private handlers: Map<string, Set<Handler>> = new Map();
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null;
  private reconnectDelay = 1000;
  private maxDelay = 30_000;

  connect(token: string): void {
    if (this.ws?.readyState === WebSocket.OPEN) return;

    const isDev = import.meta.env.DEV;
    const base = isDev ? 'ws://localhost:8002' : (import.meta.env.VITE_EXPERT_WS_URL ?? '');
    this.ws = new WebSocket(`${base}/ws/expert?token=${token}`);

    this.ws.onopen = () => {
      this.reconnectDelay = 1000;   // reset backoff on success
    };

    this.ws.onmessage = (event) => {
      const msg = JSON.parse(event.data) as { channel: string; data: unknown };
      this.handlers.get(msg.channel)?.forEach(h => h(msg.data));
    };

    this.ws.onclose = () => this._scheduleReconnect(token);
    this.ws.onerror = () => this.ws?.close();
  }

  subscribe(channel: string, handler: Handler): () => void {
    if (!this.handlers.has(channel)) this.handlers.set(channel, new Set());
    this.handlers.get(channel)!.add(handler);
    return () => this.handlers.get(channel)?.delete(handler);
  }

  disconnect(): void {
    if (this.reconnectTimer) clearTimeout(this.reconnectTimer);
    this.ws?.close();
    this.ws = null;
  }

  private _scheduleReconnect(token: string): void {
    this.reconnectTimer = setTimeout(() => {
      this.reconnectDelay = Math.min(this.reconnectDelay * 2, this.maxDelay);
      this.connect(token);
    }, this.reconnectDelay);
  }
}

export const wsManager = new WebSocketManager();
```

---

## Frontend Hook

```typescript
// app/src/shared/ws/useExpertWS.ts
import { useEffect } from 'react';
import { wsManager } from './WebSocketManager';
import { useAuthStore } from '@/modules/auth/store/authStore';

export function useExpertWS() {
  const token = useAuthStore(s => s.accessToken);

  useEffect(() => {
    if (token) wsManager.connect(token);
    return () => wsManager.disconnect();
  }, [token]);

  return { subscribe: wsManager.subscribe.bind(wsManager) };
}
```

---

## Redis Streams (Durable Event Log)

```python
# For durable events (signal history, audit trail) use Redis Streams
# NOT pub/sub (pub/sub is fire-and-forget)

async def publish_signal_event(redis: aioredis.Redis, signal: ProviderSignal) -> None:
    await redis.xadd(
        f"stream:signals:{signal.provider_id}",
        {"data": signal.model_dump_json()},
        maxlen=10_000,    # cap stream length
    )

async def consume_signal_events(redis: aioredis.Redis, provider_id: str, last_id: str = "0") -> list:
    results = await redis.xread(
        {f"stream:signals:{provider_id}": last_id},
        count=100,
        block=5000,   # wait up to 5s for new events
    )
    return results
```

---

## WebSocket Authentication (JWT from query param)

```python
# JWT in query param — because WS handshake cannot set Authorization header
# app/core/auth.py
async def get_ws_user(token: str, db: AsyncSession) -> User | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if not user_id:
            return None
        return await get_user_by_id(db, user_id)
    except JWTError:
        return None
```

---

## Anti-Patterns

```
✗ Creating a new WebSocket per component (use singleton manager)
✗ Polling REST while a WebSocket is open (wasteful and inconsistent)
✗ No reconnection logic (WebSocket connections drop regularly)
✗ No exponential backoff on reconnect (floods server on outage)
✗ Trusting WS messages without validation (validate schema on receipt)
✗ Storing WebSocket in React state (breaks singleton pattern)
✗ Using pub/sub for audit trail (use Redis Streams — pub/sub is lossy)
✗ Sending JWT as WS message body (use query param on handshake)
✗ Broadcasting to all users (always scope to user_id or account_id)
```
