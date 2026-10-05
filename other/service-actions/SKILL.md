---
name: ha:service-actions
description: "Service action handling — services.py registered in async_setup, strict voluptuous schemas, entity/device/area targeting, ServiceValidationError vs HomeAssistantError, response data, entity services, coordinator/time-interval scheduling. Use when writing services.py, service handlers, or periodic work."
effort: medium
user-invocable: false
paths:
  - "**/services.py"
  - "**/components/*/services.py"
  - "**/custom_components/*/services.py"
  - "**/test_services.py"
---

# Service Actions & Scheduling Reference

Quick reference for Home Assistant service action (Python) patterns.

## Service Kind Detection

**Before applying patterns, decide what kind of action you are adding:**

```bash
grep -rn "async_register" homeassistant/components/<domain>/services.py
grep -rn "async_register_entity_service" homeassistant/components/<domain>/*.py
grep -rn "SupportsResponse" homeassistant/components/<domain>/services.py
```

**Pick the registration site by what the action targets:**

| Global service action | Entity service |
|------------------------|----------------|
| Registered in `async_setup` (a `services.py` module) — P18 | Registered per-platform via `async_register_entity_service` |
| Targets are validated by the voluptuous schema (`entity_id`/`device_id`/`area_id`) | Framework resolves targets and dispatches to the entity method |
| Handler receives a `ServiceCall`, resolves targets itself | Handler is a method on the entity; feature checks via `supported_features` |
| Use when the action spans the integration or takes no entity | Use when the action is one operation on one entity |

**No registry needed** — periodic work is not a service action. Recurring fetches
belong on the coordinator `update_interval` (a module constant, PS6); recurring
side-effects that are not fetches use `async_track_time_interval`. Service actions with
a return value set `supports_response=SupportsResponse.ONLY|OPTIONAL`.
See `${CLAUDE_SKILL_DIR}/references/advanced-service-patterns.md` for response data,
entity services, and scheduling.

---

## Iron Laws — Never Violate These

1. **REGISTER IN `async_setup`, NOT `async_setup_entry` (P18)** — service actions live
   in a `services.py` module registered once in `async_setup`; registering per config
   entry duplicates handlers on every reload. "Nowadays, we prefer registering service
   actions in `async_setup` in the init module." — MartinHjelmare,
   https://github.com/home-assistant/core/pull/154306#discussion_r2668008389
2. **SCHEMAS ARE STRICT — NO `vol.ALLOW_EXTRA` (P18)** — every accepted key is declared;
   unknown keys are a validation error, not silently passed through. "We normally don't
   mark service action schemas to allow extra parameters." — MartinHjelmare,
   https://github.com/home-assistant/core/pull/155198#discussion_r2599103290
3. **RAISE THE RIGHT EXCEPTION, TRANSLATED (P3)** — `ServiceValidationError` for user
   error, `HomeAssistantError` for device/API failure; both carry a `translation_domain`
   + `translation_key`. "Raise `ServiceValidationError` here in the service action handler
   with a translated error message." — MartinHjelmare,
   https://github.com/home-assistant/core/pull/155465#discussion_r2797370954
4. **VALIDATE WITH SELECTORS; TRUST THE SCHEMA (PS15, P3)** — use selectors over bare
   string validators, then read schema-guaranteed keys directly — never `dict.get` for a
   required key. "Don't use `dict.get` for keys which are guaranteed to be in the schema."
   — emontnemery, https://github.com/home-assistant/core/pull/159222#discussion_r2624589777
5. **CHECK STATE/FEATURES BEFORE ACTING (P3)** — a request the target cannot satisfy is a
   user error: raise a translated `ServiceValidationError`, do not silently no-op. "this
   will raise `ServiceValidationError('This alert cannot be acknowledged…')`" — reviewer,
   https://github.com/home-assistant/core/pull/139594#discussion_r2313097615
6. **NO BLOCKING I/O IN THE HANDLER (P4)** — service handlers run on the event loop; push
   blocking calls into `hass.async_add_executor_job` or the library's async API. "don't do
   blocking I/O in the event loop, even in tests" — MartinHjelmare,
   https://github.com/home-assistant/core/pull/154625#discussion_r2619211602
7. **PERIODIC WORK IS SCHEDULED, NOT A SERVICE — AND THE INTERVAL IS A CONSTANT (PS6)** —
   recurring fetches use the coordinator `update_interval`; other recurring work uses
   `async_track_time_interval`. The interval is a module constant, never user-configurable.
   "We don't allow options for changing scan interval." — MartinHjelmare,
   https://github.com/home-assistant/core/pull/154428#discussion_r2493741931

## Quick Service Action Template

```python
# services.py
SERVICE_SEND = "send"
ATTR_MESSAGE = "message"

SERVICE_SEND_SCHEMA = vol.Schema(  # strict: no vol.ALLOW_EXTRA (P18)
    {
        vol.Required(ATTR_ENTITY_ID): cv.entity_id,
        vol.Required(ATTR_MESSAGE): cv.string,
    }
)


def async_setup_services(hass: HomeAssistant) -> None:
    """Register integration service actions (called from async_setup, P18)."""

    async def async_handle_send(call: ServiceCall) -> None:
        entity_id = call.data[ATTR_ENTITY_ID]  # schema-guaranteed, no .get (PS15)
        entry = _resolve_entry(hass, entity_id)
        if entry is None:
            raise ServiceValidationError(  # user error (P3)
                translation_domain=DOMAIN, translation_key="entity_not_found"
            )
        try:
            await entry.runtime_data.client.send(call.data[ATTR_MESSAGE])
        except MyDeviceError as err:
            raise HomeAssistantError(  # device/API failure (P3)
                translation_domain=DOMAIN, translation_key="send_failed"
            ) from err

    hass.services.async_register(
        DOMAIN, SERVICE_SEND, async_handle_send, schema=SERVICE_SEND_SCHEMA
    )
```

```python
# __init__.py
async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the integration."""
    async_setup_services(hass)  # once, not per entry (P18)
    return True
```

## Exception Semantics

| Situation | Raise | Result |
|-----------|-------|--------|
| Bad/impossible input from the user | `ServiceValidationError` (translated) | Surfaced to the user; not logged as a traceback |
| Target cannot satisfy the request (state/feature) | `ServiceValidationError` (translated) | User error — never a silent no-op |
| Device/API/library failure at call time | `HomeAssistantError` (translated) | Surfaced as an action failure |
| Programmer error (wrong key on a strict schema) | (schema rejects it) | Validation error before the handler runs |
| Never | `_LOGGER.error(...)` then `raise` | Log-and-raise is forbidden (P2) |

## Quick Decisions

### Which registration?

- **Acts on one entity, feature-gated** → entity service (`async_register_entity_service`)
- **Spans the integration / takes no entity** → global service in `services.py` (P18)
- **Returns data to the caller** → `supports_response=SupportsResponse.ONLY|OPTIONAL`
- **Recurring fetch for entities** → coordinator `update_interval` constant (PS6), not a service
- **Recurring non-fetch side-effect** → `async_track_time_interval`, torn down on unload (PS5)

### Testing Pattern

```python
await hass.services.async_call(
    DOMAIN, "send", {"entity_id": "sensor.demo", "message": "hi"}, blocking=True
)
assert mock_client.send.called

# Response-returning action: pass return_response=True and assert the payload
result = await hass.services.async_call(
    DOMAIN, "fetch", {...}, blocking=True, return_response=True
)
assert result == {"items": [...]}
```

## Common Anti-patterns

| Wrong | Right |
|-------|-------|
| `hass.services.async_register(...)` in `async_setup_entry` | Register in `async_setup` via `services.py` (P18) |
| `vol.Schema({...}, extra=vol.ALLOW_EXTRA)` | Declare every key; strict schema (P18) |
| `raise HomeAssistantError("Bad value")` for user input | `ServiceValidationError(translation_domain=..., translation_key=...)` (P3) |
| `call.data.get(ATTR_MESSAGE)` for a required key | `call.data[ATTR_MESSAGE]` — trust the schema (PS15) |
| Recreating the schema inside the handler each call | Module-level schema constant (review §12.2) |
| `time.sleep`/`requests.get` in the handler | `async_add_executor_job` or the library's async API (P4) |
| A service action that runs itself on a timer | Coordinator `update_interval` / `async_track_time_interval` (PS6) |

## References

For detailed patterns, see:

- `${CLAUDE_SKILL_DIR}/references/service-handler-patterns.md` - Handler anatomy, exception mapping (P3), supported-feature checks, target resolution
- `${CLAUDE_SKILL_DIR}/references/service-registration.md` - `services.py` registration (P18), strict voluptuous schemas, selectors, scheduling
- `${CLAUDE_SKILL_DIR}/references/testing-patterns.md` - Testing service calls, response data, assertions (OSS core fixtures)
- `${CLAUDE_SKILL_DIR}/references/advanced-service-patterns.md` - Response data (`SupportsResponse`), entity services, coordinator/time-interval scheduling
