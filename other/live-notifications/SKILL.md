---
name: Live Notifications
description: Delivering real-time updates to users via WebSocket, SSE, or Push API for live notification systems with proper architecture, queuing, and delivery mechanisms.
---

# Live Notifications

> **Current Level:** Intermediate  
> **Domain:** Real-time / Communication

---

## Overview

Live notification systems deliver real-time updates to users via WebSocket, SSE, or Push API. This guide covers architecture, implementation, and best practices for building notification systems that deliver timely updates to users across devices.

## Notification System Architecture

```
Event Source → Backend → Queue → Notification Service → Delivery
     ↓            ↓         ↓            ↓                ↓
  Database    Processing  Redis    WebSocket/SSE    User Device
```

## Database Schema

```sql
-- notifications table
CREATE TABLE notifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  
  type VARCHAR(50) NOT NULL,
  title VARCHAR(255) NOT NULL,
  message TEXT NOT NULL,
  
  data JSONB,
  
  read BOOLEAN DEFAULT FALSE,
  read_at TIMESTAMP,
  
  action_url VARCHAR(500),
  
  created_at TIMESTAMP DEFAULT NOW(),
  expires_at TIMESTAMP,
  
  INDEX idx_user (user_id),
  INDEX idx_read (user_id, read),
  INDEX idx_created (created_at)
);

-- notification_preferences table
CREATE TABLE notification_preferences (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  
  type VARCHAR(50) NOT NULL,
  enabled BOOLEAN DEFAULT TRUE,
  
  channels JSONB DEFAULT '{"web": true, "email": false, "push": false}',
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  UNIQUE(user_id, type)
);

-- notification_groups table
CREATE TABLE notification_groups (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  
  type VARCHAR(50) NOT NULL,
  count INTEGER DEFAULT 1,
  last_notification_id UUID REFERENCES notifications(id),
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_user_type (user_id, type)
);
```

## Real-time Delivery

### WebSocket Implementation

```typescript
// services/notification-socket.service.ts
import { Server, Socket } from 'socket.io';

export class NotificationSocketService {
  constructor(private io: Server) {
    this.setupHandlers();
  }

  private setupHandlers(): void {
    this.io.on('connection', (socket) => {
      const userId = socket.data.user.id;

      // Join user's notification room
      socket.join(`notifications:${userId}`);

      // Send unread count
      this.sendUnreadCount(socket, userId);

      // Mark as read
      socket.on('mark-as-read', async (notificationId: string) => {
        await this.markAsRead(notificationId, userId);
      });

      // Mark all as read
      socket.on('mark-all-as-read', async () => {
        await this.markAllAsRead(userId);
      });
    });
  }

  async sendNotification(userId: string, notification: Notification): Promise<void> {
    // Save to database
    const saved = await db.notification.create({
      data: {
        userId,
        type: notification.type,
        title: notification.title,
        message: notification.message,
        data: notification.data,
        actionUrl: notification.actionUrl
      }
    });

    // Send via WebSocket
    this.io.to(`notifications:${userId}`).emit('notification', {
      id: saved.id,
      type: saved.type,
      title: saved.title,
      message: saved.message,
      data: saved.data,
      actionUrl: saved.actionUrl,
      createdAt: saved.createdAt
    });

    // Update unread count
    await this.sendUnreadCount(null, userId);
  }

  private async sendUnreadCount(socket: Socket | null, userId: string): Promise<void> {
    const count = await db.notification.count({
      where: {
        userId,
        read: false
      }
    });

    const target = socket || this.io.to(`notifications:${userId}`);
    target.emit('unread-count', { count });
  }

  private async markAsRead(notificationId: string, userId: string): Promise<void> {
    await db.notification.update({
      where: {
        id: notificationId,
        userId
      },
      data: {
        read: true,
        readAt: new Date()
      }
    });

    await this.sendUnreadCount(null, userId);
  }

  private async markAllAsRead(userId: string): Promise<void> {
    await db.notification.updateMany({
      where: {
        userId,
        read: false
      },
      data: {
        read: true,
        readAt: new Date()
      }
    });

    await this.sendUnreadCount(null, userId);
  }
}

interface Notification {
  type: string;
  title: string;
  message: string;
  data?: any;
  actionUrl?: string;
}
```

### SSE Implementation

```typescript
// pages/api/notifications/stream.ts
import type { NextApiRequest, NextApiResponse } from 'next';

const clients = new Map<string, NextApiResponse>();

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const userId = req.query.userId as string;

  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  // Store client
  clients.set(userId, res);

  // Send initial unread count
  sendUnreadCount(userId, res);

  // Cleanup on disconnect
  req.on('close', () => {
    clients.delete(userId);
    res.end();
  });
}

async function sendUnreadCount(userId: string, res: NextApiResponse): Promise<void> {
  const count = await getUnreadCount(userId);
  res.write(`data: ${JSON.stringify({ type: 'unread-count', count })}\n\n`);
}

export async function sendNotificationToUser(userId: string, notification: any): Promise<void> {
  const client = clients.get(userId);
  if (client) {
    client.write(`data: ${JSON.stringify({ type: 'notification', ...notification })}\n\n`);
  }
}
```

## Notification Types

```typescript
// types/notifications.ts
export enum NotificationType {
  COMMENT = 'comment',
  MENTION = 'mention',
  LIKE = 'like',
  FOLLOW = 'follow',
  MESSAGE = 'message',
  SYSTEM = 'system',
  ORDER = 'order',
  PAYMENT = 'payment'
}

export interface NotificationTemplate {
  type: NotificationType;
  title: (data: any) => string;
  message: (data: any) => string;
  actionUrl: (data: any) => string;
}

export const notificationTemplates: Record<NotificationType, NotificationTemplate> = {
  [NotificationType.COMMENT]: {
    type: NotificationType.COMMENT,
    title: (data) => `New comment from ${data.userName}`,
    message: (data) => data.comment,
    actionUrl: (data) => `/posts/${data.postId}#comment-${data.commentId}`
  },
  [NotificationType.MENTION]: {
    type: NotificationType.MENTION,
    title: (data) => `${data.userName} mentioned you`,
    message: (data) => data.text,
    actionUrl: (data) => data.url
  },
  [NotificationType.LIKE]: {
    type: NotificationType.LIKE,
    title: (data) => `${data.userName} liked your post`,
    message: (data) => data.postTitle,
    actionUrl: (data) => `/posts/${data.postId}`
  }
};
```

## Notification Center UI

```typescript
// components/NotificationCenter.tsx
import { useEffect, useState } from 'react';
import { Bell } from 'lucide-react';

export function NotificationCenter() {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    const socket = getSocket();

    // Listen for new notifications
    socket.on('notification', (notification: Notification) => {
      setNotifications(prev => [notification, ...prev]);
      setUnreadCount(prev => prev + 1);
      
      // Show browser notification
      if (Notification.permission === 'granted') {
        new Notification(notification.title, {
          body: notification.message,
          icon: '/icon.png'
        });
      }
    });

    // Listen for unread count
    socket.on('unread-count', ({ count }: { count: number }) => {
      setUnreadCount(count);
    });

    // Load initial notifications
    loadNotifications();

    return () => {
      socket.off('notification');
      socket.off('unread-count');
    };
  }, []);

  const loadNotifications = async () => {
    const response = await fetch('/api/notifications');
    const data = await response.json();
    setNotifications(data.notifications);
  };

  const markAsRead = async (notificationId: string) => {
    const socket = getSocket();
    socket.emit('mark-as-read', notificationId);

    setNotifications(prev =>
      prev.map(n => n.id === notificationId ? { ...n, read: true } : n)
    );
  };

  const markAllAsRead = async () => {
    const socket = getSocket();
    socket.emit('mark-all-as-read');

    setNotifications(prev => prev.map(n => ({ ...n, read: true })));
    setUnreadCount(0);
  };

  return (
    <div className="notification-center">
      <button
        className="notification-button"
        onClick={() => setIsOpen(!isOpen)}
      >
        <Bell />
        {unreadCount > 0 && (
          <span className="badge">{unreadCount}</span>
        )}
      </button>

      {isOpen && (
        <div className="notification-dropdown">
          <div className="header">
            <h3>Notifications</h3>
            {unreadCount > 0 && (
              <button onClick={markAllAsRead}>Mark all as read</button>
            )}
          </div>

          <div className="notification-list">
            {notifications.length === 0 ? (
              <div className="empty">No notifications</div>
            ) : (
              notifications.map(notification => (
                <NotificationItem
                  key={notification.id}
                  notification={notification}
                  onRead={markAsRead}
                />
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
}

function NotificationItem({ notification, onRead }: NotificationItemProps) {
  return (
    <div
      className={`notification-item ${!notification.read ? 'unread' : ''}`}
      onClick={() => {
        if (!notification.read) {
          onRead(notification.id);
        }
        if (notification.actionUrl) {
          window.location.href = notification.actionUrl;
        }
      }}
    >
      <div className="notification-icon">
        {getNotificationIcon(notification.type)}
      </div>
      <div className="notification-content">
        <div className="title">{notification.title}</div>
        <div className="message">{notification.message}</div>
        <div className="time">{formatTime(notification.createdAt)}</div>
      </div>
      {!notification.read && <div className="unread-dot" />}
    </div>
  );
}
```

## Notification Preferences

```typescript
// services/notification-preferences.service.ts
export class NotificationPreferencesService {
  async getPreferences(userId: string): Promise<NotificationPreference[]> {
    return db.notificationPreference.findMany({
      where: { userId }
    });
  }

  async updatePreference(
    userId: string,
    type: string,
    updates: Partial<NotificationPreference>
  ): Promise<void> {
    await db.notificationPreference.upsert({
      where: {
        userId_type: { userId, type }
      },
      create: {
        userId,
        type,
        ...updates
      },
      update: updates
    });
  }

  async shouldSendNotification(
    userId: string,
    type: string,
    channel: 'web' | 'email' | 'push'
  ): Promise<boolean> {
    const preference = await db.notificationPreference.findUnique({
      where: {
        userId_type: { userId, type }
      }
    });

    if (!preference || !preference.enabled) {
      return false;
    }

    return preference.channels[channel] === true;
  }
}
```

## Grouping and Aggregation

```typescript
// services/notification-grouping.service.ts
export class NotificationGroupingService {
  async groupNotifications(userId: string, type: string): Promise<void> {
    const recentNotifications = await db.notification.findMany({
      where: {
        userId,
        type,
        createdAt: {
          gte: new Date(Date.now() - 60 * 60 * 1000) // Last hour
        }
      },
      orderBy: { createdAt: 'desc' }
    });

    if (recentNotifications.length >= 3) {
      // Create or update group
      await db.notificationGroup.upsert({
        where: {
          userId_type: { userId, type }
        },
        create: {
          userId,
          type,
          count: recentNotifications.length,
          lastNotificationId: recentNotifications[0].id
        },
        update: {
          count: recentNotifications.length,
          lastNotificationId: recentNotifications[0].id,
          updatedAt: new Date()
        }
      });

      // Send grouped notification
      await notificationSocketService.sendNotification(userId, {
        type: `${type}_group`,
        title: `${recentNotifications.length} new ${type}s`,
        message: 'Click to view all',
        actionUrl: `/notifications?type=${type}`
      });
    }
  }
}
```

## Rate Limiting

```typescript
// services/notification-rate-limiter.service.ts
export class NotificationRateLimiterService {
  private redis: Redis;

  constructor() {
    this.redis = new Redis(process.env.REDIS_URL!);
  }

  async canSendNotification(userId: string, type: string): Promise<boolean> {
    const key = `notification_rate:${userId}:${type}`;
    const count = await this.redis.incr(key);

    if (count === 1) {
      await this.redis.expire(key, 3600); // 1 hour window
    }

    // Max 10 notifications per hour per type
    return count <= 10;
  }

  async getRemainingQuota(userId: string, type: string): Promise<number> {
    const key = `notification_rate:${userId}:${type}`;
    const count = await this.redis.get(key);
    return Math.max(0, 10 - parseInt(count || '0'));
  }
}
```

## Mobile Push Integration

```typescript
// services/push-notification.service.ts
import admin from 'firebase-admin';

export class PushNotificationService {
  async sendPushNotification(
    userId: string,
    notification: Notification
  ): Promise<void> {
    // Get user's FCM tokens
    const tokens = await this.getUserTokens(userId);

    if (tokens.length === 0) {
      return;
    }

    const message = {
      notification: {
        title: notification.title,
        body: notification.message
      },
      data: {
        notificationId: notification.id,
        type: notification.type,
        actionUrl: notification.actionUrl || ''
      },
      tokens
    };

    const response = await admin.messaging().sendMulticast(message);

    // Remove invalid tokens
    if (response.failureCount > 0) {
      await this.removeInvalidTokens(userId, response.responses, tokens);
    }
  }

  private async getUserTokens(userId: string): Promise<string[]> {
    const devices = await db.device.findMany({
      where: {
        userId,
        fcmToken: { not: null }
      }
    });

    return devices.map(d => d.fcmToken!);
  }

  private async removeInvalidTokens(
    userId: string,
    responses: any[],
    tokens: string[]
  ): Promise<void> {
    const invalidTokens = responses
      .map((response, index) => ({
        response,
        token: tokens[index]
      }))
      .filter(({ response }) => !response.success)
      .map(({ token }) => token);

    if (invalidTokens.length > 0) {
      await db.device.deleteMany({
        where: {
          userId,
          fcmToken: { in: invalidTokens }
        }
      });
    }
  }
}
```

## Email Fallback

```typescript
// services/notification-email.service.ts
export class NotificationEmailService {
  async sendEmailNotification(
    userId: string,
    notification: Notification
  ): Promise<void> {
    const user = await db.user.findUnique({ where: { id: userId } });

    if (!user || !user.email) {
      return;
    }

    await emailService.send({
      to: user.email,
      subject: notification.title,
      template: 'notification',
      data: {
        title: notification.title,
        message: notification.message,
        actionUrl: notification.actionUrl,
        unsubscribeUrl: `/settings/notifications`
      }
    });
  }
}
```

## Analytics

```typescript
// services/notification-analytics.service.ts
export class NotificationAnalyticsService {
  async trackNotificationSent(notification: Notification): Promise<void> {
    await db.notificationAnalytics.create({
      data: {
        notificationId: notification.id,
        type: notification.type,
        event: 'sent',
        timestamp: new Date()
      }
    });
  }

  async trackNotificationRead(notificationId: string): Promise<void> {
    await db.notificationAnalytics.create({
      data: {
        notificationId,
        event: 'read',
        timestamp: new Date()
      }
    });
  }

  async trackNotificationClicked(notificationId: string): Promise<void> {
    await db.notificationAnalytics.create({
      data: {
        notificationId,
        event: 'clicked',
        timestamp: new Date()
      }
    });
  }

  async getNotificationMetrics(type: string): Promise<NotificationMetrics> {
    const analytics = await db.notificationAnalytics.findMany({
      where: {
        notification: { type }
      }
    });

    const sent = analytics.filter(a => a.event === 'sent').length;
    const read = analytics.filter(a => a.event === 'read').length;
    const clicked = analytics.filter(a => a.event === 'clicked').length;

    return {
      sent,
      read,
      clicked,
      readRate: sent > 0 ? (read / sent) * 100 : 0,
      clickRate: sent > 0 ? (clicked / sent) * 100 : 0
    };
  }
}

interface NotificationMetrics {
  sent: number;
  read: number;
  clicked: number;
  readRate: number;
  clickRate: number;
}
```

---

## Quick Start

### WebSocket Notifications

```typescript
// Server
io.on('connection', (socket) => {
  const userId = socket.handshake.auth.userId
  
  // Join user room
  socket.join(`user:${userId}`)
  
  // Send notification
  socket.emit('notification', {
    id: '123',
    type: 'message',
    title: 'New message',
    body: 'You have a new message',
    timestamp: Date.now()
  })
})

// Send to specific user
io.to('user:123').emit('notification', notificationData)
```

### Notification Queue

```typescript
class NotificationQueue {
  async enqueue(notification: Notification) {
    await redis.lpush('notifications', JSON.stringify(notification))
  }
  
  async process() {
    while (true) {
      const notification = await redis.brpop('notifications', 10)
      if (notification) {
        await this.deliver(JSON.parse(notification[1]))
      }
    }
  }
}
```

---

## Production Checklist

- [ ] **Real-time Delivery**: WebSocket or SSE for instant delivery
- [ ] **Persistence**: Store notifications in database
- [ ] **Preferences**: Respect user notification preferences
- [ ] **Grouping**: Group similar notifications
- [ ] **Queue**: Queue system for reliable delivery
- [ ] **Retry**: Retry failed deliveries
- [ ] **Analytics**: Track notification metrics
- [ ] **Performance**: Optimize for scale
- [ ] **Testing**: Test notification delivery
- [ ] **Documentation**: Document notification system
- [ ] **Monitoring**: Monitor delivery rates
- [ ] **Error Handling**: Handle delivery failures

---

## Anti-patterns

### ❌ Don't: No Persistence

```typescript
// ❌ Bad - No persistence
socket.emit('notification', notification)
// Lost if user offline!
```

```typescript
// ✅ Good - Persist notifications
await db.notifications.create({ data: notification })
socket.emit('notification', notification)
// User can fetch when back online
```

### ❌ Don't: Spam Users

```typescript
// ❌ Bad - Too many notifications
user.actions.forEach(action => {
  sendNotification(`You ${action}`)  // Spam!
})
```

```typescript
// ✅ Good - Group notifications
const actions = user.actions
sendNotification(`You have ${actions.length} updates`)
```

---

## Integration Points

- **WebSocket Patterns** (`34-real-time-features/websocket-patterns/`) - WebSocket implementation
- **Server-Sent Events** (`34-real-time-features/server-sent-events/`) - SSE alternative
- **Push Notifications** (`31-mobile-development/push-notifications/`) - Mobile push

---

## Further Reading

- [WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)

## Best Practices

1. **Real-time Delivery** - Use WebSocket for instant delivery
2. **Persistence** - Store notifications in database
3. **Preferences** - Respect user preferences
4. **Grouping** - Group similar notifications
5. **Rate Limiting** - Prevent notification spam
6. **Mobile Push** - Integrate with FCM/APNs
7. **Email Fallback** - Send email for important notifications
8. **Analytics** - Track notification metrics
9. **Performance** - Optimize for scale
10. **Testing** - Test notification delivery

## Resources

- [Socket.IO](https://socket.io/)
- [Firebase Cloud Messaging](https://firebase.google.com/docs/cloud-messaging)
- [Web Push API](https://developer.mozilla.org/en-US/docs/Web/API/Push_API)
- [Notification API](https://developer.mozilla.org/en-US/docs/Web/API/Notifications_API)
