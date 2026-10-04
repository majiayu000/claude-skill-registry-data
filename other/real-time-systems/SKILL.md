---
name: real-time-systems
description: Real-time & live-data systems — WebSocket, Server-Sent Events (SSE), Socket.IO, and WebRTC. Use when building chat, live notifications, presence, collaborative editing, live dashboards, multiplayer, or any bidirectional/streaming feature. Covers transport selection, horizontal scaling with a Redis adapter, delivery guarantees & reconnection/replay, auth on the handshake, backpressure/heartbeats, security, and serverless/Next.js caveats. Triggers on WebSocket, SSE, Socket.IO, WebRTC, real-time, live updates, presence, pub/sub fan-out, or instant messaging.
---

# Real-Time Systems — WebSocket, SSE & Live Data

**Agent**: Netflix Backend Architect (James Wilson) + Meta React Architect (Sarah Chen)
**Stack**: Node.js + TypeScript · **Targets**: native `ws`, Socket.IO 4+, SSE, WebRTC

The hard part of real-time isn't opening a socket — it's **reconnection, delivery
guarantees, auth, and scaling past one server**. Choose the simplest transport that meets
the need, then design for failure.

---

## 0. Transport decision — pick the simplest that works

| Need | Transport | Why |
|---|---|---|
| Server → client stream (notifications, live dashboard, progress, token streaming) | **SSE** | HTTP, auto-reconnect + `Last-Event-ID` built in, works through proxies, trivial to scale. **Default for one-way.** |
| Bidirectional, low-latency (chat, multiplayer, collab) | **WebSocket** | Full-duplex; use when the client must push frequently too |
| Bidirectional + rooms/namespaces + fallback + reconnection out of the box | **Socket.IO** | Batteries-included WS wrapper; best DX for production app features |
| Peer-to-peer media/data (video/voice calls, screen share) | **WebRTC** | Direct P2P; needs signaling (often over WS) + STUN/TURN |
| Occasional updates, must traverse hostile proxies | Long-poll / SSE | Avoid raw WS if infra is unfriendly |

**Guidance**: If data only flows server→client, **use SSE** — it's dramatically simpler
and more robust than WebSocket. Reach for WebSocket/Socket.IO only when the client pushes
often or you need rooms/presence. Don't adopt WebRTC unless you truly need P2P media.

---

## 1. SSE — the underrated default for one-way streams

```typescript
// Express — server → client stream
app.get('/events', authMiddleware, (req, res) => {
  res.set({
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache, no-transform',
    Connection: 'keep-alive',
  })
  res.flushHeaders()

  const send = (event: string, data: unknown, id?: string) => {
    if (id) res.write(`id: ${id}\n`)
    res.write(`event: ${event}\n`)
    res.write(`data: ${JSON.stringify(data)}\n\n`)   // blank line terminates the event
  }

  const heartbeat = setInterval(() => res.write(': ping\n\n'), 15000)  // keep proxies open
  const onNotify = (n: Notification) => send('notification', n, n.id)
  bus.on(`user:${req.userId}`, onNotify)

  req.on('close', () => { clearInterval(heartbeat); bus.off(`user:${req.userId}`, onNotify) })
})
```
Client: `new EventSource('/events')` auto-reconnects and sends `Last-Event-ID` so you can
**replay missed events** from that id. That reconnection+replay is free with SSE and
manual with raw WebSocket — a big reason to prefer it.

---

## 2. WebSocket (native `ws`) — when the client pushes too

```typescript
import { WebSocketServer } from 'ws'
const wss = new WebSocketServer({ server: httpServer, maxPayload: 1 << 20 /* 1MB cap */ })

wss.on('connection', (ws, req) => {
  const user = authenticate(req)                 // verify token from query/cookie — see §5
  if (!user) return ws.close(1008, 'unauthorized')

  ws.isAlive = true
  ws.on('pong', () => { ws.isAlive = true })     // liveness (see heartbeat below)
  ws.on('message', (raw) => {
    if (raw.length > 1 << 20) return ws.close(1009, 'too big')
    const msg = safeJson(raw); if (!msg) return  // never trust the payload
    handle(user, msg, ws)
  })
})

// Heartbeat: terminate dead peers so you don't leak connections
setInterval(() => {
  for (const ws of wss.clients) {
    if (!ws.isAlive) { ws.terminate(); continue }
    ws.isAlive = false; ws.ping()
  }
}, 30000)
```

---

## 3. Socket.IO — production app features (rooms, reconnection, fallback)

```typescript
import { Server } from 'socket.io'
const io = new Server(httpServer, { cors: { origin: ORIGIN, credentials: true } })

io.use((socket, next) => {                       // auth on the handshake
  try { socket.data.userId = verifyJwt(socket.handshake.auth.token).sub; next() }
  catch { next(new Error('unauthorized')) }
})

io.on('connection', (socket) => {
  socket.join(`user:${socket.data.userId}`)      // personal room for targeted pushes
  socket.on('join-room', (roomId) => {
    if (canJoin(socket.data.userId, roomId))     // authorize EVERY action, not just connect
      socket.join(roomId)
  })
  socket.on('send-message', async ({ roomId, text }) => {
    if (!canPost(socket.data.userId, roomId)) return
    const msg = await persist({ roomId, userId: socket.data.userId, text })  // save first
    io.to(roomId).emit('message', msg)           // then fan out
  })
})
```
Rooms are the scaling primitive — **target rooms, never loop over sockets**.

---

## 4. Scaling past one server (the step everyone forgets)

A second server instance breaks in-memory rooms: a user on server A can't receive a
message emitted on server B. Fix with a **pub/sub backplane** so all instances share events.

```typescript
import { createAdapter } from '@socket.io/redis-adapter'
import { createClient } from 'redis'
const pub = createClient({ url: process.env.REDIS_URL }); const sub = pub.duplicate()
await Promise.all([pub.connect(), sub.connect()])
io.adapter(createAdapter(pub, sub))              // rooms/emits now sync across instances
```
- Native `ws` / SSE: publish events to Redis Pub/Sub (or Streams for durability — see
  [[redis-expert]]); each instance subscribes and pushes to its local connections.
- **Sticky sessions**: Socket.IO's HTTP long-poll fallback needs the LB to pin a client to
  one instance (`sticky`/ip-hash), or force `transports: ['websocket']`. Pure WS/SSE don't.
- Behind Nginx/ALB: enable WebSocket upgrade headers and raise idle/proxy read timeouts
  above your heartbeat interval, or the proxy will kill idle connections.

---

## 5. Auth & security (do not skip)

- **Authenticate on the handshake** (JWT in `auth` payload, or a cookie), reject before
  accepting. Then **authorize every message/room action** — connection auth ≠ per-action authz.
- **Token expiry**: long-lived sockets outlive short JWTs. Re-check on sensitive actions,
  or push a "re-auth" event and disconnect on expiry.
- **Validate origin** (`cors.origin` allowlist) to prevent Cross-Site WebSocket Hijacking;
  use **WSS/HTTPS** in production.
- **Cap payload size** (`maxPayload`) and **rate-limit** messages per socket (token bucket
  in Redis) — a socket can flood you far faster than HTTP.
- **Never trust the client**: validate/parse every message (schema-check), and never
  broadcast raw user input without sanitizing for the consumers (XSS on the frontend).

---

## 6. Delivery guarantees & reconnection — design for the network dropping

Real networks drop. Decide your guarantee explicitly:

- **At-most-once** (Pub/Sub, plain emit): simplest; a reconnecting client misses whatever
  happened while offline. Fine for presence, typing indicators, live cursors.
- **At-least-once + replay** (durable): needed for chat/notifications where a lost message
  is a bug. Persist messages with a monotonic id; on (re)connect the client sends its last
  seen id and you **replay the gap** from the DB / Redis Stream. SSE gives you `Last-Event-ID`
  for free; for WS send `{ lastEventId }` on reconnect.
- **Idempotency & ordering**: include a stable message id; clients dedupe. If order matters,
  sequence per room and let clients reorder/buffer.
- **Presence**: track `online` in Redis with a TTL refreshed by heartbeat; on disconnect,
  start a short grace timer before marking offline (avoids flicker on brief drops).

Client reconnection (Socket.IO handles backoff; do the rejoin yourself):
```typescript
const socket = io(URL, { auth: { token }, reconnectionDelayMax: 5000 })
socket.on('connect', () => {
  socket.emit('resume', { rooms: myRooms, lastEventId })   // rejoin + request replay
})
```

---

## 7. Performance & backpressure

- **Batch** high-frequency updates (e.g. coalesce cursor moves to ~20–30/s); don't emit on
  every change.
- **Backpressure**: check `ws.bufferedAmount` (native) / drop or throttle for slow clients;
  a stuck consumer must not balloon server memory.
- **Binary** (MessagePack / protobuf) for high-throughput numeric streams; JSON is fine
  for chat-scale.
- **Fan-out cost**: broadcasting to a 100k-member room is expensive — shard rooms, or move
  to a managed fan-out service at that scale.

---

## 8. Serverless / Next.js caveat (common gotcha)

Serverless functions and the Next.js App Router **cannot hold a long-lived WebSocket** —
they're request-scoped and may freeze between invocations. Options:
- **SSE** works from a long-running Node route/runtime but NOT reliably on short-lived
  serverless; verify your platform supports streaming responses.
- Run a **separate always-on WS server** (a Node process / container), or use a **managed
  realtime service** (Pusher, Ably, Supabase Realtime, or a hosted Socket.IO). The Next.js
  app connects to it as a client. Don't try to host raw WS inside serverless functions.

---

## 9. Pre-ship self-check

1. Is this actually one-way? If so, are you using **SSE** instead of WebSocket?
2. Handshake authenticated **and** every message/room action authorized?
3. Origin allowlisted, WSS/HTTPS, payload capped, per-socket rate limit?
4. Heartbeat + dead-connection cleanup (no leaked sockets)?
5. Does it work with **more than one server instance** (Redis adapter / pub-sub backplane)?
6. On reconnect, does the client **rejoin rooms and replay missed messages** (or is
   at-most-once acceptable here)?
7. Messages persisted before fan-out (so history/replay is possible)?
8. High-frequency updates batched; slow clients handled (backpressure)?
9. On serverless/Next.js: WS handled by a dedicated server or managed service, not a function?

Related: [[redis-expert]] (adapter, presence, durable Streams), [[node-backend]],
[[microservices]], [[security-expert]].
