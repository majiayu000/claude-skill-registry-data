---
name: ha:testing
description: "Python / Home Assistant testing patterns — pytest, the mealie-pattern conftest mock, JSON fixtures, snapshot_platform, black-box state-machine assertions. Use when working on tests/components/**/test_*.py, conftest.py, or fixtures, or fixing test failures."
effort: medium
user-invocable: false
paths:
  - "tests/components/**/test_*.py"
  - "tests/components/**/conftest.py"
  - "tests/components/**/common.py"
  - "tests/components/**/fixtures/**"
---

# Home Assistant Testing Reference

> **Entity-platform integrations**: snapshot the whole platform with `snapshot_platform` and set the entry up through the core API — assert what the user sees, not internal objects. See the `entity-platforms` skill.

Quick reference for Home Assistant (pytest) testing patterns.

## Iron Laws — Never Violate These

1. **BLACK-BOX BY DEFAULT (P13)** — Set the entry up via `hass.config_entries.async_setup`; assert `hass.states.get(...)` and `hass.services.async_call(...)`. Never touch `runtime_data`, coordinators, or entity objects — patch only the third-party library. "we should not touch runtime_data" — joostlek, https://github.com/home-assistant/core/pull/155099#discussion_r2488878373
2. **NO CONDITIONALS IN TESTS (P12)** — No `if`/branching in a `test_*` body; parametrize or split, and know the expected value in advance. "We should avoid if statements in tests." — edenhaus, https://github.com/home-assistant/core/pull/156588#discussion_r2707493472
3. **MOCK ONLY AT THE LIBRARY BOUNDARY (PS14)** — One `autospec=True` library mock in `conftest.py`, patched at BOTH the `__init__` and `config_flow` import sites. Never patch core internals, the executor, or the stdlib. "we should make sure we patch the entrypoints" — joostlek, https://github.com/home-assistant/core/pull/175448#discussion_r3519164396
4. **FIXTURES ARE JSON (PS14)** — Large/realistic payloads live in `tests/components/<domain>/fixtures/` and load via `load_json_object_fixture`; config entries reflect a real-world entry. "Consider storing the large amounts of data in json fixtures" — joostlek, https://github.com/home-assistant/core/pull/168125#discussion_r3082146845
5. **SIMULATE TIME (P14)** — Advance the clock with `freezer.tick(...)` + `async_fire_time_changed(hass)`. Never `time.sleep`/`asyncio.sleep` (>0.1s), never `async_refresh`/`async_update_entity`. "use the `freezer` to skip time... a 'natural' refresh" — joostlek, https://github.com/home-assistant/core/pull/162041#discussion_r2769309201
6. **CONFIG FLOW 100% COVERAGE (P15)** — Every step and error path tested; each error path must recover and end in `CREATE_ENTRY`. "This should end in CREATE_ENTRY to test that it's able to recover" — joostlek, https://github.com/home-assistant/core/pull/152000#discussion_r2649291946
7. **SNAPSHOT ENTITY PLATFORMS (PS13)** — Use `snapshot_platform`; review `.ambr` diffs before commit; never re-assert what the snapshot already covers. "You probably can just use `snapshot_platform`" — joostlek, https://github.com/home-assistant/core/pull/148989#discussion_r2227954744
8. **ASSERT CALL ARGS, NOT JUST COUNTS** — Assert the arguments (and whole structures at once), not only that a mock was called. "Please assert the call args of all mock calls, besides the call count." — MartinHjelmare, https://github.com/home-assistant/core/pull/161936#discussion_r2848214581

## Quick Decisions

### Which Test Setup?

| Testing | Use |
|---------|-----|
| Config entry setup/reload/unload | `MockConfigEntry` + `hass.config_entries.async_setup` (`test_init.py`) — assert `entry.state` transitions (P13) |
| Config flow | `hass.config_entries.flow.async_init(...)` + `async_configure(...)` (`test_config_flow.py`, 100% — P15) |
| Entity platform | `snapshot_platform` + `@pytest.mark.usefixtures("entity_registry_enabled_by_default")` (PS13) |
| Service action | `hass.services.async_call(...)` and assert the state machine / mock call args (P18) |
| Frontend `src/common` util | Vitest unit test in the mirrored `test/` path (FS15 / FI-6) |

### When to worry about isolation?

- ✅ Black-box tests driven through the core config-entries API — survive refactors
- ✅ Time advanced with `freezer` + `async_fire_time_changed` (P14)
- ❌ Tests touching `runtime_data`/coordinators/`hass.data` directly (P13)
- ❌ Tests relying on real wall-clock time or `time.sleep` (P14)

### Mock or not?

- ✅ Mock: the third-party library, at its boundary, with `autospec=True` (PS14)
- ❌ Don't mock: `hass`, the state machine, coordinators, your own flow code, or the stdlib

### JSON fixture or inline dict?

- Use `load_json_object_fixture` for **realistic / large** API payloads
- Inline a small dict only for a **tiny one-off** value the reader must see in the test

## Quick Patterns

```python
# Setup composition (black-box, P13)
async def test_setup(hass: HomeAssistant, mock_config_entry: MockConfigEntry) -> None:
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    assert mock_config_entry.state is ConfigEntryState.LOADED

# State-machine assertion (never read entity objects)
assert hass.states.get("sensor.kitchen_temperature").state == "21.5"

# Service call + assert library call args (P18, MartinHjelmare)
await hass.services.async_call(DOMAIN, "set_mode", {"mode": "eco"}, blocking=True)
mock_client.set_mode.assert_awaited_once_with("eco")

# Simulate time — never sleep (P14)
freezer.tick(UPDATE_INTERVAL)
async_fire_time_changed(hass)
await hass.async_block_till_done()

# Config flow recovery ends in CREATE_ENTRY (P15)
result = await hass.config_entries.flow.async_configure(result["flow_id"], user_input)
assert result["type"] is FlowResultType.CREATE_ENTRY

# Snapshot a whole platform (PS13)
await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)
```

## Common Anti-patterns

| Wrong | Right |
|-------|-------|
| `await asyncio.sleep(30)` | `freezer.tick(...)` + `async_fire_time_changed(hass)` (P14) |
| `coordinator.async_refresh()` in a test | Advance time for a natural refresh (P14) |
| `entry.runtime_data.client` / `hass.data[DOMAIN]` in a test | Assert via `hass.states.get` / service calls (P13) |
| `if condition:` inside a `test_*` body | `@pytest.mark.parametrize` the expected value (P12) |
| Large inline data dict in the test | JSON fixture + `load_json_object_fixture` (PS14) |
| `patch("...coordinator...")` / patching core internals | Patch the library at `__init__` + `config_flow` sites (PS14) |
| Re-asserting each entity a snapshot covers | `snapshot_platform` once (PS13) |

## References

For detailed patterns, see:

- `${CLAUDE_SKILL_DIR}/references/pytest-patterns.md` - Fixtures, markers, parametrize, assertions, running subsets
- `${CLAUDE_SKILL_DIR}/references/mocking-patterns.md` - The mealie-pattern conftest, autospec, patch sites (PS14)
- `${CLAUDE_SKILL_DIR}/references/lit-testing.md` - ha-frontend Vitest tests for `src/common`, component testing (FS15/FI-6)
- `${CLAUDE_SKILL_DIR}/references/fixture-patterns.md` - JSON fixtures, `load_json_object_fixture`, service-action testing
