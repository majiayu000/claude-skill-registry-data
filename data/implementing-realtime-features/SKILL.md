---
name: implementing-realtime-features
description: Implementing Supabase realtime subscriptions and live updates for StickerNest. Use when the user asks to add realtime, live updates, presence, subscriptions, postgres_changes, broadcast channels, or sync data across tabs/devices. Covers Supabase Realtime, EventBus integration, and subscription lifecycle.
---

# Implementing Realtime Features for StickerNest

This skill covers adding live, real-time functionality using Supabase Realtime, the EventBus, and cross-tab synchronization.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Supabase Realtime                         │
│  ┌─────────────────┐  ┌─────────────────┐                   │
│  │ postgres_changes│  │    broadcast    │                   │
│  │ (persistent)    │  │   (ephemeral)   │                   │
│  └────────┬────────┘  └────────┬────────┘                   │
└───────────┼─────────────────────┼───────────────────────────┘
            │                     │
            ▼                     ▼
┌─────────────────────────────────────────────────────────────┐
│                      Services Layer                          │
│  ChatService │ NotificationService │ BroadcastService        │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   SocialEventBridge                          │
│         (Normalizes events → EventBus)                       │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                       EventBus                               │
│              (social:* events for widgets)                   │
└─────────────────────────┬───────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
    Widgets          Components        TransportManager
                                       (cross-tab sync)
```

---

## Two Types of Realtime

### 1. postgres_changes (Persistent Data)
Use for data stored in database tables.

```typescript
// Subscribe to table changes with filter
const channel = supabaseClient
  .channel('chat-messages')
  .on(
    'postgres_changes',
    {
      event: '*',  // INSERT, UPDATE, DELETE, or *
      schema: 'public',
      table: 'chat_messages',
      filter: `canvas_id=eq.${canvasId}`,
    },
    (payload) => {
      // payload.eventType: 'INSERT' | 'UPDATE' | 'DELETE'
      // payload.new: New row data
      // payload.old: Previous row data (for UPDATE/DELETE)
      handleChange(payload);
    }
  )
  .subscribe((status) => {
    if (status === 'SUBSCRIBED') {
      console.log('Listening for changes');
    }
  });

// Cleanup
channel.unsubscribe();
```

### 2. broadcast (Ephemeral Data)
Use for transient data like cursor positions, typing indicators.

```typescript
// Subscribe to broadcast channel
const channel = supabaseClient
  .channel('canvas-presence')
  .on('broadcast', { event: 'cursor' }, (payload) => {
    updateCursor(payload.payload);
  })
  .on('broadcast', { event: 'typing' }, (payload) => {
    showTypingIndicator(payload.payload);
  })
  .subscribe();

// Send broadcast (no database storage)
channel.send({
  type: 'broadcast',
  event: 'cursor',
  payload: { x: 100, y: 200, userId: 'abc' },
});
```

---

## Service Pattern

### Creating a Realtime Service

```typescript
// src/services/social/MyRealtimeService.ts

import { getSupabaseClient } from '@/contexts/AuthContext';
import { RealtimeChannel, RealtimePostgresChangesPayload } from '@supabase/supabase-js';

interface MyDataRow {
  id: string;
  user_id: string;
  content: string;
  created_at: string;
}

type ChangeCallback = (payload: RealtimePostgresChangesPayload<MyDataRow>) => void;

class MyRealtimeServiceClass {
  private channels: Map<string, RealtimeChannel> = new Map();
  private callbacks: Map<string, Set<ChangeCallback>> = new Map();

  /**
   * Subscribe to changes for a specific scope (e.g., canvasId)
   */
  subscribe(scopeId: string, callback: ChangeCallback): () => void {
    const supabase = getSupabaseClient();
    if (!supabase) {
      console.warn('Supabase not available');
      return () => {};
    }

    // Track callback
    if (!this.callbacks.has(scopeId)) {
      this.callbacks.set(scopeId, new Set());
    }
    this.callbacks.get(scopeId)!.add(callback);

    // Create channel if not exists
    if (!this.channels.has(scopeId)) {
      const channel = supabase
        .channel(`my-data:${scopeId}`)
        .on(
          'postgres_changes',
          {
            event: '*',
            schema: 'public',
            table: 'my_table',
            filter: `scope_id=eq.${scopeId}`,
          },
          (payload) => {
            // Notify all callbacks for this scope
            this.callbacks.get(scopeId)?.forEach((cb) => {
              try {
                cb(payload as RealtimePostgresChangesPayload<MyDataRow>);
              } catch (err) {
                console.error('Callback error:', err);
              }
            });
          }
        )
        .subscribe((status, err) => {
          if (status === 'SUBSCRIBED') {
            console.log(`Subscribed to my-data:${scopeId}`);
          } else if (status === 'CHANNEL_ERROR') {
            console.error(`Subscription error:`, err);
          }
        });

      this.channels.set(scopeId, channel);
    }

    // Return unsubscribe function
    return () => {
      const callbacks = this.callbacks.get(scopeId);
      if (callbacks) {
        callbacks.delete(callback);

        // If no more callbacks, clean up channel
        if (callbacks.size === 0) {
          this.channels.get(scopeId)?.unsubscribe();
          this.channels.delete(scopeId);
          this.callbacks.delete(scopeId);
        }
      }
    };
  }

  /**
   * Clean up all subscriptions
   */
  cleanup(): void {
    this.channels.forEach((channel) => channel.unsubscribe());
    this.channels.clear();
    this.callbacks.clear();
  }
}

export const MyRealtimeService = new MyRealtimeServiceClass();
```

---

## EventBus Integration

### Emitting Realtime Events to EventBus

```typescript
// In SocialEventBridge or service

import { EventBus } from '@/runtime/EventBus';

function setupRealtimeToEventBus(eventBus: EventBus) {
  // Subscribe to service
  ChatService.subscribeToMessages(canvasId, (payload) => {
    if (payload.eventType === 'INSERT') {
      eventBus.emit('social:message-new', {
        message: payload.new,
        canvasId,
      });
    } else if (payload.eventType === 'DELETE') {
      eventBus.emit('social:message-deleted', {
        messageId: payload.old.id,
        canvasId,
      });
    }
  });
}
```

### Standard Social Event Names

| Event | Payload | When |
|-------|---------|------|
| `social:message-new` | `{ message, canvasId }` | New chat message |
| `social:message-deleted` | `{ messageId, canvasId }` | Message deleted |
| `social:notification-new` | `{ notification }` | New notification |
| `social:notification-read` | `{ notificationId }` | Notification marked read |
| `social:presence-update` | `{ userId, status, cursor }` | User presence changed |
| `social:typing-start` | `{ userId, canvasId }` | User started typing |
| `social:typing-stop` | `{ userId, canvasId }` | User stopped typing |
| `social:feed-update` | `{ activity }` | New activity in feed |
| `social:follow-new` | `{ followerId, followingId }` | New follow |

---

## Presence Management

### Using PresenceManager

```typescript
import { PresenceManager } from '@/runtime/PresenceManager';

// Initialize (usually in App.tsx)
PresenceManager.initialize(eventBus, transportManager, {
  heartbeatInterval: 5000,
  staleTimeout: 30000,
  cursorThrottle: 50,
});

// Update cursor position
PresenceManager.updateCursor(x, y);

// Update selection
PresenceManager.updateSelection(selectedWidgetIds);

// Get all present users
const users = PresenceManager.getPresenceMap();

// Subscribe to presence changes
PresenceManager.subscribe((presenceMap) => {
  // Update UI with new presence data
});

// Cleanup
PresenceManager.shutdown();
```

### Custom Presence Data

```typescript
// Extend presence with custom data
PresenceManager.updateCustomData({
  currentTool: 'select',
  viewportBounds: { x: 0, y: 0, width: 1920, height: 1080 },
});
```

---

## Cross-Tab Synchronization

### How It Works

```
Tab A emits event
    ↓
TransportManager.handleLocalEvent()
    ↓
Routes based on syncPolicy:
  - BroadcastChannelTransport (same browser)
  - SharedWorkerTransport (shared state)
  - WebSocketTransport (cross-device)
    ↓
Tab B receives via transport
    ↓
RuntimeMessageDispatcher.dispatch()
    ↓
EventBus.emitFromRemote() with loop guard
    ↓
Local handlers fire
```

### Event Metadata for Sync

```typescript
// Events include metadata to prevent loops
eventBus.emit('social:message-new', payload, {
  originTabId: 'tab-123',
  originDeviceId: 'device-abc',
  hopCount: 0,
  seenBy: ['tab-123'],
});

// Loop guard checks
if (metadata.seenBy.includes(currentTabId)) {
  return; // Already processed
}
if (metadata.hopCount > 10) {
  return; // Too many hops
}
```

---

## Subscription Lifecycle

### Setup Pattern

```typescript
// In React component
useEffect(() => {
  const unsubscribes: Array<() => void> = [];

  // Subscribe to multiple services
  unsubscribes.push(
    ChatService.subscribeToMessages(canvasId, handleMessage)
  );
  unsubscribes.push(
    NotificationService.subscribeToNotifications(handleNotification)
  );
  unsubscribes.push(
    BroadcastService.subscribeToCanvas(canvasId, handleBroadcast)
  );

  // Cleanup all on unmount
  return () => {
    unsubscribes.forEach((unsub) => unsub());
  };
}, [canvasId]);
```

### In Zustand Stores

```typescript
// Store with subscription management
export const useMyStore = create<MyState & MyActions>()((set, get) => ({
  items: [],
  _unsubscribe: null as (() => void) | null,

  subscribe: () => {
    // Clean up existing subscription
    get()._unsubscribe?.();

    const unsubscribe = MyService.subscribe((payload) => {
      if (payload.eventType === 'INSERT') {
        set((state) => ({
          items: [...state.items, payload.new],
        }));
      }
    });

    set({ _unsubscribe: unsubscribe });
    return unsubscribe;
  },

  unsubscribe: () => {
    get()._unsubscribe?.();
    set({ _unsubscribe: null });
  },
}));
```

---

## Optimistic Updates

### Pattern for Instant UI Feedback

```typescript
async function sendMessage(content: string) {
  const tempId = `temp-${Date.now()}`;

  // 1. Optimistic update (instant)
  addMessage({
    id: tempId,
    content,
    status: 'sending',
  });

  try {
    // 2. Send to server
    const result = await ChatService.sendMessage(canvasId, content);

    // 3. Replace temp with real (realtime will also fire)
    replaceMessage(tempId, {
      ...result,
      status: 'sent',
    });
  } catch (err) {
    // 4. Mark as failed
    updateMessage(tempId, { status: 'failed' });
  }
}
```

---

## Debouncing Broadcasts

### For High-Frequency Events

```typescript
// BroadcastService pattern
private cursorDebounceTimer: ReturnType<typeof setTimeout> | null = null;
private pendingCursor: { x: number; y: number } | null = null;

broadcastCursor(x: number, y: number): void {
  this.pendingCursor = { x, y };

  if (!this.cursorDebounceTimer) {
    this.cursorDebounceTimer = setTimeout(() => {
      if (this.pendingCursor) {
        this.channel?.send({
          type: 'broadcast',
          event: 'cursor',
          payload: this.pendingCursor,
        });
        this.pendingCursor = null;
      }
      this.cursorDebounceTimer = null;
    }, 16); // ~60fps
  }
}
```

---

## Error Handling

### Reconnection Strategy

```typescript
const channel = supabase
  .channel('my-channel')
  .on('postgres_changes', {...}, handler)
  .subscribe((status, err) => {
    switch (status) {
      case 'SUBSCRIBED':
        console.log('Connected');
        break;
      case 'CHANNEL_ERROR':
        console.error('Channel error:', err);
        // Supabase auto-reconnects, but you can add custom logic
        break;
      case 'TIMED_OUT':
        console.warn('Subscription timed out');
        break;
      case 'CLOSED':
        console.log('Channel closed');
        break;
    }
  });
```

---

## Reference Files

| File | Purpose |
|------|---------|
| `src/services/social/ChatService.ts` | Chat realtime subscriptions |
| `src/services/social/NotificationService.ts` | Notification subscriptions |
| `src/services/social/BroadcastService.ts` | Ephemeral broadcast channels |
| `src/runtime/PresenceManager.ts` | Presence and cursor sync |
| `src/runtime/SocialEventBridge.ts` | Bridge to EventBus |
| `src/runtime/TransportManager.ts` | Cross-tab/device sync |

---

## Best Practices

1. **Always return unsubscribe functions** - Prevent memory leaks
2. **Use postgres_changes for persistent data** - Messages, notifications
3. **Use broadcast for ephemeral data** - Cursors, typing indicators
4. **Debounce high-frequency events** - Cursor updates, widget state
5. **Include scope filters** - `filter: 'canvas_id=eq.xyz'`
6. **Handle all subscription states** - SUBSCRIBED, ERROR, TIMEOUT
7. **Clean up on component unmount** - Call unsubscribe in useEffect cleanup
8. **Use EventBus for widget communication** - Standard event names
