---
name: WebSocket & Real-time
description: WebSocket real-time updates, SSE broadcasting, event buffering
version: 3.0.0
author: Family Budget Team
tags: [websocket, sse, realtime, broadcast, events]
dependencies: [api-development]
architecture_refs:
  - $ref: ../../docs/architecture/functionality/realtime.yaml
  - $ref: ../../docs/architecture/endpoints/websocket.yaml
  - $ref: ../../docs/architecture/flows/ws-broadcast.yaml
---

# WebSocket & Real-time Skill

Автоматизация WebSocket real-time updates и SSE broadcasting.

## When to Use

- Добавить WebSocket broadcast к endpoint
- Создать новый WebSocket event type
- Интегрировать frontend WebSocket listener
- Настроить SSE connection

## Architecture Context

**References:**
- Functionality: [$ref](../../docs/architecture/functionality/realtime.yaml)
- Endpoints: [$ref](../../docs/architecture/endpoints/websocket.yaml)
- Flows: [$ref](../../docs/architecture/flows/ws-broadcast.yaml)

**CRITICAL Constraint (Current Implementation):**
- **WORKERS=1 REQUIRED** - `BudgetConnectionManager` is in-memory, NOT shared between workers
- Multi-worker setup breaks WebSocket/SSE (events lost between workers)
- **Reason**: No Redis Pub/Sub implemented yet

**Future Scaling (Redis Pub/Sub)**:
- Implement Redis Pub/Sub for event synchronization between workers
- Workers subscribe to Redis channel, broadcast to local connections
- Allows scaling to multiple workers: WORKERS>1

Reference: `_shared/validation-logic.md#4-single-worker-sse-constraint`

## Commands

### Command: add-ws-broadcast

**Usage:**
```
Добавь WebSocket broadcast для события <event-name> после <operation>.
```

**What It Does:**
1. Add broadcast call to endpoint after operation
2. Add event to event_buffer (for SSE polling)
3. Create frontend handler in budgetWSClient.js
4. Document event in websocket.yaml

**Template Reference:**
- `templates/ws-broadcast.py` - Backend broadcast pattern
- `templates/ws-client.js` - Frontend WebSocket client

**Example:**
```python
# Backend (endpoint)
from backend.app.api.v1.endpoints.budget_sse import event_buffer, ws_manager

# After creating/updating resource
await ws_manager.broadcast(
    "resource_created",
    {"id": resource.id, "name": resource.name}
)
event_buffer.add_event(
    "resource_created",
    {"id": resource.id, "name": resource.name},
    time.time()
)
```

```javascript
// Frontend (budgetWSClient.js)
case 'resource_created':
    this.handleResourceCreated(data);
    break;
```

### Command: create-ws-event

**Usage:**
```
Создай новый WebSocket event type <event-name>.
```

**What It Does:**
1. Define event schema
2. Add backend broadcast logic
3. Add frontend handler
4. Document in websocket.yaml

**Template Reference:**
- `templates/websocket-manager.py` - WebSocket connection manager

## Validation Checklist

- [ ] Broadcast added to endpoint after operation
- [ ] Event added to event_buffer (SSE polling)
- [ ] Frontend handler added to budgetWSClient.js
- [ ] Event documented in websocket.yaml
- [ ] WORKERS=1 enforced in docker-compose.yml
- [ ] WebSocket events reach all clients
- [ ] SSE connection stable

Reference: `_shared/validation-logic.md#4-single-worker-sse-constraint`

## Common Mistakes

**Multi-worker WebSocket:**
- **Symptom**: Events don't reach some clients (user A creates fact, user B doesn't see update)
- **Fix**: Ensure WORKERS=1 in docker-compose.yml OR implement Redis Pub/Sub
- **Reference**: `_shared/validation-logic.md#4`

**Forgot event_buffer.add_event():**
- **Symptom**: SSE polling clients don't receive events
- **Fix**: Add event to both ws_manager AND event_buffer

**Frontend handler not added:**
- **Symptom**: Events received but UI doesn't update
- **Fix**: Add case to budgetWSClient.js switch statement

## Critical Constraint: WORKERS=1

**Why WORKERS=1 is Required:**
- `BudgetConnectionManager` is in-memory (NOT Redis Pub/Sub)
- Each uvicorn worker has separate manager instance
- User A on worker 1 creates transaction → broadcast only reaches worker 1 clients
- User B on worker 2 doesn't receive event → stale UI
- **MUST** run with single worker until Redis Pub/Sub implemented

**docker-compose.yml:**
```yaml
# ✅ CORRECT
services:
  backend:
    command: uvicorn app.main:app --workers 1

# ❌ WRONG - Breaks WebSocket
services:
  backend:
    command: uvicorn app.main:app --workers 4
```

**Scaling Options (Future):**
- Implement Redis Pub/Sub for event synchronization
- Share connection manager state between workers
- Use external message queue (RabbitMQ, Kafka)

## Related Skills

- **api-development**: Add broadcasts to endpoints
- **frontend-development**: Integrate WebSocket in UI

## Quick Links

- WebSocket Architecture: [$ref](../../docs/architecture/functionality/realtime.yaml)
- Broadcast Flow: [$ref](../../docs/architecture/flows/ws-broadcast.yaml)
- Frontend Client: `frontend/web/static/js/budgetWSClient.js`
- Backend Manager: `backend/app/api/v1/endpoints/budget_sse.py`
