---
name: real-time-systems
description: Real-Time Systems - WebSocket & Live Data Mastery. Build chat apps, live dashboards, collaborative tools, multiplayer games, or real-time notifications. Use when implementing bidirectional communication, live updates, or instant messaging.
---

# Real-Time Systems - WebSocket & Live Data Mastery

**Purpose**: Build real-time, bidirectional communication systems for chat, notifications, collaboration, and live updates

**Agent**: Netflix Backend Architect / Meta React Architect
**Use When**: Building chat apps, live dashboards, collaborative tools, multiplayer games, or real-time notifications

---

## Overview

Real-time systems enable instant, bidirectional communication between clients and servers without polling.

**Technologies**:
- **WebSocket**: Full-duplex communication over TCP
- **Server-Sent Events (SSE)**: Server-to-client streaming
- **Socket.IO**: WebSocket wrapper with fallbacks
- **WebRTC**: Peer-to-peer video/audio/data

**Use Cases**:
- Chat applications
- Live notifications
- Collaborative editing (Google Docs)
- Live dashboards
- Multiplayer games
- Stock tickers

---

## Technology Comparison

| Technology | Direction | Use Case | Complexity |
|------------|-----------|----------|------------|
| WebSocket | Bidirectional | Chat, games, collaboration | Medium |
| SSE | Server → Client | Notifications, dashboards | Low |
| Socket.IO | Bidirectional | Production apps with fallbacks | Low |
| WebRTC | P2P | Video/audio calls, file sharing | High |

### When to Use What

- **WebSocket (native)**: Full control, minimal overhead, browser-only
- **Socket.IO**: Production apps, needs rooms/namespaces, fallback support
- **SSE**: One-way server updates (dashboards, notifications)
- **WebRTC**: Direct peer communication (video calls)

---

## Quick Start: Socket.IO (Recommended)

### Server
```typescript
import { Server } from 'socket.io'
import { createServer } from 'http'

const httpServer = createServer()
const io = new Server(httpServer, {
  cors: { origin: 'http://localhost:3000', credentials: true }
})

io.on('connection', (socket) => {
  socket.on('join-room', (roomId) => socket.join(roomId))

  socket.on('send-message', ({ roomId, message }) => {
    io.to(roomId).emit('receive-message', {
      senderId: socket.id,
      message,
      timestamp: Date.now()
    })
  })
})

httpServer.listen(8080)
```

### Client (React)
```typescript
import { useEffect, useState } from 'react'
import { io } from 'socket.io-client'

const socket = io('http://localhost:8080')

function Chat() {
  const [messages, setMessages] = useState([])

  useEffect(() => {
    socket.emit('join-room', 'room-123')
    socket.on('receive-message', (data) => {
      setMessages(prev => [...prev, data])
    })
    return () => socket.off('receive-message')
  }, [])

  const sendMessage = (text) => {
    socket.emit('send-message', { roomId: 'room-123', message: text })
  }

  return <div>{/* UI */}</div>
}
```

---

## Common Patterns

### 1. Chat Application
- User authentication via handshake
- Room management (join/leave)
- Typing indicators
- Message persistence to database
- User presence tracking

### 2. Live Notifications
- Redis Pub/Sub for multi-server
- User-specific rooms (`user:${userId}`)
- Push from anywhere in app

### 3. Live Dashboard
- Periodic stats broadcast
- Dashboard room subscription
- Rolling window data (last 60 seconds)

### 4. Collaborative Editing
- Operational Transform for conflict resolution
- Document state sync on join
- Cursor position sharing

**For detailed code examples**: Read `references/code-examples.md`

---

## Best Practices

### 1. Authentication
```typescript
io.use((socket, next) => {
  const token = socket.handshake.auth.token
  try {
    socket.userId = jwt.verify(token, process.env.JWT_SECRET).userId
    next()
  } catch (error) {
    next(new Error('Authentication failed'))
  }
})
```

### 2. Reconnection Handling
```typescript
const socket = io('http://localhost:8080', {
  reconnection: true,
  reconnectionDelay: 1000,
  reconnectionDelayMax: 5000,
  reconnectionAttempts: 5
})

socket.on('connect', () => {
  socket.emit('join-room', currentRoomId) // Rejoin rooms
})
```

### 3. Rate Limiting
- Track message timestamps per socket
- Limit to X messages per minute
- Emit error on exceed

### 4. Horizontal Scaling
```typescript
import { createAdapter } from '@socket.io/redis-adapter'

io.adapter(createAdapter(pubClient, subClient))
// Now multiple Socket.IO servers sync via Redis
```

---

## Performance Tips

| Pattern | Bad | Good |
|---------|-----|------|
| Data format | JSON for everything | Binary (MessagePack) for high-frequency |
| Updates | Send every change | Batch updates |
| Targeting | Loop through sockets | Use rooms |

---

## Monitoring

```typescript
io.on('connection', (socket) => {
  console.log(`Total: ${io.engine.clientsCount}`)
})

setInterval(() => {
  console.log('Rooms:', io.sockets.adapter.rooms.size)
  console.log('Memory:', process.memoryUsage())
}, 60000)
```

---

## Reference Files

For detailed code examples including:
- WebSocket native implementation
- Socket.IO server/client patterns
- Server-Sent Events
- Chat, notifications, dashboard, collaborative editing
- Authentication, reconnection, rate limiting
- Performance optimization

**Read**: `references/code-examples.md`

---

**Remember**: Real-time systems need careful design. Handle reconnections, authenticate users, rate limit, and scale horizontally with Redis.

**Created**: 2026-02-04
**Maintained By**: Netflix Backend Architect
**Version**: Socket.IO 4+
