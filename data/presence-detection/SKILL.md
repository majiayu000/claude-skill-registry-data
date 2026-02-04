---
name: Presence Detection
description: Tracking user online/offline status, typing indicators, and activity states using WebSocket connections and Redis for real-time presence information.
---

# Presence Detection

> **Current Level:** Intermediate  
> **Domain:** Real-time / Backend

---

## Overview

Presence detection tracks user online/offline status, typing indicators, and activity states. This guide covers implementation patterns using WebSocket and Redis to provide real-time presence information for collaborative features, chat applications, and live user status.

---

## Presence Concepts

```
States:
- Online: User is active
- Away: User is idle
- Busy: User is in focus mode
- Offline: User is disconnected

Events:
- User joined
- User left
- User typing
- User stopped typing
- Status changed
```

## Online/Offline Status

```typescript
// services/presence.service.ts
import { Server, Socket } from 'socket.io';
import { Redis } from 'ioredis';

export class PresenceService {
  private redis: Redis;

  constructor(private io: Server) {
    this.redis = new Redis(process.env.REDIS_URL!);
    this.setupHandlers();
  }

  private setupHandlers(): void {
    this.io.on('connection', async (socket) => {
      const userId = socket.data.user.id;

      // Set user online
      await this.setUserOnline(userId, socket.id);

      // Broadcast to others
      socket.broadcast.emit('user-online', {
        userId,
        timestamp: Date.now()
      });

      // Handle disconnect
      socket.on('disconnect', async () => {
        await this.setUserOffline(userId, socket.id);

        // Check if user has other connections
        const isOnline = await this.isUserOnline(userId);
        
        if (!isOnline) {
          socket.broadcast.emit('user-offline', {
            userId,
            timestamp: Date.now()
          });
        }
      });
    });
  }

  async setUserOnline(userId: string, socketId: string): Promise<void> {
    const key = `presence:${userId}`;
    
    // Add socket to user's set
    await this.redis.sadd(key, socketId);
    
    // Set expiry (auto-cleanup)
    await this.redis.expire(key, 3600);

    // Update last seen
    await this.updateLastSeen(userId);
  }

  async setUserOffline(userId: string, socketId: string): Promise<void> {
    const key = `presence:${userId}`;
    await this.redis.srem(key, socketId);
  }

  async isUserOnline(userId: string): Promise<boolean> {
    const key = `presence:${userId}`;
    const count = await this.redis.scard(key);
    return count > 0;
  }

  async getOnlineUsers(): Promise<string[]> {
    const keys = await this.redis.keys('presence:*');
    const userIds: string[] = [];

    for (const key of keys) {
      const count = await this.redis.scard(key);
      if (count > 0) {
        userIds.push(key.replace('presence:', ''));
      }
    }

    return userIds;
  }

  async updateLastSeen(userId: string): Promise<void> {
    const key = `last_seen:${userId}`;
    await this.redis.set(key, Date.now());
  }

  async getLastSeen(userId: string): Promise<number | null> {
    const key = `last_seen:${userId}`;
    const timestamp = await this.redis.get(key);
    return timestamp ? parseInt(timestamp) : null;
  }
}
```

## Heartbeat Mechanism

```typescript
// Client-side heartbeat
class PresenceClient {
  private heartbeatInterval: NodeJS.Timeout | null = null;
  private socket: Socket;

  constructor(socket: Socket) {
    this.socket = socket;
    this.startHeartbeat();
  }

  private startHeartbeat(): void {
    // Send heartbeat every 30 seconds
    this.heartbeatInterval = setInterval(() => {
      this.socket.emit('heartbeat', {
        timestamp: Date.now()
      });
    }, 30000);
  }

  stopHeartbeat(): void {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = null;
    }
  }
}

// Server-side heartbeat handler
socket.on('heartbeat', async () => {
  const userId = socket.data.user.id;
  await presenceService.updateLastSeen(userId);
});

// Check for stale connections
setInterval(async () => {
  const onlineUsers = await presenceService.getOnlineUsers();
  
  for (const userId of onlineUsers) {
    const lastSeen = await presenceService.getLastSeen(userId);
    
    if (lastSeen && Date.now() - lastSeen > 60000) {
      // User hasn't sent heartbeat in 60 seconds
      await presenceService.markUserAsAway(userId);
    }
  }
}, 30000);
```

## Typing Indicators

```typescript
// services/typing-indicator.service.ts
export class TypingIndicatorService {
  private typingUsers = new Map<string, Set<string>>();
  private typingTimeouts = new Map<string, NodeJS.Timeout>();

  constructor(private io: Server) {
    this.setupHandlers();
  }

  private setupHandlers(): void {
    this.io.on('connection', (socket) => {
      socket.on('typing-start', ({ roomId }) => {
        this.handleTypingStart(socket, roomId);
      });

      socket.on('typing-stop', ({ roomId }) => {
        this.handleTypingStop(socket, roomId);
      });

      socket.on('disconnect', () => {
        this.handleDisconnect(socket);
      });
    });
  }

  private handleTypingStart(socket: Socket, roomId: string): void {
    const userId = socket.data.user.id;
    const key = `${roomId}:${userId}`;

    // Add user to typing set
    if (!this.typingUsers.has(roomId)) {
      this.typingUsers.set(roomId, new Set());
    }
    this.typingUsers.get(roomId)!.add(userId);

    // Broadcast to room
    socket.to(roomId).emit('user-typing', {
      userId,
      userName: socket.data.user.name
    });

    // Auto-stop after 3 seconds
    if (this.typingTimeouts.has(key)) {
      clearTimeout(this.typingTimeouts.get(key)!);
    }

    const timeout = setTimeout(() => {
      this.handleTypingStop(socket, roomId);
    }, 3000);

    this.typingTimeouts.set(key, timeout);
  }

  private handleTypingStop(socket: Socket, roomId: string): void {
    const userId = socket.data.user.id;
    const key = `${roomId}:${userId}`;

    // Remove user from typing set
    this.typingUsers.get(roomId)?.delete(userId);

    // Clear timeout
    if (this.typingTimeouts.has(key)) {
      clearTimeout(this.typingTimeouts.get(key)!);
      this.typingTimeouts.delete(key);
    }

    // Broadcast to room
    socket.to(roomId).emit('user-stopped-typing', { userId });
  }

  private handleDisconnect(socket: Socket): void {
    const userId = socket.data.user.id;

    // Remove from all rooms
    this.typingUsers.forEach((users, roomId) => {
      if (users.has(userId)) {
        users.delete(userId);
        socket.to(roomId).emit('user-stopped-typing', { userId });
      }
    });

    // Clear all timeouts for this user
    this.typingTimeouts.forEach((timeout, key) => {
      if (key.endsWith(`:${userId}`)) {
        clearTimeout(timeout);
        this.typingTimeouts.delete(key);
      }
    });
  }

  getTypingUsers(roomId: string): string[] {
    return Array.from(this.typingUsers.get(roomId) || []);
  }
}
```

## Client-Side Typing Indicator

```typescript
// hooks/useTypingIndicator.ts
import { useEffect, useState, useCallback } from 'react';
import { Socket } from 'socket.io-client';
import { debounce } from 'lodash';

export function useTypingIndicator(socket: Socket | null, roomId: string) {
  const [typingUsers, setTypingUsers] = useState<string[]>([]);

  useEffect(() => {
    if (!socket) return;

    socket.on('user-typing', ({ userId, userName }) => {
      setTypingUsers(prev => {
        if (!prev.includes(userName)) {
          return [...prev, userName];
        }
        return prev;
      });
    });

    socket.on('user-stopped-typing', ({ userId }) => {
      setTypingUsers(prev => prev.filter(name => name !== userId));
    });

    return () => {
      socket.off('user-typing');
      socket.off('user-stopped-typing');
    };
  }, [socket]);

  const startTyping = useCallback(() => {
    socket?.emit('typing-start', { roomId });
  }, [socket, roomId]);

  const stopTyping = useCallback(() => {
    socket?.emit('typing-stop', { roomId });
  }, [socket, roomId]);

  const debouncedStopTyping = useMemo(
    () => debounce(stopTyping, 1000),
    [stopTyping]
  );

  const handleTyping = useCallback(() => {
    startTyping();
    debouncedStopTyping();
  }, [startTyping, debouncedStopTyping]);

  return { typingUsers, handleTyping };
}

// Usage
function ChatInput({ roomId }: { roomId: string }) {
  const { socket } = useSocket();
  const { typingUsers, handleTyping } = useTypingIndicator(socket, roomId);

  return (
    <div>
      {typingUsers.length > 0 && (
        <div className="typing-indicator">
          {typingUsers.join(', ')} {typingUsers.length === 1 ? 'is' : 'are'} typing...
        </div>
      )}
      <input
        type="text"
        onChange={handleTyping}
        placeholder="Type a message..."
      />
    </div>
  );
}
```

## Active/Away/Busy Status

```typescript
// services/user-status.service.ts
export class UserStatusService {
  async setUserStatus(userId: string, status: UserStatus): Promise<void> {
    const key = `status:${userId}`;
    
    await this.redis.hset(key, {
      status,
      updatedAt: Date.now()
    });

    await this.redis.expire(key, 3600);

    // Broadcast status change
    this.io.emit('user-status-changed', {
      userId,
      status,
      timestamp: Date.now()
    });
  }

  async getUserStatus(userId: string): Promise<UserStatus> {
    const key = `status:${userId}`;
    const data = await this.redis.hgetall(key);
    
    if (!data.status) {
      return 'offline';
    }

    return data.status as UserStatus;
  }

  async setCustomStatus(userId: string, customStatus: CustomStatus): Promise<void> {
    const key = `custom_status:${userId}`;
    
    await this.redis.hset(key, {
      text: customStatus.text,
      emoji: customStatus.emoji,
      expiresAt: customStatus.expiresAt || 0
    });

    this.io.emit('user-custom-status-changed', {
      userId,
      customStatus
    });
  }
}

type UserStatus = 'online' | 'away' | 'busy' | 'offline';

interface CustomStatus {
  text: string;
  emoji?: string;
  expiresAt?: number;
}

// Client-side idle detection
class IdleDetector {
  private idleTimeout: NodeJS.Timeout | null = null;
  private idleTime = 5 * 60 * 1000; // 5 minutes

  constructor(private onIdle: () => void, private onActive: () => void) {
    this.setupListeners();
  }

  private setupListeners(): void {
    ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'].forEach(
      (event) => {
        document.addEventListener(event, () => this.resetIdleTimer(), true);
      }
    );

    this.resetIdleTimer();
  }

  private resetIdleTimer(): void {
    if (this.idleTimeout) {
      clearTimeout(this.idleTimeout);
    }

    this.onActive();

    this.idleTimeout = setTimeout(() => {
      this.onIdle();
    }, this.idleTime);
  }
}

// Usage
const idleDetector = new IdleDetector(
  () => {
    socket.emit('set-status', { status: 'away' });
  },
  () => {
    socket.emit('set-status', { status: 'online' });
  }
);
```

## Presence UI Components

```typescript
// components/UserPresence.tsx
import { useEffect, useState } from 'react';

interface PresenceProps {
  userId: string;
  showLastSeen?: boolean;
}

export function UserPresence({ userId, showLastSeen = true }: PresenceProps) {
  const [status, setStatus] = useState<UserStatus>('offline');
  const [lastSeen, setLastSeen] = useState<number | null>(null);

  useEffect(() => {
    const socket = getSocket();

    // Get initial status
    socket.emit('get-user-status', { userId }, (response: any) => {
      setStatus(response.status);
      setLastSeen(response.lastSeen);
    });

    // Listen for status changes
    socket.on('user-status-changed', (data: any) => {
      if (data.userId === userId) {
        setStatus(data.status);
      }
    });

    socket.on('user-online', (data: any) => {
      if (data.userId === userId) {
        setStatus('online');
      }
    });

    socket.on('user-offline', (data: any) => {
      if (data.userId === userId) {
        setStatus('offline');
        setLastSeen(data.timestamp);
      }
    });

    return () => {
      socket.off('user-status-changed');
      socket.off('user-online');
      socket.off('user-offline');
    };
  }, [userId]);

  return (
    <div className="user-presence">
      <div className={`status-indicator status-${status}`} />
      {status === 'offline' && showLastSeen && lastSeen && (
        <span className="last-seen">
          Last seen {formatLastSeen(lastSeen)}
        </span>
      )}
    </div>
  );
}

function formatLastSeen(timestamp: number): string {
  const diff = Date.now() - timestamp;
  const minutes = Math.floor(diff / 60000);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);

  if (days > 0) return `${days}d ago`;
  if (hours > 0) return `${hours}h ago`;
  if (minutes > 0) return `${minutes}m ago`;
  return 'just now';
}
```

## Performance at Scale

```typescript
// Use Redis Pub/Sub for multi-server setup
const publisher = createClient({ url: process.env.REDIS_URL });
const subscriber = publisher.duplicate();

await Promise.all([publisher.connect(), subscriber.connect()]);

// Subscribe to presence events
await subscriber.subscribe('presence:online', (message) => {
  const { userId } = JSON.parse(message);
  io.emit('user-online', { userId, timestamp: Date.now() });
});

await subscriber.subscribe('presence:offline', (message) => {
  const { userId } = JSON.parse(message);
  io.emit('user-offline', { userId, timestamp: Date.now() });
});

// Publish presence events
async function publishUserOnline(userId: string): Promise<void> {
  await publisher.publish('presence:online', JSON.stringify({ userId }));
}

async function publishUserOffline(userId: string): Promise<void> {
  await publisher.publish('presence:offline', JSON.stringify({ userId }));
}
```

---

## Quick Start

### Presence with WebSocket

```javascript
const io = require('socket.io')(server)

io.on('connection', (socket) => {
  const userId = socket.handshake.auth.userId
  
  // User comes online
  socket.on('presence:online', () => {
    redis.set(`presence:${userId}`, 'online', 'EX', 300)  // 5 min TTL
    io.emit('presence:update', { userId, status: 'online' })
  })
  
  // Heartbeat
  socket.on('presence:heartbeat', () => {
    redis.set(`presence:${userId}`, 'online', 'EX', 300)
  })
  
  // User goes offline
  socket.on('disconnect', () => {
    redis.del(`presence:${userId}`)
    io.emit('presence:update', { userId, status: 'offline' })
  })
})
```

### Typing Indicator

```javascript
const typingUsers = new Map()

socket.on('typing:start', ({ channelId }) => {
  typingUsers.set(`${userId}:${channelId}`, Date.now())
  io.to(channelId).emit('typing:update', { userId, typing: true })
  
  // Auto-stop after 3 seconds
  setTimeout(() => {
    typingUsers.delete(`${userId}:${channelId}`)
    io.to(channelId).emit('typing:update', { userId, typing: false })
  }, 3000)
})
```

---

## Production Checklist

- [ ] **Heartbeat**: Implement heartbeat to detect disconnections
- [ ] **Redis**: Store presence in Redis for performance
- [ ] **Pub/Sub**: Use pub/sub for multi-server setups
- [ ] **TTL**: Set TTL on presence keys
- [ ] **Typing Indicators**: Implement typing indicators
- [ ] **Status States**: Support multiple status states (online, away, busy)
- [ ] **Privacy**: Respect user privacy settings
- [ ] **Performance**: Optimize for high user counts
- [ ] **Monitoring**: Monitor presence system health
- [ ] **Testing**: Test with network interruptions
- [ ] **Documentation**: Document presence API
- [ ] **Rate Limiting**: Limit presence updates

---

## Anti-patterns

### ❌ Don't: No Heartbeat

```javascript
// ❌ Bad - No heartbeat
socket.on('connect', () => {
  setPresence(userId, 'online')  // Never updates!
})
```

```javascript
// ✅ Good - Heartbeat
socket.on('connect', () => {
  setPresence(userId, 'online')
  
  // Send heartbeat every 30 seconds
  const heartbeat = setInterval(() => {
    socket.emit('presence:heartbeat')
  }, 30000)
  
  socket.on('disconnect', () => clearInterval(heartbeat))
})
```

### ❌ Don't: No TTL

```javascript
// ❌ Bad - Presence never expires
redis.set(`presence:${userId}`, 'online')  // Stays forever!
```

```javascript
// ✅ Good - TTL on presence
redis.set(`presence:${userId}`, 'online', 'EX', 300)  // Expires in 5 min
```

---

## Integration Points

- **WebSocket Patterns** (`34-real-time-features/websocket-patterns/`) - WebSocket implementation
- **Live Chat** (`29-customer-support/live-chat/`) - Chat presence
- **Redis Caching** (`04-database/redis-caching/`) - Presence storage

---

## Further Reading

- [Socket.io Presence](https://socket.io/docs/v4/rooms/)
- [Redis Pub/Sub](https://redis.io/docs/manual/pubsub/)
4. **Debouncing** - Debounce typing indicators
5. **Idle Detection** - Detect idle users
6. **Last Seen** - Track last seen timestamp
7. **Cleanup** - Clean up stale presence data
8. **Privacy** - Respect user privacy settings
9. **Performance** - Optimize for scale
10. **Mobile** - Handle mobile app lifecycle

## Resources

- [Socket.IO](https://socket.io/)
- [Redis](https://redis.io/)
- [Presence Patterns](https://www.pubnub.com/blog/how-to-build-user-presence-detection/)
