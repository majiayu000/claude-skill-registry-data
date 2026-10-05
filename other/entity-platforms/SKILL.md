---
name: ha:entity-platforms
description: "Home Assistant entity platform patterns — platform modules (sensor.py), EntityDescriptions with value_fn, unique IDs, has_entity_name, device/entity registries, DeviceInfo, entity categories. Use when creating entity platforms, editing _attr_* properties, EntityDescriptions, device_info, or deciding whether an entity should exist."
effort: medium
user-invocable: false
---

# Home Assistant Entity Platform Patterns Reference

Reference for entity platform patterns in Home Assistant integrations.
HA's entity built-ins complement the coordinator and the registries — integration architecture, asyncio, and config-flow rules still apply.
Only the data-modeling patterns shift toward EntityDescriptions, `_attr_*` properties, DeviceInfo, and the device/entity registries.

## Iron Laws

Hard rules — the iron-law-judge blocks on these.

1. **UNIQUE IDS ARE STABLE, IMMUTABLE DEVICE IDENTIFIERS (P7)** — Serial number, `dr.format_mac()`, burned-in EEPROM ID, coordinates. Never host/port/IP/hostname/name/URL/email/username or any user-configured value; no `DOMAIN` prefixes, no platform suffixes (scope is already per `(integration_domain, entity_domain)`). A unique ID that changes orphans the user's history, settings, and automations. "Host and port do not qualify for a unique identifier, as they can change." — frenck, https://github.com/home-assistant/core/pull/148104#discussion_r2186877132 · "User configured values are not allowed to be used as unique ID." — balloob, https://github.com/home-assistant/core/pull/174931#discussion_r3484941101 · ADR-0011, https://developers.home-assistant.io/docs/entity_registry_index/
2. **MODEL UNKNOWN STATE AS `None` (P8)** — Never a sentinel (`-1`, `""`, `0`), a fake state, or a silently-returned stale last value; `"unknown"` never appears in ENUM `options`. HA renders `unknown` for you when the value property returns `None`. "We never set the state unknown directly. Instead, the native/state value... should return `None`." — frenck, https://github.com/home-assistant/core/pull/151652#discussion_r2321543174
3. **EVERY ENTITY SETS `_attr_has_entity_name = True`; THE MAIN-FEATURE ENTITY SETS `_attr_name = None` (P17)** — Non-primary entities get a `translation_key`; the primary feature displays the bare device name. "all new integrations should use `_attr_has_entity_name = True`... set `_attr_name = None`" — joostlek, https://github.com/home-assistant/core/pull/148181#discussion_r2249342063 · `has-entity-name` Bronze rule, https://developers.home-assistant.io/docs/core/integration-quality-scale/rules/has-entity-name/

## Strong Defaults

High-severity review findings — legitimate exceptions exist, so know the WHY before deviating.

4. **ENTITY DESCRIPTIONS: FULLY GENERIC OR FULLY CUSTOM — NEVER HALFWAY (PS11)** — Either the description carries a `value_fn` (and friends) so one entity class serves every description, or the entity is fully hand-written; don't subclass a description without adding fields, and don't keep per-entity `if/elif` ladders a `value_fn` would replace. WHY: halfway designs pay both costs — indirection *and* special cases. "extend the SensorEntityDescription and add a value_fn... keep this class more generic" — joostlek, https://github.com/home-assistant/core/pull/173043#discussion_r3413375038 (tension with the no-over-abstraction default PS10 is real — genericism wins for entity platforms)
5. **DEVICE CLASS / STATE CLASS / UNIT MUST BE SEMANTICALLY VALID TOGETHER (PS8)** — Use `suggested_display_precision`, never `round()` in the value property; prefer built-in device classes over custom translations. WHY: the recorder builds long-term statistics from this trio; an invalid combination corrupts them. "You can't have measurement with monetary, as the unit of measurement is always wrong" — joostlek, https://github.com/home-assistant/core/pull/156225#discussion_r2524894434 · **Anti-pattern (SUPERSEDED)**: runtime unit-of-measurement switching under a device class — breaks long-term statistics; never suggest it.
6. **RICH, HONEST DEVICE INFO (PS16)** — `via_device` for children, MAC in `connections`, `model` vs `model_id` as distinct fields, `None` over `"Unknown"`; hub devices are created in `__init__.py` via the device registry, never as entity side effects; entities never leave their platform module. WHY: the device page renders exactly what you register, and hub creation must not depend on platform load order. "create the hub devices directly in the device registry in `__init__.py`... not dependent on platform loading" — joostlek, https://github.com/home-assistant/core/pull/160044#discussion_r2658179480 · "The entities should not leave the platform." — MartinHjelmare, https://github.com/home-assistant/core/pull/159140#discussion_r2628359742
7. **STATIC/CONFIG DATA IS NOT AN ENTITY (PS7)** — Serial numbers, firmware versions, fixed capabilities belong in DeviceInfo; raw/debug payloads belong in `diagnostics.py` (PII redacted via `async_redact_data`); no arbitrary/dynamic `extra_state_attributes` dicts; diagnostic entities ship disabled by default. WHY: every entity costs recorder storage and dashboard attention forever. "The serial number should not be an entity." — frenck, https://github.com/home-assistant/core/pull/149237#discussion_r2269179540 · "The name might contain personal information? Is it relevant for a diagnostic dump?" — frenck, https://github.com/home-assistant/core/pull/169518#discussion_r3169300667

## Quick Reference

### Should This Entity Exist? — Model What the Dashboard Will Show

Judgment tier (PS7 + rejected-from-law items §D1/§D4/§D10) — maintainers raise these as *questions* in review; they are never mechanical blocks. Ask them before writing any platform code:

- **What will the dashboard show?** Model what the dashboard will show — not what the API returns. One API field ≠ one entity.
- **Is it static?** Serial, model, firmware → DeviceInfo. Raw payloads → `diagnostics.py` with `async_redact_data` (PS7).
- **Is it the semantically correct platform?** A togglable relay is a `switch`, not a writable `number`; a door contact is a `binary_sensor` with a device class, not a `sensor` returning `"open"`.
- **Who is it for?** Debug/monitoring values → `EntityCategory.DIAGNOSTIC` + `_attr_entity_registry_enabled_default = False` (collapsed and off for the average dashboard; power users opt in). Settings that modify device behavior → `EntityCategory.CONFIG`. Primary functionality → category `None`.
- **Device variants?** Model variant differences go in the description tuple or a subclass — deduplicate; never copy-paste a platform per model (§D10).
- **User-selectable entity sets?** Implement an options flow that removes entities from the registry — don't repurpose `disabled_by`, and never override `RegistryEntryDisabler.USER` (https://developers.home-assistant.io/docs/entity_registry_disabled_by/).

### Platform Module Anatomy (sensor.py)

```python
# homeassistant/components/<domain>/sensor.py — one platform, one module
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import MyConfigEntry, MyCoordinator  # type MyConfigEntry = ConfigEntry[MyCoordinator]  (P6)


@dataclass(frozen=True, kw_only=True)
class MySensorEntityDescription(SensorEntityDescription):
    """Fully generic (PS11): value_fn does ALL per-entity work."""

    value_fn: Callable[[DeviceData], float | None]


SENSORS: tuple[MySensorEntityDescription, ...] = (
    MySensorEntityDescription(
        key="temperature",
        translation_key="temperature",           # strings.json: entity.sensor.temperature.name (P9)
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=1,           # PS8 — never round() in the property
        value_fn=lambda data: data.temperature,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: MyConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up sensors from a config entry."""
    coordinator = entry.runtime_data                     # typed runtime_data, never hass.data (P6)
    async_add_entities(
        MySensor(coordinator, description) for description in SENSORS
    )


class MySensor(CoordinatorEntity[MyCoordinator], SensorEntity):
    """Entity reads coordinator.data — it never fetches (see /ha:coordinator-patterns)."""

    entity_description: MySensorEntityDescription
    _attr_has_entity_name = True                         # P17

    def __init__(
        self, coordinator: MyCoordinator, description: MySensorEntityDescription
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.device.serial}_{description.key}"  # P7
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.device.serial)},
        )

    @property
    def native_value(self) -> float | None:
        """Return the sensor value — None when the device can't answer (P8)."""
        return self.entity_description.value_fn(self.coordinator.data)
```

`P6` companion: the config entry type alias lives in `coordinator.py` — "don't use hass data instead use runtime_data." — edenhaus, https://github.com/home-assistant/core/pull/167872#discussion_r3064090359

### Unique IDs — Decided Before First Registration, Immutable Forever (P7)

```python
# CORRECT — burned-in identifiers survive every network/rename event
self._attr_unique_id = f"{device.serial_number}_{description.key}"
self._attr_unique_id = dr.format_mac(discovery_info.macaddress)

# WRONG — anything mutable silently forks the entity and strands its history
self._attr_unique_id = f"{entry.data[CONF_HOST]}_{description.key}"  # host changes with DHCP
self._attr_unique_id = f"{DOMAIN}_{device.name}"   # names are user-editable; no domain prefixes
self._attr_unique_id = f"{device.serial}_sensor"   # no platform suffixes — scope is already per platform
```

| Valid sources | Invalid sources |
| --- | --- |
| Device serial number | IP address / host / port |
| MAC via `dr.format_mac()` | Device name / hostname |
| Geographic coordinates (lat/lon) | URL |
| Burned-in identifier (EEPROM) | Email address / username |
| Config entry ID (fallback, single-device entries only) | Any user-configured value |

Changing a unique ID after release is a breaking change: users lose settings, history, and automations (https://developers.home-assistant.io/docs/entity_registry_index/). If the device truly exposes nothing unique, fall back to `entry.entry_id` — never fabricate one from connection data.

### Naming — has_entity_name and Translation Keys (P17)

```python
class TemperatureSensor(SensorEntity):
    _attr_has_entity_name = True
    _attr_translation_key = "temperature"   # -> entity.sensor.temperature.name in strings.json


class MainPowerSwitch(SwitchEntity):
    _attr_has_entity_name = True
    _attr_name = None                       # THE feature of the device: shows the bare device name
```

With a device named "Kitchen Sensor": the field entity displays "Kitchen Sensor Temperature"; the main feature displays "Kitchen Sensor". `translation_key` is only supported with `has_entity_name = True` (https://developers.home-assistant.io/docs/core/integration-quality-scale/rules/has-entity-name/).

**Detection**: if the device class's default translated name already says exactly what the entity is, omit both `_attr_name` and `translation_key` — the device-class translation is used (P9 corollary). Check sibling entities in the integration you touch; never mix literal-name and translated-name styles in one platform. See `/ha:translations` for the strings.json side.

### State — `None` for Unknown, `available` for Unreachable (P8)

```python
# CORRECT — None means "no answer right now"; HA renders `unknown`
@property
def native_value(self) -> int | None:
    if (reading := self.coordinator.data.rssi) is None:
        return None
    return reading

# WRONG — sentinels and stale values poison history and statistics
return -1                                   # fake number enters long-term statistics
return ""                                   # fake state
return self._last_value                     # stale value masquerading as fresh
options = ["heating", "cooling", "unknown"] # "unknown" is never an ENUM option
```

The availability half is separate: when the *device* is unreachable, `available` returns `False` (`CoordinatorEntity` derives it from the last refresh; `entity-unavailable` Silver rule). Unknown value on a reachable device → `None`; unreachable device → unavailable.

### Measurement Semantics — device_class / state_class / unit / precision (PS8)

Controlled presentation goes through the description fields, not ad-hoc math in the value property — `suggested_display_precision` is the display-level analogue of a rounding call, and it keeps the full-precision value flowing into statistics:

```python
MySensorEntityDescription(
    key="energy_today",
    device_class=SensorDeviceClass.ENERGY,               # brings name, icon, unit conversion for free
    state_class=SensorStateClass.TOTAL_INCREASING,       # must be valid WITH the device class
    native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
    suggested_display_precision=2,                        # never round() in native_value
    value_fn=lambda data: data.energy_today,
)
```

- The trio must be semantically valid together: MEASUREMENT with MONETARY is always wrong ("You can't have measurement with monetary, as the unit of measurement is always wrong" — joostlek, https://github.com/home-assistant/core/pull/156225#discussion_r2524894434); totals that reset use `TOTAL_INCREASING`.
- Prefer a built-in device class over a custom `translation_key` — the device class supplies translated names, icons, and unit conversion (https://developers.home-assistant.io/docs/core/entity/).
- **Never** switch `native_unit_of_measurement` at runtime under a device class — SUPERSEDED anti-pattern, breaks long-term statistics.

### DeviceInfo — What the Device Page Renders (PS16)

The registries are the single source of truth for what the frontend shows on the device page — richness here is free UI:

```python
_attr_device_info = DeviceInfo(
    identifiers={(DOMAIN, device.serial)},        # first-pass match; unique within your domain
    connections={(dr.CONNECTION_NETWORK_MAC, dr.format_mac(device.mac))},  # globally unique; fallback match
    via_device=(DOMAIN, hub.serial),              # parent hub -> device topology in the UI
    manufacturer="Vendor Inc.",
    model="Model X",                              # marketing name
    model_id="VX-100",                            # hardware/SKU code — a DIFFERENT field, not a duplicate
    sw_version=device.firmware,                   # None over "Unknown" when absent
    hw_version=device.hardware_revision,
)
```

- DeviceInfo is only processed when the entity loads via a config entry AND has a `unique_id` (https://developers.home-assistant.io/docs/device_registry_index/).
- Identifiers are matched first, connections as fallback — use identifiers as the primary key.
- Hub/gateway devices: `dr.async_get(hass)` + `async_get_or_create(...)` in `__init__.py`, so children can `via_device`-link regardless of platform load order (joostlek, https://github.com/home-assistant/core/pull/160044#discussion_r2658179480).
- Entity classes are defined and instantiated in their own platform module — "The entities should not leave the platform." (MartinHjelmare, https://github.com/home-assistant/core/pull/159140#discussion_r2628359742).
- Support user-initiated removal with `async_remove_config_entry_device()`; return `False` only for devices that must not be removed (e.g. the gateway itself).
- Subscriptions and stored references belong in `async_added_to_hass` (runs only for *enabled* entities), torn down via `async_on_remove` — PS4, see `/ha:coordinator-patterns`.

### File Conventions (integration layout)

| File            | Location                                              | Behaviour                                            |
| --------------- | ----------------------------------------------------- | ---------------------------------------------------- |
| Platform        | `homeassistant/components/<domain>/sensor.py`         | description tuple + `async_setup_entry` + entity classes |
| Shared base     | `homeassistant/components/<domain>/entity.py`         | common `CoordinatorEntity` base carrying `device_info` |
| Coordinator     | `homeassistant/components/<domain>/coordinator.py`    | owns fetch + `type XConfigEntry` alias (P6)           |
| Constants       | `homeassistant/components/<domain>/const.py`          | shared-only constants (PS10); platform-local ones stay local |
| Entity strings  | `strings.json` → `entity.<platform>.<translation_key>.name` | translated names (P9/P17)                        |
| Icons           | `icons.json` → `entity.<platform>.<key>`              | icon translations                                     |
| Diagnostics     | `homeassistant/components/<domain>/diagnostics.py`    | raw dumps via `async_redact_data` (PS7)               |
| Snapshots       | `tests/components/<domain>/snapshots/*.ambr`          | `snapshot_platform` output (PS13)                     |

(Custom integrations: same layout under `custom_components/<domain>/`.)

### Scaffold & Snapshot Workflow

```bash
# Core checkout: generate the integration skeleton (no analog for custom_components — copy a reference integration)
python3 -m script.scaffold integration
#   ? domain / name / codeowner / PyPI package / auth & discovery flows

# Validate manifest/strings/icons/quality_scale after every platform change
python3 -m script.hassfest --domain my_domain

# Snapshot the whole platform (PS13) — review .ambr diffs before commit, never hand-edit them
pytest tests/components/my_domain/ --snapshot-update
pytest tests/components/my_domain/ --cov=homeassistant.components.my_domain --cov-report term-missing
```

Snapshot pointer (PS13): every entity platform gets a `snapshot_platform` test; never re-assert what the snapshot already covers — "You probably can just use `snapshot_platform` which is a built in one" — joostlek, https://github.com/home-assistant/core/pull/148989#discussion_r2227954744. See `/ha:testing` for the fixture/mock side.

New-integration scope (PR2): one platform, Bronze tier, complete `quality_scale.yaml` — see `/ha:quality-scale`.

## Research

Prefer the highest-fidelity source available:

1. **Installed core source** (exact version from your environment):

   ```bash
   pip show homeassistant | grep -i location
   code $(python3 -c "import homeassistant.components.sensor as m; print(m.__file__)")
   ```

   Reference integrations maintainers point to for current entity-platform style: `mealie`, `niko_home_control`, `trmnl`.

2. **ha-docs-fetcher skill** (synced to developers.home-assistant.io):

   Use the `ha-docs-fetcher` skill to fetch entity, device-registry, and
   entity-registry docs matching the core version you're targeting.

3. **WebFetch official docs** (fallback when neither is available):

   ```
   WebFetch(url: "https://developers.home-assistant.io/docs/core/entity/", prompt: "Extract entity base class and _attr_ docs.")
   WebFetch(url: "https://developers.home-assistant.io/docs/device_registry_index/", prompt: "Extract DeviceInfo/identifiers/via_device docs.")
   WebFetch(url: "https://developers.home-assistant.io/docs/entity_registry_index/", prompt: "Extract unique-ID and disabled_by docs.")
   ```

If `ha-docs-fetcher` is not configured, the SessionStart hook suggests how to install it.
