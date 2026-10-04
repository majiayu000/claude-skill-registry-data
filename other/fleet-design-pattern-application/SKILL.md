---
name: fleet-design-pattern-application
description: How engineers apply the architect's recommended design patterns in implementation — translating pattern names into code structure, following constraints, and verifying compliance.
---

# Design Pattern Application — Engineer's Pattern Implementation

The architect's design_input specifies patterns. Your job is to APPLY them correctly. "Use adapter pattern for external API calls" isn't vague advice — it's a structural requirement with specific implementation implications.

## From Pattern Name to Code Structure

### Adapter Pattern
**When architect says:** "Use adapter pattern for {external service}"
**What you build:**
```python
# fleet/core/ports.py — interface (inner layer)
class ExternalServicePort:
    async def fetch_data(self, query: str) -> dict: ...

# fleet/infra/external_adapter.py — implementation (outer layer)
class ExternalServiceAdapter(ExternalServicePort):
    def __init__(self, base_url: str, api_key: str):
        self._client = httpx.AsyncClient(base_url=base_url)
        self._api_key = api_key
    
    async def fetch_data(self, query: str) -> dict:
        resp = await self._client.get(f"/api/search", params={"q": query})
        return resp.json()
```
**Key:** Interface in core/. Implementation in infra/. Core never imports infra.

### Repository Pattern
**When architect says:** "Use repository for data access"
**What you build:**
```python
# fleet/core/task_repository.py — interface
class TaskRepository:
    async def get(self, task_id: str) -> Task: ...
    async def list(self, filters: dict) -> list[Task]: ...
    async def save(self, task: Task) -> None: ...

# fleet/infra/mc_task_repository.py — MC-backed implementation
class MCTaskRepository(TaskRepository):
    async def get(self, task_id: str) -> Task:
        return await self._mc.get_task(self._board_id, task_id)
```
**Key:** Business logic uses the repository interface. Swapping MC for a different backend = new repository class, zero core changes.

### Builder Pattern
**When architect says:** "Use builder for {complex object construction}"
**What you build:**
```python
# Like fleet/core/event_chain.py — build_task_complete_chain()
def build_task_complete_chain(task_id, agent, summary, ...):
    chain = EventChain(operation="task_complete")
    chain.add(EventSurface.INTERNAL, "update_task_status", required=True)
    chain.add(EventSurface.PUBLIC, "push_branch", required=False)
    chain.add(EventSurface.CHANNEL, "notify_irc", required=False)
    return chain
```
**Key:** Builder functions construct complex objects step by step. Caller doesn't need to know the internal structure.

### Strategy Pattern
**When architect says:** "Use strategy for {multiple approaches}"
**What you build:**
```python
# Like fleet/core/backend_router.py
def route_task(task, agent, backends):
    for backend in backends:
        if backend.can_handle(task):
            return backend.route(task, agent)
```
**Key:** Multiple strategies behind one interface. The router picks the right one.

## Verifying Your Pattern Application

Before committing, verify:

1. **Does my code match the pattern?** Compare to the architect's design_input — did you follow the structure they specified?
2. **Does it respect domain boundaries?** Use `/fleet-domain-boundary-enforcement` — core doesn't import infra.
3. **Is the responsibility single?** Use the SRP test — can you describe this module without "and"?
4. **Does the architect's fleet precedent match?** Check existing code for how the pattern is used elsewhere in the fleet.

## When the Pattern Doesn't Fit

Sometimes during implementation you discover the architect's recommended pattern doesn't work for your specific case. DON'T silently deviate.

**Instead:**
```
fleet_chat(
    "Design question: arch_design_contribution for task X recommends adapter pattern, "
    "but the external service uses WebSocket (persistent connection), not request-response. "
    "Adapter assumes request-response. Should I use Observer pattern instead?",
    mention="architect"
)
```

The architect revises. You implement the revised pattern. The contribution model handles disagreements through communication, not silence.

## The Fleet's Existing Patterns (Reference)

| Pattern | Where | Why |
|---------|-------|-----|
| Adapter | mc_client, gh_client, ntfy_client, plane_client | Each external service behind stable interface |
| Builder | event_chain.py (build_*_chain functions) | Complex chains built step by step |
| Strategy | backend_router.py | Multiple routing backends |
| Repository | contributions.py (load_synergy_matrix) | Data access abstracted from source |
| Facade | context_assembly.py | Complex multi-source data behind one call |
| Observer | _emit_event pattern in tools.py | Tools emit, systems react |
| Template Method | role_providers.py | Base provider, role-specific overrides |

When the architect says "follow the pattern in mc_client.py," look at mc_client.py. The codebase is the reference implementation.
