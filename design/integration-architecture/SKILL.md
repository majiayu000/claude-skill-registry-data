---
name: ha:integration-architecture
description: "Home Assistant integration design — config-entry-backed components, async_setup_entry/async_unload_entry symmetry, typed runtime_data, DataUpdateCoordinator, platform forwarding, dispatcher/events, manifest.json. Use when editing integration setup, the module layout, or designing boundaries."
effort: medium
user-invocable: false
---

# Integration Architecture Reference

> **Entity/coordinator work**: the `entity-platforms` skill covers entities and
> platform files; the `coordinator-patterns` skill covers data fetching. Use
> those for entity/coordinator internals — the integration-boundary, setup
> lifecycle, and dispatcher patterns below still apply.

Reference for designing and implementing Home Assistant integrations (config-entry-backed components).

## Iron Laws — Never Violate These

1. **PROTOCOL LIVES IN A PUBLISHED LIBRARY** — Transport, protocol, parsing, and device semantics belong in a PyPI library (dependency-transparency: CI-published, tagged, no pre-releases); never in the integration (P11, https://github.com/home-assistant/core/pull/158279#discussion_r2600415810)
2. **TYPED RUNTIME_DATA IS MANDATORY** — Per-entry state lives on `entry.runtime_data`, typed via `type XConfigEntry = ConfigEntry[XData]`; never `hass.data`, untyped dicts, or module globals (P6, https://github.com/home-assistant/core/pull/167872#discussion_r3064090359)
3. **VALIDATE BEFORE YOU CREATE; SET UP BEFORE YOU FORWARD** — Config flow tests the connection before `async_create_entry`; the client is created and the first refresh done in `__init__.py`, raising `ConfigEntryNotReady`/`ConfigEntryAuthFailed` on failure (P16, https://github.com/home-assistant/core/pull/169500#discussion_r3570262283)
4. **SETUP AND UNLOAD ARE SYMMETRIC** — Every platform forwarded and every subscription/listener registered in setup is torn down in `async_unload_entry`, via `entry.async_on_unload` (PS3, https://github.com/home-assistant/core/pull/162188#discussion_r2765956114)

## Integration Structure

```
homeassistant/components/example/   # domain == folder name (manifest.json)
├── __init__.py            # async_setup_entry / async_unload_entry (P16)
├── config_flow.py         # UI setup steps (voluptuous schemas + selectors)
├── coordinator.py         # DataUpdateCoordinator subclass (PS20)
├── entity.py              # shared CoordinatorEntity base
├── sensor.py              # one platform per file (binary_sensor.py, ...)
├── const.py               # SHARED constants only (PS10)
├── services.py            # service actions, registered in async_setup (P18)
├── diagnostics.py         # redacted diagnostics dump (PS7)
├── manifest.json          # domain, requirements, iot_class, quality_scale
├── strings.json           # user-facing translations (P9)
├── quality_scale.yaml     # all 56 rules with todo/exempt/done (PR2)
└── icons.json             # entity/service icon translations
```

## Typed Runtime Data (CRITICAL)

Per-entry objects (coordinator, client) live on `entry.runtime_data`, never in
`hass.data` or module globals. Type the entry so every access is checked (P6):

```python
# coordinator.py
type ExampleConfigEntry = ConfigEntry[ExampleDataUpdateCoordinator]


# __init__.py
async def async_setup_entry(hass: HomeAssistant, entry: ExampleConfigEntry) -> bool:
    """Set up Example from a config entry."""
    coordinator = ExampleDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()  # raises ConfigEntryNotReady (P16)

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ExampleConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
```

`emontnemery`: "It's not OK to store data in (module) global variables."
(https://github.com/home-assistant/core/pull/130281#discussion_r3232606549). Cross-entry
sharing uses a typed `HassKey`, never a bare `hass.data[DOMAIN]` dict.

## Quick Decisions

### When to SPLIT into a separate integration?

- The device/service is a genuinely different product with its own library
- New integrations ship ONE platform at Bronze first — grow later (PR2)
- Independent codeowner could own it
- Protocol differs enough to need its own PyPI dependency

### When to KEEP together?

- Entities describe the same device/hub and share one coordinator
- Platforms poll the same API in one coordinator refresh
- Splitting would force cross-integration calls for shared state

### Cross-Integration References

```python
# ✅ Depend via manifest "dependencies"/"after_dependencies"; import the
#    component ROOT, not a submodule (CONTESTED #5 — pylint root-import wins)
from homeassistant.components import bluetooth

# ❌ Reaching into another integration's internals
from homeassistant.components.other.coordinator import OtherCoordinator  # don't
```

## Anti-patterns

| Wrong | Right |
|-------|-------|
| Protocol/parsing bytes inside the integration | Published PyPI library (P11) |
| `hass.data[DOMAIN]` dicts / module globals for entry state | Typed `entry.runtime_data` (P6) |
| `async_create_entry` before any client call | Test the connection in the flow first (P16) |
| Forwarding platforms with no matching unload | Symmetric `async_unload_platforms` (PS3) |
| Constants used in one module living in `const.py` | Keep single-use constants local (PS10) |

## Data-Fetch Notes

- **Polling integrations**: `DataUpdateCoordinator` owns the fetch; a fixed
  `update_interval` constant (never user-configurable — PS6); entities read
  `coordinator.data`.
- **Push integrations**: no polling interval; the library pushes updates and the
  integration dispatches them (`async_dispatcher_send`) — coordinator discipline
  differs legitimately (PS3).
- Detect which fits: look at the library — does it expose a subscription/callback
  (push) or only request/response calls (poll)? — before choosing the pattern.

## References

For detailed patterns, see:

- `${CLAUDE_SKILL_DIR}/references/setup-patterns.md` - Full setup/unload lifecycle, first refresh, dispatcher/events, hub devices, large-integration split
- `${CLAUDE_SKILL_DIR}/references/runtime-data.md` - Typed `runtime_data` (P6), ConfigEntry context, session injection (PS5), reauth
- `${CLAUDE_SKILL_DIR}/references/lifecycle-patterns.md` - Setup/unload ordering, platform forwarding, update listeners, teardown placement
- `${CLAUDE_SKILL_DIR}/references/surface-patterns.md` - services.py (P18), diagnostics, exceptions (P3), manifest.json, strings.json
- `${CLAUDE_SKILL_DIR}/references/structure-patterns.md` - Integration structure, const.py placement, anti-patterns, cross-integration boundaries
