---
name: ha:coordinator-patterns
description: "Coordinator patterns — DataUpdateCoordinator anatomy, typed runtime_data, CoordinatorEntity data flow, push vs poll, first refresh, unload symmetry, config-entry migrations. Use when editing coordinator.py, runtime_data wiring, CoordinatorEntity classes, or async_migrate_entry."
effort: medium
user-invocable: false
paths:
  - "**/coordinator.py"
  - "**/entity.py"
  - "**/components/*/__init__.py"
  - "**/custom_components/*/__init__.py"
---

# Coordinator Patterns Reference

Reference for working with `DataUpdateCoordinator`, typed `runtime_data`, and
`CoordinatorEntity` data flow. Detect whether the integration polls or is pushed before
applying patterns: look for `update_interval=timedelta(...)` (polling) versus
`update_interval=None` + library callbacks/dispatcher (push). Some integrations use both
for different data streams — match the pattern to the coordinator you're editing.

## Iron Laws — Never Violate These

1. **THE LIBRARY OWNS THE PROTOCOL** (P11) — Transport, parsing, and device semantics live in the published PyPI library; the coordinator only orchestrates fetches. "Transport code and protocol details should always go in a 3rd party library published on PyPI." — MartinHjelmare, https://github.com/home-assistant/core/pull/158279#discussion_r2600415810
2. **`_async_update_data` RAISES — IT NEVER LOGS-AND-RETURNS** (PS3, P3) — `UpdateFailed` for fetch errors, `ConfigEntryAuthFailed` for auth; the base class handles availability, logging, and retry. "We just need to raise UpdateFailed... the coordinator will take part of everything" — joostlek, https://github.com/home-assistant/core/pull/162188#discussion_r2765956114
3. **TYPE THE COORDINATOR AND THE ENTRY** (P6) — `type XConfigEntry = ConfigEntry[XCoordinator]` on `runtime_data`; never `hass.data[DOMAIN]`, never `dict[str, Any]`. "don't use hass data instead use runtime_data." — edenhaus, https://github.com/home-assistant/core/pull/167872#discussion_r3064090359
4. **FIRST REFRESH HAPPENS IN SETUP** (P16) — `await coordinator.async_config_entry_first_refresh()` inside `async_setup_entry`; failures become `ConfigEntryNotReady`/`ConfigEntryAuthFailed` automatically. "The first refresh method needs to be called within the `async_setup_entry`" — MartinHjelmare, https://github.com/home-assistant/core/pull/166175#discussion_r3032611222
5. **ENTITIES READ `coordinator.data` — THEY NEVER FETCH** — entity properties are pure views over the coordinator snapshot; a fetch per entity is the event-loop analog of an N+1 query (P4, PS3).
6. **UPDATE INTERVALS ARE MODULE CONSTANTS** (PS3, PS6) — never parameters, never user-configurable. "We don't allow options for changing scan interval." — MartinHjelmare, https://github.com/home-assistant/core/pull/154428#discussion_r2493741931
7. **UNLOAD SYMMETRICALLY** (PS3, PS5) — every listener, session, and background task registered during setup is torn down via `entry.async_on_unload`; no leaked clients across reloads. "Why would we leak one on every reload?" — joostlek, https://github.com/home-assistant/core/pull/169689#discussion_r3547362246
8. **NO PRE-SEEDED `data`, NO MANUAL AVAILABILITY** (PS3) — never assign `coordinator.data = {}` or hand-roll `_attr_available` bookkeeping the base class already does. "No need to initialize data as a dict, `_async_update_data` will be run at start" — joostlek, https://github.com/home-assistant/core/pull/148181#discussion_r2249340085
9. **NEVER `async_refresh()` OR COORDINATOR ACCESS IN TESTS** (P13, P14) — move time with `freezer.tick` + `async_fire_time_changed`. "Don't access the coordinator directly in tests. Move time forward instead" — MartinHjelmare, https://github.com/home-assistant/core/pull/154677#discussion_r2522917818

## Quick Coordinator Templates

### Polling coordinator

```python
type MyConfigEntry = ConfigEntry[MyCoordinator]  # P6

UPDATE_INTERVAL = timedelta(minutes=5)  # constant, never user-config (PS6)


class MyCoordinator(DataUpdateCoordinator[MyDeviceData]):
    """Coordinate fetching from the device."""

    config_entry: MyConfigEntry

    def __init__(
        self, hass: HomeAssistant, config_entry: MyConfigEntry, client: MyClient
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            config_entry=config_entry,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
        )
        self.client = client

    async def _async_setup(self) -> None:
        """One-time init before the first refresh (PS3)."""
        self.device_info = await self.client.get_device_info()

    async def _async_update_data(self) -> MyDeviceData:
        """Fetch a full snapshot; raise, never log-and-return (PS3, P2)."""
        try:
            return await self.client.get_data()
        except MyAuthError as err:
            raise ConfigEntryAuthFailed from err  # triggers reauth flow
        except MyConnectionError as err:
            raise UpdateFailed(
                translation_domain=DOMAIN, translation_key="update_failed"
            ) from err
```

### CoordinatorEntity

```python
class MySensor(CoordinatorEntity[MyCoordinator], SensorEntity):
    """Pure view over coordinator.data — never fetches."""

    _attr_has_entity_name = True  # P17

    def __init__(
        self, coordinator: MyCoordinator, description: MySensorEntityDescription
    ) -> None:
        """Initialize the sensor. No side effects in constructors (PS4)."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.device_info.serial}_{description.key}"  # P7

    @property
    def native_value(self) -> float | None:
        """Return None for unknown — never a sentinel (P8)."""
        return self.entity_description.value_fn(self.coordinator.data)
```

## Quick Decisions

### Poll vs Push vs No Coordinator

| Pattern | Use When |
|----------|----------|
| Polling coordinator (`update_interval` constant) | API must be polled; one fetch feeds all entities |
| Push coordinator (`update_interval=None` + `async_set_updated_data`) | Library delivers callbacks/websocket events |
| No coordinator | Single entity, trivial fetch — "I am starting to doubt if a coordinator is the right pattern" — joostlek, https://github.com/home-assistant/core/pull/159140#discussion_r2657808028 (rejected-5 guidance) |

### Coordinator Data Shape

| Data | Shape |
|--------------|----------|
| Single device | One library model or frozen dataclass — don't wrap a single object in a dataclass (P6 corollary) |
| Multiple devices | `dict[str, DeviceData]` keyed by stable device id (P7) — entities index by their id |

## Common Anti-patterns

| Wrong | Right |
|-------|-------|
| `except Exception: _LOGGER.error(...)` in `_async_update_data` | `raise UpdateFailed(...) from err` (PS3, P1, P2) |
| `self.data = {}` before first refresh | Let `async_config_entry_first_refresh` populate it (PS3) |
| `update_interval=timedelta(seconds=entry.options["scan_interval"])` | Module constant `UPDATE_INTERVAL` (PS6) |
| `await self.client.fetch()` inside an entity property | Read `self.coordinator.data` |
| Overriding `available` with `last_update_success` | Delete it — "Is default for CoordinatorEntity" — joostlek, https://github.com/home-assistant/core/pull/149456#discussion_r2538844415 |
| `struct.unpack`/checksum math in `_async_update_data` | Parse in the PyPI library (P11) |

## References

For detailed patterns, see:

- `${CLAUDE_SKILL_DIR}/references/typed-data.md` - Typed coordinator data, dataclasses vs library models, `runtime_data` typing (P6), None-for-unknown (P8)
- `${CLAUDE_SKILL_DIR}/references/data-flow.md` - CoordinatorEntity data flow, derived values, dynamic device discovery, sequential vs parallel fetches
- `${CLAUDE_SKILL_DIR}/references/entry-migrations.md` - Config-entry `version`/`minor_version` migrations, `async_migrate_entry`, unique-id migrations (PR3, P7)
- `${CLAUDE_SKILL_DIR}/references/lifecycle.md` - Setup/unload symmetry, `_async_setup`, first refresh (P16), session discipline (PS5), poll-after-write
- `${CLAUDE_SKILL_DIR}/references/push-patterns.md` - Push coordinators, dispatcher wiring (PS4), parent/child fan-out at scale, `always_update=False`
