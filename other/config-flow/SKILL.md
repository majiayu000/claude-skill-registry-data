---
name: ha:config-flow
description: "Home Assistant config flow patterns — async_step_user/zeroconf/dhcp/reauth/reconfigure, options flow, subentries, unique IDs, selectors, strings.json wiring, 100% flow test coverage. Use when writing config_flow.py, options/subentry flows, the config section of strings.json, or config-flow tests."
effort: medium
user-invocable: false
---

# Home Assistant Config Flow Reference

Reference for config-flow patterns in Home Assistant integrations.
The config flow is the integration's front door: it collects input, validates it against
the real device/service, claims a unique ID, and creates the config entry. Setup work
(client creation, first refresh) does NOT belong here — it lives in `__init__.py` and the
coordinator (see `/ha:coordinator-patterns`).

## Iron Laws — Never Violate These

1. **VALIDATE BEFORE CREATE (P16)** — The user step must call the library and prove the
   connection/credentials *before* `async_create_entry`. Client creation + first refresh
   live in `__init__.py`/the coordinator, which raise `ConfigEntryNotReady`/
   `ConfigEntryAuthFailed` on failure. DOC-BACKED: `test-before-configure` +
   `test-before-setup` (Bronze). "move the client initialization to `__init__.py`" —
   joostlek, https://github.com/home-assistant/core/pull/169500#discussion_r3570262283
2. **UNIQUE IDS ARE STABLE, IMMUTABLE DEVICE IDENTIFIERS (P7)** — Serial number,
   `format_mac()`, burned-in ID. Never host/port/hostname/IP/name/URL/email/user-config;
   no domain prefixes or platform suffixes. DOC-BACKED: `entity-unique-id` +
   `unique-config-entry` (Bronze), ADR-0011. "Host and port do not qualify for a unique
   identifier, as they can change." — frenck,
   https://github.com/home-assistant/core/pull/148104#discussion_r2186877132; "User
   configured values are not allowed to be used as unique ID." — balloob,
   https://github.com/home-assistant/core/pull/174931#discussion_r3484941101
3. **CLAIM THE UNIQUE ID BEFORE CREATING (P7)** — Every create path calls
   `await self.async_set_unique_id(...)` then `self._abort_if_unique_id_configured()`;
   discovery steps do it *before* showing the confirm form so duplicates abort early.
   Fallback to the config-entry ID only when the device has nothing unique
   (registries.md fallback; emontnemery,
   https://github.com/home-assistant/core/pull/135844#discussion_r2303143344).
4. **100% FLOW COVERAGE; EVERY ERROR PATH RECOVERS AND ENDS IN CREATE_ENTRY (P15)** —
   Assert `unique_id`, `step_id`, and the already-configured abort. DOC-BACKED:
   `config-flow-test-coverage` (Bronze, merge-blocking). "This should end in
   CREATE_ENTRY to test that it's able to recover" — joostlek,
   https://github.com/home-assistant/core/pull/152000#discussion_r2649291946; "We're
   missing tests of the config flow. It requires 100% coverage." — MartinHjelmare,
   https://github.com/home-assistant/core/pull/158968#discussion_r2617578256
5. **EVERY FLOW STRING IS A TRANSLATION KEY (P9)** — Step titles, descriptions, `data`,
   `data_description`, `error`, and `abort` all live in strings.json; no dashes in keys;
   reuse common keys via `[%key:common::...%]` references. DOC-BACKED: ADR-0009, i18n
   docs. "As the string is the same, it means the same for the user, so why don't we use
   the same key?" — joostlek,
   https://github.com/home-assistant/core/pull/160263#discussion_r2987673952
6. **NEVER LOG-AND-RAISE IN VALIDATION HELPERS (P2)** — The exception carries the
   message; the flow's error dict decides what the user sees. "Don't both log and raise
   an exception. Let the handler of the exception decide" — MartinHjelmare,
   https://github.com/home-assistant/core/pull/152121#discussion_r2343364995

## Strong Defaults — Flag, Don't Block

1. **Selector craft (PS15)** — The right selector for the data type (password
   `TextSelector`, `DurationSelector`, `NumberSelector`, `CountrySelector`); prefill on
   error with `add_suggested_values_to_schema`; `data_description` for every new key;
   integration name injected via placeholders, never hardcoded into translated strings.
   "Use text selectors, not bare strings." — emontnemery,
   https://github.com/home-assistant/core/pull/158228#discussion_r2931027722; "Use
   `add_suggested_values_to_schema` so the user doesn't need to fill in everything
   again" — emontnemery,
   https://github.com/home-assistant/core/pull/125595#discussion_r2321110457
2. **No `dict.get` for schema-guaranteed keys (PS2)** — masks bugs and loses typing.
   "Don't use `dict.get` for keys which are guaranteed to be in the schema." —
   emontnemery, https://github.com/home-assistant/core/pull/159222#discussion_r2624589777
3. **No user-configurable scan interval (PS6)** — never a flow or options field.
   DOC-BACKED: `appropriate-polling` (Bronze). "We don't allow options for changing scan
   interval." — MartinHjelmare,
   https://github.com/home-assistant/core/pull/154428#discussion_r2493741931
4. **Subentries for per-item configuration (Strong Defaults §D-7 — STRONG hint)** —
   commands, sensor mappings, rooms belong in config subentries, not comma-separated
   options. Newer than the docs snapshot; never contradicts it. "represent the commands
   as config subentries" — emontnemery,
   https://github.com/home-assistant/core/pull/151690#discussion_r2919382819
5. **Reauth and reconfigure flows are expected (emontnemery A-1.6)** — reauth
   auto-starts when setup raises `ConfigEntryAuthFailed`. DOC-BACKED: quality-scale
   `reauthentication-flow` / `reconfiguration-flow`. "In follow-up PR please add reauth
   flow (auto start if credentials are invalid)" — emontnemery,
   https://github.com/home-assistant/core/pull/150886#discussion_r2485620547

## Quick Flow Template

```python
STEP_USER_DATA_SCHEMA = vol.Schema(  # module level — never rebuilt per call
    {
        vol.Required(CONF_HOST): TextSelector(),
        vol.Required(CONF_PASSWORD): TextSelector(
            TextSelectorConfig(type=TextSelectorType.PASSWORD)
        ),
    }
)


class ExampleConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Example."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # broad catch is ALLOWED here — the P1 carve-out
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(info.serial)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=info.title, data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(
                STEP_USER_DATA_SCHEMA, user_input
            ),
            errors=errors,
        )
```

The config flow is the ONE place `except Exception` is permitted (P1 carve-out) — it maps
to `errors["base"] = "unknown"` so the flow always recovers.

## Quick Decisions

### Which Step?

| Entry point | Step | Notes |
|---|---|---|
| Manual setup | `async_step_user` | The default; validate then create |
| Network discovery | `async_step_zeroconf` / `ssdp` / `dhcp` / `bluetooth` / `usb` / `mqtt` / `hassio` / `homekit` | Claim unique ID from discovery info first, confirm second |
| Credentials expired | `async_step_reauth` → `reauth_confirm` | Auto-started by `ConfigEntryAuthFailed` |
| Settings changed (host moved) | `async_step_reconfigure` | Ends in update+reload+abort, never `async_create_entry` |
| Tunables after setup | `OptionsFlowWithReload` | `async_step_init` first |
| Per-item config (commands, mappings) | Config subentries | STRONG hint (§D-7) |

Reserved step names are the framework's contract — see
`${CLAUDE_SKILL_DIR}/references/flow-anatomy.md` for the full list and each pattern.

### Error-Dict Recovery

`errors["base"] = "cannot_connect"` maps to `config.error.cannot_connect` in strings.json;
`errors[CONF_PASSWORD] = "invalid_auth"` attaches to one field. Showing the form again
with errors + suggested values IS the recovery path P15 tests must exercise.

## File Conventions

| File | Location | Behaviour |
|---|---|---|
| Flow handler | `homeassistant/components/<domain>/config_flow.py` | `ConfigFlow, domain=DOMAIN`; flow-only constants live here (PS10) |
| Manifest | `<domain>/manifest.json` | `"config_flow": true` (+ `zeroconf`/`dhcp` matchers) |
| Strings | `<domain>/strings.json` | `config.step/error/abort`, `options`, `config_subentries` trees |
| Setup | `<domain>/__init__.py` | client creation, first refresh, `ConfigEntryNotReady`/`ConfigEntryAuthFailed` (P16) |
| Tests | `tests/components/<domain>/test_config_flow.py` | 100% coverage of config_flow.py (P15) |
| Quality scale | `<domain>/quality_scale.yaml` | `config-flow`, `test-before-configure`, `unique-config-entry` statuses |

## Verification Workflow

```bash
ruff format . && ruff check . --fix
python3 -m script.hassfest --domain <domain>          # validates manifest + strings.json
python3 -m script.translations develop                # apply strings.json locally
pytest tests/components/<domain>/test_config_flow.py \
  --cov=homeassistant.components.<domain>.config_flow --cov-report term-missing
# The coverage report must show 100% — P15 is merge-blocking.
```

## Common Anti-patterns

| Wrong | Right |
|---|---|
| `vol.Required(CONF_PASSWORD): str` | password-type `TextSelector` (PS15) |
| `async_create_entry` without touching the library | validate the connection first (P16) |
| `await self.async_set_unique_id(user_input[CONF_HOST])` | serial / `format_mac()` (P7) |
| Empty form redisplayed after an error | `add_suggested_values_to_schema` (PS15) |
| `user_input.get(CONF_HOST)` on a `vol.Required` key | `user_input[CONF_HOST]` (PS2) |
| Error-path test ends asserting `FORM`/`ABORT` | continue the flow to `CREATE_ENTRY` (P15) |
| Reconfigure finishing with `async_create_entry` | `async_update_reload_and_abort` |

## References

For detailed patterns, see:

- `${CLAUDE_SKILL_DIR}/references/flow-anatomy.md` - Reserved steps, discovery, reauth, reconfigure, options, subentries
- `${CLAUDE_SKILL_DIR}/references/schema-and-strings.md` - Selectors, suggested values, data_description, strings.json wiring
- `${CLAUDE_SKILL_DIR}/references/testing-flows.md` - 100% coverage, recovery tests, abort/unique-ID assertions

## Research

Prefer the highest-fidelity source available:

1. **The core checkout itself** (exact APIs for your branch):

   ```bash
   code homeassistant/config_entries.py         # ConfigFlow, OptionsFlow, subentries
   code homeassistant/helpers/selector.py       # every selector + config dataclass
   ```

2. **Reference integrations** — joostlek's recommended exemplars for structure and
   test style: `mealie`, `niko_home_control`, `trmnl`
   (https://github.com/home-assistant/core/pull/174407#discussion_r3559832778).

3. **WebFetch official dev docs** (fallback):

   ```
   WebFetch(url: "https://developers.home-assistant.io/docs/config_entries_config_flow_handler/", prompt: "Extract flow step docs.")
   WebFetch(url: "https://developers.home-assistant.io/docs/data_entry_flow_index/", prompt: "Extract show_form/create_entry/abort docs.")
   ```
