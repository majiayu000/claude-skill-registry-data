---
name: ha:examples
description: Provide examples and walkthroughs for Home Assistant integration, coordinator, config-flow, entity platform, service-action, and Lit (ha-frontend) patterns. Use when "how do I...", "show me an example", or "what does X look like".
effort: low
---

# Examples & Walkthroughs

## Official Guides (Reference)

For standard implementation patterns, always check official guides first:

| Topic | Guide |
|-------|-------|
| Integration manifest | [developers.home-assistant.io/docs/creating_integration_manifest](https://developers.home-assistant.io/docs/creating_integration_manifest) |
| Config entries / setup | [developers.home-assistant.io/docs/config_entries_index](https://developers.home-assistant.io/docs/config_entries_index) |
| Config flow | [developers.home-assistant.io/docs/config_entries_config_flow_handler](https://developers.home-assistant.io/docs/config_entries_config_flow_handler) |
| Fetching data (coordinator) | [developers.home-assistant.io/docs/integration_fetching_data](https://developers.home-assistant.io/docs/integration_fetching_data) |
| Entities | [developers.home-assistant.io/docs/core/entity](https://developers.home-assistant.io/docs/core/entity) |
| Lit (frontend) | [lit.dev/docs](https://lit.dev/docs/) |
| Testing | [developers.home-assistant.io/docs/development_testing](https://developers.home-assistant.io/docs/development_testing) |
| Quality Scale | [developers.home-assistant.io/docs/core/integration-quality-scale](https://developers.home-assistant.io/docs/core/integration-quality-scale) |

## Pattern Categories

If you're asking "how do I..." about one of these, check the matching
skill first — each covers the full depth; below is one representative
snippet per category.

### Integration Setup → `integration-architecture`, `python-idioms`

Config-entry setup, `async_setup_entry`/`async_unload_entry` symmetry, typed
`runtime_data`, platform forwarding.

```python
# __init__.py — config-entry setup with typed runtime_data
type ExampleConfigEntry = ConfigEntry[ExampleCoordinator]

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ExampleConfigEntry) -> bool:
    """Set up Example from a config entry."""
    coordinator = ExampleCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ExampleConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
```

### Lit Patterns → `lit-patterns`, `lit-render-audit`

ha-frontend components: the `hass` object, `hass.localize`, `@lit/task`,
`ha-*` components, `repeat()` for keyed lists.

```typescript
@customElement("ha-example-panel")
export class HaExamplePanel extends LitElement {
  @property({ attribute: false }) public hass!: HomeAssistant;

  @property() public entityId = "";

  private _detailTask = new Task(this, {
    task: async ([entityId], { signal }) => {
      if (!entityId) return undefined;
      return this.hass.callWS({ type: "example/get_detail", entity_id: entityId });
    },
    args: () => [this.entityId],
  });

  protected render() {
    return this._detailTask.render({
      pending: () => html`<ha-circular-progress indeterminate></ha-circular-progress>`,
      complete: (detail) => html`<h2>${detail?.name}</h2>`,
      error: (e) => html`<ha-alert alert-type="error">${String(e)}</ha-alert>`,
    });
  }
}
```

### Coordinator Patterns → `coordinator-patterns`, `setup-failure-debug`, `blocking-io-check`

`DataUpdateCoordinator` anatomy, typed `runtime_data`, entities reading
`coordinator.data`, first refresh. This plugin's coordinator skill covers
**both** poll and push — pick poll (`update_interval`) when the device has no
push channel, push (`async_set_updated_data`) when the library streams updates.

```python
# coordinator.py — poll coordinator
class ExampleCoordinator(DataUpdateCoordinator[ExampleData]):
    def __init__(self, hass: HomeAssistant, entry: ExampleConfigEntry) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=5),
        )
        self.client = entry.runtime_data_client

    async def _async_update_data(self) -> ExampleData:
        try:
            return await self.client.async_get_data()
        except AuthError as err:
            raise ConfigEntryAuthFailed from err
        except ClientError as err:
            raise UpdateFailed(err) from err
```

```python
# coordinator.py — push coordinator (library streams updates)
class ExamplePushCoordinator(DataUpdateCoordinator[ExampleData]):
    async def _async_setup(self) -> None:
        self.client.subscribe(self._handle_push)

    @callback
    def _handle_push(self, data: ExampleData) -> None:
        self.async_set_updated_data(data)
```

### Service Action Patterns → `service-actions`

Registering service actions in `async_setup`, voluptuous schema,
`ServiceValidationError`, idempotency.

```python
# services.py — register a service action
SERVICE_SEND = "send_message"
SEND_SCHEMA = vol.Schema(
    {
        vol.Required("entry_id"): str,
        vol.Required("message"): str,
    }
)


def async_setup_services(hass: HomeAssistant) -> None:
    """Register integration service actions (called from async_setup, P18)."""

    async def async_handle_send(call: ServiceCall) -> None:
        entry = hass.config_entries.async_get_entry(call.data["entry_id"])
        if entry is None or entry.state is not ConfigEntryState.LOADED:
            raise ServiceValidationError("Integration not loaded")
        # idempotent where the device allows: safe to re-issue
        await entry.runtime_data.client.async_send(call.data["message"])

    hass.services.async_register(DOMAIN, SERVICE_SEND, async_handle_send, schema=SEND_SCHEMA)
```

## Plugin-Specific Patterns

Patterns NOT in official guides (unique to this plugin):

### Dev Instance Workflow

```bash
# 1. Set up a dev environment (once)
script/setup

# 2. Run Home Assistant against a throwaway config dir
hass -c config

# 3. Or use the devcontainer / script/develop for the full dev loop
script/develop

# Tail logs for your integration while it runs
tail -f config/home-assistant.log | grep homeassistant.components.example
```

Inspect live state and registries from the running instance via Developer
Tools (States / Template) or the websocket API — see the `dev-instance` skill.

### Multi-Agent Review Workflow

```bash
# 1. Plan feature with specialist agents
/ha:plan Add a cloud integration with OAuth

# 2. After implementation, review with multiple perspectives
/ha:review homeassistant/components/example/coordinator.py  # Python idioms
# config-flow-reviewer runs automatically on config_flow.py changes

# 3. Before submitting
# quality-scale-auditor checks tier readiness
```

### Iron Laws Enforcement

This plugin enforces non-negotiable rules across all agents:

**Python Idioms:**

- NO custom polling loop when a `DataUpdateCoordinator` fits
- Coordinator owns the fetch; entities read `coordinator.data`
- voluptuous schemas + selectors for config-flow input

**Lit (ha-frontend):**

- NEVER fetch data synchronously in the constructor — use `@lit/task`
- ALWAYS use `repeat()` with stable keys for lists
- Use the `hass` object and `hass.localize` — never hardcode user-facing strings

**Service Actions:**

- Validate input with a voluptuous schema; raise `ServiceValidationError` on bad input
- Register in `async_setup`, not `async_setup_entry` (P18)
- Keep handlers idempotent where the device allows

**Security:**

- Validate at boundaries (config-flow input via voluptuous)
- Never log secrets (tokens, passwords); redact them in diagnostics
- No blocking I/O on the event loop (P4)

## Example Workflows

### Bug Investigation

```bash
# 1. Start with obvious checks
/ha:investigate Sensor unavailable after reload

# 2. Agent checks the obvious list:
#    - File saved? mypy clean? hassfest clean?
#    - ConfigEntryNotReady raised (not swallowed) on transient setup failure?
#    - unique_id collision, or entity never added to the platform?
#    - coordinator.data populated (did the first refresh run)?

# 3. If complex, escalate to Ralph Wiggum Loop (if installed)
/ralph-loop:ralph-loop "Fix example tests. Output <promise>DONE</promise> when green."
```

### Feature Planning

```bash
# 1. Research phase
/ha:research DataUpdateCoordinator push vs poll best practices

# 2. Plan with structure analysis
/ha:plan Add a daily summary service action

# 3. Agents coordinate:
#    - pypi-library-researcher evaluates deps
#    - coordinator-specialist designs the update path
#    - entity-model-designer plans the entities
```

### Security Audit

```bash
# 1. Run security analyzer on config-flow code
/ha:review homeassistant/components/example/config_flow.py

# 2. Check for common issues:
#    - Secrets logged, or stored unredacted in entry.data / diagnostics?
#    - Config-flow input validated (voluptuous) before create_entry?
#    - unique_id set to prevent duplicate entries?
#    - Blocking I/O anywhere in the async setup path?
```

## When to Use Official Docs vs Plugin

| Situation | Use |
|-----------|-----|
| "How do I create an integration?" | Official HA developer docs |
| "Is my integration design idiomatic?" | Plugin's `/ha:review` |
| "How do I add a frontend panel?" | Official Lit + frontend docs |
| "Does my Lit component have re-render/memory issues?" | Plugin's Iron Laws (`lit-render-audit`) |
| "How do I reach a quality-scale tier?" | Official quality-scale docs |
| "Is my integration ready for the next tier?" | Plugin's `quality-scale-auditor` |
