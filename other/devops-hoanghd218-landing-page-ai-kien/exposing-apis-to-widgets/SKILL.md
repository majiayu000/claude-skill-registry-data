---
name: exposing-apis-to-widgets
description: Exposing StickerNest APIs to widgets via the Protocol. Use when the user asks about widget API, widget requests, social API for widgets, widget permissions, widget:request, or how widgets call backend services. Covers Protocol messages, request handling, and permission system.
---

# Exposing APIs to Widgets

This skill covers how to expose StickerNest services to widgets through the Widget Protocol, enabling widgets to access social features, data, and actions securely.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        Widget (iframe)                       │
│                                                              │
│   WidgetAPI.request('social:getFeed', { type: 'public' })   │
│                            │                                 │
└────────────────────────────┼────────────────────────────────┘
                             │ postMessage
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                      WidgetHost                              │
│                                                              │
│   1. Validate permission (social:read)                       │
│   2. Route to handler                                        │
│   3. Call service (FeedService.getGlobalFeed)               │
│   4. Return result                                           │
│                            │                                 │
└────────────────────────────┼────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                       Services                               │
│   FeedService │ ChatService │ SocialGraphService            │
└─────────────────────────────────────────────────────────────┘
```

---

## Protocol Message Types

### Widget → Host: Request

```typescript
// Widget sends
window.parent.postMessage({
  type: 'widget:request',
  payload: {
    requestId: 'req-123',  // Unique ID for matching response
    action: 'social:getFeed',
    data: { type: 'public', limit: 20 },
  },
}, '*');
```

### Host → Widget: Response

```typescript
// Host responds
iframe.contentWindow.postMessage({
  type: 'widget:response',
  payload: {
    requestId: 'req-123',  // Matches request
    result: { activities: [...] },
    error: null,  // Or error message if failed
  },
}, '*');
```

---

## Widget-Side API

### Request Helper

```javascript
// In widget code
const WidgetAPI = {
  pendingRequests: new Map(),

  request(action, data = {}) {
    return new Promise((resolve, reject) => {
      const requestId = `req-${Date.now()}-${Math.random().toString(36).slice(2)}`;

      // Store resolver
      this.pendingRequests.set(requestId, { resolve, reject });

      // Send request
      window.parent.postMessage({
        type: 'widget:request',
        payload: { requestId, action, data },
      }, '*');

      // Timeout after 30 seconds
      setTimeout(() => {
        if (this.pendingRequests.has(requestId)) {
          this.pendingRequests.delete(requestId);
          reject(new Error('Request timeout'));
        }
      }, 30000);
    });
  },

  handleResponse(payload) {
    const { requestId, result, error } = payload;
    const pending = this.pendingRequests.get(requestId);

    if (pending) {
      this.pendingRequests.delete(requestId);
      if (error) {
        pending.reject(new Error(error));
      } else {
        pending.resolve(result);
      }
    }
  },

  // Convenience methods
  async getFeed(type = 'public', limit = 20) {
    return this.request('social:getFeed', { type, limit });
  },

  async follow(userId) {
    return this.request('social:follow', { userId });
  },

  async sendMessage(channelId, content) {
    return this.request('social:sendMessage', { channelId, content });
  },

  async getProfile(userId) {
    return this.request('social:getProfile', { userId });
  },
};

// Listen for responses
window.addEventListener('message', (event) => {
  if (event.data?.type === 'widget:response') {
    WidgetAPI.handleResponse(event.data.payload);
  }
});
```

---

## Host-Side Request Handler

### WidgetHost Implementation

```typescript
// src/runtime/WidgetHost.ts

import { FeedService } from '@/services/social/FeedService';
import { ChatService } from '@/services/social/ChatService';
import { SocialGraphService } from '@/services/social/SocialGraphService';
import { ProfileService } from '@/services/social/ProfileService';
import { NotificationService } from '@/services/social/NotificationService';

interface WidgetRequest {
  requestId: string;
  action: string;
  data: Record<string, any>;
}

class WidgetHost {
  private manifest: WidgetManifest;
  private iframe: HTMLIFrameElement;
  private authContext: AuthContextType;

  constructor(manifest: WidgetManifest, iframe: HTMLIFrameElement, auth: AuthContextType) {
    this.manifest = manifest;
    this.iframe = iframe;
    this.authContext = auth;

    window.addEventListener('message', this.handleMessage.bind(this));
  }

  private handleMessage(event: MessageEvent) {
    // Verify origin matches iframe
    if (event.source !== this.iframe.contentWindow) return;

    const { type, payload } = event.data || {};

    if (type === 'widget:request') {
      this.handleRequest(payload as WidgetRequest);
    }
  }

  private async handleRequest(request: WidgetRequest) {
    const { requestId, action, data } = request;

    try {
      // Check permission
      if (!this.hasPermission(action)) {
        throw new Error(`Permission denied: ${action}`);
      }

      // Route to handler
      const result = await this.routeAction(action, data);

      // Send success response
      this.sendResponse(requestId, result, null);
    } catch (err) {
      // Send error response
      this.sendResponse(requestId, null, err.message);
    }
  }

  private hasPermission(action: string): boolean {
    const permissions = this.manifest.permissions || [];

    // Map actions to required permissions
    const permissionMap: Record<string, string> = {
      'social:getFeed': 'social:read',
      'social:getProfile': 'social:read',
      'social:getMessages': 'social:read',
      'social:getNotifications': 'social:read',
      'social:follow': 'social:write',
      'social:unfollow': 'social:write',
      'social:sendMessage': 'social:write',
      'social:markRead': 'social:write',
      'canvas:getData': 'canvas:read',
      'canvas:setData': 'canvas:write',
      'storage:get': 'storage:read',
      'storage:set': 'storage:write',
    };

    const required = permissionMap[action];
    if (!required) return false;

    return permissions.includes(required) || permissions.includes('*');
  }

  private async routeAction(action: string, data: any): Promise<any> {
    // Require authentication for most actions
    if (action.startsWith('social:') && !this.authContext.isAuthenticated) {
      throw new Error('Authentication required');
    }

    switch (action) {
      // === Feed API ===
      case 'social:getFeed':
        return this.handleGetFeed(data);

      // === Profile API ===
      case 'social:getProfile':
        return ProfileService.getProfile(data.userId);

      case 'social:searchProfiles':
        return ProfileService.searchProfiles(data.query, data.limit);

      // === Social Graph API ===
      case 'social:follow':
        return SocialGraphService.followUser(data.userId);

      case 'social:unfollow':
        return SocialGraphService.unfollowUser(data.userId);

      case 'social:getFollowers':
        return SocialGraphService.getFollowers(data.userId, data.limit);

      case 'social:getFollowing':
        return SocialGraphService.getFollowing(data.userId, data.limit);

      case 'social:checkFollowing':
        return SocialGraphService.checkIsFollowing(data.userId);

      // === Chat API ===
      case 'social:getMessages':
        return ChatService.getMessages(data.channelId, data.limit, data.before);

      case 'social:sendMessage':
        return ChatService.sendMessage(data.channelId, data.content, data.replyTo);

      case 'social:deleteMessage':
        return ChatService.deleteMessage(data.messageId);

      // === Notification API ===
      case 'social:getNotifications':
        return NotificationService.getNotifications(data.limit);

      case 'social:markRead':
        return NotificationService.markAsRead(data.notificationId);

      case 'social:markAllRead':
        return NotificationService.markAllAsRead();

      // === Presence API ===
      case 'social:getOnlineUsers':
        return this.getOnlineUsers(data.canvasId);

      // === Storage API ===
      case 'storage:get':
        return this.getWidgetStorage(data.key);

      case 'storage:set':
        return this.setWidgetStorage(data.key, data.value);

      default:
        throw new Error(`Unknown action: ${action}`);
    }
  }

  private async handleGetFeed(data: { type: string; limit?: number; offset?: number }) {
    const { type, limit = 20, offset = 0 } = data;

    switch (type) {
      case 'public':
        return FeedService.getGlobalFeed(limit, offset);
      case 'friends':
        return FeedService.getFriendsFeed(limit, offset);
      case 'user':
        return FeedService.getUserFeed(data.userId, limit, offset);
      default:
        throw new Error(`Unknown feed type: ${type}`);
    }
  }

  private sendResponse(requestId: string, result: any, error: string | null) {
    this.iframe.contentWindow?.postMessage({
      type: 'widget:response',
      payload: { requestId, result, error },
    }, '*');
  }

  // Widget-specific storage
  private async getWidgetStorage(key: string): Promise<any> {
    const storageKey = `widget:${this.manifest.id}:${key}`;
    const value = localStorage.getItem(storageKey);
    return value ? JSON.parse(value) : null;
  }

  private async setWidgetStorage(key: string, value: any): Promise<void> {
    const storageKey = `widget:${this.manifest.id}:${key}`;
    localStorage.setItem(storageKey, JSON.stringify(value));
  }
}
```

---

## Permission System

### Manifest Permissions

```json
{
  "id": "my-social-widget",
  "permissions": [
    "social:read",      // Read feeds, profiles, messages
    "social:write",     // Follow, send messages, etc.
    "social:subscribe", // Subscribe to realtime events
    "storage:read",     // Read widget storage
    "storage:write",    // Write widget storage
    "canvas:read",      // Read canvas data
    "canvas:write"      // Modify canvas (admin widgets only)
  ]
}
```

### Permission Categories

| Permission | Actions Allowed |
|------------|----------------|
| `social:read` | getFeed, getProfile, getMessages, getFollowers |
| `social:write` | follow, unfollow, sendMessage, markRead |
| `social:subscribe` | Subscribe to realtime events |
| `storage:read` | Get widget-scoped storage |
| `storage:write` | Set widget-scoped storage |
| `canvas:read` | Read canvas metadata, widget list |
| `canvas:write` | Add/remove widgets, modify canvas |
| `*` | All permissions (dangerous!) |

### Permission Request Flow

```javascript
// Widget can check if it has permission
async function checkPermission(permission) {
  const result = await WidgetAPI.request('system:checkPermission', { permission });
  return result.granted;
}

// Host grants based on manifest
case 'system:checkPermission':
  return {
    granted: this.manifest.permissions?.includes(data.permission) ?? false,
  };
```

---

## Real-time Event Subscriptions

### Subscribing to Events

```javascript
// Widget requests subscription
await WidgetAPI.request('social:subscribe', {
  events: ['social:message-new', 'social:notification-new'],
});

// Host enables event forwarding
case 'social:subscribe':
  data.events.forEach(eventName => {
    this.subscribedEvents.add(eventName);
  });
  return { subscribed: data.events };
```

### Forwarding Events to Widget

```typescript
// In WidgetHost
private setupEventForwarding() {
  this.eventBus.on('social:*', (event, payload) => {
    if (this.subscribedEvents.has(event)) {
      this.iframe.contentWindow?.postMessage({
        type: 'widget:event',
        payload: { type: event, payload },
      }, '*');
    }
  });
}
```

---

## API Reference

### Feed API

| Action | Data | Returns |
|--------|------|---------|
| `social:getFeed` | `{ type, limit?, offset? }` | `{ activities: Activity[] }` |

### Profile API

| Action | Data | Returns |
|--------|------|---------|
| `social:getProfile` | `{ userId }` | `{ profile: Profile }` |
| `social:searchProfiles` | `{ query, limit? }` | `{ profiles: Profile[] }` |

### Social Graph API

| Action | Data | Returns |
|--------|------|---------|
| `social:follow` | `{ userId }` | `{ success: boolean }` |
| `social:unfollow` | `{ userId }` | `{ success: boolean }` |
| `social:getFollowers` | `{ userId, limit? }` | `{ users: Profile[] }` |
| `social:getFollowing` | `{ userId, limit? }` | `{ users: Profile[] }` |
| `social:checkFollowing` | `{ userId }` | `{ isFollowing: boolean }` |

### Chat API

| Action | Data | Returns |
|--------|------|---------|
| `social:getMessages` | `{ channelId, limit?, before? }` | `{ messages: Message[] }` |
| `social:sendMessage` | `{ channelId, content, replyTo? }` | `{ message: Message }` |
| `social:deleteMessage` | `{ messageId }` | `{ success: boolean }` |

### Notification API

| Action | Data | Returns |
|--------|------|---------|
| `social:getNotifications` | `{ limit? }` | `{ notifications: Notification[] }` |
| `social:markRead` | `{ notificationId }` | `{ success: boolean }` |
| `social:markAllRead` | `{}` | `{ success: boolean }` |

### Storage API

| Action | Data | Returns |
|--------|------|---------|
| `storage:get` | `{ key }` | `{ value: any }` |
| `storage:set` | `{ key, value }` | `{ success: boolean }` |

---

## Error Handling

### Standard Error Responses

```typescript
// Permission denied
{ error: 'Permission denied: social:write' }

// Not authenticated
{ error: 'Authentication required' }

// Invalid action
{ error: 'Unknown action: invalid:action' }

// Service error
{ error: 'Failed to fetch feed: Network error' }

// Validation error
{ error: 'Invalid userId format' }
```

### Widget Error Handling

```javascript
try {
  const result = await WidgetAPI.getFeed('public');
  renderFeed(result.activities);
} catch (err) {
  if (err.message.includes('Permission denied')) {
    showPermissionError();
  } else if (err.message.includes('Authentication required')) {
    showLoginPrompt();
  } else {
    showGenericError(err.message);
  }
}
```

---

## Security Best Practices

1. **Always validate permissions** - Check manifest before routing
2. **Never expose tokens** - Only pass user ID, not session
3. **Scope storage by widget** - `widget:{id}:{key}`
4. **Rate limit requests** - Prevent abuse
5. **Validate all input** - Sanitize data from widgets
6. **Log sensitive actions** - Audit trail for writes
7. **Use allowlist for actions** - Reject unknown actions

---

## Reference Files

| File | Purpose |
|------|---------|
| `src/runtime/WidgetHost.ts` | Request routing and handling |
| `src/runtime/WidgetSandbox.ts` | Iframe sandboxing |
| `src/types/widget.ts` | Widget manifest types |
| `src/services/social/` | Backend services |

---

## Adding New APIs

### Step 1: Define Permission

```typescript
// In permissionMap
'myfeature:getData': 'myfeature:read',
'myfeature:setData': 'myfeature:write',
```

### Step 2: Add Route Handler

```typescript
case 'myfeature:getData':
  return MyService.getData(data.id);

case 'myfeature:setData':
  return MyService.setData(data.id, data.value);
```

### Step 3: Document in Widget

```javascript
// In widget WidgetAPI
async getMyData(id) {
  return this.request('myfeature:getData', { id });
}
```
