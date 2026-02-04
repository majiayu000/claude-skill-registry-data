---
name: building-social-widgets
description: Building social widgets for StickerNest's default social experience. Use when the user asks to create feed widgets, chat widgets, notification widgets, profile widgets, friends list, or any social UI that plugs into the social layer. Covers widget-based social UI, Protocol integration, and theming.
---

# Building Social Widgets for StickerNest

This skill covers creating the default social widget set that provides the built-in social experience. All social UI is widget-based, making it customizable and replaceable.

## Philosophy

> "The built-in social experience is just a pre-installed widget set using the same Protocol as any custom widget."

- Default widgets prove the API works
- Users can replace/augment with custom widgets
- Everything is themeable via CSS variables
- Widgets connect to public and friends-only feeds

---

## Default Social Widget Set

| Widget ID | Purpose | Feed Type |
|-----------|---------|-----------|
| `social-feed-public` | Global activity feed | Public |
| `social-feed-friends` | Friends-only activity feed | Friends |
| `social-chat` | Canvas chat room | Canvas-scoped |
| `social-notifications` | Notification center | User-scoped |
| `social-profile-card` | User profile display | Per-user |
| `social-friends-list` | Online friends list | User-scoped |
| `social-who-online` | Canvas presence | Canvas-scoped |
| `social-dm-inbox` | Direct messages | User-scoped |

---

## Widget Manifest Template (Social)

```json
{
  "id": "social-feed-public",
  "name": "Public Feed",
  "version": "1.0.0",
  "description": "Shows public activity from all users",
  "kind": "2d",
  "entry": "index.html",
  "category": "social",
  "tags": ["social", "feed", "activity"],
  "author": "StickerNest",
  "capabilities": {
    "draggable": true,
    "resizable": true,
    "rotatable": false
  },
  "defaultSize": {
    "width": 320,
    "height": 480
  },
  "permissions": [
    "social:read",
    "social:subscribe"
  ],
  "inputs": {
    "feedType": {
      "type": "string",
      "description": "Feed type: 'public' or 'friends'",
      "default": "public"
    },
    "limit": {
      "type": "number",
      "description": "Number of items to show",
      "default": 20
    }
  },
  "outputs": {
    "activitySelected": {
      "type": "object",
      "description": "When user clicks an activity"
    }
  }
}
```

---

## Social Widget HTML Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Social Feed</title>
  <style>
    /* Theme tokens - inherited from host */
    :root {
      --social-bg: var(--widget-bg, #1a1a2e);
      --social-text: var(--widget-text, #eee);
      --social-text-muted: var(--widget-text-muted, #888);
      --social-border: var(--widget-border, #333);
      --social-accent: var(--widget-accent, #6366f1);
      --social-item-bg: var(--widget-item-bg, #252542);
      --social-item-hover: var(--widget-item-hover, #2d2d4a);
      --social-avatar-size: 40px;
      --social-spacing: 12px;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: system-ui, -apple-system, sans-serif;
      background: var(--social-bg);
      color: var(--social-text);
      height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }

    .header {
      padding: var(--social-spacing);
      border-bottom: 1px solid var(--social-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .header h2 {
      font-size: 14px;
      font-weight: 600;
    }

    .feed {
      flex: 1;
      overflow-y: auto;
      padding: var(--social-spacing);
    }

    .feed-item {
      display: flex;
      gap: var(--social-spacing);
      padding: var(--social-spacing);
      background: var(--social-item-bg);
      border-radius: 8px;
      margin-bottom: 8px;
      cursor: pointer;
      transition: background 0.15s;
    }

    .feed-item:hover {
      background: var(--social-item-hover);
    }

    .avatar {
      width: var(--social-avatar-size);
      height: var(--social-avatar-size);
      border-radius: 50%;
      background: var(--social-accent);
      flex-shrink: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: bold;
      font-size: 14px;
    }

    .avatar img {
      width: 100%;
      height: 100%;
      border-radius: 50%;
      object-fit: cover;
    }

    .content {
      flex: 1;
      min-width: 0;
    }

    .username {
      font-weight: 600;
      font-size: 13px;
    }

    .action {
      font-size: 13px;
      color: var(--social-text-muted);
    }

    .action .verb {
      color: var(--social-accent);
    }

    .timestamp {
      font-size: 11px;
      color: var(--social-text-muted);
      margin-top: 4px;
    }

    .empty-state {
      text-align: center;
      padding: 40px 20px;
      color: var(--social-text-muted);
    }

    .loading {
      text-align: center;
      padding: 20px;
      color: var(--social-text-muted);
    }
  </style>
</head>
<body>
  <div class="header">
    <h2 id="title">Public Feed</h2>
    <button id="refresh" style="background: none; border: none; color: var(--social-accent); cursor: pointer;">
      Refresh
    </button>
  </div>

  <div class="feed" id="feed">
    <div class="loading">Loading...</div>
  </div>

  <script>
    // Widget Protocol v3.0 implementation
    const WidgetAPI = {
      ready: false,
      instanceId: null,
      config: {},

      init() {
        window.addEventListener('message', this.handleMessage.bind(this));
        this.send('widget:ready');
      },

      send(type, payload = {}) {
        window.parent.postMessage({ type, payload }, '*');
      },

      handleMessage(event) {
        const { type, payload } = event.data || {};

        switch (type) {
          case 'widget:init':
            this.instanceId = payload.instanceId;
            this.config = payload.config || {};
            this.ready = true;
            this.onReady();
            break;

          case 'widget:event':
            this.onEvent(payload.type, payload.payload);
            break;

          case 'widget:theme':
            this.applyTheme(payload);
            break;
        }
      },

      onReady() {
        // Override in widget
      },

      onEvent(eventType, payload) {
        // Override in widget
      },

      emit(outputName, data) {
        this.send('widget:emit', { type: outputName, payload: data });
      },

      request(action, data) {
        return new Promise((resolve) => {
          const requestId = Date.now().toString();
          const handler = (event) => {
            if (event.data?.type === 'widget:response' &&
                event.data?.payload?.requestId === requestId) {
              window.removeEventListener('message', handler);
              resolve(event.data.payload.result);
            }
          };
          window.addEventListener('message', handler);
          this.send('widget:request', { action, data, requestId });
        });
      },

      applyTheme(tokens) {
        const root = document.documentElement;
        Object.entries(tokens).forEach(([key, value]) => {
          root.style.setProperty(`--${key}`, value);
        });
      },

      // Social-specific helpers
      async getFeed(type = 'public', limit = 20) {
        return this.request('social:getFeed', { type, limit });
      },

      async follow(userId) {
        return this.request('social:follow', { userId });
      },

      async unfollow(userId) {
        return this.request('social:unfollow', { userId });
      },

      subscribeTo(eventName, callback) {
        this._eventHandlers = this._eventHandlers || {};
        this._eventHandlers[eventName] = callback;
      }
    };

    // Feed Widget Implementation
    class FeedWidget {
      constructor() {
        this.feedEl = document.getElementById('feed');
        this.titleEl = document.getElementById('title');
        this.refreshBtn = document.getElementById('refresh');
        this.feedType = 'public';
        this.activities = [];

        this.refreshBtn.addEventListener('click', () => this.loadFeed());
      }

      async init(config) {
        this.feedType = config.feedType || 'public';
        this.titleEl.textContent = this.feedType === 'friends'
          ? 'Friends Feed'
          : 'Public Feed';

        await this.loadFeed();

        // Subscribe to live updates
        WidgetAPI.subscribeTo('social:feed-update', (activity) => {
          this.addActivity(activity, true);
        });
      }

      async loadFeed() {
        this.feedEl.innerHTML = '<div class="loading">Loading...</div>';

        try {
          const result = await WidgetAPI.getFeed(this.feedType, 20);
          this.activities = result.activities || [];
          this.render();
        } catch (err) {
          this.feedEl.innerHTML = `
            <div class="empty-state">
              Failed to load feed. <a href="#" onclick="feedWidget.loadFeed()">Retry</a>
            </div>
          `;
        }
      }

      addActivity(activity, prepend = false) {
        if (prepend) {
          this.activities.unshift(activity);
        } else {
          this.activities.push(activity);
        }
        this.render();
      }

      render() {
        if (this.activities.length === 0) {
          this.feedEl.innerHTML = `
            <div class="empty-state">
              No activities yet.<br>
              Follow some users to see their updates!
            </div>
          `;
          return;
        }

        this.feedEl.innerHTML = this.activities.map(activity => `
          <div class="feed-item" data-id="${activity.id}">
            <div class="avatar">
              ${activity.actor?.avatar_url
                ? `<img src="${activity.actor.avatar_url}" alt="">`
                : activity.actor?.display_name?.[0] || '?'}
            </div>
            <div class="content">
              <div class="action">
                <span class="username">${activity.actor?.display_name || 'Unknown'}</span>
                <span class="verb">${this.formatVerb(activity.verb)}</span>
                ${activity.metadata?.title || activity.object_type}
              </div>
              <div class="timestamp">${this.formatTime(activity.created_at)}</div>
            </div>
          </div>
        `).join('');

        // Add click handlers
        this.feedEl.querySelectorAll('.feed-item').forEach(item => {
          item.addEventListener('click', () => {
            const id = item.dataset.id;
            const activity = this.activities.find(a => a.id === id);
            if (activity) {
              WidgetAPI.emit('activitySelected', activity);
            }
          });
        });
      }

      formatVerb(verb) {
        const verbs = {
          published: 'published',
          forked: 'forked',
          liked: 'liked',
          commented: 'commented on',
          followed: 'followed',
        };
        return verbs[verb] || verb;
      }

      formatTime(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;

        if (diff < 60000) return 'just now';
        if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
        if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
        return date.toLocaleDateString();
      }
    }

    // Initialize
    const feedWidget = new FeedWidget();

    WidgetAPI.onReady = () => {
      feedWidget.init(WidgetAPI.config);
    };

    WidgetAPI.onEvent = (type, payload) => {
      if (WidgetAPI._eventHandlers?.[type]) {
        WidgetAPI._eventHandlers[type](payload);
      }
    };

    WidgetAPI.init();
  </script>
</body>
</html>
```

---

## Social Protocol Messages

### Widget → Host Requests

| Action | Payload | Response |
|--------|---------|----------|
| `social:getFeed` | `{ type, limit, offset }` | `{ activities: [...] }` |
| `social:getProfile` | `{ userId }` | `{ profile: {...} }` |
| `social:follow` | `{ userId }` | `{ success: boolean }` |
| `social:unfollow` | `{ userId }` | `{ success: boolean }` |
| `social:sendMessage` | `{ channelId, content }` | `{ message: {...} }` |
| `social:getMessages` | `{ channelId, limit }` | `{ messages: [...] }` |
| `social:getNotifications` | `{ limit }` | `{ notifications: [...] }` |
| `social:markRead` | `{ notificationId }` | `{ success: boolean }` |
| `social:getOnlineUsers` | `{ canvasId }` | `{ users: [...] }` |

### Host → Widget Events

| Event | Payload | When |
|-------|---------|------|
| `social:feed-update` | `{ activity }` | New activity posted |
| `social:message-new` | `{ message }` | New chat message |
| `social:notification-new` | `{ notification }` | New notification |
| `social:presence-update` | `{ userId, status }` | User online/offline |
| `social:typing` | `{ userId, isTyping }` | Typing indicator |

---

## Chat Widget Example

```html
<!-- Simplified for brevity -->
<script>
class ChatWidget {
  constructor() {
    this.messages = [];
    this.channelId = null;
  }

  async init(config) {
    this.channelId = config.channelId || 'global';
    await this.loadMessages();

    // Subscribe to new messages
    WidgetAPI.subscribeTo('social:message-new', (msg) => {
      if (msg.channelId === this.channelId) {
        this.addMessage(msg);
      }
    });

    // Subscribe to typing indicators
    WidgetAPI.subscribeTo('social:typing', (data) => {
      this.showTypingIndicator(data.userId, data.isTyping);
    });
  }

  async sendMessage(content) {
    const result = await WidgetAPI.request('social:sendMessage', {
      channelId: this.channelId,
      content,
    });
    // Optimistic update already handled, realtime confirms
  }

  // ... render methods
}
</script>
```

---

## Notification Widget Example

```javascript
class NotificationWidget {
  async init() {
    await this.loadNotifications();

    WidgetAPI.subscribeTo('social:notification-new', (notif) => {
      this.addNotification(notif, true);
      this.playSound();
      this.showBadge();
    });
  }

  async markAsRead(notificationId) {
    await WidgetAPI.request('social:markRead', { notificationId });
    this.updateNotification(notificationId, { read: true });
  }

  async markAllRead() {
    await WidgetAPI.request('social:markAllRead', {});
    this.notifications.forEach(n => n.read = true);
    this.render();
  }
}
```

---

## Theming Social Widgets

### Required CSS Variables

```css
/* Base widget tokens (inherited from canvas theme) */
--widget-bg
--widget-text
--widget-text-muted
--widget-border
--widget-accent
--widget-item-bg
--widget-item-hover

/* Social-specific tokens */
--social-avatar-size: 40px;
--social-avatar-border: 2px solid var(--widget-accent);
--social-online-color: #22c55e;
--social-offline-color: #6b7280;
--social-unread-bg: rgba(99, 102, 241, 0.1);
--social-typing-color: var(--widget-text-muted);
--social-chat-bubble-self: var(--widget-accent);
--social-chat-bubble-other: var(--widget-item-bg);
```

### Theme Inheritance

```javascript
// Host sends theme tokens on init and updates
WidgetAPI.applyTheme({
  'widget-bg': '#1a1a2e',
  'widget-text': '#ffffff',
  'widget-accent': '#6366f1',
  // ...
});
```

---

## Widget Set Registration

```typescript
// src/widgets/builtin/social/index.ts

export const socialWidgetSet = {
  id: 'social-default',
  name: 'StickerNest Social',
  description: 'Default social widgets for feeds, chat, and notifications',
  widgets: [
    {
      id: 'social-feed-public',
      path: '/widgets/social/feed-public/',
    },
    {
      id: 'social-feed-friends',
      path: '/widgets/social/feed-friends/',
    },
    {
      id: 'social-chat',
      path: '/widgets/social/chat/',
    },
    {
      id: 'social-notifications',
      path: '/widgets/social/notifications/',
    },
    {
      id: 'social-profile-card',
      path: '/widgets/social/profile-card/',
    },
    {
      id: 'social-friends-list',
      path: '/widgets/social/friends-list/',
    },
    {
      id: 'social-who-online',
      path: '/widgets/social/who-online/',
    },
    {
      id: 'social-dm-inbox',
      path: '/widgets/social/dm-inbox/',
    },
  ],
};
```

---

## Testing Social Widgets

```typescript
// tests/social-widgets.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Social Feed Widget', () => {
  test('loads public feed', async ({ page }) => {
    await page.goto('/canvas/test');

    // Add feed widget
    await page.click('[data-widget="social-feed-public"]');

    // Wait for feed to load
    await expect(page.locator('.feed-item')).toBeVisible();
  });

  test('receives realtime updates', async ({ page }) => {
    // Setup feed widget
    await page.goto('/canvas/test');

    // Post activity from another context
    await postTestActivity();

    // Verify feed updates
    await expect(page.locator('.feed-item').first())
      .toContainText('published');
  });
});
```

---

## Reference Files

| File | Purpose |
|------|---------|
| `public/test-widgets/activity-feed/` | Existing feed widget |
| `public/test-widgets/chat-room/` | Existing chat widget |
| `public/test-widgets/notification-center/` | Existing notification widget |
| `src/widgets/builtin/social/` | Built-in social widgets |
| `src/runtime/WidgetHost.ts` | Widget sandbox host |
| `src/services/social/` | Social backend services |

---

## Best Practices

1. **Always use Protocol requests** - Never call services directly
2. **Subscribe to realtime events** - Keep UI in sync
3. **Theme with CSS variables** - Inherit from host theme
4. **Handle empty states** - Show helpful messages
5. **Optimistic updates** - Instant feedback before server confirms
6. **Accessible markup** - Proper ARIA labels, keyboard nav
7. **Mobile-friendly** - Touch targets, responsive layout
8. **Error boundaries** - Graceful degradation on failures
