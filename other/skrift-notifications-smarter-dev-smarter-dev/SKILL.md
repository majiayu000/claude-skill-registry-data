---
name: skrift-notifications
description: "Skrift real-time notification system — SSE delivery, pluggable backends (InMemory, Redis, PgNotify), group keys, and dismiss patterns."
---

# Skrift Notifications

Real-time notification system delivered via Server-Sent Events (SSE). Notifications appear as toast popups and persist until dismissed.

## Delivery Scopes

```python
from skrift.lib.notifications import notify_session, notify_user, notify_broadcast, _ensure_nid

# Session-scoped — stored, replayed on reconnect
nid = _ensure_nid(request)
await notify_session(nid, "generic", title="Saved", message="Your draft was saved.")

# User-scoped — stored, delivered to all sessions of a user
await notify_user(str(user.id), "generic", title="New reply", message="Someone replied.")

# Broadcast — ephemeral, not stored, all active connections
await notify_broadcast("new_tweet", tweet_id="...", content_html="...")
```

| Function | Stored? | Target | Use case |
|----------|---------|--------|----------|
| `await notify_session(nid, type, *, group=None, **payload)` | Yes | Single session | Transient feedback (saves, errors) |
| `await notify_user(user_id, type, *, group=None, **payload)` | Yes | All sessions of user | Cross-device (replies, likes) |
| `await notify_broadcast(type, *, group=None, **payload)` | No | All connections | Feed updates (new posts) |

Stored notifications replay on reconnect. Broadcast notifications are ephemeral.

## Group Key — Replace-in-Place

All three functions accept an optional `group` keyword. A new notification with the same group key automatically dismisses the previous one:

```python
# Progress updates — each replaces the previous toast
nid = _ensure_nid(request)
await notify_session(nid, "generic", group="deploy", title="Deploying…", message="Step 1/3")
await notify_session(nid, "generic", group="deploy", title="Deploying…", message="Step 2/3")
await notify_session(nid, "generic", group="deploy", title="Deployed!", message="Done")

# User-scoped status update
await notify_user(str(user.id), "generic", group="upload-status", title="Uploading…", message="50%")
await notify_user(str(user.id), "generic", group="upload-status", title="Upload complete", message="100%")

# Broadcast
await notify_broadcast("generic", group="maintenance", title="Maintenance", message="Starting soon…")
```

## Dismissing by Group Key (Backend)

```python
from skrift.lib.notifications import dismiss_session_group, dismiss_user_group

# Dismiss the active "deploy" notification without knowing its UUID
await dismiss_session_group(nid, "deploy")

# Dismiss from a user's queue (pushes dismissed event to all their sessions)
await dismiss_user_group(str(user.id), "upload-status")
```

## Notification Types

- `"generic"` — rendered as a toast with `title` + `message` (built-in UI)
- `"dismissed"` — internal, triggers client-side removal
- Custom types — dispatched via `sk:notification` CustomEvent for app-specific handling

## Controller Pattern — Notify on Action

```python
from skrift.lib.notifications import notify_user

@post("/{item_id:uuid}/comment", guards=[auth_guard])
async def comment(self, request: Request, db_session: AsyncSession, item_id: UUID) -> Redirect:
    user = await self._get_user(request, db_session)
    comment = await comment_service.create(db_session, user.id, item_id, form.data.content)

    item = await item_service.get_by_id(db_session, item_id)
    if item and str(item.user_id) != str(user.id):
        await notify_user(
            str(item.user_id),
            "generic",
            title=f"{user.name} commented on your post",
            message=form.data.content[:100],
        )

    return Redirect(path=f"/items/{item_id}")
```

## Backend Architecture

The notification service uses a pluggable backend system for storage and cross-replica fanout.

### Backend Protocol

```python
class NotificationBackend(Protocol):
    async def start(self) -> None: ...
    async def stop(self) -> None: ...
    async def store(self, scope: str, scope_id: str, notification: Notification) -> None: ...
    async def remove(self, notification_id: UUID) -> None: ...
    async def remove_by_group(self, scope: str, scope_id: str, group: str) -> UUID | None: ...
    async def get_queued(self, scope: str, scope_id: str) -> list[Notification]: ...
    async def publish(self, message: dict) -> None: ...
    def on_remote_message(self, callback: Callable[[dict], Any]) -> None: ...
```

### InMemoryBackend (default)

Dict-based storage, no cross-replica fanout. Suitable for single-process deployments.

- No configuration needed — used automatically when `notifications.backend` is unset
- Notifications stored in Python dicts, lost on restart

### RedisBackend

Database storage + Redis pub/sub for cross-replica fanout.

- Notifications persisted in `stored_notifications` table
- Pub/sub via a Redis channel for real-time fanout across replicas
- Requires `skrift[redis]` extra (`pip install 'skrift[redis]'`)

### PgNotifyBackend

Database storage + PostgreSQL `LISTEN`/`NOTIFY` for cross-replica fanout.

- Notifications persisted in `stored_notifications` table
- Uses PostgreSQL's native `LISTEN`/`NOTIFY` — no extra infrastructure
- Automatic reconnect with exponential backoff
- Requires `asyncpg` (already a Skrift dependency)

### `_DatabaseStorageMixin`

Shared by `RedisBackend` and `PgNotifyBackend`. Provides:
- DB-backed `store()`, `remove()`, `remove_by_group()`, `get_queued()`
- Background cleanup task: deletes notifications older than 24 hours (runs every 10 minutes)

## Backend Configuration

Configure in `app.yaml`:

```yaml
# InMemory (default — no config needed)
# notifications:
#   backend: ""

# Redis
redis:
  url: $REDIS_URL
  prefix: "myapp"        # optional key prefix

notifications:
  backend: "skrift.lib.notification_backends:RedisBackend"

# PgNotify (uses existing db.url)
notifications:
  backend: "skrift.lib.notification_backends:PgNotifyBackend"
```

Config classes in `skrift/config.py`:

```python
class RedisConfig(BaseModel):
    url: str = ""
    prefix: str = ""  # e.g. "myapp" → keys like "myapp:skrift:notifications"

class NotificationsConfig(BaseModel):
    backend: str = ""  # empty = InMemoryBackend; or "module:ClassName"
```

Backend is instantiated in `skrift/asgi.py` during app creation and started/stopped via ASGI lifespan hooks.

## StoredNotification Model

Used by `RedisBackend` and `PgNotifyBackend` for persistent storage:

```python
class StoredNotification(Base):
    __tablename__ = "stored_notifications"

    scope: Mapped[str]          # "session" or "user"
    scope_id: Mapped[str]       # nid or user_id
    type: Mapped[str]           # notification type
    payload_json: Mapped[str]   # JSON-encoded payload
    group_key: Mapped[str | None]
    notified_at: Mapped[datetime]
```

Indexes: `(scope, scope_id)`, `(scope, scope_id, group_key)`, `(notified_at)`.

Cleanup: rows older than 24 hours are deleted automatically by the backend's cleanup loop.

## SSE Protocol (Three-Phase)

1. **Flush**: Server sends all queued notifications for the session/user
2. **Sync**: Server sends `event: sync` — client reconciles (removes dismissed-elsewhere items)
3. **Live**: Server pushes new notifications as they arrive; 30s keepalive comments prevent proxy timeouts

During the Live phase, group-based replacement sends a `"dismissed"` event for the old notification followed by the new one.

## Client Behavior

- Auto-connects on page load and `window.focus`, disconnects on `window.blur`
- Reconnects after 5s on error
- Deduplicates via `_displayedIds` Set
- Max visible toasts: 3 (desktop) / 2 (mobile); excess queued
- Dispatches `sk:notification` CustomEvent (cancelable) for every notification
- Only renders `"generic"` type as toast; custom types handled via event listeners
- Global instance: `window.__skriftNotifications` (exposes `.status` getter)

### Custom Event Handling (Client-Side)

```javascript
document.addEventListener('sk:notification', (e) => {
    const data = e.detail;  // { type, id, ...payload }
    if (data.type === 'my_custom_type') {
        // Handle custom notification — build your own UI
        e.preventDefault();  // Prevents default generic toast
    }
});
```

### Connection Status Events

```javascript
document.addEventListener('sk:notification-status', (e) => {
    console.log(e.detail.status); // "connecting" | "connected" | "disconnected" | "reconnecting"
});
```

## Dismiss Flow

1. User clicks dismiss → client adds `.sk-notification-exit` (slide-out animation)
2. Client sends `DELETE /notifications/{id}`
3. Server removes from queues, broadcasts `"dismissed"` event to user's other sessions
4. Other sessions remove the toast via `_removeDismissed()`

Backend dismiss by group: `dismiss_session_group(nid, group)` and `dismiss_user_group(user_id, group)`.

## Hook Integration

Two hook constants defined in `skrift/lib/hooks.py`:
- `NOTIFICATION_SENT` — action fired after a notification is sent
- `NOTIFICATION_DISMISSED` — action fired after a notification is dismissed

## Key Files

| File | Purpose |
|------|---------|
| `skrift/lib/notifications.py` | `NotificationService` singleton, convenience functions |
| `skrift/lib/notification_backends.py` | `InMemoryBackend`, `RedisBackend`, `PgNotifyBackend` |
| `skrift/db/models/notification.py` | `StoredNotification` model |
| `skrift/controllers/notifications.py` | SSE stream + dismiss HTTP endpoints |
| `skrift/static/js/notifications.js` | `SkriftNotifications` client class |
| `skrift/static/css/skrift.css` | `.sk-notification*` toast styles |
| `skrift/config.py` | `RedisConfig`, `NotificationsConfig` classes |

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/notifications/stream` | SSE stream (auto-connected by `notifications.js`) |
| `DELETE` | `/notifications/{id}` | Dismiss by notification UUID |
| `DELETE` | `/notifications/group/{group}` | Dismiss by group key |
